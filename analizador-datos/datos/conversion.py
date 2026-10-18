"""Lógica pura (sin Django) de conversión de bases y análisis de caracteres."""
from dataclasses import dataclass

VALOR_MIN = 0
VALOR_MAX = 65_535
MAX_CARACTERES = 20
MAX_LARGO_NUMERO = 64

BASES = {
    2: ("Binaria", "01"),
    8: ("Octal", "01234567"),
    10: ("Decimal", "0123456789"),
    16: ("Hexadecimal", "0123456789abcdefABCDEF"),
}


class ErrorDeEntrada(ValueError):
    """Entrada inválida; el mensaje está pensado para mostrarse al usuario."""


@dataclass(frozen=True)
class ResultadoNumero:
    decimal: int
    binario: str          # completado al siguiente límite de byte
    octal: str
    hexadecimal: str
    bits_significativos: int
    bytes_necesarios: int


@dataclass(frozen=True)
class FilaCaracter:
    caracter: str
    visible: str          # representación legible (p. ej. «espacio»)
    decimal: int
    punto_codigo: str     # U+00F1
    hexadecimal: str      # 0xF1
    bytes_utf8: str       # C3 B1
    cantidad_bytes: int


def validar_y_convertir(texto: str, base: int) -> int:
    """Convierte `texto` desde `base` a entero validando dígitos y rango."""
    if base not in BASES:
        raise ErrorDeEntrada("La base de origen debe ser 2, 8, 10 o 16.")

    nombre, digitos = BASES[base]
    texto = (texto or "").strip()

    if not texto:
        raise ErrorDeEntrada("Escribe un número: el campo no puede estar vacío.")
    if len(texto) > MAX_LARGO_NUMERO:
        raise ErrorDeEntrada(f"El número es demasiado largo (máximo {MAX_LARGO_NUMERO} caracteres).")
    if texto.startswith("-"):
        raise ErrorDeEntrada("No se permiten valores negativos: ingresa un número de 0 en adelante.")

    invalidos = sorted({c for c in texto if c not in digitos})
    if invalidos:
        lista = ", ".join(f"«{c}»" for c in invalidos)
        raise ErrorDeEntrada(
            f"Dígito(s) no válido(s) para base {base} ({nombre.lower()}): {lista}. "
            f"Dígitos permitidos: {', '.join(digitos[:base] if base != 16 else '0123456789ABCDEF')}."
        )

    valor = int(texto, base)
    if not VALOR_MIN <= valor <= VALOR_MAX:
        raise ErrorDeEntrada(
            f"Valor fuera de rango: {valor} no está entre {VALOR_MIN} y {VALOR_MAX:,}.".replace(",", " ")
        )
    return valor


def analizar_numero(texto: str, base: int) -> ResultadoNumero:
    valor = validar_y_convertir(texto, base)
    bits = max(1, valor.bit_length())          # el 0 necesita 1 bit para escribirse
    n_bytes = (bits + 7) // 8
    return ResultadoNumero(
        decimal=valor,
        binario=format(valor, "b").zfill(n_bytes * 8),
        octal=format(valor, "o"),
        hexadecimal=format(valor, "X"),
        bits_significativos=bits,
        bytes_necesarios=n_bytes,
    )


_NOMBRES_ESPECIALES = {" ": "espacio", "\t": "tabulador", "\n": "salto de línea", "\r": "retorno"}


def analizar_texto(texto: str) -> list[FilaCaracter]:
    """Devuelve una fila por carácter (punto de código Unicode)."""
    if texto is None or texto == "":
        raise ErrorDeEntrada("Escribe un texto: el campo no puede estar vacío.")
    if len(texto) > MAX_CARACTERES:
        raise ErrorDeEntrada(
            f"El texto tiene {len(texto)} caracteres; el máximo permitido es {MAX_CARACTERES}."
        )

    filas = []
    for c in texto:
        codigo = ord(c)
        codificado = c.encode("utf-8")
        filas.append(
            FilaCaracter(
                caracter=c,
                visible=_NOMBRES_ESPECIALES.get(c, c),
                decimal=codigo,
                punto_codigo=f"U+{codigo:04X}",
                hexadecimal=f"0x{codigo:X}",
                bytes_utf8=" ".join(f"{b:02X}" for b in codificado),
                cantidad_bytes=len(codificado),
            )
        )
    return filas

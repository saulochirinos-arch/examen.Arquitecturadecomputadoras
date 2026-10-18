from django.test import SimpleTestCase

from datos.conversion import ErrorDeEntrada, analizar_numero, analizar_texto, validar_y_convertir


class ConversionesValidas(SimpleTestCase):
    def test_decimal_255_cabe_en_un_byte(self):
        r = analizar_numero("255", 10)
        self.assertEqual((r.binario, r.octal, r.hexadecimal), ("11111111", "377", "FF"))
        self.assertEqual((r.bits_significativos, r.bytes_necesarios), (8, 1))

    def test_binario_se_completa_al_siguiente_byte(self):
        r = analizar_numero("256", 10)
        self.assertEqual(r.binario, "0000000100000000")  # 16 bits
        self.assertEqual((r.bits_significativos, r.bytes_necesarios), (9, 2))

    def test_desde_binario_octal_y_hexadecimal(self):
        self.assertEqual(analizar_numero("101010", 2).decimal, 42)
        self.assertEqual(analizar_numero("777", 8).decimal, 511)
        self.assertEqual(analizar_numero("ff", 16).decimal, 255)   # minúsculas aceptadas
        self.assertEqual(analizar_numero("71D", 16).decimal, 1821)

    def test_limites_del_rango(self):
        self.assertEqual(analizar_numero("0", 10).binario, "00000000")
        maximo = analizar_numero("FFFF", 16)
        self.assertEqual(maximo.decimal, 65535)
        self.assertEqual(maximo.binario, "1" * 16)
        self.assertEqual(maximo.bytes_necesarios, 2)

    def test_el_relleno_binario_siempre_es_multiplo_de_8(self):
        for n in (1, 127, 128, 4095, 65535):
            self.assertEqual(len(analizar_numero(str(n), 10).binario) % 8, 0)


class ErroresDeValidacion(SimpleTestCase):
    def test_digito_invalido_para_la_base(self):
        with self.assertRaisesMessage(ErrorDeEntrada, "base 2"):
            validar_y_convertir("102", 2)
        with self.assertRaisesMessage(ErrorDeEntrada, "base 8"):
            validar_y_convertir("89", 8)
        with self.assertRaisesMessage(ErrorDeEntrada, "base 16"):
            validar_y_convertir("1G", 16)

    def test_fuera_de_rango(self):
        with self.assertRaisesMessage(ErrorDeEntrada, "fuera de rango"):
            validar_y_convertir("65536", 10)
        with self.assertRaisesMessage(ErrorDeEntrada, "fuera de rango"):
            validar_y_convertir("10000", 16)

    def test_negativo_y_vacio(self):
        with self.assertRaisesMessage(ErrorDeEntrada, "negativos"):
            validar_y_convertir("-5", 10)
        with self.assertRaisesMessage(ErrorDeEntrada, "vacío"):
            validar_y_convertir("   ", 10)

    def test_no_acepta_prefijos_ni_separadores(self):
        for malo in ("0x1F", "1_000", "+5", "1.5", "٣"):
            with self.assertRaises(ErrorDeEntrada, msg=malo):
                validar_y_convertir(malo, 16 if malo == "0x1F" else 10)


class TextoUtf8(SimpleTestCase):
    def test_enie_ocupa_dos_bytes_utf8(self):
        (fila,) = analizar_texto("ñ")
        self.assertEqual(fila.decimal, 241)
        self.assertEqual(fila.punto_codigo, "U+00F1")
        self.assertEqual(fila.hexadecimal, "0xF1")
        self.assertEqual(fila.bytes_utf8, "C3 B1")
        self.assertEqual(fila.cantidad_bytes, 2)

    def test_ascii_ocupa_un_byte(self):
        (fila,) = analizar_texto("A")
        self.assertEqual((fila.decimal, fila.punto_codigo, fila.bytes_utf8), (65, "U+0041", "41"))

    def test_limite_de_20_caracteres(self):
        self.assertEqual(len(analizar_texto("a" * 20)), 20)
        with self.assertRaisesMessage(ErrorDeEntrada, "máximo permitido es 20"):
            analizar_texto("a" * 21)

    def test_texto_vacio(self):
        with self.assertRaisesMessage(ErrorDeEntrada, "vacío"):
            analizar_texto("")

    def test_emoji_usa_cuatro_bytes(self):
        (fila,) = analizar_texto("😀")
        self.assertEqual((fila.punto_codigo, fila.bytes_utf8), ("U+1F600", "F0 9F 98 80"))

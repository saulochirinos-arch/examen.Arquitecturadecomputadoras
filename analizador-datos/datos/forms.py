from django import forms

from .conversion import (
    BASES,
    MAX_CARACTERES,
    MAX_LARGO_NUMERO,
    ErrorDeEntrada,
    analizar_numero,
    analizar_texto,
)


class NumeroForm(forms.Form):
    numero = forms.CharField(
        label="Número",
        strip=False,
        error_messages={"required": "Escribe un número: el campo no puede estar vacío."},
        widget=forms.TextInput(attrs={"placeholder": "Ej.: 1821", "autocomplete": "off", "spellcheck": "false"}),
    )
    base = forms.TypedChoiceField(
        label="Base de origen",
        choices=[(b, f"{b} · {nombre}") for b, (nombre, _) in BASES.items()],
        coerce=int,
        initial=10,
        error_messages={"invalid_choice": "Selecciona una base válida: 2, 8, 10 o 16.",
                        "required": "Selecciona la base de origen."},
    )

    def clean(self):
        datos = super().clean()
        if "numero" in datos and "base" in datos:
            try:
                datos["resultado"] = analizar_numero(datos["numero"], datos["base"])
            except ErrorDeEntrada as e:
                self.add_error("numero", str(e))
        return datos


class TextoForm(forms.Form):
    texto = forms.CharField(
        label=f"Texto (máximo {MAX_CARACTERES} caracteres)",
        strip=False,
        error_messages={"required": "Escribe un texto: el campo no puede estar vacío."},
        widget=forms.TextInput(attrs={"placeholder": "Ej.: Comayagüela", "autocomplete": "off", "spellcheck": "false"}),
    )

    def clean(self):
        datos = super().clean()
        if "texto" in datos:
            try:
                datos["filas"] = analizar_texto(datos["texto"])
            except ErrorDeEntrada as e:
                self.add_error("texto", str(e))
        return datos

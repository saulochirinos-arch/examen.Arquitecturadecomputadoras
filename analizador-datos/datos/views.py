from django.shortcuts import render

from .forms import NumeroForm, TextoForm


def index(request):
    """Una sola página con dos formularios independientes (se distinguen por `accion`)."""
    accion = request.POST.get("accion") if request.method == "POST" else None

    form_numero = NumeroForm(request.POST, prefix="n") if accion == "numero" else NumeroForm(prefix="n")
    form_texto = TextoForm(request.POST, prefix="t") if accion == "texto" else TextoForm(prefix="t")

    contexto = {"form_numero": form_numero, "form_texto": form_texto, "accion": accion}
    if accion == "numero" and form_numero.is_valid():
        contexto["resultado"] = form_numero.cleaned_data["resultado"]
    if accion == "texto" and form_texto.is_valid():
        contexto["filas"] = form_texto.cleaned_data["filas"]

    return render(request, "datos/index.html", contexto)

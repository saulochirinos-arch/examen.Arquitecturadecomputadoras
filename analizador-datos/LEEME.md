# Analizador de representación de datos

App web en Python 3.12 + Django 5.2 (sin base de datos).

## Usar (un clic)

- **Windows:** doble clic en `iniciar.bat`
- **Linux / macOS:** `./iniciar.sh`

Se instala Django, se inicia el servidor y se abre <http://127.0.0.1:8000>.

> **Importante:** no abras `datos/templates/datos/index.html` con doble clic. Es un template de Django (tiene `{% ... %}`) y solo se ve bien cuando lo sirve el servidor.

## Pruebas (19)

```bash
# con el entorno activado (.venv\Scripts\activate en Windows, source .venv/bin/activate en Linux/macOS)
python manage.py test
```

## Qué incluye

- **Formulario 1:** número + base (2, 8, 10, 16). Valida dígitos y rango 0–65 535; muestra decimal, binario (completado a 8, 16… bits), octal, hexadecimal, bits significativos y bytes.
- **Formulario 2:** texto de hasta 20 caracteres; por carácter muestra decimal, `U+`, hexadecimal y bytes UTF-8.
- **Errores claros:** vacío, dígito inválido para la base, negativo, fuera de rango y texto demasiado largo.

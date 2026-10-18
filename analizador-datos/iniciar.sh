#!/usr/bin/env bash
# Linux / macOS: crea el entorno, instala Django y abre la app en el navegador.
set -e
cd "$(dirname "$0")"
PORT="${PORT:-8000}"

for c in python3.12 python3 python; do
  if command -v "$c" >/dev/null 2>&1; then PY="$c"; break; fi
done
[ -z "$PY" ] && { echo "No se encontró Python. Instala Python 3.12."; exit 1; }

[ -d .venv ] || "$PY" -m venv .venv
. .venv/bin/activate
python -m pip install -q -r requirements.txt

export DEBUG=1
URL="http://127.0.0.1:$PORT"
echo "Abre $URL en el navegador (Ctrl+C para detener)."
if [ -z "$NO_BROWSER" ]; then
  ( sleep 2; (xdg-open "$URL" || open "$URL") >/dev/null 2>&1 ) &
fi
exec python manage.py runserver "127.0.0.1:$PORT"

@echo off
chcp 65001 >nul
cd /d "%~dp0"

py -3.12 --version >nul 2>nul && (set "PY=py -3.12") || (set "PY=python")
%PY% --version >nul 2>nul || (echo No se encontro Python. Instala Python 3.12 desde python.org y marca "Add to PATH". & pause & exit /b 1)

if not exist .venv\Scripts\python.exe %PY% -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install -q -r requirements.txt

set DEBUG=1
echo Abriendo http://127.0.0.1:8000  (Ctrl+C para detener)
start "" /b cmd /c "timeout /t 3 /nobreak >nul && start http://127.0.0.1:8000"
python manage.py runserver 127.0.0.1:8000
pause

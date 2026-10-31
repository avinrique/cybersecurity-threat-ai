@echo off
rem Start Vigil with one command: sets up Python packages on first run, then opens the web page
cd /d "%~dp0"

if not exist venv (
  echo First run: setting up, takes a minute...
  python -m venv venv
)
venv\Scripts\python -m pip install --quiet --disable-pip-version-check -r requirements.txt

if "%PORT%"=="" set PORT=5077
echo Vigil is running at http://127.0.0.1:%PORT% - press Ctrl+C to stop
start "" /b powershell -NoProfile -Command "Start-Sleep 4; Start-Process 'http://127.0.0.1:%PORT%'"
venv\Scripts\python src\deploy.py

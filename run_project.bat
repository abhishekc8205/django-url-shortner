@echo off
setlocal

REM One-click startup for this Django project.
REM It creates .venv, activates it, installs packages, migrates the database,
REM and starts the local development server.

cd /d "%~dp0"

where py >nul 2>nul
if errorlevel 1 (
    echo Python was not found. Install Python 3, then run this file again.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    py -3 -m venv .venv
    if errorlevel 1 goto :error
)

call ".venv\Scripts\activate.bat"
if errorlevel 1 goto :error

echo Installing required packages...
python -m pip install --upgrade pip
if errorlevel 1 goto :error
python -m pip install -r requirements.txt
if errorlevel 1 goto :error

if not exist ".env" (
    echo Creating local .env file from .env.example...
    copy /y ".env.example" ".env" >nul
    if errorlevel 1 goto :error
)

echo Updating the database...
python manage.py migrate
if errorlevel 1 goto :error

echo.
echo Server is starting at http://127.0.0.1:8000/
echo Press Ctrl+C to stop the server.
python manage.py runserver
exit /b %errorlevel%

:error
echo.
echo Setup stopped because a command failed.
pause
exit /b 1

@echo off
REM Voice Assistant Quick Start Script for Windows

echo ================================
echo Voice Assistant Setup Script
echo ================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo Found: %PYTHON_VERSION%
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo Dependencies installed
echo.

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo Warning: Please edit .env and add your Google Gemini API key
    echo    Get your key from: https://aistudio.google.com/apikey
    echo.
    pause
)

REM Create necessary directories
echo Creating necessary directories...
if not exist "static\css" mkdir static\css
if not exist "static\js" mkdir static\js
if not exist "templates" mkdir templates
if not exist "logs" mkdir logs
echo Directories created
echo.

REM Run the application
echo Starting the voice assistant...
echo    Access it at: http://localhost:8080
echo.
echo Press Ctrl+C to stop the server
echo.
python -m src.app
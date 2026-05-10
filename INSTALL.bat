@echo off
:: NOVA v6 First-time Setup Script
:: Sets up virtual environments and installs dependencies

echo ==============================================
echo           NOVA v6 Installation Setup
echo ==============================================

:: Change to the directory where the script is located
cd /d "%~dp0"

echo [INFO] Creating Python virtual environment in 'server\venv'...
python -m venv server\venv

if not exist "server\venv\Scripts\pip.exe" (
    echo [ERROR] Failed to create virtual environment. Ensure python is in your PATH.
    pause
    exit /b
)

echo [INFO] Upgrading pip...
server\venv\Scripts\python.exe -m pip install --upgrade pip

echo [INFO] Installing server dependencies...
server\venv\Scripts\pip.exe install -r server\requirements_server.txt

echo [INFO] Installing client dependencies...
server\venv\Scripts\pip.exe install -r server\requirements_client.txt

echo [INFO] Installing Python-docx for generating architecture documents...
server\venv\Scripts\pip.exe install python-docx

echo ==============================================
echo [SUCCESS] NOVA setup complete!
echo You can now double-click 'START_NOVA.bat' to launch the system.
echo ==============================================
pause
exit

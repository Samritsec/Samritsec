@echo off
:: NOVA v6 Startup Script
:: Double-click to launch everything (Server + Client)

echo ==============================================
echo           Starting NOVA v6 AGI Engine
echo ==============================================

:: Change to the directory where the script is located
cd /d "%~dp0"

:: Check if server virtual environment exists
if not exist "server\venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found. Please run INSTALL.bat first.
    pause
    exit /b
)

:: Change directly into the server directory so paths are simple
cd /d "%~dp0server"

:: Perform a quick health check to see if critical packages are installed
venv\Scripts\python.exe -c "import jwt, customtkinter" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Required libraries are missing. The virtual environment is incomplete.
    echo Please run INSTALL.bat again and ensure it finishes without errors.
    pause
    exit /b
)

:: Start the FastAPI Server in a new window
echo [INFO] Launching NOVA Server...
start "NOVA Server" cmd /k "venv\Scripts\python.exe server_v6.py"

:: Give the server a few seconds to initialize
timeout /t 3 /nobreak > nul

:: Start the CustomTkinter Client in a new window
echo [INFO] Launching NOVA Client UI...
start "NOVA Client" cmd /k "venv\Scripts\python.exe nova_client.py"

:: Optionally start the floating toggle
echo [INFO] Launching NOVA Floating Toggle...
start "NOVA Toggle" cmd /k "venv\Scripts\python.exe nova_floating_toggle.py"

echo.
echo [SUCCESS] NOVA has been launched.
echo You can safely close this window.
exit

#!/usr/bin/env bash
echo "=============================================="
echo "          NOVA v1 Installation Setup          "
echo "=============================================="

cd "$(dirname "$0")/.."

echo "[INFO] Checking for Python 3..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 could not be found. Please install python3."
else
    echo "[INFO] Creating Python virtual environment in 'venv'..."
    python3 -m venv venv

    echo "[INFO] Upgrading pip..."
    ./venv/bin/python3 -m pip install --upgrade pip

    echo "[INFO] Installing dependencies..."
    ./venv/bin/python3 -m pip install -r requirements.txt

    chmod +x main.py
    chmod +x scripts/start.sh

    echo "=============================================="
    echo "[SUCCESS] NOVA setup complete!"
    echo "You can now run './scripts/start.sh' to launch the ecosystem."
    echo "=============================================="
fi

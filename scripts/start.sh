#!/usr/bin/env bash
echo "=============================================="
echo "          Starting NOVA v1 Ecosystem          "
echo "=============================================="

cd "$(dirname "$0")/.."

if [ ! -f "venv/bin/python3" ]; then
    echo "[ERROR] Virtual environment not found. Please run ./scripts/install.sh first."
else
    echo "[INFO] Launching NOVA..."
    ./venv/bin/python3 main.py
fi

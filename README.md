# NOVA v1
**Linux-First AI Workstation Ecosystem**

NOVA is a modular, user-friendly desktop shell and AI orchestrator. It is built natively for Linux, serving as a powerful assistant overlaid with offensive/defensive security tools, developer workspaces, and sandboxed autonomy.

## Project Goal
To create a strictly controlled but highly capable AI environment that can:
- Assist in daily workflow via a modern GUI.
- Plan and execute complex tasks safely.
- Utilize modular tool packs.
- Maintain an encrypted, persistent memory state.

## Current State
This repository has been reset. The old Windows-based legacy architecture has been completely purged. We are currently implementing the foundational architecture and GUI shell.

Please see `ARCHITECTURE.md` for the foundational decisions regarding Linux distribution targets, hardware requirements, permission matrices, and security models.

## Setup Instructions

NOVA is built natively for Linux. Ensure you have `python3` and `python3-venv` installed on your system.

1. **Install dependencies:**
   ```bash
   ./scripts/install.sh
   ```
   *This will create a virtual environment (`venv`) and install PyQt6, PyYAML, and Cryptography.*

2. **Launch the application:**
   ```bash
   ./scripts/start.sh
   ```

## Structure
- `core/`: The heart of NOVA (Orchestrator, Memory, Security, Config).
- `gui/`: The Linux-native PyQt6 graphical user interface.
- `tools/`: The modular capability system (Offensive, Defensive, Developer).
- `scripts/`: Deployment and maintenance utilities (`install.sh`, `start.sh`).

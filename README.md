# NOVA v6 CAPSULE

Welcome to **NOVA**, a Jarvis-inspired autonomous personal AI agent for Windows PC.

NOVA is a 3-tier intelligence routing orchestrator with an encrypted local memory system. It offers a sleek, dark-themed CustomTkinter UI client and a floating toggle desktop widget for quick access.

## Features

- **3-Tier Intelligence Routing Orchestrator**: Uses different tiers of processing for fast, standard, and deep thought tasks.
- **Encrypted Local Memory**: Uses SQLite and Fernet for secure, private local storage.
- **Floating Toggle Widget**: A frameless, always-on-top desktop widget for quick launching.
- **FastAPI Backend**: Robust backend with WebSocket support and JWT authentication.
- **Thread-safe CustomTkinter UI**: Sleek, responsive, and robust desktop UI.

## Getting Started

1. **Install Dependencies**: Double-click `INSTALL.bat` to create a virtual environment and install all requirements.
2. **Launch NOVA**: Double-click `START_NOVA.bat` to launch the server, the desktop client, and the floating toggle widget.

## Structure

- `server/`: Contains the FastAPI server, agent logic, local memory (brain), and UI clients.
- `server/server_v6.py`: The FastAPI backend with WebSockets.
- `server/nova_client.py`: The CustomTkinter desktop UI.
- `server/nova_floating_toggle.py`: The quick-launch floating desktop widget.
- `server/agents/orchestrator.py`: The intelligence routing logic.
- `server/brain/nova_core.py`: Encrypted local memory system.

## Documentation

- `CAPSULE_NOTES.md`: Bug lists and sprint roadmap.
- `NOVA_v6_Architecture.docx`: System architecture details.
- `NOVA_AGI_Blueprint.docx`: AGI engine blueprints.
- `NOVA_Cost_Breakdown.docx`: Hardware and cost breakdown for deployment.

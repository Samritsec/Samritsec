# NOVA v1 Linux Ecosystem Architecture

## Primary Objective
NOVA is a Linux-first AI workstation ecosystem. It acts as an autonomous, user-friendly desktop shell overlaid with advanced defensive and offensive security tool packs, a developer workspace, and a deeply integrated AI orchestrator capable of planning and executing tasks safely.

## Proposed Decisions for Missing Items

Before writing functional code, the following decisions have been mapped out to address the missing items from the project spec. These form the foundation of Phase 1.

### 1. Target Linux Distro/Base
*   **Recommendation:** **Debian/Ubuntu-based (e.g., Kali Linux or Parrot OS) OR Arch Linux (BlackArch).**
*   **Rationale:** Since NOVA focuses heavily on offensive and defensive security tools, building on top of Kali/Parrot provides immediate access to thousands of pre-configured tools via standard repos. Ubuntu LTS is a fallback for max stability.

### 2. Hardware Requirements
*   **Minimum:** 16GB RAM, 4-core CPU, 50GB storage. (Suitable for running smaller 3B-7B models quantized, plus the GUI).
*   **Recommended:** 32GB RAM, 8-core CPU, Dedicated GPU (NVIDIA RTX 3060 or higher with 8GB+ VRAM), 100GB NVMe SSD. (Suitable for 8B-14B models natively, rapid code compilation, and sandbox virtualization).

### 3. Package Manager Strategy
*   **System Packages:** `apt` (Debian) or `pacman` (Arch) for OS-level dependencies.
*   **Python Dependencies:** `uv` or `poetry` for isolated, reproducible virtual environments.
*   **NOVA Plugin Manager:** A custom built-in package manager (`nova-pm`) that downloads and verifies signed ZIP/Tarballs containing tools and AI skills.

### 4. Model Hosting Strategy
*   **Primary:** Local **Ollama** engine running as a systemd service.
*   **Models:** `llama3.1:8b` (General logic/planning), `llava` (Vision/Eyes), `nomic-embed-text` (Vector embeddings for memory).
*   **Audio:** Local Whisper (`openai-whisper`) for STT; `piper` or `Coqui TTS` for high-quality Linux TTS (replacing the clunky Windows `pyttsx3`).

### 5. Permission Matrix
*   **Tier 0 (Unrestricted):** Basic conversation, local deep-dive research, querying non-sensitive APIs, reading public repos.
*   **Tier 1 (Notify & Log):** Creating files in the user workspace, launching sandboxed tools, scraping web targets.
*   **Tier 2 (Explicit Approval Required):** Deleting files, modifying system configs (`/etc/`), installing OS packages, executing offensive network attacks (`nmap`, `metasploit`), updating the AI's core codebase.

### 6. Backup and Restore Plan
*   **User Data & Memory:** Daily automated snapshots using `rsync` or `timeshift` stored in `~/.nova/backups`.
*   **Database:** SQLite memory databases will be duplicated before any schema migration.
*   **Rollback:** The GUI will feature a "Time Machine" module to revert to the last stable configuration if an AI self-modification breaks the system.

### 7. Logging Policy
*   **Audit Logs:** Every tool execution and system command must be logged to a secured SQLite database or `/var/log/nova/audit.log` (if running as root/service).
*   **Format:** Timestamp, Caller (User vs AI), Action Type, Target, Approval Status.

### 8. Plugin Signing/Review Workflow
*   **Format:** Plugins are strictly defined using a `.nova-plugin` manifest (JSON/YAML) alongside Python execution scripts.
*   **Review:** The Orchestrator AI will statically analyze the plugin code for destructive patterns. The user must review a summary report and explicitly click "Approve and Install" in the GUI.

### 9. Update Mechanism
*   **Core:** Git-based pulls from the verified upstream repository, wrapped in a rollback safety script.
*   **Self-Healing:** If an update fails, the `systemd` daemon falls back to the `.bak` directory.

### 10. Offline/Online Operation Modes
*   **Offline Mode:** Default. Relies on Ollama, local ChromaDB vector stores, and local tool packs.
*   **Online Mode:** Activated per-session. Allows the AI to use `Playwright` to surf the web, scrape OSINT data, or interact with external APIs (GitHub, Shodan).

---

## Directory Scaffold for Phase 1

The minimal starting structure avoids monoliths and embraces isolated domains:

```text
nova/
├── core/                   # The heart of NOVA
│   ├── orchestrator/       # AI planning and routing
│   ├── memory/             # RAG, SQLite history, and encrypted storage
│   ├── security/           # Permission matrix and sandboxing logic
│   └── config/             # YAML/JSON config loaders
├── gui/                    # Linux-native desktop shell
│   ├── dashboard/          # Main status and monitoring views
│   ├── chat/               # Interaction interface
│   └── components/         # Reusable widgets
├── tools/                  # The modular toolpack system
│   ├── offensive/          # OSINT, scanners, exploits
│   ├── defensive/          # Log analyzers, monitors
│   └── developer/          # Code helpers, script generators
├── scripts/                # Install, update, and backup scripts
├── tests/                  # Pytest suite
└── main.py                 # Minimal application entry point
```

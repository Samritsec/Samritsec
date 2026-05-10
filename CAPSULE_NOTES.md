# CAPSULE NOTES: Bug List & Sprint Roadmap

## Sprint Roadmap (NOVA v6)

### Sprint 1: Foundation (Completed)
- [x] FastAPI backend with WebSockets and JWT Authentication (`server_v6.py`).
- [x] 3-tier intelligence routing orchestrator (`agents/orchestrator.py`).
- [x] Encrypted local memory with SQLite/Fernet (`brain/nova_core.py`).
- [x] Basic CustomTkinter client interface.

### Sprint 2: UI & Stability (Completed)
- [x] Resolve thread-safety issues in `nova_client.py` (background asyncio vs Tkinter main thread).
- [x] Implement sleek dark theme.
- [x] Add auto-scroll and status indicators.

### Sprint 3: The Capsule Request (In Progress)
- [x] Create `NOVA_v6_CAPSULE/` structure.
- [x] Floating toggle widget (`nova_floating_toggle.py`) with neon logo.
- [x] Root level `START_NOVA.bat` and `INSTALL.bat`.
- [x] Root level documentations (`README.md`, `CAPSULE_NOTES.md`).
- [ ] Structural/architecture `.docx` generation.
- [ ] Finalize `requirements_server.txt` and `requirements_client.txt`.

### Sprint 4: Advanced AGI capabilities (Upcoming)
- [ ] Hook in live LLM keys into the 3-tier system.
- [ ] Implement Playwright autonomous web-browsing agent.
- [ ] Expand ChromaDB vector knowledge base.

---

## Known Bugs & Issues

1. **Bug**: Tkinter exception `RuntimeError: main thread is not in main loop` when background asyncio tasks update the UI.
   - **Status**: **RESOLVED** in Sprint 2 by utilizing `self.after()` for all UI updates from async threads.
2. **Bug**: Initial missing modules (e.g. `pynput`, `chromadb`, etc.) preventing server start.
   - **Status**: **RESOLVED** by expanding `requirements_server.txt` and `requirements_client.txt` in Sprint 3.
3. **Issue**: Floating toggle transparency might render as black on some non-Windows OS.
   - **Status**: OPEN. Noted as primarily targeted for Windows environments.

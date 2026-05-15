# NOVA v1
**Linux-First AI Workstation Ecosystem**

NOVA is a modular, user-friendly desktop shell and AI orchestrator. It is built natively for Linux, serving as a powerful assistant overlaid with offensive/defensive security tools, developer workspaces, and sandboxed autonomy.

## Project Goal
To create a strictly controlled but highly capable AI environment that can:
- Assist in daily workflow via a modern GUI.
- Plan and execute complex tasks safely.
- Utilize modular tool packs.
- Maintain an encrypted, persistent memory state.

## Current State: Phase 1
This repository has been reset to Phase 1. The old Windows-based legacy architecture has been completely purged.

Please see `ARCHITECTURE.md` for the foundational decisions regarding Linux distribution targets, hardware requirements, permission matrices, and security models.

## Structure
- `core/`: The heart of NOVA (Orchestrator, Memory, Security, Config).
- `gui/`: The Linux-native graphical user interface.
- `tools/`: The modular capability system (Offensive, Defensive, Developer).
- `scripts/`: Deployment and maintenance utilities.

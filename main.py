#!/usr/bin/env python3
import sys
from PyQt6.QtWidgets import QApplication

from core.config.loader import ConfigLoader
from gui.main_window import NovaMainWindow
from gui.dashboard.views import PlaceholderView

def main():
    print("NOVA v1 Ecosystem Initializing...")

    # 1. Load configuration
    try:
        config = ConfigLoader.load()
        print(f"Configuration loaded. Environment: {config.get('system', {}).get('environment')}")
    except Exception as e:
        print(f"Failed to load configuration: {e}")
        sys.exit(1)

    # 2. Boot Application
    app = QApplication(sys.argv)
    app.setStyle("Fusion") # Native-looking cross-desktop style

    main_window = NovaMainWindow(ConfigLoader)

    # 3. Register placeholder views mapping to the sidebar indices
    views = [
        PlaceholderView("Dashboard", "System overview, active connections, and resource usage."),
        PlaceholderView("Assistant Chat", "AI conversational interface for tasks and code generation."),
        PlaceholderView("Security Tools", "Launchpad for offensive (nmap, metasploit) and defensive tools."),
        PlaceholderView("Memory & Knowledge", "Vector DB embeddings and SQLite conversational history."),
        PlaceholderView("Audit Logs", "Tamper-evident logs of all system commands executed by AI."),
        PlaceholderView("Settings", "Configure models, plugin directories, and permissions.")
    ]

    for view in views:
        main_window.add_view(view)

    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

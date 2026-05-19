from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QLabel, QFrame
)
from PyQt6.QtCore import Qt

class NovaMainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setWindowTitle("NOVA v1 - AI Workstation")
        self.setMinimumSize(1200, 800)
        self._setup_ui()
        self._apply_theme()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(15)

        # App Logo/Title
        title_lbl = QLabel("NOVA OS")
        title_lbl.setObjectName("TitleLabel")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(title_lbl)

        # Stacked Widget for holding different views
        self.stack = QStackedWidget()

        # Add navigation buttons and hook them to the stack
        self.nav_buttons = {}
        self._add_nav_item("Dashboard", sidebar_layout, 0)
        self._add_nav_item("Assistant Chat", sidebar_layout, 1)
        self._add_nav_item("Security Tools", sidebar_layout, 2)
        self._add_nav_item("Memory & Knowledge", sidebar_layout, 3)
        self._add_nav_item("Audit Logs", sidebar_layout, 4)
        self._add_nav_item("Settings", sidebar_layout, 5)

        sidebar_layout.addStretch()

        # Environment Label
        env_lbl = QLabel(f"Env: {self.config.get('system', 'environment', 'unknown')}")
        env_lbl.setObjectName("EnvLabel")
        env_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(env_lbl)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack, stretch=1)

    def _add_nav_item(self, text, layout, index):
        btn = QPushButton(text)
        btn.setObjectName("NavButton")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(lambda _, idx=index: self.stack.setCurrentIndex(idx))
        layout.addWidget(btn)
        self.nav_buttons[text] = btn

    def add_view(self, view_widget):
        """Adds a widget to the main content stack."""
        self.stack.addWidget(view_widget)

    def _apply_theme(self):
        # A deep, modern Linux/Hacker-themed stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0d1117;
            }
            #Sidebar {
                background-color: #161b22;
                border-right: 1px solid #30363d;
            }
            #TitleLabel {
                color: #58a6ff;
                font-size: 24px;
                font-weight: bold;
                letter-spacing: 2px;
                margin-bottom: 20px;
            }
            #EnvLabel {
                color: #8b949e;
                font-size: 10px;
            }
            #NavButton {
                background-color: transparent;
                color: #c9d1d9;
                text-align: left;
                padding: 10px 15px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            #NavButton:hover {
                background-color: #21262d;
                color: #ffffff;
            }
            QLabel {
                color: #c9d1d9;
            }
        """)

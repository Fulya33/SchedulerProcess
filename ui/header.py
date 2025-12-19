"""Header Component"""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from themes.theme_manager import ThemeManager


class HeaderWidget(QWidget):
    """Application Header"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dark_mode = True
        self.init_ui()
    
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 8, 20, 20)
        layout.setSpacing(14)

        self.title_label = QLabel('CPU Scheduler')
        self.title_label.setStyleSheet("font-size: 38px; font-weight: 900; letter-spacing: -0.5px;")
        layout.addWidget(self.title_label)

        self.subtitle_label = QLabel('Process Scheduling Simulator')
        self.subtitle_label.setStyleSheet('font-size: 15px; color: #64748b; margin-left: 20px;')
        layout.addWidget(self.subtitle_label)

        layout.addStretch()

        self.export_btn = QPushButton('📄 Export PDF')
        self.export_btn.setObjectName('secondary')
        layout.addWidget(self.export_btn)

        self.dark_mode_btn = QPushButton('☀️ Light')
        self.dark_mode_btn.setObjectName('secondary')
        layout.addWidget(self.dark_mode_btn)
    
    def apply_style(self, dark_mode):
        """Apply theme styles"""
        self.dark_mode = dark_mode
        self.setStyleSheet(ThemeManager.get_header_style(dark_mode))
        
        title_color = ThemeManager.get_text_color(dark_mode, "title")
        sub_color = ThemeManager.get_text_color(dark_mode, "subtitle")
        
        self.title_label.setStyleSheet(
            f"font-size: 38px; font-weight: 900; letter-spacing: -0.5px; color: {title_color};"
        )
        self.subtitle_label.setStyleSheet(
            f"font-size: 15px; color: {sub_color}; margin-left: 20px;"
        )
        
        if dark_mode:
            self.dark_mode_btn.setText('☀️ Light')
        else:
            self.dark_mode_btn.setText('🌙 Dark')


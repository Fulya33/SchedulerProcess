"""Theme Management for the Application"""


class ThemeManager:
    """Manages application themes (Light/Dark)"""
    
    @staticmethod
    def get_light_theme():
        """Returns light theme stylesheet"""
        return """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f1f5f9, stop:1 #ffffff);
            }
            QLabel { color: #1e293b; }

            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #1d4ed8; }

            QPushButton#secondary {
                background-color: #e2e8f0;
                color: #0f172a !important;
                border: 1px solid #cbd5e1;
            }
            QPushButton#secondary:hover {
                background-color: #dbeafe;
                border-color: #93c5fd;
                color: #0f172a !important;
            }
            QPushButton#secondary:pressed {
                background-color: #cbd5e1;
                color: #0f172a !important;
            }

            QPushButton#success {
                background-color: #d1fae5;
                color: #065f46 !important;
                border: 1px solid #6ee7b7;
                padding: 14px 28px;
                font-size: 16px;
            }
            QPushButton#success:hover { 
                background-color: #a7f3d0; 
                border-color: #34d399;
                color: #065f46 !important;
            }
            QPushButton#success:pressed {
                background-color: #6ee7b7;
                color: #064e3b !important;
            }

            QPushButton#destructive {
                background-color: transparent;
                color: #ef4444 !important;
                border: 2px solid #ef4444;
            }
            QPushButton#destructive:hover { 
                background-color: #fef2f2; 
                color: #ef4444 !important;
            }
            QPushButton#destructive:pressed {
                background-color: #fee2e2;
                color: #dc2626 !important;
            }

            QLineEdit, QSpinBox {
                padding: 12px 16px;
                border: 2px solid #e5e7eb;
                border-radius: 10px;
                background-color: white;
                color: #1e293b;
                font-size: 14px;
            }
            QLineEdit:focus, QSpinBox:focus { border-color: #2563eb; }

            QTabWidget::pane {
                border: none;
                background: transparent;
            }
            QTabWidget {
                background: transparent;
            }
            QTabBar {
                background: #f1f5f9;
                spacing: 4px;
            }
            QTabBar::tab {
                height: 44px;
                padding: 12px 24px;
                margin-right: 8px;
                border: none;
                border-radius: 12px;
                background: transparent;
                color: #64748b;
                font-size: 14px;
                font-weight: 600;
            }
            QTabBar::tab:selected {
                background: #eef2ff;
                color: #2563eb;
            }
            QTabBar::tab:hover {
                background: #f8fafc;
                color: #2563eb;
            }

            QTableWidget {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 10px;
                gridline-color: #f1f5f9;
                color: #1e293b;
                font-size: 13px;
                selection-background-color: #dbeafe;
                selection-color: #1e293b;
            }
            QTableWidget::item { padding: 8px; }
            QTableWidget::item:alternate { background-color: #f8fafc; }

            QHeaderView::section {
                background-color: #f8fafc;
                color: #1e293b;
                border: none;
                border-bottom: 2px solid #2563eb;
                padding: 14px;
                font-weight: 700;
                font-size: 13px;
            }

            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical {
                border: none;
                background: #f1f5f9;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover { background: #94a3af; }
        """
    
    @staticmethod
    def get_dark_theme():
        """Returns dark theme stylesheet"""
        return """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0f172a, stop:1 #020617);
            }

            QLabel { color: #e5e7eb; }

            QPushButton {
                background-color: #e2e8f0;
                color: #0f172a !important;
                border: 1px solid #cbd5e1 !important;
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover { 
                background-color: #dbeafe; 
                border: 1px solid #93c5fd !important;
                color: #0f172a !important;
            }
            QPushButton:pressed {
                background-color: #cbd5e1;
                border: 1px solid #94a3b8 !important;
                color: #0f172a !important;
            }

            QPushButton#secondary { 
                background-color: #334155; 
                color: #e5e7eb !important;
            }
            QPushButton#secondary:hover { 
                background-color: #475569; 
                color: #e5e7eb !important;
            }
            QPushButton#secondary:pressed {
                background-color: #475569;
                color: #e5e7eb !important;
            }

            QPushButton#success { 
                background-color: #10b981; 
                color: white !important;
            }
            QPushButton#success:hover { 
                background-color: #059669; 
                color: white !important;
            }
            QPushButton#success:pressed {
                background-color: #047857;
                color: white !important;
            }

            QPushButton#destructive {
                background-color: transparent;
                color: #f87171 !important;
                border: 2px solid #f87171;
            }
            QPushButton#destructive:hover { 
                background-color: rgba(248,113,113,0.12); 
                color: #f87171 !important;
            }
            QPushButton#destructive:pressed {
                background-color: rgba(248,113,113,0.25);
                color: #ef4444 !important;
            }

            QLineEdit, QSpinBox {
                padding: 12px 16px;
                border: 2px solid #1e293b;
                border-radius: 10px;
                background-color: #020617;
                color: #e5e7eb;
                font-size: 14px;
            }
            QLineEdit:focus, QSpinBox:focus { border-color: #3b82f6; }

            /* Tab sayfasının arka planını gerçekten koyulaştır */
            QTabWidget::pane {
                background-color: rgba(2,6,23,0.75);
            }
            QTabWidget > QWidget {
                background-color: transparent;
            }
            QTabWidget {
                background: transparent;
            }
            QTabBar {
                background: #0b1220;
                spacing: 4px;
            }
            QTabBar::tab {
                height: 44px;
                padding: 12px 24px;
                margin-right: 8px;
                border-radius: 12px;
                background: transparent;
                color: #94a3b8;
                font-size: 14px;
                font-weight: 600;
            }
            QTabBar::tab:selected {
                background: #1e3a8a;
                color: #60a5fa;
            }
            QTabBar::tab:hover {
                background: rgba(59,130,246,0.15);
                color: #93c5fd;
            }

            QTableWidget {
                background-color: #020617;
                border: 1px solid #1e293b;
                border-radius: 10px;
                gridline-color: #1e293b;
                color: #e5e7eb;
                font-size: 13px;
                selection-background-color: rgba(59,130,246,0.25);
                selection-color: #e5e7eb;
            }
            QTableWidget::item { padding: 8px; color: #e5e7eb; }
            QTableWidget::item:alternate { background-color: #0b1220; }
            QHeaderView::section {
                background-color: #0f172a;
                color: #e5e7eb;
                border: none;
                border-bottom: 2px solid #3b82f6;
                padding: 14px;
                font-weight: 700;
                font-size: 13px;
            }

            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical { border: none; background: transparent; width: 10px; }
            QScrollBar::handle:vertical { background: #334155; border-radius: 5px; min-height: 30px; }
            QScrollBar::handle:vertical:hover { background: #475569; }
        """
    
    @staticmethod
    def get_messagebox_stylesheet(dark_mode=False):
        """Returns messagebox stylesheet for given theme"""
        if not dark_mode:
            return """
                QMessageBox {
                    background-color: white;
                    color: #1e293b;
                    font-size: 13px;
                }
                QLabel { color: #1e293b; }
                QPushButton {
                    background-color: #2563eb;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 10px 18px;
                    font-weight: 700;
                    min-width: 90px;
                }
                QPushButton:hover { background-color: #1d4ed8; }
            """
        return """
            QMessageBox {
                background-color: #0b1220;
                color: #e5e7eb;
                font-size: 13px;
            }
            QLabel { color: #e5e7eb; }
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 18px;
                font-weight: 700;
                min-width: 90px;
            }
            QPushButton:hover { background-color: #1d4ed8; }
        """
    
    @staticmethod
    def get_header_style(dark_mode=False):
        """Returns header widget style"""
        if not dark_mode:
            return """
                QWidget {
                    background: rgba(255,255,255,0.75);
                    border: 1px solid rgba(226,232,240,0.9);
                    border-radius: 16px;
                }
            """
        return """
            QWidget {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 rgba(15,23,42,0.95),
                    stop:1 rgba(2,6,23,0.95));
                border: 1px solid rgba(51,65,85,0.9);
                border-radius: 16px;
            }
        """
    
    @staticmethod
    def get_text_color(dark_mode=False, element="title"):
        """Returns text color for given element"""
        if element == "title":
            return "#1e293b" if not dark_mode else "#e5e7eb"
        elif element == "subtitle":
            return "#64748b" if not dark_mode else "#94a3b8"
        elif element == "label":
            return "#374151" if not dark_mode else "#94a3b8"
        return "#1e293b" if not dark_mode else "#e5e7eb"


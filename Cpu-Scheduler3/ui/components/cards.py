"""Card Components for UI"""
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsDropShadowEffect


class ModernCard(QFrame):
    """Card with professional shadow"""
    def __init__(self, dark_mode=False, parent=None):
        super().__init__(parent)
        self.dark_mode = dark_mode
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.apply_style()

    def apply_style(self):
        if not self.dark_mode:
            self.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-radius: 16px;
                    border: 1px solid #e5e7eb;
                }
                QFrame:hover {
                    border: 1px solid #cbd5e1;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background-color: rgba(15,23,42,0.85);
                    border-radius: 16px;
                    border: 1px solid rgba(51,65,85,0.9);
                }
                QFrame:hover {
                    border: 1px solid rgba(71,85,105,0.9);
                }
            """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 25 if not self.dark_mode else 55))
        self.setGraphicsEffect(shadow)


class MetricCard(QFrame):
    """Balanced metric card"""
    def __init__(self, label, value, color="#2563eb", dark_mode=False, parent=None):
        super().__init__(parent)
        self.dark_mode = dark_mode
        self.setFixedHeight(110)
        self.color = color

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 18, 24, 18)

        self.label_widget = QLabel(label)
        self.label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.value_widget = QLabel(str(value))
        self.value_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.label_widget)
        self.layout.addWidget(self.value_widget)

        self.apply_style()

    def apply_style(self):
        if not self.dark_mode:
            self.setStyleSheet("""
                QFrame {
                    background: white;
                    border-radius: 16px;
                    border: 1px solid #e5e7eb;
                }
            """)
            label_color = "#64748b"
        else:
            self.setStyleSheet("""
                QFrame {
                    background: rgba(15,23,42,0.85);
                    border-radius: 16px;
                    border: 1px solid rgba(51,65,85,0.9);
                }
            """)
            label_color = "#94a3b8"

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 20 if not self.dark_mode else 45))
        self.setGraphicsEffect(shadow)

        self.label_widget.setStyleSheet(f"color: {label_color}; font-size: 14px; font-weight: 600;")
        self.value_widget.setStyleSheet(f"color: {self.color}; font-size: 30px; font-weight: 800;")


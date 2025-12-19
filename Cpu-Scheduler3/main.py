"""Main Entry Point for CPU Scheduler Application"""
import sys
import warnings
warnings.filterwarnings('ignore')

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

from ui.main_window import CPUSchedulerApp


def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    try:
        app.setFont(QFont('SF Pro Display', 10))
    except:
        app.setFont(QFont('System', 10))

    window = CPUSchedulerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()


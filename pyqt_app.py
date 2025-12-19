"""
CPU Scheduler - ULTIMATE Professional Version
✓ Professional shadows & depth
✓ Modern tab styling
✓ Simplified color palette (3-color rule)
✓ Button hierarchy
✓ Balanced spacing & typography
✓ All previous features
✓ FIXED: modern dark mode + header readability + input table readability + messagebox readability
✓ FIXED: header right padding (buttons not glued to the edge)
✓ NEW: centered layout wrapper (no more right-stuck)
✓ NEW: premium header bar (dark gradient + border + radius)
✓ NEW: premium light mode background + secondary button surface style
"""

import sys
import warnings
warnings.filterwarnings('ignore')

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QLineEdit, QTableWidget,
    QTableWidgetItem, QTabWidget, QScrollArea, QFrame, QMessageBox,
    QFileDialog, QSpinBox, QGraphicsDropShadowEffect, QSizePolicy   # ✅ ONLY ADD
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor

import matplotlib
matplotlib.use('qtagg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_pdf import PdfPages

from scheduler_fixed import SchedulingSimulator, Process


class ScrollFriendlyCanvas(FigureCanvasQTAgg):
    """Canvas that doesn't capture scroll events"""
    def __init__(self, figure):
        super().__init__(figure)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def wheelEvent(self, event):
        event.ignore()


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


class GanttChart(QWidget):
    """Gantt Chart with animation"""
    def __init__(self, gantt_data, algo_name, dark_mode=False):
        super().__init__()
        self.gantt_data = gantt_data
        self.algo_name = algo_name
        self.dark_mode = dark_mode
        self.current_frame = 0
        self.is_animating = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(0)

        self.fig = Figure(figsize=(12, 2.0), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = ScrollFriendlyCanvas(self.fig)
        self.canvas.setMinimumHeight(170)

        self.draw_chart(len(self.gantt_data))
        layout.addWidget(self.canvas)

    def draw_chart(self, up_to_frame):
        self.ax.clear()

        unique_pids = list(set([seg['pid'] for seg in self.gantt_data if seg['pid'] != 'IDLE']))
        import matplotlib.pyplot as plt
        process_colors = {
            pid: plt.cm.Set3(i / len(unique_pids)) if len(unique_pids) > 0 else '#3b82f6'
            for i, pid in enumerate(sorted(unique_pids))
        }

        for i in range(min(up_to_frame, len(self.gantt_data))):
            segment = self.gantt_data[i]
            start = segment['start']
            duration = segment['end'] - segment['start']
            pid = segment['pid']

            if pid == 'IDLE':
                color = '#f1f5f9' if not self.dark_mode else '#1e293b'
                hatch = '///'
                alpha = 1.0
                label_color = '#94a3b8'
                fontsize = 9
            else:
                color = process_colors.get(pid, '#3b82f6')
                hatch = None
                alpha = 0.6 if i == up_to_frame - 1 and self.is_animating else 1.0
                label_color = '#1e293b' if not self.dark_mode else '#e2e8f0'
                fontsize = 11

            self.ax.barh(
                0, duration, left=start, height=0.7,
                color=color,
                edgecolor='#1e293b' if not self.dark_mode else '#e2e8f0',
                linewidth=1.2, hatch=hatch, alpha=alpha
            )

            self.ax.text(
                start + duration / 2, 0, pid,
                ha='center', va='center', fontweight='bold', fontsize=fontsize,
                color=label_color
            )

        max_time = self.gantt_data[-1]['end']
        self.ax.set_xlim(0, max_time)
        self.ax.set_ylim(-0.5, 0.5)

        self.ax.set_xlabel(
            'Time', fontsize=10, fontweight='bold',
            color='#1e293b' if not self.dark_mode else '#e2e8f0',
            labelpad=8
        )
        self.ax.set_yticks([])

        self.ax.set_facecolor('white' if not self.dark_mode else '#0b1220')
        self.fig.patch.set_facecolor('white' if not self.dark_mode else '#0b1220')

        self.ax.tick_params(
            axis='x', labelsize=9,
            colors='#1e293b' if not self.dark_mode else '#e2e8f0',
            pad=5
        )

        for spine in ['top', 'right', 'left']:
            self.ax.spines[spine].set_visible(False)

        self.ax.spines['bottom'].set_color('#cbd5e1' if not self.dark_mode else '#334155')
        self.ax.spines['bottom'].set_linewidth(1.5)

        self.ax.grid(
            axis='x', alpha=0.2,
            color='#cbd5e1' if not self.dark_mode else '#334155',
            linestyle='-', linewidth=0.8
        )

        ticks = sorted(set([0] + [s['start'] for s in self.gantt_data] + [s['end'] for s in self.gantt_data]))
        self.ax.set_xticks(ticks)

        self.fig.subplots_adjust(left=0.03, right=0.99, top=0.92, bottom=0.30)
        self.canvas.draw()

    def play(self):
        if not self.is_animating:
            self.is_animating = True
            self.current_frame = 0
            self.timer.start(800)

    def pause(self):
        self.is_animating = False
        self.timer.stop()

    def reset(self):
        self.pause()
        self.current_frame = 0
        self.draw_chart(len(self.gantt_data))

    def next_frame(self):
        self.current_frame += 1
        if self.current_frame > len(self.gantt_data):
            self.pause()
            self.current_frame = len(self.gantt_data)
        self.draw_chart(self.current_frame)


class CPUSchedulerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.processes = []
        self.results = None
        self.dark_mode = True  # Default to dark mode

        self.algo_colors = {
            'FCFS': '#2563eb',
            'SJF': '#10b981',
            'Priority Scheduling': '#ef4444'
        }

        self.gantt_widgets = []
        self.init_ui()

    # ---------------------------
    # THEME HELPERS
    # ---------------------------
    def _apply_header_text_styles(self):
        title_color = "#1e293b" if not self.dark_mode else "#e5e7eb"
        sub_color = "#64748b" if not self.dark_mode else "#94a3b8"

        self.title_label.setStyleSheet(
            f"font-size: 38px; font-weight: 900; letter-spacing: -0.5px; color: {title_color};"
        )
        self.subtitle_label.setStyleSheet(
            f"font-size: 15px; color: {sub_color}; margin-left: 20px;"
        )

    def _apply_header_bar_style(self):
        if not hasattr(self, "header_widget"):
            return

        if not self.dark_mode:
            self.header_widget.setStyleSheet("""
                QWidget {
                    background: rgba(255,255,255,0.75);
                    border: 1px solid rgba(226,232,240,0.9);
                    border-radius: 16px;
                }
            """)
        else:
            self.header_widget.setStyleSheet("""
                QWidget {
                    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                        stop:0 rgba(15,23,42,0.95),
                        stop:1 rgba(2,6,23,0.95));
                    border: 1px solid rgba(51,65,85,0.9);
                    border-radius: 16px;
                }
            """)

    def _messagebox_stylesheet(self):
        if not self.dark_mode:
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

    def show_msg(self, kind: str, title: str, text: str):
        box = QMessageBox(self)
        box.setWindowTitle(title)
        box.setText(text)
        box.setStyleSheet(self._messagebox_stylesheet())

        if kind == "info":
            box.setIcon(QMessageBox.Icon.Information)
        elif kind == "warn":
            box.setIcon(QMessageBox.Icon.Warning)
        else:
            box.setIcon(QMessageBox.Icon.Critical)

        box.exec()

    def apply_modern_theme(self):
        self.setStyleSheet("""
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
                color: #0f172a;
                border: 1px solid #cbd5e1;
            }
            QPushButton#secondary:hover {
                background-color: #dbeafe;
                border-color: #93c5fd;
            }

            QPushButton#success {
                background-color: #10b981;
                padding: 14px 28px;
                font-size: 16px;
            }
            QPushButton#success:hover { background-color: #059669; }

            QPushButton#destructive {
                background-color: transparent;
                color: #ef4444;
                border: 2px solid #ef4444;
            }
            QPushButton#destructive:hover { background-color: #fef2f2; }

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
                background: rgba(255,255,255,0.75);
                border: 1px solid rgba(226,232,240,0.9);
                border-radius: 16px;
            }
            QTabBar::tab {
                height: 44px;
                padding: 12px 24px;
                margin-right: 8px;
                border: none;
                border-radius: 16px;
                background: transparent;
                color: #64748b;
                font-size: 14px;
                font-weight: 600;
            }
            QTabBar::tab:selected { background: #eef2ff; color: #2563eb; }
            QTabBar::tab:hover { background: #f8fafc; color: #2563eb; }

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
        """)

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0f172a, stop:1 #020617);
            }

            QLabel { color: #e5e7eb; }

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

            QPushButton#secondary { background-color: #334155; }
            QPushButton#secondary:hover { background-color: #475569; }

            QPushButton#success { background-color: #10b981; }
            QPushButton#success:hover { background-color: #059669; }

            QPushButton#destructive {
                background-color: transparent;
                color: #f87171;
                border: 2px solid #f87171;
            }
            QPushButton#destructive:hover { background-color: rgba(248,113,113,0.12); }

            QLineEdit, QSpinBox {
                padding: 12px 16px;
                border: 2px solid #1e293b;
                border-radius: 10px;
                background-color: #020617;
                color: #e5e7eb;
                font-size: 14px;
            }
            QLineEdit:focus, QSpinBox:focus { border-color: #3b82f6; }

            QTabWidget::pane {
                border: none;
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 rgba(15,23,42,0.95),
                    stop:1 rgba(2,6,23,0.95));
                border: 1px solid rgba(51,65,85,0.9);
                border-radius: 16px;
            }
            QTabBar::tab {
                height: 44px;
                padding: 12px 24px;
                margin-right: 8px;
                border: none;
                border-radius: 16px;
                background: transparent;
                color: #94a3b8;
                font-size: 14px;
                font-weight: 600;
            }
            QTabBar::tab:selected {
                background: rgba(59,130,246,0.15);
                color: #60a5fa;
            }
            QTabBar::tab:hover {
                background: rgba(59,130,246,0.08);
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
        """)

    # ---------------------------
    # UI
    # ---------------------------
    def init_ui(self):
        self.setWindowTitle('CPU Process Scheduling Simulator')
        self.setMinimumSize(1500, 950)

        self.apply_dark_theme()  # Start with dark theme

        central = QWidget()
        self.setCentralWidget(central)

        outer = QVBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)  # Outer layout: 0 margin
        outer.setSpacing(0)

        # Center container with equal margins on left and right
        container_wrapper = QHBoxLayout()
        container_wrapper.setContentsMargins(20, 0, 20, 0)  # Minimum safe margin: 16-24px range (using 20px)
        container_wrapper.addStretch()
        
        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.container.setMinimumWidth(1400)  # Increased minimum width for larger appearance
        self.container.setMaximumWidth(1800)  # Increased maximum width: 1700-1800px range
        
        container_wrapper.addWidget(self.container)
        container_wrapper.addStretch()
        
        wrapper_widget = QWidget()
        wrapper_widget.setLayout(container_wrapper)
        outer.addWidget(wrapper_widget)

        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setContentsMargins(36, 40, 36, 40)  # Slightly reduced horizontal padding (40→36) to maximize width
        self.main_layout.setSpacing(24)

        header = self.create_header()
        self.main_layout.addWidget(header)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        
        # Add shadow to tab widget for visual consistency with header
        tab_shadow = QGraphicsDropShadowEffect()
        tab_shadow.setBlurRadius(20)
        tab_shadow.setXOffset(0)
        tab_shadow.setYOffset(4)
        tab_shadow.setColor(QColor(0, 0, 0, 25 if not self.dark_mode else 55))
        self.tabs.setGraphicsEffect(tab_shadow)
        
        self.main_layout.addWidget(self.tabs)

        self.create_input_tab()
        self.create_results_tab()
        self.create_gantt_tab()
        self.create_comparison_tab()

        self._apply_header_text_styles()
        self._apply_header_bar_style()

    def create_header(self):
        header = QWidget()
        layout = QHBoxLayout(header)

        layout.setContentsMargins(20, 8, 20, 20)  # Equal left and right margins
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
        self.export_btn.clicked.connect(self.export_pdf)
        layout.addWidget(self.export_btn)

        self.dark_mode_btn = QPushButton('☀️ Light')  # Start with Light button (since dark_mode=True)
        self.dark_mode_btn.setObjectName('secondary')
        self.dark_mode_btn.clicked.connect(self.toggle_dark_mode)
        layout.addWidget(self.dark_mode_btn)

        self.header_widget = header
        self._apply_header_bar_style()

        return header

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            self.apply_dark_theme()
            self.dark_mode_btn.setText('☀️ Light')
        else:
            self.apply_modern_theme()
            self.dark_mode_btn.setText('🌙 Dark')

        self._apply_header_text_styles()
        self._apply_header_bar_style()
        self.refresh_input_styles()
        
        # Update tab widget shadow for theme consistency
        if hasattr(self, 'tabs') and self.tabs.graphicsEffect():
            tab_shadow = self.tabs.graphicsEffect()
            if isinstance(tab_shadow, QGraphicsDropShadowEffect):
                tab_shadow.setColor(QColor(0, 0, 0, 25 if not self.dark_mode else 55))

        for gantt in self.gantt_widgets:
            gantt.dark_mode = self.dark_mode
            gantt.draw_chart(len(gantt.gantt_data))

        if self.results:
            self.display_results()
            self.display_gantt_charts()
            self.display_comparison()

    # ---------------------------
    # INPUT TAB
    # ---------------------------
    def create_input_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.setSpacing(20)

        self.left_panel = ModernCard(self.dark_mode)
        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(24, 24, 24, 24)
        left_layout.setSpacing(16)
        self.left_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.input_title = QLabel('Add Process')
        title_color = "#1e293b" if not self.dark_mode else "#e5e7eb"
        self.input_title.setStyleSheet(f'font-size: 24px; font-weight: 800; color: {title_color};')
        left_layout.addWidget(self.input_title)

        pid_container, self.pid_input = self.create_input_field('Process ID', 'P1')
        arrival_container, self.arrival_input = self.create_input_field('Arrival Time', '0')
        burst_container, self.burst_input = self.create_input_field('Burst Time', '5')
        priority_container, self.priority_input = self.create_input_field('Priority', '1')

        left_layout.addWidget(pid_container)
        left_layout.addWidget(arrival_container)
        left_layout.addWidget(burst_container)
        left_layout.addWidget(priority_container)

        tq_container = QWidget()
        tq_layout = QVBoxLayout(tq_container)
        tq_layout.setContentsMargins(0, 0, 0, 0)
        tq_layout.setSpacing(8)

        self.tq_label = QLabel('Time Quantum (Round Robin)')
        tq_layout.addWidget(self.tq_label)

        self.tq_spinbox = QSpinBox()
        self.tq_spinbox.setMinimum(1)
        self.tq_spinbox.setMaximum(100)
        self.tq_spinbox.setValue(3)
        self.tq_spinbox.setFixedHeight(46)
        tq_layout.addWidget(self.tq_spinbox)

        left_layout.addWidget(tq_container)

        add_btn = QPushButton('➕ Add Process')
        add_btn.clicked.connect(self.add_process)
        left_layout.addWidget(add_btn)

        upload_btn = QPushButton('📁 Upload File')
        upload_btn.clicked.connect(self.upload_file)
        left_layout.addWidget(upload_btn)

        sample_btn = QPushButton('📋 Load Sample')
        sample_btn.setObjectName('secondary')
        sample_btn.clicked.connect(self.load_sample)
        left_layout.addWidget(sample_btn)

        clear_btn = QPushButton('🗑️ Clear All')
        clear_btn.setObjectName('destructive')
        clear_btn.clicked.connect(self.clear_processes)
        left_layout.addWidget(clear_btn)

        left_layout.addStretch()

        self.right_panel = ModernCard(self.dark_mode)
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(24, 24, 24, 24)
        self.right_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.list_title = QLabel('Process List')
        list_title_color = "#1e293b" if not self.dark_mode else "#e5e7eb"
        self.list_title.setStyleSheet(f'font-size: 24px; font-weight: 800; color: {list_title_color};')
        right_layout.addWidget(self.list_title)

        self.process_table = QTableWidget()
        self.process_table.setColumnCount(4)
        self.process_table.setHorizontalHeaderLabels(['Process', 'Arrival', 'Burst', 'Priority'])
        self.process_table.horizontalHeader().setStretchLastSection(True)
        self.process_table.setAlternatingRowColors(True)
        right_layout.addWidget(self.process_table)

        run_btn = QPushButton('🚀 Run Simulation')
        run_btn.setObjectName('success')
        run_btn.setFixedHeight(56)
        run_btn.clicked.connect(self.run_simulation)
        right_layout.addWidget(run_btn)

        # ✅ FIXED: give more width to the table on wide screens
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.left_panel, 1)
        layout.addWidget(self.right_panel, 3)
        layout.setStretchFactor(self.left_panel, 1)
        layout.setStretchFactor(self.right_panel, 3)

        self.tabs.addTab(tab, '📝 Input')
        self.refresh_input_styles()

    def refresh_input_styles(self):
        if hasattr(self, "left_panel"):
            self.left_panel.dark_mode = self.dark_mode
            self.left_panel.apply_style()
        if hasattr(self, "right_panel"):
            self.right_panel.dark_mode = self.dark_mode
            self.right_panel.apply_style()

        label_color = "#374151" if not self.dark_mode else "#94a3b8"
        if hasattr(self, "tq_label"):
            self.tq_label.setStyleSheet(f'font-size: 14px; font-weight: 700; color: {label_color};')
        
        # Update title colors for dark/light mode
        if hasattr(self, "input_title"):
            title_color = "#1e293b" if not self.dark_mode else "#e5e7eb"
            self.input_title.setStyleSheet(f'font-size: 24px; font-weight: 800; color: {title_color};')
        if hasattr(self, "list_title"):
            list_title_color = "#1e293b" if not self.dark_mode else "#e5e7eb"
            self.list_title.setStyleSheet(f'font-size: 24px; font-weight: 800; color: {list_title_color};')

        if hasattr(self, "process_table"):
            if not self.dark_mode:
                self.process_table.setStyleSheet("""
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
                """)
            else:
                self.process_table.setStyleSheet("""
                    QTableWidget {
                        background-color: rgba(15,23,42,0.6);
                        border: 1px solid rgba(51,65,85,0.9);
                        border-radius: 12px;
                        gridline-color: rgba(51,65,85,0.5);
                        color: #e5e7eb;
                        font-size: 13px;
                        selection-background-color: rgba(59,130,246,0.25);
                        selection-color: #e5e7eb;
                    }
                    QTableWidget::item { padding: 8px; color: #e5e7eb; }
                    QTableWidget::item:alternate { background-color: rgba(15,23,42,0.4); }
                    QHeaderView::section {
                        background-color: rgba(15,23,42,0.8);
                        color: #e5e7eb;
                        border: none;
                        border-bottom: 2px solid #3b82f6;
                        padding: 14px;
                        font-weight: 700;
                        font-size: 13px;
                    }
                """)

    def create_input_field(self, label_text, placeholder):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        label = QLabel(label_text)
        label_color = "#374151" if not self.dark_mode else "#94a3b8"
        label.setStyleSheet(f'font-size: 14px; font-weight: 700; color: {label_color};')

        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setFixedHeight(46)

        layout.addWidget(label)
        layout.addWidget(input_field)

        return container, input_field

    def upload_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Upload Process File", "", "Text Files (*.txt);;All Files (*)"
        )

        if file_name:
            try:
                self.clear_processes()

                with open(file_name, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue

                        parts = [p.strip() for p in line.split(',')]
                        if len(parts) >= 4:
                            pid = parts[0]
                            arrival = int(parts[1])
                            burst = int(parts[2])
                            priority = int(parts[3])

                            proc = Process(pid, arrival, burst, priority)
                            self.processes.append(proc)

                            row = self.process_table.rowCount()
                            self.process_table.insertRow(row)
                            self.process_table.setItem(row, 0, QTableWidgetItem(pid))
                            self.process_table.setItem(row, 1, QTableWidgetItem(str(arrival)))
                            self.process_table.setItem(row, 2, QTableWidgetItem(str(burst)))
                            self.process_table.setItem(row, 3, QTableWidgetItem(str(priority)))

                self.show_msg("info", "Success", f"Loaded {len(self.processes)} processes!")

            except Exception as e:
                self.show_msg("error", "Error", f"Failed to load file:\n{str(e)}")

    def export_pdf(self):
        if not self.results:
            self.show_msg("warn", "Warning", "Run simulation first!")
            return

        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Report", "scheduler_report.pdf", "PDF Files (*.pdf)"
        )

        if file_name:
            try:
                with PdfPages(file_name) as pdf:
                    fig = Figure(figsize=(11, 8.5))
                    fig.text(0.5, 0.95, 'CPU Scheduling Simulation Report',
                             ha='center', fontsize=20, fontweight='bold')

                    y_pos = 0.85
                    for result in self.results.values():
                        fig.text(0.1, y_pos, result['algorithm'], fontsize=14, fontweight='bold')
                        y_pos -= 0.05

                        metrics_text = f"Avg TAT: {result['metrics']['avg_turnaround_time']}  |  "
                        metrics_text += f"Avg WT: {result['metrics']['avg_waiting_time']}  |  "
                        metrics_text += f"CPU Util: {result['metrics']['cpu_utilization']}%"

                        fig.text(0.15, y_pos, metrics_text, fontsize=11)
                        y_pos -= 0.08

                    pdf.savefig(fig, bbox_inches='tight')

                    for gantt in self.gantt_widgets:
                        pdf.savefig(gantt.fig, bbox_inches='tight')

                self.show_msg("info", "Success", "Report saved!")

            except Exception as e:
                self.show_msg("error", "Error", f"Export failed:\n{str(e)}")

    # ---------------------------
    # OTHER TABS
    # ---------------------------
    def create_results_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.results_scroll = QScrollArea()
        self.results_scroll.setWidgetResizable(True)
        self.results_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.results_content = QWidget()
        self.results_layout = QVBoxLayout(self.results_content)

        placeholder = QLabel('Run simulation to see results')
        placeholder.setStyleSheet('font-size: 18px; color: #94a3b8;')
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_layout.addWidget(placeholder)

        self.results_scroll.setWidget(self.results_content)
        layout.addWidget(self.results_scroll)

        self.tabs.addTab(tab, '📊 Results')

    def create_gantt_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.gantt_scroll = QScrollArea()
        self.gantt_scroll.setWidgetResizable(True)
        self.gantt_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.gantt_content = QWidget()
        self.gantt_layout = QVBoxLayout(self.gantt_content)

        placeholder = QLabel('Run simulation to see Gantt charts')
        placeholder.setStyleSheet('font-size: 18px; color: #94a3b8;')
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gantt_layout.addWidget(placeholder)

        self.gantt_scroll.setWidget(self.gantt_content)
        layout.addWidget(self.gantt_scroll)

        self.tabs.addTab(tab, '📈 Gantt Charts')

    def create_comparison_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.comparison_scroll = QScrollArea()
        self.comparison_scroll.setWidgetResizable(True)
        self.comparison_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.comparison_content = QWidget()
        self.comparison_layout = QVBoxLayout(self.comparison_content)

        placeholder = QLabel('Run simulation to see comparisons')
        placeholder.setStyleSheet('font-size: 18px; color: #94a3b8;')
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.comparison_layout.addWidget(placeholder)

        self.comparison_scroll.setWidget(self.comparison_content)
        layout.addWidget(self.comparison_scroll)

        self.tabs.addTab(tab, '🔄 Comparison')

    # ---------------------------
    # ACTIONS
    # ---------------------------
    def add_process(self):
        try:
            pid = self.pid_input.text().strip()
            arrival = int(self.arrival_input.text())
            burst = int(self.burst_input.text())
            priority = int(self.priority_input.text())

            if not pid:
                self.show_msg("warn", "Error", "Enter Process ID")
                return

            if any(p.pid == pid for p in self.processes):
                self.show_msg("warn", "Error", f"Process {pid} exists")
                return

            proc = Process(pid, arrival, burst, priority)
            self.processes.append(proc)

            row = self.process_table.rowCount()
            self.process_table.insertRow(row)
            self.process_table.setItem(row, 0, QTableWidgetItem(pid))
            self.process_table.setItem(row, 1, QTableWidgetItem(str(arrival)))
            self.process_table.setItem(row, 2, QTableWidgetItem(str(burst)))
            self.process_table.setItem(row, 3, QTableWidgetItem(str(priority)))

            self.pid_input.clear()
            self.arrival_input.clear()
            self.burst_input.clear()
            self.priority_input.clear()

        except ValueError:
            self.show_msg("warn", "Error", "Invalid numbers")

    def load_sample(self):
        self.clear_processes()

        samples = [
            ('P1', 0, 8, 3),
            ('P2', 1, 4, 1),
            ('P3', 2, 9, 4),
            ('P4', 3, 5, 2)
        ]

        for pid, arrival, burst, priority in samples:
            proc = Process(pid, arrival, burst, priority)
            self.processes.append(proc)

            row = self.process_table.rowCount()
            self.process_table.insertRow(row)
            self.process_table.setItem(row, 0, QTableWidgetItem(pid))
            self.process_table.setItem(row, 1, QTableWidgetItem(str(arrival)))
            self.process_table.setItem(row, 2, QTableWidgetItem(str(burst)))
            self.process_table.setItem(row, 3, QTableWidgetItem(str(priority)))

        self.show_msg("info", "Success", "Sample loaded!")

    def clear_processes(self):
        self.processes = []
        self.process_table.setRowCount(0)

    def run_simulation(self):
        if not self.processes:
            self.show_msg("warn", "Error", "Add processes first")
            return

        tq = self.tq_spinbox.value()
        if tq <= 0:
            self.show_msg("warn", "Error", "Time quantum must be > 0")
            return

        simulator = SchedulingSimulator(self.processes)
        self.results = simulator.run_all(tq)

        for result in self.results.values():
            if 'Round Robin' in result['algorithm']:
                self.algo_colors[result['algorithm']] = '#6366f1'  # Indigo

        self.display_results()
        self.display_gantt_charts()
        self.display_comparison()

        self.tabs.setCurrentIndex(1)
        self.show_msg("info", "Success", "Simulation completed!")

    # ---------------------------
    # RESULTS / GANTT / COMPARISON
    # ---------------------------
    def display_results(self):
        while self.results_layout.count():
            child = self.results_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for result in self.results.values():
            card = ModernCard(self.dark_mode)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(24, 24, 24, 24)

            title = QLabel(result['algorithm'])
            title_color = "#1e293b" if not self.dark_mode else "#e5e7eb"
            title.setStyleSheet(f'font-size: 22px; font-weight: 800; color: {title_color};')
            card_layout.addWidget(title)

            metrics_container = QWidget()
            metrics_layout = QHBoxLayout(metrics_container)
            metrics_layout.setSpacing(16)

            metrics = [
                ('Avg Turnaround Time', result['metrics']['avg_turnaround_time'], '#2563eb'),
                ('Avg Waiting Time', result['metrics']['avg_waiting_time'], '#10b981'),
                ('CPU Utilization', f"{result['metrics']['cpu_utilization']}%", '#6366f1')
            ]

            for label, value, color in metrics:
                metric_card = MetricCard(label, value, color, self.dark_mode)
                metrics_layout.addWidget(metric_card)

            card_layout.addWidget(metrics_container)

            table = QTableWidget()
            table.setColumnCount(7)
            table.setHorizontalHeaderLabels(['ID', 'Arrival', 'Burst', 'Priority', 'Finish', 'TAT', 'WT'])
            table.horizontalHeader().setStretchLastSection(True)
            table.setRowCount(len(result['processes']))
            table.setAlternatingRowColors(True)
            
            # Enable vertical header to show row numbers
            table.verticalHeader().setVisible(True)
            table.verticalHeader().setDefaultSectionSize(40)
            for i in range(len(result['processes'])):
                header_item = QTableWidgetItem(str(i + 1))
                header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setVerticalHeaderItem(i, header_item)

            if not self.dark_mode:
                table.setStyleSheet("""
                    QTableWidget {
                        background-color: #f9fafb;
                        border: 1px solid #e5e7eb;
                        border-radius: 8px;
                        gridline-color: #e5e7eb;
                        color: #1e293b;
                        selection-background-color: #dbeafe;
                        selection-color: #1e293b;
                    }
                    QTableWidget::item { padding: 8px; color: #1e293b; }
                    QTableWidget::item:alternate { background-color: white; }
                    QHeaderView::section {
                        background-color: #f1f5f9;
                        color: #1e293b;
                        padding: 12px;
                        border: none;
                        border-bottom: 2px solid #2563eb;
                        font-weight: 700;
                    }
                    QTableWidget QTableCornerButton::section {
                        background-color: #f1f5f9;
                        border: none;
                        border-bottom: 2px solid #2563eb;
                        border-right: 1px solid #e5e7eb;
                    }
                    QTableWidget::verticalHeader {
                        background-color: #f1f5f9;
                    }
                    QTableWidget::verticalHeader::section {
                        background-color: #f1f5f9;
                        color: #1e293b;
                        padding: 8px;
                        border: none;
                        border-right: 2px solid #2563eb;
                        font-weight: 700;
                        text-align: center;
                    }
                """)
            else:
                table.setStyleSheet("""
                    QTableWidget {
                        background-color: rgba(15,23,42,0.6);
                        border: 1px solid rgba(51,65,85,0.9);
                        border-radius: 12px;
                        gridline-color: rgba(51,65,85,0.5);
                        color: #e5e7eb;
                        selection-background-color: rgba(59,130,246,0.25);
                        selection-color: #e5e7eb;
                    }
                    QTableWidget::item { padding: 8px; color: #e5e7eb; }
                    QTableWidget::item:alternate { background-color: rgba(15,23,42,0.4); }
                    QHeaderView::section {
                        background-color: rgba(15,23,42,0.8);
                        color: #e5e7eb;
                        padding: 12px;
                        border: none;
                        border-bottom: 2px solid #3b82f6;
                        font-weight: 700;
                    }
                    QTableWidget QTableCornerButton::section {
                        background-color: rgba(15,23,42,0.8);
                        border: none;
                        border-bottom: 2px solid #3b82f6;
                        border-right: 1px solid rgba(51,65,85,0.9);
                    }
                    QTableWidget::verticalHeader {
                        background-color: rgba(15,23,42,0.8);
                    }
                    QTableWidget::verticalHeader::section {
                        background-color: rgba(15,23,42,0.8);
                        color: #e5e7eb;
                        padding: 8px;
                        border: none;
                        border-right: 2px solid #3b82f6;
                        font-weight: 700;
                        text-align: center;
                    }
                """)

            for i, proc in enumerate(result['processes']):
                items = [
                    QTableWidgetItem(str(proc['pid'])),
                    QTableWidgetItem(str(proc['arrival_time'])),
                    QTableWidgetItem(str(proc['burst_time'])),
                    QTableWidgetItem(str(proc['priority'])),
                    QTableWidgetItem(str(proc['finish_time'])),
                    QTableWidgetItem(str(proc['turnaround_time'])),
                    QTableWidgetItem(str(proc['waiting_time']))
                ]
                for item in items:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                for col, item in enumerate(items):
                    table.setItem(i, col, item)

            table.setMinimumHeight(200)
            table.setMaximumHeight(300)
            card_layout.addWidget(table)

            self.results_layout.addWidget(card)

        self.results_layout.addStretch(1)

    def display_gantt_charts(self):
        for gantt in self.gantt_widgets:
            gantt.pause()

        while self.gantt_layout.count():
            child = self.gantt_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.gantt_widgets = []

        for result in self.results.values():
            card = ModernCard(self.dark_mode)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(24, 24, 24, 24)

            header = QWidget()
            header_layout = QHBoxLayout(header)
            header_layout.setContentsMargins(0, 0, 0, 12)

            title_widget = QWidget()
            if not self.dark_mode:
                title_widget.setStyleSheet('background: #f1f5f9; border-radius: 10px; padding: 6px 12px;')
            else:
                title_widget.setStyleSheet('background: rgba(59,130,246,0.12); border-radius: 10px; padding: 6px 12px;')

            title_layout = QHBoxLayout(title_widget)
            title_layout.setContentsMargins(0, 0, 0, 0)

            title = QLabel(result['algorithm'])
            title_color = "#1e293b" if not self.dark_mode else "#e5e7eb"
            title.setStyleSheet(f'font-size: 18px; font-weight: 800; background: transparent; color: {title_color};')
            title_layout.addWidget(title)
            header_layout.addWidget(title_widget)

            header_layout.addStretch()

            gantt_widget = GanttChart(result['gantt_chart'], result['algorithm'], self.dark_mode)
            self.gantt_widgets.append(gantt_widget)

            play_btn = QPushButton('▶')
            play_btn.setFixedSize(36, 36)
            play_btn.setStyleSheet('background-color: #10b981; border-radius: 18px; font-size: 14px; padding: 0;')
            play_btn.clicked.connect(gantt_widget.play)

            pause_btn = QPushButton('⏸')
            pause_btn.setFixedSize(36, 36)
            pause_btn.setStyleSheet('background-color: #f59e0b; border-radius: 18px; font-size: 14px; padding: 0;')
            pause_btn.clicked.connect(gantt_widget.pause)

            reset_btn = QPushButton('↻')
            reset_btn.setFixedSize(36, 36)
            reset_btn.setStyleSheet('background-color: #64748b; border-radius: 18px; font-size: 14px; padding: 0;')
            reset_btn.clicked.connect(gantt_widget.reset)

            header_layout.addWidget(play_btn)
            header_layout.addWidget(pause_btn)
            header_layout.addWidget(reset_btn)

            card_layout.addWidget(header)
            card_layout.addWidget(gantt_widget)

            self.gantt_layout.addWidget(card)

        min_height = len(self.results) * 400 + 200
        self.gantt_content.setMinimumHeight(min_height)
        self.gantt_layout.addStretch(1)

    def display_comparison(self):
        while self.comparison_layout.count():
            child = self.comparison_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        algorithms = list(self.results.values())
        algo_names = [a['algorithm'] for a in algorithms]

        import re
        short_names = []
        for name in algo_names:
            if 'Round Robin' in name:
                m = re.search(r"TQ=(\d+)", name)
                tq = m.group(1) if m else "?"
                short_names.append(f'RR({tq})')
            elif 'Priority' in name:
                short_names.append('PRIO')
            else:
                short_names.append(name)

        metrics = [
            ('Average Turnaround Time', [a['metrics']['avg_turnaround_time'] for a in algorithms]),
            ('Average Waiting Time', [a['metrics']['avg_waiting_time'] for a in algorithms]),
            ('CPU Utilization (%)', [a['metrics']['cpu_utilization'] for a in algorithms])
        ]

        for metric_name, values in metrics:
            card = ModernCard(self.dark_mode)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(24, 24, 24, 24)

            title = QLabel(metric_name)
            title_color = "#1e293b" if not self.dark_mode else "#e5e7eb"
            title.setStyleSheet(f'font-size: 20px; font-weight: 800; margin-bottom: 12px; color: {title_color};')
            card_layout.addWidget(title)

            fig = Figure(figsize=(11, 4.5), dpi=100,
                         facecolor='white' if not self.dark_mode else '#0b1220')
            ax = fig.add_subplot(111)

            colors = [self.algo_colors.get(name, '#2563eb') for name in algo_names]
            x_pos = range(len(short_names))
            bars = ax.bar(
                x_pos, values, color=colors,
                edgecolor='#1e293b' if not self.dark_mode else '#e5e7eb',
                linewidth=1.5, width=0.6, alpha=0.9
            )

            for bar, val in zip(bars, values):
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.,
                    height + max(values) * 0.015,
                    f'{val:.1f}',
                    ha='center', va='bottom',
                    fontweight='bold', fontsize=11,
                    color='#1e293b' if not self.dark_mode else '#e2e8f0'
                )

            ax.set_xticks(list(x_pos))
            ax.set_xticklabels(
                short_names, fontsize=12, fontweight='700',
                color='#374151' if not self.dark_mode else '#9ca3af'
            )

            ax.set_ylabel(
                metric_name, fontsize=11, fontweight='bold',
                color='#1e293b' if not self.dark_mode else '#e2e8f0'
            )
            ax.tick_params(
                axis='y', labelsize=10,
                colors='#64748b' if not self.dark_mode else '#9ca3b8'
            )

            ax.grid(axis='y', alpha=0.2, linestyle='--', linewidth=0.8)
            ax.set_axisbelow(True)

            y_max = max(values)
            y_min = min(values)
            if y_max == y_min:
                ax.set_ylim(0, y_max * 1.2 if y_max > 0 else 1)
            else:
                ax.set_ylim(0, y_max * 1.15)

            ax.set_facecolor('white' if not self.dark_mode else '#0b1220')
            fig.patch.set_facecolor('white' if not self.dark_mode else '#0b1220')

            for spine in ax.spines.values():
                spine.set_color('#e5e7eb' if not self.dark_mode else '#334155')
                spine.set_linewidth(1.5)

            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            fig.tight_layout(pad=2.0)

            canvas = ScrollFriendlyCanvas(fig)
            canvas.setMinimumHeight(400)
            card_layout.addWidget(canvas)

            self.comparison_layout.addWidget(card)

        min_height = len(metrics) * 500 + 200
        self.comparison_content.setMinimumHeight(min_height)
        self.comparison_layout.addStretch(1)


def main():
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

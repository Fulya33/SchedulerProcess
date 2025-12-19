"""
Main Window for CPU Scheduler Application
Modular structure with separated components
"""
import sys
import warnings
import re
warnings.filterwarnings('ignore')

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QTabWidget, QScrollArea,
    QSpinBox, QGraphicsDropShadowEffect, QSizePolicy, QMessageBox, QFileDialog,
    QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from matplotlib.figure import Figure
from matplotlib.backends.backend_pdf import PdfPages

from scheduler_fixed import SchedulingSimulator, Process
from ui.components import ModernCard, MetricCard, GanttChart, ScrollFriendlyCanvas
from ui.header import HeaderWidget
from themes.theme_manager import ThemeManager
from utils.constants import ALGO_COLORS, DEFAULT_DARK_MODE, WINDOW_TITLE, WINDOW_MIN_SIZE
from utils.constants import CONTAINER_MIN_WIDTH, CONTAINER_MAX_WIDTH, CONTAINER_MARGIN
from utils.constants import MAIN_LAYOUT_PADDING, MAIN_LAYOUT_SPACING


class CPUSchedulerApp(QMainWindow):
    """Main Application Window"""
    
    def __init__(self):
        super().__init__()
        self.processes = []
        self.results = None
        self.dark_mode = DEFAULT_DARK_MODE
        self.algo_colors = ALGO_COLORS.copy()
        self.gantt_widgets = []
        self.init_ui()

    def init_ui(self):
        """Initialize UI components"""
        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(*WINDOW_MIN_SIZE)

        # Apply initial theme
        if self.dark_mode:
            self.setStyleSheet(ThemeManager.get_dark_theme())
        else:
            self.setStyleSheet(ThemeManager.get_light_theme())

        # Setup main layout
        central = QWidget()
        self.setCentralWidget(central)
        outer = QVBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Center container
        container_wrapper = QHBoxLayout()
        container_wrapper.setContentsMargins(CONTAINER_MARGIN, 0, CONTAINER_MARGIN, 0)
        container_wrapper.addStretch()
        
        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.container.setMinimumWidth(CONTAINER_MIN_WIDTH)
        self.container.setMaximumWidth(CONTAINER_MAX_WIDTH)
        
        container_wrapper.addWidget(self.container)
        container_wrapper.addStretch()
        
        wrapper_widget = QWidget()
        wrapper_widget.setLayout(container_wrapper)
        outer.addWidget(wrapper_widget)

        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setContentsMargins(*MAIN_LAYOUT_PADDING)
        self.main_layout.setSpacing(MAIN_LAYOUT_SPACING)

        # Create header
        self.header = HeaderWidget()
        self.header.export_btn.clicked.connect(self.export_pdf)
        self.header.dark_mode_btn.clicked.connect(self.toggle_dark_mode)
        self.main_layout.addWidget(self.header)

        # Create tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(False)
        
        # Add shadow to tab widget
        tab_shadow = QGraphicsDropShadowEffect()
        tab_shadow.setBlurRadius(20)
        tab_shadow.setXOffset(0)
        tab_shadow.setYOffset(4)
        tab_shadow.setColor(QColor(0, 0, 0, 25 if not self.dark_mode else 55))
        self.tabs.setGraphicsEffect(tab_shadow)
        
        self.main_layout.addWidget(self.tabs)

        # Create all tabs
        self.create_input_tab()
        self.create_results_tab()
        self.create_gantt_tab()
        self.create_comparison_tab()

        # Apply initial header style
        self.header.apply_style(self.dark_mode)

    def toggle_dark_mode(self):
        """Toggle between dark and light mode"""
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            self.setStyleSheet(ThemeManager.get_dark_theme())
            self.header.dark_mode_btn.setText('☀️ Light')
        else:
            self.setStyleSheet(ThemeManager.get_light_theme())
            self.header.dark_mode_btn.setText('🌙 Dark')

        self.header.apply_style(self.dark_mode)
        self.refresh_input_styles()
        
        # Update tab widget shadow
        if hasattr(self, 'tabs') and self.tabs.graphicsEffect():
            tab_shadow = self.tabs.graphicsEffect()
            if isinstance(tab_shadow, QGraphicsDropShadowEffect):
                tab_shadow.setColor(QColor(0, 0, 0, 25 if not self.dark_mode else 55))

        # Update gantt charts
        for gantt in self.gantt_widgets:
            gantt.dark_mode = self.dark_mode
            gantt.draw_chart(len(gantt.gantt_data))

        # Refresh results if available
        if self.results:
            self.display_results()
            self.display_gantt_charts()
            self.display_comparison()

    def show_msg(self, kind: str, title: str, text: str):
        """Show message box"""
        box = QMessageBox(self)
        box.setWindowTitle(title)
        box.setText(text)
        box.setStyleSheet(ThemeManager.get_messagebox_stylesheet(self.dark_mode))

        if kind == "info":
            box.setIcon(QMessageBox.Icon.Information)
        elif kind == "warn":
            box.setIcon(QMessageBox.Icon.Warning)
        else:
            box.setIcon(QMessageBox.Icon.Critical)

        box.exec()

    # Input Tab Methods
    def create_input_tab(self):
        """Create input tab with process management"""
        tab = QWidget()
        tab.setAutoFillBackground(True)
        tab.setStyleSheet("background: transparent;")
        layout = QHBoxLayout(tab)
        layout.setSpacing(20)

        # Left panel - Input form
        self.left_panel = ModernCard(self.dark_mode)
        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(24, 24, 24, 24)
        left_layout.setSpacing(16)
        self.left_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.input_title = QLabel('Add Process')
        title_color = ThemeManager.get_text_color(self.dark_mode, "title")
        self.input_title.setStyleSheet(f'font-size: 24px; font-weight: 800; color: {title_color};')
        left_layout.addWidget(self.input_title)

        # Input fields
        pid_container, self.pid_input = self.create_input_field('Process ID', 'P1')
        arrival_container, self.arrival_input = self.create_input_field('Arrival Time', '0')
        burst_container, self.burst_input = self.create_input_field('Burst Time', '5')
        priority_container, self.priority_input = self.create_input_field('Priority', '1')

        left_layout.addWidget(pid_container)
        left_layout.addWidget(arrival_container)
        left_layout.addWidget(burst_container)
        left_layout.addWidget(priority_container)

        # Time quantum
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

        # Buttons
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

        # Right panel - Process list
        self.right_panel = ModernCard(self.dark_mode)
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(24, 24, 24, 24)
        self.right_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.list_title = QLabel('Process List')
        list_title_color = ThemeManager.get_text_color(self.dark_mode, "title")
        self.list_title.setStyleSheet(f'font-size: 24px; font-weight: 800; color: {list_title_color};')
        right_layout.addWidget(self.list_title)

        self.process_table = QTableWidget()
        self.process_table.setColumnCount(4)
        self.process_table.setHorizontalHeaderLabels(['Process', 'Arrival', 'Burst', 'Priority'])
        self.process_table.horizontalHeader().setStretchLastSection(True)
        self.process_table.setAlternatingRowColors(True)
        # Disable corner button to remove white square (macOS fix)
        self.process_table.setCornerButtonEnabled(False)
        # Enable vertical header to show row numbers
        self.process_table.verticalHeader().setVisible(True)
        self.process_table.verticalHeader().setDefaultSectionSize(40)
        right_layout.addWidget(self.process_table)

        run_btn = QPushButton('🚀 Run Simulation')
        run_btn.setObjectName('success')
        run_btn.setFixedHeight(56)
        run_btn.clicked.connect(self.run_simulation)
        right_layout.addWidget(run_btn)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.left_panel, 1)
        layout.addWidget(self.right_panel, 3)
        layout.setStretchFactor(self.left_panel, 1)
        layout.setStretchFactor(self.right_panel, 3)

        self.tabs.addTab(tab, '📝 Input')
        self.refresh_input_styles()

    def create_input_field(self, label_text, placeholder):
        """Create input field with label"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        label = QLabel(label_text)
        label_color = ThemeManager.get_text_color(self.dark_mode, "label")
        label.setStyleSheet(f'font-size: 14px; font-weight: 700; color: {label_color};')

        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setFixedHeight(46)

        layout.addWidget(label)
        layout.addWidget(input_field)

        return container, input_field

    def refresh_input_styles(self):
        """Refresh input tab styles based on theme"""
        if hasattr(self, "left_panel"):
            self.left_panel.dark_mode = self.dark_mode
            self.left_panel.apply_style()
        if hasattr(self, "right_panel"):
            self.right_panel.dark_mode = self.dark_mode
            self.right_panel.apply_style()

        label_color = ThemeManager.get_text_color(self.dark_mode, "label")
        if hasattr(self, "tq_label"):
            self.tq_label.setStyleSheet(f'font-size: 14px; font-weight: 700; color: {label_color};')
        
        # Update title colors
        if hasattr(self, "input_title"):
            title_color = ThemeManager.get_text_color(self.dark_mode, "title")
            self.input_title.setStyleSheet(f'font-size: 24px; font-weight: 800; color: {title_color};')
        if hasattr(self, "list_title"):
            list_title_color = ThemeManager.get_text_color(self.dark_mode, "title")
            self.list_title.setStyleSheet(f'font-size: 24px; font-weight: 800; color: {list_title_color};')

        # Update process table styles
        if hasattr(self, "process_table"):
            # Disable corner button to remove white square (macOS fix)
            self.process_table.setCornerButtonEnabled(False)
            # Ensure vertical header is visible and update row numbers
            self.process_table.verticalHeader().setVisible(True)
            self.process_table.verticalHeader().setDefaultSectionSize(40)
            
            # Update row numbers in vertical header
            for i in range(self.process_table.rowCount()):
                header_item = QTableWidgetItem(str(i + 1))
                header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.process_table.setVerticalHeaderItem(i, header_item)
            
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
                    QTableWidget QTableCornerButton::section {
                        background-color: #f8fafc;
                        border: none;
                        border-bottom: 2px solid #2563eb;
                        border-right: 1px solid #e5e7eb;
                    }
                    QTableWidget::verticalHeader {
                        background-color: #f8fafc;
                    }
                    QTableWidget::verticalHeader::section {
                        background-color: #f8fafc;
                        color: #1e293b;
                        padding: 8px;
                        border: none;
                        border-right: 2px solid #2563eb;
                        font-weight: 700;
                        text-align: center;
                    }
                """)
                # Apply vertical header style directly (Qt stylesheet fix)
                if self.process_table.verticalHeader():
                    self.process_table.verticalHeader().setStyleSheet("""
                        QHeaderView::section {
                            background-color: #f8fafc;
                            color: #1e293b;
                            border: none;
                            border-right: 2px solid #2563eb;
                            font-weight: 700;
                            padding: 8px;
                        }
                    """)
            else:
                self.process_table.setStyleSheet("""
                    QTableWidget {
                        background-color: #111827;
                        border: 1px solid #1f2933;
                        border-radius: 10px;
                        gridline-color: #1f2933;
                        color: #e5e7eb;
                        font-size: 13px;
                        selection-background-color: rgba(59,130,246,0.25);
                        selection-color: #e5e7eb;
                    }
                    QTableWidget::item { padding: 8px; color: #e5e7eb; }
                    QTableWidget::item:alternate { background-color: #0b1220; }
                    QHeaderView::section {
                        background-color: #0b1220;
                        color: #e5e7eb;
                        border: none;
                        border-bottom: 2px solid #2563eb;
                        padding: 14px;
                        font-weight: 700;
                        font-size: 13px;
                    }
                    QTableWidget QTableCornerButton::section {
                        background-color: #0b1220;
                        border: none;
                        border-bottom: 2px solid #2563eb;
                        border-right: 1px solid #1f2933;
                    }
                    QTableWidget::verticalHeader {
                        background-color: #0b1220;
                    }
                    QTableWidget::verticalHeader::section {
                        background-color: #0b1220;
                        color: #e5e7eb;
                        padding: 8px;
                        border: none;
                        border-right: 2px solid #2563eb;
                        font-weight: 700;
                        text-align: center;
                    }
                """)
                # Apply vertical header style directly (Qt stylesheet fix)
                if self.process_table.verticalHeader():
                    self.process_table.verticalHeader().setStyleSheet("""
                        QHeaderView::section {
                            background-color: #0b1220;
                            color: #e5e7eb;
                            border: none;
                            border-right: 2px solid #2563eb;
                            font-weight: 700;
                            padding: 8px;
                        }
                    """)

    # Action Methods
    def add_process(self):
        """Add a new process"""
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
            # Add row number to vertical header
            header_item = QTableWidgetItem(str(row + 1))
            header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.process_table.setVerticalHeaderItem(row, header_item)
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
        """Load sample processes"""
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
            # Add row number to vertical header
            header_item = QTableWidgetItem(str(row + 1))
            header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.process_table.setVerticalHeaderItem(row, header_item)
            self.process_table.setItem(row, 0, QTableWidgetItem(pid))
            self.process_table.setItem(row, 1, QTableWidgetItem(str(arrival)))
            self.process_table.setItem(row, 2, QTableWidgetItem(str(burst)))
            self.process_table.setItem(row, 3, QTableWidgetItem(str(priority)))

        self.show_msg("info", "Success", "Sample loaded!")

    def clear_processes(self):
        """Clear all processes"""
        self.processes = []
        self.process_table.setRowCount(0)

    def upload_file(self):
        """Upload process file"""
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
                            # Add row number to vertical header
                            header_item = QTableWidgetItem(str(row + 1))
                            header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.process_table.setVerticalHeaderItem(row, header_item)
                            self.process_table.setItem(row, 0, QTableWidgetItem(pid))
                            self.process_table.setItem(row, 1, QTableWidgetItem(str(arrival)))
                            self.process_table.setItem(row, 2, QTableWidgetItem(str(burst)))
                            self.process_table.setItem(row, 3, QTableWidgetItem(str(priority)))

                self.show_msg("info", "Success", f"Loaded {len(self.processes)} processes!")

            except Exception as e:
                self.show_msg("error", "Error", f"Failed to load file:\n{str(e)}")

    def run_simulation(self):
        """Run scheduling simulation"""
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
                self.algo_colors[result['algorithm']] = '#6366f1'

        self.display_results()
        self.display_gantt_charts()
        self.display_comparison()

        self.tabs.setCurrentIndex(1)
        self.show_msg("info", "Success", "Simulation completed!")

    def export_pdf(self):
        """Export results to PDF"""
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

    # Tab Creation Methods
    def create_results_tab(self):
        """Create results tab"""
        tab = QWidget()
        tab.setAutoFillBackground(True)
        tab.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(tab)

        self.results_scroll = QScrollArea()
        self.results_scroll.setWidgetResizable(True)
        self.results_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.results_scroll.setStyleSheet("background: transparent;")
        
        self.results_content = QWidget()
        self.results_content.setAutoFillBackground(True)
        self.results_content.setStyleSheet("background: transparent;")
        self.results_layout = QVBoxLayout(self.results_content)

        placeholder = QLabel('Run simulation to see results')
        placeholder.setStyleSheet('font-size: 18px; color: #94a3b8;')
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_layout.addWidget(placeholder)

        self.results_scroll.setWidget(self.results_content)
        layout.addWidget(self.results_scroll)

        self.tabs.addTab(tab, '📊 Results')

    def create_gantt_tab(self):
        """Create Gantt charts tab"""
        tab = QWidget()
        tab.setAutoFillBackground(True)
        tab.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(tab)

        self.gantt_scroll = QScrollArea()
        self.gantt_scroll.setWidgetResizable(True)
        self.gantt_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.gantt_scroll.setStyleSheet("background: transparent;")
        
        self.gantt_content = QWidget()
        self.gantt_content.setAutoFillBackground(True)
        self.gantt_content.setStyleSheet("background: transparent;")
        self.gantt_layout = QVBoxLayout(self.gantt_content)

        placeholder = QLabel('Run simulation to see Gantt charts')
        placeholder.setStyleSheet('font-size: 18px; color: #94a3b8;')
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gantt_layout.addWidget(placeholder)

        self.gantt_scroll.setWidget(self.gantt_content)
        layout.addWidget(self.gantt_scroll)

        self.tabs.addTab(tab, '📈 Gantt Charts')

    def create_comparison_tab(self):
        """Create comparison tab"""
        tab = QWidget()
        tab.setAutoFillBackground(True)
        tab.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(tab)

        self.comparison_scroll = QScrollArea()
        self.comparison_scroll.setWidgetResizable(True)
        self.comparison_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.comparison_scroll.setStyleSheet("background: transparent;")
        
        self.comparison_content = QWidget()
        self.comparison_content.setAutoFillBackground(True)
        self.comparison_content.setStyleSheet("background: transparent;")
        self.comparison_layout = QVBoxLayout(self.comparison_content)

        placeholder = QLabel('Run simulation to see comparisons')
        placeholder.setStyleSheet('font-size: 18px; color: #94a3b8;')
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.comparison_layout.addWidget(placeholder)

        self.comparison_scroll.setWidget(self.comparison_content)
        layout.addWidget(self.comparison_scroll)

        self.tabs.addTab(tab, '🔄 Comparison')

    # Display Methods
    def display_results(self):
        """Display simulation results"""
        while self.results_layout.count():
            child = self.results_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for result in self.results.values():
            card = ModernCard(self.dark_mode)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(24, 24, 24, 24)

            title = QLabel(result['algorithm'])
            title_color = ThemeManager.get_text_color(self.dark_mode, "title")
            title.setStyleSheet(f'font-size: 22px; font-weight: 800; color: {title_color};')
            card_layout.addWidget(title)

            # Metrics
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

            # Results table
            table = QTableWidget()
            table.setColumnCount(7)
            table.setHorizontalHeaderLabels(['ID', 'Arrival', 'Burst', 'Priority', 'Finish', 'TAT', 'WT'])
            table.horizontalHeader().setStretchLastSection(True)
            table.setRowCount(len(result['processes']))
            table.setAlternatingRowColors(True)
            
            # Hide corner button
            table.setCornerButtonEnabled(False)
            
            # Hide vertical header to eliminate white space
            table.verticalHeader().setVisible(False)

            # Apply table styles
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
                """)
            else:
                table.setStyleSheet("""
                    QTableWidget {
                        background-color: #0f172a;
                        border: 1px solid #1f2933;
                        border-radius: 8px;
                        gridline-color: #1f2933;
                        color: #e5e7eb;
                        selection-background-color: rgba(59,130,246,0.25);
                        selection-color: #e5e7eb;
                    }
                    QTableWidget::item { padding: 8px; color: #e5e7eb; }
                    QTableWidget::item:alternate { background-color: #1a1f2e; }
                    QHeaderView::section {
                        background-color: #0b1220;
                        color: #e5e7eb;
                        padding: 12px;
                        border: none;
                        border-bottom: 2px solid #2563eb;
                        font-weight: 700;
                    }
                """)

            # Populate table
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
        """Display Gantt charts"""
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
            title_color = ThemeManager.get_text_color(self.dark_mode, "title")
            title.setStyleSheet(f'font-size: 18px; font-weight: 800; background: transparent; color: {title_color};')
            title_layout.addWidget(title)
            header_layout.addWidget(title_widget)

            header_layout.addStretch()

            gantt_widget = GanttChart(result['gantt_chart'], result['algorithm'], self.dark_mode)
            self.gantt_widgets.append(gantt_widget)

            # Control buttons
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
        """Display comparison charts"""
        while self.comparison_layout.count():
            child = self.comparison_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        algorithms = list(self.results.values())
        algo_names = [a['algorithm'] for a in algorithms]

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
            title_color = ThemeManager.get_text_color(self.dark_mode, "title")
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


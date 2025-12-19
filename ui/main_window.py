"""
Main Window for CPU Scheduler Application
Modular structure with separated components
"""
import sys
import warnings
warnings.filterwarnings('ignore')

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QGraphicsDropShadowEffect, QSizePolicy, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from matplotlib.backends.backend_pdf import PdfPages

from services.process_service import ProcessService
from services.simulation_service import SimulationService
from services.file_service import FileService
from ui.components import ModernCard
from ui.header import HeaderWidget
from ui.tabs import InputTab, ResultsTab, GanttTab, ComparisonTab
from themes.theme_manager import ThemeManager
from utils.constants import (
    ALGO_COLORS, DEFAULT_DARK_MODE, WINDOW_TITLE, WINDOW_MIN_SIZE,
    CONTAINER_MIN_WIDTH, CONTAINER_MAX_WIDTH, CONTAINER_MARGIN,
    MAIN_LAYOUT_PADDING, MAIN_LAYOUT_SPACING
)


class CPUSchedulerApp(QMainWindow):
    """Main Application Window"""
    
    def __init__(self):
        super().__init__()
        # Services
        self.process_service = ProcessService()
        self.file_service = FileService()
        self.simulation_service = None
        
        # State
        self.results = None
        self.dark_mode = DEFAULT_DARK_MODE
        self.algo_colors = ALGO_COLORS.copy()
        
        # UI Components
        self.input_tab = None
        self.results_tab = None
        self.gantt_tab = None
        self.comparison_tab = None
        
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
        
        # Center container - make it fill more of the window
        container_wrapper = QHBoxLayout()
        container_wrapper.setContentsMargins(CONTAINER_MARGIN, 0, CONTAINER_MARGIN, 0)
        # Reduce side margins to make container wider
        container_wrapper.addStretch(1)
        
        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.container.setMinimumWidth(CONTAINER_MIN_WIDTH)
        self.container.setMaximumWidth(CONTAINER_MAX_WIDTH)
        
        container_wrapper.addWidget(self.container, 10)  # Give container more space
        container_wrapper.addStretch(1)
        
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
        self.create_tabs()
        
        # Apply initial header style
        self.header.apply_style(self.dark_mode)
    
    def create_tabs(self):
        """Create all application tabs"""
        # Input Tab
        self.input_tab = InputTab(self.process_service, self.dark_mode)
        self.input_tab.add_btn.clicked.connect(self.add_process)
        self.input_tab.upload_btn.clicked.connect(self.upload_file)
        self.input_tab.sample_btn.clicked.connect(self.load_sample)
        self.input_tab.clear_btn.clicked.connect(self.clear_processes)
        self.input_tab.run_btn.clicked.connect(self.run_simulation)
        self.tabs.addTab(self.input_tab, '📝 Input')
        
        # Results Tab
        self.results_tab = ResultsTab(self.dark_mode)
        self.tabs.addTab(self.results_tab, '📊 Results')
        
        # Gantt Tab
        self.gantt_tab = GanttTab(self.dark_mode)
        self.tabs.addTab(self.gantt_tab, '📈 Gantt Charts')
        
        # Comparison Tab
        self.comparison_tab = ComparisonTab(self.dark_mode)
        self.tabs.addTab(self.comparison_tab, '🔄 Comparison')
    
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
        
        # Update tab widget shadow
        if hasattr(self, 'tabs') and self.tabs.graphicsEffect():
            tab_shadow = self.tabs.graphicsEffect()
            if isinstance(tab_shadow, QGraphicsDropShadowEffect):
                tab_shadow.setColor(QColor(0, 0, 0, 25 if not self.dark_mode else 55))
        
        # Update all tabs
        if self.input_tab:
            self.input_tab.update_theme(self.dark_mode)
        if self.results_tab:
            self.results_tab.update_theme(self.dark_mode)
        if self.gantt_tab:
            self.gantt_tab.update_theme(self.dark_mode)
        if self.comparison_tab:
            self.comparison_tab.update_theme(self.dark_mode)
    
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
    
    # Process Management Methods
    def add_process(self):
        """Add a new process"""
        pid, arrival, burst, priority = self.input_tab.get_input_values()
        
        if pid is None:
            self.show_msg("warn", "Error", "Invalid numbers")
            return
        
        if not pid:
            self.show_msg("warn", "Error", "Enter Process ID")
            return
        
        if not self.process_service.add_process(pid, arrival, burst, priority):
            self.show_msg("warn", "Error", f"Process {pid} already exists")
            return
        
        self.input_tab.clear_inputs()
        self.input_tab.refresh_process_table()
    
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
            self.process_service.add_process(pid, arrival, burst, priority)
        
        self.input_tab.refresh_process_table()
        self.show_msg("info", "Success", "Sample loaded!")
    
    def clear_processes(self):
        """Clear all processes"""
        self.process_service.clear_all()
        if self.input_tab:
            self.input_tab.refresh_process_table()
    
    def upload_file(self):
        """Upload process file"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Upload Process File", "", "Text Files (*.txt);;All Files (*)"
        )
        
        if file_name:
            try:
                self.clear_processes()
                processes = self.file_service.load_from_file(file_name)
                
                for proc in processes:
                    self.process_service.add_process(
                        proc.pid, proc.arrival_time, proc.burst_time, proc.priority
                    )
                
                self.input_tab.refresh_process_table()
                self.show_msg("info", "Success", f"Loaded {len(processes)} processes!")
            
            except Exception as e:
                self.show_msg("error", "Error", f"Failed to load file:\n{str(e)}")
    
    def run_simulation(self):
        """Run scheduling simulation"""
        if not self.process_service.has_processes():
            self.show_msg("warn", "Error", "Add processes first")
            return
        
        tq = self.input_tab.get_time_quantum()
        if tq <= 0:
            self.show_msg("warn", "Error", "Time quantum must be > 0")
            return
        
        try:
            # Create simulation service
            processes = self.process_service.get_all()
            self.simulation_service = SimulationService(processes)
            
            # Run simulation
            self.results = self.simulation_service.run_all_algorithms(tq)
            
            # Update colors for Round Robin
            for result in self.results.values():
                if 'Round Robin' in result['algorithm']:
                    self.algo_colors[result['algorithm']] = '#6366f1'
            
            # Display results
            self.results_tab.display_results(self.results)
            self.gantt_tab.display_gantt_charts(self.results)
            self.comparison_tab.display_comparison(self.results)
            
            # Switch to results tab
            self.tabs.setCurrentIndex(1)
            self.show_msg("info", "Success", "Simulation completed!")
        
        except Exception as e:
            self.show_msg("error", "Error", f"Simulation failed:\n{str(e)}")
    
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
                from matplotlib.figure import Figure
                
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
                    
                    # Save Gantt charts
                    for gantt in self.gantt_tab.gantt_widgets:
                        pdf.savefig(gantt.fig, bbox_inches='tight')
                
                self.show_msg("info", "Success", "Report saved!")
            
            except Exception as e:
                self.show_msg("error", "Error", f"Export failed:\n{str(e)}")

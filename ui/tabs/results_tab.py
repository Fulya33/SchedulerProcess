"""Results Tab for Displaying Simulation Results"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt
from ui.components import ModernCard, MetricCard
from themes.theme_manager import ThemeManager
from typing import Dict, Optional


class ResultsTab(QWidget):
    """Results tab for displaying simulation results"""
    
    def __init__(self, dark_mode: bool = False, parent=None):
        super().__init__(parent)
        self.dark_mode = dark_mode
        self.results: Optional[Dict] = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI components"""
        self.setAutoFillBackground(True)
        self.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(self)
        
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
    
    def display_results(self, results: Dict):
        """Display simulation results"""
        self.results = results
        
        # Clear existing widgets
        while self.results_layout.count():
            child = self.results_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        for result in results.values():
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
            table = self._create_results_table(result['processes'])
            card_layout.addWidget(table)
            
            self.results_layout.addWidget(card)
        
        self.results_layout.addStretch(1)
    
    def _create_results_table(self, processes: list):
        """Create results table for processes"""
        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(['ID', 'Arrival', 'Burst', 'Priority', 'Finish', 'TAT', 'WT'])
        table.horizontalHeader().setStretchLastSection(True)
        table.setRowCount(len(processes))
        table.setAlternatingRowColors(True)
        table.setCornerButtonEnabled(False)
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
        for i, proc in enumerate(processes):
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
        return table
    
    def update_theme(self, dark_mode: bool):
        """Update theme"""
        self.dark_mode = dark_mode
        if self.results:
            self.display_results(self.results)



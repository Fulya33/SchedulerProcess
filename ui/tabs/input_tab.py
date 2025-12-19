"""Input Tab for Process Management"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QSpinBox, QSizePolicy, QLayout
)
from PyQt6.QtCore import Qt
from ui.components import ModernCard
from themes.theme_manager import ThemeManager
from services.process_service import ProcessService
from services.file_service import FileService
from models.process import Process


class InputTab(QWidget):
    """Input tab for managing processes"""
    
    def __init__(self, process_service: ProcessService, dark_mode: bool = False, parent=None):
        super().__init__(parent)
        self.process_service = process_service
        self.dark_mode = dark_mode
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI components"""
        self.setAutoFillBackground(True)
        self.setStyleSheet("background: transparent;")
        layout = QHBoxLayout(self)
        layout.setSpacing(20)
        
        # Left panel - Input form
        self.left_panel = ModernCard(self.dark_mode)
        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(24, 24, 24, 24)
        left_layout.setSpacing(16)
        self.left_panel.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        self.left_panel.setMinimumWidth(350)  # Ensure minimum width for input panel
        
        self.input_title = QLabel('Add Process')
        title_color = ThemeManager.get_text_color(self.dark_mode, "title")
        self.input_title.setStyleSheet(f'font-size: 24px; font-weight: 800; color: {title_color};')
        left_layout.addWidget(self.input_title)
        
        # Input fields
        pid_container, self.pid_input = self._create_input_field('Process ID', 'P1')
        arrival_container, self.arrival_input = self._create_input_field('Arrival Time', '0')
        burst_container, self.burst_input = self._create_input_field('Burst Time', '5')
        priority_container, self.priority_input = self._create_input_field('Priority', '1')
        
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
        self.tq_spinbox.setMinimumWidth(200)
        self.tq_spinbox.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        tq_layout.addWidget(self.tq_spinbox)
        
        left_layout.addWidget(tq_container)
        
        # Buttons
        self.add_btn = QPushButton('➕ Add Process')
        self.add_btn.setMinimumHeight(46)
        self.add_btn.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self._apply_button_style(self.add_btn, 'primary')
        left_layout.addWidget(self.add_btn)
        
        self.upload_btn = QPushButton('📁 Upload File')
        self.upload_btn.setMinimumHeight(46)
        self.upload_btn.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self._apply_button_style(self.upload_btn, 'primary')
        left_layout.addWidget(self.upload_btn)
        
        self.sample_btn = QPushButton('📋 Load Sample')
        self.sample_btn.setObjectName('secondary')
        self.sample_btn.setMinimumHeight(46)
        self.sample_btn.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self._apply_button_style(self.sample_btn, 'secondary')
        left_layout.addWidget(self.sample_btn)
        
        self.clear_btn = QPushButton('🗑️ Clear All')
        self.clear_btn.setObjectName('destructive')
        self.clear_btn.setMinimumHeight(46)
        self.clear_btn.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self._apply_button_style(self.clear_btn, 'destructive')
        left_layout.addWidget(self.clear_btn)
        
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
        self.process_table.setCornerButtonEnabled(False)
        self.process_table.verticalHeader().setVisible(True)
        self.process_table.verticalHeader().setDefaultSectionSize(40)
        right_layout.addWidget(self.process_table)
        
        self.run_btn = QPushButton('🚀 Run Simulation')
        self.run_btn.setObjectName('success')
        self.run_btn.setFixedHeight(56)
        self.run_btn.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self._apply_button_style(self.run_btn, 'success')
        right_layout.addWidget(self.run_btn)
        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.left_panel, 1)
        layout.addWidget(self.right_panel, 3)
        layout.setStretchFactor(self.left_panel, 1)
        layout.setStretchFactor(self.right_panel, 3)
        
        self._refresh_styles()
        # Apply button styles after initialization
        self._force_button_colors()
    
    def _create_input_field(self, label_text, placeholder):
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
        input_field.setMinimumWidth(200)  # Ensure minimum width
        input_field.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        
        layout.addWidget(label)
        layout.addWidget(input_field)
        
        return container, input_field
    
    def _refresh_styles(self):
        """Refresh styles based on theme"""
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
        self._update_table_styles()
    
    def _update_table_styles(self):
        """Update process table styles"""
        if not hasattr(self, "process_table"):
            return
        
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
                QTableWidget::verticalHeader::section {
                    background-color: #f8fafc;
                    color: #1e293b;
                    padding: 8px;
                    border: none;
                    border-right: 2px solid #2563eb;
                    font-weight: 700;
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
                QTableWidget::verticalHeader::section {
                    background-color: #0b1220;
                    color: #e5e7eb;
                    padding: 8px;
                    border: none;
                    border-right: 2px solid #2563eb;
                    font-weight: 700;
                }
            """)
    
    def update_theme(self, dark_mode: bool):
        """Update theme"""
        self.dark_mode = dark_mode
        self._refresh_styles()
        # Force button text colors to be visible
        self._force_button_colors()
    
    def _apply_button_style(self, button, button_type):
        """Apply explicit button style to ensure text is visible"""
        if button_type == 'primary':
            if not self.dark_mode:
                button.setStyleSheet("QPushButton { color: #0f172a !important; border: 1px solid #cbd5e1 !important; background-color: #e2e8f0; }")
            else:
                button.setStyleSheet("QPushButton { color: white !important; }")
        elif button_type == 'secondary':
            if not self.dark_mode:
                button.setStyleSheet("QPushButton#secondary { color: #0f172a !important; }")
            else:
                button.setStyleSheet("QPushButton#secondary { color: #e5e7eb !important; }")
        elif button_type == 'success':
            if not self.dark_mode:
                button.setStyleSheet("QPushButton#success { color: #065f46 !important; }")
            else:
                button.setStyleSheet("QPushButton#success { color: white !important; }")
        elif button_type == 'destructive':
            if not self.dark_mode:
                button.setStyleSheet("QPushButton#destructive { color: #ef4444 !important; }")
            else:
                button.setStyleSheet("QPushButton#destructive { color: #f87171 !important; }")
    
    def _force_button_colors(self):
        """Force button text colors to be visible"""
        self._apply_button_style(self.add_btn, 'primary')
        self._apply_button_style(self.upload_btn, 'primary')
        self._apply_button_style(self.sample_btn, 'secondary')
        self._apply_button_style(self.clear_btn, 'destructive')
        self._apply_button_style(self.run_btn, 'success')
    
    def refresh_process_table(self):
        """Refresh the process table"""
        self.process_table.setRowCount(0)
        
        for i, proc in enumerate(self.process_service.get_all()):
            row = self.process_table.rowCount()
            self.process_table.insertRow(row)
            
            header_item = QTableWidgetItem(str(row + 1))
            header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.process_table.setVerticalHeaderItem(row, header_item)
            
            self.process_table.setItem(row, 0, QTableWidgetItem(proc.pid))
            self.process_table.setItem(row, 1, QTableWidgetItem(str(proc.arrival_time)))
            self.process_table.setItem(row, 2, QTableWidgetItem(str(proc.burst_time)))
            self.process_table.setItem(row, 3, QTableWidgetItem(str(proc.priority)))
    
    def get_time_quantum(self) -> int:
        """Get time quantum value"""
        return self.tq_spinbox.value()
    
    def clear_inputs(self):
        """Clear input fields"""
        self.pid_input.clear()
        self.arrival_input.clear()
        self.burst_input.clear()
        self.priority_input.clear()
    
    def get_input_values(self) -> tuple:
        """Get input values as tuple (pid, arrival, burst, priority)"""
        try:
            pid = self.pid_input.text().strip()
            arrival = int(self.arrival_input.text())
            burst = int(self.burst_input.text())
            priority = int(self.priority_input.text())
            return (pid, arrival, burst, priority)
        except ValueError:
            return (None, None, None, None)


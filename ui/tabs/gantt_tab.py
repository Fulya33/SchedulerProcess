"""Gantt Charts Tab"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt
from ui.components import ModernCard, GanttChart
from themes.theme_manager import ThemeManager
from typing import Dict, List, Optional


class GanttTab(QWidget):
    """Gantt charts tab"""
    
    def __init__(self, dark_mode: bool = False, parent=None):
        super().__init__(parent)
        self.dark_mode = dark_mode
        self.results: Optional[Dict] = None
        self.gantt_widgets: List[GanttChart] = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI components"""
        self.setAutoFillBackground(True)
        self.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(self)
        
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
    
    def display_gantt_charts(self, results: Dict):
        """Display Gantt charts"""
        self.results = results
        
        # Pause all existing animations
        for gantt in self.gantt_widgets:
            gantt.pause()
        
        # Clear existing widgets
        while self.gantt_layout.count():
            child = self.gantt_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.gantt_widgets = []
        
        for result in results.values():
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
        
        min_height = len(results) * 400 + 200
        self.gantt_content.setMinimumHeight(min_height)
        self.gantt_layout.addStretch(1)
    
    def update_theme(self, dark_mode: bool):
        """Update theme"""
        self.dark_mode = dark_mode
        for gantt in self.gantt_widgets:
            gantt.dark_mode = dark_mode
            gantt.draw_chart(len(gantt.gantt_data))
        if self.results:
            self.display_gantt_charts(self.results)



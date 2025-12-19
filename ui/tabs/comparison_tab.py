"""Comparison Tab for Algorithm Comparison"""
import re
from collections import Counter
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure
from ui.components import ModernCard, ScrollFriendlyCanvas
from themes.theme_manager import ThemeManager
from utils.constants import ALGO_COLORS
from typing import Dict, Optional


class ComparisonTab(QWidget):
    """Comparison tab for algorithm comparison"""
    
    def __init__(self, dark_mode: bool = False, parent=None):
        super().__init__(parent)
        self.dark_mode = dark_mode
        self.results: Optional[Dict] = None
        self.algo_colors = ALGO_COLORS.copy()
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI components"""
        self.setAutoFillBackground(True)
        self.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(self)
        
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
    
    def display_comparison(self, results: Dict):
        """Display comparison charts"""
        self.results = results
        
        # Clear existing widgets
        while self.comparison_layout.count():
            child = self.comparison_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        algorithms = list(results.values())
        algo_names = [a['algorithm'] for a in algorithms]
        
        # Update colors for Round Robin
        for result in algorithms:
            if 'Round Robin' in result['algorithm']:
                self.algo_colors[result['algorithm']] = '#6366f1'
        
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
        
        # Add Best Algorithm Analysis Card
        self._add_best_algorithm_analysis(algorithms, short_names, metrics)
        
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
    
    def _add_best_algorithm_analysis(self, algorithms, short_names, metrics):
        """Add best algorithm analysis card"""
        analysis_card = ModernCard(self.dark_mode)
        analysis_layout = QVBoxLayout(analysis_card)
        analysis_layout.setContentsMargins(24, 24, 24, 24)
        
        title = QLabel('📊 Best Algorithm Analysis')
        title_color = ThemeManager.get_text_color(self.dark_mode, "title")
        title.setStyleSheet(f'font-size: 22px; font-weight: 800; margin-bottom: 16px; color: {title_color};')
        analysis_layout.addWidget(title)
        
        # Find best algorithms for each metric
        tat_values = metrics[0][1]
        wt_values = metrics[1][1]
        cpu_values = metrics[2][1]
        
        best_tat_idx = tat_values.index(min(tat_values))
        best_wt_idx = wt_values.index(min(wt_values))
        best_cpu_idx = cpu_values.index(max(cpu_values))  # Higher is better for CPU utilization
        
        analysis_text = f"""
        <div style="line-height: 1.8;">
        <p style="font-size: 14px; margin: 8px 0;">
        <b style="color: {'#2563eb' if not self.dark_mode else '#60a5fa'};">🏆 Best Average Turnaround Time:</b> 
        <span style="color: {'#1e293b' if not self.dark_mode else '#e5e7eb'};">{short_names[best_tat_idx]}</span> 
        ({tat_values[best_tat_idx]:.2f} time units)
        </p>
        <p style="font-size: 14px; margin: 8px 0;">
        <b style="color: {'#10b981' if not self.dark_mode else '#34d399'};">⏱️ Best Average Waiting Time:</b> 
        <span style="color: {'#1e293b' if not self.dark_mode else '#e5e7eb'};">{short_names[best_wt_idx]}</span> 
        ({wt_values[best_wt_idx]:.2f} time units)
        </p>
        <p style="font-size: 14px; margin: 8px 0;">
        <b style="color: {'#6366f1' if not self.dark_mode else '#818cf8'};">💻 Best CPU Utilization:</b> 
        <span style="color: {'#1e293b' if not self.dark_mode else '#e5e7eb'};">{short_names[best_cpu_idx]}</span> 
        ({cpu_values[best_cpu_idx]:.2f}%)
        </p>
        </div>
        """
        
        analysis_label = QLabel(analysis_text)
        analysis_label.setWordWrap(True)
        analysis_label.setTextFormat(Qt.TextFormat.RichText)
        text_color = ThemeManager.get_text_color(self.dark_mode, "label")
        analysis_label.setStyleSheet(f'font-size: 14px; color: {text_color}; padding: 12px;')
        analysis_layout.addWidget(analysis_label)
        
        # Overall winner (if one algorithm wins multiple categories)
        winners = [short_names[best_tat_idx], short_names[best_wt_idx], short_names[best_cpu_idx]]
        winner_counts = Counter(winners)
        overall_winner = winner_counts.most_common(1)[0]
        
        if overall_winner[1] >= 2:
            overall_text = f"""
            <p style="font-size: 15px; margin-top: 12px; padding-top: 12px; border-top: 2px solid {'#e5e7eb' if not self.dark_mode else '#334155'};">
            <b style="color: {'#f59e0b' if not self.dark_mode else '#fbbf24'};">⭐ Overall Best:</b> 
            <span style="color: {'#1e293b' if not self.dark_mode else '#e5e7eb'}; font-weight: 700;">{overall_winner[0]}</span> 
            (wins {overall_winner[1]} out of 3 categories)
            </p>
            """
            overall_label = QLabel(overall_text)
            overall_label.setWordWrap(True)
            overall_label.setTextFormat(Qt.TextFormat.RichText)
            overall_label.setStyleSheet(f'font-size: 15px; color: {text_color}; padding: 12px;')
            analysis_layout.addWidget(overall_label)
        
        self.comparison_layout.addWidget(analysis_card)
    
    def update_theme(self, dark_mode: bool):
        """Update theme"""
        self.dark_mode = dark_mode
        if self.results:
            self.display_comparison(self.results)


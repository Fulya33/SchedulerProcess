"""Gantt Chart Component"""
import matplotlib
matplotlib.use('qtagg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer


class ScrollFriendlyCanvas(FigureCanvasQTAgg):
    """Canvas that doesn't capture scroll events"""
    def __init__(self, figure):
        super().__init__(figure)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def wheelEvent(self, event):
        event.ignore()


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


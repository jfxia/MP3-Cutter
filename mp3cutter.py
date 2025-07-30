# mp3cutter-c.py

import sys
import os
import base64
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QLabel, QFileDialog,
                            QSlider, QTimeEdit, QMessageBox, QProgressBar,
                            QFrame, QInputDialog, QSizePolicy)
from PyQt5.QtCore import Qt, QUrl, QTime, QThread, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QIcon, QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
plt.rcParams["font.family"] = ["Segoe UI", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
from pydub import AudioSegment
import math

ICON_FOLDER_OPEN = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgY2xhc3M9ImZlYXRoZXIgZmVhdGhlci1mb2xkZXIiPjxwYXRoIGQ9Ik0yMiAxMS4wOFYxMiBDMjIgMTYgMjEgMTcgMTggMTcuNUMxNSAxOCAxNCAxOCAxMCAxOFoiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMS41IiBzdHJva2UtbWl0ZXJsaW1pdD0iMTAiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPjxwYXRoIGQ9Ik0xNyAySDdhNS4wMDYgNS4wMDYgMCAwMC01IDV2NmExIDEgMCAwMDBoOHYtMmgtMXYtM2g4djNhMSAxIDAgMDAxIDFoMWEyIDIgMCAwMDAtNGgtM3YtM2g0YTIgMiAwIDAwMi0ydi0xYTIgMiAwIDAwLTItMkg3YTIgMiAwIDAwLTIgMnY2YTcgNy45OSA3Ljk5IDAgMDExNiAweiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1taXRlcmxpbWl0PSIxMCIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+PC9zdmc+"
ICON_SAVE = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgY2xhc3M9ImZlYXRoZXIgZmVhdGhlci1zYXZlIj48cGF0aCBkPSJNMTkgMjFIMThhMiAyIDAgMDEtMi0yVjExYTIgMiAwIDAxMi0yaDFhMiAyIDAgMDEyIDJ2OGEyIDIgMCAwMS0yIDJ6Ii8+PHBhdGggZD0iTTcgM2gxMGE0IDQgMCAwMTAgOGgtMWwtMSAyaC0xMHYtOGE0IDQgMCAwMTEtNGgzeiIvPjwvc3ZnPg=="
ICON_CANCEL = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgY2xhc3M9ImZlYXRoZXIgZmVhdGhlci14Ij48bGluZTEgeDE9IjE4IiB5MT0iNiIgeDI9IjYiIHkyPSIxOCIvPjxsaW5lMiB4MT0iNiIgeTE9IjYiIHgyPSIxOCIgeTI9IjE4Ii8+PC9zdmc+"
ICON_PLAY = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0iZmVhdGhlciBmZWF0aGVyLXBsYXkiPjxwb2x5Z29uIHBvaW50cz0iNSA0IDE5IDEyIDUgMjAiIGZpbGw9IndoaXRlIiBzdHJva2U9Im5vbmUiLz48L3N2Zz4="
ICON_PAUSE = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJ3aGl0ZSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJmZWF0aGVyIGZlYXRoZXItcGF1c2UiPjxyZWN0IHg9IjYiIHk9IjQiIHdpZHRoPSI0IiBoZWlnaHQ9IjE2IiBmaWxsPSJ3aGl0ZSIgc3Ryb2tlPSJub25lIi8+PHJlY3QgeD0iMTQiIHk9IjQiIHdpZHRoPSI0IiBoZWlnaHQ9IjE2IiBmaWxsPSJ3aGl0ZSIgc3Ryb2tlPSJub25lIi8+PC9zdmc+"
ICON_STOP = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJ3aGl0ZSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJmZWF0aGVyIGZlYXRoZXItc3F1YXJlIj48cmVjdCB4PSI1IiB5PSI1IiB3aWR0aD0iMTQiIGhlaWdodD0iMTQiIHJ4PSIyIiByeT0iMiIgZmlsbD0id2hpdGUiIHN0cm9rZT0ibm9uZSIvPjwvc3ZnPg=="

def get_icon_from_b64(b64_data):
    missing_padding = len(b64_data) % 4
    if missing_padding:
        b64_data += '=' * (4 - missing_padding)
    pixmap = QPixmap()
    pixmap.loadFromData(base64.b64decode(b64_data))
    return QIcon(pixmap)

MAX_WAVEFORM_SAMPLES = 50000
CHUNK_SIZE_MS = 10000
SCREEN_MARKER_SIZE = 30
DARK_BACKGROUND_COLOR = '#1e1e2e'
PANEL_BACKGROUND_COLOR = '#2d2d3d'
TEXT_COLOR = '#efefef'
ACCENT_COLOR = '#0080ff'
ACCENT_HOVER_COLOR = '#5ca2f0'
ACCENT_PRESSED_COLOR = '#3a7bc8'
SUCCESS_COLOR = '#5ca2f0'
DANGER_COLOR = '#777777'
WAVEFORM_COLOR = '#00aeff'
WAVEFORM_BG_COLOR = '#252536'
GRID_COLOR = '#3a3a4a'
SLIDER_HANDLE_COLOR = '#ffffff'
SLIDER_GROOVE_COLOR = '#555566'
HIGHLIGHT_COLOR = '#ffff0040'  # Semi-transparent yellow

class WaveformLoadingThread(QThread):
    progress_updated = pyqtSignal(int)
    loading_finished = pyqtSignal(object, int)
    loading_error = pyqtSignal(str)
    def __init__(self, audio_file):
        super().__init__()
        self.audio_file = audio_file
        self.stop_flag = False
    def run(self):
        try:
            audio = AudioSegment.from_file(self.audio_file)
            duration_ms = len(audio)
            sample_rate = audio.frame_rate
            total_samples = int(duration_ms / 1000 * sample_rate)
            step = max(1, total_samples // MAX_WAVEFORM_SAMPLES)
            all_samples = []
            start_ms = 0
            while start_ms < duration_ms and not self.stop_flag:
                end_ms = min(start_ms + CHUNK_SIZE_MS, duration_ms)
                chunk = audio[start_ms:end_ms].set_channels(1)
                chunk_samples = np.array(chunk.get_array_of_samples())
                if step > 1:
                    chunk_samples = chunk_samples[::step]
                all_samples.extend(chunk_samples)
                start_ms = end_ms
                progress = min(100, int(start_ms * 100 / duration_ms))
                self.progress_updated.emit(progress)
                self.msleep(10)
            if self.stop_flag:
                return
            samples = np.array(all_samples)
            duration = duration_ms / 1000
            times = np.linspace(0, duration, len(samples))
            self.loading_finished.emit((samples, times, duration), sample_rate)
        except Exception as e:
            self.loading_error.emit(f"Loading Error: {str(e)}")
    def stop(self):
        self.stop_flag = True
        self.wait()

class WaveformCanvas(FigureCanvas):
    def __init__(self, main_window, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor=DARK_BACKGROUND_COLOR)
        self.axes = self.fig.add_subplot(111)
        super(WaveformCanvas, self).__init__(self.fig)
        self.setParent(parent)
        self.main_window = main_window
        self.fig.patch.set_facecolor(DARK_BACKGROUND_COLOR)
        self.stylize_axes()
        self.fig.tight_layout()
        self.audio_samples, self.times, self.sample_rate = None, None, None
        self.duration, self.start_mark, self.end_mark = 0, 0, 0
        self.start_marker, self.end_marker = None, None
        self.highlight_area = None
        self.is_loaded = False
        self.dragging = None
        self.xlim, self.ylim = None, None
        self.mpl_connect('button_press_event', self.on_click)
        self.mpl_connect('motion_notify_event', self.on_motion)
        self.mpl_connect('button_release_event', self.on_release)
        self.mpl_connect('scroll_event', self.on_scroll)

    def stylize_axes(self):
        self.axes.set_facecolor(WAVEFORM_BG_COLOR)
        for spine in self.axes.spines.values():
            spine.set_edgecolor(GRID_COLOR)
        self.axes.tick_params(axis='x', colors=TEXT_COLOR)
        self.axes.tick_params(axis='y', colors=TEXT_COLOR)
        self.axes.xaxis.label.set_color(TEXT_COLOR)
        self.axes.yaxis.label.set_color(TEXT_COLOR)
        self.axes.title.set_color(TEXT_COLOR)
        self.axes.grid(True, color=GRID_COLOR, linestyle='--', linewidth=0.5, alpha=0.7)
        for s in self.axes.spines.values():
            s.set_color(GRID_COLOR)

    def clear(self):
        self.axes.clear()
        self.stylize_axes()
        self.start_marker, self.end_marker = None, None
        try:
            if self.highlight_area is not None:
                self.highlight_area.remove()
        except Exception:
            pass
        self.highlight_area = None
        self.audio_samples, self.times, self.sample_rate = None, None, None
        self.duration, self.start_mark, self.end_mark = 0, 0, 0
        self.is_loaded, self.dragging = False, None
        self.xlim, self.ylim = None, None
        self.draw()

    def plot_waveform(self, samples, times, duration, sample_rate):
        self.clear()
        self.audio_samples, self.times, self.sample_rate = samples, times, sample_rate
        self.duration, self.is_loaded = duration, True
        self.axes.plot(times, samples, color=WAVEFORM_COLOR, linewidth=0.8)
        self.axes.set_xlabel('Time (s)', color=TEXT_COLOR)
        self.axes.set_ylabel('Amplitude', color=TEXT_COLOR)
        self.axes.set_title('Audio Waveform (Scroll to Zoom)', color=TEXT_COLOR)
        self.axes.set_xlim(0, self.duration)
        self.xlim = (0, self.duration)
        self.start_mark = max(0.01, self.duration * 0.01)
        self.end_mark = min(self.duration - 0.01, self.duration * 0.99)
        self.axes.autoscale(enable=True, axis='y')
        self.ylim = self.axes.get_ylim()
        self._draw_highlight()
        self._draw_markers()
        self.fig.tight_layout()
        self.draw()

    def _draw_highlight(self):
        if self.highlight_area:
            self.highlight_area.remove()
            self.highlight_area = None
        if self.is_loaded and self.start_mark is not None and self.end_mark is not None:
            self.ylim = self.axes.get_ylim()
            x_coords = [self.start_mark, self.end_mark, self.end_mark, self.start_mark]
            y_coords = [self.ylim[0], self.ylim[0], self.ylim[1], self.ylim[1]]
            self.highlight_area = Polygon(
                list(zip(x_coords, y_coords)),
                facecolor=HIGHLIGHT_COLOR,
                edgecolor='none',
                zorder=5
            )
            self.axes.add_patch(self.highlight_area)

    def _create_triangle_marker(self, x, color, direction='up'):
        self.ylim = self.axes.get_ylim()
        x_screen = self.axes.transData.transform((x, 0))[0]
        if direction == 'up':
            y_pos_screen = self.axes.transData.transform((x, self.ylim[1] * 0.9))[1]
            points_screen = [
                [x_screen, y_pos_screen],
                [x_screen - SCREEN_MARKER_SIZE, y_pos_screen + SCREEN_MARKER_SIZE],
                [x_screen + SCREEN_MARKER_SIZE, y_pos_screen + SCREEN_MARKER_SIZE]
            ]
        else:
            y_pos_screen = self.axes.transData.transform((x, self.ylim[0] * 0.9))[1]
            points_screen = [
                [x_screen, y_pos_screen],
                [x_screen - SCREEN_MARKER_SIZE, y_pos_screen - SCREEN_MARKER_SIZE],
                [x_screen + SCREEN_MARKER_SIZE, y_pos_screen - SCREEN_MARKER_SIZE]
            ]
        points_data = [self.axes.transData.inverted().transform((px, py)) for px, py in points_screen]
        triangle = Polygon(points_data, facecolor=color, edgecolor=TEXT_COLOR, linewidth=1, zorder=10)
        self.axes.add_patch(triangle)
        return triangle

    def _draw_markers(self):
        if self.start_marker:
            self.start_marker.remove()
            self.start_marker = None
        if self.end_marker:
            self.end_marker.remove()

            self.end_marker = None
        self.ylim = self.axes.get_ylim()
        if self.is_loaded:
            self.start_marker = self._create_triangle_marker(self.start_mark, SUCCESS_COLOR, 'up')
            self.end_marker = self._create_triangle_marker(self.end_mark, DANGER_COLOR, 'down')
            if not hasattr(self, 'legend') or self.legend not in self.axes.get_legend_handles_labels()[1]:
                self.legend = self.axes.legend([self.start_marker, self.end_marker], ['Start', 'End'],
                                               loc='upper right', frameon=True, labelcolor=TEXT_COLOR)
                frame = self.legend.get_frame()
                frame.set_facecolor(PANEL_BACKGROUND_COLOR)
                frame.set_edgecolor(GRID_COLOR)
        self._draw_highlight()
        self.draw_idle()

    def _is_point_inside_marker(self, x, y):
        if not self.ylim or not self.is_loaded or not self.axes:
            return False, None
        try:
            display_coords = self.axes.transData.transform((x, y))
            is_inside_start = self.start_marker and self.start_marker.contains_point(display_coords)
            is_inside_end = self.end_marker and self.end_marker.contains_point(display_coords)
            if is_inside_start and is_inside_end:
                if self.dragging == 'start':
                    return True, 'start'
                elif self.dragging == 'end':
                    return True, 'end'
                else:
                    dist_to_start = abs(x - self.start_mark)
                    dist_to_end = abs(x - self.end_mark)
                    return (True, 'start') if dist_to_start <= dist_to_end else (True, 'end')
            if is_inside_start:
                return True, 'start'
            elif is_inside_end:
                return True, 'end'
            if abs(x - self.start_mark) < 0.3:
                return True, 'start'
            if abs(x - self.end_mark) < 0.3:
                return True, 'end'
            return False, None
        except Exception:
            return False, None

    def on_click(self, event):
        if not self.is_loaded or event.inaxes != self.axes or event.xdata is None:
            self.dragging = None
            return
        is_inside, marker_type = self._is_point_inside_marker(event.xdata, event.ydata)
        if is_inside:
            self.dragging = marker_type
            return
        if event.button == 1:
            self.start_mark = max(0, min(event.xdata, self.end_mark - 0.01))
            self._draw_markers()
            self.main_window.update_time_edits()
        elif event.button == 3:
            self.end_mark = min(self.duration, max(event.xdata, self.start_mark + 0.01))
            self._draw_markers()
            self.main_window.update_time_edits()
        self.dragging = None

    ### FIX: 优化 on_motion，end_mark 向右拖动不再卡顿，避免带动 start_mark
    def on_motion(self, event):
        if not self.is_loaded or self.dragging is None or event.inaxes != self.axes or event.xdata is None:
            return
        x = event.xdata
        if self.dragging == 'start':
            new_start = max(0, min(x, self.end_mark - 0.01))
            if abs(new_start - self.start_mark) > 1e-6:
                self.start_mark = new_start
                self._draw_markers()
                self.main_window.update_time_edits()
        elif self.dragging == 'end':
            new_end = min(max(x, self.start_mark + 0.01), self.duration)
            if abs(new_end - self.end_mark) > 1e-6:
                self.end_mark = new_end
                self._draw_markers()
                self.main_window.update_time_edits()

    def on_release(self, event):
        self.dragging = None
        self.draw()

    def on_scroll(self, event):
        if not self.is_loaded or event.inaxes != self.axes:
            return
        cur_xlim = self.axes.get_xlim()
        xdata = event.xdata
        scale_factor = 1.3 if event.button == 'up' else 1 / 1.3
        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        rel_pos = (xdata - cur_xlim[0]) / (cur_xlim[1] - cur_xlim[0])
        new_xlim = (xdata - new_width * rel_pos, xdata + new_width * (1 - rel_pos))
        new_xlim = (max(0, new_xlim[0]), min(self.duration, new_xlim[1]))
        self.axes.set_xlim(new_xlim)
        self.xlim = new_xlim
        self._draw_markers()
        self.draw_idle()

    def set_start_mark(self, value):
        clamped_value = max(0, min(value, self.end_mark - 0.01))
        if abs(clamped_value - self.start_mark) > 1e-9:
            self.start_mark = clamped_value
            self._draw_markers()
            return True
        return False

    def set_end_mark(self, value):
        clamped_value = min(max(value, self.start_mark + 0.01), self.duration)
        if abs(clamped_value - self.end_mark) > 1e-9:
            self.end_mark = clamped_value
            self._draw_markers()
            return True
        return False

    def get_selected_range(self):
        return self.start_mark, self.end_mark

class ProcessingThread(QThread):
    progress_updated = pyqtSignal(int)
    processing_finished = pyqtSignal(str)
    processing_error = pyqtSignal(str)
    def __init__(self, input_file, output_file, start_time, end_time):
        super().__init__()
        self.input_file, self.output_file = input_file, output_file
        self.start_time, self.end_time = start_time * 1000, end_time * 1000
        self.stop_flag = False
    def run(self):
        try:
            self.progress_updated.emit(5)
            audio = AudioSegment.from_file(self.input_file)
            self.progress_updated.emit(15)
            if not (0 <= self.start_time < self.end_time <= len(audio)):
                self.processing_error.emit("Invalid clipping range.")
                return
            trimmed_audio = audio[self.start_time:self.end_time]
            self.progress_updated.emit(60)
            bitrate = f"{audio.frame_rate//1000}k" if audio.frame_rate > 0 else "192k"
            trimmed_audio.export(self.output_file, format="mp3", bitrate=bitrate, parameters=["-q:a", "0"])
            self.progress_updated.emit(100)
            if not self.stop_flag:
                self.processing_finished.emit(self.output_file)
        except Exception as e:
            if not self.stop_flag:
                self.processing_error.emit(f"Processing Error: {str(e)}")
    def stop(self):
        self.stop_flag = True
        self.wait()

class MP3Cutter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.audio_file, self.audio_segment = None, None
        self.loading_thread, self.processing_thread = None, None
        self.playback_end_time = None
        self.player = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)
        self.player.stateChanged.connect(self.update_player_state)
        self._updating_time_edit = False

    def init_ui(self):
        self.setWindowTitle('MP3 Cutter')
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 650)
        self.setWindowIcon(get_icon_from_b64(ICON_PLAY))
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        file_area = QFrame()
        file_area.setObjectName("PanelFrame")
        file_layout = QVBoxLayout(file_area)
        file_layout.setContentsMargins(15, 15, 15, 15)
        file_layout.setSpacing(10)
        self.file_label = QLabel('Drag & drop an audio file here')
        self.file_label.setAlignment(Qt.AlignCenter)
        self.file_label.setObjectName("DropLabel")

        file_controls = QHBoxLayout()
        file_controls.setSpacing(10)
        self.select_btn = QPushButton("Load MP3 File ...")
        #self.select_btn.setIcon(get_icon_from_b64(ICON_FOLDER_OPEN))
        self.select_btn.clicked.connect(self.select_file)
        self.select_btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        self.cancel_load_btn = QPushButton("Cancel Load")
        self.cancel_load_btn.clicked.connect(self.cancel_loading)
        self.cancel_load_btn.setEnabled(False)
        self.cancel_load_btn.setObjectName("DangerButton")
        self.cancel_load_btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        file_controls.addStretch()
        file_controls.addWidget(self.select_btn)
        file_controls.addWidget(self.cancel_load_btn)
        file_controls.addStretch()
        self.load_progress_bar = QProgressBar()
        self.load_progress_bar.setVisible(False)
        self.load_progress_bar.setObjectName("LoadProgressBar")
        file_layout.addWidget(self.file_label)
        file_layout.addLayout(file_controls)
        file_layout.addWidget(self.load_progress_bar)
        waveform_frame = QFrame()
        waveform_frame.setObjectName("WaveformFrame")
        waveform_layout = QVBoxLayout(waveform_frame)
        waveform_layout.setContentsMargins(0, 0, 0, 0)
        self.wave_canvas = WaveformCanvas(self, width=10, height=4, dpi=100)
        waveform_layout.addWidget(self.wave_canvas)
        controls_area = QFrame()
        controls_area.setObjectName("PanelFrame")
        controls_layout = QVBoxLayout(controls_area)
        controls_layout.setContentsMargins(15, 15, 15, 15)
        controls_layout.setSpacing(15)
        time_layout = QHBoxLayout()
        time_layout.setSpacing(10)
        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setDisplayFormat("HH:mm:ss.zzz")
        self.start_time_edit.setObjectName("TimeEdit")
        self.end_time_edit = QTimeEdit()
        self.end_time_edit.setDisplayFormat("HH:mm:ss.zzz")
        self.end_time_edit.setObjectName("TimeEdit")
        time_layout.addWidget(QLabel("Start:"), 0)
        time_layout.addWidget(self.start_time_edit, 1)
        time_layout.addSpacing(20)
        time_layout.addWidget(QLabel("End:"), 0)
        time_layout.addWidget(self.end_time_edit, 1)
        time_layout.addStretch()
        play_layout = QHBoxLayout()
        play_layout.setSpacing(10)
        play_button_group = QHBoxLayout()
        play_button_group.setSpacing(5)
        self.play_btn = QPushButton()
        self.play_btn.setIcon(get_icon_from_b64(ICON_PLAY))
        self.play_btn.setObjectName("PlayerButton")
        self.play_btn.clicked.connect(self.play_audio)
        self.play_btn.setEnabled(False)
        self.pause_btn = QPushButton()
        self.pause_btn.setIcon(get_icon_from_b64(ICON_PAUSE))
        self.pause_btn.setObjectName("PlayerButton")
        self.pause_btn.clicked.connect(self.pause_audio)
        self.pause_btn.setEnabled(False)
        self.stop_btn = QPushButton()
        self.stop_btn.setIcon(get_icon_from_b64(ICON_STOP))
        self.stop_btn.setObjectName("PlayerButton")
        self.stop_btn.clicked.connect(self.stop_audio)
        play_button_group.addWidget(self.play_btn)
        play_button_group.addWidget(self.pause_btn)
        play_button_group.addWidget(self.stop_btn)
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setObjectName("PositionSlider")
        self.position_slider.sliderMoved.connect(self.set_position)
        play_layout.addLayout(play_button_group)
        play_layout.addSpacing(15)
        play_layout.addWidget(self.position_slider, 1)
        controls_layout.addLayout(time_layout)
        controls_layout.addLayout(play_layout)
        export_area = QHBoxLayout()
        export_area.setSpacing(10)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setObjectName("ExportProgressBar")
        self.export_btn = QPushButton("Export Clip")
        self.export_btn.clicked.connect(self.export_audio)
        self.export_btn.setEnabled(False)
        self.export_btn.setObjectName("SuccessButton")
        self.export_btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        export_area.addWidget(self.progress_bar, 1)
        export_area.addWidget(self.export_btn)
        main_layout.addWidget(file_area)
        main_layout.addWidget(waveform_frame, 1)
        main_layout.addWidget(controls_area)
        main_layout.addLayout(export_area)
        self.setAcceptDrops(True)
        file_area.setAcceptDrops(True)
        file_area.dragEnterEvent = self.drag_enter_event
        file_area.dropEvent = self.drop_event
        self.show()

    def drag_enter_event(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def drop_event(self, event: QDropEvent):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')):
                self.load_audio_file(file_path)
                break

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav *.ogg *.flac)")
        if file_path:
            self.load_audio_file(file_path)

    def load_audio_file(self, file_path):
        if self.loading_thread and self.loading_thread.isRunning():
            self.loading_thread.stop()
        self.wave_canvas.clear()
        self.audio_file = file_path
        self.audio_segment = None
        file_name = os.path.basename(file_path)
        self.file_label.setText(f'Loading: {file_name}')
        self.load_progress_bar.setVisible(True)
        self.load_progress_bar.setValue(0)
        self.select_btn.setEnabled(False)
        self.cancel_load_btn.setEnabled(True)
        self.export_btn.setEnabled(False)
        self.play_btn.setEnabled(False)
        self.loading_thread = WaveformLoadingThread(file_path)
        self.loading_thread.progress_updated.connect(self.load_progress_bar.setValue)
        self.loading_thread.loading_finished.connect(self.on_loading_finished)
        self.loading_thread.loading_error.connect(self.on_loading_error)
        self.loading_thread.start()

    def cancel_loading(self):
        if self.loading_thread and self.loading_thread.isRunning():
            self.loading_thread.stop()
            self.on_loading_canceled()

    def on_loading_canceled(self):
        self.file_label.setText('Drag & drop an audio file here')
        self.load_progress_bar.setVisible(False)
        self.select_btn.setEnabled(True)
        self.cancel_load_btn.setEnabled(False)
        self.wave_canvas.clear()
        self.audio_file = None

    def on_loading_finished(self, waveform_data, sample_rate):
        samples, times, duration = waveform_data
        file_name = os.path.basename(self.audio_file)
        self.file_label.setText(f'【 {file_name} ({duration:.2f}s)】')
        self.load_progress_bar.setVisible(False)
        self.select_btn.setEnabled(True)
        self.cancel_load_btn.setEnabled(False)
        self.export_btn.setEnabled(True)
        self.play_btn.setEnabled(True)
        self.wave_canvas.plot_waveform(samples, times, duration, sample_rate)
        try:
            self.audio_segment = AudioSegment.from_file(self.audio_file)
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.audio_file)))
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Failed to prepare audio for playback: {str(e)}")
        self.update_time_edits()
        try:
            self.start_time_edit.timeChanged.disconnect()
            self.end_time_edit.timeChanged.disconnect()
        except TypeError:
            pass
        self.start_time_edit.timeChanged.connect(self.on_start_time_changed)
        self.end_time_edit.timeChanged.connect(self.on_end_time_changed)

    def on_loading_error(self, error_msg):
        QMessageBox.critical(self, "Loading Error", error_msg)
        self.on_loading_canceled()

    def reset(self):
        if self.loading_thread and self.loading_thread.isRunning():
            self.loading_thread.stop()
            self.on_loading_canceled()

    def update_time_edits(self):
        start, end = self.wave_canvas.get_selected_range()
        self.start_time_edit.setTime(QTime(0, 0, 0).addMSecs(int(start * 1000)))
        self.end_time_edit.setTime(QTime(0, 0, 0).addMSecs(int(end * 1000)))

    def on_start_time_changed(self, time: QTime):
        if self._updating_time_edit or not self.wave_canvas.is_loaded:
            return
        self._updating_time_edit = True
        total_msecs = QTime(0, 0, 0).msecsTo(time)
        time_in_seconds = total_msecs / 1000.0
        self.wave_canvas.set_start_mark(time_in_seconds)
        self._updating_time_edit = False

    def on_end_time_changed(self, time: QTime):
        if self._updating_time_edit or not self.wave_canvas.is_loaded:
            return
        self._updating_time_edit = True
        total_msecs = QTime(0, 0, 0).msecsTo(time)
        time_in_seconds = total_msecs / 1000.0
        self.wave_canvas.set_end_mark(time_in_seconds)
        self._updating_time_edit = False

    def play_audio(self):
        if not self.player.isAvailable() or not self.wave_canvas.is_loaded:
            return
        start, end = self.wave_canvas.get_selected_range()
        self.playback_end_time = int(end * 1000)
        self.player.setPosition(int(start * 1000))
        self.player.play()

    def pause_audio(self):
        self.player.pause()

    def stop_audio(self):
        self.player.stop()
        self.playback_end_time = None

    def update_position(self, position):
        if self.playback_end_time is not None and position >= self.playback_end_time:
            self.stop_audio()
        else:
            if not self.position_slider.isSliderDown():
                self.position_slider.setValue(position)

    def update_duration(self, duration):
        self.position_slider.setRange(0, duration)

    def set_position(self, position):
        self.player.setPosition(position)

    def update_player_state(self, state):
        self.play_btn.setEnabled(state != QMediaPlayer.PlayingState)
        self.pause_btn.setEnabled(state == QMediaPlayer.PlayingState)

    def export_audio(self):
        if not self.audio_file or not self.wave_canvas.is_loaded:
            return
        default_name = f"{os.path.splitext(os.path.basename(self.audio_file))[0]}_clipped.mp3"
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Clipped File", default_name, "MP3 Files (*.mp3)")
        if save_path:
            if not save_path.lower().endswith('.mp3'):
                save_path += '.mp3'
            if os.path.abspath(save_path) == os.path.abspath(self.audio_file):
                QMessageBox.warning(self, "Warning", "Cannot overwrite original. Choose a different name.")
                return
            start, end = self.wave_canvas.get_selected_range()
            self.processing_thread = ProcessingThread(self.audio_file, save_path, start, end)
            self.processing_thread.progress_updated.connect(self.progress_bar.setValue)
            self.processing_thread.processing_finished.connect(self.on_processing_finished)
            self.processing_thread.processing_error.connect(self.on_processing_error)
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.export_btn.setEnabled(False)
            self.select_btn.setEnabled(False)
            self.processing_thread.start()

    def on_processing_finished(self, file_path):
        self.progress_bar.setVisible(False)
        self.export_btn.setEnabled(True)
        self.select_btn.setEnabled(True)
        QMessageBox.information(self, "Success", f"Audio clip saved to:\n{file_path}")

    def on_processing_error(self, error_msg):
        self.progress_bar.setVisible(False)
        self.export_btn.setEnabled(True)
        self.select_btn.setEnabled(True)
        QMessageBox.critical(self, "Error", error_msg)

    def closeEvent(self, event):
        self.player.stop()
        if self.loading_thread and self.loading_thread.isRunning():
            self.loading_thread.stop()
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("MP3 Cutter Pro")
    STYLESHEET = f"""
        QMainWindow, QDialog, QMessageBox {{
            background-color: {DARK_BACKGROUND_COLOR};
            font-family: "Segoe UI", "Microsoft YaHei", "Arial", sans-serif;
            font-size: 20px;
        }}
        QFrame#PanelFrame {{
            background-color: {PANEL_BACKGROUND_COLOR};
            border-radius: 10px;
            padding: 15px;
            border: 1px solid {GRID_COLOR};
        }}
        QFrame#WaveformFrame {{
            background-color: {WAVEFORM_BG_COLOR};
            border-radius: 8px;
            padding: 10px;
            border: 1px solid {GRID_COLOR};
        }}
        QLabel {{
            color: {TEXT_COLOR};
            font-size: 20px;
        }}
        QLabel#DropLabel {{
            background-color: rgba(45, 45, 61, 0.5); /* Semi-transparent */
            border: 2px dashed {GRID_COLOR};
            border-radius: 8px;
            font-size: 20px;
            font-weight: 500;
            color: #ffff00;
            padding: 30px;
        }}
        QPushButton {{
            background-color: {ACCENT_COLOR};
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 20px;
            font-weight: 600;
            border-radius: 6px;
            min-height: 36px;
            min-width: 90px;
        }}
        QPushButton:hover {{
            background-color: {ACCENT_HOVER_COLOR};
        }}
        QPushButton:pressed {{
            background-color: {ACCENT_PRESSED_COLOR};
        }}
        QPushButton:disabled {{
            background-color: #444455;
            color: #888899;
        }}
        QPushButton#SuccessButton {{
            background-color: {SUCCESS_COLOR};
        }}
        QPushButton#SuccessButton:hover {{
            background-color: #0080ff;
        }}
        QPushButton#SuccessButton:pressed {{
            background-color: #388e3c;
        }}
        QPushButton#DangerButton {{
            background-color: {DANGER_COLOR};
        }}
        QPushButton#DangerButton:hover {{
            background-color: #ef5350;
        }}
        QPushButton#DangerButton:pressed {{
            background-color: #d32f2f;
        }}


        QPushButton#PlayerButton {{
            background-color: {PANEL_BACKGROUND_COLOR};
            border: 1px solid {GRID_COLOR};
            border-radius: 22px;
            width: 44px;
            height: 44px;
            padding: 0px;
        }}
        QPushButton#PlayerButton:hover {{
            background-color: #3a3a4a;
            border-color: {ACCENT_COLOR};
        }}
        QPushButton#PlayerButton:pressed {{
            background-color: {ACCENT_COLOR};
        }}
        QPushButton#PlayerButton:disabled {{
            background-color: {PANEL_BACKGROUND_COLOR};
            border-color: #444455;
        }}
        QPushButton#PlayerButton:disabled QIcon {{
            /* color: #888899; */
        }}
        QTimeEdit {{
            background-color: {DARK_BACKGROUND_COLOR};
            color: {TEXT_COLOR};
            border: 1px solid {GRID_COLOR};
            border-radius: 5px;
            padding: 8px;
            font-size: 20px;
            selection-background-color: {ACCENT_COLOR};
            min-width: 140px;
        }}
        QTimeEdit:focus {{
            border: 1px solid {ACCENT_COLOR};
        }}
        QTimeEdit#TimeEdit {{
        }}
        QSlider#PositionSlider::groove:horizontal {{
            height: 8px;
            background: {SLIDER_GROOVE_COLOR};
            margin: 2px 0;
            border-radius: 4px;
        }}
        QSlider#PositionSlider::handle:horizontal {{
            background: {SLIDER_HANDLE_COLOR};
            border: 1px solid {GRID_COLOR};
            width: 18px;
            height: 18px;
            margin: -5px 0;
            border-radius: 9px;
        }}
        QSlider#PositionSlider::handle:horizontal:hover {{
            background: {ACCENT_COLOR};
            border-color: {ACCENT_COLOR};
        }}
        QSlider#PositionSlider::sub-page:horizontal {{
            background: {ACCENT_COLOR};
            border-radius: 4px;
        }}
        QProgressBar {{
            border-radius: 6px;
            text-align: center;
            color: {TEXT_COLOR};
            background-color: {DARK_BACKGROUND_COLOR};
            border: 1px solid {GRID_COLOR};
            height: 24px;
            font-size: 15px;
        }}
        QProgressBar::chunk {{
            background-color: {ACCENT_COLOR};
            border-radius: 5px;
        }}
        QProgressBar#LoadProgressBar::chunk {{
             background-color: #FFFFCC;
        }}
        QProgressBar#ExportProgressBar::chunk {{
             background-color: {SUCCESS_COLOR};
        }}
        QMessageBox QLabel {{
            color: {TEXT_COLOR};
            font-size: 20px;
        }}
        QMessageBox QPushButton {{
            min-width: 100px;
            padding: 10px 20px;
            font-size: 20px;
        }}
        QScrollBar:vertical {{
            background: {PANEL_BACKGROUND_COLOR};
            width: 17px;
            border-radius: 8px;
            margin: 15px 3px 15px 3px;
        }}
        QScrollBar::handle:vertical {{
            background: {GRID_COLOR};
            border-radius: 8px;
            min-height: 20px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {ACCENT_COLOR};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
            background: none;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}
    """
    app.setStyleSheet(STYLESHEET)
    window = MP3Cutter()
    sys.exit(app.exec_())
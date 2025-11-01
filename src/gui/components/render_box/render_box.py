import os, json, base64
import time
from PySide6.QtWidgets import (
    QWidget, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout,
    QSizePolicy, QPushButton, QStackedLayout
)
from PySide6.QtCore import Qt, Slot, QProcess, QByteArray, QEvent
from PySide6.QtGui import QPixmap, QCursor

from core.state_global.hwnd import hwndState
from core.capture_exaple import capture_window_by_hwnd, pil_image_to_png_bytes
from core.window_controller import set_window_always_on_top

script_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "workers", "capture_worker.py")
)

class Render_box(QWidget):
    def __init__(self, frames_per_milliseconds=100):
        super().__init__()
        self.process = None
        self.frames_per_milliseconds = frames_per_milliseconds
        self.frame_count = 0
        self.last_fps_time = time.time()
        self.current_fps = 0
        self.setup_ui()
        hwndState.change_hwnd.connect(self.get_hwnd_and_print)
        self.bar_options.hide()  # Oculta al iniciar



    def setup_ui(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stack = QStackedLayout(self)   # renombrado para no chocar con QWidget.layout()
        self.stack.setContentsMargins(0, 0, 0, 0)

        # Imagen principal

        self.image = QWidget()
        self.image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_layout =  QGridLayout(self.image)
        self.imagen_label = QLabel('viewing window')
        self.imagen_label.setAlignment(Qt.AlignCenter)
        self.image_layout.addWidget(self.imagen_label)
        self.stack.addWidget(self.image)


        # --- Overlay con barra en el bottom ---
        self.overlay = QWidget()
        overlay_layout = QVBoxLayout(self.overlay)
        overlay_layout.setContentsMargins(0, 0, 0, 0)
        overlay_layout.setSpacing(0)
        overlay_layout.addStretch(1)  

        self.bar_options = QWidget()
        self.bar_options.setMaximumHeight(30)
        self.bar_options.setObjectName("bar_options")
        self.bar_options.setStyleSheet("background-color: rgba(0,0,0,150);")

        bar_option_layout = QHBoxLayout(self.bar_options)
        bar_option_layout.setContentsMargins(10, 0, 10, 0)
        bar_option_layout.setSpacing(5)

        self.btn_cap = QPushButton("📷")
        self.btn_cap.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_cap.setObjectName("btn-bar")

        btn_play = QPushButton("▶")
        btn_play.setCursor(QCursor(Qt.PointingHandCursor))
        btn_play.setObjectName("btn-bar")

        btn_pause = QPushButton("||")
        btn_pause.setCursor(QCursor(Qt.PointingHandCursor))
        btn_pause.setObjectName("btn-bar")

        btn_stop = QPushButton("■")
        btn_stop.setCursor(QCursor(Qt.PointingHandCursor))
        btn_stop.setObjectName("btn-bar")

        btn_play.clicked.connect(self.init_loop)
        btn_pause.clicked.connect(self.pause_loop)
        btn_stop.clicked.connect(self.detroy_loop)

        self.text_fps = QLabel(f"Tasa de FPS: {self.current_fps}")
        self.text_fps.setObjectName("text-fps")

        bar_option_layout.addWidget(self.text_fps)
        bar_option_layout.addStretch(1)
        bar_option_layout.addWidget(self.btn_cap)
        bar_option_layout.addWidget(btn_play)
        bar_option_layout.addWidget(btn_pause)
        bar_option_layout.addWidget(btn_stop)

        overlay_layout.addWidget(self.bar_options)

        # Añadir overlay al stack (queda encima de la imagen)
        self.stack.addWidget(self.overlay)
        self.stack.setStackingMode(QStackedLayout.StackAll)

        # Hover en la imagen
        self.imagen_label.installEventFilter(self)



    def eventFilter(self, obj, event):
        if obj is self.imagen_label:
            if event.type() == QEvent.Enter:
                self.bar_options.show()
            elif event.type() == QEvent.Leave:
                self.bar_options.hide()
        return super().eventFilter(obj, event)
    
    # ---------------------------
    # Procesos de captura
    # ---------------------------
    def init_loop(self):
        try:
            if self.process is None:
                self.process = QProcess(self)
                self.pid = self.process.processId()
                self.process.setProcessChannelMode(QProcess.MergedChannels)
                self.process.readyReadStandardOutput.connect(self.loop_show_result)
                self.process.start("python", ["src/workers/capture_woker.py", str(self.hwnd)])
            else:
                self.process.readyReadStandardOutput.connect(self.loop_show_result)
        except Exception as e:
            print(f"💥 Error: {e}")

    def pause_loop(self):
        if self.process:
            self.process.readyReadStandardOutput.disconnect(self.loop_show_result)
            self.text_fps.setText("Tasa de FPS: 0")
            print(self.process.processId())

    def detroy_loop(self):
        if self.process is not None:
            self.process.terminate()
            if not self.process.waitForFinished(3000):
                self.process.kill()
            self.process = None
            self.imagen_label.clear()
            self.imagen_label.setText("viewing window")



    @Slot(int)
    def get_hwnd_and_print(self, hwnd=None):
        try:
            if hwnd is not None:
                self.hwnd = hwnd
            set_window_always_on_top(self.hwnd)

            buffer = capture_window_by_hwnd(self.hwnd)
            if buffer is None:
                return

            image = pil_image_to_png_bytes(buffer)
            if image is None:
                return

            pixmap = QPixmap()
            success = pixmap.loadFromData(image, "PNG")
            if not success:
                return

            self.cached_size = self.imagen_label.size()
            pixmap_escalada = pixmap.scaled(
                self.cached_size,
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation,
            )
            self.imagen_label.setPixmap(pixmap_escalada)
            self.bar_options.raise_()

        except Exception as e:
            print(f"💥 Error: {e}")



    def loop_show_result(self):
        while self.process and self.process.canReadLine():
            header_line = self.process.readLine().data().decode().strip()
            image_line = self.process.readLine().data().decode().strip()
            try:
                header = json.loads(header_line)
                image_bytes = base64.b64decode(image_line)
                pixmap = QPixmap()

                if pixmap.loadFromData(QByteArray(image_bytes), header.get("format", "JPEG")):
                    if not hasattr(self, "cached_size") or self.cached_size != self.imagen_label.size():
                        self.cached_size = self.imagen_label.size()

                    pixmap_escalada = pixmap.scaled(
                        self.cached_size,
                        Qt.IgnoreAspectRatio,
                        Qt.SmoothTransformation,
                    )
                    self.imagen_label.setPixmap(pixmap_escalada)

                self.frame_count += 1
                now = time.time()
                if now - self.last_fps_time >= 1.0:
                    self.current_fps = self.frame_count
                    self.frame_count = 0
                    self.last_fps_time = now
                    self.text_fps.setText(f"Tasa de FPS: {self.current_fps}")

            except Exception as e:
                print(f"❌ Error al procesar imagen: {e}")

import os, json, base64
import psutil
import signal
import time
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy, QPushButton
from PySide6.QtCore import Qt, Slot, QTimer, QObject, QProcess, QCoreApplication, QDir, QByteArray
from PySide6.QtGui import QPixmap, QCursor

from core.state_global.hwnd import hwndState

from core.capture_exaple import capture_window_by_hwnd, pil_image_to_png_bytes
from core.window_controller import set_window_always_on_top



script_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "workers", "capture_worker.py")
)

class Layaut_center(QWidget):


    def __init__(self, frames_per_milliseconds = 100):
        super().__init__()
        self.process = None
        self.frames_per_milliseconds = frames_per_milliseconds 

        self.frame_count = 0
        self.last_fps_time = time.time()
        self.current_fps = 0

        self.setup_ui()
        hwndState.change_hwnd.connect(self.get_hwnd_and_print)

       

        


    def setup_ui(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layaut = QGridLayout(self)
        self.layaut.setContentsMargins(0, 0, 0, 0)
        
        self.title_main = QLabel(f'Ventana Principal en {hwndState._hwnd}')
        self.title_main.setAlignment(Qt.AlignCenter)
        bar_options = QWidget()
        bar_options.setMaximumHeight(50)
        
        bar_options.setAttribute(Qt.WA_StyledBackground, True)
        bar_options.setObjectName('bar_options')
        bar_option_layaut = QHBoxLayout(bar_options)
        bar_option_layaut.setContentsMargins(10, 0, 10, 0)
        bar_option_layaut.setSpacing(0)
        
        btn_play = QPushButton('▶')
        btn_play.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_play.setObjectName('btn-bar')
        btn_pause = QPushButton('||')
        btn_pause.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_pause.setObjectName('btn-bar')
        btn_stop = QPushButton('■')
        btn_stop.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_stop.setObjectName('btn-bar')

        btn_play.clicked.connect(self.init_loop)
        btn_pause.clicked.connect(self.pause_loop)
        btn_stop.clicked.connect(self.detroy_loop)

        self.text_fps = QLabel(f'Tasa de FPS: {self.current_fps}')
        self.text_fps.setObjectName('text-fps')
        bar_option_layaut.addWidget(self.text_fps)
        bar_option_layaut.addStretch(1)
        bar_option_layaut.addWidget(btn_play)
        bar_option_layaut.addWidget(btn_pause)
        bar_option_layaut.addWidget(btn_stop)

        self.layaut.addWidget(self.title_main)
        self.layaut.addWidget(bar_options)
        

    
    def init_loop(self):
        if self.process is None: 
            self.process = QProcess(self)
            self.pid = self.process.processId()
            self.process.setProcessChannelMode(QProcess.MergedChannels)
            self.process.readyReadStandardOutput.connect(self.loop_show_result)
            self.process.start('python', ['src/workers/capture_woker.py', str(self.hwnd)])
        else:
            pass



    def pause_loop(self):
        pass
            

    def detroy_loop(self):
        pass




    Slot(int)
    def get_hwnd_and_print(self, hwnd=None):
        try:
            if hwnd is not None: self.hwnd = hwnd
            set_window_always_on_top(self.hwnd)
                # 1. Capturar
            buffer = capture_window_by_hwnd(self.hwnd)
            if buffer is None: return
                    
                # 2. Convertir a bytes
            image = pil_image_to_png_bytes(buffer)
            if image is None: return
                    
            # 3. Crear QPixmap y CARGAR DATOS
            pixmap = QPixmap()
            success = pixmap.loadFromData(image, 'PNG')
            if not success: return
            self.cached_size = self.title_main.size()
            # 4. ESCALAR (solo después de cargar)
            pixmap_escalada = pixmap.scaled(
                self.cached_size,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            # 5. Mostrar
            self.title_main.setPixmap(pixmap_escalada)

        except Exception as e:
            print(f"💥 Error: {e}")


    def loop_show_result(self):
        while self.process.canReadLine():
            header_line = self.process.readLine().data().decode().strip()
            image_line = self.process.readLine().data().decode().strip()

            try:
                header = json.loads(header_line)
                image_bytes = base64.b64decode(image_line)
        
                pixmap = QPixmap()
                if pixmap.loadFromData(QByteArray(image_bytes), header.get('format', 'JEPG')):
                    

                    if not hasattr(self, 'cached_size') or self.cached_size != self.title_main.size():
                        self.cached_size = self.title_main.size()

                    pixmap_escalada = pixmap.scaled(
                        self.cached_size,
                        Qt.AspectRatioMode.IgnoreAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )

                self.title_main.setPixmap(pixmap_escalada)

                self.frame_count += 1
                now = time.time()

                if now - self.last_fps_time >= 1.0:
                    self.current_fps = self.frame_count
                    self.frame_count = 0
                    self.last_fps_time = now
                    self.text_fps.setText(f'Tasa de FPS: {self.current_fps}')

            except Exception as e:
                print(f"❌ Error al procesar imagen: {e}")


"""
if not self.cached_size or self.cached_size != self.title_main.size():
    self.cached_size = self.title_main.size()
    self.scaled_pixmap = pixmap.scaled(self.cached_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
self.title_main.setPixmap(self.scaled_pixmap)
"""
"""  LA SIGUIENTE CLASE ES PARA ANALIZAR  """

"""
class CaptureWorker(QObject):
    frame_ready = Signal(bytes)  # señal con los datos de imagen

    def __init__(self, hwnd, interval=30):
        super().__init__()
        self.hwnd = hwnd
        self.interval = interval
        self._running = True

    def start(self):
        # bucle de captura en este hilo
        import time
        while self._running:
            buffer = capture_window_by_hwnd(self.hwnd)
            if buffer:
                image = pil_image_to_png_bytes(buffer)
                if image:
                    self.frame_ready.emit(image)
            time.sleep(self.interval / 1000.0)  # intervalo en ms → seg

    def stop(self):
        self._running = False
        """


"""
class MainWindow(QMainWindow):
    def __init__(self, hwnd):
        super().__init__()
        self.label = QLabel(self)
        self.setCentralWidget(self.label)

        # Crear hilo y worker
        self.thread = QThread()
        self.worker = CaptureWorker(hwnd, interval=30)  # ~33 FPS
        self.worker.moveToThread(self.thread)

        # Conectar señales
        self.thread.started.connect(self.worker.start)
        self.worker.frame_ready.connect(self.update_frame)

        # Iniciar
        self.thread.start()

    @Slot(bytes)
    def update_frame(self, image_bytes):
        pixmap = QPixmap()
        if pixmap.loadFromData(image_bytes, 'PNG'):
            self.label.setPixmap(
                pixmap.scaled(
                    self.label.width(),
                    self.label.height(),
                    Qt.AspectRatioMode.IgnoreAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )

    def closeEvent(self, event):
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()
        super().closeEvent(event)
"""
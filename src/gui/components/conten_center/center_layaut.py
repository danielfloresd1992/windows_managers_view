from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy, QPushButton
from PySide6.QtCore import Qt, Slot, QTimer, QObject
from PySide6.QtGui import QPixmap

from core.state_global.hwnd import hwndState

from core.capture_exaple import capture_window_by_hwnd, pil_image_to_png_bytes
from core.window_controller import set_window_always_on_top


import io


class Layaut_center(QWidget):



    def __init__(self, frames_per_milliseconds = 100):
        super().__init__()
        self.frames_per_milliseconds = frames_per_milliseconds 
        self.setup_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.get_hwnd)
        hwndState.change_hwnd.connect(self.get_hwnd)



    def setup_ui(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layaut = QGridLayout(self)
        self.title_main = QLabel(f'Ventana Principal en {hwndState._hwnd}')
        self.title_main.setAlignment(Qt.AlignCenter)

        bar_buttons = QWidget()
        bar_buttons.setMaximumHeight(40)
        bar_buttons.setAttribute(Qt.WA_StyledBackground, True)
        bar_buttons.setObjectName('bar-btn-center')

        btn_play = QPushButton('PLAY')
        btn_pause = QPushButton('PAUSE')
        btn_stop = QPushButton('STOP')

        btn_play.clicked.connect(self.init_loop)
        btn_pause.clicked.connect(self.pause_loop)
        btn_stop.clicked.connect(self.detroy_loop)

        layaut_bar_buttons = QHBoxLayout(bar_buttons)
        layaut_bar_buttons.addWidget(btn_play)
        layaut_bar_buttons.addWidget(btn_pause)
        layaut_bar_buttons.addWidget(btn_stop)
        
        self.layaut.addWidget(self.title_main)
        self.layaut.addWidget(bar_buttons)
        


    
    def init_loop(self):
        self.timer.start(self.frames_per_milliseconds)


    def pause_loop(self):
        if self.timer.isActive(): self.timer.stop()

    def detroy_loop(self):
        self.timer.destroyed()



    Slot(int)
    def get_hwnd(self, hwnd=None):
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
            
            # 4. ESCALAR (solo después de cargar)
            pixmap_escalada = pixmap.scaled(
                self.title_main.width(), 
                self.title_main.height(),
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            # 5. Mostrar
            self.title_main.setPixmap(pixmap_escalada)

        except Exception as e:
            print(f"💥 Error: {e}")



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
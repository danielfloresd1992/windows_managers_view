from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy
from PySide6.QtCore import Qt, Slot, QTimer
from PySide6.QtGui import QPixmap

from core.state_global.hwnd import hwndState

from core.capture_exaple import capture_window_by_hwnd, pil_image_to_png_bytes
from core.window_controller import set_window_always_on_top


import io


class Layaut_center(QWidget):


    def __init__(self):
        super().__init__()
        self.setup_ui()
        hwndState.change_hwnd.connect(self.get_hwnd)


       


    def setup_ui(self):

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layaut = QGridLayout(self)

        self.title_main = QLabel(f'Ventana Principal en {hwndState._hwnd}')
        self.title_main.setAlignment(Qt.AlignCenter)
        self.layaut.addWidget(self.title_main)
        

        



    Slot(int)
    def get_hwnd(self, hwnd):
        try:
            while True:
                set_window_always_on_top(hwnd)
                
                # 1. Capturar
                buffer = capture_window_by_hwnd(hwnd)
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


    



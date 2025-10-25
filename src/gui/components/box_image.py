from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout;
from PySide6.QtGui import QPixmap;
from PySide6.QtCore import Qt, QTimer

from core.capture_exaple import capture_window_by_hwnd, pil_image_to_png_bytes
from core.window_controller import set_window_always_on_top
from core.state_global.hwnd import hwndState



class Box_cap(QWidget):


    def __init__(self, id_window):
        super().__init__()
        self.id_windows = id_window
       
        self.set_ui()


    
    def set_ui(self):
        self.setObjectName('Image-render')

        layaut_content = QHBoxLayout(self)
        self.image_label = QLabel()
        layaut_content.addWidget(self.image_label)
        self.update_frame()
    


    def cap_img(self):
        if(self.activateWindow): set_window_always_on_top(self.id_windows)
        image_buffer = capture_window_by_hwnd(self.id_windows)
        return  pil_image_to_png_bytes( image_buffer)
    




    def update_frame(self):
        image = QPixmap()
        image.loadFromData(self.cap_img(), 'png')
        image = image.scaled(180, 140, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(image)
        



    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            hwndState.set_hwnd(self.id_windows)
        elif event.button() == Qt.RightButton:
            print('Click derecho en el widget')
        # Importante: llamar al padre si quieres que otros eventos sigan funcionando
        super().mousePressEvent(event)
# gui/main_window.py
from PySide6.QtWidgets import QMainWindow
from core.window_controller import WindowController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window_controller = WindowController()
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Window Manager Pro")
        self.setGeometry(100, 100, 1000, 700)
        # ... resto de tu UI ...
    
  
from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow, QStatusBar, QDialog, QLabel, QVBoxLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt


class BtnIco(QPushButton):
    
    def __init__(self, ico_path='', title='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setIcon(QIcon(ico_path))
        
        self.setFixedHeight(30)
        self.setFixedWidth(30)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                
            }
            QPushButton:hover {
                background-color: #dddddd;
            }
        """)
        self.setToolTip(title)
        self.setCursor(Qt.PointingHandCursor)
        


        
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Calcular tamaño del icono = 95% del botón
        w = int(self.width() * 0.90)
        h = int(self.height() * 0.90)
        self.setIconSize(QSize(w, h))
        

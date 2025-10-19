import sys
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from PySide6.QtGui import QMouseEvent
from dotenv import load_dotenv


load_dotenv()


#components 



class CustomTitleBar(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self._start_pos = None
        self._is_dragging = False
        self.setup_ui()




    def setup_ui(self):

        self.setObjectName('title_bar')
        self.setFixedHeight(40)



        self.setStyleSheet("""
            #title_bar {
                width: '100%';
                background-color: #ffffff;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QLabel#title_label {
                color: white;
                font-weight: bold;
                font-size: 12px;
                padding-left: 12px;
            }
            QPushButton#MinimizeButton, 
            QPushButton#MaximizeButton, 
            QPushButton#CloseButton {
                border: none;
                background-color: transparent;
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 0px 8px;
                min-width: 20px;
                min-height: 20px;
            }
            QPushButton#MinimizeButton:hover {
                background-color: #34495e;
            }
            QPushButton#MaximizeButton:hover {
                background-color: #34495e;
            }
            QPushButton#CloseButton:hover {
                background-color: #e74c3c;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setObjectName('layout_title_bar')
        layout.setContentsMargins(0, 0, 5, 0)
        layout.setSpacing(0)

        self.title = QLabel(f'{os.getenv("name_project", "App")} {os.getenv("version", "1.0")}')
        self.title.setObjectName('title_label')
        self.title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)



        btn_minimize = QPushButton('−')
        btn_minimize.setObjectName('MinimizeButton')
        btn_minimize.clicked.connect(self.parent().showMinimized)


        btn_maximize = QPushButton('□')
        btn_maximize.setObjectName('MaximizeButton')
        btn_maximize.clicked.connect(self.toggle_maximize_restore)
        
        btn_close = QPushButton('✕')
        btn_close.setObjectName('CloseButton')
        btn_close.clicked.connect(self.parent().close)


        layout.addWidget(self.title)
        layout.addStretch(1)
        layout.addWidget(btn_minimize)
        layout.addWidget(btn_maximize)
        layout.addWidget(btn_close)





    def toggle_maximize_restore(self):
        """Alterna entre maximizar y restaurar la ventana"""
        parent = self.parent()
        if parent.isMaximized():
            parent.showNormal()
        else:
            parent.showMaximized()
    


    def mousePressEvent(self, event: QMouseEvent):
        """Maneja el evento de presión del mouse"""
        if event.button() == Qt.LeftButton:
            self._start_pos = event.globalPosition().toPoint()
            self._is_dragging = True
            event.accept()
    


    def mouseMoveEvent(self, event: QMouseEvent):
        """Maneja el evento de movimiento del mouse"""
        if self._is_dragging and self._start_pos:
            delta = event.globalPosition().toPoint() - self._start_pos
            self.parent().move(self.parent().pos() + delta)
            self._start_pos = event.globalPosition().toPoint()
            event.accept()
    



    def mouseReleaseEvent(self, event: QMouseEvent):
        """Maneja el evento de liberación del mouse"""
        if event.button() == Qt.LeftButton:
            self._is_dragging = False
            self._start_pos = None
            event.accept()
    


    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """Maximiza/restaura con doble click"""
        if event.button() == Qt.LeftButton:
            self.toggle_maximize_restore()
            event.accept()


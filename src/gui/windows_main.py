import os
from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt
from core.app_singleton import AppSingleton

from gui.components.title_bar.window_bar import CustomTitleBar





class MainWindow(QMainWindow):


    def __init__(self):
        super().__init__()
        self.setObjectName('MainWindowStyle')
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setup_ui()
        self.center_windows()
    

    
    def setup_ui(self):

        self.resize(1024,768)

        
        # CONTENEDOR PRINCIPAL
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)



        # DECLARACIÓN DE COMPONENTES PRINCIPALES
        self.title_bar = CustomTitleBar(self)
    

        self.setCentralWidget(central_widget)
        content_center = QWidget()
        self.content_layaut = QHBoxLayout(content_center)

        

       
        content_center.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


        #INTRIDUCIÓN DE COMPÓNENTES PRNCIPALES
        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(content_center)


   
    def add_center(self, component):
        self.content_layaut.addWidget(component)

        


    def center_windows(self):
        screen =QApplication.primaryScreen() 
        screen_geometry = screen.availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
    


    def test_singleton(self):
        """Probar que el singleton funciona"""
        app = AppSingleton.get_app()
        print(f"✅ Singleton funcionando - App: {app}")


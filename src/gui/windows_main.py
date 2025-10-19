from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt
from core.app_singleton import AppSingleton
from gui.components.window_bar import CustomTitleBar



class MainWindow(QMainWindow):


    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setup_ui()
        self.center_windows()
        self.setStyleSheet("background-color: #000000;")

    
    def setup_ui(self):

        self.resize(800,600)
        self.title_bar = CustomTitleBar(self)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)


        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)


        # Barra de título personalizada
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)
        
        # Contenido principal
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: #ecf0f1;")
        self.content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.content_widget)
        
        # Configurar contenido interno
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.addWidget(QLabel("Contenido principal de la aplicación - Layout al 100%"))
        
        # Estilo para la ventana
        self.setStyleSheet("""
            MainWindow {
                background-color: #ecf0f1;
                border-radius: 8px;
            }
        """)



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
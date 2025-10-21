from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt
from core.app_singleton import AppSingleton
from gui.components.title_bar.window_bar import CustomTitleBar



class MainWindow(QMainWindow):


    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setup_ui()
        self.center_windows()
    

    
    def setup_ui(self):

        self.resize(800,600)

        
        # CONTENEDOR PRINCIPAL
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)



        # BARRA DE TÍTULO PERSONALIZADA
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)


        self.setCentralWidget(central_widget)

        content_center = QWidget()
        content_layaut = QVBoxLayout(content_center)

        title_main = QLabel("Ventana Principal")
        title_main.setAlignment(Qt.AlignCenter)

        content_layaut.addWidget(title_main)


        main_layout.addWidget(content_center)
        content_center.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
        
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
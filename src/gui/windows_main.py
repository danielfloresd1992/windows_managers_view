from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from core.app_singleton import AppSingleton



class MainWindow(QMainWindow):


    def __init__(self):
        super().__init__()
        # ✅ No crea QApplication, usa el singleton
        self.setup_ui()

    
    def setup_ui(self):

        self.setWindowTitle("Window Manager Pro")
        self.setGeometry(100, 100, 1000, 700)


        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout(central_widget)
        
        # Componentes
        title = QLabel("🖥️ Gestor de Ventanas")
        title.setStyleSheet("font-size: 18pt; font-weight: bold; margin: 10px;")
        
        status = QLabel("✅ Aplicación inicializada correctamente")
        
        # Botón de prueba que usa el singleton
        test_btn = QPushButton("Probar Singleton")
        test_btn.clicked.connect(self.test_singleton)
        
        layout.addWidget(title)
        layout.addWidget(status)
        layout.addWidget(test_btn)
    


    def test_singleton(self):
        """Probar que el singleton funciona"""
        app = AppSingleton.get_app()
        print(f"✅ Singleton funcionando - App: {app}")
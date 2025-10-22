from PySide6.QtWidgets import QWidget, QVBoxLayout,QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap



class Sidebar_Dock(QWidget):
     


    def __init__(self, parent=None, title='Panel Lateral', src_ico='src/resources/ico.png'):
        super().__init__(parent)

        self.ico=src_ico
        self.title=title
        self.setup_ui()
            
            
    
    def setup_ui(self):
        self.setObjectName('SidebarDock')
        self.setFixedWidth(250)  # Sidebar de 250px de ancho
        self.setAttribute(Qt.WA_StyledBackground, True)
        layout_dock = QVBoxLayout(self)
    


        header = QWidget()
        header_layaut = QHBoxLayout(header)
        header.setObjectName('Head')
        header.setAttribute(Qt.WA_StyledBackground, True)
        header.setFixedHeight(50)


        img_image = QLabel()

        ico = QPixmap(self.ico)
        ico = ico.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        img_image.setFixedSize(32,32)

        if not ico.isNull():
            img_image.setPixmap(ico)
        else:
            print('No se pudo cargar la imagen:', self.ico)


        text_title = QLabel(self.title)
        text_title.setObjectName('title_semibold')

        header_layaut.addWidget(img_image)
        header_layaut.addWidget(text_title)


        layout_dock.addWidget(header, alignment=Qt.AlignTop)
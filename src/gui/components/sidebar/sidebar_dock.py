from PySide6.QtWidgets import QWidget, QVBoxLayout,QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Property, Signal
from PySide6.QtGui import QPixmap





class Sidebar_Dock(QWidget):
     
     
    countChanged = Signal(int)


    def __init__(self, parent=None, title='Panel Lateral', src_ico='src/resources/ico.png', window_globals=None):
        super().__init__(parent)

        self.windows = window_globals

        self.ico=src_ico
        self.title=title
        self.setup_ui()
        self.countChanged.connect(self._on_count_changed)
            
            
    
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



        content_center = QWidget()
        content_layaut = QVBoxLayout(content_center)

        self.text_content = QLabel(f'Contador: {self.count}')
        self.text_content.setAlignment(Qt.AlignCenter)

        content_btn = QWidget()
        content_btn_layaut = QHBoxLayout(content_btn)


        sustraccion_btn = QPushButton('Sustraer')
        sustraccion_btn.setObjectName('btn_primary')
        sustraccion_btn.clicked.connect(self.sub_count)
        content_btn_layaut.addWidget(sustraccion_btn)


        addition_btn = QPushButton('Agregar')
        addition_btn.setObjectName('btn_primary')
        addition_btn.clicked.connect(self.add_count)
        content_btn_layaut.addWidget(addition_btn)

      


    

        content_layaut.addWidget(self.text_content)
        content_layaut.addWidget(content_btn)

        layout_dock.addWidget(header, alignment=Qt.AlignTop)
        layout_dock.addWidget(content_center)



    @Property(int, notify=countChanged)
    def count(self):
        return self._count
    
    @count.setter
    def count(self, value):
        if self._count != value:  # Solo actualizar si cambió
            self._count = value
            self.countChanged.emit(value)  # ¡Esto hace que sea reactivo!



    def add_count(self):
        self.count +=1
       

    def sub_count(self):
        self.count -=1



    def _on_count_changed(self, value):
        """Se llama automáticamente cuando count cambia - similar a useEffect"""
        self.text_content.setText(f'Contador: {value}')
        print(f'El contador es: {value}')
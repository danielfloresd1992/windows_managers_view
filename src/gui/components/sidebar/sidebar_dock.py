from PySide6.QtWidgets import QWidget, QVBoxLayout,QHBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap

from core.window_global import windows_monitor

from gui.components.box_image import Box_cap




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
        layout_dock.setContentsMargins(0,0,0,0)
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

        self.scroll_area = QScrollArea()
        self.scroll_area.setAttribute(Qt.WA_StyledBackground, True)
        self.scroll_area.setObjectName('ScrollAreaSidebar')
        # Opcional pero recomendado: Hace que el scroll area ocupe todo el espacio disponible
        self.scroll_area.setWidgetResizable(True)

        content_center = QWidget()
        content_center.setAttribute(Qt.WA_StyledBackground, True)
        content_center.setObjectName('ContentSidebar')
        self.content_layaut = QVBoxLayout(content_center)
        self.content_layaut.setContentsMargins(0,0,0,0)
        self.content_layaut.setAlignment(Qt.AlignTop| Qt.AlignHCenter)
        self.scroll_area.setWidget(content_center)

        layout_dock.addWidget(header, alignment=Qt.AlignTop)
        layout_dock.addWidget(self.scroll_area)





    
    def print_list(self, list_windows):
        
        if(list_windows):
            for window in list_windows:
                self.content_layaut.addWidget(Box_cap(window))



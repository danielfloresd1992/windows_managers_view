from PySide6.QtWidgets import QApplication, QMainWindow,  QHBoxLayout, QWidget, QVBoxLayout, QLabel,QStatusBar, QPushButton, QSizePolicy, QGridLayout, QDialog, QTabWidget
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QCursor, QIcon


from gui.components.title_bar.window_bar import CustomTitleBar
from gui.components.custon_btn.btn_footer import BtnIco
from gui.components.render_box.render_box import  Render_box




class MainWindow(QMainWindow):

    MARGIN = 16  # margen sensible para detectar bordes



    def __init__(self):
        super().__init__()
        self.setObjectName('MainWindowStyle')
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setWindowFlag(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setContentsMargins(0,0,0,0)
        # variables internas para resize
        self._resizing = False
        self._resize_direction = None
        self._start_pos = None
        self._start_geom = None
        
        self.list_box = []
        
            

        self.setup_ui()
        self.center_windows()

        # 🔑 activar mouse tracking en toda la jerarquía
        self.setMouseTracking(True)
     #   self.centralWidget().setMouseTracking(True)
        for child in self.findChildren(QWidget):
            child.setMouseTracking(True)

        
        self._create_list_box()
        "inserción______⤵️_______"
        self.append_renderbox(4, add=True)


    def setup_ui(self):
       
        self.resize(1024, 768)

        main_content = QWidget()
        main_content.setContentsMargins(0,0,0,0)
        self.layout_main = QVBoxLayout(main_content)
        self.layout_main.setContentsMargins(0,0,0,0)
        "inserción______⤵️_______"
        self.setCentralWidget(main_content)


        title_bar = CustomTitleBar(self)
        self.layout_main.addWidget(title_bar)
        "inserción______⤵️_______"
   
   
        self.window_child = QMainWindow()
        self.window_child.setAttribute(Qt.WA_StyledBackground, True)
        self.window_child.setWindowFlag(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        "inserción______⤵️_______"
        self.layout_main.addWidget(self.window_child)
        
        
        """______PESTAÑAS______"""
        self.tabs = QTabWidget()
        self.tabs.setContentsMargins(0, 0, 0, 0)
        self.tabs.setAttribute(Qt.WA_StyledBackground, True)
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                /* 1. Fondo */
                background: #292929; /* Color gris claro */
                
                /* 2. Borde */
               
                border-bottom: none; /* Quitamos el borde inferior para que se pegue al contenido */
                border-top-left-radius: 4px; /* Esquinas superiores redondeadas */
                border-top-right-radius: 4px;
                
                /* 3. Espacio interno (Padding) */
                padding: 8px 12px; /* Aumenta el alto y ancho de la pestaña */
                
                /* 4. Fuente */
                color: #ffffff; /* Texto gris oscuro */
                font-size: 10pt;
            }
            QTabWidget {
                background-color: #000000;
                border: 0;
                padding: 0;
            }
        """)        
        "inserción______⤵️_______"
        self.window_child.setCentralWidget(self.tabs)
        
        
        
        """__________VIEW_________"""
        content_box = QWidget()
        content_box.setObjectName('TabContent')
      
        self.content_box_layout = QGridLayout(content_box)
        self.content_box_layout.setSpacing(0)
        self.content_box_layout.setContentsMargins(0,0,0,0)
       
        "inserción______⤵️_______"
        self.tabs.addTab(content_box, 'Smart Streaming')
        
        
        
        """PESTAÑA DE DISPOSITIVOS"""
        content_box = QWidget()
        "inserción______⤵️_______"
        self.tabs.addTab(content_box, 'Dispositivos')
        
        
        
        """____BARRA DE OPCIONES___"""
        status = QStatusBar()
        status.setAttribute(Qt.WA_StyledBackground, True)
        status.setFixedHeight(35)
        status.setObjectName('FooterBar')
        
        status.showMessage('Servidor Activo')
        
        status.setStyleSheet("QStatusBar { background-color: #424242; color: white; }")
        "inserción______⤵️_______"
        self.window_child.setStatusBar(status)
        

        btn = BtnIco(ico_path='resource/layout.png', title='Divisiones de ventanas: (3x3, 2x2, etc.)')
        btn.clicked.connect(self.open_dialog)
        "inserción______⤵️_______"
        status.addPermanentWidget(btn)
        
        
    
    
    def append_renderbox(self, amount: int = 2, add=False):
        
        amount_box = 0
        row = 0
        print(amount)
        print(self.list_box)
        if add == False: self._clear_layout_only()
                
        while row < amount:
            col = 0
            while col < amount:
                box_seleted = self.list_box[amount_box]
                self.content_box_layout.addWidget(box_seleted, row, col)
                box_seleted.show()
                amount_box = amount_box + 1
                col = col + 1
            row = row + 1
            
            
            
    def _create_list_box(self):
        while len(self.list_box) < 16:
            box = Render_box(index=len(self.list_box))
            self.list_box.append(box)
        
        
        
    def _clear_layout_only(self):
        while self.content_box_layout.count():
            item = self.content_box_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                    # Lo ocultamos para que no se quede "flotando" en la esquina de la ventana
                    widget.hide()
                        # Opcional: desvincularlo totalmente del layout padre
                    widget.setParent(None)
        
        
        
        
    def open_dialog(self):
        dlg = QDialog(parent=self)
        dlg.setFixedHeight(180)
        dlg.setFixedWidth(260)
        dlg.setStyleSheet("QDialog { background-color: #424242; color: white; }")
        dlg.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)  # sin barra de título
        dlg.setWindowFlags(dlg.windowFlags() | Qt.WindowStaysOnTopHint) 
        
        def close_dlg():
            dlg.close()
  
        contain_layout = QVBoxLayout()
        
        title = QLabel('Divisiones de las ventanas')
        title.setAlignment(Qt.AlignCenter)
        contain_layout.addWidget(title)
      
        btn_one = BtnIco(ico_path='resource/1-.png', title='Una ventana principal', h=40, w=40)
        btn_one.clicked.connect(lambda checked=False: self.append_renderbox(amount=1))
 
        btn_quad = BtnIco(ico_path='resource/2x2-.png', title='2 X 2', h=40, w=40)
        btn_quad.clicked.connect(lambda checked=False: self.append_renderbox(amount=2))
        
        btn_nine = BtnIco(ico_path='resource/3x3-.png', title='9 X 9', h=40, w=40)
        btn_nine.clicked.connect(lambda checked=False: self.append_renderbox(amount=3))
        
        btn_max = BtnIco(ico_path='resource/4x4-.png', title='4 X 4', h=40, w=40)
        btn_max.clicked.connect(lambda checked=False: self.append_renderbox(amount=4))
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn_one)
        btn_layout.addWidget(btn_quad)
        btn_layout.addWidget(btn_nine)
        btn_layout.addWidget(btn_max)
        btn_layout.addStretch()
        
        contain_layout.addLayout(btn_layout, stretch=1)
        contain_layout.setAlignment(Qt.AlignCenter)  # centra todo el contenido

        btn_cancel = QPushButton('Cancelar')
        btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                text-decoration: underline;
                color: #ffffff
            }             
        """)
        btn_cancel.clicked.connect(close_dlg)
        contain_layout.addWidget(btn_cancel, alignment=Qt.AlignCenter)
        dlg.setLayout(contain_layout)
        dlg.exec()
            
    

    def center_windows(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)




    # --------------------
    # LÓGICA DE REDIMENSIONAMIENTO
    # ---------------------------
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._start_pos = event.globalPosition().toPoint()
            self._start_geom = self.geometry()
            self._resize_direction = self._get_resize_direction(event.pos())
            if self._resize_direction:
                self._resizing = True




    def mouseMoveEvent(self, event):
        pos = event.pos()
        if not self._resizing:
            self._update_cursor(pos)
        else:
            self._resize_window(event.globalPosition().toPoint())




    def mouseReleaseEvent(self, event):
        self._resizing = False
        self._resize_direction = None




    def _get_resize_direction(self, pos):
        rect = self.rect()
        x, y = pos.x(), pos.y()
        margin = self.MARGIN
        if x < margin and y < margin:
            return 'top_left'
        elif x > rect.width() - margin and y < margin:
            return 'top_right'
        elif x < margin and y > rect.height() - margin:
            return 'bottom_left'
        elif x > rect.width() - margin and y > rect.height() - margin:
            return 'bottom_right'
        elif x < margin:
            return 'left'
        elif x > rect.width() - margin:
            return 'right'
        elif y < margin:
            return 'top'
        elif y > rect.height() - margin:
            return 'bottom'
        return None




    def _update_cursor(self, pos):
        direction = self._get_resize_direction(pos)
        cursors = {
            'top_left': Qt.SizeFDiagCursor,
            'bottom_right': Qt.SizeFDiagCursor,
            'top_right': Qt.SizeBDiagCursor,
            'bottom_left': Qt.SizeBDiagCursor,
            'left': Qt.SizeHorCursor,
            'right': Qt.SizeHorCursor,
            'top': Qt.SizeVerCursor,
            'bottom': Qt.SizeVerCursor,
        }
        self.setCursor(cursors.get(direction, Qt.ArrowCursor))



    def _resize_window(self, global_pos):
        delta = global_pos - self._start_pos
        geom = QRect(self._start_geom)
        dir = self._resize_direction

        if 'left' in dir:
            geom.setLeft(geom.left() + delta.x())
        if 'right' in dir:
            geom.setRight(geom.right() + delta.x())
        if 'top' in dir:
            geom.setTop(geom.top() + delta.y())
        if 'bottom' in dir:
            geom.setBottom(geom.bottom() + delta.y())

        # respetar tamaño mínimo
        if geom.width() >= self.minimumWidth() and geom.height() >= self.minimumHeight():
            self.setGeometry(geom)
            
            
            
            

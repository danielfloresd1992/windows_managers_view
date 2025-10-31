from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QGridLayout
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QCursor


from gui.components.title_bar.window_bar import CustomTitleBar




class MainWindow(QMainWindow):

    MARGIN = 8  # margen sensible para detectar bordes



    def __init__(self):
        super().__init__()
        self.setObjectName('MainWindowStyle')
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setWindowFlag(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # variables internas para resize
        self._resizing = False
        self._resize_direction = None
        self._start_pos = None
        self._start_geom = None

        self.setup_ui()
        self.center_windows()

        # 🔑 activar mouse tracking en toda la jerarquía
        self.setMouseTracking(True)
        self.centralWidget().setMouseTracking(True)
        for child in self.findChildren(QWidget):
            child.setMouseTracking(True)



    def setup_ui(self):
        self.resize(1024, 768)

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

        # INTRIDUCIÓN DE COMPÓNENTES PRNCIPALES
        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(content_center)



    def add_center(self, component):
        self.content_layaut.addWidget(component)



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
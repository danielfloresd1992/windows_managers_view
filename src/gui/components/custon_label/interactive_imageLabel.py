from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QPoint, Signal
from PySide6.QtGui import QPixmap, QMouseEvent, QPainter, QBrush, QPen


class interactive_imageLabel(QLabel):
    
    point_change = Signal(list)
    
    
    def __init__(self, parent=None, roi=[]):
        super().__init__(parent)
        self.setMouseTracking(True)

        # Flag para mostrar/ocultar puntos
        self.show_points = True

        # Puntos iniciales (0–1000)
        self.points = [
            QPoint(100, 100),
            QPoint(900, 100),
            QPoint(900, 900),
            QPoint(100, 900),
        ]

        self.active_point_index = -1
        self.point_radius = 10
        self.current_pixmap = QPixmap()
        self.hide_points()

    # ------------------------------------------------------------
    # CONTROL DE VISIBILIDAD DE PUNTOS
    # ------------------------------------------------------------
    def hide_points(self):
        self.show_points = False
        self.update()

    def show_points_fn(self):
        self.show_points = True
        self.update()

    def toggle_points(self):
        self.show_points = not self.show_points
        self.update()

    # ------------------------------------------------------------
    # PIXMAP
    # ------------------------------------------------------------
    def setPixmap(self, pixmap):
        self.current_pixmap = pixmap
        super().setPixmap(pixmap)
        self.update()

    # ------------------------------------------------------------
    # CONVERSIÓN DE COORDENADAS
    # ------------------------------------------------------------
    def get_scaled_point(self, point_percentage: QPoint) -> QPoint:
        width = self.width()
        height = self.height()
        x = int(point_percentage.x() * width / 1000)
        y = int(point_percentage.y() * height / 1000)
        return QPoint(x, y)

    def get_percentage_point(self, point_pixel: QPoint) -> QPoint:
        width = self.width()
        height = self.height()
        if width == 0 or height == 0:
            return QPoint(0, 0)

        x = int(point_pixel.x() * 1000 / width)
        y = int(point_pixel.y() * 1000 / height)

        x = max(0, min(x, 1000))
        y = max(0, min(y, 1000))
        return QPoint(x, y)

    # ------------------------------------------------------------
    # DIBUJO
    # ------------------------------------------------------------
    def paintEvent(self, event):
        super().paintEvent(event)

        # Si los puntos están ocultos, no dibujar nada
        if not self.show_points:
            return

        if self.width() < 1 or self.height() < 1 or self.current_pixmap.isNull():
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        last_p_pixel = None
        for i, p_percentage in enumerate(self.points):
            p_pixel = self.get_scaled_point(p_percentage)

            # Líneas
            if last_p_pixel is not None:
                painter.setPen(QPen(Qt.white, 1, Qt.DashLine))
                painter.drawLine(last_p_pixel, p_pixel)
            last_p_pixel = p_pixel

            # Puntos
            color = Qt.red if i == self.active_point_index else Qt.yellow
            painter.setPen(QPen(Qt.black, 2))
            painter.setBrush(QBrush(color))
            painter.drawEllipse(p_pixel, self.point_radius, self.point_radius)

        # Cerrar polígono
        first_p_pixel = self.get_scaled_point(self.points[0])
        painter.setPen(QPen(Qt.white, 1, Qt.DashLine))
        painter.drawLine(last_p_pixel, first_p_pixel)

        painter.end()


    # ------------------------------------------------------------
    # EVENTOS DEL MOUSE
    # ------------------------------------------------------------
    def mousePressEvent(self, event: QMouseEvent):
        if not self.show_points:
            return
        if event.button() == Qt.LeftButton:
            for i, p_percentage in enumerate(self.points):
                p_pixel = self.get_scaled_point(p_percentage)

                dx = event.pos().x() - p_pixel.x()
                dy = event.pos().y() - p_pixel.y()
                distance = (dx**2 + dy**2)**0.5

                if distance < self.point_radius:
                    self.active_point_index = i
                    self.update()
                    return
        super().mousePressEvent(event)



    def mouseMoveEvent(self, event: QMouseEvent):
        if not self.show_points:
            return
        if self.active_point_index != -1 and event.buttons() & Qt.LeftButton:
            new_pos_pixel = event.pos()
            new_pos_pixel.setX(max(0, min(new_pos_pixel.x(), self.width())))
            new_pos_pixel.setY(max(0, min(new_pos_pixel.y(), self.height())))
            new_pos_percentage = self.get_percentage_point(new_pos_pixel)
            self.points[self.active_point_index] = new_pos_percentage
            self.update()
        super().mouseMoveEvent(event)




    def mouseReleaseEvent(self, event: QMouseEvent):
        if not self.show_points:
            return
        if event.button() == Qt.LeftButton and self.active_point_index != -1:
            self.active_point_index = -1
            self.update()
            self.point_change.emit(self.qpoints_to_list(self.points))
            
        super().mouseReleaseEvent(event)



    # ------------------------------------------------------------
    # OBTENER COORDENADAS EN PIXELES ORIGINALES
    # ------------------------------------------------------------
    def get_coordinates(self, image_width: int, image_height: int) -> list[list[int]]:
        if image_width <= 0 or image_height <= 0:
            return []

        coordinates = []
        for p_percentage in self.points:
            x = int(p_percentage.x() * image_width / 1000)
            y = int(p_percentage.y() * image_height / 1000)
            coordinates.append([x, y])

        return coordinates


    def qpoints_to_list(qpoints: list[QPoint]) -> list[list[int]]:
        """Convierte una lista de QPoints a una lista de listas [[x, y], ...]"""
        return [[p.x(), p.y()] for p in qpoints]


    def list_to_qpoints(data: list[list[int]]) -> list[QPoint]:
        """Convierte una lista de listas [[x, y], ...] a una lista de QPoints"""
        # Usamos una lista de comprensión para instanciar los QPoints
        return [QPoint(coord[0], coord[1]) for coord in data]
from PySide6.QtWidgets import  QLabel
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPixmap, QMouseEvent, QPainter, QBrush, QPen, QMouseEvent



class interactive_imageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True) # Para detectar movimiento sin tener que presionar
        
        # 4 puntos iniciales almacenados como porcentaje (0 a 1000)
        # Esto asegura que los puntos se escalen cuando se redimensiona el QLabel.
        self.points = [
            QPoint(100, 100),  # Top-left (10% x, 10% y)
            QPoint(900, 100),  # Top-right
            QPoint(900, 900),  # Bottom-right
            QPoint(100, 900),  # Bottom-left
        ]
        self.active_point_index = -1 # Índice del punto que está siendo arrastrado
        self.point_radius = 10       # Radio visual del círculo del punto (en píxeles)
        self.current_pixmap = QPixmap()


    def setPixmap(self, pixmap):
        """
        Sobrescribe setPixmap.
        Guarda el pixmap actual (escalado en Render_box) y llama al método base.
        """
        self.current_pixmap = pixmap
        super().setPixmap(pixmap)
        self.update() # Forzar el repintado de los puntos


    def get_scaled_point(self, point_percentage: QPoint) -> QPoint:
        """Convierte las coordenadas de porcentaje (0-1000) a coordenadas de píxeles reales."""
        width = self.width()
        height = self.height()
        x = int(point_percentage.x() * width / 1000)
        y = int(point_percentage.y() * height / 1000)
        return QPoint(x, y)


    def get_percentage_point(self, point_pixel: QPoint) -> QPoint:
        """Convierte las coordenadas de píxeles reales a coordenadas de porcentaje (0-1000)."""
        width = self.width()
        height = self.height()
        # Evitar división por cero
        if width == 0 or height == 0:
            return QPoint(0, 0)
            
        x = int(point_pixel.x() * 1000 / width)
        y = int(point_pixel.y() * 1000 / height)
        
        # Asegurar que los valores se mantengan entre 0 y 1000
        x = max(0, min(x, 1000))
        y = max(0, min(y, 1000))
        return QPoint(x, y)


    def paintEvent(self, event):
        """Dibuja el QPixmap (llamado por el padre) y luego dibuja los puntos encima."""
        super().paintEvent(event) # Dibuja la imagen base (QPixmap)

        # Solo dibujar si el QLabel tiene un tamaño válido
        if self.width() < 1 or self.height() < 1 or self.current_pixmap.isNull():
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dibujar los puntos y las líneas
        last_p_pixel = None
        for i, p_percentage in enumerate(self.points):
            p_pixel = self.get_scaled_point(p_percentage)
            
            # --- Líneas (Opcional: dibuja el polígono de selección) ---
            if last_p_pixel is not None:
                painter.setPen(QPen(Qt.white, 1, Qt.DashLine))
                painter.drawLine(last_p_pixel, p_pixel)
            last_p_pixel = p_pixel
            
            # --- Puntos ---
            if i == self.active_point_index:
                color = Qt.red # El punto activo es rojo
            else:
                color = Qt.yellow # Puntos inactivos son amarillos
            
            painter.setPen(QPen(Qt.black, 2)) # Borde negro
            painter.setBrush(QBrush(color, Qt.SolidPattern))
            painter.drawEllipse(p_pixel, self.point_radius, self.point_radius)
        
        # Conectar el último punto al primero para cerrar el polígono
        first_p_pixel = self.get_scaled_point(self.points[0])
        painter.setPen(QPen(Qt.white, 1, Qt.DashLine))
        painter.drawLine(last_p_pixel, first_p_pixel)
        
        painter.end()


    def mousePressEvent(self, event: QMouseEvent):
        """Maneja el clic del ratón para seleccionar un punto."""
        if event.button() == Qt.LeftButton:
            
            for i, p_percentage in enumerate(self.points):
                p_pixel = self.get_scaled_point(p_percentage)
                
                # Cálculo de la distancia euclídea entre el clic y el centro del punto
                dx = event.pos().x() - p_pixel.x()
                dy = event.pos().y() - p_pixel.y()
                distance = (dx**2 + dy**2)**0.5
                
                # Si el clic está dentro del radio del punto, se activa
                if distance < self.point_radius:
                    self.active_point_index = i
                    self.update() # Para repintar el punto activo en color rojo
                    return
        
        super().mousePressEvent(event)


    def mouseMoveEvent(self, event: QMouseEvent):
        """Maneja el movimiento del ratón para arrastrar el punto activo."""
        if self.active_point_index != -1 and event.buttons() & Qt.LeftButton:
            
            # 1. Obtener la nueva posición del ratón (en píxeles)
            new_pos_pixel = event.pos()
            
            # 2. Asegurarse de que el punto no se salga de los límites (0 a width/height)
            new_pos_pixel.setX(max(0, min(new_pos_pixel.x(), self.width())))
            new_pos_pixel.setY(max(0, min(new_pos_pixel.y(), self.height())))

            # 3. Convertir la nueva posición a porcentaje (0-1000)
            new_pos_percentage = self.get_percentage_point(new_pos_pixel)
            
            # 4. Actualizar el punto
            self.points[self.active_point_index] = new_pos_percentage
            self.update() # Forzar el repintado
            
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Maneja la liberación del ratón para deseleccionar el punto."""
        if event.button() == Qt.LeftButton and self.active_point_index != -1:
            self.active_point_index = -1
            self.update()
        
        super().mouseReleaseEvent(event)
        
        
    def get_coordinates(self, image_width: int, image_height: int) -> list[list[int]]:
        """
        Calcula y devuelve las posiciones de los 4 puntos en píxeles 
        referenciados al tamaño de la imagen original no escalada.

        Args:
            image_width (int): La anchura original del QPixmap no escalado.
            image_height (int): La altura original del QPixmap no escalado.

        Retorna:
            list[list[int]]: Una lista de 4 listas, donde cada lista interior 
                             es la coordenada [x, y] del punto en la imagen original.
                             Ejemplo: [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
        """
        if image_width <= 0 or image_height <= 0:
            return []

        coordinates = []
        # Los puntos se guardan como porcentajes de 0 a 1000
        for p_percentage in self.points:
            # La coordenada X se calcula: (PorcentajeX / 1000) * AnchoOriginal
            x = int(p_percentage.x() * image_width / 1000)
            
            # La coordenada Y se calcula: (PorcentajeY / 1000) * AltoOriginal
            y = int(p_percentage.y() * image_height / 1000)
            
            coordinates.append([x, y])
            
        return coordinates
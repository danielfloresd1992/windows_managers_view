import os, json, base64, sys
import re
import time



from PySide6.QtWidgets import (
    QFrame, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout,
    QSizePolicy, QPushButton
)
from PySide6.QtCore import Qt, Slot, QProcess,  QUrl, QPoint,  QRect
from PySide6.QtWebSockets import QWebSocket
from PySide6.QtGui import QPixmap, QCursor

from ..custon_label.interactive_imageLabel import interactive_imageLabel

from core.state_global.hwnd import hwndState
from core.capture_exaple import capture_window_by_hwnd, pil_image_to_png_bytes
from core.window_controller import set_window_always_on_top




script_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "workers", "capture_worker.py")
)



class Render_box(QFrame):
    
    
    def __init__(self, frames_per_milliseconds=100):
        super().__init__()
        self.open = True
        self.setAcceptDrops(True)
        
        self.analytical_mode = False
        self.websocket = None
        self.process = None
        self.frames_per_milliseconds = frames_per_milliseconds
        self.frame_count = 0
        self.last_fps_time = time.time()
        self.current_fps = 0
        
        self.with_image = 0
        self.height_image = 0
        
        self.setup_ui()
        hwndState.change_hwnd.connect(self.get_hwnd_and_print)
        #self.bar_options.hide()  # Oculta al iniciar
        



    def setup_ui(self):
        self.setObjectName('box-content')
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stack = QVBoxLayout(self)   # renombrado para no chocar con QWidget.layout()
        self.stack.setContentsMargins(0, 0, 0, 0)

        # Imagen principal


        self.imagen_label = interactive_imageLabel('viewing window')
        self.imagen_label.setAlignment(Qt.AlignCenter)
    
        self.imagen_label.installEventFilter(self)
        
        self.bar_options = QWidget()
        self.bar_options.setAttribute(Qt.WA_StyledBackground, True)
        self.bar_options.setMaximumHeight(30)
        self.bar_options.setObjectName("bar_options")
       


        bar_option_layout = QHBoxLayout(self.bar_options)
        bar_option_layout.setContentsMargins(10, 0, 10, 0)
        bar_option_layout.setSpacing(5)

        self.btn_cap = QPushButton("📷")
        self.btn_cap.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_cap.setObjectName("btn-bar")

        btn_play = QPushButton("▶")
        btn_play.setCursor(QCursor(Qt.PointingHandCursor))
        btn_play.setObjectName("btn-bar")

        btn_pause = QPushButton("||")
        btn_pause.setCursor(QCursor(Qt.PointingHandCursor))
        btn_pause.setObjectName("btn-bar")

        btn_stop = QPushButton("■")
        btn_stop.setCursor(QCursor(Qt.PointingHandCursor))
        btn_stop.setObjectName("btn-bar")

        btn_play.clicked.connect(self.init_loop)
        btn_pause.clicked.connect(self.pause_loop)
        btn_stop.clicked.connect(self.detroy_loop)

        self.text_fps = QLabel(f"Tasa de FPS: {self.current_fps}")
        self.text_fps.setObjectName('text-fps')
        
        self.text_size = QLabel(f'Tamaño del cuadro: {self.with_image}x{self.height_image}')
        self.text_size.setObjectName('text-fps')
        
        bar_option_layout.addWidget(self.text_fps)
        bar_option_layout.addWidget(self.text_size)
        bar_option_layout.addStretch(1)
        bar_option_layout.addWidget(self.btn_cap)
        bar_option_layout.addWidget(btn_play)
        bar_option_layout.addWidget(btn_pause)
        bar_option_layout.addWidget(btn_stop)



        self.stack.addWidget(self.imagen_label)
        self.stack.addWidget(self.bar_options)  
      
    
    
    
    # ---------------------------
    # Procesos de captura
    # ---------------------------
    def init_loop(self):
        try:
           
            print(f"🔄 Iniciando loop para hwnd: {self.hwnd}")
            if hasattr(self.process, 'canReadLine') :print(self.process.canReadLine())
            if self.hwnd is None:
                print("❌ No hay hwnd definido")
                return
                
            if self.process is None:
                self.process = QProcess(self)
                self.process.setProcessChannelMode(QProcess.MergedChannels)
                self.process.readyReadStandardOutput.connect(self.loop_show_result)
                
                # 🔥 USAR sys.executable EN LUGAR DE 'python'
                python_exe = sys.executable  # Esto apunta al Python que ejecuta la aplicación
                worker_script = 'src/workers/capture_woker.py'
                arguments = [worker_script, str(self.hwnd)]
                
                print(f"🐍 Usando Python: {python_exe}")
                if not os.path.exists(worker_script):
                    print(f"❌ Worker no encontrado: {worker_script}")
                    return
                    
                self.process.start(python_exe, arguments)
                
                if not self.process.waitForStarted(5000):
                    print("❌ No se pudo iniciar el proceso")
                    return
                    
                print("✅ Proceso de captura iniciado")
            else:
                self.process.readyReadStandardOutput.connect(self.loop_show_result)
                pass
                
        except Exception as e:
            print(f"💥 Error: {e}")
            import traceback
            traceback.print_exc()
            



    def pause_loop(self):
        if self.process:
            pass
            self.process.readyReadStandardOutput.disconnect(self.loop_show_result)
            self.text_fps.setText("Tasa de FPS: 0")
            print(self.process.processId())


    def detroy_loop(self):
        if self.process is not None:
            self.process.terminate()
            if not self.process.waitForFinished(3000):
                self.process.kill()
            self.process = None
            self.imagen_label.clear()
            self.imagen_label.setText("viewing window")
            self.close_socket()



    @Slot(int)
    def get_hwnd_and_print(self, hwnd=None):
        try:
            if hwnd is not None:
                self.hwnd = hwnd
            set_window_always_on_top(self.hwnd)
            buffer = capture_window_by_hwnd(self.hwnd)
            if buffer is None:
                return
            image = pil_image_to_png_bytes(buffer)
            if image is None:
                return
            self.update_streaming_frame(image, type_image='bytes', tets = False)
            self.bar_options.raise_()
        except Exception as e:
            print(f"💥 Error: {e}")



    def loop_show_result(self):
        if not self.process:
            return

        # Leer todos los datos disponibles
        data = self.process.readAllStandardOutput().data().decode('utf-8', errors='ignore')
        lines = data.strip().split('\n')
        
        # Procesar las líneas en pares (header e imagen)
        i = 0
        while i < len(lines) - 1:


            line1 = lines[i].strip()
            line2 = lines[i+1].strip()
            # Si la primera línea está vacía, saltar
            if not line1:
                i += 1
                continue
                
            # Verificar que no son mensajes de error
            if line1.startswith(('qt.', 'Traceback', 'File "', 'UnicodeEncodeError')):
                i += 1
                continue
                
            try:
                header = json.loads(line1)
                # Verificar que tiene la estructura esperada
                if not isinstance(header, dict) or 'timestamp' not in header:
                    i += 2
                    continue
                    
                image_bytes = base64.b64decode(line2)
              
                # Cálculo de FPS
                self.frame_count += 1
                now = time.time()
                if now - self.last_fps_time >= 1.0:
                    self.current_fps = self.frame_count
                    self.frame_count = 0
                    self.last_fps_time = now
                    self.text_fps.setText(f'Tasa de FPS: {self.current_fps}')
                    
                
                if not self.websocket == None: 
                    image_base64 = base64.b64encode(image_bytes).decode()
                    result_coordinates = self.imagen_label.get_coordinates(self.width, self.height)
                    data_to_Send = {
                        'header': header,
                        'image' : image_base64,
                        'roi_coordinates': result_coordinates
                    }
                    
                    if self.open == True:
                        self.open = False
                        self.websocket.sendTextMessage(json.dumps(data_to_Send))
                        print('frame sent to websocket')
                    else:
                        print('websocket busy, frame skipped')
                        
                    #self.update_streaming_frame(image_base64, type_image='base64', tets=True)
                    
            except (json.JSONDecodeError, Exception) as e:
                # Ignorar errores y continuar con el siguiente par
                self.open = True
                print(f"💥 Error procesando líneas: {e}")
            i += 2
            
            
        
        
    def update_streaming_frame(self, frame, type_image='base64', tets=False):
        try:
            if tets: self.open = True
            pixmap = QPixmap()
           
            map = False
            if type_image == 'base64':
                base64_str = re.sub(r'^data:image/\w+;base64,', '', frame)
                frame_bytes = base64.b64decode(base64_str)
                map = pixmap.loadFromData(frame_bytes, 'JPEG')
            else:
                map = pixmap.loadFromData(frame, "PNG")
            if map:
                if not hasattr(self, "cached_size") or self.cached_size != self.imagen_label.size():
                    self.cached_size = self.imagen_label.size()
                size = pixmap.size()
                self.width = size.width()
                self.height = size.height()
                self.text_size.setText(f'Tamaño del cuadro: {self.width}x{self.height}')
                pixmap_escalada = pixmap.scaled(
                    self.cached_size,
                    Qt.IgnoreAspectRatio,
                    Qt.SmoothTransformation,
                )
                self.imagen_label.setPixmap(pixmap_escalada)
                
                
        except Exception as e:
            print(f"💥 Error en update_streaming_frame: {e}")

            
        


    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-boxcap'):
            event.acceptProposedAction()
        else:
            event.ignore()



    def dropEvent(self, event):
        try:
            if event.mimeData().hasFormat("application/x-boxcap"):
                raw = bytes(event.mimeData().data("application/x-boxcap")).decode("utf-8")
                other_hwnd, other_title = raw.split("|", 1)
                self.get_hwnd_and_print(int(other_hwnd))
                # Evitar copiarse a sí mismo
                if int(other_hwnd) == getattr(self, "id_windows", None):
                    event.ignore()
                    return
                # Copiar datos del otro widget
                self.id_windows = int(other_hwnd)
                self.title = other_title
                event.acceptProposedAction()
                
                if self.websocket is None: self.init_websocket()
            else:
                event.ignore()
        except Exception as e:
            print(f"💥 Error en dropEvent: {e}")
            
            
            
    def init_websocket(self):        
      
        self.websocket = QWebSocket()
        # 2. Conectar señales del QWebSocket a slots de la clase
        self.websocket.connected.connect(self.on_connected)
        self.websocket.textMessageReceived.connect(self.on_text_message_received)

        # 3. Intentar abrir la conexión
        websocket_url = QUrl('ws://72.68.60.171:9000/ws')  # Cambia a tu URL de servidor
        self.websocket.open(websocket_url)
        
        
        
    @Slot()
    def on_connected(self):
        """Manejador llamado cuando la conexión WebSocket se ha establecido."""
        print("Conexión WebSocket establecida.")
       
      

    @Slot(str)
    def on_text_message_received(self, message):
        """Manejador llamado cuando se recibe un mensaje de texto."""
        try:
            data = json.loads(message)
            if data['status'] == 'success':
                processed_image = data['processed_image']
                self.update_streaming_frame(processed_image, type_image='base64')
            if data['status'] == 'error':
                raise Exception(data.get('message', 'Error desconocido del servidor'))
        except Exception as e:
            print(f"💥 Error al procesar mensaje WebSocket: {e}")
        finally:
            self.open = True

       
        
    
    @Slot()
    def on_disconnected(self):
        """Manejador llamado cuando la conexión WebSocket se cierra."""
        print("Conexión WebSocket cerrada.")
        
        
    def close_socket(self):
        self.websocket.close()

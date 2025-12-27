from PySide6.QtWebSockets import QWebSocket
from PySide6.QtCore import QObject, Signal, QUrl, QTimer, Slot
from PySide6.QtNetwork import QAbstractSocket



class Socket_services(QObject):
    
  

    connected_signal = Signal(bool, str)
    disconnected_signal = Signal(bool, str)
    re_connect_signal = Signal(str)
    
    
    def __init__(self):
        # 2. Ahora super().__init__() funcionará correctamente
        super().__init__()
        
        self.client = QWebSocket()
        self.client.connected.connect(self._on_connected)
        self.client.disconnected.connect(self._on_disconnected)
        self.client.textMessageReceived.connect(self.on_text_message_received)

        
      
    def conect_server(self, url):
        self.url = url
        self.client.open(QUrl(self.url))
        
    
    
    def _on_connected(self):
        print(f"Conneted to server")
        print('✅ WebSocket connected sucessfull')
        self.connected_signal.emit(True, 'Server connect') # Notifica a la UI
        
        if  hasattr(self, 'reconnect_timer'):
            self.reconnect_timer.stop()
            self.reconnect_timer.deleteLater()
            
            
            
        
    def _on_disconnected(self):
        print('❌ WebSocket offline')
        self._loop_conection()
        self.disconnected_signal.emit(False, "Server Offline")
        
        
        
    def _on_error(self, error):
        # El signal de error de Qt suele enviar información técnica
        error_msg = self.client.errorString()
        print(f"💥 Error socket: {error_msg}")
        
        
        self.disconnected_signal.emit(False, f"Error: {error_msg}")
        
        
        
    def _loop_conection(self):
        print('Bucle de reconexión al socket')
        self.reconnect_timer = QTimer()
        self.reconnect_timer.setInterval(5000)  # Intentar cada 5 segundos
        self.reconnect_timer.timeout.connect(self._on_timeout)
        self.reconnect_timer.start()
        
    
    def _on_timeout(self): 
        print('hola')
        self.conect_server(self.url) 
        self.re_connect_signal.emit("Reconectando...")
        
        
        
    
    
    @Slot(str)
    def on_text_message_received(self, message):
        print(message)
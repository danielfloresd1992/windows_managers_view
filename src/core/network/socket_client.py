from PySide6.QtWebSockets import QWebSocket
from PySide6.QtCore import QObject, Signal, QUrl, QTimer, Slot
from PySide6.QtNetwork import QAbstractSocket
import json



class Socket_services(QObject):
    
  

    connected_signal = Signal(bool, str)
    disconnected_signal = Signal(bool, str)
    re_connect_signal = Signal(str)
    
    signal_inference = Signal(dict)
    
    
    
    def __init__(self, url=None, type_inference=None):
        # 2. Ahora super().__init__() funcionará correctamente
        super().__init__()
        self.url = url
        self.type_inference = type_inference
        self.client = QWebSocket()
        self.client.connected.connect(self._on_connected)
        self.client.disconnected.connect(self._on_disconnected)
        self.client.textMessageReceived.connect(self.on_text_message_received)


        
      
    def conect_server(self):
        self.client.open(QUrl(f'{self.url}/{self.type_inference}'))
        
    
    
    
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
        self.conect_server() 
        self.re_connect_signal.emit("Reconectando...")
        
        
        
        
    def send_frame(self,component_key, frame_data):
        try:
            if component_key is None: raise ValueError('component_key o campos de frame_data son indefinidos')
            
            data_to_send = {
                'event': 'inference',
                'id_connection': self.id_connection,
                'type_inference': self.type_inference,
                'component_key': component_key,
                'data': frame_data
            }

            self.client.sendTextMessage(json.dumps(data_to_send))
        except Exception as e:

            print(e)
    
    
    
    
    @Slot(str)
    def on_text_message_received(self, message):
    
        data = json.loads(message)

        if data.get('event') is not None:
            
            if data['event'] == 'conection_init': self.id_connection = data['id_connection']

            elif data['event'] == 'inference': self.signal_inference.emit(data)
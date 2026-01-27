from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QSslConfiguration , QNetworkCookieJar, QNetworkReply, QSslSocket
from PySide6.QtCore import QObject , QUrl, QByteArray,Signal
import json



class Jarvis_api(QObject):
    
    
    error_request = Signal(str)
    selected_establishmentSignal = Signal(dict)
    
    
    def __init__(self, emailuser=None, password=None, url_api=None):
        super().__init__()
        self.email_jarvis_request = emailuser
        self.password_jarvis_request = password
        self.url_api_base = url_api

        self.session_user = None
        self.error_User = None
        self.list_of_establishments = None
        self.selected_establishment = None
        
        self.manager_request = QNetworkAccessManager()
        cookie_jar = QNetworkCookieJar()
        self.manager_request.setCookieJar(cookie_jar)
        
        self.ssl_config = QSslConfiguration.defaultConfiguration()  # OBTIENE LA CONFIGURACIÓN SSL
        self.ssl_config.setPeerVerifyMode(QSslSocket.VerifyNone) # DESACTIVA ERROR DE CERTIFICADOS SSL INVALIDO
        
        self.create_session()
        self.fetching_establishment()
        
        
    
    def selection_establishment(self, name):
        for iteration in self.list_of_establishments:
            if iteration['name'] == name:
                self.selected_establishment = iteration
        print(self.selected_establishment)
    
    
    
    
    def create_session(self):
        body_dic = { "email": self.email_jarvis_request, "password": self.password_jarvis_request } 
        response = self._request(resource='auth/login', body=body_dic, berb='post')
        response.finished.connect(lambda: self._handler_response_session(response))
        
        
        
    def fetching_establishment(self):
        response = self._request(resource='localligth')
        response.finished.connect(lambda: self._handler_response_establishment(response))
        
        
        
    def send_alert_to_api(self, title='Alerta de perimetral', params=None):
        try:
            if self.session_user is None:
                self.error_request.emit('Error de sesión')
                return None
            if self.selected_establishment is None:
                self.error_request.emit('Seleciones un establecimiento o lugar')
                return None

            imageurl = 'https://amazona365.ddns.net/api_jarvis/v1/novelty/img=novelty_1769530415033.jpeg'
            data = {
                'title': f'{title} ("Modo IA")',
                'userName': f"{self.session_user['name']} {self.session_user['surName']}",
                
                'userId': self.session_user['_id'],
                'localName': self.selected_establishment['name'],
                'localId': self.selected_establishment['_id'],
                'ruleBonus': {'worth': 0, 'acomulate': 0},
                'alertId': '6977974dfed1f0dcaffceefa',
                'description': 'Alerta generada con IA',
                'imageToShare': imageurl,
                'menu': f'{title} ("Modo IA")\Proximamente...\ignorar esta alerta',
                'imageUrl': [
                    {'url': imageurl, 'caption': 'alert'}
                ]
            }
            print(data)
            response = self._request(resource='novelties', body=data, berb='post')
            response.finished.connect(lambda: self.__handler_response_alert(response))
        except Exception as e:
            print(e)        
        
        
        
    def _request(self, resource='', body=None, berb='get'):
        try:
            request = QNetworkRequest(QUrl(f'{self.url_api_base}/{resource}'))
            request.setSslConfiguration(self.ssl_config)
            request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
            
            # Agregar cabeceras personalizadas
            request.setRawHeader(QByteArray(b'Source-Application'), QByteArray(b'Jarvis_Vision'))
            request.setRawHeader(QByteArray(b'Version-App'), QByteArray(b'1.0'))
            
            if berb == 'post':
                body_byte = QByteArray(json.dumps(body).encode("utf-8"))
                return self.manager_request.post(request, body_byte)
            else:
                return self.manager_request.get(request)
                
        except Exception  as e:
            print(e)
            
            
    
    
    def _handler_response_session(self, reply: QNetworkReply):
        if reply.error() == QNetworkReply.NetworkError.NoError: 
            data = reply.readAll().data().decode() 
            try: 
                json_data = json.loads(data) 
                print('User autenticated')
                self.session_user = json_data
                print(json_data)
            except Exception:
                print("Respuesta texto:", data)
             
        else: 
            print("Error en la respuesta:", reply.errorString())
            self.error_request.emit('Error en la autenticación en el servicio de Jarvis365')
            
            
            
            
    def _handler_response_establishment(self, reply: QNetworkReply):
        if reply.error() == QNetworkReply.NetworkError.NoError: 
            data = reply.readAll().data().decode() 
            try: 
                json_data = json.loads(data) 
          
                self.list_of_establishments = json_data
         
            except Exception:
                print("Respuesta texto:", data)
        else:
        
            print("Error en la respuesta:", reply.errorString())
            self.error_request.emit('Error al obtener la lista de clientes')
            
            
    
    def __handler_response_alert(self, reply: QNetworkReply):
        if reply.error() == QNetworkReply.NetworkError.NoError: 
            data = reply.readAll().data().decode() 
            try: 
                json_data = json.loads(data) 
          
                print(json_data)
         
            except Exception:
                print("Respuesta texto:", data)
        else:
            data = reply.readAll().data().decode() 
         
            json_data = json.loads(data) 
            print(json_data)
            print("Error en la respuesta:", reply.errorString())
            self.error_request.emit('Error al enviar la alerta')
            
            
            
            
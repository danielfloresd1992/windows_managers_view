from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QSslConfiguration , QNetworkCookieJar, QNetworkReply
from PySide6.QtCore import QObject , QUrl, QByteArray
import json



class Jarvis_api(QObject):
    
    
    def __init__(self, username=None, password=None, url_api=None):
        super().__init__()
        self.email_jarvis_request = username
        self.password_jarvis_request = password
        self.url_api_base = QUrl(url_api)
        
        self.Session = None
        
        self.manager_request = QNetworkAccessManager()
        cookie_jar = QNetworkCookieJar()
        self.manager_request.setCookieJar(cookie_jar)
        
        self.ssl_config = QSslConfiguration.defaultConfiguration()  # OBTIENE LA CONFIGURACIÓN SSL
        self.ssl_config.setPeerVerifyMode(self.ssl_config) # DESACTIVA ERROR DE CERTIFICADOS SSL INVALIDO
        
        self.create_session()
        
    
    def create_session(self):
        body_dic = f' "email":{self.email_jarvis_request}, "password": {self.password_jarvis_request}'
        body_byte = QByteArray(json.dumps(body_dic).encode("utf-8"))
        response = self._request(resource='auth/login', body=body_byte, berb='post')
        print(response)
        
        
    def _request(self, resource='', body=None, berb='get'):
        response = None
        request = QNetworkRequest(f'{self.url_api_base}/{resource}')
        request.setSslConfiguration(self.ssl_config)
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        
        if berb == 'post':
            response = self.manager_request.post(request, body)
        else:
            response = self.manager_request.get(request)
            
        return response
            
            
            
            
            
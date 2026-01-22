from hikvisionapi import Client
import xml.etree.ElementTree as ET
import threading
import time
import requests
import json
import cv2
import matplotlib.pyplot as plt



def open_device(name, ip, http_port, rtsp_port, user, password):
    result = {
        'valid': False,
        'data': {
            'name': name,
            'ip':ip,
            'http_port': http_port,
            'rtsp_port':rtsp_port,
            'user': user,
            'password': password
        }
    }
    try:
    
        api = Client( f'http://{ip}:{http_port}', user, password, timeout=5)
        response = api.System.deviceInfo(method='get')
   
        video_inputs = api.System.Video.inputs.channels(method='get')
        
        data = json.loads(video_inputs)
        
        
        for i in data['VideoInputChannelList']['VideoInputChannel']: 
            print(i)
        
      
        
        result['valid'] = True
        result['response'] =  response
        
       
        return result
        
        
        
    except requests.exceptions.HTTPError as e:

        if e.response and e.response.status_code == 401:
            result['message'] = f'{ip}:{http_port}", False, "invalid_credentials'
        else:
            result['message'] = f'{ip}:{http_port}", False, "invalid_credentials'
            
        result['error'] = 'invalid_credentials'
        return result
            
    except requests.exceptions.ConnectionError:
            result['message'] = f'{ip}:{http_port}", connection_error'
            result['error'] = 'connection_error'
            return result
            
    except requests.exceptions.Timeout:
        result['message'] = f'{ip}:{http_port}", timeout'
        result['error'] = 'timeout'
        return result
    except Exception as e:
        result['message'] = f'{ip}:{http_port}, unknown_error: {str(e)}'
        result['error'] = 'unknown_error'
        return result
        
        

result = open_device(name='amazonas', ip='72.68.60.117', http_port='8080', rtsp_port=554, user='test', password='test1234')





if result['valid']:
   
    url = f"rtsp://{result['data']['user']}:{result['data']['password']}@{result['data']['ip']}:{result['data']['rtsp_port']}/Streaming/Channels/202"
    
    cap = cv2.VideoCapture(url)
    

    '''
    if not cap.isOpened():
        print('Error conection rstp')
        exit()
        
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print('Error read frame')
            continue
        
        #cv2.imshow('Request successfull', frame)
        
        plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) 
        plt.show()
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    
    '''
    
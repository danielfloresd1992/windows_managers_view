import json
import os
from pathlib import Path
from appdirs import user_config_dir



class SettingsModel:
    
    def __init__(self, app_name='windows_managers_view', filename='config.json'): 
        project_root = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(project_root, ".."))
        
        config_dir = user_config_dir(app_name)
        os.makedirs(config_dir, exist_ok=True)
        
        self.file_path = os.path.join(config_dir, filename)

        self.data = {}
        self.load_config()
        
        
        
    def load_config(self): 
        print(self.file_path)
        if os.path.exists(self.file_path): 
            try:
                with open(self.file_path, 'r', encoding='utf-8') as file: 
                    self.data = json.load(file) 
                    print('Archivo de configuración creado 📄')
            except json.JSONDecodeError: # Si el archivo está vacío o corrupto, regenerar 
                self.data = self.default_config() 
                self.save_config()
                print('Archivo de configuración cargado ✅')
        else: 
            self.data = self.default_config()
            self.save_config()
                
                
                
                
    def save_config(self): 
        with open(self.file_path, 'w', encoding='utf-8') as file: 
            json.dump(self.data, file, indent=4)
                
                
                
    def default_config(self): 
        return { 'last_inference': 'default', 'boxs_config': [{'index': i} for i in range(16)] }
    
    
    
    def set(self, key, value): 
        self.data[key] = value 
        self.save_config() 
        
        
        
    def get(self, key, default=None): 
        return self.data.get(key, default)
    
    
    
    def update_box_config(self, index, key, value):
        """ Actualiza o añade una propiedad dentro de un diccionario de boxs_config. """ 
        for box in self.data['boxs_config']: 
            print(index)
            print(box['index'])
            if box['index'] == index:
                print(box)
                box[key] = value 
                self.save_config() 
                
                return # Si no existe el índice, opcionalmente lo creamos 
        new_box = {'index': index, key: value} 
        self.data['boxs_config'].append(new_box) 
        self.save_config()
        
        
    def get_box_config(self, index):
        for box in self.data['boxs_config']:
            if box['index'] == index:
               return box

        
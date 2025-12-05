import json
from pathlib import Path
import appdirs # Necesitarás instalar esta librería: pip install appdirs



class SettingsModel:
    def __init__(self):
        self.organization_name = 'amazonas365'
        self.application_name = 'windows_managers_view'

        config_dir = Path(appdirs.user_config_dir(self.application_name, self.organization_name))
        config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = config_dir / '"user_settings.json'
        
        self.data = self._get_default_settings()
        self.load_settings()
        
        
        
    def _get_default_settings(self):
        return {
            "coordinates_roi": [[100, 100], [900, 100], [900, 900], [100, 900]]
        }
        
        
        
    def load_settings(self):
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    settings = json.load(f)
                    self.data.update(settings)
                    
            except (json.JSONDecodeError, IOError):
                pass
            
            
        return self._get_default_settings()
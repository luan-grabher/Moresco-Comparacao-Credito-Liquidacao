import json
import os


def get_config_from_json():
    config_file_path = 'config.json'
    
    is_config_file_exists = os.path.exists(config_file_path)
    if not is_config_file_exists:
        return create_config_file()        
    
    with open('config.json', 'r') as f:
        config = json.load(f)
                
    return config

def get_config(keys : list = [], type_needed = None):
    config = get_config_from_json()
    
    value = None
    if keys:
        for key in keys:
            if key in (value if value else config):
                value = value[key] if value else config[key]
                
                
    if type_needed and not isinstance(value, type_needed):
        return None
    
    return value
        
def create_config_file():
    config = {
        'test': {
            'path': 'C:/Users/USER/Documents/Moresco-Comparacao-Credito-Liquidacao/downloads'
        }
    }
    
    with open('config.json', 'w') as f:
        json.dump(config, f)
        
    return config


if __name__ == '__main__':
    print(get_config(['test', 'path']))
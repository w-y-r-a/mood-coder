from models import Setup
from config import config

def same_key(key: str):
    key1 = config.get('Global', 'BINDING_KEY')
    if key1 == key:
        return True
    return False
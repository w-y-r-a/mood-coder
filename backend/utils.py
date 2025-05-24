from models import Setup
from config import config

def same_key(key: str) -> bool:
    key1 = config.get('Global', 'BINDING_KEY')
    return key1 == key
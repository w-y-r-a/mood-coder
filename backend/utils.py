import hashlib
import secrets

def hash_key(key: str) -> str:
    """Hash the binding key for secure storage"""
    salt = secrets.token_hex(16)
    return hashlib.pbkdf2_hmac('sha256', key.encode(), salt.encode(), 100000).hex() + ':' + salt

def verify_key(key: str, hashed: str) -> bool:
    """Verify a key against its hash"""
    stored_hash, salt = hashed.split(':')
    return hashlib.pbkdf2_hmac('sha256', key.encode(), salt.encode(), 100000).hex() == stored_hash
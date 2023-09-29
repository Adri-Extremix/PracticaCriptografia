import os
import base64
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

def guarrear(pwd):
    salt = os.urandom(16)
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
    )
    key = kdf.derive(bytes(pwd, 'ascii'))
    b64_key = base64.b64encode(key)
    key_final = b64_key.decode('ascii')
    
    b64_salt = base64.b64encode(salt)
    salt_final = b64_salt.decode('ascii')
    
    return salt_final, key_final

def verificar(pwd, key, salt):
    bytes_b64_salt = bytes(salt, 'ascii')
    bytes_salt = base64.b64decode(bytes_b64_salt)
    kdf = Scrypt(
        salt=bytes_salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
    )
    bytes_b64_key = bytes(key, 'ascii')
    bytes_key = base64.b64decode(bytes_b64_key)
    return kdf.verify(bytes(pwd, 'ascii'), bytes_key)
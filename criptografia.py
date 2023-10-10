import os
import base64
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

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

def derivar_key_sign_up(pwd):

    salt = os.urandom(16)

    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000,

    )
    key = kdf.derive(bytes(pwd,'ascii'))



    b64_salt = base64.b64encode(salt)
    salt_final = b64_salt.decode('ascii')

    

    return key,salt_final

def derivar_key(pwd,salt):

    


    bytes_b64_salt = bytes(salt, 'ascii')
    bytes_salt = base64.b64decode(bytes_b64_salt)

    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=bytes_salt,
    iterations=480000,

    )

    key = kdf.derive(bytes(pwd,'ascii'))

    return key


def encriptado_autenticado(datos,key):

    data = bytes(datos,'ascii')
    chacha = ChaCha20Poly1305(key)
    nonce_bytes = os.urandom(12)
    ct_bytes = chacha.encrypt(nonce_bytes,data,None)

    b64_ct = base64.b64encode(ct_bytes)
    ct = b64_ct.decode('ascii')

    b64_nonce = base64.b64encode(nonce_bytes)
    nonce = b64_nonce.decode('ascii')

    return ct,nonce

def desencriptado_autenticado(ct,nonce,key):

    bytes_b64_nonce = bytes(str(nonce), 'ascii')
    bytes_nonce = base64.b64decode(bytes_b64_nonce)

    bytes_b64_ct = bytes(ct, 'ascii')
    bytes_ct = base64.b64decode(bytes_b64_ct)

    chacha = ChaCha20Poly1305(key)
    data_bytes = chacha.decrypt(bytes_nonce,bytes_ct,None)

    data = data_bytes.decode('ascii')

    return data
import os
import base64
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

def generar_token(pwd):
    # Genero un salt de 16 bits pseudoaleatorios
    salt = os.urandom(16)
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
    )
    # Genero el token a través de la contraseña del usuario
    key = kdf.derive(bytes(pwd, 'ascii'))

    # Convierto tanto el salt como el token a base64 y después a ascii
    # Con el objetivo de insertarlos en la base de datos
    b64_key = base64.b64encode(key)
    key_final = b64_key.decode('ascii')
    
    b64_salt = base64.b64encode(salt)
    salt_final = b64_salt.decode('ascii')
    
    return salt_final, key_final

def verificar(pwd, key, salt):
    # Reconvierto el salt y el token guardado a bytes en base64 y despues a bytes
    bytes_b64_salt = bytes(salt, 'ascii')
    bytes_salt = base64.b64decode(bytes_b64_salt)
    
    bytes_b64_key = bytes(key, 'ascii')
    bytes_key = base64.b64decode(bytes_b64_key)

    kdf = Scrypt(
        salt=bytes_salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
    )
    # Verifico que la contraseña del usuario corresponde con el token
    return kdf.verify(bytes(pwd, 'ascii'), bytes_key)

def derivar_key_sign_up(pwd):
    # Genero un salt pseudoaleatorio
    salt = os.urandom(16)

    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000,

    )
    # Genero la clave derivada a partir de la contraseña
    key = kdf.derive(bytes(pwd,'ascii'))
    # Convierto el salt en base64 y a ascii para guardarlo
    b64_salt = base64.b64encode(salt)
    salt_final = b64_salt.decode('ascii')

    return key,salt_final

def derivar_key(pwd,salt):
    # Reconvierto el salt guardado
    bytes_b64_salt = bytes(salt, 'ascii')
    bytes_salt = base64.b64decode(bytes_b64_salt)

    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=bytes_salt,
    iterations=480000,

    )
    # Genero la clave derivada con la contraseña 
    key = kdf.derive(bytes(pwd,'ascii'))

    return key


def encriptado_autenticado(datos,key):
    
    data = bytes(datos,'ascii')
    chacha = ChaCha20Poly1305(key)
    # Genero el nonce
    nonce_bytes = os.urandom(12)
    # Cifro los datos con el nonce
    ct_bytes = chacha.encrypt(nonce_bytes,data,None)
    # Convierto los datos cifrados y el nonce a base64 y a ascii
    b64_ct = base64.b64encode(ct_bytes)
    ct = b64_ct.decode('ascii')

    b64_nonce = base64.b64encode(nonce_bytes)
    nonce = b64_nonce.decode('ascii')

    return ct,nonce

def desencriptado_autenticado(ct,nonce,key):
    # Reconvierto los datos cifrados y el nonce a bytes
    bytes_b64_nonce = bytes(str(nonce), 'ascii')
    bytes_nonce = base64.b64decode(bytes_b64_nonce)

    bytes_b64_ct = bytes(ct, 'ascii')
    bytes_ct = base64.b64decode(bytes_b64_ct)

    chacha = ChaCha20Poly1305(key)
    # Descifro los datos con el nonce
    data_bytes = chacha.decrypt(bytes_nonce,bytes_ct,None)

    data = data_bytes.decode('ascii')

    return data
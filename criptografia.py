import os
import base64
import json

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization

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


def get_serialized_key(path,pwd=None):
	with open(path, "rb") as key_file:
		private_key = serialization.load_pem_private_key(
			key_file.read(),
			password=bytes(pwd, 'ascii'),
		)
	return private_key
    
def firmar(operacion, id, usuario, pass_firma):
	private_key = get_serialized_key("PKI1/Banki/BankiKey.pem",pass_firma)
	operacion = usuario + " - " + operacion 
	op_bytes = bytes(operacion, 'ascii')
	signature = private_key.sign(
		op_bytes,
		padding.PKCS1v15(),
		hashes.SHA1()
	)
	firma_64 = base64.b64encode(signature)
	firma = firma_64.decode('ascii')
	with open("recibos/operacion-" + id + ".json", "w", encoding='ascii') as file:
		message = {
			"mensaje": operacion,
            "firma": firma,
			"certificado": "PKI1/Banki/BankiCert.pem",
			"cadena_certificacion": "PKI1/Banki/certs.pem" 
        }
		json.dump(message, file)


def verify_sign(public_key,operation,firma):
	try:	
		public_key.verify(
			firma,
			operation,
			padding.PKCS1v15(),
			hashes.SHA1()
		)
		return 0
	except:
		return -1

def verify_bill(path):
	with open(path,"rb") as file:
		data = json.load(file)
	with open(data["certificado"],"rb") as file:
		cert_banki = x509.load_pem_x509_certificate(file.read())
	with open(data["cadena_certificacion"],"rb") as file:
		cert_chain = x509.load_pem_x509_certificates(file.read())
	

	firma_b64 = bytes((data["firma"]), 'ascii')
	firma_bytes = base64.b64decode(firma_b64)

	if verify_sign(cert_banki.public_key(),bytes(data["mensaje"], 'ascii'),firma_bytes) == -1:
		print("No verifico el recibo")
		return -1
	
	if verify_sign(cert_chain[0].public_key(), cert_banki.tbs_certificate_bytes, cert_banki.signature) == -1:
		print("No verifico Banki")
		return -1
	
	if verify_sign(cert_chain[0].public_key(), cert_chain[0].tbs_certificate_bytes, cert_chain[0].signature) == -1:
		print("No verifico la raiz")
		return -1
	return 0

"""
	return 0 
	indice = 0;
	cert = cert_banki
	print(cert.public_key())
	cert_next = cert_chain[indice]
	print(cert_next.public_key())
	while (1):
		if verify_sign(cert_next.public_key(), cert.tbs_certificate_bytes, cert.signature) == -1:
			print(indice)
			return -1
		if (cert.issuer == cert.subject):
			return 0
		if (cert_next.issuer == cert_next.subject):
			cert = cert_next
		else: 
			cert = cert_next
			indice += 1
			cert_next = cert_chain[indice]"""

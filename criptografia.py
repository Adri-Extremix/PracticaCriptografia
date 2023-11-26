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
	"""Función que se encarga de derivar una contraseña"""
	#Genera un salt aleatorio, y genera un kdf
	salt = os.urandom(16)
    
	kdf = Scrypt(
		salt=salt,
		length=32,
		n=2**14,
		r=8,
		p=1,
	)

	#Deriva la clave y la pasa a base 64
	key = kdf.derive(bytes(pwd, 'ascii'))
	b64_key = base64.b64encode(key)
	key_final = b64_key.decode('ascii')

	#Pasa el salt a base 64
	b64_salt = base64.b64encode(salt)
	salt_final = b64_salt.decode('ascii')
	return salt_final, key_final

def verificar(pwd, key, salt):
	"""Función que se encarga de verificar una clave"""
	#Obtiene el salt en bytes y genera un kdf
	bytes_b64_salt = bytes(salt, 'ascii')
	bytes_salt = base64.b64decode(bytes_b64_salt)
	kdf = Scrypt(
		salt=bytes_salt,
		length=32,
		n=2**14,
		r=8,
		p=1,
	)

	#Pasa la key a bytes y se verifica con el kdf
	bytes_b64_key = bytes(key, 'ascii')
	bytes_key = base64.b64decode(bytes_b64_key)
	return kdf.verify(bytes(pwd, 'ascii'), bytes_key)

def derivar_key_sign_up(pwd):
	"""Función que se encarga de deruvar la clave del sign up"""
    #Genera un salt y genera un kdf 
	salt = os.urandom(16)

	kdf = PBKDF2HMAC(
	algorithm=hashes.SHA256(),
	length=32,
	salt=salt,
	iterations=480000,
	)

	#Se pasan el kdf y el saltr a base 64, luego se devuelven
	key = kdf.derive(bytes(pwd,'ascii'))
	b64_salt = base64.b64encode(salt)
	salt_final = b64_salt.decode('ascii')
	return key,salt_final

def derivar_key(pwd,salt):
	"""Función que se encarga de derivar una clave"""
	#Obtiene los datos en bytes
	bytes_b64_salt = bytes(salt, 'ascii')
	bytes_salt = base64.b64decode(bytes_b64_salt)

	#Obtiene un kdf con el salt
	kdf = PBKDF2HMAC(
	algorithm=hashes.SHA256(),
	length=32,
	salt=bytes_salt,
	iterations=480000,
	)

	#Deriva la contraseña en bytes usando el kdf
	key = kdf.derive(bytes(pwd,'ascii'))
	return key

def encriptado_autenticado(datos,key):
	"""Función que encripta un mensaje autenticado"""
	#Se pasan los datos a bytes y emplea el algoritmo ChaCha20Poly1305 para encriptar
	data = bytes(datos,'ascii')
	chacha = ChaCha20Poly1305(key)

	#Se geneera un nonce y se encriptan los datos
	nonce_bytes = os.urandom(12)
	ct_bytes = chacha.encrypt(nonce_bytes,data,None)

	#Guarda y devuelve los datos encriptados y el nonce en base 64
	b64_ct = base64.b64encode(ct_bytes)
	ct = b64_ct.decode('ascii')

	b64_nonce = base64.b64encode(nonce_bytes)
	nonce = b64_nonce.decode('ascii')

	return ct,nonce

def desencriptado_autenticado(ct,nonce,key):
	"""Función que desencripta un mensaje autenticado"""
	#Obtiene los datos de base64 a bytes
	bytes_b64_nonce = bytes(str(nonce), 'ascii')
	bytes_nonce = base64.b64decode(bytes_b64_nonce)

	bytes_b64_ct = bytes(ct, 'ascii')
	bytes_ct = base64.b64decode(bytes_b64_ct)

	#Se desencripta los datos usando el algoritmo ChaCha20Poly1305
	chacha = ChaCha20Poly1305(key)
	data_bytes = chacha.decrypt(bytes_nonce,bytes_ct,None)
	data = data_bytes.decode('ascii')
	return data


def get_serialized_key(path,pwd=None):
	"""Función que obtiene la clave privada del fichero serializado"""
	with open(path, "rb") as key_file:
		private_key = serialization.load_pem_private_key(
			key_file.read(),
			password=bytes(pwd, 'ascii'),
		)
	return private_key
    
def firmar(operacion, id, usuario, pass_firma):
	"""Función que firma un mensaje"""
	#Se obtiene la clave privada del fichero serializado .pem
	private_key = get_serialized_key("PKI/Banki/Akey.pem",pass_firma)

	#Se formatea la operación
	operacion = usuario + " - " + operacion 
	op_bytes = bytes(operacion, 'ascii')

	#Obtiene la firma y se pasa a base 64
	signature = private_key.sign(
		op_bytes,
		padding.PSS(
			mgf=padding.MGF1(hashes.SHA256()),
			salt_length=padding.PSS.MAX_LENGTH
		),
		hashes.SHA256()
	)
	firma_64 = base64.b64encode(signature)
	firma = firma_64.decode('ascii')

	#Se escribe el recibo en formato JSON, que contiene el mensae, la firma, el certificado y la cadena de ceritficación
	with open("recibos/operacion-" + usuario + "-" + id + ".json", "w", encoding='ascii') as file:
		message = {
			"mensaje": operacion,
		    "firma": firma,
			"certificado": "PKI/Banki/Acert.pem",
			"cadena_certificacion": "PKI/Banki/certs.pem" 
		}
		json.dump(message, file, indent=4)

def verify_sign_SHA256(public_key,operation,firma):
	"""Función que verifica una firma con el algoritmo SHA256 y padding PSS"""
	try:	
		public_key.verify(
			firma,
			operation,
			padding.PSS(
			    mgf=padding.MGF1(hashes.SHA256()),
			    salt_length=padding.PSS.MAX_LENGTH
			),
			hashes.SHA256()
		)
		return 0
	except:
		return -1


def verify_sign_SHA1(public_key,operation,firma):
	"""Función que verifica una firma con el algoritmo SHA1 y padding PKCS1v15"""
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
	"""Función que verifica la firma y la cadena de certificación"""
    #Abre los archivos y se guardan
	try:
		with open(path,"rb") as file:
		    data = json.load(file)
		with open(data["certificado"],"rb") as file:
		    cert_banki = x509.load_pem_x509_certificate(file.read())
		with open(data["cadena_certificacion"],"rb") as file:
		    cert_chain = x509.load_pem_x509_certificates(file.read())
	except:
		return -1

	#Intenta hacer un cast de base 64 a bytes
	try:
		firma_b64 = bytes((data["firma"]), 'ascii')
		firma_bytes = base64.b64decode(firma_b64)
	except: 
		return -1

	#Verifica la firma
	if verify_sign_SHA256(cert_banki.public_key(),bytes(data["mensaje"], 'ascii'),firma_bytes) == -1:
		return -1

	#Verifica la cadena de certificación
	indice = 0;
	cert = cert_banki
	cert_next = cert_chain[indice]
	while (1):
		#Verifica la firma
		if verify_sign_SHA1(cert_next.public_key(), cert.tbs_certificate_bytes, cert.signature) == -1:
		    return -1
		#Si está en la raíz, para
		if (cert.issuer == cert.subject):
		    return 0
		#Si el siguiente es la raíz, solo actualizas el actual
		if (cert_next.issuer == cert_next.subject):
		    cert = cert_next
		#Si el siguiente no es la raíz, se actualiza el actual y el siguiente
		else: 
		    cert = cert_next
		    indice += 1
		    cert_next = cert_chain[indice]

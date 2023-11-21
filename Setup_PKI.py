
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
import os
def generate_private_key():
	private_key = rsa.generate_private_key(
		public_exponent=65537,
		key_size=2048,
	)
	return private_key
    
def serialize_private_key(private_key):
	#key = AAAAAAAAAAAAAAAAAAHHHHHHHHHHHH 
	pem = private_key.private_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PrivateFormat.PKCS8,
		encryption_algorithm=serialization.BestAvailableEncryption(bytes(os.getenv("PASSWORD_FIRMA"),'ascii'))
	) 
	with open("PKI1/Banki/BankiKey.pem","wb") as f:
		f.write(pem)
	return
    
#def serialize_public_key(private_key):
#	publick_key = private_key.public_key()
#	pem = public_key.public_bytes(
#    	encoding=serialization.Encoding.PEM,
#    	formar=serialization.PublicFormat.SubjectPublicKeyInfo
#    )
#	with open("PKI1/Banki/ac1cert.pem")
#	return
    

def create_CSR(country,estado,localidad,nombre_org,nombre,private_key):
	csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
		x509.NameAttribute(NameOID.COUNTRY_NAME,country),
		x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME,estado),
		x509.NameAttribute(NameOID.LOCALITY_NAME,localidad),
		x509.NameAttribute(NameOID.ORGANIZATION_NAME,nombre_org),
		x509.NameAttribute(NameOID.COMMON_NAME,nombre),
	])).sign(private_key,hashes.SHA256())
	with open("PKI1/Banki/CSR.pem","wb") as f:
		f.write(csr.public_bytes(serialization.Encoding.PEM))
		
private_key = generate_private_key()
serialize_private_key(private_key)
create_CSR(u"ES",u"MADRID",u"LEGANES",u"CRIPTO",u"BANKI",private_key)
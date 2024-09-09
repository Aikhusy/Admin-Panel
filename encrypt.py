import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes



def derive_key(passphrase, salt):
    
    return scrypt(passphrase, salt, key_len=32, N=2**14, r=8, p=1)

# Encrypt the password
def encrypt_password(password, passphrase):
    salt = get_random_bytes(16)  
    key = derive_key(passphrase, salt)
    cipher = AES.new(key, AES.MODE_GCM)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(password.encode('utf-8'))
    return base64.b64encode(nonce + salt + tag + ciphertext).decode('utf-8')
from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto import Random
from Crypto.Cipher import AES

BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                    chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

key = md5('password'.encode('utf8')).hexdigest()


class Encryption(object):

    def __init__(self):
        pass

    def encrypt(self, raw):
        raw = pad(raw)
        iv = b'\xe5U\xea\xdd\xbf\xf4\xcd\xef\xc2g\xdc\xce\x16\xb6\xf5\xd7'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:])).decode('utf8')

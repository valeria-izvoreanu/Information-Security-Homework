import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233
kPrim = 'WmZq3t6w9z$C&F)J'
iv = '0102030405060708'
key = ''


def ecb(blocks, key):
    text = ''
    #decripteaza fiecare bloc si il adauga variabilei text
    for i in blocks:
        cipher = Cipher(algorithms.AES(key), modes.ECB())
        decryptor = cipher.decryptor()
        textBlock = decryptor.update(i)
        text = text + textBlock.decode('latin-1')
    return text


def myxor(var1, var2):
    return bytes(a ^ b for a, b in zip(var1, var2))


def ofb(blocks, key, iv):
    #cripteaza vectorul iv si il salveaza in var flux
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    flux = encryptor.update(iv) + encryptor.finalize()
    #xoreaza cifrul cu fluxul
    cipherContent = myxor(blocks[0], flux)
    #repeta operatia pentru toate blocurile
    for i in range(1, len(blocks), 1):
        encryptor = cipher.encryptor()
        flux = encryptor.update(flux) + encryptor.finalize()
        cipherContent += myxor(blocks[i], flux)
    return cipherContent.decode('latin-1')



print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)

#citeste modul de operare
Response = ClientSocket.recv(2048)
opMod = Response.decode('latin-1')
print(opMod)
#citeste si decripteaza cheia
Response = ClientSocket.recv(2048)
if opMod == 'ECB':
    cipher = Cipher(algorithms.AES(bytes(kPrim, 'utf-8')), modes.ECB())
else:
    cipher = Cipher(algorithms.AES(bytes(kPrim, 'utf-8')), modes.OFB(bytes(iv, 'utf-8')))
decryptor = cipher.decryptor()
key = decryptor.update(Response)
print(key)
#anunta KM ca A poate incepe criptarea
ClientSocket.send(str.encode('Start'))
#citeste textul criptat
plaintext = ClientSocket.recv(2048)
#separa textul in blocuri
blocks = [plaintext[i:i + 16] for i in range(0, len(plaintext), 16)]
#decripteaza blocurile in dependenta de modul setat
if opMod == 'ECB':
    text = ecb(blocks, key)
    print(text)
else:
    text = ofb(blocks, key, str.encode(iv))
    print(text)

ClientSocket.close()

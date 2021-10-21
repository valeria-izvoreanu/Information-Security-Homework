import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233
kPrim = 'WmZq3t6w9z$C&F)J'
iv = '0102030405060708'
key = ''


def ecb(blocks, key):
    #cripteaza primul bloc si salveaza-l in cipherContent
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    cipherContent = (encryptor.update(blocks[0]) + encryptor.finalize())
    #cripteaza fiecare bloc
    for i in range(1, len(blocks), 1):
        encryptor = cipher.encryptor()
        cipherBlock = encryptor.update(blocks[i]) + encryptor.finalize()
        cipherContent += cipherBlock
    return cipherContent

#xoreaza doi byte array
def myxor(var1, var2):
    return bytes(a ^ b for a, b in zip(var1, var2))


def ofb(blocks, key, iv):
    #cripteaza vectorul iv si il salveaza in flux pentru viitorul bloc
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    flux = encryptor.update(iv) + encryptor.finalize()
    #xoreaza primul bloc cu vectorul criptat
    cipherContent = myxor(blocks[0], flux)
    #repeta operatia pentru toate blocurile
    for i in range(1, len(blocks), 1):
        encryptor = cipher.encryptor()
        flux = encryptor.update(flux) + encryptor.finalize()
        cipherContent += myxor(blocks[i], flux)
    return cipherContent


print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)
#citeste modul de operare de la tastatura si-l trimite lui KM
Input = input('Alege modul de operare (ECB, OFB): ')
ClientSocket.send(str.encode(Input))
#citeste cheia si o decripteaza, folosind libraria pentru asta
Response = ClientSocket.recv(2048)
if Input == 'ECB':
    cipher = Cipher(algorithms.AES(bytes(kPrim, 'utf-8')), modes.ECB())
else:
    cipher = Cipher(algorithms.AES(bytes(kPrim, 'utf-8')), modes.OFB(bytes(iv, 'utf-8')))
decryptor = cipher.decryptor()
key = decryptor.update(Response)
print(key)
#citeste semnalul sa inceapa criptarea de la B
Response = ClientSocket.recv(2048)
print(Response)
textBlocks = []
#citeste continutul fisierului pe blocuri de 128 biti(16B)
with open('input.txt', 'rb') as infile:
    while True:
        block = infile.read(16)
        if not block:
            break
        textBlocks.append(block)

#daca ultimul bloc nu este de 16B, adauga padding
if len(textBlocks[-1]) < 16:
    tmp = ''
    for i in range(16 - len(textBlocks[-1])):
        tmp = tmp + ' '
    tmpBlock = textBlocks[-1].decode('utf-8')
    tmpBlock = tmpBlock + tmp
    textBlocks[-1] = str.encode(tmpBlock)

#cripteaza blocurile in dependenta de modul setat si trimite blocurile lui KM
if Input == 'ECB':
    cipherContent = ecb(textBlocks, key)
    print(cipherContent.decode('latin-1'))
    ClientSocket.sendall(cipherContent)
else:
    cipherContent = ofb(textBlocks, key, str.encode(iv))
    print(cipherContent.decode('latin-1'))
    ClientSocket.sendall(cipherContent)

ClientSocket.close()

import socket
import os
import threading
from _thread import *
from time import sleep

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
kPrim = 'WmZq3t6w9z$C&F)J'
iv = '0102030405060708'
k = ''
threadAId = 0
threadBId = 0
encryptedKey = ''
opMod = ''
lock = threading.Lock()
begin = False
content = ''

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection):
    #variabile globale ce vor apartine ambelor threaduri
    global threadAId
    global threadBId
    global k
    global encryptedKey
    global opMod
    global begin
    global content
    connection.send(str.encode('Welcome'))
    #salveaza id-urile fiecarui thread
    if threadAId == 0:
        threadAId = threading.get_ident()
    else:
        threadBId = threading.get_ident()
    localThread = threading.get_ident()

    #genereaza cheia K random
    k = os.urandom(16)


    if localThread == threadAId:
        #daca suntem in threadul A citeste modul de operare
        Response = connection.recv(2048)
        opMod = Response.decode('utf-8')
    else:
        #daca suntem in threadul B asteapta pana A trimide modul de operare
        #si trimite lui B modul de operare
        while opMod == '':
            sleep(1)
        connection.sendall(str.encode(opMod))
    #pune cheia intr-un lock astfel incat KM sa cripteze cheia doar odata
    lock.acquire()
    if encryptedKey == '':
        # pentru cheie vom folosi modul de encriptare din librarie
        if opMod == 'ECB':
            cipher = Cipher(algorithms.AES(bytes(kPrim, 'utf-8')), modes.ECB())
        else:
            cipher = Cipher(algorithms.AES(bytes(kPrim, 'utf-8')), modes.OFB(bytes(iv, 'utf-8')))
        encryptor = cipher.encryptor()
        encriptedKey = encryptor.update(k) + encryptor.finalize()
    lock.release()
    #trimite cheia ambilor noduri
    connection.sendall(encriptedKey)
    #daca suntem in threadul B citeste mesajul de incepere a comunicarii
    if localThread == threadBId:
        connection.recv(2048)
        begin = True
    else:
        #daca suntem in A asteapta semnalul de la B
        #si anunta-l pe A sa inceapa criptarea
        while not begin:
            sleep(1)
        connection.sendall(str.encode('Start'))
    #daca este in A citeste textul criptat
    if localThread == threadAId:
        content = connection.recv(2048)
        print(content)
    #daca este in B asteapta textul criptat si il trimite lui B
    else:
        while content == '':
            sleep(1)
        connection.sendall(content)
    connection.close()


while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client,))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

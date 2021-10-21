# Tema1-SI
1.	Tema a fost scrisa in limbaj Python cu libraria criptografica cryptography
2.	[Symmetric encryption — Cryptography 36.0.0.dev1 documentation](https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/?highlight=aes)
3.	Comunicarea este de tip Server-Client cu socket, unde Managerul de chei este serverul si nodurile A si B sunt clientii. 
4.	Cheile au fost generate cu libraria os. Cheia comuna KPrim si vectorul de initializare au fost date ca parametri globali fiecarui nod.

## Comunicare
Se trimit mesaje cu modul de operare(explicit ECB sau OFB) de la A la KM si de la KM la B dupa care se trimite si cheia criptata ambelor noduri, pana cand nodul B zice ca se poate de inceput comunicarea.Daca comunicarea se incepe, nodul A va cripta continutul textului, il va trimite lui MC si acesta ii va trimite nodului B, care-l va decripta si va afisa mesajul decriptat.

## ECB
ECB(criptare) a fost implementat in A astfel:
-	Am separat in blocuri de 16B continutul fisierul
-	Pentru ultimul bloc facem padding daca nu e complet
-	Pentru fiecare bloc facem criptarea cu cheia citita, decriptata dupa ce a fost primita de la KM
-	Si fiecare dintre aceste blocuri criptate le adaugam la ciphertext care este textul nostru din fisier criptat si este trimis lui KM

ECB(decriptare) a fost implementat in B astfel:
-	Am separat in blocuri de 16B ciphertextul
-	Decriptam fiecare bloc utilizand cheia citita si decriptata
-	Returnam la final plaintextul 

## OFB
OFB(criptare) a fost implementat in A astfel:
-	Separam in blocuri de 16B continutul fisierului
-	Criptam vectorul de initializare cu cheia primita si il salvam
-	Si updatam blocul pentru criptare ca fiind rezultatul anterior
-	Facem xor pe rezultatul criptarii si blocul nostru
-	Adaugam rezultatul xorului la ciphertext
- Repetam pentru fiecare bloc
- Returnam textul criptat

OFB(decriptare) a fost implementat in B astfel:
-	Separam in blocuri de 16B plaintextul
-	Criptam vectorul de initializare cu cheia primita si il salvam
-	Si updatam blocul pentru criptare ca fiind rezultatul anterior
-	Facem xor pe rezultatul criptarii si blocul criptat
-	Adaugam rezultatul xorului la plaintext
- Repetam pentru fiecare bloc
- Returnam textul obtinut

# Tema1-SI
1.	The theme was written in Python using the cryptographic library cryptography.
2.	[Symmetric encryption — Cryptography 36.0.0.dev1 documentation](https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/?highlight=aes)
3.	The communication is of the Server-Client type with sockets, where the Key Manager is the server and nodes A and B are the clients.
4.	The keys were generated with the os library. The common key KPrim and the initialization vector were given as global parameters to each node.
   
## Communication
Messages are sent with the mode of operation (explicitly ECB or OFB) from A to the KM and from the KM to B, after which the encrypted key is sent to both nodes until node B says that communication can begin. If the communication starts, node A will encrypt the content of the text, send it to KM, and KM will forward it to node B, which will decrypt it and display the decrypted message.

## ECB
ECB (encryption) was implemented in A as follows:
- The file content was separated into 16B blocks.
- Padding was added to the last block if it was not complete.
- Each block was encrypted with the key read and decrypted after being received from the KM.
- Each of these encrypted blocks was added to the ciphertext, which is our encrypted file content, and sent to KM.

ECB (decryption) was implemented in B as follows:
- The ciphertext was separated into 16B blocks.
- Each block was decrypted using the key read and decrypted.
- The plaintext was returned at the end.

## OFB
OFB (encryption) was implemented in A as follows:
- The file content was separated into 16B blocks.
- The initialization vector was encrypted with the received key and saved.
- The block for encryption was updated to the previous result.
- XOR was performed on the encryption result and our block.
- The XOR result was added to the ciphertext.
- This was repeated for each block.
- The encrypted text was returned.

OFB (decryption) was implemented in B as follows:
- The plaintext was separated into 16B blocks.
- The initialization vector was encrypted with the received key and saved.
- The block for encryption was updated to the previous result.
- XOR was performed on the encryption result and the encrypted block.
- The XOR result was added to the plaintext.
- This was repeated for each block.
- The obtained text was returned.

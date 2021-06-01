''' This module implements a UDP server with symmetric enryption and a Message 
Authentication Code. The Vigenere cipher is used for illustration purposes.'''

# Import modules.

import crypto
import hashlib
import numpy as np
import os
import socket as sock


class Server():
    ''' UDP server class for a symmetric key encrypted connection from a client.'''
    
    def __init__(self,
                 host,
                 port,
                 buff):

        # Setup the UDP parameters.
        self.host = host 
        self.port = port
        self.buff = buff
        self.addr = (self.host, self.port)

        # Create a decrypting object and also initialise the secret key.
        # This key will need to be given to the client.
        self.cipher = crypto.Vigenere()
        self.key = self.cipher.genKey(10)
        print("The secret key is: {}".format(self.key))


    def verifyMAC(self, msgAndMAC):
        ''' Function to verify the MAC on the received message. 
        INPUT: 
            msgAndMAC - The decrypted message.
        OUTPUT:
            msg - The message.
            MAC - The Message Authentication Code.'''

        # The message and MAC were concatenated and then encrypted together.
        # We have received the decrypted message so we can now split the 
        # two messages. 
        msgLen = len(msgAndMAC)
        msg = msgAndMAC[0:msgLen - self.cipher.MAC_LENGTH]
        mac = msgAndMAC[-self.cipher.MAC_LENGTH:]

        # Calculate the hash on the message.
        hsh = hashlib.md5(msg.encode()).hexdigest()
        #msgStr = str(msg, 'utf-8')
        #hshStr = str(hsh, 'utf-8')
        print("\nReceived msg: {}".format(msg))
        
        if mac == hsh:
            print("The MAC HASH has been verified.")
        else:
            print("WARNING: MAC VERIFICATION FAILED.")
            print("Received digest: {}".format(mac))
            print("Expected digest: {}".format(hsh))


    def run(self):
        ''' Run the UDP server. '''

        # Bind the socket.
        UDPSock = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
        UDPSock.bind(self.addr)

        # Accept connections and process messages until an exit message is received.
        print("Waiting for connection and message from client")
        while True:
            # Wait for any data to be returned.
            (data, addr) = UDPSock.recvfrom(self.buff)

            # Convert UDP data to string for Vigenere cipher.
            encryptedStr = str(data,'utf-8')
            #print("Encrypted Message from: {}".format(encryptedStr))

            # Now decrypt the message.
            msg = self.cipher.decrypt(encryptedStr, self.key)
            #print("Decrypted message: {}\n".format(msg))
            
            self.verifyMAC(msg)
            
            # Exit if exit message given.
            if msg == "exit":
                #UDPSock.sendto("EXITING".encode(), (self.host, self.port))
                break
            elif msg == "createNewkey":
                self.key = self.cipher.genKey(10)
                print(self.key)

        UDPSock.close()

        # Kill the thread/everything without any cleanup.
        os._exit(0)


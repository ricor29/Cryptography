''' UDP client module to send symmetric encryption messages.'''

# Import modules.
import crypto
import hashlib
import os
import socket as sock


class Client():
    ''' UDP client class that sends encrypted messages to a server. The 
    Vigenere cipher is used for illustration purposes.'''

    def __init__(self,
                 host,
                 port):

        # Initialise UDP client parameters.
        self.host = host #"127.0.0.1"
        self.port = port #13000
        self.addr = (self.host, self.port)
        
        # Get the user to enter the secret symmetric key.
        self.key = input("Enter the symmetric key or type 'exit': ")

        # Create the crypto object that will do the decrypt.
        self.cipher = crypto.Vigenere()


    def run(self):
        ''' Function to run the client.'''

        # Setup the socket.
        UDPSock = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)

        # Iterate and send data over the socket when new input is received.
        while True:

            # Receive message from the command line.
            msg = input("\nEnter message, or type 'enterNewKey, or type 'exit': ")

            # Exit if the phrase exit is given.
            if msg == 'exit':
                break
            elif msg == 'enterNewKey':
                self.key = input("Enter secret symmetric key server uses: ")

            # Create the HASH for the MAC.
            hsh = hashlib.md5(msg.encode()).hexdigest()
            print("Message hash is: {}".format(hsh))
            
            # Encrypt the message and hsh.
            encryptMsg = self.cipher.encrypt(msg+hsh, self.key)

            # Convert data to send.
            data = encryptMsg.encode()

            # Send data over socket.
            UDPSock.sendto(data, self.addr)

        # Close the socket.
        UDPSock.close()

        # Terminate everything.
        os._exit(0)

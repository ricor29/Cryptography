''' This module implements a naive crypto algorithm for test purposes with a MAC. '''


from abc import ABC, abstractmethod
import numpy as np
import string

class Cipher(ABC):
    ''' An abstract base class that forces and encrypt and decrypt interface.'''
    
    def __init__(self,):
        ''' Initialisation'''
        super().__init__()
        
    @abstractmethod
    def encrypt(self):
        pass

    @abstractmethod
    def decrypt(self):
        pass



class Vigenere(Cipher):
    ''' Vigenere cipher that uses a keyword to specify which of 26 rotations should be used.'''

    def __init__(self):
        ''' Initialise the class.'''

        # Possible letters in alphabet.
        self.alphabetPossible = {chr(i):i for i in range(128)}
        
        ''' {'A':0, 'B':1, 'C':2, 'D':3, 
                            'E':4, 'F':5, 'G':6,  'H':7,  'I':8,
                            'J':9,  'K':10,'L':11,  'M':12, 'N': 13,
                            'O':14,  'P':15, 'Q':16, 'R':17, 
                            'S':18, 'T':19, 'U':20, 'V':21, 'W':22,
                            'X':23,'Y':24, 'Z':25,
                            '1':26, 
                            '2':27,
                            '3':28,
                            '4':29,
                            '5':30,
                            '6':31,
                            '7':32,
                            '8':33,
                            '9':34,
                            '0':35,
                            ':':36,
                            ';':37,
                            '<':38,
                            '=':39,
                            '>':40,
                            '?':41,
                            '@':42 } '''


        # Calculate length of the alphabet.
        self.lenAlphabet = len(self.alphabetPossible)

        # Set the length of the Message Authentication Code.
        self.MAC_LENGTH = 32

    def keyShiftIdx(self, key):
        ''' Convert the key word to it's corresponding index in the alphabet.'''
        
        # First make sure key is in uppercase.
        key = key.upper()
        
        # Use the numerical index of the letters in the key (i.e. A=0, D=3), to create
        # a new keyArray. The new keyArray contains just the indexes and will be used 
        # in the Vigenere cypher as the amount of shift to rotate the alphabet by.
        keyArray = []
        for i in range(0, len(key)):
            keyElement = ord(key[i]) - ord('\x00') # subtract the start of ASCII alphabet used to base at 0.
            keyArray.append(keyElement)
            
        return keyArray
 
    
    def shift(self, character, n):
        ''' Encode the character by shifting it by n places in the alphabet.
        INPUT:
            character - The character to shift/rotate.
            n - The number of places to shift the character by.
        OUTPUT:
            The shifted character (converted to lower case letters).
        '''

        # Shift the capitalised character by n units. If the shift goes over 
        # the end of the alphabet apply the modulus operator to ensure it wraps.
        # NB the substraction of ord('0') is to make sure the modulus operator
        # is acting on a number between 0 and 26.
        shiftedInt = (ord(character) - ord('\x00') + n) % self.lenAlphabet

        # Due to subtracting ord('A') we need to add an offset back if we want 
        # the cipher text to be in the range of usual letters. We can either add
        # ord('A') to create capitalised letters or ord('0') for lower case. 
        # Adding ord('0') here.
        shiftedInt += ord('\x00')

        # Convert to a character.
        shiftedChar = chr(shiftedInt)

        return shiftedChar

    
    def encrypt(self, plainTxt, keyWord):
        ''' Encrypt a plain text with a supplied key.
        INPUTS: 
            plainText - a text string.
            key - a string (that must be all lower case).
        OUTPUTS:
            cipherText - the encrypted text string.
        '''

        # Convert the key to alphabet indices (Vignere specific).
        key = self.keyShiftIdx(keyWord)

        # Strip any unwanted characters i.e. not in the alphabet.
        plainTxtSafe = "".join([l for l in plainTxt if l in self.alphabetPossible])


        # Now create the cipher text. This is done by taking each character in the message and
        # shifting by the number specified in the key. 
        cipherTxt = "".join([self.shift(plainTxtSafe[i], key[i % len(key)]) for i in range(len(plainTxtSafe))])

        return cipherTxt


    def decrypt(self, cipherTxt, keyWord):
        ''' Decrypt a cipher text with a supplied key.
        INPUTS: 
            cipherTxt - a text string.
            key - a string (that must be all lower case).
        OUTPUTS:
            plainTxt - the decrypted text string.
        '''
        
        # Convert the key to alphabet indices (Vignere specific).
        key = self.keyShiftIdx(keyWord)

        # Same as encrypt but have a negative shift of the key to go backwards.
        plainTxt = "".join([self.shift(cipherTxt[i], -key[i % len(key)]) for i in range(len(cipherTxt))])

        return plainTxt


    def genKey(self, keyLength):
        ''' Generate a random character key for the VIGENERE cipher.'''
        
        # Get string of all upper and lower case letters to create key word with.
        letters = string.ascii_uppercase + string.ascii_lowercase
        
        # Now randomly select 10.
        listLetters = list(letters) #self.alphabetPossible.keys())
        key = np.random.choice(listLetters,10)
        
        return ''.join(str(i) for i in key)
        
        
    

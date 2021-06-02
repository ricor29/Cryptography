''' Helper functions and classes to illustrate Cryptographic maths.'''

import numpy as np
from random import randrange, getrandbits


def gcd(x,y):
    ''' Euclid's Greatest Common Divisor algorithm to find the 
        largest number that divides both x and y.
        
        INPUTS: 
            x - an integer.
            y - an integer.
    
        OUTPUTS:
            x - the greatest common divisor.
    '''

    # Iteratively go through switching the input order and also 
    # performing mod for second input.
    while y != 0:
        (x, y) = (y, x % y)
    return x


def eulPhi(n):
    ''' Calculate the number of coprimes in range 1 to n.'''
    
    # Initialise the counter.
    nFound = 0
    
    # Simple check every number if gcd is 1 and if yes then add to the counter.
    for k in range(1, n+1): # +1 as strictly speaking the formula is to include n.
        if gcd(n,k) == 1:
            nFound += 1
  
    return nFound


class FermatLittleTheorem():
    ''' Class to compute the modular inverse.'''
    
    def extendedGcd(self, a,b):
        ''' Extended Euclid's Greatest Common Divisor algorithm to find the 
            largest number that divides both a and b.

            INPUTS: 
                a - an integer.
                b - an integer.

            OUTPUTS:
                g - the greatest common divisor.
                * - the coefficients of Bézout's identity, which are integers x and y such that a x + b y = gcd(a, b).
        '''

        # Iteratively go through switching the input order and also 
        # performing mod for second input.
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.extendedGcd(b % a, a)
            return(g, x - (b//a)*y, y)


    def modInverse(self, a, m):
        ''' Modular inverse aa−1≡1(mod m)

            INPUTS: 
                a - the integer number a
                m - the modulo m

            OUTPUTS:
                modularInverse - None if doesn't exist or value if it does.
        '''        
        
        
        # Check if inverse exists and if it does return
        g, x, y = self.extendedGcd(a,m)
        
        if g != 1:
            print("GCD must equal 1 for an inverse to exist!")
            return None
        else:
            print("This assumes a and m are coprime (i.e. no common divisor except 1 exists).")
            return x % m
    
    
class SemiPrime():
    ''' Class to generate two primes that can form a semi-prime. '''


    def __init__(self):
        ''' Initialisation.'''
        pass


    def bruteForcePrimeCheck(self, x):
        ''' Function to check for primality.
        INPUT:
            x - positive integer number to check (will convert to positive if not).
            
        OUTPUT:
            Bool True=Prime else False.
        '''

        # Check is an int.
        if not isinstance(x, int):
            raise Exception("Not an integer") 

        # Convert to a positive number.
        x = abs(x)
        
        # A prime must have two factors so 1 does not count.
        if (x == 0) or (x == 1):
            return False
        elif x == 2:
            return True
            
        # Do a simple check to rule out half the potential numbers.
        elif x%2 == 0:
            return False
            
        # Start the brute force checking.
        else:

            
            # Skipping every other "even" number go through up to 
            # the square root of x (plus rounding factor).
            for n in range(3, int(np.sqrt(float(x)))+2, 2):
                # Is the modulo 0 - if so then prime
                if x % n == 0:
                    return False

            print("PRIME FOUND: {}".format(x))
            return True


    def nextCandidate(self, bitLength):
        ''' Create an integer (odd!) at random for a given number of bits.
        
        INPUT:
            bitLength: int that specifies the length of the number in bits.
            
        OUTPUT:
            randInt: int that has been generated.
        '''
        
        # First create the random bits of required length.
        randInt = getrandbits(bitLength)
        
        #print(format(randInt,'0'+str(bitLength)+'b'))
        
        # Now make sure that the most significant bit is 1 so that we don't 
        # drop bits. Also repeat for LSB.
        # Shift the first bit to the MSB and or with randInt.
        randInt |= 1 << bitLength - 1
        
        #print(format(randInt,'0'+str(bitLength)+'b'))
       
        # Now also or with the number 1 (which by definition is in LSB position).
        randInt |= 1  # Could be done in step above but to show intent clearer.
    
        #print(format(randInt,'0'+str(bitLength)+'b'))
    
        return randInt


    def createTwoPrimes(self, bitLength):
        ''' Create a prime number.
        
        INPUT:
            bitLength: int that specifies the length of the number in bits.
            
        OUTPUT:
            prime: A prime number.
        '''
        
        # First start with a candidate that is not 2 or a prime (to seed while
        # loop below).
        firstPrime = 6
        # Now find the first prime number.
        while not self.bruteForcePrimeCheck(firstPrime):
            firstPrime = self.nextCandidate(bitLength)

        print(firstPrime)

        # Now start with a candidate that is not 2 or a prime.
        secondPrime = 6
        # Now find the first prime number.
        while not self.bruteForcePrimeCheck(secondPrime):
            secondPrime = self.nextCandidate(bitLength)
            
        print(secondPrime)

        return firstPrime, secondPrime




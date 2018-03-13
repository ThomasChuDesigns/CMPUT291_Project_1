from uuid import uuid4
from hashlib import pbkdf2_hmac

def generateHashedPassword(password):
    # creates a binary value to store into database
    hash_name = 'sha256'
    salt = 'ssdirf993lksiqb4'
    iterations = 100000

    dk = pbkdf2_hmac(hash_name, bytearray(password, 'ascii'), bytearray(salt, 'ascii'), iterations)
    binary_value = bin(int.from_bytes(dk, 'big'))

    return binary_value

def generateID():
    # creates a uuid for new users
    return str(uuid4()).split('-')[0]
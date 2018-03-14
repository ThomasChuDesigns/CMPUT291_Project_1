from uuid import uuid4
from hashlib import pbkdf2_hmac
import binascii

def generateHashedPassword(password):
    # creates a binary value to store into database
    hash_name = 'sha256'
    salt = 'ssdirf993lksiqb4'
    iterations = 100000

    # create a byte object of hashed password, then convert to hexdecimal to binary
    dk = pbkdf2_hmac(hash_name, bytearray(password, 'ascii'), bytearray(salt, 'ascii'), iterations)

    return dk

def generateID():
    # creates a uuid for new users
    return str(uuid4()).split('-')[0]

def generateServiceID(controller):
    controller.cursor.execute("SELECT CAST(service_no AS INTEGER) AS no_id FROM service_agreements ORDER BY no_id DESC LIMIT 1")
    result = controller.cursor.fetchone()

    # no entries create one
    if not result:
        return 0
        
    return result[0] + 1

def createNewUser(controller, uid, role, login, password):
    password = generateHashedPassword(password)
    controller.cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?)", (uid, role, login, password,))
    controller.connection.commit()
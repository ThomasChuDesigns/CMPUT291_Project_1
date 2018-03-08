from hashlib import pbkdf2_hmac

user_types = {
    'Account Manager': AccountManager,
    'Supervisor': Supervisor,
    'Dispatcher': Dispatcher,
    'Driver': Driver,
}

def canLogin(connection, cursor, username, password):
    hash_name = 'sha256'
    salt = 'ssdirf993lksiqb4'
    iterations = 100000

    dk = pbkdf2_hmac(hash_name, bytearray(password, 'ascii'), bytearray(salt, 'ascii'), iterations)

    # fetch user with same username
    cursor.execute("SELECT role, password FROM users WHERE login = ?", username)
    candid = cursor.fetchone()

    # compare hashed password, if equal create new user
    if dk == candid[1]:
        return user_types[candid[0]](connection, cursor, username)

    return None

class Auth:
    def __init__(self, connection, cursor, username):
        self.username = username

    def options(self):
        pass
    


class AccountManager(Auth):
    role = 'Account Manager'
    def __init__(self, connection, cursor, username):
        pass

    def getMasterAccount(account_no):
        pass
    
    def addMasterAccount():
        pass

    def createServiceAgreement(account_no):
        pass
    
    def getSummaryReport(account_no)
    

class Supervisor(AccountManager):
    def __init__(self, connection, cursor, username):
        pass

    def getAccountManagerReport(personell_id):
        pass

class Dispatcher(Auth):
    role = 'Dispatcher'
    def __init__(self, connection, cursor, username):
        pass

    def createFulfillment():
        pass

class Driver(Auth):
    role = 'Driver'
    def __init__(self, connection, cursor, username):
        pass

    def getTasks():
        pass

    def getTask():
        pass

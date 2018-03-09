from hashlib import pbkdf2_hmac
from uuid import uuid4

# authenticates user and creates new user instance if credentials are correct
def canLogin(connection, cursor, username, password):
    user_types = {
        'Account Manager': AccountManager,
        'Supervisor': Supervisor,
        'Dispatcher': Dispatcher,
        'Driver': Driver,
    }

    hash_name = 'sha256'
    salt = 'ssdirf993lksiqb4'
    iterations = 100000

    dk = pbkdf2_hmac(hash_name, bytearray(password, 'ascii'), bytearray(salt, 'ascii'), iterations)

    # fetch user with same username
    cursor.execute("SELECT user_id, role, password FROM users WHERE login = ?", username)
    candid = cursor.fetchone()

    # compare hashed password, if equal create new user
    if dk == candid[2]:
        return user_types[candid[1]](connection, cursor, candid[0])

    return None

class User:
    def __init__(self, connection, cursor, userid):
        self.connection = connection
        self.cursor = cursor
        self.user_id = userid

    def options(self):
        pass

class Admin(User):
    def __init__(self, connection, cursor, userid):
        pass
    
    def addUser(self, username, password, id, role):
        pass
    
    def updateUser(self, username):
        pass

    def deleteUser(self, username):
        pass

class AccountManager(User):
    role = 'Account Manager'
    def __init__(self, connection, cursor, user_id):
        pass

    def getManagedAccounts(self):
        self.cursor.execute("SELECT account_no FROM accounts WHERE account_mgr = ?", self.user_id)
        return self.cursor.fetchall()

    def getMasterAccount(self,account_no):
        # get information of master account if account is under user's management
        if account_no in self.getManagedAccounts():
            self.cursor.execute("SELECT * FROM accounts WHERE account_no = ?", account_no)
            return self.cursor.fetchone()
        
        return None

    def addMasterAccount(self, customer_name, customer_info, customer_type, end_date, total_amount):
        new_id = 'AC-' + str(uuid4()).split('-')[0]
        self.cursor.execute("INSERT INTO accounts VALUES(?, ?, ?, strftime('now'), ?, ?)", (new_id, customer_name, customer_info, customer_type, end_date, total_amount))
        self.connection.commit()
        
    def createServiceAgreement(self, account_no):
        pass
    
    def getSummaryReport(self, account_no):
        pass
    

class Supervisor(AccountManager):
    def __init__(self, connection, cursor, user_id):
        pass

    def getAccountManagerReport(self, personell_id):
        pass

class Dispatcher(User):
    role = 'Dispatcher'
    def __init__(self, connection, cursor, user_id):
        pass

    def createFulfillment(self):
        pass

class Driver(User):
    role = 'Driver'
    def __init__(self, connection, cursor, user_id):
        pass

    def getTasks(self):
        pass

    def getTaskInfo(self):
        pass

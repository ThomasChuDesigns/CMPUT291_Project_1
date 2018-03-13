from hashlib import pbkdf2_hmac
from uuid import uuid4

# authenticates user and creates new user instance if credentials are correct
def canLogin(controller, username, password):
    user_types = {
        'account manager': AccountManager,
        'supervisor': Supervisor,
        'dispatcher': Dispatcher,
        'driver': Driver,
    }

    hash_name = 'sha256'
    salt = 'ssdirf993lksiqb4'
    iterations = 100000

    # hash the password and get the binary value of it
    dk = pbkdf2_hmac(hash_name, bytearray(password, 'ascii'), bytearray(salt, 'ascii'), iterations)
    binary_hash = bin(int.from_bytes(dk, 'big'))

    # fetch user with same username
    controller.cursor.execute("SELECT * FROM users WHERE login == ?", (username,))
    candid = controller.cursor.fetchone()

    # compare hashed password, if equal create new session for user
    if binary_hash == candid['password']:
        return user_types[candid['role']](controller, candid['user_id'])

    print('Login unsuccessful')
    return None

class User:
    def __init__(self, controller, userid):
        self.controller = controller
        self.user_id = userid

        print("Logged in as {}".format(userid))

    def options(self):
        pass

class Admin(User):
    def __init__(self, controller, userid):
        pass
    
    def addUser(self, username, password, id, role):
        pass
    
    def updateUser(self, username):
        pass

    def deleteUser(self, username):
        pass

class AccountManager(User):
    role = 'Account Manager'

    def getManagedAccounts(self):
        # queries all master accounts under account manager management
        self.controller.cursor.execute("SELECT account_no FROM accounts WHERE account_mgr = ?", (self.user_id,))
        return self.controller.cursor.fetchall()

    def getMasterAccount(self,account_no):
        # get information of master account if account is under user's management
        if account_no in self.getManagedAccounts():
            self.controller.cursor.execute("SELECT * FROM accounts WHERE account_no = ?", (account_no,))
            data = self.controller.cursor.fetchone()

        else:
            print("This account is not managed by you!")
        return None

    def addMasterAccount(self, customer_name, customer_info, customer_type, end_date, total_amount):
        new_id = str(uuid4()).split('-')[0]
        self.controller.cursor.execute("INSERT INTO accounts VALUES(?, ?, ?, strftime('now'), ?, ?)", (new_id, customer_name, customer_info, customer_type, end_date, total_amount))
        self.controller.connection.commit()
        
    def createServiceAgreement(self, account_no):
        pass
    
    def getSummaryReport(self, account_no):
        pass
    

class Supervisor(AccountManager):
    def __init__(self, controller, user_id):
        pass

    def getAccountManagerReport(self, personell_id):
        pass

class Dispatcher(User):
    role = 'Dispatcher'
    def __init__(self, controller, user_id):
        pass

    def createFulfillment(self):
        pass

class Driver(User):
    role = 'Driver'
    def __init__(self, controller, user_id):
        pass

    def getTasks(self):
        pass

    def getTaskInfo(self):
        pass

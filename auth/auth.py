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

    def getAccountManagerReport(self, personell_id):
        pass

class Dispatcher(User):
    role = 'Dispatcher'

    def createFulfillment(self):
        print('List of Service Agreements:')
        self.printAllServices()
        service_no = input('Please enter which service agreement you would like to create a fufillment for: ')
        print('List of drivers:')
        self.printAllDrivers()
        driver = input('Please enter which driver you would like to fulfill the service: ')
        if(self.getDriverTruck(driver)):
            truck_id = self.getDriverTruck(driver)
        else:
            print('List of trucks:')
            self.printAllTrucks()
            truck_id = input('Enter the id of the truck you would like the driver to use: ')
        #todo
    
    def printAllServices(self):
        self.controller.cursor.execute("SELECT service_no FROM service_agreements")
        rows = self.controller.cursor.fetchall()
        print(rows)

    def printAllDrivers(self):
        self.controller.cursor.execute("SELECT p.name, d.owned_truck_id FROM personnel p, drivers d WHERE d.pid = p.pid")
        rows = self.controller.cursor.fetchall()
        print(rows)
        
    def getDriverTruck(self, driver):
        self.controller.cursor.execute("SELECT d.owned_truck_id FROM drivers d, personnel p WHERE p.name = driver AND d.pid = p.pid")
        row = self.controller.cursor.fetchone()
        return row[0]
    
    def printAllTrucks(self):
        self.controller.cursor.execute("SELECT truck_id FROM trucks WHERE NOT EXISTS(SELECT truck_id FROM trucks, drivers d WHERE truck_id = d.owned_truck_id)") 
        rows = self.controller.cursor.fetchall()
        print(rows)
    
class Driver(User):
    role = 'Driver'

    def getTasks(self, starting_date, ending_date, driver_id):
        self.controller.cursor.execute("SELECT sf.date_time, sa.location, sa.local_contact, sa.waste_type, sf.cid_drop_off, sf.cid_pick_up FROM service agreements sa, service_fulfillments sf WHERE sf.driver_id=:driver_id  sa.service_no = sf.service_no AND sf.date_time >:starting_date AND sf.date_time<:ending_date",{"driver_id":driver_id, "starting_date":starting_date, "ending_date":ending_date})
        rows = self.controller.cursor.fetchall()
        return rows
        

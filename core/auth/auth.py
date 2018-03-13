from hashlib import pbkdf2_hmac
from uuid import uuid4

from .util import generateHashedPassword, generateID, generateServiceID
from core.database.models import getColumnNames

# authenticates user and creates new user instance if credentials are correct
def canLogin(controller, username, password):
    user_types = {
        'account manager': AccountManager,
        'supervisor': Supervisor,
        'dispatcher': Dispatcher,
        'driver': Driver,
    }

    # hash the password then compare with entry in database
    binary_hash = generateHashedPassword(password)

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

    # setup command-line interface here
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
    role = 'account manager'

    def __init__(self, controller, userid):
        User.__init__(self, controller, userid)

    def isManaging(self, account_no):
        self.controller.cursor.execute("SELECT account_no FROM accounts WHERE account_no = ? AND account_mgr = ?", (account_no, self.user_id, ))
        return self.controller.cursor.fetchone()

    def getManagedAccounts(self):
        # queries all master accounts under account manager management
        self.controller.cursor.execute("SELECT account_no FROM accounts WHERE account_mgr = ?", (self.user_id,))
        return list(map(lambda x: x['account_no'], self.controller.cursor.fetchall()))

    def getServiceAgreements(self, account_no):
        # get information of master account if account is under user's management
        if not self.isManaging(account_no):
            return None
        
        # get query of all service agreements under a managed account
        self.controller.cursor.execute("SELECT * FROM service_agreements WHERE master_account = ? ORDER BY CAST(service_no AS INTEGER) DESC", (account_no,))
        data = self.controller.cursor.fetchall()

        # print column names
        for col_name in getColumnNames(self.controller.cursor):
            print('{:<24}'.format(col_name), end=' ')
        print('\n')

        # print entries
        for entries in data:
            for attr in entries.keys():
                print('{:<24}'.format(entries[attr]), end=' ')
            print()


    def addMasterAccount(self, customer_name, contact, customer_type, start, end):
        new_id = generateID()
        self.controller.cursor.execute("INSERT INTO accounts VALUES(?, ?, ?, ?, ?, ?, ?, 0)", (new_id, self.user_id, customer_name, contact, customer_type, start, end,))

        self.controller.connection.commit()
        return new_id
        
    def createServiceAgreement(self, account_no, location, waste_type, schedule, contact, cost, price):
        if not self.isManaging(account_no):
            return None

        # insert new entry into service agreements table
        self.controller.cursor.execute("""
        INSERT INTO service_agreements VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        """, (generateServiceID(self.controller), account_no, location, waste_type, schedule, contact, cost, price,))

        # update total_amount of the master account
        self.controller.cursor.execute("""
        UPDATE accounts SET total_amount = total_amount + ?
        WHERE account_no = ? 
        """, (price, account_no,))
        
        self.controller.connection.commit()
        

    
    def getSummaryReport(self, account_no):
        # returns a dict object with keys: agreements, total_price, total_expenses, waste_types for a single master account
        if not self.isManaging(account_no):
            return None

        self.controller.cursor.execute("""
        SELECT COUNT(*) AS count, SUM(price) AS total_price, SUM(internal_cost) AS total_cost, COUNT(DISTINCT waste_type) AS types 
        FROM service_agreements WHERE master_account = ?
        """, (account_no, ))

        result = self.controller.cursor.fetchone()

        for col_name in getColumnNames(self.controller.cursor):
            print('{:<24}'.format(col_name), end=' ')
        print('\n')

        print('{:<24} {:<24} {:<24} {:<24}'.format(result['count'], result['total_price'], result['total_cost'], result['types']))
    

class Supervisor(AccountManager):
    def __init__(self, controller, userid):
        AccountManager.__init__(self, controller, userid)

    def getManagedAccounts(self):
        pass

    def getAccountManagerReport(self, personnel_id):
        pass

class Dispatcher(User):
    role = 'dispatcher'

    def __init__(self, controller, userid):
        User.__init__(self, controller, userid)

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
    role = 'driver'

    def __init__(self, controller, userid):
        User.__init__(self, controller, userid)

    def getTasks(self, starting_date, ending_date, driver_id):
        self.controller.cursor.execute("SELECT sf.date_time, sa.location, sa.local_contact, sa.waste_type, sf.cid_drop_off, sf.cid_pick_up FROM service agreements sa, service_fulfillments sf WHERE sf.driver_id=:driver_id  sa.service_no = sf.service_no AND sf.date_time >:starting_date AND sf.date_time<:ending_date",{"driver_id":driver_id, "starting_date":starting_date, "ending_date":ending_date})
        rows = self.controller.cursor.fetchall()
        return rows
        

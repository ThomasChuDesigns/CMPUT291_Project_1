from hashlib import pbkdf2_hmac
from uuid import uuid4

from .util import generateHashedPassword, generateID, generateServiceID
from core.database.util import getColumnNames

# authenticates user and creates new user instance if credentials are correct
def canLogin(controller, username, password):
    user_types = {
        'admin': Admin,
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

    print('Login Unsuccessful')
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
    role = 'admin'

    def __init__(self, controller, userid):
        User.__init__(self, controller, userid)

    def getUsername(self, username):
        self.controller.cursor.execute("SELECT login FROM users WHERE login = ?", (username,))
        return self.controller.cursor.fetchone()
    
    def getID(self, pid, role = ''):
        if role == 'account manager':
            self.controller.cursor.execute("SELECT pid FROM account_managers WHERE pid = ?", (pid,))
        elif role == 'driver':
            self.controller.cursor.execute("SELECT pid FROM drivers WHERE pid = ?", (pid,))
        else:
            self.controller.cursor.execute("SELECT pid FROM personnel WHERE pid = ?", (pid,))

        return self.controller.cursor.fetchone()

    def addUser(self, username, password, pid, role):
        # username exists in users table or pid not found in personnel
        if self.getUsername(username) or not self.getID(pid, role):
            print('ERROR: username exists already or ID does not exists in personnel list')
            return False

        
        # add new user to users table
        self.controller.cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?)", (pid, role, username, generateHashedPassword(password),))
        self.controller.connection.commit()

        return True


    def deleteUser(self, username):
        # username not found in users table
        if not self.getUsername(username):
            return False

        # delete if username exists in users table
        self.controller.cursor.execute("DELETE FROM users WHERE login = ?", (username,))
        self.controller.connection.commit()
        return True

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
        
        return data


    def addMasterAccount(self, customer_name, contact, customer_type, start, end):
        new_id = generateID()

        # insert new entry to accounts using params given
        self.controller.cursor.execute("INSERT INTO accounts VALUES(?, ?, ?, ?, ?, ?, ?, 0)", 
        (new_id, self.user_id, customer_name, contact, customer_type, start, end,))

        # commit changes to database
        self.controller.connection.commit()
        return new_id
        
    def createServiceAgreement(self, account_no, location, waste_type, schedule, contact, cost, price):
        if not self.isManaging(account_no):
            return None

        # generate a service_no using previous entries
        service_no = generateServiceID(self.controller)

        # insert new entry into service agreements table
        self.controller.cursor.execute("""
        INSERT INTO service_agreements VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        """, (service_no, account_no, location, waste_type, schedule, contact, cost, price,))

        # update total_amount of the master account
        self.controller.cursor.execute("""
        UPDATE accounts SET total_amount = total_amount + ?
        WHERE account_no = ? 
        """, (price, account_no,))
        
        self.controller.connection.commit()

        return service_no
        

    
    def getSummaryReport(self, account_no):
        # returns a dict object with keys: agreements, total_price, total_expenses, waste_types for a single master account
        if not self.isManaging(account_no):
            return None

        # querys total services, total price, total costs, types of waste for a given account
        self.controller.cursor.execute("""
        SELECT COUNT(*) AS count, SUM(price) AS total_price, SUM(internal_cost) AS total_cost, COUNT(DISTINCT waste_type) AS types 
        FROM service_agreements WHERE master_account = ?
        """, (account_no, ))

        return self.controller.cursor.fetchone()
    

class Supervisor(User):
    def __init__(self, controller, userid):
        User.__init__(self, controller, userid)

    def isSupervising(self, mgr_id):
        return mgr_id in self.getSupervisedManagers()
    
    def getSupervisedAccounts(self):
        # queries all account id's under account managers supervised by this user
        # returns a list of the account id's

        self.controller.cursor.execute("SELECT account_no FROM accounts WHERE account_mgr IN (SELECT pid FROM personnel WHERE supervisor_pid = ?)", (self.user_id,))
        return list(map(lambda x: x['account_no'], self.controller.cursor.fetchall()))

    def getSupervisedManagers(self):
        # queries all pid under supervision of session user id
        self.controller.cursor.execute("SELECT pid FROM personnel WHERE supervisor_pid = ?", (self.user_id,))
        return list(map(lambda x: x['pid'], self.controller.cursor.fetchall())) 

    def addMasterAccount(self, mgr_id, customer_name, contact, customer_type, start, end):
        # inserts a new master account into accounts table under a supervised manager
        # returns the new master account's id

        if not self.isSupervising(mgr_id):
            print("You are not supervising this manager!")
            return None

        new_id = generateID()

        # insert new entry to accounts using params given
        self.controller.cursor.execute("INSERT INTO accounts VALUES(?, ?, ?, ?, ?, ?, ?, 0)", 
        (new_id, self.user_id, customer_name, contact, customer_type, start, end,))

        # commit changes to database
        self.controller.connection.commit()
        return new_id


    def getSummaryReport(self, account_no):
        # if successful, returns a dictionary of reported values (# of services, total price, total cost, waste types)
        if not account_no in self.getSupervisedAccounts():
            print("You do not have permission to access account: {}".format(account_no))
            return None
        
        # querys total services, total price, total costs, types of waste for a given account
        self.controller.cursor.execute("""
        SELECT COUNT(*) AS count, SUM(price) AS total_price, SUM(internal_cost) AS total_cost, COUNT(DISTINCT waste_type) AS types 
        FROM service_agreements WHERE master_account = ?
        """, (account_no,))

        return self.controller.cursor.fetchone()


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
        

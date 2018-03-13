from hashlib import pbkdf2_hmac
from uuid import uuid4

from .util import generateHashedPassword, generateID, generateServiceID
from core.database.util import getColumnNames, displayQuery, displayRow

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

    return None

def loginPrompt(controller):
    attempts = 0
    while(attempts < 3):
        username = input('Enter Username: ')
        password = input('Enter Password: ')
        session = canLogin(controller, username, password)

        if session: return session  # successfully logged in
        
        attempts += 1
        print('Login Unsuccessful ({}) attempts left'.format(3 - attempts))


class User:

    def __init__(self, controller, userid):
        self.choice = None
        self.controller = controller
        self.user_id = userid

        print("Logged in as {}".format(userid))

    # setup command-line interface here
    def options(self):
        pass

    def show(self):

        # WRITE YOUR TASKS IN OPTIONS FUNCTION
        self.options()

        # logout is universal so leave it here
        if self.choice == 'exit':
            print('logging out...')
            return False

        return True

class Admin(User):
    role = 'admin'

    def __init__(self, controller, userid):
        User.__init__(self, controller, userid)

    def showUsers(self):
        self.controller.cursor.execute("SELECT user_id, role, login FROM users")
        return self.controller.cursor.fetchall()

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
        print('User {} added!'.format(username))

        return True


    def deleteUser(self, username):
        # username not found in users table
        if not self.getUsername(username):
            return False

        # delete if username exists in users table
        self.controller.cursor.execute("DELETE FROM users WHERE login = ?", (username,))
        self.controller.connection.commit()
        print('User {} deleted!'.format(username))
        return True
    
    def options(self):
        print('-'*36)
        displayQuery(self.controller, self.showUsers())
        print("There are 2 options, enter the number corresponding to it:")
        print("Add login credentials for a personnel (1)")
        print("Delete login credentials for a personnel (2)")
        print("Enter 'exit' to logout")
        print('-'*36)
        self.choice = input("Please enter an option: ")
        if self.choice == '1':
            username = input('Enter a username for user: ')
            password = input('Enter a password for user: ')
            pid = input('Enter the users pid: ')
            role = input('Enter the users role: ')
            self.addUser(username, password, pid, role)
        elif self.choice == '2':
            username = input('Enter a username for user: ')
            self.deleteUser(username)


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
        
        return data

    def getMasterAccount(self, account_no):
        self.controller.cursor.execute("SELECT * FROM accounts WHERE account_no = ?", (account_no,))
        return self.controller.cursor.fetchone()

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
            print("You do not have permission to access account: {}".format(account_no))
            return None

        # querys total services, total price, total costs, types of waste for a given account
        self.controller.cursor.execute("""
        SELECT COUNT(*) AS count, SUM(price) AS total_price, SUM(internal_cost) AS total_cost, COUNT(DISTINCT waste_type) AS types 
        FROM service_agreements WHERE master_account = ?
        """, (account_no, ))

        return self.controller.cursor.fetchone()

    def options(self):
        print('-'*36)
        print("You have 4 options, enter the number corresponding to it:")
        print("Get master account information (1)")
        print("Create new master account (2)")
        print("Create new service agreement (3)")
        print("Create summary report for customer (4)")
        print("Enter 'exit' to logout")
        print('-'*36)

        self.choice = input("Please enter an option: ")
        if self.choice == '1':
            account_no = input('Enter a account_no: ')
            # display info first, then their service agreements
            displayRow(self.controller, self.getMasterAccount(account_no))
            print()
            displayQuery(self.controller, self.getServiceAgreements(account_no))
        elif self.choice == '2':
            name = input('Enter customer name: ')
            contact = input('Enter customer contact info: ')
            customer_type = input('Enter customer type: ')
            start = input('Enter start date (YYYY-MM-DD): ')
            end = input('Enter end date (YYYY-MM-DD): ')
            self.addMasterAccount(name, contact, customer_type, start, end)
            print('New master account made for {}!'.format(name))
        elif self.choice == '3':
            account_no = input('Enter account number: ')
            location = input('Enter service location: ')
            waste_type = input('Enter waste type: ')
            schedule = input('Enter schedule memo: ')
            contact = input('Enter contact info: ')
            cost = input('Enter internal costs: ')
            price = input('Enter price: ')
            self.createServiceAgreement(account_no, location, waste_type, schedule, contact, cost, price)
        elif self.choice == '4':
            account_no = input('Enter account number: ')
            displayRow(self.controller, self.getSummaryReport(account_no))
    

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

    
    def getManagerSummaryReport(self):
        self.controller.cursor.execute("""
        SELECT account_mgr, COUNT(DISTINCT(account_no)) AS total_master, COUNT(*) AS total_service, 
        SUM(price) AS total_price, SUM(internal_cost) AS total_cost, SUM(price) - SUM(internal_cost) AS profit
        FROM service_agreements JOIN accounts ON master_account = account_no
        WHERE account_mgr IN (SELECT pid FROM personnel WHERE supervisor_pid = ?)
        GROUP BY account_mgr ORDER BY profit DESC
        """, (self.user_id,))

        return self.controller.cursor.fetchall()

    def options(self):
        print('-'*36)
        print("You have 4 options, enter the number corresponding to it:")
        print("Add a master account under a manager (1)")
        print("Create summary report of customer (2)")
        print("Create summary report of manager (3)")
        print("Enter 'exit' to logout")
        print('-'*36)

        self.choice = input("Please enter an option: ")
        if self.choice == '1':
            mgr_id = input('Enter supervising manager id: ')
            name = input('Enter customer name: ')
            contact = input('Enter customer contact info: ')
            customer_type = input('Enter customer type: ')
            start = input('Enter start date (YYYY-MM-DD): ')
            end = input('Enter end date (YYYY-MM-DD): ')
            self.addMasterAccount(mgr_id, name, contact, customer_type, start, end)
        elif self.choice == '2':
            account_no = input('Enter account number: ')
            displayRow(self.controller, self.getSummaryReport(account_no))
        elif self.choice == '3':
            displayQuery(self.controller, self.getManagerSummaryReport())


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
        

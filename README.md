# CMPUT 291 Project 1
This is a system to handle a waste management companies database. Employees are able to maintain their records on this program and also get information about their shifts or records of customer accounts.

###### * For Developers
If your wish to extend the functionality, please read the documentation as it will help break down the process behind the program. We divided the functionalities into modules which organizes and allows for easier scalability if there is intention to create extensions to this program.

#### Installation

Requirements: Python3.6, pip3

##### 1. Create a virtual environment (Optional)

Goto the directory you want to store your virtualenv
```
virtualenv ENV_NAME

cd ENV_NAME
```

##### 2. Activate your environment

###### For OSX

```
source bin/activate
```

###### For Windows

```
.\Scripts\activate
```

##### 3. Clone repository to virtual environment and import dependencies
```
git clone https://github.com/ThomasChuDesigns/CMPUT291_Project_1.git
cd CMPUT291_Project_1
pip3 install -r requirements.txt
```

##### 4. Run Program
In your terminal, change to this repository folder and run this command:
```
python3 main.py
```

## Documentation:
### core.auth 
#### core.auth.auth
* **FUNCTION canLogin(controller, username, password)**: checks if password matches with databases password respective to username. If authentication is successful, return a User class according to the role of the user.
	* **account manager role**: returns AccountManager class
	*  **supervisor role**: returns Supervisor class
	*  **dispatcher role**: returns Dispatcher class
	*  **driver role**: returns Driver class
	*  **admin role**: returns Admin class

	returns None if role in database does not match any of these roles.
* **CLASS User**: a class which supplies the basic functionality for the program. Roles will use this class as a foundation for their functionalities.
	* **controller**: A class which connects us to the database. Use this to query and change database
	* **user_id**: the id of the user logged in, used for querying results
	* **options()**: empty function, add functions for your role here
* **CLASS Admin(User)**: Admin instance created if role is 'admin'
	* **addUser(id, role, username, password)**: creates a user with permissions based on their role. There must be an existing id in according role's table that matches the parameter id  when calling this function
	* **deleteUser(username)**: deletes all entry of the user according to their username. Their record in their role's table will also be deleted

* **CLASS AccountManager(User)**: AccountManager instance created if role is 'account manager'
	* **isManaging(account_no)**: checks if account is being managed by this user
	* **getManagedAccounts()**: returns a list of all accounts under user's management
	* **getServiceAgreements(account_no)**: returns a list of service_agreement  under account_no
	* **addMasterAccount(customer_name, contact, customer_type, start, end)**: adds a new master account
	* **createServiceAgreement(account_no, location, waste_type, schedule, contact, cost, price)**: adds a new service agreement under account_no
	* **getSummaryReport(account_no)**: gets a report of an account, number of services, total price, total internal costs, types of waste

* **CLASS Supervisor(User)**: Supervisor instance created if role is 'supervisor'
	* **isSupervising(mgr_id)**: checks if user is supervising this account manager
	* **getSupervisedAccounts()**: returns all **accounts** under account managers that are supervised by user
	* **getSupervisedManagers()**: returns all **account managers** under user's supervision
	* **addMasterAccount(mgr_id, customer_name, contact, customer_type, start, end)**: creates new master account under a account manager under user's supervision
	* **getSummaryReport(account_no)**: returns a report like account managers but can be any account managed by manager under user's supervision

* **CLASS Dispatcher(User)**: Dispatcher instance created if role is 'dispatcher'
	* **createFulfillment()**: creates a service fulfillment entry with input given
	* **printAllServices()**: prints services 
	* **printAllDrivers()**: returns all **account managers** under user's supervision
	* **getDriverTruck(driver)**: creates new master account under a account manager under user's supervision
	* **printAllTrucks()**: returns a report like account managers but can be any account managed by manager under user's supervision

* **CLASS Driver(User)**: Driver instance created if role is 'driver'
	* **getTasks(starting_date, ending_date, driver_id)**: checks if user is supervising this account manager

#### core.auth.util
* **generateHashPassword(password)**: hashes password and returns a binary value of the hashed password
* **generateID()**: creates a unique ID using uuid4 function from uuid module
* **generateServiceID()**: creates the highest ID + 1 from service agreements table

### core.database
#### core.database.controller
* **CLASS Controller(directory, database_file)**: a class that handles all connections to the database. (ie. making queries)
	* **database**: path of the database file
	* **cursor**: object in sqlite3 library to execute sql commands using strings.
	* **connection**: connecting to our database to commit changes
#### core.database.util
* **readSQL(controller, sql_file)**: read sql file and executes it onto the database
* **getColumnNames(cursor)**: returns a list of the column names from latest query
* 
#### Test cases
Our repository has included test cases for all the roles. We run all our test cases before we commit changes to make sure everything works fine.

```
# ALWAYS USE test_data.sql and test.db FOR TESTING

/example.py			# boilerplate for testcases
/testcases.py		# test case for for all roles
```
import sqlite3, os

from core.database.controller import Controller
from core.database.util import readSQL

from core.auth.auth import canLogin

# An example testcase, logging in to an account from example_data.sql and ran on test.db 
#
#
#
#

def admin():
    # create a controller to test.db
    db_directory = os.path.dirname(__file__) + '/data'
    test_db = Controller(db_directory, 'test.db')

    # insert schema and data into test db
    readSQL(test_db, os.path.join(db_directory, 'p1-tables.sql'))
    readSQL(test_db, os.path.join(db_directory, 'test_data.sql'))

    # try logging in
    session = canLogin(test_db, 'owner', 'admin')
    assert session

    assert session.role == 'admin'
    assert session.addUser('user1', 'pass1', '12', 'supervisor')
    assert not session.addUser('user1', 'pass1', '13', 'driver')
    assert not session.addUser('user1', 'pass1', '14', 'account manager')

    assert session.deleteUser('user1')

    print("Test case for admin passed!")

def accm():
    # create a controller to test.db
    db_directory = os.path.dirname(__file__) + '/data'
    test_db = Controller(db_directory, 'test.db')

    # insert schema and data into test db
    readSQL(test_db, os.path.join(db_directory, 'p1-tables.sql'))
    readSQL(test_db, os.path.join(db_directory, 'test_data.sql'))

    # try logging in
    session = canLogin(test_db, 'd4nny', 'password')

    assert session
    assert session.addMasterAccount('thomas', '(780) 111-1111', 'industrial', '2018-02-25', '2018-03-25')

    assert not session.createServiceAgreement('1', 'McDonalds', 'mixed waste', 'everyday', '(780) 111-1111', 250, 350)
    assert not session.createServiceAgreement('1', 'Burger King', 'paper', 'everyday', '(780) 111-1111', 250, 237)
    assert session.createServiceAgreement('0', 'Wendys', 'metal', 'everyday', '(780) 111-1111', 30, 50) == 0
    assert session.createServiceAgreement('0', 'Home', 'mixed waste', 'everyday', '(780) 111-1111', 30, 50) == 1

    assert not session.getServiceAgreements('1')
    assert session.getServiceAgreements('0')

    summary = session.getSummaryReport('0')
    
    assert summary['count'] == 2
    assert summary['total_price'] == 100
    assert summary['total_cost'] == 60
    assert summary['types'] == 2

    print("All test cases passed for account managers!")


def supervisor():
    # create a controller to test.db
    db_directory = os.path.dirname(__file__) + '/data'
    test_db = Controller(db_directory, 'test.db')

    # insert schema and data into test db
    readSQL(test_db, os.path.join(db_directory, 'p1-tables.sql'))
    readSQL(test_db, os.path.join(db_directory, 'test_data.sql'))

    # try logging in
    session = canLogin(test_db, 'thomas', 'notpassword')

    assert session.getSupervisedAccounts() == ['0']
    assert session.getSupervisedManagers() == ['111111']

    assert session.isSupervising('6969') == False
    assert session.addMasterAccount('6969', 'fail', '(780) 111-1111', 'industrial', '2018-02-25', '2018-03-25') == None
    assert session.addMasterAccount('111111', 'pass', '(780) 111-1111', 'industrial', '2018-02-25', '2018-03-25')

    assert session.getSummaryReport('0')
    assert session.getSummaryReport('1') == None

    print('All test cases passed for supervisors!')


def main():
    admin()
    accm()
    supervisor()

if __name__ == "__main__":
    main()
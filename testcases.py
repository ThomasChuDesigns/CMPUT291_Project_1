import sqlite3, os

from core.database.controller import Controller
from core.database.util import readSQL, displayQuery, displayRow

from core.auth.auth import canLogin

db_directory = os.path.join(os.path.dirname(__file__), 'data/')
# test cases to make sure program works xd

def admin(db):
    # insert schema and data into test db
    readSQL(db, os.path.join(db_directory, 'p1-tables.sql'))
    readSQL(db, os.path.join(db_directory, 'test_data.sql'))

    # try logging in
    session = canLogin(db, 'owner', 'admin')
    assert session

    assert session.role == 'admin'
    assert session.addUser('user1', 'pass1', '12', 'supervisor')
    assert not session.addUser('user1', 'pass1', '13', 'driver')
    assert not session.addUser('user1', 'pass1', '14', 'account manager')

    assert session.deleteUser('user1')

    print("Test case for admin passed!")

def accm(db):
    # insert schema and data into test db
    readSQL(db, os.path.join(db_directory, 'p1-tables.sql'))
    readSQL(db, os.path.join(db_directory, 'test_data.sql'))

    # try logging in
    session = canLogin(db, 'd4nny', 'password')

    assert session
    assert session.addMasterAccount('thomas', '(780) 111-1111', 'industrial', '2018-02-25', '2018-03-25')

    assert not session.createServiceAgreement('1', 'McDonalds', 'mixed waste', 'everyday', '(780) 111-1111', 250, 350)
    assert not session.createServiceAgreement('1', 'Burger King', 'paper', 'everyday', '(780) 111-1111', 250, 237)
    assert session.createServiceAgreement('0', 'Wendys', 'metal', 'everyday', '(780) 111-1111', 30, 50)
    assert session.createServiceAgreement('0', 'Home', 'mixed waste', 'everyday', '(780) 111-1111', 30, 50)

    assert not session.getServiceAgreements('1')
    assert session.getServiceAgreements('0')

    summary = session.getSummaryReport('0')
    
    assert summary
    print(tuple(summary))

    print("All test cases passed for account managers!")


def supervisor(db):

    # insert schema and data into test db
    readSQL(db, os.path.join(db_directory, 'p1-tables.sql'))
    readSQL(db, os.path.join(db_directory, 'test_data.sql'))

    # try logging in
    session = canLogin(db, 'thomas', 'notpassword')

    assert session.getSupervisedAccounts()
    assert session.getSupervisedManagers()

    assert session.isSupervising('6969') == False
    assert session.addMasterAccount('6969', 'fail', '(780) 111-1111', 'industrial', '2018-02-25', '2018-03-25') == None
    assert session.addMasterAccount('111111', 'pass', '(780) 111-1111', 'industrial', '2018-02-25', '2018-03-25')

    assert session.getSummaryReport('0')
    assert session.getSummaryReport('1')

    assert session.getManagerSummaryReport()

    print('All test cases passed for supervisors!')

def dispatcher(db):

    # insert schema and data into test db
    readSQL(db, os.path.join(db_directory, 'p1-tables.sql'))
    readSQL(db, os.path.join(db_directory, 'test_data.sql'))

    session = canLogin(db, 'lol', 'dispatcher')
    assert session.getPublicTrucks()
    assert session.getTruckDriver('100')
    assert session.getAvailableAgreements()

    print('All test cases passed for dispatcher!')

def main():
    # create a controller to test.db
    
    test_db = Controller(db_directory, 'test.db')

    # run role testcases here
    admin(test_db)
    accm(test_db)
    supervisor(test_db)
    dispatcher(test_db)


if __name__ == "__main__":
    main()
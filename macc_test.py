import sqlite3, os

from core.database.controller import Controller
from core.database.models import readSQL

import core.auth.auth as auth

# Testing master account functions

def main():
    # create a controller to test.db
    db_directory = os.path.dirname(__file__) + '/data'
    test_db = Controller(db_directory, 'test.db')

    # insert schema and data into test db
    readSQL(test_db, os.path.join(db_directory, 'p1-tables.sql'))
    readSQL(test_db, os.path.join(db_directory, 'test_data.sql'))

    # try logging in
    session = auth.canLogin(test_db, 'd4nny', 'password')

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

if __name__ == "__main__":
    main()
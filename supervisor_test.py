import sqlite3, os

from core.database.controller import Controller
from core.database.models import readSQL

import core.auth.auth as auth

# Testing supervisor functions

def main():
    # create a controller to test.db
    db_directory = os.path.dirname(__file__) + '/data'
    test_db = Controller(db_directory, 'test.db')

    # insert schema and data into test db
    readSQL(test_db, os.path.join(db_directory, 'p1-tables.sql'))
    readSQL(test_db, os.path.join(db_directory, 'test_data.sql'))

    # try logging in
    session = auth.canLogin(test_db, 'thomas', 'notpassword')

    assert session.getSupervisedAccounts() == ['0']
    assert session.getSupervisedManagers() == ['111111']

    assert session.isSupervising('6969') == False
    assert session.addMasterAccount('6969', 'fail', '(780) 111-1111', 'industrial', '2018-02-25', '2018-03-25') == None
    assert session.addMasterAccount('111111', 'pass', '(780) 111-1111', 'industrial', '2018-02-25', '2018-03-25')

    assert session.getSummaryReport('0')
    assert session.getSummaryReport('1') == None

    print('All test cases passed for supervisors!')

if __name__ == "__main__":
    main()
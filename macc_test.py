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

    x = session.addMasterAccount('thomas', '(780) 111-1111', 'industrial', '2018-02-25', '2018-03-25')
    print("Master Account Key: {}".format(x))

    print("Accounts managed by {}:".format(session.user_id))
    print("\n".join(session.getManagedAccounts()))

    session.createServiceAgreement(x, 'McDonalds', 'mixed waste', 'everyday', '(780) 111-1111', 250, 350)
    session.createServiceAgreement(x, 'Burger King', 'paper', 'everyday', '(780) 111-1111', 250, 237)
    session.createServiceAgreement(x, 'Wendys', 'metal', 'everyday', '(780) 111-1111', 250, 123)
    session.createServiceAgreement(x, 'Home', 'mixed waste', 'everyday', '(780) 111-1111', 43, 235)

    session.getServiceAgreements(x)
    print()
    session.getSummaryReport(x)

if __name__ == "__main__":
    main()
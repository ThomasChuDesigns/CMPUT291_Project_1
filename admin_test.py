import sqlite3, os

from core.database.controller import Controller
from core.database.util import readSQL

from core.auth.auth import canLogin

# An example testcase, logging in to an account from example_data.sql and ran on test.db 
#
#
#
#

def main():
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

if __name__ == "__main__":
    main()
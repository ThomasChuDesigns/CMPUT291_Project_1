import sqlite3, os

from core.database.controller import Controller
from core.database.util import readSQL, displayQuery, displayRow

from core.auth.auth import canLogin, loginPrompt

# An example testcase, logging in to an account from example_data.sql and ran on test.db 
#
#
#
#

def main():
    # create a controller to test.db
    db_directory = os.path.join(os.path.dirname(__file__), 'data/')
    test_db = Controller(db_directory, 'test.db')

    # insert schema and data into test db
    readSQL(test_db, os.path.join(db_directory, 'p1-tables.sql'))
    readSQL(test_db, os.path.join(db_directory, 'test_data.sql'))

    # try logging in
    session = loginPrompt(test_db)

    status = session.show()
    while(status):
        status = session.show()

    test_db.connection.close()

if __name__ == "__main__":
    main()
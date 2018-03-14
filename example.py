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
    test_db = Controller(db_directory, 'waste_management.db')

    # try logging in
    session = loginPrompt(test_db)
    
    if session:
        print("login successful!")

    test_db.connection.close()

if __name__ == "__main__":
    main()
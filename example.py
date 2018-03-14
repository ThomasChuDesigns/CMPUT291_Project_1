import sqlite3, os

from core.database.controller import Controller
from core.database.util import readSQL, displayQuery, displayRow

from core.auth.auth import canLogin, loginPrompt

# Access the test database with this

def main():
    # create a controller to test.db
    db_directory = os.path.join(os.path.dirname(__file__), 'data/')
    test_db = Controller(db_directory, 'test.db')

    # try logging in
    session = loginPrompt(test_db)

    while(session.show()):
        pass

    test_db.connection.close()

if __name__ == "__main__":
    main()
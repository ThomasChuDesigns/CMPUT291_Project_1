import sqlite3, os

from core.database.controller import Controller
from core.database.util import readSQL, displayQuery, displayRow

from core.auth.util import generateHashedPassword, generateID, createNewUser

# This script allows you to add users into the database


def main():
    # create a controller to test.db
    db_directory = os.path.join(os.path.dirname(__file__), 'data/')
    ctrl_db = Controller(db_directory, 'test.db')

    # insert schema and data into test db
    readSQL(ctrl_db, os.path.join(db_directory, 'p1-tables.sql'))
    readSQL(ctrl_db, os.path.join(db_directory, 'test_data.sql'))

    createNewUser(ctrl_db, '111110', 'account manager', 'bobby', 'password')
    createNewUser(ctrl_db, '12345', 'admin', 'owner', 'password')
    createNewUser(ctrl_db, '1', 'driver', 'test', 'password')
    createNewUser(ctrl_db, '300', 'dispatcher', 'lol', 'password')
    createNewUser(ctrl_db, '111111', 'account manager', 'd4nny', 'password')
    createNewUser(ctrl_db, '222222', 'supervisor', 'thomas', 'password')

    #user_id = generateID()
    #role = input('Enter user\'s role: ')
    #login = input('Enter username: ')
    #password = input('Enter password: ')

    #createNewUser(ctrl_db, user_id, role, login, password)

    #ctrl_db.cursor.execute("SELECT user_id, role, login FROM users")
    #displayQuery(ctrl_db, ctrl_db.cursor.fetchall())

    ctrl_db.connection.close()

if __name__ == "__main__":
    main()
import sqlite3, os

from core.database.controller import Controller
from core.database.util import readSQL, displayQuery, displayRow

from core.auth.util import generateHashedPassword, generateID, createNewUser

# This script allows you to add users into the database


def main():
    # create a controller to test.db
    db_directory = os.path.join(os.path.dirname(__file__), 'data/')
    ctrl_db = Controller(db_directory, 'test.db')

    user_id = generateID()
    role = input('Enter user\'s role: ')
    login = input('Enter username: ')
    password = input('Enter password: ')

    createNewUser(ctrl_db, user_id, role, login, password)

    ctrl_db.cursor.execute("SELECT user_id, role, login FROM users")
    displayQuery(ctrl_db, ctrl_db.cursor.fetchall())

    ctrl_db.connection.close()

if __name__ == "__main__":
    main()
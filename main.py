from core.database.controller import Controller
from core.database.util import displayQuery
from core.auth.util import generateID
from core.auth.auth import canLogin,loginPrompt

import os


# start script to access database
def main():
    # create a controller to waste_management.db
    db_directory = os.path.join(os.path.dirname(__file__), 'data/')
    ctrl_db = Controller(db_directory, 'waste_management.db')

    # try logging in
    session = loginPrompt(ctrl_db)

    while(session.show()):
        pass

    ctrl_db.connection.close()

if __name__ == "__main__":
    main()
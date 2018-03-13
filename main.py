from database.controller import Controller
from auth.auth import canLogin

import os


# start script to access database
def main():
    controller = Controller(os.path.dirname(__file__), 'data/waste_management.db')

    canLogin(controller, 'tinypeacock735', 'storm1')



if __name__ == "__main__": 
    main()
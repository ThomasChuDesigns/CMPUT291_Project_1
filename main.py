import sqlite3
import os

# start script to access database
def main():
    database = os.path.join(os.path.dirname(__file__), "data/database.db")
    sqlite3.connect()




if __name__ == "__main__": 
    main()
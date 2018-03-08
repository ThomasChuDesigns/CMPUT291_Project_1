import sqlite3
import os

from database.models import readSQL

# start script to access database
def main():
    directory = os.path.dirname(__file__)

    database = os.path.join(directory, "data/database.db")
    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')

    # create schema
    readSQL(connection, cursor, os.path.join(directory, "data/p1-tables.sql"))
    readSQL(connection, cursor, os.path.join(directory, "data/a2-data.sql"))

    cursor.execute("SELECT * FROM trucks;")
    rows = cursor.fetchall()
    for entry in rows:
        print(" ".join(entry))




if __name__ == "__main__": 
    main()
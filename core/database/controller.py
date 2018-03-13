import sqlite3
import os

class Controller():
    # use this class to access the database to retrieve queries or add/update/delete entries
    
    def __init__(self, directory, database_file):

        self.database = os.path.join(directory, database_file)
        self.connection = sqlite3.connect(self.database)
        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()
        self.cursor.execute(' PRAGMA forteign_keys=ON; ')
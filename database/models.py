def readSQL(connection, cursor, sql_file):
    with open(sql_file, 'r') as f:
        cursor.executescript(f.read())
        connection.commit()
        f.close()


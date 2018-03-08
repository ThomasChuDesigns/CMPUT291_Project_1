def readSQL(connection, cursor, sql_file):
    with open(sql_file, 'r') as f:
        cursor.execute(f.read())
        connection.commit()


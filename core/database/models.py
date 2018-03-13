def readSQL(controller, sql_file):
    with open(sql_file, 'r') as f:
        controller.cursor.executescript(f.read())
        controller.connection.commit()
        f.close()


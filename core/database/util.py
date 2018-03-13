def readSQL(controller, sql_file):
    with open(sql_file, 'r') as f:
        controller.cursor.executescript(f.read())
        controller.connection.commit()
        f.close()


def getColumnNames(cursor):
    return list(map(lambda x: x[0], cursor.description))

def displayColumns(controller):
    # display header
    for col_name in getColumnNames(controller.cursor):
        print('{:<18}'.format(col_name), end=' ')
    print()

def displayRow(controller, result, header = True):
    # nothing to print end
    if result == None: return
    
    # if header is set to true display columns
    if header: displayColumns(controller)

    for entry in result:
        if entry == None: continue
        print('{:<18}'.format(entry), end=' ')
    print()

def displayQuery(controller, results):
    # nothing to print
    if results == None: return
    
    # display columns
    displayColumns(controller)

    # display body
    for row in results:
        displayRow(controller, tuple(row), False)


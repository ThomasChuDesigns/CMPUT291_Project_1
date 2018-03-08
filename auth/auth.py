def canLogin(connection, cursor, username, password):
    pass


class Auth:
    def __init__(self, connection, cursor, username, password):
        self.username = username

    def options(self):
        pass
    


class AccountManager(Auth):
    role = 'Account Manager'
    def __init__(self, connection, cursor, username, password):
        pass

class Supervisor(AccountManager):
    def __init__(self, connection, cursor, username, password):
        pass

class Dispatcher(Auth):
    role = 'Dispatcher'
    def __init__(self, connection, cursor, username, password):
        pass

class Driver(Auth):
    role = 'Driver'
    def __init__(self, connection, cursor, username, password):
        pass

from .users import Users
from .accounts import Accounts
from .transactions import Transactions


class Client(Users, Accounts, Transactions):
    pass

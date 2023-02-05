from .api import Api


class ClientBase:
    """
    Client for pocketsmith API
    """

    api: Api

    def __init__(self, developer_key: str):
        self.api = Api(developer_key=developer_key)

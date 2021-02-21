from ClientStorageBase import *


class ClientMemoryStorage(ClientStorageBase):
    def __init__(self) -> None:
        self.client: list = []

    def add_client(self, client: Client) -> None:
        self.client.append(client)

    def get_client(self, client_id: int) -> Client:
        for x in self.client:
            if x.id == client_id:
                return x
        raise FileNotFoundError

    def remove_client(self, client_id: int) -> Client:
        client = self.get_client(client_id)
        self.client.pop(client)
        return client

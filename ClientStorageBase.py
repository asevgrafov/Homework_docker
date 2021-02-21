from abc import ABC, abstractmethod
from Models import *


class ClientStorageBase(ABC):

    @abstractmethod
    def add_client(self, client: Client) -> None:
        pass

    @abstractmethod
    def get_client(self, client_id: int) -> Client:
        pass

    @abstractmethod
    def remove_client(self, client_id: int) -> Client:
        pass

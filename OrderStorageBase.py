from abc import ABC, abstractmethod
from Models import *


class OrderStorageBase(ABC):

    @abstractmethod
    def add_order(self, order: Order) -> None:
        pass

    @abstractmethod
    def get_order(self, order_id: int) -> Order:
        pass

    @abstractmethod
    def update_order(self, order: Order) -> Order:
        pass
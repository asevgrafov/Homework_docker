from abc import ABC, abstractmethod
from Models import *


class DriverStorageBase(ABC):

    @abstractmethod
    def add_driver(self, driver: Driver) -> None:
        pass

    @abstractmethod
    def get_driver(self, driver_id: int) -> Driver:
        pass

    @abstractmethod
    def remove_driver(self, driver_id: int) -> Driver:
        pass

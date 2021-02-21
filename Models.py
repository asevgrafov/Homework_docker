from flask import jsonify
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship

from OrderStatus import *

Base = declarative_base()


class Driver(Base):
    __tablename__ = 'drivers'  # имя таблицы
    # Атрибуты класса описывают колонки таблицы, их типы данных и ограничения
    id = Column(Integer, primary_key=True, autoincrement=True, comment="Идентификатор водителя")
    name = Column(String(100), comment="Имя водителя")
    car = Column(String(100), comment="Описание машины водителя")
    orders = relationship("Order", cascade="all, delete")

    # переопределение выдачи объекта на экран через print
    def repr(self) -> str:
        return "<Driver(name={0}, car={1})".format(
            self.name,
            self.car
            )

    def to_json(self) -> dict:
        json_return = {"id": self.id,
                       "name": self.name,
                       "car": self.car}
        return jsonify(json_return)


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, autoincrement=True, comment="Идентификатор клиента")
    name = Column(String(100), comment="Имя клиента")
    is_vip = Column(String, comment="Вип клиент")
    orders = relationship("Order", cascade="all, delete")

    def repr(self) -> str:
        return "<Client(name={0}, is_vip={1})".format(
            self.name,
            self.is_vip
            )

    def to_json(self) -> dict:
        json_return = {"id": self.id,
                       "name": self.name,
                       "is_vip": self.is_vip}
        return jsonify(json_return)


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True, comment="Идентификатор заказа")
    address_from = Column(VARCHAR, nullable=False, comment="Адрес клиента")
    address_to = Column(VARCHAR, nullable=False, comment="Куда едем")
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    driver_id = Column(Integer, ForeignKey('drivers.id'), nullable=False)
    date_created = Column(String, nullable=False)
    status = Column(VARCHAR, nullable=False)

    def to_json(self) -> dict:
        json_return = {"id": self.id,
                       "address_from": self.address_from,
                       "address_to": self.address_to,
                       "client_id": self.client_id,
                       "driver_id": self.driver_id,
                       "date_created": self.date_created,
                       "status": self.status
                       }
        return jsonify(json_return)

    def set_status(self, status: str) -> None:
        order_status = OrderStatus(self.status)
        order_status.change_to_state(status)
        self.status = order_status.status

    def check_state(self) -> None:
        if self.status != "not_accepted":
            raise OrderStatusInvalidStateException(message="Невозможно изменить данные в текущем статусе заказа")

    def set_driver_id(self, driver_id: int) -> None:
        self.check_state()
        self.driver_id = driver_id

    def set_client_id(self, client_id: int) -> None:
        self.check_state()
        self.client_id = client_id

    def set_date_created(self, date_created: str) -> None:
        self.check_state()
        self.date_created = date_created

    def set_address_from(self, address_from: str) -> None:
        if self.address_from != address_from:
            raise OrderStatusInvalidStateException(message="Адрес невозможно изменить")

    def set_address_to(self, address_to: str) -> None:
        if self.address_to != address_to:
            raise OrderStatusInvalidStateException(message="Адрес невозможно изменить")

    def repr(self) -> str:
        return "<Order(address_from={0}, address_to={1}, client_id={2}, driver_id={3}, " \
               "date_created={4}, status={5}".format(
                self.address_from,
                self.address_to,
                self.client_id,
                self.driver_id,
                self.date_created,
                self.status
                )

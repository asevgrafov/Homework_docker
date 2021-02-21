from DriverStorageBase import *
from faker import Faker
from faker_vehicle import VehicleProvider
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine


class DriverDBStorage(DriverStorageBase):
    def __init__(self) -> None:
        engine = create_engine('postgresql+psycopg2://postgres:postgres@postgres/users')
        Base.metadata.create_all(engine)
        self.session: Session = sessionmaker(bind=engine)()

    def add_driver(self, driver: Driver) -> None:
        """Добавление водителя"""
        self.session.add(driver)
        self.session.commit()

    def get_driver(self, driver_id: int) -> Driver:
        """Поиск воителя в базе по Id"""
        return self.session.query(Driver).filter(Driver.id == driver_id).one()

    def remove_driver(self, driver_id: int) -> Driver:
        """Удаление водителя"""
        driver = self.session.query(Driver).filter(Driver.id == driver_id).one()
        self.session.delete(driver)
        self.session.commit()
        self.session.close()
        return driver

    def insert_test_data(self) -> None:
        """Добавление тестовых данных"""
        fake = Faker('ru_RU')
        fake.add_provider(VehicleProvider)
        for _ in range(5):
            # Новая запись в таблице создаётся как объект класса
            new_driver = Driver(name=fake.first_name_nonbinary(),
                                car=fake.vehicle_make_model())

            self.session.add(new_driver)  # добавление записи в таблицу
        self.session.commit()

import random
from faker import Faker
from ClientStorageBase import *
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine


class ClientDBStorage(ClientStorageBase):
    def __init__(self) -> None:
        engine = create_engine('postgresql+psycopg2://postgres:postgres@postgres/users')
        Base.metadata.create_all(engine)
        self.session: Session = sessionmaker(bind=engine)()

    def add_client(self, client: Client) -> None:
        """Добавление клиента"""
        self.session.add(client)
        self.session.commit()

    def get_client(self, client_id: int) -> Client:
        """Поиск клиента в базе по Id"""
        return self.session.query(Client).filter(Client.id == client_id).one()

    def remove_client(self, client_id: int) -> Client:
        """Удаление клиента"""
        client = self.session.query(Client).filter(Client.id == client_id).one()
        self.session.delete(client)
        self.session.commit()
        return client

    def insert_test_data(self) -> None:
        """Добавление тестовых данных"""
        fake = Faker('ru_RU')
        for _ in range(5):
            # Новая запись в таблице создаётся как объект класса
            new_client = Client(name=fake.first_name_nonbinary(),
                                is_vip=random.choice([True, False]))
            self.session.add(new_client)  # добавление записи в таблицу
        self.session.commit()

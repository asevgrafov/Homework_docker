from OrderStorageBase import *
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine


class OrderDBStorage(OrderStorageBase):
    def __init__(self) -> None:
        engine = create_engine('postgresql+psycopg2://postgres:postgres@postgres/users')
        Base.metadata.create_all(engine)
        self.session: Session = sessionmaker(bind=engine)()

    def add_order(self, order: Order) -> None:
        self.session.add(order)
        self.session.commit()

    def get_order(self, order_id: int) -> Order:
        return self.session.query(Order).filter(Order.id == order_id).one()

    def update_order(self, order: Order) -> Order:
        self.session.commit()
        return order

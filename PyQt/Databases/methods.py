from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alchemy_models import Category, Units, Positions, Goods, Employees,Vendors,Base


PATH_DB = 'database.sqlite3'
TABLES = [Category(category_name='Продукты', category_description='Какие-то продукты'),
          Units(unit="Шт"),
          Positions(position="Менеджер"),
          Goods(good_name="Iphone"),
          Employees(employee_fio="Иванов Иван Иванович"),
          Vendors(vendor_name="Apple", vendor_owner_chip_form="ООО", vendor_address="California",
                  vendor_phone='8900', vendor_email="Apple@apple.com")
          ]

class Repository:

    def __init__(self, path_db):
        self.engine = create_engine(f'sqlite:///{path_db}?check_same_thread=False')
        self.create_base()
        self.session = self.get_session()


    def create_base(self):
        """Создаем БД"""
        base = Base
        base.metadata.create_all(self.engine)

    def get_session(self):
        """Создаем объект сессии"""
        session = sessionmaker(bind=self.engine)
        session = session()
        return session

    def add_session(self, tables):
        """Закружаем сущность в базу"""
        session = self.get_session()
        session.add_all(tables)
        session.commit()



if __name__ == '__main__':
    REP = Repository(PATH_DB)
    REP.add_session(TABLES)

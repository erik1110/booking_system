from sqlalchemy import Column, ForeignKey, String, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 定義 Users 模型
class Users(Base):
    __tablename__ = 'users'
    user_id = Column('user_id', String(20), primary_key=True)
    name = Column('name', String(50), nullable=False)
    password = Column('password', String(20), nullable=False)
    address = Column('address', String(100))
    phone = Column('phone', String(20))
    birthday = Column('birthday', String(20))


# 定義 Items 模型
class Items(Base):
    __tablename__ = 'items'
    item_id = Column('item_id', Integer, primary_key=True)
    name = Column('name', String(100), nullable=False)
    price = Column('price', Float)
    description = Column('description', String(200))
    available_day = Column('available_day', String(20))
    location = Column('location', String(10))
    image = Column('image', String(100))
    user_id = Column('user_id', Integer)
    borrow_date = Column('borrow_date', String(20))
    return_date = Column('return_date', String(20))
    status = Column('status', String(20))
    
class Records(Base):
    __tablename__ = 'records'
    records_id = Column('records_id', Integer, primary_key=True)
    item_id = Column('item_id', ForeignKey('items.item_id'))
    user_id = Column('user_id', ForeignKey('users.user_id'))
    borrow_date = Column('borrow_date', String(20))
    return_date = Column('return_date', String(20))

class Reservation(Base):
    __tablename__ = 'reservation'
    reservation_id = Column('reservation_id', Integer, primary_key=True)
    item_id = Column('item_id', ForeignKey('items.item_id'))
    user_id = Column('user_id', ForeignKey('users.user_id'))
    reverse_date = Column('reverse_date', String(20))

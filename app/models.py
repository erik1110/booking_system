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

# 定義 Items 模型 (物品)
class Items(Base):
    __tablename__ = 'items'
    item_id = Column('item_id', Integer, primary_key=True)
    name = Column('name', String(100), nullable=False)
    price = Column('price', Float)
    description = Column('description', String(200))
    available_day = Column('available_day', Integer)
    location = Column('location', String(10))
    image = Column('image', String(100))
    user_id = Column('user_id', Integer)
    borrow_date = Column('borrow_date', String(20))
    return_date = Column('return_date', String(20))
    booking_status = Column('booking_status', String(20))
    reserve_status = Column('reserve_status', String(20))
    # 定義一對多的關係
    records_items = relationship('Records_items')

# 定義 Records 模型 (單據)
class Records(Base):
    __tablename__ = 'records'
    records_id = Column('records_id', String(100), primary_key=True)
    action = Column('action', String(20))
    user_id = Column('user_id', ForeignKey('users.user_id'))
    records_date = Column('records_date', String(20))
    total = Column('total', Integer)
    # 定義一對多的關係
    records_items = relationship('Records_items')

# 定義 Records_items 模型 (單據詳細)
class Records_items(Base):
    __tablename__ = 'records_items'
    id = Column('id', Integer, primary_key=True)
    records_id = Column('records_id', ForeignKey('records.records_id'))
    item_id = Column('item_id', ForeignKey('items.item_id'))
    user_id = Column('user_id', ForeignKey('users.user_id'))
    records_date = Column('records_date', String(20))
    action = Column('action', String(20))
    # 定義多對一的關係 （RecordsLineItems -> Records）
    records = relationship('Records', backref='Records_items')
    # 定義多對一的關係 （RecordsLineItems -> Items
    items = relationship('Items', backref='Records_items')

# # 定義 Reservation 模型
# class Reservation(Base):
#     __tablename__ = 'reservation'
#     reservation_id = Column('reservation_id', Integer, primary_key=True)
#     item_id = Column('item_id', ForeignKey('items.item_id'))
#     user_id = Column('user_id', ForeignKey('users.user_id'))
#     reverse_date = Column('reverse_date', String(20))

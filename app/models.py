from sqlalchemy import Column, ForeignKey, String, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 定義 Users 模型
class Users(Base):
    __tablename__ = 'users'
    user_id = Column('user_id', String(30), primary_key=True)
    name = Column('name', String(30), nullable=False)
    password = Column('password', String(30), nullable=False)
    address = Column('address', String(30))
    phone = Column('phone', String(20))
    birthday = Column('birthday', DateTime)
    available_status = Column('available_status', String(20))

# 定義 Items 模型 (物品)
class Items(Base):
    __tablename__ = 'items'
    item_id = Column('item_id', String(30), primary_key=True)
    name = Column('name', String(30), nullable=False)
    price = Column('price', Integer)
    fine = Column('fine', Integer)
    description = Column('description', String(30))
    available_day = Column('available_day', Integer)
    location = Column('location', String(10))
    image = Column('image', String(100))
    user_id = Column('user_id', String(30))
    borrow_date = Column('borrow_date', DateTime)
    expected_date = Column('expected_date', DateTime)
    return_date = Column('return_date', DateTime)
    reserve_date = Column('reserve_date', DateTime)
    booking_status = Column('booking_status', String(30))
    reserve_status = Column('reserve_status', String(30))
    # 定義一對多的關係
    items_hist = relationship('items_hist')

# 定義 Orders 模型 (單據)
class Orders(Base):
    __tablename__ = 'orders'
    order_id = Column('order_id', String(100), primary_key=True)
    action = Column('action', String(20))
    user_id = Column('user_id', ForeignKey('users.user_id'))
    records_date = Column('records_date', String(20))
    total = Column('total', Float)
    # 定義一對多的關係
    items_hist = relationship('items_hist')

# 定義 ItemsHist 模型 (單據詳細)
class ItemsHist(Base):
    __tablename__ = 'items_hist'
    hist_id = Column('hist_id', String(30), primary_key=True)
    item_id = Column('item_id', ForeignKey('items.item_id'))
    user_id = Column('user_id', ForeignKey('users.user_id'))
    borrow_date = Column('borrow_date', DateTime)
    expected_date = Column('expected_date', DateTime)
    return_date = Column('return_date', DateTime)
    reserve_date = Column('reserve_date', DateTime)
    borrow_order_id = Column('borrow_order_id', ForeignKey('orders.order_id'))
    return_order_id = Column('return_order_id', ForeignKey('orders.order_id'))
    reserve_order_id = Column('reserve_order_id', ForeignKey('orders.order_id'))
    # 定義多對一的關係 (ItemsHist -> Orders)
    orders = relationship('Orders', backref='items_hist')
    # 定義多對一的關係 (ItemsHist -> Items)
    items = relationship('Items', backref='items_hist')

# 定義 Comments 模型
class Comments(Base):
    __tablename__ = 'comments'
    comment_id = Column('comment_id', String(30), primary_key=True)
    item_id = Column('item_id', ForeignKey('items.item_id'))
    user_id = Column('user_id', ForeignKey('users.user_id'))
    content = Column('content', String(100))
    comment_date = Column('comment_date', DateTime)

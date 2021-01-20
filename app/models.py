from sqlalchemy import Column, ForeignKey, String, Integer, Float
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
    birthday = Column('birthday', String(30))
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
    borrow_date = Column('borrow_date', String(30))
    expected_date = Column('expected_date', String(30))
    return_date = Column('return_date', String(30))
    reserve_date = Column('reserve_date', String(30))
    booking_status = Column('booking_status', String(30))
    reserve_status = Column('reserve_status', String(30))
    # 定義一對多的關係 (Items -> ItemsHist)
    items_hist = relationship('ItemsHist')
    # 定義一對多的關係 (Items -> Comments)
    comments = relationship('Comments')

# 定義 Orders 模型 (單據)
class Orders(Base):
    __tablename__ = 'orders'
    order_id = Column('order_id', String(100), primary_key=True)
    action = Column('action', String(20))
    user_id = Column('user_id', ForeignKey('users.user_id'))
    total = Column('total', Float)
    order_date = Column('order_date', String(20))
    # # 定義一對多的關係 (Orders -> ItemsHist)
    # items_hist = relationship('ItemsHist')

# 定義 ItemsHist 模型 (單據詳細)
class ItemsHist(Base):
    __tablename__ = 'items_hist'
    hist_id = Column('hist_id', String(30), primary_key=True)
    item_id = Column('item_id', ForeignKey('items.item_id'))
    user_id = Column('user_id', ForeignKey('users.user_id'))
    borrow_date = Column('borrow_date', String(30))
    expected_date = Column('expected_date', String(30))
    return_date = Column('return_date', String(30))
    reserve_date = Column('reserve_date', String(30))
    borrow_order_id = Column('borrow_order_id', String(30))
    return_order_id = Column('return_order_id', String(30))
    reserve_order_id = Column('reserve_order_id', String(30))
    # # 定義多對一的關係 (ItemsHist -> Orders)
    # orders = relationship('Orders', backref='ItemsHist')
    # 定義多對一的關係 (ItemsHist -> Items)
    items = relationship('Items', backref='ItemsHist')

# 定義 Comments 模型
class Comments(Base):
    __tablename__ = 'comments'
    comment_id = Column('comment_id', String(30), primary_key=True)
    item_id = Column('item_id', ForeignKey('items.item_id'))
    user_id = Column('user_id', ForeignKey('users.user_id'))
    content = Column('content', String(100))
    comment_date = Column('comment_date', String(30))
    # 定義多對一的關係 (Comments -> Items)
    items = relationship('Items', backref='Comments')

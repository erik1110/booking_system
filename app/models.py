from sqlalchemy import Column, ForeignKey, String, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 定義Customer模型
class Customer(Base):
    __tablename__ = 'customers'
    id = Column('id', String(20), primary_key=True)
    name = Column('name', String(50), nullable=False)
    password = Column('password', String(20), nullable=False)
    address = Column('address', String(100))
    phone = Column('phone', String(20))
    birthday = Column('birthday', String(20))


# 定義Goods模型
class Goods(Base):
    __tablename__ = 'goods'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(100), nullable=False)
    price = Column('price', Float)
    description = Column('description', String(200))
    location = Column('location', String(10))
    image = Column('image', String(100))
    # 定義一對多的關係（Goods->OrderLineItem）
    orderLineItems = relationship('OrderLineItem')  # OrderLineItem模型


# 定義Orders模型
class Orders(Base):
    __tablename__ = 'orders'
    id = Column('id', String(20), primary_key=True)
    orderdate = Column('order_date', String(20))
    status = Column('status', Integer)  # 1待付款 0已付款
    total = Column('total', Float)
    # 定義一對多的關系（Orders->OrderLineItem）
    orderLineItems = relationship('OrderLineItem')  # OrderLineItem模型


class OrderLineItem(Base):
    __tablename__ = 'orderLineItems'
    id = Column('id', Integer, primary_key=True)
    quantity = Column('quantity', Integer)
    subtotal = Column('sub_total', Float)
    goodsid = Column('goodsid', ForeignKey('goods.id'))  # goods是表，不是模型對象
    orderid = Column('orderid', ForeignKey('orders.id'))  # orders是表，不是模型對象
    # 定義一對多的關系（OrderLineItem->Orders），backref表示反向關聯
    orders = relationship('Orders', backref='OrderLineItem')  # Orders和OrderLineItem都是模型
    # 定義一對多的關系（OrderLineItem->Goods），backref表示反向關聯
    goods = relationship('Goods', backref='OrderLineItem')  # Goods和OrderLineItem都是模型

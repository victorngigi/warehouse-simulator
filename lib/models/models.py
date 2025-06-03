# lib/models/models.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    MetaData,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

DATABASE_URL = "sqlite:///db/warehouse.db"
engine = create_engine(DATABASE_URL, echo=False)

Session = sessionmaker(bind=engine)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    sku = Column(String(100), unique=True, nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)
    price_per_unit = Column(Float, nullable=False)

    order_items = relationship("OrderItem", backref="product", cascade="all, delete-orphan")

    def __repr__(self):
        return (
            f"<Product(id={self.id}, name='{self.name}', "
            f"sku='{self.sku}', stock={self.stock_quantity})>"
        )


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_name = Column(String(255), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String(50), nullable=False, default="pending")

    order_items = relationship("OrderItem", backref="order", cascade="all, delete-orphan")
    shipment = relationship("Shipment", backref="order", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return (
            f"<Order(id={self.id}, customer='{self.customer_name}', "
            f"status='{self.status}', date={self.order_date})>"
        )


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    def __repr__(self):
        return (
            f"<OrderItem(id={self.id}, order_id={self.order_id}, "
            f"product_id={self.product_id}, quantity={self.quantity}, "
            f"unit_price={self.unit_price})>"
        )


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    shipped_date = Column(DateTime, default=None)
    delivery_status = Column(
        String(50), nullable=False, default="not shipped"
    )  

    def __repr__(self):
        return (
            f"<Shipment(id={self.id}, order_id={self.order_id}, "
            f"shipped_date={self.shipped_date}, status='{self.delivery_status}')>"
        )

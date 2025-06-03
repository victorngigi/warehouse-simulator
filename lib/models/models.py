from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    MetaData,
    Enum,
    Float,
    CheckConstraint
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

ORDER_STATUSES = ("pending", "fulfilled", "cancelled")
DELIVERY_STATUSES = ("not shipped", "in transit", "delivered")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    sku = Column(String(100), unique=True, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    order_items = relationship("OrderItem", backref="product", cascade="all, delete-orphan")

    def __repr__(self):
        return (
            f"<Product(id={self.id}, name='{self.name}', "
            f"sku='{self.sku}', stock={self.stock_quantity})>"
        )

    def __str__(self):
        return f"{self.name} (SKU: {self.sku}) - ${self.price_per_unit:.2f} [{self.stock_quantity} in stock]"

    def is_in_stock(self, quantity):
        return self.stock_quantity >= quantity


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, nullable=False)
    customer_name = Column(String(255), nullable=False)
    order_date = Column(DateTime, nullable=False, default=datetime.now)
    status = Column(Enum(*ORDER_STATUSES, name="order_status"), nullable=False, default="pending")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    order_items = relationship("OrderItem", backref="order", cascade="all, delete-orphan")
    shipment = relationship("Shipment", backref="order", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return (
            f"<Order(id={self.id}, customer='{self.customer_name}', "
            f"status='{self.status}', date={self.order_date})>"
        )

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name} - {self.status}"

    def total_amount(self):
        return sum(item.unit_price * item.quantity for item in self.order_items)


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)

    __table_args__ = (
        CheckConstraint('quantity > 0', name='ck_order_items_quantity_positive'),
    )

    def __repr__(self):
        return (
            f"<OrderItem(id={self.id}, order_id={self.order_id}, "
            f"product_id={self.product_id}, quantity={self.quantity}, "
            f"unit_price={self.unit_price})>"
        )

    def __str__(self):
        return f"{self.quantity} x Product #{self.product_id} @ ${self.unit_price:.2f}"


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    shipped_date = Column(DateTime, default=None)
    delivery_status = Column(Enum(*DELIVERY_STATUSES, name="delivery_status"), nullable=False, default="not shipped")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return (
            f"<Shipment(id={self.id}, order_id={self.order_id}, "
            f"shipped_date={self.shipped_date}, status='{self.delivery_status}')>"
        )

    def __str__(self):
        return f"Shipment #{self.id} - Order #{self.order_id} - {self.delivery_status}"

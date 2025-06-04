# lib/helpers.py
from lib.models import Session, Product, Order 
from datetime import datetime

def print_products(session):
    """Print all products from the given session in a neat format."""
    products = session.query(Product).order_by(Product.id).all()
    print("\n--- 📦 Current Inventory Stock ---")
    if not products:
        print(" (Empty shelves! No products found. Time to restock!)\n")
    else:
        print("ID | Product Name           | SKU        | Stock | Price (KSH)")
        print("---|------------------------|------------|-------|------------")
        for p in products:
            name_padded = p.name.ljust(22)[:22]
            sku_padded = p.sku.ljust(10)[:10]
            print(f"{str(p.id).ljust(2)} | {name_padded} | {sku_padded} | {str(p.stock_quantity).ljust(5)} | {p.price_per_unit:.2f}")
        print("----------------------------------------------------\n")

def print_orders(session):
    """Print all orders from the given session in a neat format."""
    orders = session.query(Order).order_by(Order.id).all()
    print("\n--- 📦 Current Orders ---")
    if not orders:
        print(" (No orders in the system yet. Time to get selling!)\n")
    else:
        print("ID | Customer Name          | Order Date           | Status     | Items | Total Value")
        print("---|------------------------|----------------------|------------|-------|------------")
        for o in orders:
            customer_name_padded = o.customer_name.ljust(22)[:22]
            order_date_str = o.order_date.strftime("%Y-%m-%d %H:%M").ljust(20)
            status_padded = o.status.ljust(10)
            total_value = sum(item.quantity * item.unit_price for item in o.order_items) 
            print(f"{str(o.id).ljust(2)} | {customer_name_padded} | {order_date_str} | {status_padded} | {str(len(o.order_items)).ljust(5)} | KSH-{total_value:.2f}")
        print("--------------------------------------------------------------------------------\n")


def get_product_by_sku(session, sku):
    """Retrieve a product by SKU."""
    return session.query(Product).filter(Product.sku == sku).first()

def get_order_by_id(session, order_id):
    """Retrieve an order by its ID."""
    return session.query(Order).filter(Order.id == order_id).first()

def get_product_by_id(session, product_id):
    """Retrieve a product by its ID."""
    return session.get(Product, product_id) 
# lib/helpers.py

from lib.models import Session, Product, Order

def print_products(session):
    """Print all products from the given session in a neat format."""
    products = session.query(Product).order_by(Product.id).all()
    if not products:
        print("  (no products found)")
    for p in products:
        print(f"  [{p.id}] {p.name} (SKU: {p.sku}) – "
              f"Stock: {p.stock_quantity}, Price: {p.price_per_unit}")


def print_orders(session):
    """Print all orders from the given session in a neat format."""
    orders = session.query(Order).order_by(Order.id).all()
    if not orders:
        print("  (no orders found)")
    for o in orders:
        print(f"  [{o.id}] Customer: {o.customer_name} – Status: {o.status}")

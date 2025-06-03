from lib.models import Product, Order

def print_products(session):
    """Print all products from the given session in a neat format."""
    products = session.query(Product).order_by(Product.id).all()
    if not products:
        print("  (no products found)")
        return

    print("\n--- Product Inventory ---")
    for p in products:
        print(f"  [{p.id}] {p.name} (SKU: {p.sku}) - Stock: {p.stock_quantity}, Price: ${p.price_per_unit:.2f}")

def print_orders(session):
    """Print all orders from the given session in a neat format."""
    orders = session.query(Order).order_by(Order.id).all()
    if not orders:
        print("  (no orders found)")
        return

    print("\n--- Order List ---")
    for o in orders:
        date_str = o.order_date.strftime("%Y-%m-%d %H:%M") if o.order_date else "N/A"
        print(f"  [{o.id}] Customer: {o.customer_name} - Status: {o.status} - Date: {date_str}")

def get_product_by_sku(session, sku):
    """Retrieve a product by SKU."""
    return session.query(Product).filter(Product.sku == sku).first()

def get_order_by_id(session, order_id):
    """Retrieve an order by its ID."""
    return session.query(Order).filter(Order.id == order_id).first()

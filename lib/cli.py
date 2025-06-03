# lib/cli.py

import sys
from lib.models import Session, Product, Order, OrderItem, Shipment
from datetime import datetime


def list_products():
    session = Session()
    products = session.query(Product).order_by(Product.id).all()
    print("\n--- Inventory ---")
    if not products:
        print("  (no products found)\n")
    else:
        for p in products:
            print(f"  [{p.id}] {p.name} (SKU: {p.sku}) – "
                  f"Stock: {p.stock_quantity}, Price: {p.price_per_unit}")
        print("")
    session.close()


def add_product():
    session = Session()
    name = input("Product name: ").strip()
    sku = input("SKU: ").strip()
    try:
        price = float(input("Price per unit: ").strip())
        qty = int(input("Quantity in stock: ").strip())
    except ValueError:
        print("Invalid number. Operation canceled.")
        session.close()
        return

    existing = session.query(Product).filter_by(sku=sku).first()
    if existing:
        print("A product with that SKU already exists.")
        session.close()
        return

    product = Product(
        name=name,
        sku=sku,
        price_per_unit=price,
        stock_quantity=qty
    )
    session.add(product)
    session.commit()
    print(f"Added product [{product.id}] {product.name}.\n")
    session.close()


def create_order():
    session = Session()
    customer = input("Customer name: ").strip()
    if not customer:
        print("Customer name cannot be empty.")
        session.close()
        return

    order = Order(customer_name=customer)
    session.add(order)
    session.commit()  

    while True:
        list_products()
        choice = input("Enter Product ID to add (0 to finish): ").strip()
        try:
            pid = int(choice)
        except ValueError:
            print("Invalid ID.")
            continue

        if pid == 0:
            break

        prod = session.query(Product).get(pid)
        if not prod:
            print("Product not found.")
            continue

        try:
            qty = int(input(f"Quantity of '{prod.name}': ").strip())
        except ValueError:
            print("Invalid quantity.")
            continue

        if qty <= 0 or prod.stock_quantity < qty:
            print("Insufficient stock or invalid quantity.")
            continue

        prod.stock_quantity -= qty
        item = OrderItem(
            order_id=order.id,
            product_id=prod.id,
            quantity=qty,
            unit_price=prod.price_per_unit
        )
        session.add(item)
        session.commit()
        print(f"  Added {qty} × {prod.name} to order #{order.id}.\n")

    if not order.order_items:
        session.delete(order)
        session.commit()
        print("Order canceled (no items).")
    else:
        print(f"Order #{order.id} for '{customer}' created with {len(order.order_items)} item(s).")
    session.close()


def list_orders():
    session = Session()
    orders = session.query(Order).order_by(Order.id).all()
    print("\n--- Orders ---")
    if not orders:
        print("  (no orders found)\n")
    else:
        for o in orders:
            print(f"  [{o.id}] Customer: {o.customer_name} – "
                  f"Status: {o.status}, Items: {len(o.order_items)}")
        print("")
    session.close()


def fulfill_order():
    session = Session()
    list_orders()
    try:
        oid = int(input("Enter Order ID to fulfill: ").strip())
    except ValueError:
        print("Invalid ID.")
        session.close()
        return

    order = session.query(Order).get(oid)
    if not order:
        print("Order not found.")
        session.close()
        return
    if order.status != "pending":
        print(f"Order is already '{order.status}'.")
        session.close()
        return

    order.status = "fulfilled"
    shipment = Shipment(order_id=order.id, delivery_status="not shipped")
    session.add(shipment)
    session.commit()
    print(f"Order #{order.id} marked as fulfilled; shipment created (ID {shipment.id}).")
    session.close()


def track_shipments():
    session = Session()
    shipments = session.query(Shipment).order_by(Shipment.id).all()
    print("\n--- Shipments ---")
    if not shipments:
        print("  (no shipments found)\n")
    else:
        for s in shipments:
            print(f"  [{s.id}] Order #{s.order_id} – Status: {s.delivery_status}, "
                  f"Shipped date: {s.shipped_date}")
        print("")
    session.close()


def update_shipment():
    session = Session()
    track_shipments()
    try:
        sid = int(input("Enter Shipment ID to update: ").strip())
    except ValueError:
        print("Invalid ID.")
        session.close()
        return

    shipment = session.query(Shipment).get(sid)
    if not shipment:
        print("Shipment not found.")
        session.close()
        return

    print(f"Current status: {shipment.delivery_status}")
    new_status = input("New status (e.g., 'in transit', 'delivered'): ").strip()
    if not new_status:
        print("Status cannot be empty.")
        session.close()
        return

    shipment.delivery_status = new_status
    if new_status.lower() == "delivered":
        shipment.shipped_date = datetime.utcnow()
    session.commit()
    print(f"Shipment #{shipment.id} status updated to '{new_status}'.")
    session.close()


def exit_program():
    print("Goodbye!")
    sys.exit()


def menu():
    print("\n=== Warehouse Simulator ===")
    print("0. Exit")
    print("1. List Products")
    print("2. Add Product")
    print("3. Create Order")
    print("4. List Orders")
    print("5. Fulfill Order (create shipment)")
    print("6. Track Shipments")
    print("7. Update Shipment Status")


def main():
    while True:
        menu()
        choice = input("> ").strip()
        if choice == "0":
            exit_program()
        elif choice == "1":
            list_products()
        elif choice == "2":
            add_product()
        elif choice == "3":
            create_order()
        elif choice == "4":
            list_orders()
        elif choice == "5":
            fulfill_order()
        elif choice == "6":
            track_shipments()
        elif choice == "7":
            update_shipment()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()

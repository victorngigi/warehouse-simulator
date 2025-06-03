import sys
from lib.models import Session, Product, Order, OrderItem, Shipment
from datetime import datetime


def list_products():
    session = Session()
    try:
        products = session.query(Product).order_by(Product.id).all()
        print("\n--- Inventory ---")
        if not products:
            print("  (no products found)\n")
        else:
            for p in products:
                print(f"  [{p.id}] {p.name} (SKU: {p.sku}) – "
                      f"Stock: {p.stock_quantity}, Price: KSH-{p.price_per_unit:.2f}")
            print("")
    finally:
        session.close()


def add_product():
    session = Session()
    try:
        name = input("Product name: ").strip()
        sku = input("SKU: ").strip()
        try:
            price = float(input("Price per unit: ").strip())
            qty = int(input("Quantity in stock: ").strip())
        except ValueError:
            print("Invalid number. Operation canceled.")
            return

        if session.query(Product).filter_by(sku=sku).first():
            print("A product with that SKU already exists.")
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
    except Exception as e:
        session.rollback()
        print(f"Error adding product: {e}")
    finally:
        session.close()

def update_product():
    session = Session()
    list_products()
    try:
        pid = int(input("Enter Product ID to update: ").strip())
    except ValueError:
        print("Invalid ID.")
        session.close()
        return

    product = session.query(Product).get(pid)
    if not product:
        print("Product not found.")
        session.close()
        return

    print(f"Current name: {product.name}")
    new_name = input("New name (leave blank to keep): ").strip()
    if new_name:
        product.name = new_name

    print(f"Current price: {product.price_per_unit}")
    try:
        new_price = input("New price (leave blank to keep): ").strip()
        if new_price:
            product.price_per_unit = float(new_price)
    except ValueError:
        print("Invalid price input. Update canceled.")
        session.close()
        return

    print(f"Current stock quantity: {product.stock_quantity}")
    try:
        new_stock = input("New stock quantity (leave blank to keep): ").strip()
        if new_stock:
            product.stock_quantity = int(new_stock)
    except ValueError:
        print("Invalid quantity input. Update canceled.")
        session.close()
        return

    session.commit()
    print(f"Product [{product.id}] updated.")
    session.close()


def delete_product():
    session = Session()
    list_products()
    try:
        pid = int(input("Enter Product ID to delete: ").strip())
    except ValueError:
        print("Invalid ID.")
        session.close()
        return

    product = session.query(Product).get(pid)
    if not product:
        print("Product not found.")
        session.close()
        return

    # Check if product is in any pending orders
    linked_items = session.query(OrderItem).filter_by(product_id=pid).count()
    if linked_items > 0:
        print("Cannot delete product: It is linked to existing order items.")
        session.close()
        return

    confirm = input(f"Are you sure you want to delete product '{product.name}'? (y/n): ").strip().lower()
    if confirm == "y":
        session.delete(product)
        session.commit()
        print("Product deleted.")
    else:
        print("Delete canceled.")

    session.close()


def create_order():
    session = Session()
    try:
        customer = input("Customer name: ").strip()
        if not customer:
            print("Customer name cannot be empty.")
            return

        order = Order(customer_name=customer, order_date=datetime.now())
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

            prod = session.get(Product, pid)
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
            print(f"  Added {qty} x {prod.name} to order #{order.id}.\n")

        if not order.order_items:
            session.delete(order)
            session.commit()
            print("Order canceled (no items).")
        else:
            print(f"Order #{order.id} for '{customer}' created with {len(order.order_items)} item(s).")
    except Exception as e:
        session.rollback()
        print(f"Error creating order: {e}")
    finally:
        session.close()


def list_orders():
    session = Session()
    try:
        orders = session.query(Order).order_by(Order.id).all()
        print("\n--- Orders ---")
        if not orders:
            print("  (no orders found)\n")
        else:
            for o in orders:
                print(f"  [{o.id}] Customer: {o.customer_name} - "
                      f"Status: {o.status}, Items: {len(o.order_items)}")
            print("")
    finally:
        session.close()

def update_order():
    session = Session()
    list_orders()
    try:
        oid = int(input("Enter Order ID to update: ").strip())
    except ValueError:
        print("Invalid ID.")
        session.close()
        return

    order = session.query(Order).get(oid)
    if not order:
        print("Order not found.")
        session.close()
        return

    print(f"Current customer name: {order.customer_name}")
    new_customer = input("New customer name (leave blank to keep): ").strip()
    if new_customer:
        order.customer_name = new_customer

    print(f"Current status: {order.status}")
    new_status = input("New status (leave blank to keep): ").strip()
    if new_status:
        order.status = new_status

    session.commit()
    print(f"Order [{order.id}] updated.")
    session.close()

def delete_order():
    session = Session()
    list_orders()
    try:
        oid = int(input("Enter Order ID to delete: ").strip())
    except ValueError:
        print("Invalid ID.")
        session.close()
        return

    order = session.query(Order).get(oid)
    if not order:
        print("Order not found.")
        session.close()
        return

    confirm = input(f"Are you sure you want to delete order #{order.id} and all its items? (y/n): ").strip().lower()
    if confirm == "y":
        session.delete(order)
        session.commit()
        print("Order and related items deleted.")
    else:
        print("Delete canceled.")
        session.close()
        return
    try:
        for item in order.items:
            product = item.product
            product.stock_quantity += item.quantity
        
        session.delete(order)
        session.commit()
        print(f"Order #{order.id} deleted successfully.")
    except Exception as e:
        session.rollback()
        print(f"Error deleting order: {e}")
    finally:
        session.close()


def fulfill_order():
    session = Session()
    try:
        list_orders()
        oid_input = input("Enter Order ID to fulfill: ").strip()
        oid = int(oid_input)
        order = session.get(Order, oid)
        if not order:
            print("Order not found.")
            return
        if order.status != "pending":
            print(f"Order is already '{order.status}'.")
            return

        order.status = "fulfilled"
        shipment = Shipment(order_id=order.id, delivery_status="not shipped")
        session.add(shipment)
        session.commit()
        print(f"Order #{order.id} marked as fulfilled; shipment created (ID {shipment.id}).")
    except ValueError:
        print("Invalid ID.")
    except Exception as e:
        session.rollback()
        print(f"Error fulfilling order: {e}")
    finally:
        session.close()


def track_shipments():
    session = Session()
    try:
        shipments = session.query(Shipment).order_by(Shipment.id).all()
        print("\n--- Shipments ---")
        if not shipments:
            print("  (no shipments found)\n")
        else:
            for s in shipments:
                shipped_str = s.shipped_date.strftime("%Y-%m-%d %H:%M:%S") if s.shipped_date else "N/A"
                print(f"  [{s.id}] Order #{s.order_id} - Status: {s.delivery_status}, Shipped date: {shipped_str}")
            print("")
    finally:
        session.close()


def update_shipment():
    session = Session()
    try:
        track_shipments()
        sid_input = input("Enter Shipment ID to update: ").strip()
        sid = int(sid_input)
        shipment = session.get(Shipment, sid)
        if not shipment:
            print("Shipment not found.")
            return

        print(f"Current status: {shipment.delivery_status}")
        new_status = input("New status (e.g., 'in transit', 'delivered'): ").strip()
        if not new_status:
            print("Status cannot be empty.")
            return

        shipment.delivery_status = new_status
        if new_status.lower() == "delivered":
            shipment.shipped_date = datetime.now()
        session.commit()
        print(f"Shipment #{shipment.id} status updated to '{new_status}'.")
    except ValueError:
        print("Invalid ID.")
    except Exception as e:
        session.rollback()
        print(f"Error updating shipment: {e}")
    finally:
        session.close()

def delete_shipment():
    session = Session()
    track_shipments()
    try:
        sid = int(input("Enter Shipment ID to delete: ").strip())
    except ValueError:
        print("Invalid ID.")
        session.close()
        return

    shipment = session.query(Shipment).get(sid)
    if not shipment:
        print("Shipment not found.")
        session.close()
        return

    confirm = input(f"Are you sure you want to delete shipment #{shipment.id}? (y/n): ").strip().lower()
    if confirm == "y":
        session.delete(shipment)
        session.commit()
        print("Shipment deleted.")
    else:
        print("Delete canceled.")

    session.close()



def go_back_or_exit():
    while True:
        print("\n🔁 Press [M] to return to the main menu or [E] to exit.")
        choice = input("> ").strip().lower()
        if choice == "m":
            return
        elif choice == "e":
            exit_program()
        else:
            print("❌ Invalid choice. Please enter 'M' or 'E'.")

def exit_program():
    print("\n👋 Goodbye! Thanks for using the Warehouse Simulator!")
    sys.exit()

def menu():
    print("""

🧱  Welcome to the 🏭 Warehouse Simulator 3000!
==============================================
📦 Manage Products, Orders, and Shipments with ease!

Please choose an option:
 [0]  Exit
 [1]  📋 List Products
 [2]  ➕ Add Product
 [3]  🛒 Create Order
 [4]  📦 List Orders
 [5]  ✅ Fulfill Order
 [6]  🚚 Track Shipments
 [7]  🔧 Update Shipment Status
 [8]  ✏️ Update Product
 [9]  ❌ Delete Product
 [10]  ✏️ Update Order
 [11]  ❌ Delete Order
 [12]  ❌ Delete Shipment
""")

def main():
    actions = {
        "0": exit_program,
        "1": list_products,
        "2": add_product,
        "3": create_order,
        "4": list_orders,
        "5": fulfill_order,
        "6": track_shipments,
        "7": update_shipment,
        "8": update_product,
        "9": delete_product,
        "10": update_order,
        "11": delete_order,
        "12": delete_shipment,
    }

    while True:
        menu()
        choice = input("👉 Enter your choice: ").strip()
        action = actions.get(choice)
        if action:
            action()
            go_back_or_exit()
        else:
            print("❌ Invalid option! Please choose a number from the menu.")


if __name__ == "__main__":
    main()

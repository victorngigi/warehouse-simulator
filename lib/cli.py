import sys
from lib.models import Session, Product, Order, OrderItem, Shipment
from lib.helpers import print_products, print_orders, get_product_by_sku, get_order_by_id, get_product_by_id
from datetime import datetime


def get_user_input(prompt_message, type=str, allow_empty=False, options=None):
  
    while True:
        user_input = input(f"✨ {prompt_message}: ").strip()
        if not user_input and allow_empty:
            return None
        if not user_input and not allow_empty:
            print("❗ Input cannot be empty. Please try again.")
            continue

        try:
            if type is int:
                value = int(user_input)
            elif type is float:
                value = float(user_input)
            else: 
                value = user_input

            if options and value.lower() not in [opt.lower() for opt in options]:
                print(f"❌ Invalid choice. Please select from {', '.join(options)}.")
                continue

            return value
        except ValueError:
            print(f"❌ Invalid input. Please enter a valid {type.__name__}.")

def confirm_action(prompt_message):
    """Asks for a y/n confirmation with better feedback."""
    while True:
        response = input(f"❓ {prompt_message} (y/n): ").strip().lower()
        if response in ('y', 'yes'):
            return True
        elif response in ('n', 'no'):
            print("🚫 Action canceled.")
            return False
        else:
            print("🤔 Invalid response. Please type 'y' for yes or 'n' for no.")


def list_products():
    session = Session()
    try:
        print_products(session)
    finally:
        session.close()

def add_product():
    session = Session()
    try:
        print("\n--- ➕ Adding a New Product ---")
        name = get_user_input("Enter product name", allow_empty=False)
        sku = get_user_input("Enter unique SKU", allow_empty=False)

        if get_product_by_sku(session, sku):
            print(f"❌ Oops! A product with SKU '{sku}' already exists. Try a different SKU.")
            return

        price = get_user_input("Enter price per unit (e.g., 25.50)", type=float)
        qty = get_user_input("Enter initial quantity in stock", type=int)

        if price is None or qty is None:
             print("Operation canceled due to invalid input.")
             return

        if price <= 0:
            print("❌ Price must be greater than zero. Product not added.")
            return
        if qty < 0:
            print("❌ Quantity cannot be negative. Product not added.")
            return

        product = Product(
            name=name,
            sku=sku,
            price_per_unit=price,
            stock_quantity=qty
        )
        session.add(product)
        session.commit()
        print(f"✅ Success! Product '{product.name}' (ID: {product.id}) added to inventory!\n")
    except Exception as e:
        session.rollback()
        print(f"❗ An unexpected error occurred while adding the product: {e}. Please try again.")
    finally:
        session.close()

def update_product():
    session = Session()
    print("\n--- ✏️ Updating a Product ---")
    list_products()
    pid = get_user_input("Enter the ID of the product you want to update", type=int)

    if pid is None:
        return

    product = get_product_by_id(session, pid)
    if not product:
        print(f"🔍 Product with ID {pid} not found. Please check the ID and try again.")
        session.close()
        return

    print(f"\n--- Updating Product: {product.name} (ID: {product.id}) ---")

    new_name = get_user_input(f"Current name: {product.name}. Enter new name (or leave blank to keep)", allow_empty=True)
    if new_name is not None and new_name != "":
        product.name = new_name
        print(f"Updated name to: {product.name}")

    new_price = get_user_input(f"Current price: KSH-{product.price_per_unit:.2f}. Enter new price (or leave blank to keep)", type=float, allow_empty=True)
    if new_price is not None and new_price != "":
        if new_price <= 0:
            print("❌ Price must be greater than zero. Price update skipped.")
        else:
            product.price_per_unit = new_price
            print(f"Updated price to: KSH-{product.price_per_unit:.2f}")

    new_stock = get_user_input(f"Current stock quantity: {product.stock_quantity}. Enter new stock quantity (or leave blank to keep)", type=int, allow_empty=True)
    if new_stock is not None and new_stock != "":
        if new_stock < 0:
            print("❌ Stock quantity cannot be negative. Stock update skipped.")
        else:
            product.stock_quantity = new_stock
            print(f"Updated stock quantity to: {product.stock_quantity}")

    try:
        session.commit()
        print(f"✅ Product '{product.name}' (ID: {product.id}) updated successfully!\n")
    except Exception as e:
        session.rollback()
        print(f"❗ An error occurred during product update: {e}. Changes have been rolled back.")
    finally:
        session.close()

def delete_product():
    session = Session()
    print("\n--- ❌ Deleting a Product ---")
    list_products()
    pid = get_user_input("Enter the ID of the product you want to delete", type=int)

    if pid is None:
        return

    product = get_product_by_id(session, pid)
    if not product:
        print(f"🔍 Product with ID {pid} not found. Nothing to delete.")
        session.close()
        return

    linked_items_count = session.query(OrderItem).filter_by(product_id=pid).count()
    if linked_items_count > 0:
        print(f"🛑 Cannot delete '{product.name}'. It's currently linked to {linked_items_count} existing order item(s).")
        print("To delete this product, you must first remove it from all orders.")
        session.close()
        return

    if confirm_action(f"Are you absolutely sure you want to PERMANENTLY delete product '{product.name}' (ID: {product.id})? This cannot be undone"):
        try:
            session.delete(product)
            session.commit()
            print(f"🗑️ Product '{product.name}' has been successfully deleted.\n")
        except Exception as e:
            session.rollback()
            print(f"❗ Error deleting product: {e}. Changes rolled back.")
        finally:
            session.close()
    else:
        session.close()


def create_order():
    session = Session()
    try:
        print("\n--- 🛒 Creating a New Order ---")
        customer = get_user_input("Enter customer name", allow_empty=False)
        if customer is None:
            print("Order creation canceled.")
            return

        order = Order(customer_name=customer, order_date=datetime.now(), status="pending")
        session.add(order)
        session.commit()

        print(f"\n🎉 Order #{order.id} for '{customer}' initiated! Let's add some items...")

        items_added = False
        while True:
            list_products()
            print("Current Order Items:")
            if order.order_items:
                for item in order.order_items:
                    print(f"  - {item.quantity} x {item.product.name} (KSH-{item.unit_price:.2f} each)")
            else:
                print("  (No items added yet.)")

            choice = get_user_input("Enter Product ID to add (or type '0' to finalize order, 'C' to cancel order)", type=str).upper()

            if choice == "0":
                break
            elif choice == "C":
                confirm_cancel = confirm_action(f"Are you sure you want to cancel order #{order.id}? This will remove all items and the order.")
                if confirm_cancel:
                    for item in order.order_items:
                        product = get_product_by_id(session, item.product_id)
                        if product:
                            product.stock_quantity += item.quantity
                            session.add(product)
                    session.delete(order)
                    session.commit()
                    print(f"❌ Order #{order.id} canceled and stock returned.\n")
                    return
                else:
                    print("👍 Continuing to add items to the current order.")
                    continue

            try:
                pid = int(choice)
            except ValueError:
                print("❌ Invalid input. Please enter a valid Product ID, '0' to finish, or 'C' to cancel.")
                continue

            prod = get_product_by_id(session, pid)
            if not prod:
                print(f"🔍 Product with ID {pid} not found. Please choose from the list.")
                continue

            qty = get_user_input(f"How many units of '{prod.name}' (available: {prod.stock_quantity})?", type=int)
            if qty is None:
                continue

            if qty <= 0:
                print("❌ Quantity must be greater than zero. Please try again.")
                continue
            if prod.stock_quantity < qty:
                print(f"⚠️ Insufficient stock! Only {prod.stock_quantity} units of '{prod.name}' are available. Please enter a lower quantity.")
                continue

            existing_item = next((item for item in order.order_items if item.product_id == prod.id), None)
            if existing_item:
                existing_item.quantity += qty
                session.add(existing_item)
                print(f"🔄 Updated quantity for {prod.name} in order #{order.id} to {existing_item.quantity}.")
            else:
                item = OrderItem(
                    order_id=order.id,
                    product_id=prod.id,
                    quantity=qty,
                    unit_price=prod.price_per_unit
                )
                session.add(item)
                order.order_items.append(item)
                print(f"✅ Added {qty} x '{prod.name}' to order #{order.id}.")

            prod.stock_quantity -= qty
            session.add(prod)

            session.commit()

            items_added = True

        if not items_added:
            session.delete(order)
            session.commit()
            print("⚠️ No items added to the order. Order canceled.\n")
        else:
            print(f"\n✨ Order #{order.id} for '{customer}' successfully created with {len(order.order_items)} unique item(s)! Ready for fulfillment.\n")
    except Exception as e:
        session.rollback()
        print(f"❗ An unexpected error occurred while creating the order: {e}. Order creation rolled back.")
    finally:
        session.close()

def list_orders():
    session = Session()
    try:
        print_orders(session)
    finally:
        session.close()

def update_order():
    session = Session()
    print("\n--- ✏️ Updating an Order ---")
    list_orders()
    oid = get_user_input("Enter the ID of the order you want to update", type=int)

    if oid is None:
        return

    order = get_order_by_id(session, oid)
    if not order:
        print(f"🔍 Order with ID {oid} not found. Please check the ID and try again.")
        session.close()
        return

    print(f"\n--- Updating Order: #{order.id} for '{order.customer_name}' ---")

    new_customer = get_user_input(f"Current customer: {order.customer_name}. Enter new customer name (or leave blank to keep)", allow_empty=True)
    if new_customer is not None and new_customer != "":
        order.customer_name = new_customer
        print(f"🚨 Updated customer name to: {new_customer}")

    valid_statuses = ["pending", "fulfilled", "cancelled"]
    print(f"🚨 Current status: {order.status}. Valid statuses: {', '.join(valid_statuses)}")
    new_status = get_user_input("Enter new status (e.g., 'pending', 'fulfilled', 'cancelled') or leave blank to keep", allow_empty=True, options=valid_statuses)
    if new_status is not None and new_status != "":
        order.status = new_status
        print(f"🚨 Updated order status to: {order.status}")

    try:
        session.commit()
        print(f"✅ Order #{order.id} updated successfully!\n")
    except Exception as e:
        session.rollback()
        print(f"❗ An error occurred during order update: {e}. Changes have been rolled back.")
    finally:
        session.close()

def delete_order():
    session = Session()
    print("\n--- ❌ Deleting an Order ---")
    list_orders()
    oid = get_user_input("Enter the ID of the order you want to delete", type=int)

    if oid is None:
        return

    order = get_order_by_id(session, oid)
    if not order:
        print(f"🔍 Order with ID {oid} not found. Nothing to delete.")
        session.close()
        return

    if confirm_action(f"‼️ Are you absolutely sure you want to PERMANENTLY delete order #{order.id} (for '{order.customer_name}') and return its items to stock? This cannot be undone."):
        try:
            for item in order.order_items:
                product = get_product_by_id(session, item.product_id)
                if product:
                    product.stock_quantity += item.quantity
                    session.add(product)

            session.delete(order)
            session.commit()
            print(f"🗑️ Order #{order.id} for '{order.customer_name}' has been successfully deleted and stock returned.\n")
        except Exception as e:
            session.rollback()
            print(f"❗ Error deleting order: {e}. Changes rolled back.")
        finally:
            session.close()
    else:
        session.close()

def fulfill_order():
    session = Session()
    try:
        print("\n--- ✅ Fulfilling an Order ---")
        list_orders()
        oid = get_user_input("Enter the Order ID to fulfill", type=int)

        if oid is None:
            return

        order = get_order_by_id(session, oid)
        if not order:
            print(f"🔍 Order with ID {oid} not found. Please check the ID.")
            return

        if order.status == "fulfilled":
            print(f"🚀 Order #{order.id} is already marked as 'fulfilled'. No action needed.")
            return
        elif order.status == "cancelled":
            print(f"🚫 Order #{order.id} is 'cancelled' and cannot be fulfilled.")
            return

        all_stock_available = True
        for item in order.order_items:
            product = get_product_by_id(session, item.product_id)
            if not product or product.stock_quantity < item.quantity:
                print(f"⚠️ Insufficient stock for '{item.product.name}' (needed: {item.quantity}, available: {product.stock_quantity if product else 'N/A'}). Cannot fulfill order.")
                all_stock_available = False
                break

        if not all_stock_available:
            print("🛑 Order cannot be fulfilled due to insufficient stock for some items.")
            return

        if confirm_action(f"Confirm fulfillment for Order #{order.id} (Customer: '{order.customer_name}')?"):
            order.status = "fulfilled"
            for item in order.order_items:
                product = get_product_by_id(session, item.product_id)
                product.stock_quantity -= item.quantity
                session.add(product)

            shipment = Shipment(order_id=order.id, delivery_status="not shipped")
            session.add(shipment)
            session.commit()
            print(f"🎉 Order #{order.id} successfully fulfilled! A new shipment (ID: {shipment.id}) has been created.\n")
        else:
            print("🚨 Order fulfillment canceled.")

    except ValueError:
        print("❌ Invalid input. Please enter a valid Order ID.")
    except Exception as e:
        session.rollback()
        print(f"❗ An unexpected error occurred while fulfilling the order: {e}. Please try again.")
    finally:
        session.close()


def track_shipments():
    session = Session()
    try:
        shipments = session.query(Shipment).order_by(Shipment.id).all()
        print("\n--- 🚚 Shipment Tracking ---")
        if not shipments:
            print(" (No shipments recorded yet. Fulfill an order to see one here!)\n")
        else:
            print("ID | Order ID | Delivery Status | Shipped Date")
            print("---|----------|-----------------|-------------------")
            for s in shipments:
                shipped_str = s.shipped_date.strftime("%Y-%m-%d %H:%M:%S") if s.shipped_date else "Pending Dispatch"
                print(f"{str(s.id).ljust(2)} | {str(s.order_id).ljust(8)} | {s.delivery_status.ljust(15)} | {shipped_str}")
            print("----------------------------------------------------\n")
    finally:
        session.close()

def update_shipment():
    session = Session()
    print("\n--- 🔧 Updating Shipment Status ---")
    track_shipments()
    sid = get_user_input("Enter the Shipment ID to update", type=int)

    if sid is None:
        return

    shipment = session.get(Shipment, sid)
    if not shipment:
        print(f"🔍 Shipment with ID {sid} not found. Please check the ID.")
        session.close()
        return

    valid_statuses = ["not shipped", "in transit", "delivered", "returned", "on hold"]
    print(f"Current status for Shipment #{shipment.id}: {shipment.delivery_status}")
    print(f"Available statuses: {', '.join(valid_statuses)}")

    new_status = get_user_input("Enter new delivery status (e.g., 'in transit', 'delivered')", options=valid_statuses).lower()
    if new_status is None:
        print("🚨 Shipment status update canceled.")
        return

    if new_status == shipment.delivery_status:
        print("🚨 Status is already the same. No changes made.")
        session.close()
        return

    shipment.delivery_status = new_status
    if new_status == "delivered" and not shipment.shipped_date:
        shipment.shipped_date = datetime.now()
        print("📦 Automatically setting 'Shipped Date' to now as status is 'delivered'.")
    elif new_status != "delivered" and shipment.shipped_date and confirm_action("Do you want to clear the 'Shipped Date' (e.g., if re-routing)?"):
        shipment.shipped_date = None
        print("🚨 Shipped Date cleared.")

    try:
        session.commit()
        print(f"✅ Shipment #{shipment.id} status successfully updated to '{new_status}'!\n")
    except Exception as e:
        session.rollback()
        print(f"❗ Error updating shipment: {e}. Changes rolled back.")
    finally:
        session.close()

def delete_shipment():
    session = Session()
    print("\n--- ❌ Deleting a Shipment ---")
    track_shipments()
    sid = get_user_input("Enter the Shipment ID to delete", type=int)

    if sid is None:
        return

    shipment = session.query(Shipment).get(sid)
    if not shipment:
        print(f"🔍 Shipment with ID {sid} not found. Nothing to delete.")
        session.close()
        return

    if confirm_action(f"Are you absolutely sure you want to PERMANENTLY delete shipment #{shipment.id}? This cannot be undone."):
        try:
            session.delete(shipment)
            session.commit()
            print(f"🗑️ Shipment #{shipment.id} has been successfully deleted.\n")
        except Exception as e:
            session.rollback()
            print(f"❗ Error deleting shipment: {e}. Changes rolled back.")
        finally:
            session.close()
    else:
        session.close()


def go_back_or_exit():
    while True:
        print("\n---")
        print("Want to do more? 🤔")
        print("🔁 Press [M] to return to the main menu.")
        print("👋 Press [E] to exit the Warehouse Simulator.")
        choice = input("Your command: ").strip().lower()
        if choice == "m":
            print("\nReturning to main menu...\n")
            return
        elif choice == "e":
            exit_program()
        else:
            print("❌ Invalid choice. Please enter 'M' or 'E'.")

def exit_program():
    print("\n🎉 Mission complete! Goodbye from the Warehouse Simulator! See you next time! 👋\n")
    sys.exit()

def menu():
    print("""

==============================================
🧱 Welcome to the 🏭 Warehouse Simulator 3000!
==============================================
📦 Master your inventory, orders, and shipments with ease!

What's on your agenda today? Choose an option:
---
[0] 👋 Exit the Simulator
---
[1] 📋 List Products (See what's in stock!)
[2] ➕ Add a New Product (Grow your inventory!)
[3] ✏️ Update an Existing Product (Adjust details or stock levels)
[4] ❌ Delete a Product (Remove items from inventory)
---
[5] 🛒 Create a New Order (Start a customer order)
[6] 📦 List All Orders (View all placed orders)
[7] ✅ Fulfill an Order (Prepare orders for dispatch)
[8] ✏️ Update an Order (Modify customer name or status)
[9] ❌ Delete an Order (Cancel and remove an order)
---
[10] 🚚 Track Shipments (Monitor delivery progress)
[11] 🔧 Update Shipment Status (Change delivery status)
[12] ❌ Delete a Shipment (Remove a shipment record)
---
""")

def main():
    actions = {
        "0": exit_program,
        "1": list_products,
        "2": add_product,
        "3": update_product,  
        "4": delete_product,  
        "5": create_order,    
        "6": list_orders,     
        "7": fulfill_order,   
        "8": update_order,    
        "9": delete_order,    
        "10": track_shipments, 
        "11": update_shipment, 
        "12": delete_shipment, 
    }

    while True:
        menu()
        choice = input("🚀 Your command, warehouse manager: ").strip()
        action = actions.get(choice)
        if action:
            action()
            go_back_or_exit()
        else:
            print("🚫 Invalid choice! Please enter a number from the menu. Let's get this right! 🧐")


if __name__ == "__main__":
    main()
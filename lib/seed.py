#lib/seed.py

from lib.models import Session, Product, Order, OrderItem, Shipment
from datetime import datetime

def seed_database():
    """
    Populates the database with sample data for products, orders, order items, and shipments.
    It clears existing data before adding new records.
    """
    session = Session()
    try:
        print("--- 🌱 Starting database seeding process ---")

        print("\n🗑️ Clearing all existing data from tables...")
        session.query(Shipment).delete()
        session.query(OrderItem).delete()
        session.query(Order).delete()
        session.query(Product).delete()
        session.commit()
        print("✅ All previous data successfully deleted.")

        print("\n➕ Adding sample products to inventory...")
        products_data = [
            {"name": "Wireless Ergonomic Mouse", "sku": "WM-ERGO-001", "price_per_unit": 2500.00, "stock_quantity": 100},
            {"name": "Mechanical Gaming Keyboard", "sku": "KB-MECH-G", "price_per_unit": 8500.00, "stock_quantity": 50},
            {"name": "Ultra HD 4K Monitor 27''", "sku": "MON-UHD-27", "price_per_unit": 35000.00, "stock_quantity": 30},
            {"name": "USB-C Hub 7-in-1", "sku": "HUB-USBC-7", "price_per_unit": 1800.00, "stock_quantity": 200},
            {"name": "Noise-Cancelling Headphones", "sku": "HP-NC-AUDIO", "price_per_unit": 12000.00, "stock_quantity": 75},
            {"name": "External SSD 1TB", "sku": "SSD-EXT-1TB", "price_per_unit": 9000.00, "stock_quantity": 60},
            {"name": "Webcam Full HD 1080p", "sku": "CAM-HD-1080", "price_per_unit": 4000.00, "stock_quantity": 90},
            {"name": "Portable Power Bank 20000mAh", "sku": "PB-20K-MAH", "price_per_unit": 3000.00, "stock_quantity": 150}
        ]
        seeded_products = []
        for p_data in products_data:
            product = Product(**p_data)
            session.add(product)
            seeded_products.append(product)
        session.commit() 
        print(f"✅ Added {len(seeded_products)} products.")

        print("\n🛒 Adding sample orders and their items...")

      
        order1 = Order(customer_name="Jane Doe", order_date=datetime(2025, 5, 20, 10, 30), status="fulfilled")
        session.add(order1)
        session.commit() 

        
        qty1_1 = 2
        seeded_products[0].stock_quantity -= qty1_1 
        order_item1_1 = OrderItem(order_id=order1.id, product_id=seeded_products[0].id, quantity=qty1_1, unit_price=seeded_products[0].price_per_unit)
        session.add(order_item1_1)
        
        qty1_2 = 1
        seeded_products[2].stock_quantity -= qty1_2 
        order_item1_2 = OrderItem(order_id=order1.id, product_id=seeded_products[2].id, quantity=qty1_2, unit_price=seeded_products[2].price_per_unit)
        session.add(order_item1_2)

        order2 = Order(customer_name="John Smith", order_date=datetime(2025, 5, 22, 14, 00), status="pending")
        session.add(order2)
        session.commit()

        
        qty2_1 = 1
        seeded_products[1].stock_quantity -= qty2_1 
        order_item2_1 = OrderItem(order_id=order2.id, product_id=seeded_products[1].id, quantity=qty2_1, unit_price=seeded_products[1].price_per_unit)
        session.add(order_item2_1)
        
        qty2_2 = 3
        seeded_products[3].stock_quantity -= qty2_2 
        order_item2_2 = OrderItem(order_id=order2.id, product_id=seeded_products[3].id, quantity=qty2_2, unit_price=seeded_products[3].price_per_unit)
        session.add(order_item2_2)

        order3 = Order(customer_name="Alice Brown", order_date=datetime(2025, 5, 25, 9, 00), status="cancelled")
        session.add(order3)
        session.commit()

        
        qty3_1 = 1
        order_item3_1 = OrderItem(order_id=order3.id, product_id=seeded_products[4].id, quantity=qty3_1, unit_price=seeded_products[4].price_per_unit)
        session.add(order_item3_1)

        order4 = Order(customer_name="Bob White", order_date=datetime(2025, 5, 28, 16, 45), status="fulfilled")
        session.add(order4)
        session.commit()

        
        qty4_1 = 1
        seeded_products[5].stock_quantity -= qty4_1
        order_item4_1 = OrderItem(order_id=order4.id, product_id=seeded_products[5].id, quantity=qty4_1, unit_price=seeded_products[5].price_per_unit)
        session.add(order_item4_1)
       
        qty4_2 = 1
        seeded_products[6].stock_quantity -= qty4_2
        order_item4_2 = OrderItem(order_id=order4.id, product_id=seeded_products[6].id, quantity=qty4_2, unit_price=seeded_products[6].price_per_unit)
        session.add(order_item4_2)
       
        qty4_3 = 2
        seeded_products[7].stock_quantity -= qty4_3
        order_item4_3 = OrderItem(order_id=order4.id, product_id=seeded_products[7].id, quantity=qty4_3, unit_price=seeded_products[7].price_per_unit)
        session.add(order_item4_3)

        session.commit() 
        print(f"✅ Added {session.query(Order).count()} orders and their items.")

        
        print("\n🚚 Adding sample shipments...")

       
        shipment1 = Shipment(order_id=order1.id, delivery_status="delivered", shipped_date=datetime(2025, 5, 21, 9, 00))
        session.add(shipment1)

        
        shipment2 = Shipment(order_id=order4.id, delivery_status="in transit", shipped_date=datetime(2025, 5, 29, 10, 00))
        session.add(shipment2)

        session.commit()
        print(f"✅ Added {session.query(Shipment).count()} shipments.")

        print("\n--- 🎉 Database seeding complete! You're ready to go! ---")

    except Exception as e:
        session.rollback()
        print(f"\n❌ An error occurred during seeding: {e}. All changes have been rolled back.")
    finally:
        session.close()


if __name__ == "__main__":
    seed_database()
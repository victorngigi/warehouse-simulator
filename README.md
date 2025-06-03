# Warehouse Inventory and Order Fulfillment System

## Overview

This project is a cli model implementation for managing products, orders, order items, and shipments in a warehouse inventory and order fulfillment system. It uses SQLAlchemy ORM with SQLite as the database.

---

## Features

- Manage products with SKU, stock quantity, and pricing.
- Create and track customer orders with multiple order items.
- Maintain order statuses: pending, fulfilled, and cancelled.
- Track shipment details including shipping date and delivery status.
- Automatic timestamp updates for records.
- Data integrity enforced with constraints and cascade deletes.

---

## Technologies Used

- Python 3.x
- SQLAlchemy ORM
- SQLite database
- datetime module for timestamps

---

## Database Models

### Product
- `id` (Primary Key)  
- `name` (String, required)  
- `sku` (String, unique, required)  
- `stock_quantity` (Integer, required)  
- `price_per_unit` (Float, required)  
- `updated_at` (DateTime, auto-updated)  

### Order
- `id` (Primary Key)  
- `customer_name` (String, required)  
- `order_date` (DateTime, defaults to current time)  
- `status` (Enum: pending, fulfilled, cancelled)  
- `updated_at` (DateTime, auto-updated)  

### OrderItem
- `id` (Primary Key)  
- `order_id` (ForeignKey to Order, required)  
- `product_id` (ForeignKey to Product, required)  
- `quantity` (Integer, required, must be > 0)  
- `unit_price` (Float, required)  

### Shipment
- `id` (Primary Key)  
- `order_id` (ForeignKey to Order, required)  
- `shipped_date` (DateTime, nullable)  
- `delivery_status` (Enum: not shipped, in transit, delivered)  
- `updated_at` (DateTime, auto-updated)  

---

## Usage

1. Create a SQLAlchemy engine and session:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///db/warehouse.db")
Session = sessionmaker(bind=engine)
session = Session()
```

2. Create tables (run once):

```python
Base.metadata.create_all(engine)
```

3. Perform CRUD operations using session:  
   - Add products, create orders with order items, and track shipments.  
   - Use model methods like `product.is_in_stock(quantity)` and `order.total_amount()` for business logic.

---

## Naming Conventions

- Constraints and indexes use consistent naming conventions for easier database management.

---

## Notes

- Cascading deletes ensure related records are cleaned up when orders or products are deleted.  
- Enum types enforce valid status values.  
- Check constraints maintain data integrity (e.g., quantity > 0).

---

## License

This project is open source and free to use.

---

## Author

Created by Victor Kinyanjui Ngigi for Moringa School Phase 3

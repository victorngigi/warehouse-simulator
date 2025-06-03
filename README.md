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
- Alembic for migrations

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

## Setup Instructions

1. Clone the repository:

   ```
   git clone <your-repository-url>
   cd <your-repository-folder>
   ```

2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate    # On Linux/macOS
   .\venv\Scripts\activate     # On Windows
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Initialize the database:

   ```
   python -m alembic upgrade head
   ```

## Usage

1. Activate your virtual environment (venv):

   ```
   source venv/bin/activate    # On Linux/macOS
   .\venv\Scripts\activate     # On Windows
   ```

2. Run the application from the project root using the module syntax:

   ```
   python -m lib.cli
   ```

3. Follow the CLI prompts to interact with the warehouse inventory and order fulfillment system.


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

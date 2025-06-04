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

## Database Schema

Here's a detailed look at the database schema:

| Table        | Column          | Type         | Constraints                   |
|--------------|-----------------|--------------|-------------------------------|
| `products`   | `id`            | `INTEGER`    | `PRIMARY KEY`, `NOT NULL`     |
|              | `name`          | `VARCHAR(255)`| `NOT NULL`                    |
|              | `sku`           | `VARCHAR(100)`| `UNIQUE`, `NOT NULL`          |
|              | `stock_quantity`| `INTEGER`    | `NOT NULL`                    |
|              | `price_per_unit`| `FLOAT`      | `NOT NULL`                    |
| `orders`     | `id`            | `INTEGER`    | `PRIMARY KEY`, `NOT NULL`     |
|              | `customer_name` | `VARCHAR(255)`| `NOT NULL`                    |
|              | `order_date`    | `DATETIME`   | `NOT NULL`                    |
|              | `status`        | `VARCHAR(50)`| `NOT NULL`                    |
| `order_items`| `id`            | `INTEGER`    | `PRIMARY KEY`, `NOT NULL`     |
|              | `order_id`      | `INTEGER`    | `NOT NULL`, `FOREIGN KEY` (`orders.id`)|
|              | `product_id`    | `INTEGER`    | `NOT NULL`, `FOREIGN KEY` (`products.id`)|
|              | `quantity`      | `INTEGER`    | `NOT NULL`                    |
|              | `unit_price`    | `FLOAT`      | `NOT NULL`                    |
| `shipments`  | `id`            | `INTEGER`    | `PRIMARY KEY`, `NOT NULL`     |
|              | `order_id`      | `INTEGER`    | `NOT NULL`, `FOREIGN KEY` (`orders.id`)|
|              | `shipped_date`  | `DATETIME`   |                               |
|              | `delivery_status`| `VARCHAR(50)`| `NOT NULL`                    |

**Relationships:**
- `order_items.order_id` relates to `orders.id` (Many-to-One)
- `order_items.product_id` relates to `products.id` (Many-to-One)
- `shipments.order_id` relates to `orders.id` (One-to-One)

---

## Folder Structure

```Bash
warehouse-simulator
├── Pipfile
├── Pipfile.lock
├── README.md
├── alembic.ini
├── db
│   └── warehouse.db
├── lib
│   ├── cli.py
│   ├── debug.py
│   ├── helpers.py
│   └── models
│       ├── init.py
│       └── models.py
├── migrations
│   ├── README
│   ├── env.py
│   └── script.py.mako
└── requirements.txt
```

## Setup Instructions

1. Clone the repository:

   ```Bash
   git clone <your-repository-url>
   cd <your-repository-folder>
   ```

2. Install dependencies and create the virtual environment (if it doesn't exist):

   ```Bash
   pipenv install
   ```
   _This command will automatically create a virtual environment for your project (if one doesn't already exist), install the dependencies listed in your Pipfile, and synchronize them with Pipfile.lock._

3. Initialize the database:

   ```Bash
   python -m alembic upgrade head
   ```
   

## Usage

1. Run the application using Pipenv:

   ```Bash
   pipenv run python -m lib.cli
   ```
   _This command executes python -m lib.cli directly within the project's virtual environment managed by Pipenv, without needing to manually activate it._

2. If you want to enter the virtual environment's shell to run multiple commands or for development:

   ```Bash
   pipenv shell
   ```
 _Once inside, your shell prompt will change, indicating the virtual environment is active. You can then run commands like ```python -m lib.cli``` or ```alembic upgrade head``` directly without ```pipenv run```_
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

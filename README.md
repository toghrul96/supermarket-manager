# Supermarket Manager

**Supermarket Manager** is a desktop application built with PySide6 that helps you easily manage inventory, checkout, reports, and user roles. It offers a clean interface, role-based access control, and sales data displayed through tables. Data is stored using CSV files for simple management.

---

## Features

- **User Login System** with role-based access (e.g., Manager, Cashier)
- **Checkout Interface** with barcode entry, real-time price calculations, and support for discounts and promotions
- **Inventory Management** with item addition, deletion, search and stock updates
- **Sales Reporting** with dynamic tables that display Sales History, Sales Summary, Top Products, and Top Users by date
- **User Management** with user account addition, deletion, and management
- **CSV-based Data Handling** for inventory, sales, and users

---

## Technologies Used

- **Python 3**
- **[PySide6](https://doc.qt.io/qtforpython/)** – GUI framework
- **Qt Designer** – Used to visually design `.ui` files for all UI screens
- **bcrypt** – For secure password hashing and authentication

---

## Sample Data

The `data/` folder contains sample CSV files:
- `inventory_data.csv`
- `sales_data.csv`
- `user_data.csv`

---

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/toghrul96/supermarket-manager.git
   cd supermarket-manager
   ```

2. **Install Dependencies**
    ```bash
   pip install -r requirements.txt
   ```

3. **Launch the App**
    ```bash
   python log_in.py
   ```

---

### Development Notes

To convert .ui files to Python code, run:
```bash
pyside6-uic ui/main.ui -o ui/ui_main.py
```

To compile the Qt resource file (.qrc) to Python, run:

```bash
pyside6-rcc icons/resource.qrc -o resource_rc.py
```







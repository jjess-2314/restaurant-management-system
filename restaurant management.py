import pyodbc

# Database Connection
class DBConnection:
    def __init__(self):
        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                                   'SERVER=localhost;'  
                                   'DATABASE=RestaurantDB;'
                                   'Trusted_Connection=yes;')
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()

    def fetch_all(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()

# MenuItem Class
class MenuItem:
    def __init__(self, item_id=None, name=None, price=None):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.is_available = True if item_id is None else self.get_availability(item_id)

    def get_availability(self, item_id):
        db = DBConnection()
        result = db.fetch_one("SELECT is_available FROM MenuItems WHERE item_id = ?", (item_id,))
        db.close()
        return result[0] if result else True

    def mark_unavailable(self):
        db = DBConnection()
        db.execute_query("UPDATE MenuItems SET is_available = 0 WHERE item_id = ?", (self.item_id,))
        db.close()
        self.is_available = False

    def mark_available(self):
        db = DBConnection()
        db.execute_query("UPDATE MenuItems SET is_available = 1 WHERE item_id = ?", (self.item_id,))
        db.close()
        self.is_available = True

    def save_to_db(self):
        db = DBConnection()
        db.execute_query("INSERT INTO MenuItems (item_id, name, price, is_available) VALUES (?, ?, ?, ?)",
                         (self.item_id, self.name, self.price, self.is_available))
        db.close()

    def __str__(self):
        status = "Available" if self.is_available else "Not Available"
        return f"MenuItem[ID={self.item_id}, Name={self.name}, Price={self.price}, Status={status}]"

# Customer Class
class Customer:
    def __init__(self, customer_id=None, name=None):
        self.customer_id = customer_id
        self.name = name
        self.orders = self.get_orders(customer_id) if customer_id else []

    def get_orders(self, customer_id):
        db = DBConnection()
        result = db.fetch_all("SELECT m.item_id, m.name, m.price FROM MenuItems m "
                              "JOIN Orders o ON m.item_id = o.item_id "
                              "WHERE o.customer_id = ?", (customer_id,))
        db.close()
        return [MenuItem(item_id=row[0], name=row[1], price=row[2]) for row in result]

    def place_order(self, item):
        if item.is_available:
            db = DBConnection()
            db.execute_query("INSERT INTO Orders (customer_id, item_id) VALUES (?, ?)",
                             (self.customer_id, item.item_id))
            item.mark_unavailable()
            db.close()
            print(f"{self.name} ordered '{item.name}'.")
        else:
            print(f"Sorry, '{item.name}' is not available.")

    def cancel_order(self, item):
        db = DBConnection()
        db.execute_query("DELETE FROM Orders WHERE customer_id = ? AND item_id = ?",
                         (self.customer_id, item.item_id))
        item.mark_available()
        db.close()
        print(f"{self.name} canceled order for '{item.name}'.")

    def save_to_db(self):
        db = DBConnection()
        db.execute_query("INSERT INTO Customers (customer_id, name) VALUES (?, ?)",
                         (self.customer_id, self.name))
        db.close()

    def __str__(self):
        return f"Customer[ID={self.customer_id}, Name={self.name}, Orders={len(self.orders)}]"

# Restaurant Class
class Restaurant:
    def __init__(self, name):
        self.name = name
        self.db = DBConnection()

    def add_item(self, item):
        item.save_to_db()
        print(f"Added menu item '{item.name}'.")

    def remove_item(self, item_id):
        db = self.db
        db.execute_query("DELETE FROM MenuItems WHERE item_id = ?", (item_id,))
        print(f"Removed menu item with ID {item_id}.")

    def list_menu(self):
        db = self.db
        items = db.fetch_all("SELECT item_id, name, price, is_available FROM MenuItems")
        print(f"\nMenu at {self.name}:")
        for item in items:
            status = "Available" if item[3] else "Not Available"
            print(f"MenuItem[ID={item[0]}, Name={item[1]}, Price={item[2]}, Status={status}]")

    def add_customer(self, customer):
        customer.save_to_db()
        print(f"Added customer '{customer.name}'.")

    def __str__(self):
        return f"Restaurant[Name={self.name}]"

# -----------------------
# Sample Usage
if __name__ == "__main__":
    restaurant = Restaurant("City Restaurant")

    # Add Menu Items
    item1 = MenuItem(item_id=1, name="Pizza", price=250.00)
    item2 = MenuItem(item_id=2, name="Burger", price=120.00)
    restaurant.add_item(item1)
    restaurant.add_item(item2)

    # Add Customers
    customer1 = Customer(customer_id=201, name="Alice")
    customer2 = Customer(customer_id=202, name="Bob")
    restaurant.add_customer(customer1)
    restaurant.add_customer(customer2)

    # List Menu
    restaurant.list_menu()

    # Place Orders
    customer1.place_order(item1)
    customer2.place_order(item1)

    # Cancel Orders
    customer1.cancel_order(item1)
    customer2.cancel_order(item1)

    # Final Menu Status
    restaurant.list_menu()



class Item:
    def __init__(self, id, name, price, stock):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_stock(self):
        return self.stock

    def set_price(self, price):
        self.price = price

    def set_stock(self, stock):
        self.stock = stock

    def display(self):
        print(f"{self.id:<10} {self.name:<20} {self.price:<10.2f} {self.stock:<10}")

class InventoryManager:
    def __init__(self):
        self.items = []

    def add_item(self):
        id = self.get_int_input("Enter Item ID: ")
        name = input("Enter Item Name: ")
        price = self.get_float_input("Enter Price: ")
        stock = self.get_int_input("Enter Stock Quantity: ")
        self.items.append(Item(id, name, price, stock))
        print("Item added successfully!")

    def update_item(self):
        id = self.get_int_input("Enter Item ID to update: ")
        item = self.search_item(id)
        if item is None:
            print("Item not found!")
            return
        print("1. Update Price")
        print("2. Update Stock")
        choice = self.get_int_input("Choose an option: ")
        if choice == 1:
            new_price = self.get_float_input("Enter new price: ")
            item.set_price(new_price)
            print("Price updated successfully!")
        elif choice == 2:
            new_stock = self.get_int_input("Enter new stock quantity: ")
            item.set_stock(new_stock)
            print("Stock updated successfully!")
        else:
            print("Invalid option!")

    def view_inventory(self):
        if not self.items:
            print("No items in inventory.")
            return
        print("\n---------------------- INVENTORY ----------------------")
        print(f"{'ID':<10} {'NAME':<20} {'PRICE':<10} {'STOCK':<10}")
        print("--------------------------------------------------------")
        for item in self.items:
            item.display()
        print("--------------------------------------------------------\n")

    def generate_bill(self):
        cart = {}
        while True:
            id = self.get_int_input("Enter Item ID to purchase (0 to finish): ")
            if id == 0:
                break
            item = self.search_item(id)
            if item is None:
                print("Item not found.")
                continue
            qty = self.get_int_input("Enter quantity: ")
            if qty > item.get_stock():
                print("Not enough stock!")
                continue
            cart[item] = cart.get(item, 0) + qty
            item.set_stock(item.get_stock() - qty)
            print("Item added to cart!")
        if not cart:
            print("No items purchased.")
            return
        print("\n-------------------------- BILL --------------------------")
        print(f"{'ITEM':<20} {'QTY':<10} {'PRICE':<10} {'TOTAL':<10}")
        print("-----------------------------------------------------------")
        grand_total = 0
        for item, qty in cart.items():
            price = item.get_price()
            total = qty * price
            grand_total += total
            print(f"{item.get_name():<20} {qty:<10} {price:<10.2f} {total:<10.2f}")
        tax = grand_total * 0.18
        final_total = grand_total + tax
        print("-----------------------------------------------------------")
        print(f"Subtotal: {grand_total:.2f}")
        print(f"GST (18%): {tax:.2f}")
        print(f"Final Total: {final_total:.2f}")
        print("-----------------------------------------------------------")
        print("Thank you for shopping!")

    def search_item(self, id):
        for item in self.items:
            if item.get_id() == id:
                return item
        return None

    def get_int_input(self, prompt=""):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Invalid input! Enter a number: ")

    def get_float_input(self, prompt=""):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Invalid input! Enter a valid number: ")

    def show_menu(self):
        while True:
            print("\n====== BILLING & INVENTORY SYSTEM ======")
            print("1. Add Item")
            print("2. Update Item")
            print("3. View Inventory")
            print("4. Generate Bill")
            print("5. Exit")
            choice = self.get_int_input("Enter choice: ")
            if choice == 1:
                self.add_item()
            elif choice == 2:
                self.update_item()
            elif choice == 3:
                self.view_inventory()
            elif choice == 4:
                self.generate_bill()
            elif choice == 5:
                print("Exiting system...")
                break
            else:
                print("Invalid choice! Try again.")

if __name__ == "__main__":
    manager = InventoryManager()
    manager.show_menu()
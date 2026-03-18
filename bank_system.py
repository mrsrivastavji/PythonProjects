import sqlite3
from getpass import getpass

class BankAccount:
    def __init__(self, account_number, holder_name, balance, pin):
        self.account_number = account_number
        self.holder_name = holder_name
        self.balance = balance
        self.pin = pin

    def get_account_number(self):
        return self.account_number

    def get_holder_name(self):
        return self.holder_name

    def get_balance(self):
        return self.balance

    def get_pin(self):
        return self.pin

    def set_balance(self, balance):
        self.balance = balance


class BankSystem:
    def __init__(self, db_name="bankdb.sqlite"):
        self.db_name = db_name
        self.initialize_database()

    def initialize_database(self):
        """Create database and accounts table if they don't exist"""
        try:
            con = sqlite3.connect(self.db_name)
            cursor = con.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    accountNumber TEXT PRIMARY KEY,
                    holderName TEXT NOT NULL,
                    balance REAL NOT NULL,
                    pin INTEGER NOT NULL
                )
            ''')
            con.commit()
            con.close()
        except Exception as e:
            print(f"DB Error: {e}")

    def connect(self):
        """Establish database connection"""
        try:
            return sqlite3.connect(self.db_name)
        except Exception as e:
            print(f"DB Error: {e}")
            return None

    def get_account(self, acc_no):
        """Retrieve account from database"""
        try:
            con = self.connect()
            cursor = con.cursor() # type: ignore
            cursor.execute("SELECT * FROM accounts WHERE accountNumber=?", (acc_no,))

            row = cursor.fetchone()
            con.close() # type: ignore

            if row:
                return BankAccount(row[0], row[1], row[2], row[3])

        except Exception as e:
            print(f"DB Error: {e}")

        return None

    def update_balance(self, acc_no, new_balance):
        """Update account balance in database"""
        try:
            con = self.connect()
            cursor = con.cursor() # type: ignore
            cursor.execute("UPDATE accounts SET balance=? WHERE accountNumber=?", (new_balance, acc_no))
            con.commit() # type: ignore
            con.close() # type: ignore
        except Exception as e:
            print(f"DB Error: {e}")

    # --------------------------------------------------------
    # MAIN FEATURES
    # --------------------------------------------------------

    def create_account(self):
        """Create a new account"""
        acc_no = input("Enter Account Number: ").strip()

        # Check if account already exists
        if self.get_account(acc_no) is not None:
            print("Account already exists!")
            return

        name = input("Enter Holder Name: ").strip()

        try:
            amount = float(input("Enter Initial Deposit: "))
        except ValueError:
            print("Invalid amount! Please enter a valid number.")
            return

        try:
            pin = int(input("Set a 4-digit PIN: "))
            if pin < 0 or pin > 9999:
                print("PIN must be a 4-digit number (0-9999)!")
                return
        except ValueError:
            print("Invalid PIN! Please enter a valid number.")
            return

        try:
            con = self.connect()
            cursor = con.cursor() # type: ignore
            cursor.execute("INSERT INTO accounts VALUES (?, ?, ?, ?)", (acc_no, name, amount, pin))
            con.commit() # type: ignore
            con.close() # type: ignore
            print("Account created successfully!")

        except Exception as e:
            print(f"DB Error: {e}")

    def deposit_money(self):
        """Deposit money into account"""
        account = self.verify_account()
        if account is None:
            return

        try:
            amt = float(input("Enter amount to deposit: "))
        except ValueError:
            print("Invalid amount! Please enter a valid number.")
            return

        if amt <= 0:
            print("Invalid amount!")
            return

        new_bal = account.get_balance() + amt
        self.update_balance(account.get_account_number(), new_bal)
        print(f"₹{amt} deposited successfully.")

    def withdraw_money(self):
        """Withdraw money from account"""
        account = self.verify_account()
        if account is None:
            return

        try:
            amt = float(input("Enter amount to withdraw: "))
        except ValueError:
            print("Invalid amount! Please enter a valid number.")
            return

        if amt <= 0 or amt > account.get_balance():
            print("Insufficient balance or invalid amount!")
            return

        new_bal = account.get_balance() - amt
        self.update_balance(account.get_account_number(), new_bal)
        print(f"₹{amt} withdrawn successfully.")

    def view_balance(self):
        """View account balance"""
        account = self.verify_account()
        if account is None:
            return

        print(f"Your current balance: ₹{account.get_balance()}")

    def verify_account(self):
        """Verify account number and PIN"""
        acc_no = input("Enter Account Number: ").strip()

        account = self.get_account(acc_no)

        if account is None:
            print("Account not found!")
            return None

        try:
            pin = int(input("Enter PIN: "))
        except ValueError:
            print("Invalid PIN! Please enter a valid number.")
            return None

        if pin != account.get_pin():
            print("Incorrect PIN!")
            return None

        return account

    def run(self):
        """Main menu loop"""
        while True:
            print("\n==== BANK ACCOUNT MANAGEMENT ====")
            print("1. Create Account")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. View Balance")
            print("5. Exit")

            try:
                choice = int(input("Choose an option: "))

                if choice == 1:
                    self.create_account()
                elif choice == 2:
                    self.deposit_money()
                elif choice == 3:
                    self.withdraw_money()
                elif choice == 4:
                    self.view_balance()
                elif choice == 5:
                    print("Thank you! Exiting system...")
                    break
                else:
                    print("Invalid choice! Try again.")

            except ValueError:
                print("Invalid input! Please enter a valid number.")


if __name__ == "__main__":
    bank = BankSystem()
    bank.run()

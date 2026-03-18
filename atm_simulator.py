class Account:
    def __init__(self, balance: float, pin: int):
        self._balance = balance
        self._pin = pin

    def verify_pin(self, entered_pin: int) -> bool:
        return self._pin == entered_pin

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount > 0:
            self._balance += amount

    def withdraw(self, amount: float) -> bool:
        if amount > 0 and amount <= self._balance:
            self._balance -= amount
            return True
        return False


class ATM:
    def __init__(self, account: Account):
        self.account = account
        self.session_active = False

    def start_session(self) -> None:
        try:
            entered_pin = int(input("Enter PIN: "))
        except ValueError:
            print("Invalid PIN format. Session terminated.")
            return

        if self.account.verify_pin(entered_pin):
            print("Login successful!")
            self.session_active = True
            self._show_menu()
        else:
            print("Incorrect PIN. Session terminated.")

    def _show_menu(self) -> None:
        while self.session_active:
            print("\n--- ATM MENU ---")
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Exit")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                print(f"Your balance: ₹{self.account.balance:.2f}")
            elif choice == "2":
                try:
                    dep_amt = float(input("Enter deposit amount: "))
                except ValueError:
                    print("Invalid amount.")
                    continue
                self.account.deposit(dep_amt)
                print("Amount deposited successfully.")
            elif choice == "3":
                try:
                    w_amt = float(input("Enter withdrawal amount: "))
                except ValueError:
                    print("Invalid amount.")
                    continue
                if self.account.withdraw(w_amt):
                    print("Withdrawal successful.")
                else:
                    print("Insufficient balance.")
            elif choice == "4":
                print("Exiting session...")
                self.session_active = False
            else:
                print("Invalid choice.")


if __name__ == "__main__":
    user_account = Account(5000.0, 1234)
    atm = ATM(user_account)
    atm.start_session()
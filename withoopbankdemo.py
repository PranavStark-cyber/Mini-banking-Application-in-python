import json
import os

CUSTOMER_FILE = "customers.txt"
ACCOUNT_FILE = "accounts.txt"
TRANSACTION_FILE = "transactions.txt"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# === File Utility ===
class FileStore:
    @staticmethod
    def load(filename):
        return json.load(open(filename)) if os.path.exists(filename) else {}

    @staticmethod
    def save(filename, data):
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

# === Core Classes ===
class Bank:
    def __init__(self):
        self.customers = FileStore.load(CUSTOMER_FILE)
        self.accounts = FileStore.load(ACCOUNT_FILE)
        self.transactions = FileStore.load(TRANSACTION_FILE)

    def save_all(self):
        FileStore.save(CUSTOMER_FILE, self.customers)
        FileStore.save(ACCOUNT_FILE, self.accounts)
        FileStore.save(TRANSACTION_FILE, self.transactions)

    def get_new_id(self):
        return str(len(self.accounts) + 1001)

    def create_customer(self):
        username = input("Enter new username: ")
        if username in self.customers:
            print("Username already exists.")
            return
        password = input("Enter password: ")
        name = input("Customer name: ")
        initial = self.get_amount("Initial deposit: ")
        if initial is None:
            return

        cid = self.get_new_id()
        self.customers[username] = {"password": password, "id": cid}
        self.accounts[cid] = {"name": name, "balance": initial}
        self.transactions[cid] = [f"Initial deposit: {initial}"]
        self.save_all()
        print(f"Customer created successfully with ID: {cid}")

    def get_amount(self, prompt):
        try:
            amt = float(input(prompt))
            if amt <= 0:
                raise ValueError
            return amt
        except ValueError:
            print("Invalid amount.")
            return None

    def deposit(self, cid):
        amt = self.get_amount("Enter amount to deposit: ")
        if amt is None:
            return
        self.accounts[cid]["balance"] += amt
        self.transactions[cid].append(f"Deposit: {amt}")
        self.save_all()
        print("Deposit successful.")

    def withdraw(self, cid):
        amt = self.get_amount("Enter amount to withdraw: ")
        if amt is None:
            return
        if amt > self.accounts[cid]["balance"]:
            print("Insufficient balance.")
            return
        self.accounts[cid]["balance"] -= amt
        self.transactions[cid].append(f"Withdrawal: {amt}")
        self.save_all()
        print("Withdrawal successful.")

    def check_balance(self, cid):
        print("Current balance:", self.accounts[cid]["balance"])

    def show_transactions(self, cid):
        print("Transaction History:")
        for t in self.transactions.get(cid, []):
            print("-", t)

    def customer_login(self):
        username = input("Username: ")
        password = input("Password: ")
        user = self.customers.get(username)
        if user and user["password"] == password:
            print("Customer login successful.")
            self.customer_menu(user["id"])
        else:
            print("Invalid credentials.")

    def admin_login(self):
        username = input("Admin username: ")
        password = input("Admin password: ")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            print("Admin login successful.")
            self.admin_menu()
        else:
            print("Invalid admin credentials.")

    # === Menus ===
    def admin_menu(self):
        while True:
            print("\n--- Admin Menu ---")
            print("1. Create Customer")
            print("2. Logout")
            choice = input("Select: ")
            if choice == "1":
                self.create_customer()
            elif choice == "2":
                break
            else:
                print("Invalid choice.")

    def customer_menu(self, cid):
        while True:
            print("\n--- Customer Menu ---")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Check Balance")
            print("4. Transaction History")
            print("5. Logout")
            choice = input("Select: ")
            if choice == "1":
                self.deposit(cid)
            elif choice == "2":
                self.withdraw(cid)
            elif choice == "3":
                self.check_balance(cid)
            elif choice == "4":
                self.show_transactions(cid)
            elif choice == "5":
                break
            else:
                print("Invalid choice.")

    def start(self):
        while True:
            print("\n--- Mini Banking System ---")
            print("1. Admin Login")
            print("2. Customer Login")
            print("3. Exit")
            choice = input("Choose: ")
            if choice == "1":
                self.admin_login()
            elif choice == "2":
                self.customer_login()
            elif choice == "3":
                print("Goodbye.")
                break
            else:
                print("Invalid option.")

# === Run ===
if __name__ == "__main__":
    bank = Bank()
    bank.start()

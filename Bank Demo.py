import os
import json

# File constants
CUSTOMER_FILE = "customers.txt"
ACCOUNT_FILE = "accounts.txt"
TRANSACTION_FILE = "transactions.txt"

# Admin credentials
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

# Load/save helpers
def load_file(filename): 
    return json.load(open(filename)) if os.path.exists(filename) else {}

def save_file(filename, data): 
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# Data
customers = load_file(CUSTOMER_FILE)
accounts = load_file(ACCOUNT_FILE)
transactions = load_file(TRANSACTION_FILE)

# Utilities
def get_new_id():
    return str(len(accounts) + 5555)

def get_positive_float(prompt):
    try:
        amt = float(input(prompt))
        if amt <= 0:
            raise ValueError
        return amt
    except ValueError:
        print("Invalid amount.")
        return None

def save_all():
    save_file(CUSTOMER_FILE, customers)
    save_file(ACCOUNT_FILE, accounts)
    save_file(TRANSACTION_FILE, transactions)

def show_balance(acc_id):
    print(f"Balance: {accounts[acc_id]['balance']}")

def show_history(acc_id):
    print("Transaction History:")
    for t in transactions.get(acc_id, []):
        print("-", t)

def transact(acc_id, is_deposit=True):
    action = "deposit" if is_deposit else "withdraw"
    amt = get_positive_float(f"Enter amount to {action}: ")
    if amt is None:
        return

    if not is_deposit and amt > accounts[acc_id]["balance"]:
        print("Insufficient funds.")
        return

    accounts[acc_id]["balance"] += amt if is_deposit else -amt
    transactions.setdefault(acc_id, []).append(f"{'Deposit' if is_deposit else 'Withdrawal'}: {amt}")
    save_all()
    print(f"{action.title()} successful.")

# Admin functions
def create_customer():
    username = input("New username: ")
    if username in customers:
        print("Username already exists.")
        return

    password = input("Password: ")
    name = input("Full name: ")
    amt = get_positive_float("Initial deposit: ")
    if amt is None:
        return

    new_id = get_new_id()
    customers[username] = {"password": password, "id": new_id}
    accounts[new_id] = {"name": name, "balance": amt}
    transactions[new_id] = [f"Initial deposit: {amt}"]
    save_all()
    print(f"Customer created with ID: {new_id}")

def list_all_customers():
    print("\n--- All Customers ---")
    for username, data in customers.items():
        acc_id = data['id']
        name = accounts.get(acc_id, {}).get("name", "Unknown")
        print(f"ID: {acc_id}, Username: {username}, Name: {name}")

# Menu dispatcher
def menu_handler(acc_id, is_admin=False):
    while True:
        print(f"\n--- {'Admin' if is_admin else 'Customer'} Menu ---")
        print("1. Deposit\n2. Withdraw\n3. Check Balance\n4. Transaction History")
        if is_admin:
            print("5. Create Customer\n6. List Customers\n7. Logout")
        else:
            print("5. Logout")

        choice = input("Select: ")

        if choice in ["1", "2", "3", "4"]:
            target_id = acc_id
            if is_admin:
                target_id = input("Enter customer ID: ")
                if target_id not in accounts:
                    print("Invalid customer ID.")
                    continue

            if choice == "1":
                transact(target_id, True)
            elif choice == "2":
                transact(target_id, False)
            elif choice == "3":
                show_balance(target_id)
            elif choice == "4":
                show_history(target_id)

        elif is_admin and choice == "5":
            create_customer()
        elif is_admin and choice == "6":
            list_all_customers()
        elif (is_admin and choice == "7") or (not is_admin and choice == "5"):
            break
        else:
            print("Invalid choice.")

# Login
def login():
    role = input("Login as admin or customer? ").strip().lower()
    uname = input("Username: ")
    pwd = input("Password: ")

    if role == "admin":
        if uname == ADMIN_USER and pwd == ADMIN_PASS:
            print("Admin login successful.")
            menu_handler("", is_admin=True)
        else:
            print("Invalid admin credentials.")

    elif role == "customer":
        user = customers.get(uname)
        if user and user["password"] == pwd:
            print("Customer login successful.")
            menu_handler(user["id"])
        else:
            print("Invalid customer credentials.")
    else:
        print("Invalid role.")

# Entry
def main():
    while True:
        print("\n--- Mini Banking System ---")
        print("1. Login\n2. Exit")
        choice = input("Choose: ")
        if choice == "1":
            login()
        elif choice == "2":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

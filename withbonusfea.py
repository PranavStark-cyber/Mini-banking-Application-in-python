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

def transfer_money(from_acc_id):
    to_acc_id = input("Enter recipient account ID: ")
    if to_acc_id not in accounts:
        print("Recipient account not found.")
        return

    amt = get_positive_float("Enter amount to transfer: ")
    if amt is None:
        return

    if accounts[from_acc_id]["balance"] < amt:
        print("Insufficient funds.")
        return

    # Perform transfer
    accounts[from_acc_id]["balance"] -= amt
    accounts[to_acc_id]["balance"] += amt

    transactions.setdefault(from_acc_id, []).append(f"Transferred {amt} to {to_acc_id}")
    transactions.setdefault(to_acc_id, []).append(f"Received {amt} from {from_acc_id}")
    save_all()
    print("Transfer successful.")

def apply_interest(rate=0.02):
    print(f"Applying {rate*100:.2f}% interest to all accounts.")
    for acc_id, acc_data in accounts.items():
        interest = acc_data["balance"] * rate
        acc_data["balance"] += interest
        transactions.setdefault(acc_id, []).append(f"Interest added: {interest:.2f}")
    save_all()
    print("Interest applied to all accounts.")

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

# Menu dispatcher
def menu_handler(acc_id, is_admin=False):
    actions = {
        "1": lambda: transact(acc_id, True),
        "2": lambda: transact(acc_id, False),
        "3": lambda: show_balance(acc_id),
        "4": lambda: show_history(acc_id),
        "5": lambda: transfer_money(acc_id)
    }

    while True:
        print(f"\n--- {'Admin' if is_admin else 'Customer'} Menu ---")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Transaction History")
        print("5. Transfer Money")
        if is_admin:
            print("6. Apply Interest")
            print("7. Create Customer")
            print("8. Logout")
        else:
            print("6. Logout")

        choice = input("Select: ")
        if choice in actions:
            actions[choice]()
        elif is_admin and choice == "6":
            apply_interest()
        elif is_admin and choice == "7":
            create_customer()
        elif (is_admin and choice == "8") or (not is_admin and choice == "6"):
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

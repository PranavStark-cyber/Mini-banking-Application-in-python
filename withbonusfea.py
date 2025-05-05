# Define file names
ADMIN_FILE = "admin.txt"
CUSTOMER_FILE = "customer.txt"
ACCOUNT_FILE = "bank_acc.txt"
USER_FILE = "user.txt"
ID_COUNTER_FILE = "id_counter.txt"
ACC_COUNTER_FILE = "acc_counter.txt"
DELETE_FILE = "delete.txt"
TRANSACTION_FILE = "transaction.txt"

# Helper functions for file operations
def read_data(filename):
    try:
        with open(filename, "r") as f:
            return eval(f.read())
    except (FileNotFoundError, SyntaxError):
        return {}

def write_data(filename, data):
    with open(filename, "w") as f:
        f.write(str(data))

def read_counter(filename):
    try:
        with open(filename, "r") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 1000

def write_counter(filename, counter):
    with open(filename, "w") as f:
        f.write(str(counter))

# Load all data
admins = read_data(ADMIN_FILE)
customers = read_data(CUSTOMER_FILE)
accounts = read_data(ACCOUNT_FILE)
users = read_data(USER_FILE)
transactions = read_data(TRANSACTION_FILE)
id_counter = read_counter(ID_COUNTER_FILE)
acc_counter = read_counter(ACC_COUNTER_FILE)

# Initialize default admin if not present
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"

# Save all
def save_all():
    write_data(ADMIN_FILE, admins)
    write_data(CUSTOMER_FILE, customers)
    write_data(ACCOUNT_FILE, accounts)
    write_data(USER_FILE, users)
    write_data(TRANSACTION_FILE, transactions)
    write_counter(ID_COUNTER_FILE, id_counter)
    write_counter(ACC_COUNTER_FILE, acc_counter)

if DEFAULT_ADMIN_USERNAME not in admins:
    admins[DEFAULT_ADMIN_USERNAME] = DEFAULT_ADMIN_PASSWORD
    save_all()


# Input utilities
def input_nonempty(prompt):
    val = input(prompt).strip()
    while not val:
        print("Input cannot be empty.")
        val = input(prompt).strip()
    return val

def input_positive_float(prompt):
    while True:
        try:
            val = float(input(prompt))
            if val <= 0:
                raise ValueError
            return val
        except ValueError:
            print("Please enter a valid positive number.")

# Core Functions
def create_customer():
    global id_counter
    username = input_nonempty("New username: ")
    if username in users:
        print("Username already exists.")
        return
    password = input_nonempty("Password: ")
    name = input_nonempty("Full Name: ")

    customer_id = f"C{id_counter}"
    id_counter += 1
    customers[customer_id] = {"name": name, "username": username}
    users[username] = {"password": password, "id": customer_id}
    print(f"Customer created with ID: {customer_id}")
    save_all()

def create_account():
    global acc_counter
    cust_id = input_nonempty("Customer ID: ")
    if cust_id not in customers:
        print("Invalid customer ID.")
        return
    amount = input_positive_float("Initial deposit: ")
    acc_id = f"A{acc_counter}"
    acc_counter += 1
    accounts[acc_id] = {"customer_id": cust_id, "balance": amount}
    transactions[acc_id] = [f"Initial deposit: {amount}"]
    print(f"Account created with Account ID: {acc_id}")
    save_all()

def update_admin():
    uname = input_nonempty("Admin username to update: ")
    if uname not in admins:
        print("Admin not found.")
        return
    new_pass = input_nonempty("New password: ")
    admins[uname] = new_pass
    print("Admin updated.")
    save_all()

def create_admin():
    uname = input_nonempty("New admin username: ")
    if uname in admins:
        print("Admin already exists.")
        return
    passwd = input_nonempty("Password: ")
    admins[uname] = passwd
    print("Admin created.")
    save_all()

def delete_admin():
    uname = input_nonempty("Admin username to delete: ")
    if uname in admins:
        del admins[uname]
        print("Admin deleted.")
        save_all()
    else:
        print("Admin not found.")

def update_customer():
    cid = input_nonempty("Customer ID to update: ")
    if cid in customers:
        new_name = input_nonempty("New name: ")
        customers[cid]["name"] = new_name
        print("Customer updated.")
        save_all()
    else:
        print("Customer not found.")

def delete_customer():
    cid = input_nonempty("Customer ID to delete: ")
    if cid in customers:
        with open(DELETE_FILE, "a") as f:
            f.write(str({cid: customers[cid]}) + "\n")
        uname = customers[cid]["username"]
        users.pop(uname, None)
        del customers[cid]
        print("Customer deleted.")
        save_all()
    else:
        print("Customer not found.")

def change_password(username):
    current = input_nonempty("Current password: ")
    if users[username]["password"] == current:
        new_pass = input_nonempty("New password: ")
        users[username]["password"] = new_pass
        print("Password updated.")
        save_all()
    else:
        print("Incorrect password.")

def deposit(account_id):
    if account_id not in accounts:
        print("Invalid account ID.")
        return
    amt = input_positive_float("Amount to deposit: ")
    accounts[account_id]["balance"] += amt
    transactions[account_id].append(f"Deposit: {amt}")
    print("Deposit successful.")
    save_all()

def withdraw(account_id):
    if account_id not in accounts:
        print("Invalid account ID.")
        return
    amt = input_positive_float("Amount to withdraw: ")
    if amt > accounts[account_id]["balance"]:
        print("Insufficient funds.")
        return
    accounts[account_id]["balance"] -= amt
    transactions[account_id].append(f"Withdraw: {amt}")
    print("Withdrawal successful.")
    save_all()

def show_balance(account_id):
    if account_id in accounts:
        print("Balance:", accounts[account_id]["balance"])
    else:
        print("Invalid account ID.")

def show_transactions(account_id):
    if account_id in transactions:
        print("Transaction History:")
        for t in transactions[account_id]:
            print("-", t)
    else:
        print("No transactions found.")

def transfer_cash():
    from_acc = input_nonempty("Enter your account ID: ")
    to_acc = input_nonempty("Enter recipient account ID: ")
    if from_acc not in accounts or to_acc not in accounts:
        print("Invalid account IDs.")
        return
    amt = input_positive_float("Amount to transfer: ")
    if accounts[from_acc]["balance"] < amt:
        print("Insufficient funds.")
        return
    accounts[from_acc]["balance"] -= amt
    accounts[to_acc]["balance"] += amt
    transactions[from_acc].append(f"Transfer to {to_acc}: {amt}")
    transactions[to_acc].append(f"Transfer from {from_acc}: {amt}")
    print(f"Transfer successful: {amt} transferred to {to_acc}.")
    save_all()

def login():
    role = input_nonempty("Login as admin or customer? ").lower()
    username = input_nonempty("Username: ")
    password = input_nonempty("Password: ")

    if role == "admin":
        if admins.get(username) == password:
            print("Admin login successful.")
            admin_menu()
        else:
            print("Invalid admin credentials.")
    elif role == "customer":
        user = users.get(username)
        if user and user["password"] == password:
            print("Customer login successful.")
            customer_menu(username)
        else:
            print("Invalid customer credentials.")
    else:
        print("Invalid role.")

def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. Create Customer\n2. Create Account\n3. Update Customer\n4. Delete Customer")
        print("5. Create Admin\n6. Update Admin\n7. Delete Admin\n8. Transfer Cash\n9. Logout")
        choice = input("Choice: ")
        if choice == "1":
            create_customer()
        elif choice == "2":
            create_account()
        elif choice == "3":
            update_customer()
        elif choice == "4":
            delete_customer()
        elif choice == "5":
            create_admin()
        elif choice == "6":
            update_admin()
        elif choice == "7":
            delete_admin()
        elif choice == "8":
            transfer_cash()
        elif choice == "9":
            break
        else:
            print("Invalid choice.")

def customer_menu(username):
    user_id = users[username]["id"]
    while True:
        print("\n--- Customer Menu ---")
        print("1. Deposit\n2. Withdraw\n3. Balance\n4. Transactions\n5. Change Password\n6. Logout")
        choice = input("Choice: ")
        acc_ids = [k for k, v in accounts.items() if v["customer_id"] == user_id]
        if not acc_ids:
            print("No account linked. Contact admin.")
            break
        acc_id = acc_ids[0]  # Assume one account for simplicity

        if choice == "1":
            deposit(acc_id)
        elif choice == "2":
            withdraw(acc_id)
        elif choice == "3":
            show_balance(acc_id)
        elif choice == "4":
            show_transactions(acc_id)
        elif choice == "5":
            change_password(username)
        elif choice == "6":
            break
        else:
            print("Invalid choice.")

# Main entry
def main():
    while True:
        print("\n--- Mini Banking System ---")
        print("1. Login\n2. Exit")
        choice = input("Select: ")
        if choice == "1":
            login()
        elif choice == "2":
            break
        else:
            print("Invalid choice.")

main()

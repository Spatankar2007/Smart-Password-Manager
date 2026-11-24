import os
import json
import secrets
import string
import re
import hashlib
import getpass
from datetime import datetime
from cryptography.fernet import Fernet

#                 FILE CONFIGURATION
KEY_FILE = "secret.key"
DATA_FILE = "passwords.json"
LOG_FILE = "activity.log"

#                 ENCRYPTION KEY MANAGEMENT

def load_or_create_key():
    """
    Loads the existing encryption key.
    If no key exists, creates a new one.
    """

    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as file:
            return file.read()

    key = Fernet.generate_key()

    with open(KEY_FILE, "wb") as file:
        file.write(key)

    print("New encryption key generated.")

    return key

# Create encryption object
ENCRYPTION_KEY = load_or_create_key()
cipher = Fernet(ENCRYPTION_KEY)


#                 MASTER PASSWORD


MASTER_FILE = "master.hash"

def hash_master_password(password):
    """
    Creates SHA-256 hash of the master password.
    The original master password is never stored.
    """

    return hashlib.sha256(password.encode()).hexdigest()


def setup_master_password():
    """
    Creates the master password when the program
    is run for the first time.
    """

    print("\n======================================")
    print("      CREATE MASTER PASSWORD")
    print("======================================")

    while True:

        password = getpass.getpass("Create master password: ")

        if len(password) < 8:
            print("Master password must contain at least 8 characters.")
            continue

        confirm = getpass.getpass("Confirm master password: ")

        if password != confirm:
            print("Passwords do not match.")
            continue

        password_hash = hash_master_password(password)

        with open(MASTER_FILE, "w") as file:
            file.write(password_hash)

        print("\nMaster password created successfully!")

        return True

def verify_master_password():
    """
    Verifies the master password before allowing access
    to the password manager.
    """
    if not os.path.exists(MASTER_FILE):
        setup_master_password()
        return True

    with open(MASTER_FILE, "r") as file:
        stored_hash = file.read().strip()

    MAX_ATTEMPTS = 3

    for attempt in range(MAX_ATTEMPTS):

        password = getpass.getpass("Enter master password: ")

        entered_hash = hash_master_password(password)

        if entered_hash == stored_hash:

            print("\nLogin successful!")
            return True

        remaining = MAX_ATTEMPTS - attempt - 1

        if remaining > 0:
            print(
                f"Incorrect password. "
                f"Attempts remaining: {remaining}"
            )

    print("\nToo many failed attempts.")
    print("Access denied.")

    return False
#                 FILE HANDLING

def load_data():
    """
    Loads password data from JSON file.
    """

    if not os.path.exists(DATA_FILE):
        return {}

    try:

        with open(DATA_FILE, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:

        print("Warning: Password file is corrupted.")
        return {}


def save_data(data):
    """
    Saves password data into JSON file.
    """

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

#                 ACTIVITY LOG

def log_activity(action):
    """
    Records important actions performed
    in the password manager.
    """

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(LOG_FILE, "a") as file:
        file.write(f"[{timestamp}] {action}\n")

#                 PASSWORD GENERATOR

def generate_password(length=16,
                      use_upper=True,
                      use_lower=True,
                      use_digits=True,
                      use_symbols=True):

    """
    Generates a cryptographically secure password
    using Python's secrets module.
    """

    character_sets = []

    if use_upper:
        character_sets.append(string.ascii_uppercase)

    if use_lower:
        character_sets.append(string.ascii_lowercase)

    if use_digits:
        character_sets.append(string.digits)

    if use_symbols:
        character_sets.append("!@#$%^&*()-_=+[]{}?")

    if not character_sets:
        print("At least one character type must be selected.")
        return None

    minimum_required = len(character_sets)

    if length < minimum_required:
        print(
            f"Password length must be at least "
            f"{minimum_required}."
        )
        return None

    password = []

    # Guarantee one character from every selected category
    for charset in character_sets:
        password.append(secrets.choice(charset))

    all_characters = "".join(character_sets)

    # Fill remaining positions
    for _ in range(length - len(password)):
        password.append(
            secrets.choice(all_characters)
        )

    # Securely shuffle password
    secrets.SystemRandom().shuffle(password)

    return "".join(password)

#                 PASSWORD STRENGTH

def check_strength(password):
    """
    Calculates a password strength score.
    """

    score = 0
    suggestions = []

    # Length
    if len(password) >= 12:
        score += 25
    elif len(password) >= 8:
        score += 15
    else:
        suggestions.append("Use at least 8 characters.")

    # Uppercase
    if re.search(r"[A-Z]", password):
        score += 15
    else:
        suggestions.append("Add uppercase letters.")

    # Lowercase
    if re.search(r"[a-z]", password):
        score += 15
    else:
        suggestions.append("Add lowercase letters.")

    # Numbers
    if re.search(r"[0-9]", password):
        score += 15
    else:
        suggestions.append("Add numbers.")

    # Symbols
    if re.search(r"[^A-Za-z0-9]", password):
        score += 20
    else:
        suggestions.append("Add special symbols.")

    # Repeated characters
    if re.search(r"(.)\1\1", password):
        score -= 10
        suggestions.append(
            "Avoid repeating the same character."
        )

    score = max(0, min(score, 100))

    if score >= 80:
        level = "VERY STRONG"
    elif score >= 60:
        level = "STRONG"
    elif score >= 40:
        level = "MODERATE"
    else:
        level = "WEAK"

    print("\n--------------------------------")
    print("PASSWORD STRENGTH ANALYSIS")
    print("--------------------------------")
    print(f"Score    : {score}/100")
    print(f"Strength : {level}")

    if suggestions:

        print("\nSuggestions:")

        for suggestion in suggestions:
            print("- " + suggestion)

    else:
        print("\nExcellent password!")

    return score

#                 ADD PASSWORD

def add_password():

    account = input("Enter account name: ").strip()

    if not account:
        print("Account name cannot be empty.")
        return

    username = input(
        "Enter username/email: "
    ).strip()

    print("\nPassword Options")
    print("1. Enter password manually")
    print("2. Generate secure password")

    choice = input("Choose option: ").strip()

    if choice == "1":

        password = getpass.getpass(
            "Enter password: "
        )

    elif choice == "2":

        try:
            length = int(
                input("Enter password length: ")
            )

            password = generate_password(length)

            if password is None:
                return

            print("\nGenerated Password:")
            print(password)

        except ValueError:

            print("Please enter a valid number.")
            return

    else:

        print("Invalid choice.")
        return

    # Check password strength
    check_strength(password)

    # Encrypt password
    encrypted_password = cipher.encrypt(
        password.encode()
    ).decode()

    data = load_data()

    if account in data:

        print(
            "\nAccount already exists."
        )

        overwrite = input(
            "Do you want to overwrite it? (y/n): "
        ).lower()

        if overwrite != "y":
            print("Operation cancelled.")
            return

    data[account] = {
        "username": username,
        "password": encrypted_password,
        "created": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "updated": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    save_data(data)

    log_activity(
        f"Password added/updated for account: {account}"
    )

    print(
        f"\nPassword for '{account}' "
        "saved successfully!"
    )
#                 GUI ADD PASSWORD

def save_password(account, username, password):

    account = account.strip()
    username = username.strip()

    if not account:
        return False, "Account name cannot be empty."

    if not username:
        return False, "Username/email cannot be empty."

    if not password:
        return False, "Password cannot be empty."

    # Check password strength
    score = check_strength(password)

    # Encrypt password
    encrypted_password = cipher.encrypt(
        password.encode()
    ).decode()

    data = load_data()

    if account in data:
        return False, "Account already exists."

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    data[account] = {
        "username": username,
        "password": encrypted_password,
        "created": current_time,
        "updated": current_time
    }

    save_data(data)

    log_activity(
        f"Password added for account: {account}"
    )

    return True, score
#                 VIEW PASSWORD

def retrieve_password():

    account = input(
        "Enter account name: "
    ).strip()

    data = load_data()

    if account not in data:

        print("Account not found.")
        return

    try:

        encrypted_password = data[account]["password"]

        decrypted_password = cipher.decrypt(
            encrypted_password.encode()
        ).decode()

        username = data[account].get(
            "username", ""
        )

        print("\n--------------------------------")
        print("ACCOUNT INFORMATION")
        print("--------------------------------")

        print(f"Account  : {account}")
        print(f"Username : {username}")

        # Hide password initially
        print("Password : " + "*" * len(decrypted_password))

        reveal = input(
            "\nReveal password? (y/n): "
        ).lower()

        if reveal == "y":

            print(
                f"Password : {decrypted_password}"
            )

        log_activity(
            f"Password retrieved for account: {account}"
        )

    except Exception:

        print(
            "Unable to decrypt password."
        )

#                 GUI RETRIEVE PASSWORD

def get_password(account):

    account = account.strip()

    if not account:
        return False, "Account name cannot be empty."

    data = load_data()

    if account not in data:
        return False, "Account not found."

    try:
        encrypted_password = data[account]["password"]

        decrypted_password = cipher.decrypt(
            encrypted_password.encode()
        ).decode()

        username = data[account].get(
            "username",
            ""
        )

        log_activity(
            f"Password retrieved for account: {account}"
        )

        return True, {
            "account": account,
            "username": username,
            "password": decrypted_password
        }

    except Exception:
        return False, "Unable to decrypt the password."
    
#                 GUI GET ACCOUNTS

def get_accounts():

    data = load_data()

    return list(data.keys())
#                 GUI SEARCH PASSWORDS

def search_saved_passwords(search_text):

    search_text = search_text.strip().lower()

    if not search_text:
        return False, "Please enter something to search."

    data = load_data()
    results = []

    for account, details in data.items():

        if isinstance(details, dict):
            username = details.get("username", "")
        else:
            username = ""

        if (
            search_text in account.lower()
            or search_text in username.lower()
       ):
            results.append({
                "account": account,
                "username": username
            })

    if not results:
        return False, "No matching accounts found."

    return True, results
#                 GUI ACTIVITY LOG

def get_activity_log():

    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, "r") as file:
        logs = file.readlines()

    return logs
#                 GUI DELETE PASSWORD

def delete_saved_password(account):

    account = account.strip()

    if not account:
        return False, "Account name cannot be empty."

    data = load_data()

    if account not in data:
        return False, "Account not found."

    del data[account]

    save_data(data)

    log_activity(
        f"Password deleted for account: {account}"
    )

    return True, "Password deleted successfully."
#                 GUI UPDATE PASSWORD

def update_saved_password(account, new_password):

    account = account.strip()

    if not account:
        return False, "Account name cannot be empty."

    if not new_password:
        return False, "New password cannot be empty."

    data = load_data()

    if account not in data:
        return False, "Account not found."

    # Check password strength
    score = check_strength(new_password)

    # Encrypt new password
    encrypted_password = cipher.encrypt(
        new_password.encode()
    ).decode()

    # Update password
    data[account]["password"] = encrypted_password

    # Update timestamp
    data[account]["updated"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Save updated data
    save_data(data)

    # Record activity
    log_activity(
        f"Password updated for account: {account}"
    )

    return True, score
#                 UPDATE PASSWORD
def update_password():

    account = input(
        "Enter account name to update: "
    ).strip()

    data = load_data()

    if account not in data:

        print("Account not found.")
        return

    print("\nGenerate a new password automatically?")

    choice = input(
        "Enter Y for generator or N to enter manually: "
    ).lower()

    if choice == "y":

        try:

            length = int(
                input(
                    "Enter new password length: "
                )
            )

            new_password = generate_password(length)

            if new_password is None:
                return

            print("\nGenerated Password:")
            print(new_password)

        except ValueError:

            print("Invalid length.")
            return

    else:

        new_password = getpass.getpass(
            "Enter new password: "
        )

    check_strength(new_password)

    encrypted_password = cipher.encrypt(
        new_password.encode()
    ).decode()

    data[account]["password"] = encrypted_password

    data[account]["updated"] = (
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    save_data(data)

    log_activity(
        f"Password updated for account: {account}"
    )

    print("\nPassword updated successfully!")

#                 DELETE PASSWORD

def delete_password():

    account = input(
        "Enter account name to delete: "
    ).strip()

    data = load_data()

    if account not in data:

        print("Account not found.")
        return

    confirm = input(
        f"Are you sure you want to delete "
        f"'{account}'? (y/n): "
    ).lower()

    if confirm == "y":

        del data[account]

        save_data(data)

        log_activity(
            f"Password deleted for account: {account}"
        )

        print("\nAccount deleted successfully.")

    else:

        print("Deletion cancelled.")

#                 SEARCH ACCOUNTS
def search_accounts():

    keyword = input(
        "Enter account name to search: "
    ).lower().strip()

    data = load_data()

    matches = []

    for account in data:

        if keyword in account.lower():
            matches.append(account)

    if not matches:

        print("\nNo matching accounts found.")
        return

    print("\nMatching Accounts:")

    for index, account in enumerate(
        matches, start=1
    ):

        print(f"{index}. {account}")

#                 LIST ALL ACCOUNTS
def list_accounts():

    data = load_data()

    if not data:

        print("\nNo passwords stored.")
        return

    print("\n================================")
    print("        SAVED ACCOUNTS")
    print("================================")

    for index, account in enumerate(
        data.keys(), start=1
    ):

        username = data[account].get(
            "username", ""
        )

        print(
            f"{index}. {account} "
            f"({username})"
        )

#                 PASSWORD GENERATOR MENU
def password_generator_menu():

    try:

        length = int(
            input(
                "\nEnter password length: "
            )
        )

        if length < 4:

            print(
                "Password should be at least 4 characters."
            )

            return

    except ValueError:

        print("Invalid length.")
        return

    print("\nCharacter Options")

    upper = input(
        "Include uppercase letters? (y/n): "
    ).lower() == "y"

    lower = input(
        "Include lowercase letters? (y/n): "
    ).lower() == "y"

    digits = input(
        "Include numbers? (y/n): "
    ).lower() == "y"

    symbols = input(
        "Include symbols? (y/n): "
    ).lower() == "y"

    password = generate_password(
        length,
        upper,
        lower,
        digits,
        symbols
    )

    if password:

        print("\n================================")
        print("      GENERATED PASSWORD")
        print("================================")
        print(password)

        check_strength(password)

        log_activity(
            "Password generated"
        )

#                 MAIN MENU
def main():

    print("\n==========================================")
    print("       SMART PASSWORD MANAGER")
    print("       Secure Password Management System")
    print("==========================================")

    # Authentication
    if not verify_master_password():
        return

    while True:

        print("\n")
        print("================================")
        print("          MAIN MENU")
        print("================================")

        print("1. Add Password")
        print("2. Retrieve Password")
        print("3. Update Password")
        print("4. Delete Password")
        print("5. Search Account")
        print("6. List All Accounts")
        print("7. Generate Password")
        print("8. Check Password Strength")
        print("9. Exit")

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":

            add_password()

        elif choice == "2":

            retrieve_password()

        elif choice == "3":

            update_password()

        elif choice == "4":

            delete_password()

        elif choice == "5":

            search_accounts()

        elif choice == "6":

            list_accounts()

        elif choice == "7":

            password_generator_menu()

        elif choice == "8":

            password = getpass.getpass(
                "Enter password to analyze: "
            )

            check_strength(password)

        elif choice == "9":

            print(
                "\nThank you for using "
                "Smart Password Manager!"
            )

            print("Exiting program...")

            break

        else:

            print(
                "\nInvalid choice. "
                "Please select 1-9."
            )

#                 PROGRAM START

if __name__ == "__main__":
    main()



import json
import secrets
import string
from pathlib import Path
from datetime import datetime


class Bank:
    database = Path(__file__).with_name("data.json")

    @classmethod
    def load_data(cls):
        if not cls.database.exists():
            return []

        try:
            with open(cls.database, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("Invalid database format")

            for account in data:
                account.setdefault("balance", 0)
                account.setdefault("transactions", [])

            return data

        except (json.JSONDecodeError, ValueError) as error:
            raise ValueError(f"Cannot load database: {error}") from error

    @classmethod
    def save_data(cls, accounts):
        temp_file = cls.database.with_suffix(".tmp")

        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(accounts, file, indent=4)

        temp_file.replace(cls.database)

    @staticmethod
    def generate_account_number(accounts):
        while True:
            number = "".join(
                secrets.choice(string.digits) for _ in range(10)
            )

            if not any(
                account["accountNo"] == number
                for account in accounts
            ):
                return number

    @staticmethod
    def authenticate(accounts, account_number, pin):
        for account in accounts:
            if (
                secrets.compare_digest(
                    str(account["accountNo"]),
                    str(account_number).strip()
                )
                and secrets.compare_digest(
                    str(account["pin"]),
                    str(pin)
                )
            ):
                return account

        return None

    @staticmethod
    def create_account(accounts, name, age, email, pin):
        name = name.strip()
        email = email.strip()

        if not name or not email:
            raise ValueError("Name and email are required.")

        if age < 18:
            raise ValueError("You must be at least 18 years old.")

        if not email or "@" not in email:
            raise ValueError("Enter a valid email address.")

        if len(str(pin)) != 4 or not str(pin).isdigit():
            raise ValueError("PIN must contain exactly 4 digits.")

        if any(
            account["email"].lower() == email.lower()
            for account in accounts
        ):
            raise ValueError("This email is already registered.")

        account = {
            "name": name,
            "age": int(age),
            "email": email,
            "pin": str(pin),
            "accountNo": Bank.generate_account_number(accounts),
            "balance": 0.0,
            "transactions": []
        }

        accounts.append(account)
        Bank.save_data(accounts)

        return account

    @staticmethod
    def add_transaction(account, transaction_type, amount):
        account.setdefault("transactions", []).append({
            "type": transaction_type,
            "amount": round(amount, 2),
            "balance": round(account["balance"], 2),
            "date": datetime.now().strftime(
                "%d-%m-%Y %I:%M:%S %p"
            )
        })

    @staticmethod
    def deposit(accounts, account, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        if amount > 10000:
            raise ValueError("Maximum deposit is ₹10,000 per transaction.")

        account["balance"] = round(account["balance"] + amount, 2)
        Bank.add_transaction(account, "Deposit", amount)
        Bank.save_data(accounts)

    @staticmethod
    def withdraw(accounts, account, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        if amount > account["balance"]:
            raise ValueError("Insufficient balance.")

        account["balance"] = round(account["balance"] - amount, 2)
        Bank.add_transaction(account, "Withdrawal", amount)
        Bank.save_data(accounts)

    @staticmethod
    def update_account(
        accounts, account, name, email, new_pin=""
    ):
        name = name.strip()
        email = email.strip()

        if not name or not email or "@" not in email:
            raise ValueError("Enter a valid name and email.")

        if new_pin and (
            len(new_pin) != 4 or not new_pin.isdigit()
        ):
            raise ValueError("New PIN must contain exactly 4 digits.")

        if any(
            other["email"].lower() == email.lower()
            and other["accountNo"] != account["accountNo"]
            for other in accounts
        ):
            raise ValueError("Email is already used by another account.")

        account["name"] = name
        account["email"] = email

        if new_pin:
            account["pin"] = new_pin

        Bank.save_data(accounts)

    @staticmethod
    def delete_account(accounts, account):
        accounts.remove(account)
        Bank.save_data(accounts)

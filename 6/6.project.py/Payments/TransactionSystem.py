from Payments.credit_card import CreditCard
from Payments.crypto_wallet import CryptoWallet
from Payments.paypal import PayPal
from datetime import datetime as dt_time
import time


class TransactionSystem:
    def __init__(self):
        self._methods = []


    def add_method(self):
        add_username = input("Input Username: ")
        while not add_username:
            add_username = input("Input Username: ")
        print("Choose a Payment method: ")
        print("1. Credit Card.")
        print("2. PayPal.")
        print("3. Crypto Wallet.")
        add_choice = input("> ")
        try:
            add_bal = float(input("Input balance: "))
        except (ValueError,TypeError):
            print("Invalid balance input.")
            return
        if add_choice == '1':
            add_cardnum = input("Input Card Number (exactly 16 digits): ")
            add_cvv = input("Input Card's CVV (exactly 4 digits): ")
            new_method = CreditCard(add_username)
            new_method.balance = add_bal
            new_method.card_number = add_cardnum
            new_method.cvv = add_cvv
            print("Entering Authentication details...")
            time.sleep(0.5)
            if not new_method.authenticate():
                print("Authentication Failed.")
                return
            print("Authentication Successful.")
            self._methods.append(new_method)

        elif add_choice == '2':
            add_email = input("""Paypal Email:
Example: ✅user@example.com, ✅john.doe@sub.domain.co.uk, ❌user@domain..com, ❌@example.com
Input Paypal Email:  """)
            add_password = input("Input User Password (8 or more digits): ")
            new_method = PayPal(add_username)
            new_method.balance = add_bal
            new_method.email = add_email
            new_method.password = add_password
            print("Entering Authentication details...")
            time.sleep(0.5)
            if not new_method.authenticate():
                print("Authentication Failed.")
                return
            print("Authentication Successful.")
            self._methods.append(new_method)

        elif add_choice == '3':
            add_walletaddress = input("Input Wallet Address (start with 0x, exactly 14 characters long) (Example: 0xA1B2c3D4e5F6): ")
            add_privatekey = input("Input Private Key: ")
            new_method = CryptoWallet(add_username)
            new_method.balance = add_bal
            new_method.wallet_address = add_walletaddress
            new_method.private_key = add_privatekey
            print("Entering Authentication details...")
            time.sleep(0.5)
            if not all([new_method.wallet_address,new_method.private_key]):
                print("Invalid wallet address/private key input.")
                print("Authentication Failed.")
                return
            print("Authentication Successful.")
            self._methods.append(new_method)
        else:
            print("Invalid choice.")
        time.sleep(0.5)


    def _show_methods(self):
        print("Choose a payment method: ")
        for idx,method in enumerate(self._methods,1):
            desc = type(method).__name__
            if hasattr(method,"card_number"):
                desc += f" - Card Number: ****{method.card_number[-4:]}"
            elif hasattr(method,"email"):
                desc += f" - Email: {method.email[0]}***@{method.email.split("@")[-1]}"
            elif hasattr(method,"wallet_address"):
                desc += f" - Wallet: ...{method.wallet_address[-4:]}"
            print(f"{idx}. {desc}")


    def make_payment(self):
        if not self._methods:
            print("No methods available.")
            time.sleep(0.5)
            return

        self._show_methods()
        try:
            choice = int(input("> ")) - 1
            method = self._methods[choice]
        except (ValueError,TypeError,IndexError):
            print("Invalid choice.")
            return

        print("Checking Authentication...")
        time.sleep(0.5)

        try:
            amount = float(input("Enter payment amount: "))
        except ValueError:
            print("Invalid amount input.")
            return

        print("Performing Transaction Progress..")
        time.sleep(0.5)
        if method.pay(amount):
            print("Transaction completed.")
            print("Logging transaction to log.txt...")
            self.log_transaction(method,amount)
            time.sleep(0.5)
            print(f"Remaining balance: {method.check_bal()}")
        else:
            print("Transaction failed.")
        time.sleep(0.5)


    def check_bals(self):
        if not self._methods:
            print("No methods available.")
            time.sleep(0.5)
            return
        for method in self._methods:
            print(f"{type(method).__name__} ({method.username}): {method.check_bal()}")

    def log_transaction(self,method,amount):
        with open("log.txt","a") as l:
            l.write(f"{dt_time.now()} | {type(method).__name__} | User: {method.username} | Amount: {amount}\n")

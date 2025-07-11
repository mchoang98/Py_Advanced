from .payment_method import PaymentMethod
import re


class PayPal(PaymentMethod):
    def __init__(self, username):
        super().__init__(username)
        self._email = None
        self._password = None
        # self.__authentication = False

    @property
    def email(self):
        return self._email
    @email.setter
    def email(self,em):
        if not isinstance(em,str):
            raise TypeError("Email input must be a string!")
        self._email = em
    @property
    def password(self):
        return self._password
    @password.setter
    def password(self,password):
        if not isinstance(password,str):
            raise TypeError("Password input must be a string!")
        self._password = password

    def authenticate(self):
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not (re.match(email_pattern,self._email) and len(self._password) >= 8):
            print("Invalid Email/Password.")
            return False
        return True

    def pay(self, amount):
        if self._balance >= amount:
            self._balance -= amount
            return True
        return False

    # def pay(self, amount):
    #     if self.__authentication:
    #         self._balance -= amount
    #         print(f"Transaction complete. {amount}$ is deducted from user balance.")
    #     else:
    #         print("User unauthenticated.")
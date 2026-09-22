# ============================================================
# ENCAPSULATION
# ============================================================
# Bundling data + methods that operate on it, and restricting
# direct access to internal state.
#
# Python conventions:
#   self.name      -> public    (anyone can access)
#   self._name     -> protected (by convention: "internal use")
#   self.__name    -> private   (name-mangled to _ClassName__name)

class BankAccount:
    def __init__(self, owner: str, initial_balance: float):
        self.owner = owner             # public
        self._bank_name = "PyBank"     # protected — convention only
        self.__balance = initial_balance   # private — name-mangled

    # Getter — controlled read access
    def get_balance(self) -> float:
        return self.__balance

    # Setter — controlled write access with validation
    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.__balance += amount
        print(f"Deposited {amount}. New balance: {self.__balance}")

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        self.__balance -= amount
        print(f"Withdrew {amount}. New balance: {self.__balance}")

    def __str__(self) -> str:
        return f"Account({self.owner}, balance={self.__balance})"


acc = BankAccount("Alice", 1000)
acc.deposit(500)
acc.withdraw(200)
print(acc.get_balance())     # 1300

# Trying to access private directly
# print(acc.__balance)       # AttributeError!
# Name mangling — Python renames __balance to _BankAccount__balance
print(acc._BankAccount__balance)  # 1300 — accessible but DON'T do this


# ============================================================
# @property — Pythonic way to write getters/setters
# ============================================================

class Temperature:
    def __init__(self, celsius: float):
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("Temperature below absolute zero is not possible")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9/5 + 32

    # Read-only property (no setter)
    @property
    def kelvin(self) -> float:
        return self._celsius + 273.15


t = Temperature(25)
print(t.celsius)      # 25   — calls getter
print(t.fahrenheit)   # 77.0
print(t.kelvin)       # 298.15

t.celsius = 100       # calls setter
print(t.fahrenheit)   # 212.0

# t.celsius = -300    # raises ValueError
# t.kelvin = 400      # AttributeError — no setter defined

# ============================================================
# ABSTRACTION & ABSTRACT CLASSES
# ============================================================
# Abstraction = hiding implementation details, exposing only what's needed.
# In Python, use ABC (Abstract Base Class) from the `abc` module.

from abc import ABC, abstractmethod


# ---- 1. ABSTRACT CLASS ----
# Cannot be instantiated directly.
# Forces subclasses to implement abstract methods.

class PaymentProcessor(ABC):

    @abstractmethod
    def pay(self, amount: float) -> str:
        """Process a payment of given amount."""
        ...

    @abstractmethod
    def refund(self, amount: float) -> str:
        """Refund a payment."""
        ...

    # Concrete method — shared logic available to all subclasses
    def validate_amount(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError(f"Invalid amount: {amount}")

    def process(self, amount: float) -> str:
        self.validate_amount(amount)
        return self.pay(amount)


# pp = PaymentProcessor()  # TypeError: Can't instantiate abstract class


class CreditCardProcessor(PaymentProcessor):
    def __init__(self, card_number: str):
        self.card_number = card_number[-4:]  # store only last 4 digits

    def pay(self, amount: float) -> str:
        return f"Paid ${amount} via Credit Card ending in {self.card_number}"

    def refund(self, amount: float) -> str:
        return f"Refunded ${amount} to Credit Card ending in {self.card_number}"


class PayPalProcessor(PaymentProcessor):
    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float) -> str:
        return f"Paid ${amount} via PayPal ({self.email})"

    def refund(self, amount: float) -> str:
        return f"Refunded ${amount} to PayPal ({self.email})"


class UPIProcessor(PaymentProcessor):
    def __init__(self, upi_id: str):
        self.upi_id = upi_id

    def pay(self, amount: float) -> str:
        return f"Paid ${amount} via UPI ({self.upi_id})"

    def refund(self, amount: float) -> str:
        return f"Refunded ${amount} via UPI ({self.upi_id})"


processors: list[PaymentProcessor] = [
    CreditCardProcessor("1234567890001234"),
    PayPalProcessor("user@example.com"),
    UPIProcessor("user@upi"),
]

for p in processors:
    print(p.process(100))
    print(p.refund(50))
    print()


# ---- 2. ABSTRACT PROPERTY ----

class DatabaseConnection(ABC):
    @property
    @abstractmethod
    def connection_string(self) -> str:
        ...

    @abstractmethod
    def connect(self) -> None:
        ...

    @abstractmethod
    def disconnect(self) -> None:
        ...


class MySQLConnection(DatabaseConnection):
    def __init__(self, host: str, db: str):
        self.host = host
        self.db = db

    @property
    def connection_string(self) -> str:
        return f"mysql://{self.host}/{self.db}"

    def connect(self) -> None:
        print(f"Connecting to MySQL: {self.connection_string}")

    def disconnect(self) -> None:
        print("Disconnecting from MySQL")


class PostgreSQLConnection(DatabaseConnection):
    def __init__(self, host: str, db: str):
        self.host = host
        self.db = db

    @property
    def connection_string(self) -> str:
        return f"postgresql://{self.host}/{self.db}"

    def connect(self) -> None:
        print(f"Connecting to PostgreSQL: {self.connection_string}")

    def disconnect(self) -> None:
        print("Disconnecting from PostgreSQL")


db = MySQLConnection("localhost", "mydb")
db.connect()
print(db.connection_string)
db.disconnect()


# ---- 3. ABSTRACT CLASS WITH PARTIAL IMPLEMENTATION ----
# Abstract class can have some concrete methods — it's not all-or-nothing.

class Logger(ABC):
    def log(self, message: str) -> None:
        formatted = self._format(message)
        self._write(formatted)

    def _format(self, message: str) -> str:
        from datetime import datetime
        return f"[{datetime.now().strftime('%H:%M:%S')}] {message}"

    @abstractmethod
    def _write(self, message: str) -> None:
        ...


class ConsoleLogger(Logger):
    def _write(self, message: str) -> None:
        print(f"CONSOLE: {message}")


class FileLogger(Logger):
    def __init__(self, filepath: str):
        self.filepath = filepath

    def _write(self, message: str) -> None:
        # In real code: open file and write
        print(f"FILE ({self.filepath}): {message}")


loggers: list[Logger] = [ConsoleLogger(), FileLogger("/tmp/app.log")]
for logger in loggers:
    logger.log("Application started")

# I am trying to build a simple transaction system covering 3 creational 
# Singleton, Builder, Factory


# Factory pattern I will build a general class which holds different payment systems

from abc import ABC, abstractmethod
import threading

# product
class PaymentSystem(ABC):
    @abstractmethod
    def processPayment(self, amount: float):
        pass
    
# concreate products
class CreditCardPaymentSystem(PaymentSystem):
    def processPayment(self, amount: float):
        return f"Amount CreditCard spend ${amount}"

class UPIPaymentSystem(PaymentSystem):
    def processPayment(self, amount: float):
        print(f"Amount UPI spend {amount}")
    
class NetBankingPaymentSystem(PaymentSystem):
    def processPayment(self, amount: float):
        return f"Amount NetBanking spend {amount}"
    
class PaymentSystemFactory():
    _registry = {
        "CreditCard" : CreditCardPaymentSystem,
        "UPI" : UPIPaymentSystem,
        "NetBanking" : NetBankingPaymentSystem
    }
    
    def create(self,paymentType: PaymentSystem):
        return self._registry[paymentType]()
    

# Builder pattern 
# We have mulitple transaction details so we will create a transactionBuilder to avoid constructor telescoping as few parameters are requried and some are optional

class Transaction:
    def __init__(self, builder: "TransactionBuilder"):
        self.transactionId = builder.transactionId
        self.customerId = builder.customerId
        self.amount = builder.amount
        self.currency = "INR"
        self.notes = "Dinner"
        self.timestamp = ""
        
    def get_amount(self, amount: int):
        return amount
        
class TransactionBuilder:
    def __init__(self,transactionId,customerId,amount):
        self.transactionId = transactionId
        self.customerId = customerId
        self.amount = amount
        self.currency = "INR"
        self.notes = "Dinner"
        self.timestamp = ""
        
    def set_currency(self,currency: str):
        self.currency = currency
        return self
    
    def set_notes(self,notes: str):
        self.notes = notes
        return self
    
    def set_timestamp(self,timestamp: str):
        self.timestamp = timestamp
        return self
    
    def build(self):
        return Transaction(self)
    
# Singleton pattern
# I want a logger who will all the transaction logs.
# Note we need only 1 instance of the logger class or it might cause issues.
# Also we might need lock so no other thread will try to create another instance.

class TransactionLogger:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance
    
    def log(self, message: str):
        print(f"Logging : {message}")
    
    
if __name__ == "__main__":
    
    payment = PaymentSystemFactory().create("UPI")
    txn = TransactionBuilder(1,101,500).set_currency("USD").set_notes("Lunch Party").set_timestamp("2 PM").build()
    payment.processPayment(txn.amount)
    TransactionLogger().log("Payment successful via UPI")
    
    
        
    
        
    
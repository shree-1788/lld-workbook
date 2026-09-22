# ============================================================
# LLD PATTERNS PRIMER
# ============================================================
# The most common patterns used in LLD interviews and real systems.
# Each is a short, runnable example. Full implementations belong
# in separate files (design patterns folder).

from abc import ABC, abstractmethod
from typing import Optional


# ============================================================
# 1. SINGLETON
# ============================================================
# Ensure only one instance of a class exists.

class ConfigManager:
    _instance: Optional["ConfigManager"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._settings = {}
        return cls._instance

    def set(self, key: str, value) -> None:
        self._settings[key] = value

    def get(self, key: str, default=None):
        return self._settings.get(key, default)


c1 = ConfigManager()
c2 = ConfigManager()
c1.set("debug", True)
print(c2.get("debug"))   # True — same instance
print(c1 is c2)          # True


# ============================================================
# 2. FACTORY METHOD
# ============================================================
# Let subclasses decide which object to create.

class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...

class EmailNotification(Notification):
    def send(self, message: str) -> None:
        print(f"[EMAIL] {message}")

class SMSNotification(Notification):
    def send(self, message: str) -> None:
        print(f"[SMS] {message}")

class PushNotification(Notification):
    def send(self, message: str) -> None:
        print(f"[PUSH] {message}")

class NotificationFactory:
    _registry = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "push": PushNotification,
    }

    @classmethod
    def create(cls, channel: str) -> Notification:
        if channel not in cls._registry:
            raise ValueError(f"Unknown channel: {channel}")
        return cls._registry[channel]()

    @classmethod
    def register(cls, channel: str, klass) -> None:
        cls._registry[channel] = klass


for channel in ["email", "sms", "push"]:
    NotificationFactory.create(channel).send("Hello!")


# ============================================================
# 3. OBSERVER
# ============================================================
# One-to-many dependency: when one object changes, all observers
# are notified automatically.

class EventSystem:
    def __init__(self):
        self._listeners: dict[str, list] = {}

    def subscribe(self, event: str, listener) -> None:
        self._listeners.setdefault(event, []).append(listener)

    def unsubscribe(self, event: str, listener) -> None:
        self._listeners.get(event, []).remove(listener)

    def emit(self, event: str, data=None) -> None:
        for listener in self._listeners.get(event, []):
            listener(data)


events = EventSystem()
events.subscribe("order.placed", lambda d: print(f"[EMAIL] Order {d['id']} confirmed"))
events.subscribe("order.placed", lambda d: print(f"[INVENTORY] Reduce stock for {d['id']}"))
events.emit("order.placed", {"id": "ORD-001"})


# ============================================================
# 4. STRATEGY
# ============================================================
# Define a family of algorithms, make them interchangeable.

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list: ...

class BubbleSort(SortStrategy):
    def sort(self, data: list) -> list:
        arr = data.copy()
        for i in range(len(arr)):
            for j in range(len(arr) - i - 1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

class QuickSort(SortStrategy):
    def sort(self, data: list) -> list:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        mid  = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + mid + self.sort(right)

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy) -> None:
        self._strategy = strategy

    def sort(self, data: list) -> list:
        return self._strategy.sort(data)


data = [5, 3, 8, 1, 9, 2]
sorter = Sorter(BubbleSort())
print(sorter.sort(data))   # [1, 2, 3, 5, 8, 9]
sorter.set_strategy(QuickSort())
print(sorter.sort(data))   # [1, 2, 3, 5, 8, 9]


# ============================================================
# 5. DECORATOR PATTERN (structural, not Python decorator)
# ============================================================
# Add behaviour to objects dynamically without subclassing.

class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float: ...
    @abstractmethod
    def description(self) -> str: ...

class SimpleCoffee(Coffee):
    def cost(self) -> float: return 2.0
    def description(self) -> str: return "Coffee"

class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    def cost(self) -> float: return self._coffee.cost()
    def description(self) -> str: return self._coffee.description()

class Milk(CoffeeDecorator):
    def cost(self) -> float: return self._coffee.cost() + 0.5
    def description(self) -> str: return self._coffee.description() + ", Milk"

class Sugar(CoffeeDecorator):
    def cost(self) -> float: return self._coffee.cost() + 0.25
    def description(self) -> str: return self._coffee.description() + ", Sugar"

class Whip(CoffeeDecorator):
    def cost(self) -> float: return self._coffee.cost() + 0.75
    def description(self) -> str: return self._coffee.description() + ", Whip"


order = Whip(Sugar(Milk(SimpleCoffee())))
print(order.description())   # Coffee, Milk, Sugar, Whip
print(f"${order.cost():.2f}")         # $3.50

# ============================================================
# COMPOSITION vs INHERITANCE
# ============================================================
# Inheritance  = "IS-A" relationship  (Dog IS-A Animal)
# Composition  = "HAS-A" relationship (Car HAS-A Engine)
#
# Rule of thumb: prefer composition over inheritance.
# Inheritance creates tight coupling; composition is more flexible.


# ---- 1. INHERITANCE APPROACH (tight coupling) ----

class FlyingAnimal:
    def fly(self) -> str:
        return "Flying!"

class SwimmingAnimal:
    def swim(self) -> str:
        return "Swimming!"

# Problem: what if you need a FlyingSwimmingAnimal?
# Multiple inheritance gets messy fast.
class Duck1(FlyingAnimal, SwimmingAnimal):
    def quack(self) -> str:
        return "Quack!"


# ---- 2. COMPOSITION APPROACH (flexible) ----

class FlyBehavior:
    def fly(self) -> str:
        return "Flying with wings!"


class NoFlyBehavior:
    def fly(self) -> str:
        return "Can't fly!"


class SwimBehavior:
    def swim(self) -> str:
        return "Swimming with webbed feet!"


class NoSwimBehavior:
    def swim(self) -> str:
        return "Can't swim!"


class Animal:
    def __init__(self, name: str, fly_behavior, swim_behavior):
        self.name = name
        self._fly = fly_behavior
        self._swim = swim_behavior

    # Delegate to composed objects
    def fly(self) -> str:
        return f"{self.name}: {self._fly.fly()}"

    def swim(self) -> str:
        return f"{self.name}: {self._swim.swim()}"

    def set_fly_behavior(self, behavior) -> None:
        """Behaviour can be swapped at runtime!"""
        self._fly = behavior


duck = Animal("Duck", FlyBehavior(), SwimBehavior())
penguin = Animal("Penguin", NoFlyBehavior(), SwimBehavior())
eagle = Animal("Eagle", FlyBehavior(), NoSwimBehavior())

print(duck.fly())       # Duck: Flying with wings!
print(penguin.fly())    # Penguin: Can't fly!
print(eagle.swim())     # Eagle: Can't swim!

# Runtime behaviour swap (impossible with inheritance)
duck.set_fly_behavior(NoFlyBehavior())
print(duck.fly())       # Duck: Can't fly!  (duck got injured)


# ---- 3. REAL-WORLD COMPOSITION EXAMPLE ----
# A notification system built with composition.

class EmailSender:
    def send(self, to: str, message: str) -> None:
        print(f"[EMAIL] To: {to} | {message}")


class SMSSender:
    def send(self, to: str, message: str) -> None:
        print(f"[SMS] To: {to} | {message}")


class PushNotificationSender:
    def send(self, to: str, message: str) -> None:
        print(f"[PUSH] To: {to} | {message}")


class NotificationService:
    def __init__(self):
        self._senders: list = []

    def add_channel(self, sender) -> "NotificationService":
        self._senders.append(sender)
        return self  # fluent interface

    def notify(self, user: str, message: str) -> None:
        for sender in self._senders:
            sender.send(user, message)


# Compose behaviour at runtime
service = (
    NotificationService()
    .add_channel(EmailSender())
    .add_channel(SMSSender())
    .add_channel(PushNotificationSender())
)

service.notify("alice@example.com", "Your order has shipped!")
# [EMAIL] To: alice@example.com | Your order has shipped!
# [SMS]   To: alice@example.com | Your order has shipped!
# [PUSH]  To: alice@example.com | Your order has shipped!


# ---- 4. MIXIN PATTERN ----
# A mixin is a small class that adds a specific capability.
# Used WITH inheritance but in a controlled way.
# Mixins don't make sense on their own — they augment other classes.

class TimestampMixin:
    """Adds created_at and updated_at to any model."""
    def set_created(self) -> None:
        from datetime import datetime
        self.created_at = datetime.now()

    def set_updated(self) -> None:
        from datetime import datetime
        self.updated_at = datetime.now()


class SerializeMixin:
    """Adds JSON serialization to any class."""
    def to_dict(self) -> dict:
        return {k: str(v) for k, v in self.__dict__.items()}


class BaseModel:
    pass


class User(TimestampMixin, SerializeMixin, BaseModel):
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.set_created()


user = User("Alice", "alice@example.com")
print(user.to_dict())
# {'name': 'Alice', 'email': 'alice@example.com', 'created_at': '...'}

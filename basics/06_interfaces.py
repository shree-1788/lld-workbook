# ============================================================
# INTERFACES IN PYTHON
# ============================================================
# Python has no `interface` keyword (unlike Java/C#).
# An interface = an ABC where ALL methods are abstract.
# Convention: name it with a capital I prefix or "able" suffix.
#
# Key rule: an interface defines WHAT to do, not HOW.

from abc import ABC, abstractmethod


# ---- 1. DEFINING INTERFACES ----

class Printable(ABC):
    @abstractmethod
    def print_info(self) -> None:
        ...


class Serializable(ABC):
    @abstractmethod
    def serialize(self) -> dict:
        ...

    @abstractmethod
    def deserialize(self, data: dict) -> None:
        ...


class Comparable(ABC):
    @abstractmethod
    def compare_to(self, other: object) -> int:
        """Return negative, 0, or positive."""
        ...


# ---- 2. IMPLEMENTING MULTIPLE INTERFACES ----
# A class can implement multiple interfaces — this is how Python does
# what Java achieves with `implements InterfaceA, InterfaceB`.

class Employee(Printable, Serializable, Comparable):
    def __init__(self, name: str, salary: float, emp_id: int):
        self.name = name
        self.salary = salary
        self.emp_id = emp_id

    # Printable
    def print_info(self) -> None:
        print(f"Employee #{self.emp_id}: {self.name}, Salary: ${self.salary}")

    # Serializable
    def serialize(self) -> dict:
        return {"id": self.emp_id, "name": self.name, "salary": self.salary}

    def deserialize(self, data: dict) -> None:
        self.emp_id = data["id"]
        self.name = data["name"]
        self.salary = data["salary"]

    # Comparable
    def compare_to(self, other: object) -> int:
        if not isinstance(other, Employee):
            raise TypeError("Can only compare Employee with Employee")
        if self.salary < other.salary:
            return -1
        elif self.salary > other.salary:
            return 1
        return 0


e1 = Employee("Alice", 90000, 1)
e2 = Employee("Bob", 75000, 2)

e1.print_info()
print(e1.serialize())
print(e1.compare_to(e2))    # 1  (Alice earns more)


# ---- 3. INTERFACE SEGREGATION (important for LLD) ----
# Prefer small, focused interfaces over one big fat interface.
# Each class should only implement what it actually needs.

# BAD — one fat interface
class IWorker(ABC):
    @abstractmethod
    def work(self) -> None: ...

    @abstractmethod
    def eat(self) -> None: ...

    @abstractmethod
    def sleep(self) -> None: ...


# GOOD — segregated interfaces
class IWorkable(ABC):
    @abstractmethod
    def work(self) -> None: ...


class IEatable(ABC):
    @abstractmethod
    def eat(self) -> None: ...


class ISleepable(ABC):
    @abstractmethod
    def sleep(self) -> None: ...


class HumanWorker(IWorkable, IEatable, ISleepable):
    def work(self) -> None:
        print("Human is working")

    def eat(self) -> None:
        print("Human is eating")

    def sleep(self) -> None:
        print("Human is sleeping")


class RobotWorker(IWorkable):
    # Robots don't eat or sleep — no need to implement those interfaces
    def work(self) -> None:
        print("Robot is working 24/7")


hw = HumanWorker()
rw = RobotWorker()
hw.work(); hw.eat(); hw.sleep()
rw.work()


# ---- 4. PROTOCOL (Python 3.8+) — Structural Subtyping ----
# typing.Protocol = "informal interface" — no inheritance needed.
# If an object HAS the right methods, it satisfies the protocol.

from typing import Protocol, runtime_checkable


@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> None: ...
    def get_color(self) -> str: ...


class Circle:
    def __init__(self, radius: float, color: str):
        self.radius = radius
        self.color = color

    def draw(self) -> None:
        print(f"Drawing circle with radius {self.radius}")

    def get_color(self) -> str:
        return self.color


class Square:
    def __init__(self, side: float, color: str):
        self.side = side
        self.color = color

    def draw(self) -> None:
        print(f"Drawing square with side {self.side}")

    def get_color(self) -> str:
        return self.color


# Neither Circle nor Square inherits from Drawable
# But both satisfy the protocol — duck typing + type safety

def render(shape: Drawable) -> None:
    print(f"Color: {shape.get_color()}")
    shape.draw()

render(Circle(5, "red"))
render(Square(3, "blue"))

print(isinstance(Circle(1, "x"), Drawable))  # True — runtime_checkable

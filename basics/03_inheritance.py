# ============================================================
# INHERITANCE
# ============================================================
# Child class inherits attributes and methods from parent class.
# Promotes code reuse and "is-a" relationships.

# ---- 1. SINGLE INHERITANCE ----

class Animal:
    def __init__(self, name: str, sound: str):
        self.name = name
        self.sound = sound

    def speak(self) -> str:
        return f"{self.name} says {self.sound}"

    def breathe(self) -> str:
        return f"{self.name} is breathing"


class Dog(Animal):
    def __init__(self, name: str, breed: str):
        # super() calls the parent __init__
        super().__init__(name, sound="Woof")
        self.breed = breed

    # Overriding parent method
    def speak(self) -> str:
        return f"{self.name} ({self.breed}) barks: Woof!"

    def fetch(self) -> str:
        return f"{self.name} fetches the ball!"


dog = Dog("Rex", "Labrador")
print(dog.speak())      # Rex (Labrador) barks: Woof!
print(dog.breathe())    # Rex is breathing  — inherited from Animal
print(dog.fetch())      # Rex fetches the ball!

# isinstance checks the full inheritance chain
print(isinstance(dog, Dog))     # True
print(isinstance(dog, Animal))  # True — Dog IS-A Animal

# issubclass checks class relationships
print(issubclass(Dog, Animal))  # True


# ---- 2. MULTILEVEL INHERITANCE ----
# A -> B -> C

class Vehicle:
    def __init__(self, speed: int):
        self.speed = speed

    def move(self) -> str:
        return f"Moving at {self.speed} km/h"


class Car(Vehicle):
    def __init__(self, speed: int, brand: str):
        super().__init__(speed)
        self.brand = brand

    def honk(self) -> str:
        return f"{self.brand}: Beep!"


class ElectricCar(Car):
    def __init__(self, speed: int, brand: str, battery_kw: int):
        super().__init__(speed, brand)
        self.battery_kw = battery_kw

    def charge(self) -> str:
        return f"Charging {self.brand} with {self.battery_kw} kW"


tesla = ElectricCar(200, "Tesla", 250)
print(tesla.move())     # Moving at 200 km/h  — from Vehicle
print(tesla.honk())     # Tesla: Beep!        — from Car
print(tesla.charge())   # Charging Tesla...   — own method


# ---- 3. MULTIPLE INHERITANCE ----
# Python supports inheriting from more than one class.
# MRO (Method Resolution Order) decides which method is called.

class Flyable:
    def fly(self) -> str:
        return "I can fly!"

    def describe(self) -> str:
        return "Flyable creature"


class Swimmable:
    def swim(self) -> str:
        return "I can swim!"

    def describe(self) -> str:
        return "Swimmable creature"


class Duck(Animal, Flyable, Swimmable):
    def __init__(self, name: str):
        Animal.__init__(self, name, "Quack")

    def speak(self) -> str:
        return f"{self.name} says Quack!"


duck = Duck("Donald")
print(duck.speak())       # Donald says Quack!
print(duck.fly())         # I can fly!
print(duck.swim())        # I can swim!
print(duck.describe())    # Flyable creature — MRO decides: Animal first, then Flyable

# MRO — left-to-right, depth-first (C3 linearization)
print(Duck.__mro__)
# (<class 'Duck'>, <class 'Animal'>, <class 'Flyable'>, <class 'Swimmable'>, <class 'object'>)


# ---- 4. super() IN DEPTH ----
# super() follows MRO, not just "the direct parent"

class A:
    def greet(self):
        print("Hello from A")

class B(A):
    def greet(self):
        super().greet()    # calls A.greet
        print("Hello from B")

class C(A):
    def greet(self):
        super().greet()    # calls A.greet
        print("Hello from C")

class D(B, C):
    def greet(self):
        super().greet()    # follows MRO: D -> B -> C -> A
        print("Hello from D")


d = D()
d.greet()
# Hello from A
# Hello from C
# Hello from B
# Hello from D

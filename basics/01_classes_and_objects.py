# ============================================================
# CLASSES AND OBJECTS
# ============================================================

# A class is a blueprint. An object is an instance of that blueprint.

class Car:
    # Class variable — shared across ALL instances
    total_cars = 0

    # __init__ is the constructor, called when object is created
    def __init__(self, brand: str, model: str, year: int):
        # Instance variables — unique to each object
        self.brand = brand
        self.model = model
        self.year = year
        Car.total_cars += 1

    # Instance method — operates on self (the object)
    def get_info(self) -> str:
        return f"{self.year} {self.brand} {self.model}"

    # __str__ controls what print(obj) shows
    def __str__(self) -> str:
        return self.get_info()

    # __repr__ is for developers — unambiguous representation
    def __repr__(self) -> str:
        return f"Car(brand={self.brand!r}, model={self.model!r}, year={self.year})"


# Creating objects (instances)
car1 = Car("Toyota", "Camry", 2022)
car2 = Car("Honda", "Civic", 2023)

print(car1)              # uses __str__
print(repr(car2))        # uses __repr__
print(Car.total_cars)    # 2  — class variable accessed via class name

# Accessing instance attributes
print(car1.brand)        # Toyota
print(car2.year)         # 2023

# Dynamically adding an attribute (not recommended, just FYI)
car1.color = "Red"
print(car1.color)        # Red
# car2.color would throw AttributeError — only car1 has it


# ============================================================
# __init__ vs __new__
# ============================================================
# __new__  -> allocates memory, returns the new object
# __init__ -> initializes the object (you use this 99% of the time)

class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


s1 = Singleton()
s2 = Singleton()
print(s1 is s2)   # True — same object


# ============================================================
# DELETING OBJECTS
# ============================================================
# Python uses garbage collection (reference counting + cyclic GC).
# del just removes the reference; memory freed when ref count hits 0.

car3 = Car("BMW", "X5", 2024)
del car3
# car3 is now gone from this scope

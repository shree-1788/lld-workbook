# ============================================================
# POLYMORPHISM
# ============================================================
# "Many forms" — same interface, different behaviour.
# Two types: method overriding (runtime) and duck typing.

# ---- 1. METHOD OVERRIDING (Runtime Polymorphism) ----

class Shape:
    def area(self) -> float:
        raise NotImplementedError("Subclass must implement area()")

    def perimeter(self) -> float:
        raise NotImplementedError("Subclass must implement perimeter()")

    def describe(self) -> str:
        return f"{self.__class__.__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        import math
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float):
        self.a, self.b, self.c = a, b, c

    def area(self) -> float:
        s = (self.a + self.b + self.c) / 2
        return (s * (s - self.a) * (s - self.b) * (s - self.c)) ** 0.5

    def perimeter(self) -> float:
        return self.a + self.b + self.c


# Polymorphism in action — same call, different behaviour
shapes: list[Shape] = [Circle(5), Rectangle(4, 6), Triangle(3, 4, 5)]

for shape in shapes:
    print(shape.describe())
# Circle: area=78.54, perimeter=31.42
# Rectangle: area=24.00, perimeter=20.00
# Triangle: area=6.00, perimeter=12.00


# ---- 2. DUCK TYPING ----
# "If it walks like a duck and quacks like a duck, it's a duck."
# Python doesn't check the type — it just checks if the method exists.

class Dog:
    def speak(self) -> str:
        return "Woof!"

class Cat:
    def speak(self) -> str:
        return "Meow!"

class Robot:
    def speak(self) -> str:
        return "Beep boop!"

# No inheritance needed — they all have speak()
def make_noise(entity) -> None:
    print(entity.speak())

for thing in [Dog(), Cat(), Robot()]:
    make_noise(thing)


# ---- 3. OPERATOR OVERLOADING ----
# Polymorphism applied to operators via dunder methods.

class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __len__(self) -> int:
        return 2  # a 2D vector always has 2 components

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"


v1 = Vector(1, 2)
v2 = Vector(3, 4)

print(v1 + v2)      # Vector(4, 6)
print(v2 - v1)      # Vector(2, 2)
print(v1 * 3)       # Vector(3, 6)
print(v1 == Vector(1, 2))   # True
print(len(v1))      # 2


# ---- 4. METHOD OVERLOADING (Python style) ----
# Python doesn't support true overloading. Use default args or *args.

class Calculator:
    def add(self, *args: float) -> float:
        return sum(args)

calc = Calculator()
print(calc.add(1, 2))        # 3
print(calc.add(1, 2, 3))     # 6
print(calc.add(1, 2, 3, 4))  # 10

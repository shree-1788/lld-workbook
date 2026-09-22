# ============================================================
# ENUMS
# ============================================================
# Use enums instead of magic strings/numbers.
# Critical for LLD — makes state machines, statuses, types explicit.

from enum import Enum, IntEnum, Flag, auto


# ---- 1. BASIC ENUM ----

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


print(Color.RED)            # Color.RED
print(Color.RED.name)       # RED
print(Color.RED.value)      # 1
print(Color(2))             # Color.GREEN — lookup by value
print(Color["BLUE"])        # Color.BLUE  — lookup by name

# Comparison
print(Color.RED == Color.RED)    # True
print(Color.RED == Color.GREEN)  # False
print(Color.RED is Color.RED)    # True — singletons

# Iteration
for c in Color:
    print(c.name, c.value)


# ---- 2. auto() — auto-assign values ----

class Direction(Enum):
    NORTH = auto()    # 1
    SOUTH = auto()    # 2
    EAST  = auto()    # 3
    WEST  = auto()    # 4

print(Direction.NORTH.value)   # 1


# ---- 3. STRING ENUM (common in APIs) ----

class OrderStatus(str, Enum):
    PENDING    = "PENDING"
    CONFIRMED  = "CONFIRMED"
    SHIPPED    = "SHIPPED"
    DELIVERED  = "DELIVERED"
    CANCELLED  = "CANCELLED"

status = OrderStatus.PENDING
print(status == "PENDING")     # True — str comparison works
print(f"Status: {status}")     # Status: PENDING  (not Status: OrderStatus.PENDING)


# ---- 4. ENUM WITH METHODS ----

class Planet(Enum):
    MERCURY = (3.303e+23, 2.4397e6)
    VENUS   = (4.869e+24, 6.0518e6)
    EARTH   = (5.976e+24, 6.37814e6)
    MARS    = (6.421e+23, 3.3972e6)

    def __init__(self, mass: float, radius: float):
        self.mass = mass
        self.radius = radius

    @property
    def surface_gravity(self) -> float:
        G = 6.67430e-11
        return G * self.mass / (self.radius ** 2)

    def weight_on_planet(self, earth_weight: float) -> float:
        return earth_weight * self.surface_gravity / Planet.EARTH.surface_gravity


print(f"Weight on Mars: {Planet.MARS.weight_on_planet(70):.2f} kg")


# ---- 5. IntEnum — enum that IS an int ----

class HttpStatus(IntEnum):
    OK          = 200
    CREATED     = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND   = 404
    SERVER_ERROR = 500

    @property
    def is_success(self) -> bool:
        return 200 <= self.value < 300

    @property
    def is_client_error(self) -> bool:
        return 400 <= self.value < 500


status = HttpStatus.NOT_FOUND
print(status > 400)         # False (404 > 400)
print(status.is_client_error)   # True


# ---- 6. Flag — for bitmask / permissions ----

class Permission(Flag):
    READ    = auto()    # 1
    WRITE   = auto()    # 2
    EXECUTE = auto()    # 4
    DELETE  = auto()    # 8

    # Composites
    READ_WRITE = READ | WRITE
    ADMIN = READ | WRITE | EXECUTE | DELETE


user_perms = Permission.READ | Permission.WRITE
print(user_perms)                        # Permission.READ|WRITE
print(Permission.READ in user_perms)     # True
print(Permission.DELETE in user_perms)   # False

admin_perms = Permission.ADMIN
print(Permission.EXECUTE in admin_perms)  # True


# ---- 7. REAL LLD USE CASE — State Machine with Enum ----

class VendingState(Enum):
    IDLE          = "IDLE"
    ITEM_SELECTED = "ITEM_SELECTED"
    PAYMENT       = "PAYMENT"
    DISPENSING    = "DISPENSING"
    OUT_OF_STOCK  = "OUT_OF_STOCK"


class VendingMachine:
    VALID_TRANSITIONS = {
        VendingState.IDLE:          [VendingState.ITEM_SELECTED, VendingState.OUT_OF_STOCK],
        VendingState.ITEM_SELECTED: [VendingState.PAYMENT, VendingState.IDLE],
        VendingState.PAYMENT:       [VendingState.DISPENSING, VendingState.IDLE],
        VendingState.DISPENSING:    [VendingState.IDLE],
        VendingState.OUT_OF_STOCK:  [VendingState.IDLE],
    }

    def __init__(self):
        self.state = VendingState.IDLE

    def transition(self, new_state: VendingState) -> None:
        if new_state not in self.VALID_TRANSITIONS[self.state]:
            raise ValueError(f"Invalid transition: {self.state} -> {new_state}")
        print(f"  {self.state.value} -> {new_state.value}")
        self.state = new_state


vm = VendingMachine()
vm.transition(VendingState.ITEM_SELECTED)
vm.transition(VendingState.PAYMENT)
vm.transition(VendingState.DISPENSING)
vm.transition(VendingState.IDLE)

try:
    vm.transition(VendingState.DISPENSING)  # invalid from IDLE
except ValueError as e:
    print(f"Error: {e}")

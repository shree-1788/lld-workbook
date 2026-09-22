# ============================================================
# DATACLASSES & TYPE HINTS
# ============================================================
# dataclasses auto-generate boilerplate (__init__, __repr__, __eq__)
# Type hints make code readable and enable static analysis (mypy).

from dataclasses import dataclass, field, asdict, astuple
from typing import Optional, Union, List, Dict, Tuple, Any, ClassVar
from typing import TypeVar, Generic


# ---- 1. BASIC DATACLASS ----

@dataclass
class Point:
    x: float
    y: float

p1 = Point(1.0, 2.0)
p2 = Point(1.0, 2.0)
print(p1)           # Point(x=1.0, y=2.0)   — auto __repr__
print(p1 == p2)     # True                   — auto __eq__


# ---- 2. DATACLASS WITH DEFAULTS ----

@dataclass
class Config:
    host: str = "localhost"
    port: int = 8080
    debug: bool = False
    tags: list = field(default_factory=list)   # NEVER use [] directly as default!

cfg = Config(port=9000)
print(cfg)   # Config(host='localhost', port=9000, debug=False, tags=[])


# ---- 3. FROZEN DATACLASS (immutable) ----

@dataclass(frozen=True)
class Coordinate:
    lat: float
    lng: float

coord = Coordinate(28.6, 77.2)
# coord.lat = 30.0   # FrozenInstanceError!
print(hash(coord))   # frozen dataclasses are hashable — can be dict keys


# ---- 4. ORDERED DATACLASS ----

@dataclass(order=True)
class Version:
    major: int
    minor: int
    patch: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


v1 = Version(1, 2, 0)
v2 = Version(2, 0, 0)
print(v1 < v2)     # True — compares (1,2,0) < (2,0,0) lexicographically
versions = [Version(1,10,0), Version(1,2,0), Version(2,0,0)]
print(sorted(versions))   # sorted automatically


# ---- 5. POST-INIT PROCESSING ----

@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)  # computed, not passed in constructor

    def __post_init__(self):
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Dimensions must be positive")
        self.area = self.width * self.height


r = Rectangle(4.0, 5.0)
print(r.area)    # 20.0


# ---- 6. DATACLASS UTILITIES ----

@dataclass
class Employee:
    name: str
    salary: float
    department: str

emp = Employee("Alice", 90000, "Engineering")
print(asdict(emp))     # {'name': 'Alice', 'salary': 90000, 'department': 'Engineering'}
print(astuple(emp))    # ('Alice', 90000, 'Engineering')


# ---- 7. TYPE HINTS DEEP DIVE ----

def process_data(
    items: List[int],
    mapping: Dict[str, Any],
    config: Optional[Config] = None,
    mode: Union[str, int] = "default",
) -> Tuple[int, str]:
    total = sum(items)
    return total, str(total)

# Modern syntax (Python 3.10+)
def modern_hints(
    items: list[int],
    mapping: dict[str, Any],
    config: Config | None = None,   # Union[X, None] == X | None
) -> tuple[int, str]:
    ...


# ---- 8. GENERICS ----

T = TypeVar("T")

@dataclass
class Stack(Generic[T]):
    _items: List[T] = field(default_factory=list)

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def peek(self) -> T:
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)


int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
print(int_stack.pop())   # 2

str_stack: Stack[str] = Stack()
str_stack.push("hello")
str_stack.push("world")
print(str_stack.peek())   # world


# ---- 9. ClassVar vs instance variable ----

@dataclass
class DatabasePool:
    host: str
    port: int
    max_connections: ClassVar[int] = 10   # class variable, not in __init__

    def __post_init__(self):
        print(f"Pool created for {self.host}:{self.port}, max={self.max_connections}")


pool = DatabasePool("localhost", 5432)
# DatabasePool.__init__ has only host, port — max_connections is ClassVar

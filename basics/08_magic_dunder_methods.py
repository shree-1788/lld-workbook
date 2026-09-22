# ============================================================
# MAGIC / DUNDER METHODS
# ============================================================
# Double underscore methods (__method__) let your class integrate
# with Python's built-in operations (len, print, +, [], in, etc.)

class Stack:
    def __init__(self):
        self._data: list = []

    # ---- REPRESENTATION ----
    def __str__(self) -> str:
        """Human-readable. Called by print() and str()."""
        return f"Stack{self._data}"

    def __repr__(self) -> str:
        """Developer-facing. Called in REPL and repr()."""
        return f"Stack(data={self._data!r})"

    # ---- CONTAINER BEHAVIOUR ----
    def __len__(self) -> int:
        """Called by len(obj)."""
        return len(self._data)

    def __contains__(self, item) -> bool:
        """Called by `item in obj`."""
        return item in self._data

    def __getitem__(self, index: int):
        """Called by obj[index]."""
        return self._data[index]

    def __iter__(self):
        """Called by for x in obj — makes the object iterable."""
        return iter(self._data)

    def __reversed__(self):
        """Called by reversed(obj)."""
        return reversed(self._data)

    # ---- MUTATION ----
    def push(self, item) -> None:
        self._data.append(item)

    def pop(self):
        return self._data.pop()

    # ---- COMPARISON ----
    def __eq__(self, other: object) -> bool:
        """Called by ==."""
        if not isinstance(other, Stack):
            return NotImplemented
        return self._data == other._data

    def __lt__(self, other: "Stack") -> bool:
        """Called by <. With __eq__, enables all comparisons via @functools.total_ordering."""
        return len(self) < len(other)

    # ---- BOOLEAN CONTEXT ----
    def __bool__(self) -> bool:
        """Called by if obj: — empty stack is falsy."""
        return len(self._data) > 0

    # ---- CALLABLE ----
    # Makes an instance callable like a function
    def __call__(self, item) -> None:
        self.push(item)

    # ---- CONTEXT MANAGER ----
    def __enter__(self):
        """Called by `with obj as x:`."""
        print("Stack context entered")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called when `with` block exits."""
        self._data.clear()
        print("Stack cleared on exit")
        return False   # don't suppress exceptions


s = Stack()
s.push(1); s.push(2); s.push(3)

print(s)                    # Stack[1, 2, 3]
print(repr(s))              # Stack(data=[1, 2, 3])
print(len(s))               # 3
print(2 in s)               # True
print(s[0])                 # 1
print(list(reversed(s)))    # [3, 2, 1]

for item in s:
    print(item, end=" ")    # 1 2 3
print()

s2 = Stack(); s2.push(1); s2.push(2); s2.push(3)
print(s == s2)              # True

print(bool(Stack()))        # False — empty stack is falsy
print(bool(s))              # True

s(99)                       # push via __call__
print(s)                    # Stack[1, 2, 3, 99]

with s as stack:
    stack.push(100)
    print(stack)            # Stack[1, 2, 3, 99, 100]
print(s)                    # Stack[] — cleared on exit


# ============================================================
# ARITHMETIC DUNDER METHODS (quick reference)
# ============================================================

class Money:
    def __init__(self, amount: float, currency: str = "USD"):
        self.amount = amount
        self.currency = currency

    def _check_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError(f"Cannot operate on {self.currency} and {other.currency}")

    def __add__(self, other: "Money") -> "Money":
        self._check_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        self._check_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, factor: float) -> "Money":
        return Money(self.amount * factor, self.currency)

    def __truediv__(self, divisor: float) -> "Money":
        return Money(self.amount / divisor, self.currency)

    def __iadd__(self, other: "Money") -> "Money":
        """In-place += ."""
        self._check_currency(other)
        self.amount += other.amount
        return self

    def __neg__(self) -> "Money":
        """Unary negation: -obj."""
        return Money(-self.amount, self.currency)

    def __abs__(self) -> "Money":
        return Money(abs(self.amount), self.currency)

    def __repr__(self) -> str:
        return f"{self.currency} {self.amount:.2f}"


m1 = Money(100)
m2 = Money(50)
print(m1 + m2)    # USD 150.00
print(m1 - m2)    # USD 50.00
print(m1 * 1.1)   # USD 110.00
print(m1 / 4)     # USD 25.00
m1 += m2
print(m1)         # USD 150.00


# ============================================================
# KEY DUNDER METHODS REFERENCE
# ============================================================
# __init__      constructor
# __str__       str(obj), print(obj)
# __repr__      repr(obj), REPL display
# __len__       len(obj)
# __getitem__   obj[key]
# __setitem__   obj[key] = val
# __delitem__   del obj[key]
# __contains__  item in obj
# __iter__      iter(obj), for loops
# __next__      next(obj) — for custom iterators
# __call__      obj()
# __enter__     with obj
# __exit__      end of with block
# __bool__      bool(obj), if obj
# __eq__        ==
# __lt__        <
# __add__       +
# __iadd__      +=
# __neg__       -obj (unary)
# __hash__      hash(obj), used in sets/dicts

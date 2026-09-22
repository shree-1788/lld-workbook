# ============================================================
# DECORATORS
# ============================================================
# A decorator is a function that wraps another function/class
# to add behaviour without modifying the original code.
# Heavily used in Python frameworks and LLD patterns.

import functools
import time


# ---- 1. BASIC FUNCTION DECORATOR ----

def timer(func):
    @functools.wraps(func)  # preserves original function's metadata
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.4f}s")
        return result
    return wrapper


@timer
def slow_sum(n: int) -> int:
    return sum(range(n))


print(slow_sum(1_000_000))   # prints result + time taken


# ---- 2. DECORATOR WITH ARGUMENTS ----

def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise RuntimeError(f"{func.__name__} failed after {max_attempts} attempts")
        return wrapper
    return decorator


@retry(max_attempts=3, delay=0)
def unstable_api_call(fail_count: list) -> str:
    if fail_count[0] > 0:
        fail_count[0] -= 1
        raise ConnectionError("Network error")
    return "Success!"

fails = [2]
print(unstable_api_call(fails))   # fails twice, succeeds on 3rd attempt


# ---- 3. CLASS-BASED DECORATOR ----

class Cache:
    """Memoization decorator using a class."""
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self._cache: dict = {}

    def __call__(self, *args):
        if args not in self._cache:
            self._cache[args] = self.func(*args)
        return self._cache[args]

    def clear(self) -> None:
        self._cache.clear()


@Cache
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(35))    # fast — cached results


# ---- 4. STACKING DECORATORS ----
# Applied bottom-up (closest decorator runs first).

def bold(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"**{func(*args, **kwargs)}**"
    return wrapper

def italic(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"_{func(*args, **kwargs)}_"
    return wrapper

@bold
@italic    # italic applied first, then bold wraps it
def greet(name: str) -> str:
    return f"Hello, {name}"

print(greet("Alice"))    # **_Hello, Alice_**


# ---- 5. CLASS DECORATOR ----
# A decorator that wraps a class, not a function.

def singleton(cls):
    """Makes a class a singleton."""
    instances = {}
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


@singleton
class Config:
    def __init__(self):
        self.debug = False
        self.db_url = "localhost:5432"


c1 = Config()
c2 = Config()
print(c1 is c2)     # True — same object


# ---- 6. PROPERTY AS DECORATOR (recap) ----
# @property, @x.setter, @x.deleter are built-in decorators.

class Circle:
    def __init__(self, radius: float):
        self._radius = radius

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self) -> float:
        import math
        return math.pi * self._radius ** 2


c = Circle(5)
c.radius = 10
print(c.area)        # 314.15...


# ---- 7. COMMON BUILT-IN DECORATORS ----
# @staticmethod    — no self, no cls
# @classmethod     — first arg is cls
# @property        — getter
# @functools.cache — memoization (Python 3.9+)
# @functools.lru_cache(maxsize=128) — capped memoization
# @dataclasses.dataclass — auto-generates __init__, __repr__, __eq__
# @abstractmethod  — marks abstract methods in ABC

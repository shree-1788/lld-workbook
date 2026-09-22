# ============================================================
# ITERATORS AND GENERATORS
# ============================================================
# Important for LLD when designing lazy/streaming data structures.

# ---- 1. ITERATOR PROTOCOL ----
# An object is an iterator if it has __iter__ and __next__.
# __iter__ returns self.
# __next__ returns next value or raises StopIteration.

class CountDown:
    def __init__(self, start: int):
        self.current = start

    def __iter__(self):
        return self    # this object IS the iterator

    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


for n in CountDown(5):
    print(n, end=" ")   # 5 4 3 2 1
print()

# Manual iteration
it = CountDown(3)
print(next(it))    # 3
print(next(it))    # 2
print(next(it))    # 1
# next(it)         # StopIteration


# ---- 2. ITERABLE vs ITERATOR ----
# Iterable  = has __iter__ (list, tuple, str, your custom class)
# Iterator  = has __iter__ AND __next__
# Every iterator is an iterable, not the other way around.

class NumberRange:
    """Iterable — creates a fresh iterator each time."""
    def __init__(self, start: int, stop: int):
        self.start = start
        self.stop = stop

    def __iter__(self):
        return NumberRangeIterator(self.start, self.stop)


class NumberRangeIterator:
    def __init__(self, start: int, stop: int):
        self.current = start
        self.stop = stop

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.current >= self.stop:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


r = NumberRange(1, 5)
print(list(r))    # [1, 2, 3, 4]
print(list(r))    # [1, 2, 3, 4] — fresh iterator each time (unlike a plain iterator)


# ---- 3. GENERATORS — the Pythonic way ----
# Use `yield` instead of implementing __iter__/__next__.
# State is automatically saved between yields.

def countdown(start: int):
    while start > 0:
        yield start
        start -= 1

gen = countdown(5)
print(next(gen))   # 5
print(next(gen))   # 4
for n in gen:
    print(n, end=" ")   # 3 2 1
print()


# ---- 4. GENERATOR EXPRESSION ----
# Like list comprehension but lazy — generates values on demand.

squares_list = [x**2 for x in range(10)]      # all in memory
squares_gen  = (x**2 for x in range(10))       # lazy

import sys
print(sys.getsizeof(squares_list))   # ~184 bytes
print(sys.getsizeof(squares_gen))    # ~200 bytes (constant regardless of size!)


# ---- 5. INFINITE GENERATOR ----

def natural_numbers(start: int = 1):
    n = start
    while True:
        yield n
        n += 1

def take(n: int, iterable):
    """Take first n items from any iterable."""
    for i, item in enumerate(iterable):
        if i >= n:
            break
        yield item

print(list(take(5, natural_numbers())))   # [1, 2, 3, 4, 5]


# ---- 6. yield from — delegating to sub-generator ----

def chain(*iterables):
    for it in iterables:
        yield from it    # flattens each iterable

print(list(chain([1, 2], [3, 4], [5])))   # [1, 2, 3, 4, 5]


# ---- 7. GENERATOR WITH SEND — coroutine-style ----

def accumulator():
    total = 0
    while True:
        value = yield total    # yield sends total OUT; receives value IN
        if value is None:
            break
        total += value

acc = accumulator()
next(acc)              # prime the generator (advance to first yield)
print(acc.send(10))    # 10
print(acc.send(20))    # 30
print(acc.send(5))     # 35


# ---- 8. PRACTICAL USE CASE — lazy file reader ----

def read_large_file_in_chunks(filepath: str, chunk_size: int = 1024):
    """Reads a file lazily in chunks — doesn't load entire file into memory."""
    with open(filepath, 'r') as f:
        while chunk := f.read(chunk_size):
            yield chunk

# for chunk in read_large_file_in_chunks("/path/to/large.txt"):
#     process(chunk)

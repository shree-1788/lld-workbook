# ============================================================
# CONTEXT MANAGERS
# ============================================================
# Manage resources automatically (open/close, lock/unlock, etc.)
# Used with `with` statement. Critical for LLD resource management.

# ---- 1. CLASS-BASED CONTEXT MANAGER ----

class DatabaseConnection:
    def __init__(self, host: str, db: str):
        self.host = host
        self.db = db
        self.connection = None

    def __enter__(self):
        print(f"Connecting to {self.db} at {self.host}...")
        self.connection = f"<Connection to {self.db}>"
        return self.connection   # bound to `as` variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Closing connection to {self.db}")
        self.connection = None

        # exc_type, exc_val, exc_tb are non-None if an exception occurred
        if exc_type:
            print(f"Exception inside with block: {exc_val}")
            return False   # False = don't suppress exception
        return True        # True = suppress exception (use rarely)


with DatabaseConnection("localhost", "mydb") as conn:
    print(f"Using {conn}")
    # Connection is automatically closed when block exits, even on exception


# ---- 2. GENERATOR-BASED CONTEXT MANAGER ----
# Use @contextmanager — simpler than a full class.

from contextlib import contextmanager


@contextmanager
def timer(label: str):
    import time
    start = time.perf_counter()
    try:
        yield   # code inside `with` runs here
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label}: {elapsed:.4f}s")


with timer("List creation"):
    data = list(range(1_000_000))


@contextmanager
def managed_file(path: str, mode: str = "r"):
    f = open(path, mode)
    try:
        yield f
    except Exception as e:
        print(f"Error while using file: {e}")
        raise
    finally:
        f.close()
        print(f"File {path} closed")


# with managed_file("/tmp/test.txt", "w") as f:
#     f.write("Hello!")


# ---- 3. LOCK CONTEXT MANAGER (thread safety) ----
import threading

class ThreadSafeCounter:
    def __init__(self):
        self._count = 0
        self._lock = threading.Lock()

    def increment(self) -> None:
        with self._lock:       # lock acquired, released automatically
            self._count += 1

    @property
    def value(self) -> int:
        return self._count


counter = ThreadSafeCounter()
threads = [threading.Thread(target=counter.increment) for _ in range(100)]
for t in threads: t.start()
for t in threads: t.join()
print(counter.value)   # 100 — safe with lock


# ---- 4. TRANSACTION CONTEXT MANAGER ----

class Transaction:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self._operations: list = []

    def execute(self, query: str) -> None:
        self._operations.append(query)
        print(f"Queued: {query}")

    def __enter__(self) -> "Transaction":
        print(f"BEGIN TRANSACTION on {self.db_name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"ROLLBACK — error: {exc_val}")
            self._operations.clear()
            return False   # re-raise the exception
        print(f"COMMIT — {len(self._operations)} operations")
        self._operations.clear()
        return False


with Transaction("orders_db") as txn:
    txn.execute("INSERT INTO orders VALUES (...)")
    txn.execute("UPDATE inventory SET stock = stock - 1")

print()

try:
    with Transaction("payments_db") as txn:
        txn.execute("INSERT INTO payments VALUES (...)")
        raise ValueError("Payment gateway error")   # simulates failure
except ValueError:
    pass


# ---- 5. NESTED CONTEXT MANAGERS ----

@contextmanager
def log_block(name: str):
    print(f">> {name} started")
    yield
    print(f">> {name} ended")


# Old style (nesting)
with log_block("outer"):
    with log_block("inner"):
        print("  doing work")

# Python 3.10+ style (multiple context managers in one `with`)
with log_block("A"), log_block("B"):
    print("  working in A and B")


# ---- 6. contextlib.suppress ----
from contextlib import suppress

with suppress(FileNotFoundError):
    open("/nonexistent/file.txt")   # silently ignored
print("Code continues after suppress")

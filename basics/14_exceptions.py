# ============================================================
# EXCEPTION HANDLING & CUSTOM EXCEPTIONS
# ============================================================
# Critical for LLD — proper exception hierarchies make error
# handling predictable and extensible.

# ---- 1. EXCEPTION HIERARCHY ----
# BaseException
#   ├── SystemExit
#   ├── KeyboardInterrupt
#   └── Exception
#       ├── ValueError
#       ├── TypeError
#       ├── AttributeError
#       ├── KeyError
#       ├── IndexError
#       ├── RuntimeError
#       └── ... (your custom exceptions go here)


# ---- 2. BASIC TRY/EXCEPT ----

def divide(a: float, b: float) -> float:
    try:
        return a / b
    except ZeroDivisionError:
        raise ValueError(f"Cannot divide {a} by zero")


# ---- 3. FULL TRY/EXCEPT/ELSE/FINALLY ----

def read_config(path: str) -> dict:
    try:
        f = open(path)
    except FileNotFoundError:
        print(f"Config not found: {path}")
        return {}
    except PermissionError as e:
        print(f"Permission denied: {e}")
        return {}
    else:
        # runs only if NO exception occurred in try
        data = f.read()
        f.close()
        return {"data": data}
    finally:
        # ALWAYS runs — even if try raises and we return in except
        print("read_config finished")


# ---- 4. CUSTOM EXCEPTION HIERARCHY ----
# Design your own exception tree for your domain.

class AppError(Exception):
    """Base exception for the entire application."""
    def __init__(self, message: str, code: int = 500):
        super().__init__(message)
        self.code = code
        self.message = message

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"


class ValidationError(AppError):
    """Raised when input validation fails."""
    def __init__(self, field: str, message: str):
        super().__init__(f"Validation failed for '{field}': {message}", code=400)
        self.field = field


class AuthenticationError(AppError):
    """Raised when authentication fails."""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code=401)


class AuthorizationError(AppError):
    """Raised when user lacks permission."""
    def __init__(self, action: str, resource: str):
        super().__init__(f"Not authorized to {action} on {resource}", code=403)


class NotFoundError(AppError):
    """Raised when a resource is not found."""
    def __init__(self, resource: str, identifier):
        super().__init__(f"{resource} with id={identifier} not found", code=404)


class ConflictError(AppError):
    """Raised when there's a conflict (e.g. duplicate)."""
    def __init__(self, message: str):
        super().__init__(message, code=409)


# ---- 5. USING CUSTOM EXCEPTIONS ----

class UserService:
    _users: dict = {"alice": {"password": "pass123", "role": "user"}}

    def get_user(self, username: str) -> dict:
        if username not in self._users:
            raise NotFoundError("User", username)
        return self._users[username]

    def login(self, username: str, password: str) -> str:
        user = self.get_user(username)   # may raise NotFoundError
        if user["password"] != password:
            raise AuthenticationError("Invalid password")
        return f"Token for {username}"

    def create_user(self, username: str, password: str) -> None:
        if username in self._users:
            raise ConflictError(f"User '{username}' already exists")
        if len(password) < 8:
            raise ValidationError("password", "must be at least 8 characters")
        self._users[username] = {"password": password, "role": "user"}


service = UserService()

# Catching by specific exception
try:
    service.login("bob", "pass")
except NotFoundError as e:
    print(e)   # [404] User with id=bob not found

# Catching by base class catches all subclasses
try:
    service.create_user("alice", "abc")
except ConflictError as e:
    print(e)   # [409] User 'alice' already exists
except ValidationError as e:
    print(e)

try:
    service.create_user("dave", "short")
except ValidationError as e:
    print(e)    # [400] Validation failed for 'password': must be at least 8 characters
    print(f"Field: {e.field}")


# ---- 6. EXCEPTION CHAINING ----

def parse_user_id(value: str) -> int:
    try:
        return int(value)
    except ValueError as e:
        # raise X from Y — links the original cause
        raise ValidationError("user_id", f"must be an integer, got '{value}'") from e


try:
    parse_user_id("abc")
except ValidationError as e:
    print(e)
    print(f"Caused by: {e.__cause__}")   # original ValueError


# ---- 7. CONTEXT MANAGER FOR EXCEPTION HANDLING ----

from contextlib import contextmanager

@contextmanager
def handle_app_errors():
    try:
        yield
    except ValidationError as e:
        print(f"Bad request: {e}")
    except NotFoundError as e:
        print(f"Not found: {e}")
    except AppError as e:
        print(f"App error: {e}")

with handle_app_errors():
    service.get_user("nonexistent")

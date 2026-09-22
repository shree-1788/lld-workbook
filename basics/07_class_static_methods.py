# ============================================================
# INSTANCE vs CLASS vs STATIC METHODS
# ============================================================

class Date:
    def __init__(self, day: int, month: int, year: int):
        self.day = day
        self.month = month
        self.year = year

    # ---- INSTANCE METHOD ----
    # First param is `self` — the object instance.
    # Can access and modify instance state.
    def get_formatted(self) -> str:
        return f"{self.day:02d}/{self.month:02d}/{self.year}"

    def is_leap_year(self) -> bool:
        return Date.check_leap_year(self.year)  # calls static method

    # ---- CLASS METHOD ----
    # First param is `cls` — the class itself.
    # Used as alternative constructors or factory methods.
    # Can access/modify class-level state.
    @classmethod
    def from_string(cls, date_str: str) -> "Date":
        """Create Date from 'dd-mm-yyyy' string."""
        day, month, year = map(int, date_str.split("-"))
        return cls(day, month, year)

    @classmethod
    def today(cls) -> "Date":
        """Create Date for today."""
        from datetime import date
        d = date.today()
        return cls(d.day, d.month, d.year)

    # ---- STATIC METHOD ----
    # No self, no cls. Just a utility function scoped to the class.
    # Can't access instance or class state.
    @staticmethod
    def check_leap_year(year: int) -> bool:
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    @staticmethod
    def validate_date(day: int, month: int, year: int) -> bool:
        if year < 1:
            return False
        if not 1 <= month <= 12:
            return False
        days_in_month = [31, 29 if Date.check_leap_year(year) else 28,
                         31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        return 1 <= day <= days_in_month[month - 1]

    def __repr__(self) -> str:
        return f"Date({self.day}, {self.month}, {self.year})"


# Instance method
d1 = Date(15, 8, 2024)
print(d1.get_formatted())       # 15/08/2024
print(d1.is_leap_year())        # True

# Class method — alternative constructors
d2 = Date.from_string("25-12-2023")
print(d2)                       # Date(25, 12, 2023)
d3 = Date.today()
print(d3)                       # today's date

# Static method — callable on class or instance
print(Date.check_leap_year(2000))   # True
print(Date.check_leap_year(1900))   # False
print(Date.validate_date(31, 2, 2024))  # False — Feb doesn't have 31 days
print(d1.check_leap_year(2024))     # True — callable on instance too


# ============================================================
# WHEN TO USE WHICH
# ============================================================
# Instance method  -> needs to read/write instance state (self.x)
# Class method     -> alternative constructor, factory, or needs class (cls)
# Static method    -> pure utility, logically belongs to class but no state


# ---- CLASS VARIABLE vs INSTANCE VARIABLE ----

class Counter:
    count = 0      # class variable — shared by all instances

    def __init__(self, name: str):
        self.name = name        # instance variable — unique per object
        Counter.count += 1

    @classmethod
    def get_count(cls) -> int:
        return cls.count

    @classmethod
    def reset(cls) -> None:
        cls.count = 0


c1 = Counter("first")
c2 = Counter("second")
c3 = Counter("third")

print(Counter.get_count())   # 3
print(c1.count)              # 3  — same shared variable
Counter.reset()
print(Counter.get_count())   # 0

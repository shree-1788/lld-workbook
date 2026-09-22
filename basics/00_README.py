# ============================================================
# PYTHON OOP & LLD BASICS — STUDY INDEX
# ============================================================
# Read the files in order. Each builds on the previous.
#
# File                              Topic
# ─────────────────────────────────────────────────────────
# 01_classes_and_objects.py      Classes, objects, __init__, __new__, class vs instance vars
# 02_encapsulation.py            Public/protected/private, @property, getters/setters
# 03_inheritance.py              Single, multilevel, multiple inheritance, super(), MRO
# 04_polymorphism.py             Method overriding, duck typing, operator overloading
# 05_abstraction.py              ABC, @abstractmethod, abstract properties
# 06_interfaces.py               Interface pattern, Protocol (structural subtyping)
# 07_class_static_methods.py     @classmethod, @staticmethod, when to use each
# 08_magic_dunder_methods.py     __str__, __len__, __iter__, __call__, context mgr, arithmetic
# 09_composition_vs_inheritance.py  HAS-A vs IS-A, Mixins, Strategy via composition
# 10_decorators.py               Function/class decorators, @property, stacking, @singleton
# 11_dataclasses_and_typing.py   @dataclass, type hints, Generics, frozen/ordered
# 12_iterators_and_generators.py Iterator protocol, yield, generator expressions, yield from
# 13_context_managers.py         __enter__/__exit__, @contextmanager, threading.Lock
# 14_exceptions.py               Custom exception hierarchies, chaining, best practices
# 15_enums.py                    Enum, IntEnum, Flag, auto(), enums in state machines
# 16_lld_patterns_primer.py      Singleton, Factory, Observer, Strategy, Decorator pattern
#
# ─────────────────────────────────────────────────────────
# CORE PILLARS OF OOP (quick mental map)
# ─────────────────────────────────────────────────────────
#
#  ENCAPSULATION  — bundle data + behaviour, control access
#                   tools: private(__x), protected(_x), @property
#
#  INHERITANCE    — reuse code via IS-A hierarchy
#                   tools: class Child(Parent), super(), MRO
#
#  POLYMORPHISM   — same interface, different behaviour
#                   tools: method overriding, duck typing, dunder methods
#
#  ABSTRACTION    — hide details, expose contracts
#                   tools: ABC, @abstractmethod, Protocol
#
# ─────────────────────────────────────────────────────────
# KEY PYTHON-SPECIFIC CONCEPTS TO MASTER FOR LLD
# ─────────────────────────────────────────────────────────
#
#  @property          — Pythonic encapsulation
#  @classmethod       — alternative constructors / factories
#  @staticmethod      — pure utilities scoped to a class
#  Dunder methods     — integrate with Python's built-in ops
#  ABC + Protocol     — interface contracts
#  Enum               — safe constants, state machines
#  dataclass          — lightweight value objects / DTOs
#  Composition        — prefer over deep inheritance
#  Context managers   — resource lifecycle management
#  Generators         — lazy data pipelines
#  Custom exceptions  — domain-specific error hierarchy

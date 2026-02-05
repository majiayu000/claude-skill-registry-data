---
name: SOLID Principles Code Review
description: Review Python code for adherence to SOLID principles (SRP, OCP, LSP, ISP, DIP). Use when reviewing Python code for maintainability, testability, and design quality.
---

# SOLID Principles Code Review

## Overview

This skill evaluates Python code against the five SOLID principles of object-oriented design. SOLID principles guide the creation of maintainable, flexible, and testable code.

**Scope**: This skill focuses exclusively on SOLID principle violations and design patterns, not general code quality, performance, or formatting issues.

**The Five Principles:**
- **S**ingle Responsibility Principle (SRP): One class, one responsibility
- **O**pen/Closed Principle (OCP): Open for extension, closed for modification
- **L**iskov Substitution Principle (LSP): Subclasses must be substitutable for parent classes
- **I**nterface Segregation Principle (ISP): Many small interfaces > one large interface
- **D**ependency Inversion Principle (DIP): Depend on abstractions, not concrete implementations

## When to Use

- Reviewing new features or refactoring code
- Evaluating code maintainability and testability
- Identifying design issues that make code hard to change
- Before merging significant architectural changes
- When code is becoming difficult to test or extend

## Process

Focus only on SOLID principle violations.

### Step 1: Single Responsibility Principle (SRP)

**Look for:**
- Classes with multiple reasons to change
- Methods that do more than one thing
- Mixed concerns (e.g., business logic + database access)
- Boolean flags that change method behavior
- Long classes (>200 lines often indicates multiple responsibilities)

**Red Flags:**
```python
# BAD: Multiple responsibilities
class Order:
    def calculate_total(self): pass  # Calculation
    def save_to_database(self): pass  # Persistence
    def send_email(self): pass        # Notification
```

**Good Pattern:**
```python
# GOOD: Single responsibilities
class Order:
    pass  # Just data

class OrderCalculator:
    def calculate_total(self, order): pass

class OrderRepository:
    def save(self, order): pass

class OrderNotifier:
    def send_confirmation(self, order): pass
```

### Step 2: Open/Closed Principle (OCP)

**Look for:**
- if-elif chains checking types or categories
- Type checking with `isinstance()` or `type()`
- Methods that must be modified to add new functionality
- Hard-coded lists of types

**Red Flags:**
```python
# BAD: Must modify for new shapes
def calculate_area(shape):
    if shape.type == "circle":
        return 3.14 * shape.radius ** 2
    elif shape.type == "rectangle":
        return shape.width * shape.height
    # Adding triangle requires modifying this function
```

**Good Pattern:**
```python
# GOOD: Extend via inheritance or protocol
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def calculate_area(self): pass

class Circle(Shape):
    def calculate_area(self):
        return 3.14 * self.radius ** 2

class Rectangle(Shape):
    def calculate_area(self):
        return self.width * self.height
```

### Step 3: Liskov Substitution Principle (LSP)

**Look for:**
- Subclasses throwing exceptions that parent doesn't throw
- Empty method implementations or `NotImplementedError`
- Subclasses requiring more restrictive inputs than parent
- Type checking before calling methods (indicates substitution doesn't work)
- Subclasses that weaken postconditions or strengthen preconditions

**Red Flags:**
```python
# BAD: Square can't substitute for Rectangle
class Rectangle:
    def set_width(self, width):
        self._width = width
    def set_height(self, height):
        self._height = height

class Square(Rectangle):
    def set_width(self, width):
        self._width = width
        self._height = width  # Unexpected side effect!
```

**Good Pattern:**
```python
# GOOD: Proper abstraction hierarchy
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def get_area(self): pass

class Rectangle(Shape):
    def get_area(self):
        return self._width * self._height

class Square(Shape):  # Not a Rectangle!
    def get_area(self):
        return self._side ** 2
```

### Step 4: Interface Segregation Principle (ISP)

**Look for:**
- Large abstract classes with many methods (>5-7 methods)
- Implementations with empty methods or `NotImplementedError`
- Classes implementing interfaces but only using a subset
- Comments like "not applicable" or "not supported"

**Red Flags:**
```python
# BAD: Fat interface forces all implementations
from abc import ABC, abstractmethod

class MultiFunctionDevice(ABC):
    @abstractmethod
    def print_document(self, doc): pass
    @abstractmethod
    def scan_document(self): pass
    @abstractmethod
    def fax_document(self, doc): pass

class SimplePrinter(MultiFunctionDevice):
    def print_document(self, doc):
        print(doc)
    def scan_document(self):
        raise NotImplementedError  # Forced to implement!
    def fax_document(self, doc):
        raise NotImplementedError  # Forced to implement!
```

**Good Pattern:**
```python
# GOOD: Small, focused interfaces
from abc import ABC, abstractmethod

class Printer(ABC):
    @abstractmethod
    def print_document(self, doc): pass

class Scanner(ABC):
    @abstractmethod
    def scan_document(self): pass

class SimplePrinter(Printer):
    def print_document(self, doc):
        print(doc)

class MultiFunctionPrinter(Printer, Scanner):
    def print_document(self, doc):
        print(doc)
    def scan_document(self):
        return "scanned"
```

### Step 5: Dependency Inversion Principle (DIP)

**Look for:**
- Direct imports and instantiation of concrete classes in business logic
- Hard-coded dependencies created inside `__init__`
- Difficult-to-test code requiring real databases/files/network
- High-level modules depending on low-level implementation details

**Red Flags:**
```python
# BAD: Direct dependency on concrete implementation
import sqlite3

class UserService:
    def __init__(self):
        # Hard-coded dependency
        self.db = sqlite3.connect('users.db')

    def register_user(self, name, email):
        # Business logic coupled to SQLite
        self.db.execute("INSERT INTO users VALUES (?, ?)", (name, email))
```

**Good Pattern:**
```python
# GOOD: Depend on abstraction via injection
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def save(self, user_data): pass

class SQLiteUserRepository(UserRepository):
    def __init__(self, db_path):
        self.db = sqlite3.connect(db_path)
    def save(self, user_data):
        self.db.execute("INSERT INTO users VALUES (?, ?)",
                       (user_data['name'], user_data['email']))

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository  # Injected dependency

    def register_user(self, name, email):
        self.repository.save({'name': name, 'email': email})
```

### Step 6: Python-Specific Considerations

**Prefer:**
- `Protocol` over `ABC` for structural subtyping (when runtime enforcement not needed)
- Type hints to make dependencies explicit
- Dataclasses for data structures (supports SRP)
- Decorators for cross-cutting concerns (supports OCP)
- Constructor injection for dependency injection (simplest DIP approach)

**Example with Protocol:**
```python
from typing import Protocol

class Repository(Protocol):
    def save(self, data: dict) -> None: ...
    def find(self, id: str) -> dict | None: ...

# No inheritance needed - duck typing with type hints
class InMemoryRepository:
    def save(self, data: dict) -> None: pass
    def find(self, id: str) -> dict | None: pass
```

## Output Format

For each SOLID violation found:

---
**File**: [file path]
**Lines**: [line range, e.g., "45-52" or "78"]
**Principle**: [SRP|OCP|LSP|ISP|DIP]
**Issue**: [brief description of the violation]
**Impact**: [why this matters - testability, maintainability, flexibility]
**Suggestion**: [specific refactoring approach or pattern to apply]
**Example**: [code snippet showing the improved design, if helpful]
---

## Decision Rules

### When to Flag Issues

**Always flag:**
- `NotImplementedError` in production code (ISP/LSP violation)
- Multiple `isinstance()` checks for behavior switching (OCP violation)
- Can't write unit tests without real database/network (DIP violation)
- Classes over 500 lines (likely SRP violation)
- Subclasses throwing exceptions parent doesn't throw (LSP violation)

**Flag if significant:**
- Classes with 5+ distinct responsibilities (SRP)
- Abstract classes with 7+ methods (ISP)
- Long parameter lists (might indicate missing abstractions - DIP)
- Type-based conditionals (OCP)

**Don't flag:**
- Simple scripts (<100 lines total) - SOLID overkill for simple code
- Prototypes or proof-of-concept code
- Business rule conditionals (e.g., `if total > 100:`) - these are logic, not type switching
- One-time migration scripts
- Proper use of Python idioms (duck typing, EAFP style)

### Balancing Pragmatism

SOLID principles are guidelines, not absolute rules. Consider:

- **Code lifecycle**: Is this code actively maintained or rarely changed?
- **Team context**: Will abstractions help or confuse the team?
- **Actual pain points**: Is the code currently causing problems?
- **Project size**: Small projects need less abstraction than large systems

**Suggest refactoring when:**
- Code is hard to test
- Code changes frequently break unrelated features
- Adding new features requires modifying existing code
- Team struggles to understand or modify the code

**Defer refactoring when:**
- Code works and rarely changes
- Refactoring is purely academic
- Risk of bugs outweighs benefits
- Code is scheduled for deprecation

## Anti-patterns

- ❌ **Don't**: Flag every conditional as an OCP violation
  - ✅ **Do**: Only flag type-based conditionals that require modification for new types

- ❌ **Don't**: Suggest SOLID refactoring for simple scripts
  - ✅ **Do**: Consider code context and lifecycle before suggesting abstractions

- ❌ **Don't**: Recommend ABC when Protocol would work better
  - ✅ **Do**: Prefer Protocol for flexibility unless runtime enforcement needed

- ❌ **Don't**: Focus only on violations without explaining impact
  - ✅ **Do**: Explain why the violation matters (testability, maintainability, etc.)

- ❌ **Don't**: Suggest over-engineering with excessive abstraction layers
  - ✅ **Do**: Recommend the simplest solution that solves the actual problem

## Examples

### Example 1: SRP Violation

**Context**: Order class doing too much

**Code:**
```python
class Order:
    def calculate_total(self):
        return sum(item.price for item in self.items)

    def save_to_database(self, db):
        db.execute("INSERT INTO orders VALUES (?)", (self.total,))

    def send_confirmation_email(self, email_service):
        email_service.send("Order confirmed", self.customer_email)
```

**Review Output:**
```
---
**File**: order.py
**Lines**: 1-8
**Principle**: SRP
**Issue**: Order class has three responsibilities: calculation, persistence, and notification
**Impact**: Changes to email format require modifying Order class; difficult to test calculation logic without mocking database and email
**Suggestion**: Extract into separate classes: OrderCalculator, OrderRepository, OrderNotificationService
**Example**:
class Order:
    pass  # Data only

class OrderCalculator:
    def calculate_total(self, order):
        return sum(item.price for item in order.items)

class OrderRepository:
    def save(self, order, db):
        db.execute("INSERT INTO orders VALUES (?)", (order.total,))

class OrderNotifier:
    def send_confirmation(self, order, email_service):
        email_service.send("Order confirmed", order.customer_email)
---
```

### Example 2: DIP Violation

**Context**: Service depends on concrete implementation

**Code:**
```python
import sqlite3

class UserService:
    def __init__(self):
        self.db = sqlite3.connect('users.db')

    def create_user(self, name, email):
        self.db.execute("INSERT INTO users VALUES (?, ?)", (name, email))
```

**Review Output:**
```
---
**File**: user_service.py
**Lines**: 3-8
**Principle**: DIP
**Issue**: UserService directly depends on SQLite implementation; cannot test without real database
**Impact**: Impossible to write unit tests with mocks; cannot switch to different database without modifying UserService
**Suggestion**: Introduce repository abstraction and inject via constructor
**Example**:
from typing import Protocol

class UserRepository(Protocol):
    def save(self, name: str, email: str) -> None: ...

class SQLiteUserRepository:
    def __init__(self, db_path: str):
        self.db = sqlite3.connect(db_path)
    def save(self, name: str, email: str) -> None:
        self.db.execute("INSERT INTO users VALUES (?, ?)", (name, email))

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    def create_user(self, name: str, email: str) -> None:
        self.repository.save(name, email)

# Easy to test with mock
mock_repo = Mock(spec=UserRepository)
service = UserService(mock_repo)
---
```

## Testing This Skill (TDD Validation)

Test cases are located in `skills/collaboration/solid-principles-review/examples/`:

1. **example-1-srp-violation**: Order class with multiple responsibilities
   - Expected: Flag calculation + persistence + notification in one class

2. **example-2-ocp-violation**: Type-based conditionals requiring modification
   - Expected: Flag if-elif chain checking shape types

3. **example-3-dip-violation**: Hard-coded database dependency
   - Expected: Flag direct SQLite instantiation in business logic

4. **example-4-complex-good**: Well-designed code following SOLID
   - Expected: Find zero violations or only minor improvements

Run tests by launching subagents with:
```
Apply skills/collaboration/solid-principles-review/SKILL.md to review [test file path]
```

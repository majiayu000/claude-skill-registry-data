---
name: refactoring
description: >
  Safely improve software internal design and maintainability without altering
  external behavior or breaking API contracts. Use when applying Martin Fowler
  refactoring patterns (Extract Function, Replace Conditional with Polymorphism,
  Introduce Parameter Object), reducing technical debt, keeping regression tests
  passing continuously, or breaking monolithic functions into modular units.
compatibility: >
  Agent Skills-compatible coding agents refactoring codebases with an existing test suite.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "refactoring, clean-code, technical-debt, patterns, testing, maintainability"
  topics: "software-development"
---

# Safe Code Refactoring

Refactoring is the disciplined process of restructuring existing code—improving its readability, modularity, and internal architecture—**without changing its external observable behavior**. Safe refactoring requires a reliable test suite, small incremental steps, continuous verification, and strict preservation of public API contracts.

## Core Rules

1. **Never refactor without a passing test suite**: Ensure all tests are green *before* starting. If tests are missing, write characterization tests first.
2. **Never change behavior and refactor at the same time**: Separate structural changes from behavioral fixes or new features into distinct git commits.
3. **Take small, incremental steps**: Make one structural transformation at a time, run the test suite, and commit when green.
4. **Preserve public API contracts**: If renaming or restructuring a public function, leave a deprecated backward-compatible wrapper or alias during the transition.
5. **Listen to code smells**: Refactor in response to concrete code smells (Long Function, Large Class, Feature Envy, Primitive Obsession, Duplicated Code).

---

## 1. Essential Refactoring Patterns

### Pattern 1: Extract Function / Method
Turn a chunk of code within a long function that can be grouped together into its own function whose name explains its purpose:

```python
# BEFORE: Monolithic function with mixed abstraction levels
def print_owing(invoice):
    print_banner()

    # Calculate outstanding
    outstanding = 0.0
    for order in invoice.orders:
        outstanding += order.amount

    # Print details
    print(f"Customer: {invoice.customer}")
    print(f"Amount:   {outstanding}")

# AFTER: Extracted dedicated functions
def print_owing(invoice):
    print_banner()
    outstanding = calculate_outstanding(invoice.orders)
    print_details(invoice.customer, outstanding)

def calculate_outstanding(orders: list[Order]) -> float:
    return sum(order.amount for order in orders)

def print_details(customer: str, outstanding: float) -> None:
    print(f"Customer: {customer}")
    print(f"Amount:   {outstanding}")
```

---

### Pattern 2: Replace Conditional with Polymorphism
Eliminate brittle `switch` or `if/elif/else` ladders that check type codes:

```python
# BEFORE: Fragile type check branching
class Employee:
    def get_pay(self):
        if self.type == "ENGINEER":
            return self.base_salary
        elif self.type == "SALES":
            return self.base_salary + self.commission
        elif self.type == "MANAGER":
            return self.base_salary + self.bonus

# AFTER: Polymorphic strategy / subclassing
class Employee(Protocol):
    def get_pay(self) -> float: ...

class Engineer:
    def __init__(self, base_salary: float):
        self.base_salary = base_salary

    def get_pay(self) -> float:
        return self.base_salary

class SalesPerson:
    def __init__(self, base_salary: float, commission: float):
        self.base_salary = base_salary
        self.commission = commission

    def get_pay(self) -> float:
        return self.base_salary + self.commission
```

---

### Pattern 3: Introduce Parameter Object (Preserving Primitive Obsession)
When groups of parameters naturally travel together:

```python
# BEFORE: 6 separate parameters passed around
def search_entries(query: str, start_date: str, end_date: str, max_results: int, offset: int, sort_order: str): ...

# AFTER: Cohesive value object
from dataclasses import dataclass

@dataclass(frozen=True)
class SearchFilter:
    query: str
    date_range: tuple[str, str]
    limit: int = 50
    offset: int = 0
    sort_order: str = "desc"

def search_entries(filter_params: SearchFilter): ...
```

---

## 2. The Refactoring Workflow

```
1. Verify Green: Run existing test suite (`pytest`, `cargo test`). Must be 100% passing.
      │
      ▼
2. Small Refactoring Step: Apply a single mechanical change (e.g. Extract Function).
      │
      ▼
3. Run Tests Immediately: Verify tests remain 100% green.
      │
      ├──> [Tests Failed] ──> Revert immediately (`git restore .`), do not debug.
      │
      ▼ [Tests Passed]
4. Git Commit: `refactor(core): extract calculate_outstanding helper`
      │
      ▼
5. Repeat: Take next small step.
```

---

## 3. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| Mixing refactoring with new feature work | Makes diffs impossible to review; hard to bisect regressions | Separate commits: one for refactor, one for feature |
| "Big Bang" refactoring across 30 files | Test suite breaks, changes cannot be merged | Incremental commits: keep master branch shippable |
| Breaking public API signatures | Breaks downstream client code | Use deprecation wrappers or optional parameters |
| Refactoring without test coverage | Unnoticed behavioral regressions | Write characterization tests first |

---

## 4. Verification Checklist

- [ ] All tests passed before refactoring began.
- [ ] No changes to public API function signatures without backward-compatible shims.
- [ ] All tests pass after every refactoring step.
- [ ] Git commit history shows clean, focused `refactor(...)` commits.
- [ ] Code metrics (cyclomatic complexity, line count) improved.

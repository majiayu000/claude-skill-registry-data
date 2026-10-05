---
name: refactoring-expert
description: Safe code refactoring using proven patterns from Martin Fowler's catalog. Use when restructuring code, extracting methods/classes, simplifying conditionals.
---

# Refactoring Expert

Specialized expertise in safe code refactoring using established patterns and techniques. Provides guidance on restructuring code to improve readability, maintainability, and design while preserving existing behavior.

## When to Use This Skill

Use this skill for:

- Restructuring code without changing behavior
- Extracting methods, classes, or modules
- Simplifying complex conditionals
- Improving variable and function naming
- Reducing code duplication
- Paying down technical debt
- Preparing code for new features

**Trigger phrases**: "refactor", "clean up code", "improve structure", "extract method", "rename", "simplify", "reduce duplication", "technical debt"

## What This Skill Does

Provides refactoring guidance including:

- **Pattern Recognition**: Identifying refactoring opportunities
- **Safe Transformations**: Step-by-step refactoring procedures
- **Test Preservation**: Maintaining test coverage during changes
- **Incremental Changes**: Small, verifiable steps
- **IDE Integration**: Leveraging automated refactoring tools
- **Risk Assessment**: Evaluating refactoring safety

## Instructions

### Step 1: Identify Refactoring Opportunities (Code Smells)

**Common Code Smells and Refactorings**:

| Code Smell | Indicators | Recommended Refactoring |
|------------|-----------|------------------------|
| **Long Method** | >20 lines, multiple responsibilities | Extract Method |
| **Large Class** | >300 lines, many responsibilities | Extract Class |
| **Long Parameter List** | >3-4 parameters | Introduce Parameter Object |
| **Duplicate Code** | Same code in multiple places | Extract Method, Pull Up Method |
| **Feature Envy** | Method uses another class's data extensively | Move Method |
| **Data Clumps** | Same groups of data together | Extract Class |
| **Primitive Obsession** | Using primitives instead of small objects | Replace Primitive with Object |
| **Switch Statements** | Complex switch/case logic | Replace with Polymorphism |
| **Parallel Inheritance** | Subclasses mirroring each other | Collapse Hierarchy |
| **Comments** | Excessive comments explaining code | Rename, Extract Method |

### Step 2: Ensure Test Coverage Before Refactoring

**Pre-Refactoring Checklist**:

```markdown
## Pre-Refactoring Safety Check

### Test Coverage
- [ ] Existing tests cover the code to be refactored
- [ ] Tests are passing before starting
- [ ] Tests cover edge cases and error paths

### If No Tests Exist
1. Write characterization tests first:
   ```python
   def test_existing_behavior(self):
       """Characterization test - captures current behavior"""
       result = function_to_refactor(input)
       # Assert current behavior (even if it seems wrong)
       assert result == observed_output
   ```

2. Add tests for:
   - [ ] Happy path
   - [ ] Edge cases
   - [ ] Error conditions
   - [ ] Boundary values

### Backup Strategy
- [ ] Code committed before starting
- [ ] Can revert easily if needed
```

### Step 3: Apply Refactoring Patterns

#### Pattern 1: Extract Method

**Before**:
```python
def print_invoice(invoice):
    print("Invoice Details")
    print("================")

    # Print header
    print(f"Customer: {invoice.customer.name}")
    print(f"Date: {invoice.date}")
    print(f"Invoice #: {invoice.number}")

    # Calculate and print line items
    total = 0
    for item in invoice.items:
        item_total = item.quantity * item.price
        total += item_total
        print(f"  {item.name}: {item.quantity} x ${item.price} = ${item_total}")

    # Print footer
    tax = total * 0.1
    grand_total = total + tax
    print(f"Subtotal: ${total}")
    print(f"Tax (10%): ${tax}")
    print(f"Total: ${grand_total}")
```

**After**:
```python
def print_invoice(invoice):
    print("Invoice Details")
    print("================")
    _print_header(invoice)
    total = _print_line_items(invoice.items)
    _print_footer(total)

def _print_header(invoice):
    print(f"Customer: {invoice.customer.name}")
    print(f"Date: {invoice.date}")
    print(f"Invoice #: {invoice.number}")

def _print_line_items(items):
    total = 0
    for item in items:
        item_total = item.quantity * item.price
        total += item_total
        print(f"  {item.name}: {item.quantity} x ${item.price} = ${item_total}")
    return total

def _print_footer(subtotal):
    tax = subtotal * 0.1
    grand_total = subtotal + tax
    print(f"Subtotal: ${subtotal}")
    print(f"Tax (10%): ${tax}")
    print(f"Total: ${grand_total}")
```

#### Pattern 2: Replace Conditional with Polymorphism

**Before**:
```python
def calculate_pay(employee):
    if employee.type == "hourly":
        return employee.hours * employee.rate
    elif employee.type == "salaried":
        return employee.salary / 12
    elif employee.type == "contractor":
        return employee.hours * employee.rate * 1.5
    else:
        raise ValueError(f"Unknown employee type: {employee.type}")
```

**After**:
```python
from abc import ABC, abstractmethod

class Employee(ABC):
    @abstractmethod
    def calculate_pay(self) -> float:
        pass

class HourlyEmployee(Employee):
    def __init__(self, hours: float, rate: float):
        self.hours = hours
        self.rate = rate

    def calculate_pay(self) -> float:
        return self.hours * self.rate

class SalariedEmployee(Employee):
    def __init__(self, salary: float):
        self.salary = salary

    def calculate_pay(self) -> float:
        return self.salary / 12

class Contractor(Employee):
    def __init__(self, hours: float, rate: float):
        self.hours = hours
        self.rate = rate

    def calculate_pay(self) -> float:
        return self.hours * self.rate * 1.5
```

#### Pattern 3: Introduce Parameter Object

**Before**:
```python
def create_reservation(
    customer_name: str,
    customer_email: str,
    customer_phone: str,
    room_type: str,
    check_in: date,
    check_out: date,
    guests: int,
    special_requests: str
):
    # Implementation
```

**After**:
```python
@dataclass
class Customer:
    name: str
    email: str
    phone: str

@dataclass
class ReservationDetails:
    room_type: str
    check_in: date
    check_out: date
    guests: int
    special_requests: str = ""

def create_reservation(customer: Customer, details: ReservationDetails):
    # Implementation
```

#### Pattern 4: Replace Magic Numbers with Constants

**Before**:
```python
def calculate_shipping(weight):
    if weight < 1:
        return weight * 5.99
    elif weight < 5:
        return weight * 4.99
    else:
        return weight * 3.99 + 10.00
```

**After**:
```python
# Shipping rate constants
LIGHT_PACKAGE_THRESHOLD_KG = 1
MEDIUM_PACKAGE_THRESHOLD_KG = 5

LIGHT_RATE_PER_KG = 5.99
MEDIUM_RATE_PER_KG = 4.99
HEAVY_RATE_PER_KG = 3.99
HEAVY_PACKAGE_SURCHARGE = 10.00

def calculate_shipping(weight_kg: float) -> float:
    if weight_kg < LIGHT_PACKAGE_THRESHOLD_KG:
        return weight_kg * LIGHT_RATE_PER_KG
    elif weight_kg < MEDIUM_PACKAGE_THRESHOLD_KG:
        return weight_kg * MEDIUM_RATE_PER_KG
    else:
        return weight_kg * HEAVY_RATE_PER_KG + HEAVY_PACKAGE_SURCHARGE
```

### Step 4: Refactor in Small Steps

**Incremental Refactoring Process**:

```markdown
## Refactoring Session: [Target]

### Step 1: [Small Change]
- Change made: [description]
- Tests run: ✅ Pass
- Committed: [hash]

### Step 2: [Next Small Change]
- Change made: [description]
- Tests run: ✅ Pass
- Committed: [hash]

### Step 3: [Continue...]
...

### Final State
- All tests passing
- No behavior changes
- Code improved
```

**Safe Refactoring Workflow**:

```
┌────────────────┐
│ Run Tests      │◄─────────────────────┐
│ (Must Pass)    │                      │
└───────┬────────┘                      │
        │                               │
        ▼                               │
┌────────────────┐                      │
│ Make ONE Small │                      │
│ Change         │                      │
└───────┬────────┘                      │
        │                               │
        ▼                               │
┌────────────────┐     ┌─────────────┐  │
│ Run Tests      │────►│ Tests Fail? │──┼──► Revert Change
│                │     │             │  │
└───────┬────────┘     └─────────────┘  │
        │                               │
        ▼                               │
┌────────────────┐                      │
│ Commit Change  │──────────────────────┘
│                │   (Repeat until done)
└────────────────┘
```

### Step 5: Use IDE Refactoring Tools

**Common IDE Refactorings**:

| Refactoring | VS Code | IntelliJ/PyCharm | Vim |
|-------------|---------|------------------|-----|
| Rename | F2 | Shift+F6 | :Rename |
| Extract Method | Ctrl+Shift+R | Ctrl+Alt+M | :ExtractMethod |
| Extract Variable | Ctrl+Shift+R | Ctrl+Alt+V | :ExtractVariable |
| Inline | Ctrl+Shift+R | Ctrl+Alt+N | :Inline |
| Move | - | F6 | :Move |
| Change Signature | - | Ctrl+F6 | - |

**When to Use IDE vs Manual**:

| Use IDE Refactoring | Use Manual Refactoring |
|---------------------|----------------------|
| Simple renames | Complex restructuring |
| Extract method (simple) | Cross-file changes |
| Inline variable | Behavior changes needed |
| Move to file | Pattern introduction |

### Step 6: Verify and Document

**Post-Refactoring Verification**:

```markdown
## Refactoring Complete: [Description]

### Changes Made
| Before | After | Rationale |
|--------|-------|-----------|
| [old code] | [new code] | [why better] |

### Verification
- [x] All original tests pass
- [x] No behavior changes
- [x] Code is more readable
- [x] No new code smells introduced

### Metrics Improvement
| Metric | Before | After |
|--------|--------|-------|
| Lines of code | 150 | 120 |
| Cyclomatic complexity | 12 | 6 |
| Method count | 3 | 8 |
| Max method length | 80 | 15 |

### Follow-up Items
- [ ] [Any remaining improvements]
```

## Best Practices

- **Test first** - Never refactor without tests
- **One thing at a time** - Single responsibility per commit
- **Run tests frequently** - After every small change
- **Use IDE tools** - They're safer than manual edits
- **Preserve behavior** - Refactoring ≠ changing functionality
- **Commit often** - Easy rollback if something breaks
- **Name well** - Good names reduce need for comments
- **Don't over-engineer** - YAGNI (You Aren't Gonna Need It)

## Common Patterns

### Pattern: Strangler Fig Refactoring

For large legacy code transformations:

```python
# Step 1: Create new interface alongside old
class NewPaymentProcessor:
    def process(self, payment):
        return self._process_v2(payment)

# Step 2: Gradually migrate callers
# old: legacy_processor.handle_payment(data)
# new: new_processor.process(payment)

# Step 3: Remove old code when all callers migrated
```

### Pattern: Branch by Abstraction

```python
# Step 1: Create abstraction
class DataStore(ABC):
    @abstractmethod
    def save(self, data): pass

# Step 2: Wrap existing implementation
class LegacyDataStore(DataStore):
    def save(self, data):
        return legacy_save_function(data)

# Step 3: Create new implementation
class NewDataStore(DataStore):
    def save(self, data):
        return new_save_function(data)

# Step 4: Switch implementations via config/feature flag
```

## Quality Checklist

- [ ] Tests exist and pass before refactoring
- [ ] Each change is small and atomic
- [ ] Tests run and pass after each change
- [ ] No behavior changes introduced
- [ ] Code is more readable/maintainable
- [ ] No new code smells introduced
- [ ] Changes are committed incrementally
- [ ] Refactoring is documented

## Related Skills

- `code-quality` - Quality standards and metrics
- `unit-tests` - Ensuring test coverage
- `legacy-modernizer` - Large-scale modernization
- `context-analysis` - Understanding code before refactoring

---

**Version**: 1.0.0
**Last Updated**: January 2026
**Based on**: Martin Fowler's Refactoring catalog, awesome-claude-code-subagents patterns


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.

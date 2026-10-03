---
name: refactoring
description: Safely refactor code to improve structure, readability, and maintainability without changing behavior. Use proven techniques and patterns.
triggers:
- /refactor
- /code cleanup
---

# Safe Refactoring Techniques

This skill provides systematic approaches to refactoring code safely, improving structure and maintainability while preserving behavior.

## When to use this skill

Use this skill when you need to:
- Improve code readability and maintainability
- Reduce technical debt
- Prepare code for new features
- Apply design patterns
- Simplify complex code

## Prerequisites

- Comprehensive test coverage for the code to refactor
- Understanding of the codebase and dependencies
- Version control with clean history
- Time to verify behavior hasn't changed

## Guidelines

### Refactoring Principles

**Golden Rule**
- Never refactor without tests
- Make small, incremental changes
- Run tests after each change
- Commit frequently

**When to Refactor**
- Rule of Three: Similar code appearing 3+ times
- Adding a feature is harder than it should be
- Understanding code takes too long
- Code violates SOLID principles
- Performance optimization needed

### Refactoring Workflow

**Preparation**
1. Ensure tests exist and pass
2. Review code to understand current behavior
3. Identify specific issues to address
4. Plan refactoring steps

**Execution**
1. Make one small change at a time
2. Run tests after each change
3. Commit working states frequently
4. Use IDE refactoring tools when possible

**Verification**
1. All tests pass
2. Code review by peer
3. Verify in staging environment
4. Monitor production after deployment

### Common Refactorings

**Extract Method**
```python
# Before
def process_order(order):
    print(f"Processing order {order.id}")
    if order.total > 1000:
        print("High value order - requires approval")
        send_notification(order.manager, "Approval needed")
    update_inventory(order.items)
    send_confirmation(order.customer)

# After
def process_order(order):
    log_order_processing(order)
    if requires_approval(order):
        request_approval(order)
    fulfill_order(order)

def log_order_processing(order):
    print(f"Processing order {order.id}")

def requires_approval(order):
    return order.total > 1000

def request_approval(order):
    print("High value order - requires approval")
    send_notification(order.manager, "Approval needed")

def fulfill_order(order):
    update_inventory(order.items)
    send_confirmation(order.customer)
```

**Introduce Parameter Object**
```python
# Before
def create_user(name, email, phone, address, city, zip_code):
    pass

# After
@dataclass
class UserInfo:
    name: str
    email: str
    phone: str
    address: str
    city: str
    zip_code: str

def create_user(user_info: UserInfo):
    pass
```

**Replace Conditional with Polymorphism**
```python
# Before
def calculate_salary(employee):
    if employee.type == "fulltime":
        return employee.base_salary
    elif employee.type == "contractor":
        return employee.hourly_rate * employee.hours
    elif employee.type == "intern":
        return 0

# After
class FullTimeEmployee(Employee):
    def calculate_salary(self):
        return self.base_salary

class Contractor(Employee):
    def calculate_salary(self):
        return self.hourly_rate * self.hours

class Intern(Employee):
    def calculate_salary(self):
        return 0
```

### Code Smells to Address

**Bloaters**
- Long methods → Extract methods
- Large classes → Extract classes
- Long parameter lists → Introduce parameter objects
- Data clumps → Extract classes

**Object-Orientation Abusers**
- Switch statements → Polymorphism
- Temporary fields → Extract classes
- Refused bequests → Replace inheritance with delegation
- Alternative classes → Unify interfaces

**Change Preventers**
- Divergent change → Split responsibilities
- Shotgun surgery → Move methods/fields
- Parallel inheritance → Bridge pattern

**Dispensables**
- Duplicate code → Extract common code
- Lazy classes → Inline or remove
- Data classes → Add behavior
- Dead code → Delete

### Safety Techniques

**Characterization Tests**
When tests don't exist, write tests that capture current behavior before refactoring:
```python
def test_current_behavior():
    """Document current behavior before refactoring."""
    result = legacy_function(input_data)
    assert result == expected_output  # Record actual output
```

**Parallel Implementation**
Keep old implementation while building new:
```python
def process_data(data, use_new_impl=False):
    if use_new_impl:
        return new_implementation(data)
    return old_implementation(data)
```

**Feature Flags**
Enable gradual rollout of refactored code:
```python
if feature_flags.enabled("new-payment-flow"):
    process_payment_v2(order)
else:
    process_payment_v1(order)
```

## Examples

See the `examples/` directory for:
- `extract-method-examples/` - Method extraction patterns
- `design-pattern-refactorings/` - Applying design patterns
- `legacy-code-techniques.md` - Working with untested code
- `before-after-comparisons.md` - Real refactoring examples

## References

- [Refactoring by Martin Fowler](https://refactoring.com/)
- [Refactoring Guru](https://refactoring.guru/)
- [Working Effectively with Legacy Code](https://www.amazon.com/Working-Effectively-Legacy-Michael-Feathers/dp/0131177052)
- [Clean Code by Robert Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)

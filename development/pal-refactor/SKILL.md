---
name: pal-refactor
description: Code refactoring analysis for code smells, decomposition, and modernization using PAL MCP. Use for cleanup, technical debt reduction, or code organization. Triggers on refactoring requests, code smell detection, or cleanup tasks.
---

# PAL Refactor - Code Improvement

Analyze code for refactoring opportunities with systematic investigation.

## When to Use

- Detecting code smells
- Breaking down large classes/functions
- Modernizing legacy code
- Improving code organization
- Reducing technical debt
- Preparing for feature work

## Quick Start

```python
result = mcp__pal__refactor(
    step="Scanning for code smells in data processing module",
    step_number=1,
    total_steps=2,
    next_step_required=True,
    findings="Beginning code smell analysis",
    refactor_type="codesmells",
    relevant_files=[
        "/app/services/data_processor.py"
    ],
    confidence="exploring"
)
```

## Refactor Types

| Type | Focus |
|------|-------|
| `codesmells` | Anti-patterns and bad practices |
| `decompose` | Breaking down large components |
| `modernize` | Updating legacy patterns |
| `organization` | Structure and layout |

## Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `step` | string | Refactoring analysis narrative |
| `step_number` | int | Current step |
| `total_steps` | int | Estimated total |
| `next_step_required` | bool | More analysis needed? |
| `findings` | string | Opportunities found |

## Optional Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `refactor_type` | enum | codesmells/decompose/modernize/organization |
| `focus_areas` | list | ["performance", "readability"] |
| `confidence` | enum | exploring/incomplete/partial/complete |
| `relevant_files` | list | Files needing refactoring |
| `style_guide_examples` | list | Reference files for style |
| `issues_found` | list | Opportunities with severity |

## Common Code Smells

### Size Issues
- **Long Method** - Methods > 20 lines
- **Large Class** - Classes with too many responsibilities
- **Long Parameter List** - > 3-4 parameters

### Complexity Issues
- **Deep Nesting** - More than 2-3 levels
- **Complex Conditionals** - Hard to follow logic
- **Feature Envy** - Method uses another class's data excessively

### Duplication
- **Copy-Paste Code** - Repeated logic
- **Parallel Inheritance** - Mirror class hierarchies

### Coupling Issues
- **Inappropriate Intimacy** - Classes know too much about each other
- **Message Chains** - `a.b().c().d()`

## Example: Decomposition Analysis

```python
mcp__pal__refactor(
    step="""
    Analyzing UserService for decomposition opportunities

    Current state:
    - 800 lines, 25 methods
    - Handles: auth, profile, preferences, notifications, billing
    """,
    step_number=1,
    total_steps=2,
    next_step_required=True,
    findings="""
    Decomposition opportunities:

    1. Extract AuthService (high priority)
       - login, logout, password_reset, token_refresh
       - 200 lines, 6 methods

    2. Extract NotificationService (medium)
       - send_email, send_sms, preferences
       - 150 lines, 5 methods

    3. Extract BillingService (high)
       - subscribe, cancel, invoice, payment_methods
       - 250 lines, 8 methods

    Remaining in UserService:
    - Core profile CRUD
    - 200 lines, 6 methods
    """,
    refactor_type="decompose",
    relevant_files=["/app/services/user_service.py"],
    issues_found=[
        {"severity": "high", "type": "decompose",
         "description": "UserService violates SRP - handles 5 concerns"},
        {"severity": "medium", "type": "codesmells",
         "description": "Methods averaging 40 lines - extract helpers"}
    ],
    confidence="partial"
)
```

## Refactoring Patterns

### Extract Method
```python
# Before
def process_order(order):
    # validate
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Invalid total")
    # ... more validation
    # process
    # ... processing logic

# After
def process_order(order):
    validate_order(order)
    execute_order_processing(order)
```

### Replace Conditional with Polymorphism
```python
# Before
def calculate_shipping(order):
    if order.type == "standard":
        return order.weight * 0.5
    elif order.type == "express":
        return order.weight * 1.5
    elif order.type == "overnight":
        return order.weight * 3.0

# After
class ShippingCalculator(ABC):
    @abstractmethod
    def calculate(self, order): pass

class StandardShipping(ShippingCalculator):
    def calculate(self, order):
        return order.weight * 0.5
```

## Best Practices

1. **Refactor in small steps** - One change at a time
2. **Keep tests passing** - Run after each change
3. **Commit frequently** - Easy to revert
4. **Document why** - Not just what changed
5. **Prioritize by impact** - High-traffic code first

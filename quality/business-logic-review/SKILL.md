---
name: business-logic-review
description: Review code for business logic correctness, edge cases, and alignment with requirements. Use for verifying feature implementations, catching logic errors, ensuring proper handling of business rules, and validating that code does what was intended.
---

# Business Logic Review

Verify code correctly implements business requirements and handles all cases.

## Review Focus

### Correctness
- Does the code do what the requirements specify?
- Are all business rules implemented?
- Are edge cases handled?
- Are error conditions handled appropriately?

### Completeness
- All acceptance criteria met?
- All user paths covered?
- All input variations handled?
- All output states possible?

### Consistency
- Consistent with existing behavior?
- Consistent with documented rules?
- Consistent across similar features?

## Review Process

### 1. Understand Requirements
Before reviewing code, clarify:
- What is this feature supposed to do?
- Who uses it and how?
- What are the business rules?
- What are the edge cases?

### 2. Trace User Flows
Walk through each user path:
```
Happy path: Normal successful flow
Error paths: Each way things can fail
Edge cases: Boundary conditions, empty states
```

### 3. Verify Business Rules
For each rule, find where it's enforced:
```markdown
Rule: "Users can only edit their own posts"
- Check: Is ownership validated?
- Where: Before edit operation
- How: user.id == post.author_id
```

### 4. Test Assumptions
Question implicit assumptions:
- What if the input is empty?
- What if the user is not authenticated?
- What if the resource doesn't exist?
- What if concurrent modifications occur?

## Common Logic Issues

### Missing Validation
```python
# Missing: What if user_id doesn't exist?
def get_user_orders(user_id):
    return Order.query.filter_by(user_id=user_id).all()

# Better: Handle missing user
def get_user_orders(user_id):
    user = User.query.get(user_id)
    if not user:
        raise UserNotFoundError(user_id)
    return user.orders
```

### Incorrect Boundary Conditions
```python
# Bug: Off-by-one error
if age >= 18 and age < 65:  # What about 65-year-olds?
    apply_standard_rate()

# Correct: Clear boundaries
if 18 <= age <= 64:
    apply_standard_rate()
elif age >= 65:
    apply_senior_rate()
```

### Race Conditions
```python
# Bug: Check-then-act race condition
if inventory.count > 0:
    inventory.count -= 1  # Another request could decrement first

# Better: Atomic operation
result = Inventory.query.filter(
    Inventory.id == item_id,
    Inventory.count > 0
).update({Inventory.count: Inventory.count - 1})
if result == 0:
    raise OutOfStockError()
```

### Missing State Transitions
```python
# Bug: Can transition from any state to completed
def complete_order(order):
    order.status = 'completed'

# Better: Validate state transitions
VALID_TRANSITIONS = {
    'pending': ['processing', 'cancelled'],
    'processing': ['completed', 'failed'],
}

def complete_order(order):
    if 'completed' not in VALID_TRANSITIONS.get(order.status, []):
        raise InvalidStateTransition(order.status, 'completed')
    order.status = 'completed'
```

## Review Output Format

```markdown
## Business Logic Review: [Feature Name]

### Requirements Verified
- [x] Requirement 1 - Implemented in `function_name()`
- [x] Requirement 2 - Implemented in `class.method()`
- [ ] Requirement 3 - **NOT FOUND**

### Logic Issues
- **[Location]**: [Description of logic error]
  - Expected: [What should happen]
  - Actual: [What the code does]
  - Impact: [Business impact if not fixed]

### Edge Cases
| Case | Handled? | Location |
|------|----------|----------|
| Empty input | Yes | line 42 |
| User not found | No | - |
| Concurrent edit | No | - |

### Questions for Clarification
- [Question about unclear requirement]
```

## Questions to Ask

### For Every Change
- What happens if the input is null/empty?
- What happens if the resource doesn't exist?
- What happens if the user lacks permission?
- What happens if this fails halfway through?

### For State Changes
- What states can transition to this state?
- What should happen in each prior state?
- Is the transition atomic?
- What if concurrent transitions occur?

### For Calculations
- What are the boundary values?
- What precision is required?
- What happens at min/max values?
- Are there rounding considerations?

---
name: code-improvement
description: Suggest improvements to existing code including refactoring opportunities, performance optimizations, and modernization. Use for identifying technical debt, suggesting refactors, improving code architecture, and modernizing legacy patterns.
---

# Code Improvement

Identify opportunities to improve existing code quality, performance, and maintainability.

## Improvement Categories

### Refactoring
- Extract methods/functions
- Simplify conditionals
- Remove duplication
- Improve naming
- Reduce complexity

### Performance
- Algorithm optimization
- Caching opportunities
- Query optimization
- Memory efficiency
- Lazy loading

### Modernization
- Update deprecated APIs
- Use newer language features
- Adopt current best practices
- Improve type safety

### Architecture
- Better separation of concerns
- Improved abstraction
- Cleaner interfaces
- Reduced coupling

## Refactoring Patterns

### Extract Method
```python
# Before: Long function with multiple responsibilities
def process_order(order):
    # Validate
    if not order.items:
        raise ValueError("Empty order")
    if not order.user.is_active:
        raise ValueError("Inactive user")

    # Calculate totals
    subtotal = sum(item.price * item.quantity for item in order.items)
    tax = subtotal * 0.1
    total = subtotal + tax

    # Save
    order.subtotal = subtotal
    order.tax = tax
    order.total = total
    order.save()

# After: Extracted methods
def process_order(order):
    validate_order(order)
    calculate_totals(order)
    order.save()

def validate_order(order):
    if not order.items:
        raise ValueError("Empty order")
    if not order.user.is_active:
        raise ValueError("Inactive user")

def calculate_totals(order):
    order.subtotal = sum(item.price * item.quantity for item in order.items)
    order.tax = order.subtotal * TAX_RATE
    order.total = order.subtotal + order.tax
```

### Replace Conditional with Polymorphism
```python
# Before: Type-checking conditional
def calculate_area(shape):
    if shape.type == 'circle':
        return math.pi * shape.radius ** 2
    elif shape.type == 'rectangle':
        return shape.width * shape.height
    elif shape.type == 'triangle':
        return 0.5 * shape.base * shape.height

# After: Polymorphic method
class Circle:
    def area(self):
        return math.pi * self.radius ** 2

class Rectangle:
    def area(self):
        return self.width * self.height
```

### Introduce Parameter Object
```python
# Before: Too many parameters
def create_user(name, email, age, address, city, country, phone):
    ...

# After: Parameter object
@dataclass
class UserData:
    name: str
    email: str
    age: int
    address: str
    city: str
    country: str
    phone: str

def create_user(data: UserData):
    ...
```

## Performance Improvements

### Add Caching
```python
# Before: Repeated expensive computation
def get_user_stats(user_id):
    # Complex queries every time
    return calculate_stats(user_id)

# After: With caching
from functools import lru_cache

@lru_cache(maxsize=100)
def get_user_stats(user_id):
    return calculate_stats(user_id)
```

### Batch Database Operations
```python
# Before: N+1 queries
def get_order_details(order_ids):
    orders = []
    for order_id in order_ids:
        order = Order.query.get(order_id)  # N queries
        orders.append(order)
    return orders

# After: Single query
def get_order_details(order_ids):
    return Order.query.filter(Order.id.in_(order_ids)).all()
```

### Lazy Loading
```python
# Before: Load everything upfront
class Report:
    def __init__(self):
        self.data = self._load_all_data()  # Expensive

# After: Load on demand
class Report:
    def __init__(self):
        self._data = None

    @property
    def data(self):
        if self._data is None:
            self._data = self._load_all_data()
        return self._data
```

## Improvement Output Format

```markdown
## Improvement Suggestions: [File/Module Name]

### High Impact
Improvements with significant benefit, relatively low effort.

#### 1. [Title]
**Current:**
```python
current_code()
```

**Suggested:**
```python
improved_code()
```

**Benefits:**
- [Benefit 1]
- [Benefit 2]

**Effort:** Low/Medium/High

### Medium Impact
Worth doing but lower priority.

#### 1. [Title]
...

### Future Considerations
Ideas for later, not urgent.
- [Idea 1]
- [Idea 2]
```

## When NOT to Suggest Improvements

Avoid suggesting changes that:
- Add complexity without clear benefit
- Are purely stylistic preferences
- Would require large rewrites for small gains
- Are speculative ("might be useful someday")
- Break working code for theoretical improvements

Focus on improvements that:
- Fix actual problems (bugs, performance, security)
- Significantly improve maintainability
- Have clear, measurable benefits
- Can be done incrementally

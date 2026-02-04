---
name: refactoring-to-patterns
description: Apply Fowler's refactoring patterns - recognize code smells, apply proven transformations
---

# Refactoring to Patterns

## Core Principle

Patterns solve recurring design problems. Know the patterns, recognize the smells, apply the right transformation.

**MANDATORY:** Always name the pattern explicitly. "Applying Compose Method" not "extracting some methods."

## Pattern Quick Reference

| Code Smell | Pattern | Indicator |
|------------|---------|-----------|
| Long method, multiple responsibilities | Compose Method | Can't describe in one sentence |
| Switch/if on object type | Replace Conditional with Polymorphism | Each case handles different type |
| Duplicate algorithm structure | Form Template Method | Same steps, different details |
| Scattered null checks | Introduce Null Object | `if obj != null` appears 3+ times |
| Type field drives behavior | Replace Type Code with State/Strategy | Behavior varies by type field |
| Stacked conditional features | Move Embellishment to Decorator | Optional features combined |

## Patterns

### Compose Method

Break long method into small, well-named methods at same abstraction level.

```ruby
# Before: Mixed abstraction levels
def process_order(order)
  raise "Empty" if order.items.empty?
  total = order.items.sum { |i| i.price * i.quantity }
  send_email(order.customer.email, "Confirmation", "...")
end

# After: Single abstraction level
def process_order(order)
  validate_order(order)
  total = calculate_total(order)
  send_confirmation(order, total)
end
```

### Replace Conditional with Polymorphism

```ruby
# Before: Type-based switch
def process_payment(payment)
  case payment.type
  when 'credit' then charge_credit(payment)
  when 'paypal' then charge_paypal(payment)
  end
end

# After: Polymorphic
class CreditPayment
  def process; charge_credit(self); end
end

def process_payment(payment)
  payment.process
end
```

### Form Template Method

```ruby
# Before: Duplicate structure
class PdfReport
  def generate(data)
    header + "<PDF>#{data}</PDF>" + footer
  end
end

# After: Template in base class
class Report
  def generate(data)
    header + generate_body(data) + footer
  end
end

class PdfReport < Report
  def generate_body(data); "<PDF>#{data}</PDF>"; end
end
```

### Introduce Null Object

```ruby
# Before: Scattered null checks
discount = customer ? customer.discount : 0
name = customer ? customer.name : "Guest"

# After: Null object
class NullCustomer
  def discount; 0; end
  def name; "Guest"; end
end

def find_customer(id)
  database.find(id) || NullCustomer.new
end

customer = find_customer(id)
discount = customer.discount  # No null check
```

### Replace Type Code with State/Strategy

```ruby
# Before: Type field with switches
class Employee
  def bonus(base)
    case @type
    when 'engineer' then base * 1.5
    when 'manager' then base * 2.0
    end
  end
end

# After: Delegated to type object
class Engineer
  def bonus(base); base * 1.5; end
end

class Employee
  def bonus(base); @type.bonus(base); end
end
```

## When to Apply

**Apply when:**
- Smell is clear and recurring
- Pattern simplifies the code
- Team understands the pattern
- Extension point needed now (not "someday")

**Avoid when:**
- Code already simple
- Pattern adds more complexity than it removes
- Guessing at future requirements (three strikes rule)

## Recognition Workflow

1. **Identify smell** → Map to pattern
2. **Confirm fit** → Will it reduce complexity?
3. **Apply incrementally** → Small steps, tests between
4. **Verify improvement** → Easier to read/extend?

## Key Takeaways

1. **Name patterns explicitly** - Creates shared vocabulary
2. **Three strikes rule** - Don't abstract until 3+ repetitions
3. **Test pattern fits** - Will it simplify or complicate?
4. **Extract incrementally** - Small steps with tests
5. **Same abstraction level** - Methods in composed method should match

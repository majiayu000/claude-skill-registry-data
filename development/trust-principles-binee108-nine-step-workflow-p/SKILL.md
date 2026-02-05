---
name: trust-principles
description: TRUST quality principles (Test-first, Readable, Unified, Secured, Trackable) ensuring production-ready code. Use when implementing, reviewing, testing, or evaluating code quality across all development phases.
---

# TRUST Quality Principles

## Instructions

### Apply all 5 principles

**T - Test-First:** Write tests before implementation
**R - Readable:** Clear names and documentation
**U - Unified:** Consistent patterns and conventions
**S - Secured:** Input validation, no vulnerabilities
**T - Trackable:** Tags, logs, clear commits

### For implementation

1. Write tests first (TDD)
2. Use descriptive names
3. Follow project patterns
4. Validate all inputs
5. Add tags and logs

### For review

1. Verify test coverage
2. Check code clarity
3. Ensure consistency
4. Validate security
5. Confirm documentation

## Example

<!-- CUSTOMIZE: Replace with {{MAIN_TECH_STACK}} examples -->

### Python Example
```python
# T - Test first
def test_validator():
    assert Validator.validate({'id': '123'}) == True

# All TRUST principles applied
# @FEAT:order @COMP:validator @TYPE:utility  # T - Trackable
class OrderValidator:
    '''Validates orders before processing'''  # R - Readable

    def validate(self, order: dict) -> bool:
        # S - Secured: Input validation
        if not isinstance(order, dict):
            raise TypeError("Order must be dict")

        # U - Unified: Standard pattern
        if 'order_id' not in order:
            return False

        # T - Trackable: Log
        logger.info(f"Validated: {order['order_id']}")
        return True
```

### JavaScript/TypeScript Example
```javascript
// T - Test first
test('validator validates orders', () => {
    expect(validator.validate({id: '123'})).toBe(true);
});

// All TRUST principles applied
// @FEAT:order @COMP:validator @TYPE:utility  // T - Trackable
class OrderValidator {
    /**
     * Validates orders before processing  // R - Readable
     */

    validate(order) {
        // S - Secured: Input validation
        if (typeof order !== 'object' || order === null) {
            throw new TypeError('Order must be object');
        }

        // U - Unified: Standard pattern
        if (!('orderId' in order)) {
            return false;
        }

        // T - Trackable: Log
        logger.info(`Validated: ${order.orderId}`);
        return true;
    }
}
```

### Go Example
```go
// T - Test first
func TestValidator(t *testing.T) {
    order := map[string]string{"id": "123"}
    if !validator.Validate(order) {
        t.Error("Expected validation to pass")
    }
}

// All TRUST principles applied
// @FEAT:order @COMP:validator @TYPE:utility  // T - Trackable
// OrderValidator validates orders before processing  // R - Readable
type OrderValidator struct{}

// Validate checks if order is valid
func (v *OrderValidator) Validate(order map[string]interface{}) bool {
    // S - Secured: Input validation
    if order == nil {
        panic("Order must not be nil")
    }

    // U - Unified: Standard pattern
    if _, ok := order["order_id"]; !ok {
        return false
    }

    // T - Trackable: Log
    logger.Info(fmt.Sprintf("Validated: %v", order["order_id"]))
    return true
}
```

## Checklist

```markdown
[ ] T: Tests pass?
[ ] R: Clear and documented?
[ ] U: Follows conventions?
[ ] S: Security applied?
[ ] T: Tagged and logged?
```

## Detailed Breakdown

### T - Test-First (TDD)

**Principle:** Write tests before code

**Benefits:**
- Clarifies requirements
- Ensures testability
- Prevents over-engineering
- Documents expected behavior

**Process:**
1. Write failing test
2. Write minimal code to pass
3. Refactor while keeping tests green

**Example TDD Cycle:**

```{{LANG}}
# 1. Write failing test
def test_calculate_total():
    cart = Cart([Item(price=10), Item(price=20)])
    assert cart.calculate_total() == 30

# 2. Minimal implementation
class Cart:
    def __init__(self, items):
        self.items = items

    def calculate_total(self):
        return sum(item.price for item in self.items)

# 3. Refactor (extract method)
class Cart:
    def __init__(self, items):
        self.items = items

    def calculate_total(self):
        return self._sum_prices()

    def _sum_prices(self):
        return sum(item.price for item in self.items)
```

---

### R - Readable

**Principle:** Code should read like prose

**Guidelines:**
- Descriptive names (no abbreviations)
- Clear function purposes
- Comments explain WHY, not WHAT
- Consistent formatting

**Examples:**

**❌ Not Readable:**
```{{LANG}}
def prc(o):  # What is prc? What is o?
    t = 0
    for i in o:
        t += i['p'] * i['q']
    return t
```

**✅ Readable:**
```{{LANG}}
def calculate_order_total(order_items):
    """Calculate total price for all items in order"""
    total = 0
    for item in order_items:
        total += item['price'] * item['quantity']
    return total
```

**Comment Quality:**

**❌ Bad comments (state the obvious):**
```{{LANG}}
# Increment counter
counter += 1

# Loop through users
for user in users:
```

**✅ Good comments (explain WHY):**
```{{LANG}}
# Batch size of 100 prevents memory overflow on large datasets
BATCH_SIZE = 100

# Retry 3 times because payment gateway has transient failures
MAX_RETRIES = 3
```

---

### U - Unified (Consistency)

**Principle:** Follow project patterns consistently

**Areas of Consistency:**

1. **Naming Conventions**
   ```{{LANG}}
   # ✅ Consistent
   get_user()
   get_order()
   get_product()

   # ❌ Inconsistent
   get_user()
   fetchOrder()
   retrieve_product()
   ```

2. **Error Handling**
   ```{{LANG}}
   # ✅ Consistent pattern
   def get_user(id):
       if not id:
           raise ValueError("ID required")
       # ...

   def get_order(id):
       if not id:
           raise ValueError("ID required")
       # ...
   ```

3. **Project Structure**
   ```
   ✅ Unified architecture
   services/
       user_service.py
       order_service.py
       product_service.py

   ❌ Inconsistent architecture
   services/user_service.py
   order_manager.py
   product/handler.py
   ```

4. **API Responses**
   ```json
   // ✅ Consistent format
   {"data": {...}, "error": null}
   {"data": null, "error": "Error message"}

   // ❌ Inconsistent format
   {"user": {...}}
   {"error": "Error"}
   {"success": true, "result": {...}}
   ```

---

### S - Secured

**Principle:** Never trust input, always validate

**Security Checklist:**

1. **Input Validation**
   ```{{LANG}}
   def process_payment(amount, currency):
       # Validate types
       if not isinstance(amount, (int, float)):
           raise TypeError("Amount must be numeric")

       # Validate ranges
       if amount <= 0:
           raise ValueError("Amount must be positive")

       # Validate enums
       if currency not in ['USD', 'EUR', 'GBP']:
           raise ValueError("Invalid currency")
   ```

2. **SQL Injection Prevention**
   ```{{LANG}}
   # ❌ Vulnerable
   query = f"SELECT * FROM users WHERE id = '{user_id}'"

   # ✅ Secure
   query = "SELECT * FROM users WHERE id = ?"
   db.execute(query, [user_id])
   ```

3. **XSS Prevention**
   ```{{LANG}}
   # ❌ Vulnerable
   return f"<h1>Hello {user_name}</h1>"

   # ✅ Secure (auto-escaped)
   return render_template('hello.html', name=user_name)
   ```

4. **Password Security**
   ```{{LANG}}
   # ❌ Weak
   password_hash = hashlib.md5(password.encode()).hexdigest()

   # ✅ Secure
   import bcrypt
   password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
   ```

**Reference:** See `@security-checklist` skill for complete guide

---

### T - Trackable

**Principle:** Make debugging easy

**Components:**

1. **Tags** (Code organization)
   ```{{LANG}}
   # @FEAT:payment @COMP:service @TYPE:core
   class PaymentService:
       pass
   ```

2. **Logging** (Runtime information)
   ```{{LANG}}
   # Appropriate log levels
   logger.debug("Detailed diagnostic info")
   logger.info("Normal operation milestone")
   logger.warning("Something unexpected but handled")
   logger.error("Error that needs attention")
   ```

3. **Commits** (Change history)
   ```bash
   # ✅ Clear commit
   git commit -m "Add payment validation for negative amounts (Issue #42)"

   # ❌ Unclear commit
   git commit -m "fix stuff"
   ```

4. **Monitoring** (Observability)
   ```{{LANG}}
   # Add metrics for critical operations
   def process_payment(amount):
       start_time = time.time()
       try:
           result = payment_gateway.charge(amount)
           metrics.record('payment.success', 1)
           return result
       except Exception as e:
           metrics.record('payment.failure', 1)
           raise
       finally:
           duration = time.time() - start_time
           metrics.record('payment.duration', duration)
   ```

**Reference:** See `@tag-based-search` skill for tagging guide

---

## TRUST Review Checklist

**For code-reviewer:**

```markdown
## TRUST Principles Review

### T - Test-First
- [ ] Tests exist for new code?
- [ ] Tests were written before implementation (when possible)?
- [ ] All tests pass?
- [ ] Edge cases covered?

### R - Readable
- [ ] Function/variable names descriptive?
- [ ] Complex logic explained with comments?
- [ ] Code flows logically?
- [ ] No magic numbers (constants defined)?

### U - Unified
- [ ] Follows project naming conventions?
- [ ] Error handling consistent with codebase?
- [ ] Architecture patterns maintained?
- [ ] API response format consistent?

### S - Secured
- [ ] All inputs validated?
- [ ] No SQL injection vulnerabilities?
- [ ] No XSS vulnerabilities?
- [ ] Passwords hashed (if applicable)?
- [ ] No hardcoded secrets?

### T - Trackable
- [ ] Tags added (@FEAT, @COMP, @TYPE)?
- [ ] Appropriate logging?
- [ ] Commit message clear?
- [ ] Metrics/monitoring added (if critical)?

**Overall:** [APPROVED | NEEDS_REVISION]
```

---

## Integration with Workflow

**Step 3 (Implementation):**
- Apply all 5 TRUST principles
- Verify with self-checklist

**Step 4 (Code Review):**
- code-reviewer uses TRUST checklist
- NEEDS_REVISION if any principle violated

**Step 7 (Testing):**
- T (Test-First) verified through test execution
- Edge cases confirmed

**Step 8 (Test Review):**
- test-reviewer confirms test quality
- Ensures tests validate TRUST principles

---

**For detailed principles, see [reference.md](reference.md)**
**For more examples, see [examples.md](examples.md)**

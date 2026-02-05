---
name: software-development
description: Clean code principles - avoid common issues like unnecessary try/catch, unused variables, DRY violations, and layer confusion
---

# Software Development

## Core Principle

Write the simplest code that works. Don't add complexity "just in case."

> "The best code is no code. The second best is simple code."

---

## Layer Separation (CRITICAL)

**Keep business logic in models, not controllers.**

### Models (Fat)
- Business logic and validations
- Data transformations
- Relationships and queries
- Domain rules and calculations

### Controllers (Thin)
- Request/response handling
- Parameter parsing
- Calling model methods
- Rendering views/responses

### ❌ BAD: Logic in Controller

```python
# Django - DON'T DO THIS
class OrderView(View):
    def post(self, request):
        order = Order.objects.get(id=request.POST['id'])

        # ❌ Business logic in controller
        if order.total > 100:
            discount = order.total * 0.1
        else:
            discount = 0

        order.final_price = order.total - discount
        order.status = 'confirmed'
        order.confirmed_at = timezone.now()
        order.save()

        # ❌ More business logic
        for item in order.items.all():
            item.product.stock -= item.quantity
            item.product.save()
```

### ✅ GOOD: Logic in Model

```python
# Django - DO THIS
class Order(models.Model):
    def confirm(self):
        """Business logic belongs here."""
        self.apply_discount()
        self.status = 'confirmed'
        self.confirmed_at = timezone.now()
        self.save()
        self.decrement_stock()

    def apply_discount(self):
        self.discount = self.total * 0.1 if self.total > 100 else 0
        self.final_price = self.total - self.discount

    def decrement_stock(self):
        for item in self.items.all():
            item.product.decrement_stock(item.quantity)

class OrderView(View):
    def post(self, request):
        order = Order.objects.get(id=request.POST['id'])
        order.confirm()  # ✅ Controller just calls model method
        return JsonResponse({'status': 'confirmed'})
```

### The Rule

> If you're writing `if` statements about business rules in a controller, move them to the model.

---

## DRY (Don't Repeat Yourself)

### When to Extract

**Extract when:**
- Same logic appears 3+ times
- Logic is non-trivial (not just a one-liner)
- The duplication is TRUE duplication (same intent, not coincidental)

**Don't extract when:**
- Only 2 occurrences (wait for the third)
- Code is trivially simple
- Duplication is coincidental (same code, different purposes)

### ❌ BAD: Copy-Pasted Logic

```python
# DON'T DO THIS
def create_user(data):
    if not data.get('email') or '@' not in data['email']:
        raise ValidationError('Invalid email')
    if not data.get('password') or len(data['password']) < 8:
        raise ValidationError('Password too short')
    # ... create user

def update_user(user, data):
    if not data.get('email') or '@' not in data['email']:
        raise ValidationError('Invalid email')
    if not data.get('password') or len(data['password']) < 8:
        raise ValidationError('Password too short')
    # ... update user
```

### ✅ GOOD: Extracted Common Logic

```python
# DO THIS
def validate_user_data(data):
    if not data.get('email') or '@' not in data['email']:
        raise ValidationError('Invalid email')
    if not data.get('password') or len(data['password']) < 8:
        raise ValidationError('Password too short')

def create_user(data):
    validate_user_data(data)
    # ... create user

def update_user(user, data):
    validate_user_data(data)
    # ... update user
```

### The Rule

> "Three strikes and you refactor."

---

## Try/Catch Rules

### Only Catch What Can Throw

**Don't wrap code that can't throw.**

```python
# ❌ BAD: Unnecessary try/catch
try:
    user_id = request.params['user_id']
    name = user.name.upper()
except Exception as e:
    logger.error(f"Error: {e}")
    raise

# ✅ GOOD: No try/catch needed
user_id = request.params['user_id']
name = user.name.upper()
```

### Don't Catch and Re-Throw

```python
# ❌ BAD: Pointless catch and re-throw
try:
    result = external_api.call()
except Exception as e:
    raise e  # What's the point?

# ✅ GOOD: Just let it propagate
result = external_api.call()
```

### Don't Swallow Errors

```python
# ❌ BAD: Swallowed error - bugs hide here
try:
    process_payment(order)
except Exception:
    pass  # Silent failure = debugging nightmare

# ✅ GOOD: Handle meaningfully or let it fail
try:
    process_payment(order)
except PaymentError as e:
    order.mark_payment_failed(str(e))
    notify_admin(e)
```

### When TO Use Try/Catch

- External API calls that can fail
- File/network operations
- Parsing untrusted input
- When you have a meaningful recovery strategy

---

## Unused Variables

### Don't Declare What You Don't Use

```python
# ❌ BAD: Unused variable
def process_order(order):
    user = order.user  # Never used
    items = order.items.all()  # Never used
    total = order.calculate_total()
    return total

# ✅ GOOD: Only declare what you use
def process_order(order):
    return order.calculate_total()
```

### Use Underscore for Intentionally Ignored

```python
# ✅ OK: Underscore signals intentional ignore
for _, value in enumerate(items):
    process(value)

# ✅ OK: Unpacking with ignored values
first, _, last = get_names()
```

---

## Over-Defensive Coding

### Don't Check for Impossible Conditions

```python
# ❌ BAD: User is guaranteed to exist here
def get_user_profile(user):
    if user is None:  # Can't be None - function requires user
        raise ValueError("User required")
    return user.profile

# ✅ GOOD: Trust your internal code
def get_user_profile(user):
    return user.profile
```

### Validate at Boundaries, Trust Internally

```python
# ✅ Validate at system boundary (API endpoint)
def api_get_user(request):
    user_id = request.params.get('user_id')
    if not user_id:
        return error_response("user_id required")

    user = User.find(user_id)
    if not user:
        return error_response("User not found")

    # From here, we KNOW user exists
    return success_response(format_user(user))

# ✅ Internal functions trust their inputs
def format_user(user):
    # No need to check if user is None - caller guarantees it
    return {
        'name': user.name,
        'email': user.email
    }
```

---

## Error Handling Patterns

### Be Specific About What You Catch

```python
# ❌ BAD: Catches everything
try:
    user = User.objects.get(id=user_id)
except Exception:
    return None

# ✅ GOOD: Catches specific exception
try:
    user = User.objects.get(id=user_id)
except User.DoesNotExist:
    return None
```

### Fail Fast, Fail Loud

```python
# ❌ BAD: Silent failure
def get_config(key):
    return config.get(key, None)  # Caller gets None, has no idea why

# ✅ GOOD: Explicit failure
def get_config(key):
    if key not in config:
        raise ConfigError(f"Missing required config: {key}")
    return config[key]
```

---

## Quick Checklist

Before committing code, check:

- [ ] **Layer separation**: Is business logic in models, not controllers?
- [ ] **DRY**: Is there copy-pasted logic that should be extracted?
- [ ] **Try/catch**: Is every try/catch necessary and meaningful?
- [ ] **Unused variables**: Are all declared variables actually used?
- [ ] **Over-defensive**: Am I checking for conditions that can't happen?
- [ ] **Error handling**: Am I catching specific exceptions, not `Exception`?
- [ ] **Swallowed errors**: Does every catch block do something meaningful?

---

## The Golden Rules

1. **Fat models, thin controllers** - Logic belongs in models
2. **Three strikes, then refactor** - Extract on third duplication
3. **Only catch what throws** - No unnecessary try/catch
4. **Use what you declare** - No unused variables
5. **Validate at boundaries** - Trust internal code
6. **Fail fast, fail loud** - Explicit errors over silent failures

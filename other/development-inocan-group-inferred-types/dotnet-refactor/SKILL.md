---
name: dotnet-refactor
description:
  Analyzes code quality, suggests improvements, and safely refactors code while preserving behavior.
  Use when improving code structure, addressing technical debt, or refactoring dotnet code.
---

# Refactor Skill

Systematic code refactoring with progressive disclosure.

## Workflow

### 1. Initial Assessment

- **Scope**: Identify files/modules to analyze
- **Language**: Detect programming language and idioms
- **Test Coverage**: Check if tests exist
- **Quick Scan**: Find code smells (file size, function length, complexity)

### 2. Deep Analysis

- **God Classes**: Classes or Interfaces with >8 public methods
- **Long Functions**: Functions >50 LOC or cyclomatic complexity >10
- **Deep Nesting**: Conditionals nested
- **Large Files**: Files >500 lines
- **Parameter Overload**: Public functions with >4 parameters
- **SOLID Principles**: Violations of SOLID design principles
- **Coupling**: High inter-module dependencies
- **Duplication**: Repeated code blocks (>=2 lines similar)
- **Magic Values**: Hardcoded numbers/strings without constants
- **Poor Naming**: Unclear variable/function names
- **Dead Code**: Unused functions, variables, imports
- **Global State**: Mutable global variables
- **Error Handling**: Missing error handling or overly broad catches
- **Performance Bottlenecks**: Inefficient algorithms, unnecessary loops
- **Security Concerns**: SQL injection risks, XSS vulnerabilities, exposed secrets
- **Memory Leaks**: Unclosed resources, circular references

### 3. Execute Refactoring

1. **Pre-Refactor**:
   - Ensure tests exist (warn if missing)
   - Run tests to establish baseline

2. **Refactor Incrementally**:
   - Apply one pattern at a time
   - Keep changes atomic
   - Preserve exact behavior
   - Update related documentation/comments

3. **Post-Refactor**:
   - Run tests after each change
   - Verify behavior unchanged
   - Update tests if needed (structure only)

## Refactoring Patterns Catalog

### Extract Function/Method

**When**: Function >30 LOC, doing multiple things, or code duplication

```typescript
// Before
function processUser(user: User) {
  if (!user.email || !user.email.includes('@')) {
    throw new Error('Invalid email');
  }
  const hash = crypto.createHash('sha256').update(user.password).digest('hex');
  user.password = hash;
  db.save(user);
  logger.info(`User ${user.email} processed`);
}

// After
function processUser(user: User) {
  validateEmail(user.email);
  user.password = hashPassword(user.password);
  saveUser(user);
  logUserProcessed(user.email);
}

function validateEmail(email: string) {
  if (!email || !email.includes('@')) {
    throw new Error('Invalid email');
  }
}

function hashPassword(password: string): string {
  return crypto.createHash('sha256').update(password).digest('hex');
}

function saveUser(user: User) {
  db.save(user);
}

function logUserProcessed(email: string) {
  logger.info(`User ${email} processed`);
}
```

### Extract Class/Module

**When**: Class >10 methods, multiple responsibilities

```python
# Before
class UserManager:
    def create_user(self, data): ...
    def update_user(self, id, data): ...
    def delete_user(self, id): ...
    def send_email(self, user, subject, body): ...
    def send_sms(self, user, message): ...
    def validate_password(self, password): ...
    def hash_password(self, password): ...

# After
class UserRepository:
    def create(self, data): ...
    def update(self, id, data): ...
    def delete(self, id): ...

class NotificationService:
    def send_email(self, user, subject, body): ...
    def send_sms(self, user, message): ...

class PasswordManager:
    def validate(self, password): ...
    def hash(self, password): ...
```

### Introduce Parameter Object

**When**: Functions with >4 parameters, parameters often used together

```java
// Before
public void createOrder(String userId, String productId, int quantity,
                       String address, String city, String zipCode,
                       String paymentMethod, String cardNumber) {
    // ...
}

// After
public void createOrder(OrderRequest request) {
    // ...
}

class OrderRequest {
    private String userId;
    private String productId;
    private int quantity;
    private Address shippingAddress;
    private PaymentInfo payment;
}
```

### Simplify Complex Conditionals

**When**: Nested conditionals >3 levels, hard to understand logic

```go
// Before
func canProcess(order Order) bool {
    if order.Status == "pending" {
        if order.Amount > 0 {
            if order.Customer != nil {
                if order.Customer.IsActive && order.Customer.CreditScore > 600 {
                    return true
                }
            }
        }
    }
    return false
}

// After
func canProcess(order Order) bool {
    return order.isPending() &&
           order.hasValidAmount() &&
           order.hasActiveCustomer() &&
           order.hasGoodCredit()
}

func (o Order) isPending() bool {
    return o.Status == "pending"
}

func (o Order) hasValidAmount() bool {
    return o.Amount > 0
}

func (o Order) hasActiveCustomer() bool {
    return o.Customer != nil && o.Customer.IsActive
}

func (o Order) hasGoodCredit() bool {
    return o.Customer != nil && o.Customer.CreditScore > 600
}
```

### Replace Magic Numbers/Strings

**When**: Hardcoded values without context

```csharp
// Before
public decimal CalculateTax(decimal amount) {
    if (amount > 10000) {
        return amount * 0.25;
    }
    return amount * 0.15;
}

// After
private const decimal HIGH_VALUE_THRESHOLD = 10000m;
private const decimal HIGH_VALUE_TAX_RATE = 0.25m;
private const decimal STANDARD_TAX_RATE = 0.15m;

public decimal CalculateTax(decimal amount) {
    if (amount > HIGH_VALUE_THRESHOLD) {
        return amount * HIGH_VALUE_TAX_RATE;
    }
    return amount * STANDARD_TAX_RATE;
}
```

### Invert Conditional Logic

**When**: Deeply nested conditionals, improve readability

```csharp
// Before
public decimal CalculateTax(decimal amount) {
    if (IsValidAmount(amount)) {
        // complex tax calculation logic
        return computedTax;
    }
    return 0;
}

// After
public decimal CalculateTax(decimal amount) {
    if (!IsValidAmount(amount)) {
        return 0;
    }
    // complex tax calculation logic
    return computedTax;
}

```

## Safety Rules

- Never change observable behavior
- Ensure tests exist before major refactoring
- Make atomic commits per refactoring step
- Run tests after each change
- Document breaking changes (if unavoidable)
- Preserve error handling behavior
- Maintain performance characteristics
- Keep API compatibility unless explicitly breaking

---
name: code-smell-detector
description: Detect and categorize code smells using Martin Fowler's catalog with severity scoring and refactoring recommendations. Use when reviewing code quality.
---

# Code Smell Detector

Systematic detection and categorization of code smells based on Martin Fowler's catalog and established software engineering literature. This skill provides heuristics for identifying problematic code patterns, assigns severity scores, and recommends specific refactoring strategies to resolve each smell.

## When to Use This Skill

Use this skill for:

- Reviewing code for structural quality problems before merging
- Identifying methods, classes, or modules that have grown too large or too complex
- Detecting coupling and cohesion issues across a codebase
- Prioritizing refactoring efforts based on smell severity and impact
- Training developers to recognize common anti-patterns
- Establishing code quality baselines for a project
- Preparing a codebase for new feature development by cleaning up existing smells

**Trigger phrases**: "code smell", "detect smells", "find code smells", "code quality issues", "long method", "god class", "feature envy", "data clumps", "shotgun surgery", "code review quality", "structural problems", "anti-patterns"

## What This Skill Does

This skill provides a structured methodology for code smell detection:

- **Smell Identification**: Scans code for patterns matching known smell categories from Martin Fowler's catalog, Robert C. Martin's Clean Code, and other established references
- **Severity Scoring**: Assigns each detected smell a severity level (low, medium, high, critical) based on impact, scope, and frequency
- **Category Classification**: Groups smells into bloaters, object-orientation abusers, change preventers, dispensables, and couplers
- **Detection Heuristics**: Applies quantitative thresholds (line counts, parameter counts, dependency counts) and qualitative pattern matching
- **Refactoring Recommendations**: Maps each smell to one or more recommended refactoring patterns with step-by-step guidance
- **Priority Ranking**: Ranks detected smells by remediation value (effort vs. impact) to guide refactoring order

## Instructions

### Step 1: Understand the Smell Categories

Code smells fall into five major categories. Each category targets a different class of structural problem.

#### Bloaters

Bloaters are code constructs that have grown excessively large, making them difficult to understand, test, and modify.

| Smell | Detection Heuristic | Threshold | Severity |
|-------|---------------------|-----------|----------|
| **Long Method** | Line count, cyclomatic complexity | >25 lines or complexity >10 | Medium-High |
| **Large Class** | Line count, number of fields/methods | >300 lines or >20 methods | High |
| **Long Parameter List** | Parameter count | >4 parameters | Medium |
| **Primitive Obsession** | Ratio of primitive types to domain objects | Multiple related primitives passed together | Medium |
| **Data Clumps** | Groups of variables that appear together repeatedly | Same 3+ variables in multiple locations | Medium |

#### Object-Orientation Abusers

These smells indicate incorrect or incomplete application of object-oriented principles.

| Smell | Detection Heuristic | Threshold | Severity |
|-------|---------------------|-----------|----------|
| **Switch Statements** | switch/case or if-else chains on type | >3 branches on same discriminator | Medium |
| **Parallel Inheritance Hierarchies** | Creating a subclass in one hierarchy requires creating one in another | Any occurrence | High |
| **Refused Bequest** | Subclass uses only a few inherited methods/fields | <30% usage of parent interface | Medium |
| **Alternative Classes with Different Interfaces** | Two classes perform similar work with different method signatures | Semantic similarity >70% | Medium |

#### Change Preventers

These smells make it disproportionately difficult to change the code in one place without cascading changes elsewhere.

| Smell | Detection Heuristic | Threshold | Severity |
|-------|---------------------|-----------|----------|
| **Divergent Change** | One class is changed for multiple unrelated reasons | >2 distinct change axes | High |
| **Shotgun Surgery** | One logical change requires editing many classes | >3 classes modified for one change | Critical |
| **Feature Envy** | A method accesses data from another class more than its own | >50% external field access | High |

#### Dispensables

Code that is unnecessary and whose removal would make the codebase cleaner.

| Smell | Detection Heuristic | Threshold | Severity |
|-------|---------------------|-----------|----------|
| **Dead Code** | Unreachable or unused code | Any occurrence | Medium |
| **Speculative Generality** | Abstract classes, interfaces, or parameters used by only one consumer | Single implementation with no planned extension | Low-Medium |
| **Duplicate Code** | Identical or near-identical code blocks | >5 lines duplicated in 2+ places | High |
| **Lazy Class** | A class that does too little to justify its existence | <3 methods, <30 lines of logic | Low |
| **Comments (as deodorant)** | Excessive comments explaining confusing code | Comments that describe "what" not "why" | Low |

#### Couplers

These smells indicate excessive coupling between classes or modules.

| Smell | Detection Heuristic | Threshold | Severity |
|-------|---------------------|-----------|----------|
| **Message Chains** | Long chains of method calls (a.b().c().d()) | >3 chained calls | Medium |
| **Middle Man** | A class that delegates almost all work to another | >50% methods are pure delegation | Medium |
| **Inappropriate Intimacy** | Two classes access each other's private internals | Bidirectional private access | High |
| **Incomplete Library Class** | A library class is missing needed functionality, leading to workarounds | Utility methods wrapping library calls | Low |

### Step 2: Apply Detection Heuristics

For each file or module under review, apply the following detection process.

#### Python Example: Detecting Long Method and Long Parameter List

```python
# SMELL: Long Method (42 lines, cyclomatic complexity 14)
# SMELL: Long Parameter List (7 parameters)
def process_order(customer_id, product_id, quantity, discount_code,
                  shipping_method, gift_wrap, special_instructions):
    customer = db.get_customer(customer_id)
    if not customer:
        raise ValueError("Customer not found")
    if customer.is_suspended:
        raise ValueError("Customer account suspended")

    product = db.get_product(product_id)
    if not product:
        raise ValueError("Product not found")
    if product.stock < quantity:
        raise ValueError("Insufficient stock")

    base_price = product.price * quantity
    if discount_code:
        discount = db.get_discount(discount_code)
        if discount and discount.is_valid():
            if discount.type == "percentage":
                base_price *= (1 - discount.value / 100)
            elif discount.type == "fixed":
                base_price -= discount.value
            elif discount.type == "buy_one_get_one":
                free_items = quantity // 2
                base_price -= free_items * product.price

    shipping_cost = calculate_shipping(product, quantity, shipping_method)
    if gift_wrap:
        shipping_cost += 5.99

    tax = calculate_tax(base_price, customer.state)
    total = base_price + shipping_cost + tax

    order = Order(
        customer_id=customer_id,
        product_id=product_id,
        quantity=quantity,
        subtotal=base_price,
        shipping=shipping_cost,
        tax=tax,
        total=total,
        special_instructions=special_instructions,
    )
    db.save_order(order)
    send_confirmation_email(customer, order)
    update_inventory(product, quantity)
    return order
```

**Detected smells**:

1. **Long Method** (severity: high) -- 42 lines with validation, pricing, discount logic, tax, and persistence all in one method
2. **Long Parameter List** (severity: medium) -- 7 parameters indicate a missing parameter object
3. **Switch Statements** (severity: medium) -- if/elif chain on `discount.type` suggests polymorphism

**Recommended refactoring**:

```python
@dataclass
class OrderRequest:
    customer_id: str
    product_id: str
    quantity: int
    discount_code: str | None = None
    shipping_method: str = "standard"
    gift_wrap: bool = False
    special_instructions: str = ""


def process_order(request: OrderRequest) -> Order:
    customer = _validate_customer(request.customer_id)
    product = _validate_product(request.product_id, request.quantity)
    pricing = _calculate_pricing(product, request)
    order = _create_order(customer, product, request, pricing)
    _finalize_order(customer, product, order, request.quantity)
    return order


def _validate_customer(customer_id: str) -> Customer:
    customer = db.get_customer(customer_id)
    if not customer:
        raise ValueError("Customer not found")
    if customer.is_suspended:
        raise ValueError("Customer account suspended")
    return customer


def _validate_product(product_id: str, quantity: int) -> Product:
    product = db.get_product(product_id)
    if not product:
        raise ValueError("Product not found")
    if product.stock < quantity:
        raise ValueError("Insufficient stock")
    return product


def _calculate_pricing(product: Product, request: OrderRequest) -> OrderPricing:
    base_price = product.price * request.quantity
    discount = _apply_discount(base_price, request.discount_code, product, request.quantity)
    shipping = calculate_shipping(product, request.quantity, request.shipping_method)
    if request.gift_wrap:
        shipping += 5.99
    tax = calculate_tax(discount, product.customer_state)
    return OrderPricing(subtotal=discount, shipping=shipping, tax=tax)
```

#### JavaScript Example: Detecting Feature Envy and Data Clumps

```javascript
// SMELL: Feature Envy -- this function accesses invoice fields extensively
// SMELL: Data Clumps -- address fields always appear together
function formatInvoiceSummary(invoice) {
    const customerName = invoice.customer.firstName + " " + invoice.customer.lastName;
    const address = invoice.customer.street + ", " +
        invoice.customer.city + ", " +
        invoice.customer.state + " " +
        invoice.customer.zip;
    const subtotal = invoice.items.reduce((sum, item) => sum + item.price * item.qty, 0);
    const tax = subtotal * invoice.taxRate;
    const total = subtotal + tax;
    const due = new Date(invoice.createdAt);
    due.setDate(due.getDate() + invoice.paymentTermsDays);

    return {
        to: customerName,
        address: address,
        subtotal: subtotal.toFixed(2),
        tax: tax.toFixed(2),
        total: total.toFixed(2),
        dueDate: due.toISOString().split("T")[0],
    };
}
```

**Detected smells**:

1. **Feature Envy** (severity: high) -- `formatInvoiceSummary` accesses customer and invoice internals; this logic should live on the Invoice or Customer class
2. **Data Clumps** (severity: medium) -- street, city, state, zip always appear together and should be an Address object
3. **Primitive Obsession** (severity: medium) -- payment terms as raw integer days, tax rate as raw float

**Recommended refactoring**:

```javascript
class Address {
    constructor(street, city, state, zip) {
        this.street = street;
        this.city = city;
        this.state = state;
        this.zip = zip;
    }

    format() {
        return `${this.street}, ${this.city}, ${this.state} ${this.zip}`;
    }
}

class Invoice {
    getSummary() {
        return {
            to: this.customer.fullName(),
            address: this.customer.address.format(),
            subtotal: this.calculateSubtotal().toFixed(2),
            tax: this.calculateTax().toFixed(2),
            total: this.calculateTotal().toFixed(2),
            dueDate: this.calculateDueDate(),
        };
    }

    calculateSubtotal() {
        return this.items.reduce((sum, item) => sum + item.lineTotal(), 0);
    }

    calculateTax() {
        return this.calculateSubtotal() * this.taxRate;
    }

    calculateTotal() {
        return this.calculateSubtotal() + this.calculateTax();
    }
}
```

#### Java Example: Detecting God Class and Shotgun Surgery

```java
// SMELL: God Class -- this class handles authentication, authorization,
// session management, password policy, audit logging, and user CRUD
public class UserManager {
    private UserRepository userRepo;
    private SessionStore sessionStore;
    private PasswordEncoder encoder;
    private AuditLogger auditLogger;
    private EmailService emailService;
    private RoleRepository roleRepo;
    private PermissionCache permissionCache;
    private TokenGenerator tokenGenerator;
    private RateLimiter rateLimiter;

    public User authenticate(String username, String password) { /* 30 lines */ }
    public void logout(String sessionId) { /* 15 lines */ }
    public Session createSession(User user) { /* 20 lines */ }
    public boolean authorize(User user, String resource, String action) { /* 25 lines */ }
    public void changePassword(User user, String oldPw, String newPw) { /* 35 lines */ }
    public void resetPassword(String email) { /* 25 lines */ }
    public boolean validatePasswordPolicy(String password) { /* 20 lines */ }
    public User createUser(UserDTO dto) { /* 30 lines */ }
    public User updateUser(String id, UserDTO dto) { /* 25 lines */ }
    public void deleteUser(String id) { /* 20 lines */ }
    public void assignRole(String userId, String roleId) { /* 15 lines */ }
    public void revokeRole(String userId, String roleId) { /* 15 lines */ }
    public List<Permission> getEffectivePermissions(String userId) { /* 20 lines */ }
    public void logAuditEvent(String userId, String action, String details) { /* 10 lines */ }
    public void sendWelcomeEmail(User user) { /* 15 lines */ }
    public void sendPasswordResetEmail(String email, String token) { /* 15 lines */ }
    // ... 10 more methods
}
```

**Detected smells**:

1. **God Class** (severity: critical) -- UserManager has 9 dependencies, 16+ methods, and at least 6 distinct responsibilities
2. **Shotgun Surgery** (severity: critical) -- changing authentication logic requires understanding session, audit, and rate-limiting concerns interleaved in this class
3. **Divergent Change** (severity: high) -- this class changes for authentication reasons, authorization reasons, password policy reasons, email reasons, and CRUD reasons

**Recommended refactoring**: Extract into focused classes:

```java
public class AuthenticationService {
    private final UserRepository userRepo;
    private final PasswordEncoder encoder;
    private final SessionManager sessionManager;
    private final RateLimiter rateLimiter;

    public AuthResult authenticate(String username, String password) {
        rateLimiter.checkLimit(username);
        User user = userRepo.findByUsername(username)
            .orElseThrow(() -> new AuthenticationException("Invalid credentials"));
        if (!encoder.matches(password, user.getPasswordHash())) {
            throw new AuthenticationException("Invalid credentials");
        }
        Session session = sessionManager.create(user);
        return new AuthResult(user, session);
    }
}

public class AuthorizationService {
    private final RoleRepository roleRepo;
    private final PermissionCache permissionCache;

    public boolean authorize(User user, String resource, String action) {
        List<Permission> permissions = permissionCache.getOrLoad(
            user.getId(), () -> roleRepo.getEffectivePermissions(user.getId()));
        return permissions.stream()
            .anyMatch(p -> p.matches(resource, action));
    }
}

public class PasswordService {
    private final PasswordEncoder encoder;
    private final PasswordPolicy policy;
    private final UserRepository userRepo;

    public void changePassword(User user, String oldPassword, String newPassword) {
        if (!encoder.matches(oldPassword, user.getPasswordHash())) {
            throw new InvalidPasswordException("Current password incorrect");
        }
        policy.validate(newPassword);
        user.setPasswordHash(encoder.encode(newPassword));
        userRepo.save(user);
    }
}
```

### Step 3: Score Severity

Apply the following scoring rubric to each detected smell.

#### Severity Scoring Matrix

| Factor | Weight | Low (1) | Medium (2) | High (3) | Critical (4) |
|--------|--------|---------|------------|----------|---------------|
| **Scope** | 30% | Single method | Single class | Multiple classes | Cross-module |
| **Frequency** | 25% | 1 occurrence | 2-5 occurrences | 6-15 occurrences | >15 occurrences |
| **Change Impact** | 25% | Rarely changes | Occasional changes | Frequent changes | Every sprint |
| **Comprehension Cost** | 20% | Minor confusion | Slows onboarding | Blocks understanding | Causes defects |

**Composite severity** = (Scope x 0.30) + (Frequency x 0.25) + (Change Impact x 0.25) + (Comprehension Cost x 0.20)

- 1.0-1.5: Low -- address during routine maintenance
- 1.6-2.5: Medium -- schedule for next refactoring cycle
- 2.6-3.2: High -- prioritize in current sprint
- 3.3-4.0: Critical -- address immediately, blocking quality

### Step 4: Map Smells to Refactorings

Use the following mapping to determine which refactoring technique resolves each smell.

| Smell | Primary Refactoring | Secondary Refactoring |
|-------|---------------------|----------------------|
| Long Method | Extract Method | Replace Temp with Query |
| Large Class / God Class | Extract Class | Extract Subclass |
| Long Parameter List | Introduce Parameter Object | Preserve Whole Object |
| Feature Envy | Move Method | Extract Method + Move |
| Data Clumps | Extract Class | Introduce Parameter Object |
| Primitive Obsession | Replace Primitive with Value Object | Replace Type Code with Subclasses |
| Switch Statements | Replace Conditional with Polymorphism | Replace Type Code with Strategy |
| Shotgun Surgery | Move Method, Inline Class | Consolidate into single class |
| Divergent Change | Extract Class | Split by responsibility axis |
| Duplicate Code | Extract Method | Pull Up Method, Form Template Method |
| Dead Code | Remove Dead Code | Collapse Hierarchy |
| Message Chains | Hide Delegate | Extract Method |
| Middle Man | Remove Middle Man | Inline Class |
| Speculative Generality | Collapse Hierarchy | Remove unused abstractions |

### Step 5: Generate the Smell Report

Produce a structured report for each reviewed file or module.

**Report format**:

```
## Code Smell Report: {file or module name}

### Summary
- Total smells detected: {count}
- Critical: {count} | High: {count} | Medium: {count} | Low: {count}
- Estimated remediation effort: {hours}

### Findings

#### 1. {Smell Name} (Severity: {level})
- **Location**: {file}:{line range}
- **Description**: {what the smell is and why it matters}
- **Evidence**: {specific metrics -- line count, parameter count, dependency count}
- **Recommended refactoring**: {technique name}
- **Effort estimate**: {hours}
- **Risk**: {low/medium/high} -- {what could go wrong during refactoring}

#### 2. {Smell Name} (Severity: {level})
...

### Priority Order
1. {Most impactful smell to fix first}
2. {Second priority}
...
```

## Best Practices

- **Start with the highest-severity smells**: critical and high-severity smells block productivity and cause defects; address them first
- **Fix smells incrementally**: do not attempt to refactor an entire god class in one commit; extract one responsibility at a time and verify tests pass between each extraction
- **Use IDE refactoring tools**: automated Extract Method, Rename, and Move refactorings are safer than manual edits; always prefer tool-assisted refactoring
- **Maintain test coverage during detection**: before declaring a smell "fixed", confirm that all existing tests still pass and coverage has not decreased
- **Calibrate thresholds per project**: a 25-line method threshold may be too strict for data transformation code and too lenient for business logic; adjust based on project context
- **Distinguish intentional trade-offs from accidental smells**: not every long method is a problem; some algorithms are inherently complex and splitting them reduces readability
- **Track smell trends over time**: measure total smell count, average severity, and remediation velocity across sprints to confirm quality is improving
- **Combine with static analysis tools**: use tools like SonarQube, PMD, Pylint, or ESLint as a first pass, then apply this skill for deeper structural analysis that tools miss
- **Document smell exceptions**: when a team decides to accept a smell intentionally, document the rationale in an Architecture Decision Record or inline comment

## Common Pitfalls

- **Over-detection**: flagging every method over 10 lines as a smell creates noise and erodes developer trust; use reasonable thresholds and context
- **Refactoring without tests**: attempting to fix smells in untested code often introduces regressions; write characterization tests first, then refactor
- **Treating all smells equally**: a low-severity "lazy class" in stable, rarely-changed code does not warrant the same urgency as a critical "shotgun surgery" in actively-developed code
- **Ignoring domain context**: code that appears to have "feature envy" may actually be a legitimate cross-cutting concern such as logging, validation, or serialization
- **Confusing verbosity with smell**: longer code that is clearly structured and well-named is not automatically a smell; clarity matters more than brevity
- **Premature abstraction**: extracting classes and interfaces to fix "primitive obsession" before understanding the domain can create speculative generality, trading one smell for another
- **Fixing smells in code scheduled for deletion**: if a module is being replaced next quarter, investing in smell remediation is wasted effort; focus on code with a long expected lifespan
- **Missing the root cause**: sometimes multiple surface-level smells (long method, data clumps, feature envy) all stem from a single architectural problem such as a missing domain object; fix the root cause rather than treating symptoms individually
- **Not communicating with the team**: refactoring shared code without informing other developers causes merge conflicts and confusion; coordinate smell fixes through your team's normal workflow

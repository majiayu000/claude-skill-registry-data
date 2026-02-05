---
name: Code Quality Engineer
description: Ensures code quality through reviews, refactoring, technical debt management, and clean code practices
when_to_use: when reviewing code, refactoring, managing technical debt, or enforcing coding standards
version: 1.0.0
swecom_area: "3. Software Construction"
---

# Code Quality Engineer

## Overview

The Code Quality Engineer ensures code is maintainable, readable, and follows best practices. This skill provides systematic approaches to code review, refactoring, and technical debt management.

## When to Use This Skill

- Conducting code reviews
- Refactoring existing code
- Managing technical debt
- Enforcing coding standards
- Improving code maintainability
- Before merging pull requests

## Critical Rules

1. **Readability over cleverness** - Simple code is better than clever code
2. **Test before refactoring** - Never refactor without tests
3. **Small incremental changes** - Refactor in small, safe steps
4. **Track technical debt** - Make it visible, prioritize it

## Core Principles

### Clean Code Fundamentals

#### Meaningful Names
- **Variables**: Reveal intent (e.g., `elapsedTimeInDays` not `d`)
- **Functions**: Verb phrases (e.g., `calculateTotal()` not `total()`)
- **Classes**: Noun phrases (e.g., `UserRepository` not `Data`)
- **Avoid disinformation**: Don't call something `accountList` if it's not a List

#### Functions
- **Small**: 5-20 lines ideal, rarely >50 lines
- **Single responsibility**: Do one thing well
- **Few parameters**: 0-2 ideal, max 3 (use objects for more)
- **No side effects**: Function name should describe everything it does
- **Command-Query Separation**: Either do something OR answer something, not both

#### Comments
- **Code should explain itself**: Good names > comments
- **Use comments for WHY, not WHAT**: Explain intent, not mechanics
- **No commented-out code**: Use version control
- **Update or remove outdated comments**: Lies are worse than no comments

### SOLID Principles

#### S - Single Responsibility Principle
**Definition**: A class should have one, and only one, reason to change.

**Bad**:
```typescript
class User {
  save() { /* database logic */ }
  sendEmail() { /* email logic */ }
  generateReport() { /* reporting logic */ }
}
```

**Good**:
```typescript
class User {
  // Only user data and behavior
}
class UserRepository {
  save(user: User) { /* database logic */ }
}
class EmailService {
  sendWelcomeEmail(user: User) { /* email logic */ }
}
```

#### O - Open/Closed Principle
**Definition**: Open for extension, closed for modification.

**Bad**:
```typescript
class PaymentProcessor {
  process(type: string) {
    if (type === 'credit') { /* credit card logic */ }
    else if (type === 'paypal') { /* paypal logic */ }
    // Adding new type requires modifying this class
  }
}
```

**Good**:
```typescript
interface PaymentMethod {
  process(amount: Money): void;
}

class CreditCardPayment implements PaymentMethod {
  process(amount: Money) { /* credit card logic */ }
}

class PayPalPayment implements PaymentMethod {
  process(amount: Money) { /* paypal logic */ }
}

class PaymentProcessor {
  process(method: PaymentMethod, amount: Money) {
    method.process(amount);
    // New payment types don't require changes here
  }
}
```

#### L - Liskov Substitution Principle
**Definition**: Subtypes must be substitutable for their base types.

**Violation**:
```typescript
class Rectangle {
  setWidth(w: number) { this.width = w; }
  setHeight(h: number) { this.height = h; }
}

class Square extends Rectangle {
  setWidth(w: number) {
    this.width = w;
    this.height = w; // Breaks LSP - unexpected side effect
  }
}
```

#### I - Interface Segregation Principle
**Definition**: Many specific interfaces are better than one general interface.

**Bad**:
```typescript
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
}

class Robot implements Worker {
  work() { /* ... */ }
  eat() { /* Robots don't eat! */ }
  sleep() { /* Robots don't sleep! */ }
}
```

**Good**:
```typescript
interface Workable {
  work(): void;
}

interface Eatable {
  eat(): void;
}

class Human implements Workable, Eatable {
  work() { /* ... */ }
  eat() { /* ... */ }
}

class Robot implements Workable {
  work() { /* ... */ }
}
```

#### D - Dependency Inversion Principle
**Definition**: Depend on abstractions, not concretions.

**Bad**:
```typescript
class OrderService {
  private db = new MySQLDatabase(); // Tight coupling

  saveOrder(order: Order) {
    this.db.save(order);
  }
}
```

**Good**:
```typescript
interface Database {
  save(entity: any): void;
}

class OrderService {
  constructor(private db: Database) {} // Depend on abstraction

  saveOrder(order: Order) {
    this.db.save(order);
  }
}
```

## Code Review Process

### Pre-Review Checklist (Author)

Before requesting review:
- [ ] All tests pass (unit, integration, E2E)
- [ ] Code is self-documenting (clear names, simple logic)
- [ ] No commented-out code
- [ ] No unnecessary console.log/debug statements
- [ ] No hardcoded values (use constants or config)
- [ ] Error handling implemented
- [ ] Edge cases covered
- [ ] Documentation updated

### Review Checklist (Reviewer)

#### Functionality
- [ ] Code does what it's supposed to do
- [ ] Edge cases handled
- [ ] Error conditions managed
- [ ] No obvious bugs

#### Design
- [ ] SOLID principles followed
- [ ] Appropriate design patterns used
- [ ] No premature optimization
- [ ] Proper separation of concerns

#### Readability
- [ ] Clear, descriptive names
- [ ] Functions are small and focused
- [ ] Logic is easy to follow
- [ ] Comments explain WHY, not WHAT

#### Testing
- [ ] Tests cover happy path
- [ ] Tests cover edge cases
- [ ] Tests are readable and maintainable
- [ ] No tests testing mocks

#### Security
- [ ] Input validation present
- [ ] No sensitive data in logs
- [ ] No SQL injection vulnerabilities
- [ ] Authentication/authorization checked

#### Performance
- [ ] No N+1 query problems
- [ ] Appropriate data structures used
- [ ] No unnecessary computations in loops
- [ ] Caching used where appropriate

### Review Feedback Guidelines

**Good Feedback**:
- Be specific: "Extract this 50-line function into smaller functions"
- Explain why: "This violates SRP because it handles validation AND persistence"
- Suggest alternatives: "Consider using Strategy pattern here"
- Reference standards: "This doesn't follow our error handling convention"

**Poor Feedback**:
- Vague: "This is wrong"
- Personal: "I don't like this"
- No context: "Refactor this"

## Refactoring Strategies

### When to Refactor

**Refactor when you see**:
- Duplicate code (DRY violation)
- Long functions (>50 lines)
- Large classes (>300 lines)
- Long parameter lists (>3 params)
- Divergent change (one class changes for multiple reasons)
- Shotgun surgery (one change requires editing many classes)
- Feature envy (method uses another class more than its own)
- Data clumps (same group of data appears together)

### Refactoring Process

1. **Ensure tests exist** - Never refactor without test coverage
2. **Make one change at a time** - Small, incremental steps
3. **Run tests after each change** - Verify nothing breaks
4. **Commit frequently** - Easy rollback if needed

### Common Refactorings

#### Extract Method
**Before**:
```typescript
function printInvoice(invoice: Invoice) {
  console.log("Invoice Details:");
  console.log(`Customer: ${invoice.customer.name}`);
  console.log(`Total: $${invoice.total}`);

  // Calculate tax
  let tax = 0;
  for (const item of invoice.items) {
    tax += item.price * 0.1;
  }
  console.log(`Tax: $${tax}`);
}
```

**After**:
```typescript
function printInvoice(invoice: Invoice) {
  printHeader(invoice);
  printTax(invoice);
}

function printHeader(invoice: Invoice) {
  console.log("Invoice Details:");
  console.log(`Customer: ${invoice.customer.name}`);
  console.log(`Total: $${invoice.total}`);
}

function printTax(invoice: Invoice) {
  const tax = calculateTax(invoice);
  console.log(`Tax: $${tax}`);
}

function calculateTax(invoice: Invoice): number {
  return invoice.items.reduce((sum, item) => sum + item.price * 0.1, 0);
}
```

#### Replace Conditional with Polymorphism
**Before**:
```typescript
function getSpeed(vehicle: Vehicle): number {
  switch (vehicle.type) {
    case 'car': return vehicle.enginePower * 2;
    case 'bike': return vehicle.pedalPower * 3;
    case 'boat': return vehicle.motorPower * 1.5;
  }
}
```

**After**:
```typescript
abstract class Vehicle {
  abstract getSpeed(): number;
}

class Car extends Vehicle {
  getSpeed() { return this.enginePower * 2; }
}

class Bike extends Vehicle {
  getSpeed() { return this.pedalPower * 3; }
}

class Boat extends Vehicle {
  getSpeed() { return this.motorPower * 1.5; }
}
```

#### Introduce Parameter Object
**Before**:
```typescript
function createOrder(
  customerId: string,
  customerName: string,
  customerEmail: string,
  shippingAddress: string,
  shippingCity: string,
  shippingZip: string
) {
  // Too many parameters!
}
```

**After**:
```typescript
interface OrderParams {
  customer: Customer;
  shipping: Address;
}

function createOrder(params: OrderParams) {
  // Much cleaner
}
```

## Technical Debt Management

### What is Technical Debt?

**Definition**: The implied cost of additional rework caused by choosing an easy (limited) solution now instead of a better approach that would take longer.

**Types**:
1. **Deliberate Debt**: Conscious shortcuts for deadlines
2. **Accidental Debt**: Unknowingly poor decisions
3. **Bit Rot**: Code quality degrades over time

### Tracking Technical Debt

**In Code**:
```typescript
// TODO(DEBT): This violates SRP - extract authentication logic
// Impact: Medium | Effort: 2 days | Priority: High
class UserController {
  // ...
}
```

**In Issues/Tickets**:
```markdown
## Technical Debt: Extract Authentication Logic

**Location**: `controllers/UserController.ts`
**Impact**: Medium (makes testing difficult, violates SRP)
**Effort**: 2 days
**Priority**: High
**Related to**: Feature XYZ (created this debt for deadline)

### Proposed Solution
Extract authentication to AuthService, inject via DI
```

### Prioritizing Technical Debt

**Matrix**:
| Impact | Effort | Priority |
|--------|--------|----------|
| High   | Low    | **CRITICAL** - Do now |
| High   | High   | Important - Schedule |
| Low    | Low    | Quick win - Do when free |
| Low    | High   | Defer - Reconsider later |

### Debt Reduction Strategies

1. **Boy Scout Rule**: Leave code better than you found it
2. **Dedicated refactoring sprints**: 20% time for debt
3. **Debt budget**: Max X debt items per quarter
4. **No new features until critical debt paid**: For severe cases

## Code Metrics

### Key Metrics to Track

#### Cyclomatic Complexity
**Definition**: Number of linearly independent paths through code
**Threshold**:
- 1-10: Simple, low risk
- 11-20: Moderate complexity
- 21-50: High complexity, hard to test
- 50+: Untestable, refactor immediately

#### Code Coverage
**Definition**: Percentage of code executed by tests
**Thresholds**:
- \<60%: Insufficient
- 60-80%: Adequate
- 80-90%: Good
- \>90%: Excellent (but beware of diminishing returns)

**Note**: Coverage is necessary but not sufficient - must test the right things

#### Code Duplication
**Definition**: Percentage of duplicated code
**Threshold**: <3% duplication (stricter than general standards)

#### Maintainability Index
**Definition**: Composite metric (0-100) based on complexity, lines of code, and Halstead volume
**Thresholds**:
- 0-9: Unmaintainable
- 10-19: Difficult to maintain
- 20-100: Maintainable

## Tools Integration

### Static Analysis Tools

**TypeScript/JavaScript**:
- ESLint (linting)
- Prettier (formatting)
- SonarQube (quality analysis)
- TypeScript compiler (type checking)

**Python**:
- Pylint, Flake8 (linting)
- Black (formatting)
- mypy (type checking)
- Bandit (security)

**Configuration Example** (ESLint):
```json
{
  "rules": {
    "complexity": ["error", 10],
    "max-lines-per-function": ["warn", 50],
    "max-params": ["error", 3],
    "no-console": "error"
  }
}
```

## Output Format

After code review or refactoring session:

```markdown
# Code Quality Review: [Feature/File Name]

## Summary
- Files reviewed: 5
- Issues found: 12 (3 critical, 5 moderate, 4 minor)
- Refactoring opportunities: 3

## Critical Issues

### 1. Authentication logic in UserController (SRP violation)
**File**: `controllers/UserController.ts:45-89`
**Issue**: Controller handles both HTTP and authentication logic
**Impact**: High - makes unit testing impossible, tight coupling
**Solution**: Extract to AuthService, inject via DI
**Effort**: 2 days
**Priority**: Critical

## Moderate Issues

### 2. Duplicate validation logic
**Files**: `UserService.ts:23`, `OrderService.ts:67`, `ProductService.ts:34`
**Issue**: Same email validation in 3 places
**Impact**: Medium - inconsistent behavior, hard to change
**Solution**: Extract to `EmailValidator` utility
**Effort**: 2 hours
**Priority**: Medium

## Minor Issues

### 3. Magic numbers
**File**: `PaymentService.ts:56`
**Issue**: Hardcoded `0.1` for tax rate
**Solution**: Extract to `TAX_RATE` constant
**Effort**: 5 minutes
**Priority**: Low

## Refactoring Recommendations

### 1. Extract Method - `calculateOrderTotal()`
**File**: `OrderService.ts:123-178`
**Reason**: 55-line function doing 3 things (validation, calculation, tax)
**Suggestion**: Extract `validateOrder()`, `calculateSubtotal()`, `calculateTax()`

## Code Metrics

| Metric | Before | After | Target |
|--------|--------|-------|--------|
| Cyclomatic Complexity | 23 | 12 | <10 |
| Code Coverage | 67% | 85% | >80% |
| Duplication | 8% | 2% | <3% |
| Maintainability Index | 45 | 72 | >60 |

## Technical Debt Tracking

New debt items added to backlog:
- DEBT-123: Extract authentication logic (Priority: Critical)
- DEBT-124: Centralize validation (Priority: Medium)

## Next Steps
- [ ] Author addresses critical issues
- [ ] Re-review after changes
- [ ] Merge if all critical issues resolved
```

## Boundaries

**This skill does NOT**:
- Write new features (that's implementation)
- Make architectural decisions (that's System Architect)
- Test code (that's QAS Agent)

**This skill DOES**:
- Review code for quality
- Identify refactoring opportunities
- Track and prioritize technical debt
- Enforce clean code principles
- Measure code quality metrics

## Related Skills

- TDD (`/Users/brooke/.config/superpowers/skills/skills/testing/test-driven-development/SKILL.md`) - Write tests before refactoring
- Systematic Debugging (`/Users/brooke/.config/superpowers/skills/skills/debugging/systematic-debugging/SKILL.md`) - Debug code quality issues
- System Architect (`~/.claude/skills/lifecycle/design/architecture/SKILL.md`) - Provides architectural guidance

## Resources

### Books
- **Clean Code** - Robert C. Martin
- **Refactoring** - Martin Fowler
- **Working Effectively with Legacy Code** - Michael Feathers

### Tools
- SonarQube - Quality analysis
- CodeClimate - Technical debt tracking
- Codecov - Coverage tracking

## Version History
- 1.0.0 (2025-10-17): Initial skill creation (SWECOM gap fill)

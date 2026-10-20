---
name: "core-principles"
description: 'Apply fundamental coding principles including SOLID, DRY, KISS, and common design patterns. Use when refactoring code for maintainability, reviewing design pattern usage, teaching SOLID principles, or evaluating code quality against engineering standards.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
compatibility:
 languages: ["csharp"]
---

# Core Principles

> **Purpose**: Fundamental principles guiding production code development. 
> **Focus**: SOLID, DRY, KISS, design patterns.

---

## When to Use This Skill

- Reviewing code for SOLID principle compliance
- Refactoring code for maintainability
- Choosing appropriate design patterns
- Teaching or evaluating engineering standards

## Prerequisites

- Basic OOP programming knowledge

## SOLID Principles

### Single Responsibility (SRP)
Each class has one reason to change.

```csharp
// [FAIL] Multiple responsibilities
public class User
{
 public string Name { get; set; }
 public void SaveToDatabase() { } // Persistence
 public void SendEmail() { } // Communication
}

// [PASS] Single responsibility
public class User
{
 public string Name { get; set; }
}
public class UserRepository
{
 public void Save(User user) { }
}
public class EmailService
{
 public void SendEmail(User user) { }
}
```

### Open/Closed (OCP)
Open for extension, closed for modification.

```csharp
// [PASS] Extend via abstraction
public interface IPaymentProcessor
{
 Task<PaymentResult> ProcessAsync(decimal amount);
}

public class CreditCardProcessor : IPaymentProcessor { }
public class PayPalProcessor : IPaymentProcessor { }

public class PaymentService
{
 public async Task ProcessPaymentAsync(IPaymentProcessor processor, decimal amount)
 {
 return await processor.ProcessAsync(amount);
 }
}
```

### Liskov Substitution (LSP)
Subtypes must be substitutable for base types.

```csharp
// [PASS] Derived classes extend, don't break behavior
public abstract class Bird
{
 public abstract void Move();
}

public class Sparrow : Bird
{
 public override void Move() => Fly();
}

public class Penguin : Bird
{
 public override void Move() => Walk(); // Different but valid
}
```

### Interface Segregation (ISP)
Many specific interfaces > one general interface.

```csharp
// [FAIL] Fat interface
public interface IWorker
{
 void Work();
 void Eat();
 void Sleep();
}

// [PASS] Segregated interfaces
public interface IWorkable { void Work(); }
public interface IFeedable { void Eat(); }
public interface IRestable { void Sleep(); }
```

### Dependency Inversion (DIP)
Depend on abstractions, not concretions.

```csharp
// [PASS] Depend on interface
public class OrderService
{
 private readonly IOrderRepository _repository;
 
 public OrderService(IOrderRepository repository)
 {
 _repository = repository;
 }
}
```

---

## DRY (Don't Repeat Yourself)

```csharp
// [FAIL] Duplication
public class UserService
{
 public User GetUser(int id)
 {
 var conn = new SqlConnection(connectionString);
 conn.Open();
 // ... query logic
 }
 
 public Order GetOrder(int id)
 {
 var conn = new SqlConnection(connectionString);
 conn.Open();
 // ... query logic
 }
}

// [PASS] Extract common logic
public abstract class BaseRepository
{
 protected SqlConnection GetConnection()
 {
 var conn = new SqlConnection(connectionString);
 conn.Open();
 return conn;
 }
}
```

---

## KISS (Keep It Simple, Stupid)

```csharp
// [FAIL] Overengineered
public class UserValidator
{
 public bool Validate(User user)
 {
 var strategy = ValidatorStrategyFactory
 .CreateStrategy(user.UserType)
 .GetValidationChain()
 .Execute(new ValidationContext(user));
 return strategy.IsValid;
 }
}

// [PASS] Simple
public class UserValidator
{
 public bool Validate(User user)
 {
 return !string.IsNullOrEmpty(user.Email) &&
 user.Email.Contains("@") &&
 user.Age >= 13;
 }
}
```

---

## YAGNI (You Aren't Gonna Need It)

Don't build features "just in case". Build what's needed now.

---

## Best Practices

### [PASS] DO

- **Follow SOLID** - Especially SRP and DIP
- **Keep functions small** - One thing, well
- **Use meaningful names** - Self-documenting code
- **Favor composition** - Over inheritance
- **Write tests** - Design for testability
- **Refactor regularly** - Improve as you go
- **Document complex logic** - Why, not what

### [FAIL] DON'T

- **Violate SOLID** - Leads to rigid, fragile code
- **Duplicate code** - Extract to methods/classes
- **Overcomplicate** - Simple solutions first
- **Build unused features** - YAGNI
- **Skip code reviews** - Catch issues early
- **Ignore tech debt** - Pay it down regularly

---

**See Also**: [Code Organization](../code-organization/SKILL.md) - [Testing](../../development/testing/SKILL.md)

**Last Updated**: January 13, 2026

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Over-engineering with patterns | Apply YAGNI - only use patterns when complexity warrants them |
| DRY violation detected | Extract shared logic into a utility method or base class |

## References

- [Design Patterns](references/design-patterns.md)
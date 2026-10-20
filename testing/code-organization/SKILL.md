---
name: "code-organization"
description: 'Structure projects for maintainability and scalability with clean architecture and separation of concerns. Use when setting up a new project structure, refactoring monolithic codebases, implementing dependency injection, or organizing modules for team collaboration.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
---

# Code Organization

> **Purpose**: Structure projects for maintainability, scalability, and team collaboration.

---

## When to Use This Skill

- Setting up a new project structure
- Refactoring monolithic codebases
- Implementing dependency injection
- Organizing modules for team collaboration
- Choosing between architectural patterns

## Prerequisites

- Understanding of SOLID principles
- Familiarity with project target language

## Decision Tree

```
Structuring a project?
+- New project?
| +- Single app? -> Standard layered structure (API/Domain/Infra)
| +- Multiple services? -> Monorepo or separate repos
| - Library/package? -> src/ + tests/ + docs/ + examples/
+- Existing project, adding feature?
| +- Follow existing patterns (consistency > perfection)
| - Feature cuts across layers? -> Consider vertical slices
+- File getting too large (> 300 lines)?
| - Split by responsibility (SRP)
+- Folder getting too deep (> 4 levels)?
| - Flatten or reorganize by feature
- Shared code between projects?
 - Extract to shared library / internal package
```

## Project Structure

### C# (.NET Solution)

```
Solution/
+-- src/
| +-- MyProject.Api/ # Web API project
| | +-- Controllers/
| | | +-- UsersController.cs
| | | +-- ProductsController.cs
| | | -- OrdersController.cs
| | +-- Middleware/
| | | +-- AuthenticationMiddleware.cs
| | | +-- LoggingMiddleware.cs
| | | -- RateLimitingMiddleware.cs
| | +-- Filters/
| | | +-- ValidationFilter.cs
| | | -- ExceptionFilter.cs
| | +-- Program.cs
| | +-- Startup.cs # or configure in Program.cs
| | +-- appsettings.json
| | -- appsettings.Development.json
| +-- MyProject.Core/ # Domain/Business logic
| | +-- Entities/
| | | +-- User.cs
| | | +-- Product.cs
| | | -- Order.cs
| | +-- Interfaces/
| | | +-- IUserRepository.cs
| | | +-- IEmailService.cs
| | | -- IPaymentService.cs
| | +-- Services/
| | | +-- UserService.cs
| | | +-- PaymentService.cs
| | | -- EmailService.cs
| | +-- DTOs/
| | | +-- UserDto.cs
| | | -- ProductDto.cs
| | -- Exceptions/
| | +-- UserNotFoundException.cs
| | -- DuplicateEmailException.cs
| +-- MyProject.Infrastructure/ # Data access & external services
| | +-- Data/
| | | +-- ApplicationDbContext.cs
| | | -- Migrations/
| | +-- Repositories/
| | | +-- UserRepository.cs
| | | -- OrderRepository.cs
| | -- Services/
| | +-- EmailService.cs
| | -- BlobStorageService.cs
| -- MyProject.Shared/ # Shared utilities
| +-- Constants/
| | -- AppConstants.cs
| +-- Helpers/
| | -- StringHelper.cs
| -- Validators/
| -- EmailValidator.cs
+-- tests/
| +-- MyProject.UnitTests/
| +-- MyProject.IntegrationTests/
| -- MyProject.E2ETests/
+-- docs/
+-- scripts/
+-- .gitignore
+-- MyProject.sln
-- README.md
```

---

## Best Practices

### 1. Single Responsibility Principle

```csharp
// [FAIL] Bad: Class does too much
public class User
{
 public void SaveToDatabase() { }
 public void SendEmail() { }
 public void GenerateReport() { }
}

// [PASS] Good: Separate concerns
public class User
{
 // Just data and behavior
 public int Id { get; set; }
 public string Email { get; set; }
 public string Name { get; set; }
}

public class UserRepository
{
 public async Task SaveAsync(User user) { }
}

public class EmailService
{
 public async Task SendToUserAsync(User user, string message) { }
}

public class ReportGenerator
{
 public async Task GenerateUserReportAsync(User user) { }
}
```

### 2. Keep Files Small

- Max 300-400 lines per file
- Split large files into smaller classes
- Group related functionality

### 3. Clear Naming

```csharp
// [PASS] Good naming conventions
// Files: PascalCase.cs
// Classes: PascalCase
// Interfaces: IPascalCase
// Methods: PascalCase
// Variables/parameters: camelCase
// Constants: PascalCase or UPPER_SNAKE_CASE

// UserService.cs
public class UserService
{
 private const int MaxLoginAttempts = 3;
 
 public async Task<bool> AuthenticateUserAsync(string email, string password)
 {
 // Implementation
 }
}
```

### 4. Use Namespaces Properly

```csharp
// Organize by feature or layer
namespace MyProject.Core.Services
{
 public class UserService { }
}

namespace MyProject.Core.Entities
{
 public class User { }
}

namespace MyProject.Infrastructure.Repositories
{
 public class UserRepository { }
}

namespace MyProject.Api.Controllers
{
 public class UsersController { }
}
```

---

**Related Skills**:
- [Core Principles](../core-principles/SKILL.md)
- [Scalability](../scalability/SKILL.md)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Circular dependencies | Extract shared interfaces into a separate abstractions project |
| Growing monolith | Identify bounded contexts and extract vertical slices |
| DI container performance | Register scoped/transient services only when needed, prefer singleton for stateless |

## References

- [Code Org Patterns](references/code-org-patterns.md)
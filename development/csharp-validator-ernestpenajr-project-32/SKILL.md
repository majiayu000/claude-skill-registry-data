---
name: csharp-validator
description: Comprehensive C# code validation, static analysis, and best practices verification for .NET applications. Use when validating C# code, checking SOLID principles, reviewing async/await patterns, verifying nullable reference types usage, checking Entity Framework queries, ensuring security best practices, or reviewing .NET code quality and architecture.
---

# C# Code Validation and Best Practices Skill

## Overview
This skill provides comprehensive C# code validation, static analysis, and best practices verification for .NET applications based on senior developer standards.

## Tools and Validation Methods

### 1. Roslyn Analyzers - Primary Validation Tool

**Installation:**
\`\`\`bash
# Install via NuGet
dotnet add package Microsoft.CodeAnalysis.NetAnalyzers
dotnet add package StyleCop.Analyzers
dotnet add package SonarAnalyzer.CSharp
dotnet add package Roslynator.Analyzers
\`\`\`

### 2. .editorconfig Configuration
Create an \`.editorconfig\` file at project root with naming conventions, code style rules, and formatting standards.

### 3. Code Analysis Configuration
Enable all analyzers in \`Directory.Build.props\`:

\`\`\`xml
<PropertyGroup>
  <AnalysisMode>All</AnalysisMode>
  <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
  <Nullable>enable</Nullable>
  <TreatWarningsAsErrors Condition="'$(Configuration)' == 'Release'">true</TreatWarningsAsErrors>
</PropertyGroup>
\`\`\`

## Senior Developer Standards

### 1. SOLID Principles

#### Single Responsibility Principle

✅ **Good:**
\`\`\`csharp
public class UserService
{
    private readonly IUserRepository _repository;
    private readonly IUserValidator _validator;
    private readonly INotificationService _notificationService;

    public async Task<Result<User>> CreateUserAsync(User user, CancellationToken cancellationToken = default)
    {
        var validationResult = await _validator.ValidateAsync(user, cancellationToken);
        if (!validationResult.IsValid)
            return Result<User>.Failure(validationResult.Errors);

        var createdUser = await _repository.AddAsync(user, cancellationToken);
        await _notificationService.SendWelcomeEmailAsync(createdUser.Email, cancellationToken);
        
        return Result<User>.Success(createdUser);
    }
}
\`\`\`

### 2. Nullable Reference Types

Always enable and properly use nullable reference types:

\`\`\`csharp
public class UserService
{
    private readonly ILogger<UserService> _logger;  // Non-nullable
    private string? _cachedUserName;  // Nullable

    public async Task<User?> GetUserAsync(int? userId)
    {
        if (userId is null)
            return null;
        return await _repository.GetByIdAsync(userId.Value);
    }
}
\`\`\`

### 3. Async/Await Best Practices

- Always use Async suffix for async methods
- Always pass CancellationToken
- Avoid async void except for event handlers
- Use ConfigureAwait(false) in library code

### 4. Entity Framework Core

- Use AsNoTracking for read-only queries
- Avoid N+1 query problems with Include
- Use projections to limit data

## Validation Process

When validating C# code:

1. **Check for analyzer packages** in the project
2. **Run dotnet build** with TreatWarningsAsErrors
3. **Review for SOLID violations** especially SRP and DIP
4. **Verify nullable reference types** are enabled and used correctly
5. **Check async/await patterns** including CancellationToken usage
6. **Look for security issues** like SQL injection, missing validation
7. **Verify exception handling** is appropriate
8. **Check for performance issues** like N+1 queries
9. **Ensure proper DI usage** and avoid service locator pattern
10. **Validate test coverage** and quality

## Manual Review Checklist

1. **Architecture & Design**
   - [ ] SOLID principles followed
   - [ ] Proper separation of concerns
   - [ ] Dependency injection used correctly

2. **Code Quality**
   - [ ] Meaningful variable and method names
   - [ ] Methods under 50 lines
   - [ ] No code duplication (DRY)

3. **Async/Await**
   - [ ] All async methods have Async suffix
   - [ ] CancellationToken passed through
   - [ ] No async void (except event handlers)
   - [ ] No blocking calls (.Result, .Wait())

4. **Null Safety**
   - [ ] Nullable reference types enabled
   - [ ] Proper null checking
   - [ ] ArgumentNullException for public APIs

5. **Security**
   - [ ] Input validation on all public methods
   - [ ] Parameterized queries only
   - [ ] Sensitive data protected

6. **Testing**
   - [ ] Unit tests for business logic (80%+ coverage)
   - [ ] Tests follow AAA pattern
   - [ ] Edge cases covered

---
name: csharp-cleanup
description: Modernize async patterns, optimize LINQ usage, update .NET APIs, and clean up C# codebases. Use when cleaning up C# projects, removing unused using.
---

# C# Code Cleanup

Systematically identify and remove dead code, update deprecated APIs, and apply modern C# patterns to maintain a clean, maintainable codebase.

## When to Use This Skill

Use this skill when you need to:

- Remove unused using directives and dead code
- Update deprecated .NET API usage
- Apply modern C# features (6.0+)
- Fix ReSharper/Rider warnings
- Modernize async/await patterns
- Optimize LINQ usage
- Clean up before code review

**Trigger phrases**: "cleanup C#", "remove dead code C#", "modernize C#", "fix ReSharper", ".NET refactor", "cleanup dotnet"

## What This Skill Does

### Cleanup Areas

1. **Dead Code Removal**
   - Unused using directives
   - Unused private methods and fields
   - Unreachable code
   - Redundant code

2. **Style Compliance**
   - ReSharper/Rider warnings
   - StyleCop rules
   - Naming conventions

3. **Modernization**
   - Nullable reference types
   - Pattern matching
   - Records
   - File-scoped namespaces

## Instructions

### Step 1: Run Analysis Tools

```bash
# Build and check for warnings
dotnet build

# Run code analysis
dotnet format --verify-no-changes

# Check for nullable warnings
dotnet build /warnaserror:nullable
```

### Step 2: Identify Dead Code

```csharp
// Unused using directives
// Remove any using statements not referenced

// Unused private members
// Remove private fields, properties, methods that are never accessed

// Unreachable code
// Remove code after return statements or in impossible branches
```

### Step 3: Modernize Patterns

#### Null-Conditional and Null-Coalescing (C# 6+)

```csharp
// Before
string name = user != null ? user.Name : "Unknown";
// After
string name = user?.Name ?? "Unknown";

// Before
if (handler != null)
{
    handler(this, args);
}
// After
handler?.Invoke(this, args);

// Null-coalescing assignment (C# 8+)
// Before
if (list == null)
{
    list = new List<string>();
}
// After
list ??= new List<string>();
```

#### String Interpolation (C# 6+)

```csharp
// Before
string message = string.Format("Hello, {0}! You have {1} messages.", name, count);
// After
string message = $"Hello, {name}! You have {count} messages.";

// Raw string literals (C# 11+)
string json = """
    {
        "name": "John",
        "age": 30
    }
    """;
```

#### Expression-Bodied Members (C# 6+)

```csharp
// Before
public string FullName
{
    get { return $"{FirstName} {LastName}"; }
}
// After
public string FullName => $"{FirstName} {LastName}";

// Before
public override string ToString()
{
    return $"{Name}: {Value}";
}
// After
public override string ToString() => $"{Name}: {Value}";
```

#### Pattern Matching (C# 7+)

```csharp
// Before
if (obj is string)
{
    string s = (string)obj;
    Console.WriteLine(s.Length);
}
// After
if (obj is string s)
{
    Console.WriteLine(s.Length);
}

// Switch expressions (C# 8+)
// Before
string GetDescription(Status status)
{
    switch (status)
    {
        case Status.Active: return "Active";
        case Status.Inactive: return "Inactive";
        case Status.Pending: return "Pending";
        default: return "Unknown";
    }
}
// After
string GetDescription(Status status) => status switch
{
    Status.Active => "Active",
    Status.Inactive => "Inactive",
    Status.Pending => "Pending",
    _ => "Unknown"
};

// Property patterns (C# 8+)
if (person is { Age: >= 18, Name: not null })
{
    // Adult with name
}
```

#### Records (C# 9+)

```csharp
// Before
public class User
{
    public string Name { get; init; }
    public string Email { get; init; }

    public User(string name, string email)
    {
        Name = name;
        Email = email;
    }

    // Plus Equals, GetHashCode, ToString...
}
// After
public record User(string Name, string Email);

// Record with additional members
public record User(string Name, string Email)
{
    public string DisplayName => $"{Name} <{Email}>";
}
```

#### File-Scoped Namespaces (C# 10+)

```csharp
// Before
namespace MyApp.Services
{
    public class UserService
    {
        // ...
    }
}
// After
namespace MyApp.Services;

public class UserService
{
    // ...
}
```

#### Global Using Directives (C# 10+)

```csharp
// GlobalUsings.cs
global using System;
global using System.Collections.Generic;
global using System.Linq;
global using System.Threading.Tasks;
global using Microsoft.Extensions.Logging;
```

#### Required Members (C# 11+)

```csharp
// Before
public class User
{
    public User(string name, string email)
    {
        Name = name;
        Email = email;
    }

    public string Name { get; set; }
    public string Email { get; set; }
}
// After
public class User
{
    public required string Name { get; init; }
    public required string Email { get; init; }
}
```

### Step 4: Optimize LINQ

```csharp
// Avoid multiple enumerations
// Before
if (items.Count() > 0)
{
    var first = items.First();
}
// After
var itemList = items.ToList();
if (itemList.Count > 0)
{
    var first = itemList[0];
}

// Use Any() instead of Count() > 0
// Before
if (items.Count() > 0)
// After
if (items.Any())

// Use FirstOrDefault instead of Where().FirstOrDefault()
// Before
items.Where(x => x.Id == id).FirstOrDefault()
// After
items.FirstOrDefault(x => x.Id == id)

// Use method syntax for complex queries
// Before
(from u in users
 where u.IsActive
 select u.Name).ToList()
// After
users.Where(u => u.IsActive).Select(u => u.Name).ToList()
```

### Step 5: Async/Await Best Practices

```csharp
// Use ConfigureAwait(false) in library code
// Before
var result = await GetDataAsync();
// After (library code)
var result = await GetDataAsync().ConfigureAwait(false);

// Avoid async void (except event handlers)
// Before
public async void ProcessData()
// After
public async Task ProcessDataAsync()

// Use Task.WhenAll for parallel operations
// Before
var result1 = await GetData1Async();
var result2 = await GetData2Async();
// After
var results = await Task.WhenAll(GetData1Async(), GetData2Async());

// Use CancellationToken
public async Task<Data> GetDataAsync(CancellationToken cancellationToken = default)
{
    return await _client.GetAsync(url, cancellationToken);
}

// Avoid .Result and .Wait() - use async all the way
// Before
var result = GetDataAsync().Result;
// After
var result = await GetDataAsync();
```

### Step 6: Clean Up Dependencies

```bash
# Remove unused NuGet packages
dotnet list package

# Check for outdated packages
dotnet list package --outdated

# Remove unused project references
dotnet list reference
```

## Tools

- **Visual Studio/Rider**: Built-in code analysis
- **ReSharper**: Advanced code inspection
- **StyleCop**: Style checking
- **Roslynator**: Additional analyzers
- **SonarLint**: Quality analysis

## Quality Checklist

- [ ] Unused using directives removed
- [ ] Unused private members removed
- [ ] Deprecated APIs updated
- [ ] Modern C# patterns applied
- [ ] Nullable reference types enabled/addressed
- [ ] LINQ optimized
- [ ] Async patterns correct
- [ ] Build succeeds without warnings
- [ ] Tests still pass

## Common Issues and Solutions

### Issue: Nullable reference type warnings
**Solution**: Enable nullable context and add appropriate null checks or annotations:
```csharp
#nullable enable
public string? NullableName { get; set; }
public string NonNullName { get; set; } = string.Empty;
```

### Issue: Async void methods
**Solution**: Change to async Task and ensure callers await:
```csharp
// Before
public async void OnButtonClick() { ... }
// After
public async Task OnButtonClickAsync() { ... }
```

### Issue: Multiple LINQ enumerations
**Solution**: Materialize the collection once:
```csharp
var list = query.ToList();
if (list.Any())
{
    ProcessItems(list);
}
```

## Related Skills

- `code-review-quality` - Code quality assessment
- `security-review` - Security analysis

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates code_cleanup/csharp_cleanup.md


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.

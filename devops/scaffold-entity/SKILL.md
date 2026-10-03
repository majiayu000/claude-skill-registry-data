---
name: scaffold-entity
description: Scaffold a new entity with AuditableEntity base, status enum, DbSet, UnitOfWork update, and EF Core migration
argument-hint: [ServiceName EntityName]
allowed-tools: Bash, Write, Read, Edit
---

# Scaffold Entity `$ARGUMENTS`

Usage: `/scaffold-entity ServiceName EntityName`  
Example: `/scaffold-entity BatteryService Battery`

## Step 1 — Entity: `Domain/Entities/{Entity}.cs`

```csharp
namespace {Service}.Domain.Entities;

public class {Entity} : AuditableEntity
{
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
    public {Entity}StatusEnum Status { get; set; } = {Entity}StatusEnum.Active;

    // Nullable FK for optional relationships
    // public Guid? ParentId { get; set; }
    // public ParentEntity? Parent { get; set; }
    // public ICollection<ChildEntity> Children { get; set; } = new List<ChildEntity>();
}
```

## Step 2 — Enum: `Domain/Enums/{Entity}StatusEnum.cs`

```csharp
namespace {Service}.Domain.Enums;

public enum {Entity}StatusEnum
{
    Active = 1,      // BẮT ĐẦU TỪ 1, KHÔNG phải 0
    Inactive = 2,
    // Thêm values theo nghiệp vụ
}
```

## Step 3 — Update DbContext: `Infrastructure/Persistence/ApplicationDbContext.cs`

```csharp
public DbSet<{Entity}> {Entity}s { get; set; }
```

## Step 4 — Update UoW Interface: `Application/Interfaces/I{Service}UnitOfWork.cs`

```csharp
IGenericRepository<{Entity}> {Entity}s { get; }
```

## Step 5 — Update UoW Impl: `Infrastructure/Implements/UnitOfWork.cs`

```csharp
// Constructor
{Entity}s = new GenericRepository<{Entity}>(_context);

// Property
public IGenericRepository<{Entity}> {Entity}s { get; }
```

## Step 6 — Run Migration

```bash
cd services/{Service}/src/{Service}.Api
dotnet ef migrations add Add{Entity} -p ../{Service}.Infrastructure -s .
```

## Checklist
- [ ] Extends AuditableEntity
- [ ] Enum values start from 1
- [ ] DbSet added to ApplicationDbContext
- [ ] Repository added to IUnitOfWork interface + initialized in constructor
- [ ] Migration created

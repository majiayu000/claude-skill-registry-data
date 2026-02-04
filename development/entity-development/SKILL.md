---
name: entity-development
description: Use when creating or modifying domain entities with static expressions, computed properties, field tracking, and validation methods.
---

# Entity Development Workflow

## When to Use This Skill

- Creating new domain entities
- Adding computed properties to entities
- Creating static expression methods (filtering, queries)
- Implementing entity validation
- Setting up field change tracking

## Pre-Flight Checklist

- [ ] Identify the correct service/domain
- [ ] Check for similar entities: `grep "class {EntityName}" --include="*.cs"`
- [ ] Identify if audited or non-audited entity needed
- [ ] Check existing expression patterns in domain

## File Location

```
{Service}.Domain/
└── Entities/
    └── {EntityName}.cs
```

## Entity Type Decision

### Non-Audited Entity (Basic)

```csharp
public class Employee : RootEntity<Employee, string>
{
    // No CreatedBy, UpdatedBy, CreatedDate, etc.
}
```

### Audited Entity (With Audit Trail)

```csharp
public class AuditedEmployee : RootAuditedEntity<AuditedEmployee, string, string>
{
    // Includes: CreatedBy, UpdatedBy, CreatedDate, UpdatedDate
}
```

## Implementation Pattern

### Basic Entity Structure

```csharp
[TrackFieldUpdatedDomainEvent]  // Optional: Track all field changes
public sealed class Entity : RootEntity<Entity, string>
{
    // ═══════════════════════════════════════════════════════════════════════════
    // CORE PROPERTIES
    // ═══════════════════════════════════════════════════════════════════════════

    [TrackFieldUpdatedDomainEvent]  // Track specific field changes
    public string Name { get; set; } = "";

    public string Code { get; set; } = "";
    public string CompanyId { get; set; } = "";
    public EntityStatus Status { get; set; }
    public DateTime? EffectiveDate { get; set; }

    // ═══════════════════════════════════════════════════════════════════════════
    // NAVIGATION PROPERTIES
    // ═══════════════════════════════════════════════════════════════════════════

    [JsonIgnore]
    public Company? Company { get; set; }

    [JsonIgnore]
    public List<EntityChild>? Children { get; set; }

    // ═══════════════════════════════════════════════════════════════════════════
    // COMPUTED PROPERTIES (MUST have empty set { })
    // ═══════════════════════════════════════════════════════════════════════════

    [ComputedEntityProperty]
    public bool IsActive
    {
        get => Status == EntityStatus.Active && !IsDeleted;
        set { }  // Required empty setter for EF Core
    }

    [ComputedEntityProperty]
    public string DisplayName
    {
        get => $"{Code} - {Name}".Trim();
        set { }  // Required empty setter
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // STATIC EXPRESSIONS (For Repository Queries)
    // ═══════════════════════════════════════════════════════════════════════════

    // Simple filter expression
    public static Expression<Func<Entity, bool>> OfCompanyExpr(string companyId)
        => e => e.CompanyId == companyId;

    // Unique constraint expression
    public static Expression<Func<Entity, bool>> UniqueExpr(string companyId, string code)
        => e => e.CompanyId == companyId && e.Code == code;

    // Filter by status list
    public static Expression<Func<Entity, bool>> FilterByStatusExpr(List<EntityStatus> statuses)
    {
        var statusSet = statuses.ToHashSet();
        return e => e.Status.HasValue && statusSet.Contains(e.Status.Value);
    }

    // Composite expression with conditional
    public static Expression<Func<Entity, bool>> ActiveInCompanyExpr(string companyId, bool includeInactive = false)
        => OfCompanyExpr(companyId).AndAlsoIf(!includeInactive, () => e => e.IsActive);

    // Full-text search columns
    public static Expression<Func<Entity, object?>>[] DefaultFullTextSearchColumns()
        => [e => e.Name, e => e.Code, e => e.Description];

    // ═══════════════════════════════════════════════════════════════════════════
    // ASYNC EXPRESSIONS (When External Dependencies Needed)
    // ═══════════════════════════════════════════════════════════════════════════

    public static async Task<Expression<Func<Entity, bool>>> FilterWithLicenseExprAsync(
        IRepository<License> licenseRepo,
        string companyId,
        CancellationToken ct = default)
    {
        var hasLicense = await licenseRepo.HasLicenseAsync(companyId, ct);
        return hasLicense ? PremiumFilterExpr() : StandardFilterExpr();
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // VALIDATION METHODS
    // ═══════════════════════════════════════════════════════════════════════════
    // Naming Convention:
    // - Validate[Context]() → Returns PlatformValidationResult, never throws
    // - Ensure[Context]Valid() → Returns void/T, throws PlatformValidationException
    // - At call site: Use Validate...().EnsureValid() instead of wrapper Ensure methods

    public PlatformValidationResult ValidateCanBeUpdated()
    {
        return PlatformValidationResult.Valid()
            .And(() => !IsDeleted, "Entity is deleted")
            .And(() => Status != EntityStatus.Locked, "Entity is locked");
    }

    public async Task<PlatformValidationResult> ValidateAsync(
        IRepository<Entity> repository,
        CancellationToken ct = default)
    {
        return await PlatformValidationResult.Valid()
            .And(() => Name.IsNotNullOrEmpty(), "Name is required")
            .And(() => Code.IsNotNullOrEmpty(), "Code is required")
            .AndNotAsync(async () => await repository.AnyAsync(
                e => e.Id != Id && e.CompanyId == CompanyId && e.Code == Code, ct),
                "Code already exists");
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // INSTANCE METHODS
    // ═══════════════════════════════════════════════════════════════════════════

    public void Activate() => Status = EntityStatus.Active;
    public void Deactivate() => Status = EntityStatus.Inactive;
    public void Reset() { /* reset logic */ }
}
```

## Expression Composition Patterns

| Pattern     | Usage                            | Example                             |
| ----------- | -------------------------------- | ----------------------------------- |
| `AndAlso`   | Combine two expressions with AND | `expr1.AndAlso(expr2)`              |
| `OrElse`    | Combine two expressions with OR  | `expr1.OrElse(expr2)`               |
| `AndAlsoIf` | Conditional AND                  | `.AndAlsoIf(condition, () => expr)` |
| `OrElseIf`  | Conditional OR                   | `.OrElseIf(condition, () => expr)`  |

```csharp
// Composing multiple expressions
var expr = Entity.OfCompanyExpr(companyId)
    .AndAlso(Entity.FilterByStatusExpr(statuses))
    .AndAlsoIf(deptIds.Any(), () => Entity.FilterByDeptExpr(deptIds))
    .AndAlsoIf(searchText.IsNotNullOrEmpty(), () => Entity.SearchExpr(searchText));
```

## Computed Property Rules

:white_check_mark: **MUST have empty setter `set { }`**

```csharp
[ComputedEntityProperty]
public bool IsRoot
{
    get => Id == RootId;
    set { }  // Required for EF Core mapping
}
```

:x: **Wrong - No setter**

```csharp
[ComputedEntityProperty]
public bool IsRoot => Id == RootId;  // Will cause EF Core issues
```

## Anti-Patterns to AVOID

:x: **Business logic in properties**

```csharp
// WRONG - calling services in property
public bool IsValid => validationService.Validate(this);
```

:x: **Missing [JsonIgnore] on navigation**

```csharp
// WRONG - circular reference issues
public Company Company { get; set; }
```

:x: **Complex logic in getters**

```csharp
// WRONG - should be a method
public List<Item> ActiveItems => Items.Where(x => x.IsActive).ToList();
```

## Verification Checklist

- [ ] Entity inherits from correct base class (RootEntity or RootAuditedEntity)
- [ ] Computed properties have `[ComputedEntityProperty]` and empty `set { }`
- [ ] Navigation properties have `[JsonIgnore]`
- [ ] Static expressions follow naming convention: `{Purpose}Expr`
- [ ] Full-text search columns defined if searchable
- [ ] Validation methods return `PlatformValidationResult`
- [ ] `[TrackFieldUpdatedDomainEvent]` on tracked fields

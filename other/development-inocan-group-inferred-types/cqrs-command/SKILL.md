---
name: cqrs-command
description: Use when creating or modifying a CQRS Command (Save, Create, Update, Delete) or command handler in .NET backend.
---

# CQRS Command Development Workflow

## Pre-Flight Checklist

- [ ] Search for similar commands: `grep "Command.*{EntityName}" --include="*.cs"`
- [ ] Identify correct folder: `{Service}.Application/UseCaseCommands/{Feature}/`
- [ ] Check if entity DTO exists: `grep "class {EntityName}Dto" --include="*.cs"`
- [ ] Identify service-specific repository: `I{Service}RootRepository<{Entity}>`

## File Organization Rule (CRITICAL)

**Command + Handler + Result = ONE FILE**

```
{Service}.Application/
└── UseCaseCommands/
    └── {Feature}/
        └── Save{Entity}Command.cs  ← Contains all 3 classes
```

## Implementation Steps

### Step 1: Create Command Class

```csharp
public sealed class Save{Entity}Command : PlatformCqrsCommand<Save{Entity}CommandResult>
{
    public string? Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public List<IFormFile> Files { get; set; } = [];

    public override PlatformValidationResult<IPlatformCqrsRequest> Validate()
    {
        return base.Validate()
            .And(_ => Name.IsNotNullOrEmpty(), "Name is required")
            .And(_ => FromDate <= ToDate, "Invalid date range");
    }
}
```

### Step 2: Create Result Class (same file)

```csharp
public sealed class Save{Entity}CommandResult : PlatformCqrsCommandResult
{
    public {Entity}Dto Entity { get; set; } = null!;
}
```

### Step 3: Create Handler (same file)

```csharp
internal sealed class Save{Entity}CommandHandler :
    PlatformCqrsCommandApplicationHandler<Save{Entity}Command, Save{Entity}CommandResult>
{
    private readonly I{Service}RootRepository<{Entity}> repository;

    public Save{Entity}CommandHandler(
        ILoggerFactory loggerFactory,
        IPlatformUnitOfWorkManager unitOfWorkManager,
        IServiceProvider serviceProvider,
        IPlatformRootServiceProvider rootServiceProvider,
        I{Service}RootRepository<{Entity}> repository)
        : base(loggerFactory, unitOfWorkManager, serviceProvider, rootServiceProvider)
    {
        this.repository = repository;
    }

    // Optional: Async validation
    protected override async Task<PlatformValidationResult<Save{Entity}Command>> ValidateRequestAsync(
        PlatformValidationResult<Save{Entity}Command> validation, CancellationToken ct)
    {
        return await validation
            .AndAsync(req => repository.GetByIdsAsync(req.RelatedIds, ct)
                .ThenValidateFoundAllAsync(req.RelatedIds, ids => $"Not found: {ids}"));
    }

    protected override async Task<Save{Entity}CommandResult> HandleAsync(
        Save{Entity}Command req, CancellationToken ct)
    {
        // 1. Get or create entity
        var entity = req.Id.IsNullOrEmpty()
            ? req.MapToNewEntity().With(e => e.CreatedBy = RequestContext.UserId())
            : await repository.GetByIdAsync(req.Id, ct)
                .EnsureFound($"Entity not found: {req.Id}")
                .Then(e => req.UpdateEntity(e));

        // 2. Validate entity
        await entity.ValidateAsync(repository, ct).EnsureValidAsync();

        // 3. Save (parallel with file upload if needed)
        var (saved, _) = await (
            repository.CreateOrUpdateAsync(entity, ct),
            req.Files.ParallelAsync(f => fileService.UploadAsync(f, ct))
        );

        return new Save{Entity}CommandResult { Entity = new {Entity}Dto(saved) };
    }
}
```

## Validation Patterns

**Validation Method Naming Conventions:**

| Pattern                  | Return Type                   | Behavior                                        |
| ------------------------ | ----------------------------- | ----------------------------------------------- |
| `Validate[Context]()`    | `PlatformValidationResult<T>` | Never throws, returns validation result         |
| `Ensure[Context]Valid()` | `void` or `T`                 | Throws `PlatformValidationException` if invalid |

- Methods that start with `Validate` should return a validation result, not throw
- Methods that start with `Ensure` are allowed to throw exceptions
- At call site: Use `Validate...().EnsureValid()` instead of creating wrapper `Ensure...` methods

### Sync Validation (in Command class)

```csharp
public override PlatformValidationResult<IPlatformCqrsRequest> Validate()
{
    return base.Validate()
        .And(_ => Name.IsNotNullOrEmpty(), "Name required")
        .And(_ => StartDate <= EndDate, "Invalid range")
        .Of<IPlatformCqrsRequest>();
}
```

### Async Validation (in Handler)

```csharp
protected override async Task<PlatformValidationResult<T>> ValidateRequestAsync(...)
{
    return await validation
        .AndAsync(req => repo.AnyAsync(e => e.Code == req.Code, ct), "Code exists")
        .AndNotAsync(req => repo.AnyAsync(e => e.IsLocked, ct), "Entity locked");
}
```

## Anti-Patterns to AVOID

- :x: Calling side effects directly (notifications, external APIs)
- :x: Creating separate files for Command/Handler/Result
- :x: Mapping DTO→Entity in handler (use DTO's `MapToEntity()` method)
- :x: Using generic `IPlatformRootRepository<>` instead of service-specific
- :x: Catching exceptions in handler (let platform handle errors)

## Side Effects Rule

**NEVER call side effects in command handlers!**

If command needs notifications/emails, create Entity Event Handler:

```
UseCaseEvents/{Feature}/Send{Action}On{Event}{Entity}EntityEventHandler.cs
```

Platform automatically raises `PlatformCqrsEntityEvent` on repository CRUD.

## Verification Checklist

- [ ] File contains Command + Result + Handler in ONE file
- [ ] Uses service-specific repository (`I{Service}RootRepository<T>`)
- [ ] Validation uses fluent API (`.And()`, `.AndAsync()`)
- [ ] No direct side effect calls in handler
- [ ] DTO mapping in DTO class, not handler
- [ ] Uses `RequestContext.UserId()` for audit fields

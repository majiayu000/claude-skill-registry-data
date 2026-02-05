---
name: cqrs-ddd
description: CQRS+DDD implementation patterns for .NET. Use when designing aggregates, implementing command/query handlers, setting up repositories, or understanding architectural principles. Triggers on "CQRS", "DDD", "aggregate", "command handler", "query handler", "repository", "value object", "domain event", "entity configuration".
---

# CQRS+DDD Implementation Patterns

Comprehensive guide for implementing CQRS+DDD architecture in this .NET/EF Core codebase.

## Quick Reference

### Layer Dependencies

```
┌─────────────────┐
│   Api Layer     │  Controllers, Middleware
└────────┬────────┘
         │ depends on
         ▼
┌─────────────────┐
│Application Layer│  Commands, Queries, Handlers
└────────┬────────┘
         │ depends on
         ▼
┌─────────────────┐
│  Domain Layer   │◄──┐  Entities, Value Objects
└─────────────────┘   │
         ▲             │
         │ implements  │
┌────────┴────────┐   │
│Infrastructure   │───┘  Repositories, DbContext
└─────────────────┘
```

### CQRS Separation

| Command (Write) | Query (Read) |
| --------------- | ------------ |
| Via Aggregate Root | Direct DB query |
| Transaction required | AsNoTracking() |
| Business rules apply | Performance priority |

### Domain Layer Patterns

```csharp
// Entity Base
public abstract class Entity<TId> where TId : notnull
{
    public TId Id { get; protected set; }
}

// Aggregate Root
public abstract class AggregateRoot<TId> : Entity<TId>
{
    private readonly List<DomainEvent> _domainEvents = new();
    protected void AddDomainEvent(DomainEvent e) => _domainEvents.Add(e);
}

// Value Object (C# record)
public record StudentId(Guid Value);
```

### Application Layer Patterns

```csharp
// Command Handler
public class CreateCourseCommandHandler : IRequestHandler<CreateCourseCommand, string>
{
    public async Task<string> Handle(CreateCourseCommand request, CancellationToken ct)
    {
        var course = Course.Create(new CourseCode(request.Code), request.Name);
        await _repository.AddAsync(course, ct);
        await _repository.SaveChangesAsync(ct);
        return course.Id.Value;
    }
}

// Query Handler
public class GetCoursesQueryHandler : IRequestHandler<GetCoursesQuery, List<CourseDto>>
{
    public async Task<List<CourseDto>> Handle(GetCoursesQuery request, CancellationToken ct)
    {
        return await _context.Courses
            .AsNoTracking()
            .Select(c => new CourseDto { ... })
            .ToListAsync(ct);
    }
}
```

### Infrastructure Layer Patterns

```csharp
// Entity Configuration
public class EnrollmentConfiguration : IEntityTypeConfiguration<Enrollment>
{
    public void Configure(EntityTypeBuilder<Enrollment> builder)
    {
        builder.Property(e => e.Id)
            .HasConversion(v => v.Value, v => new EnrollmentId(v));
        builder.OwnsOne(e => e.Semester);
        builder.Ignore(e => e.DomainEvents);
    }
}
```

## Key Rules

| Rule | Description |
| ---- | ----------- |
| 1 Aggregate = 1 Transaction | No cross-aggregate changes in same transaction |
| ID References Only | Reference other aggregates by ID, not entity |
| 1 Repository per Aggregate | One repository per aggregate root |
| Validation in Domain | Value objects validate on construction |
| No FluentValidation | Use aggregate/value object validation |

## New Aggregate Checklist

| Step | Action | File/Location |
| ---- | ------ | ------------- |
| 1 | Create Flyway migration | `Migrations/V{n}__*.sql` |
| 2 | Add DbSet to DbContext | `*DbContext.cs` |
| 3 | Create EntityConfiguration | `Configurations/*Configuration.cs` |
| 4 | Implement Repository | `Repositories/*Repository.cs` |
| 5 | Register DI | `Program.cs` |

## Resources

| File | Content |
| ---- | ------- |
| [architecture.md](references/architecture.md) | Architectural principles, bounded contexts |
| [domain-layer.md](references/domain-layer.md) | Entity, Aggregate, Value Object patterns |
| [application-layer.md](references/application-layer.md) | CQRS handlers, validation, transactions |
| [infrastructure-layer.md](references/infrastructure-layer.md) | EF Core, repositories, migrations |

## Related Skills

- [testing-strategy](../testing-strategy/SKILL.md) - Handler testing patterns
- [slow-query-detector](../slow-query-detector/SKILL.md) - N+1 and performance issues

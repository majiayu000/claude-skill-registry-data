---
name: backend-feature
description: Scaffolds backend features including new domain entities, new properties on existing entities, and new business operations. Use when creating a new domain entity, extending an existing entity with new properties, or adding new business features/commands.
allowed-tools: Read, Glob, Grep, Write, Edit, Bash(dotnet:*, ls:*, mkdir:*)
---

# Backend Feature Scaffolding

This skill handles three scenarios:
1. **New Entity** - Create a complete vertical slice for a new domain entity
2. **New Property** - Add properties to an existing entity
3. **New Feature** - Add business operations (commands/queries) to an existing entity

## Scenario 1: New Entity

For a new entity named `[EntityName]` (e.g., `Customer`, `Order`, `Product`), this skill generates:

```
Domain/
└── [EntityName]s/
    ├── [EntityName].cs                 # Rich domain entity
    ├── DomainEvents/
    │   ├── [EntityName]Created.cs
    │   ├── [EntityName]Updated.cs
    │   └── [EntityName]Deleted.cs
    ├── Dtos/
    │   ├── [EntityName]Dto.cs
    │   ├── [EntityName]ForCreationDto.cs
    │   ├── [EntityName]ForUpdateDto.cs
    │   └── [EntityName]ParametersDto.cs
    ├── Features/
    │   ├── Add[EntityName].cs
    │   ├── Update[EntityName].cs
    │   ├── Delete[EntityName].cs
    │   ├── Get[EntityName].cs
    │   └── Get[EntityName]List.cs
    ├── Mappings/
    │   └── [EntityName]Mapper.cs
    └── Models/
        ├── [EntityName]ForCreation.cs
        └── [EntityName]ForUpdate.cs

Databases/
└── EntityConfigurations/
    └── [EntityName]Configuration.cs    # EF Core entity configuration

Controllers/
└── v1/
    └── [EntityName]sController.cs
```

## Scenario 2: New Property on Existing Entity

When adding properties to an existing entity, update these files:

| File | Changes |
|------|---------|
| `[EntityName].cs` | Add property with private setter |
| `[EntityName]ForCreation.cs` | Add property if set at creation |
| `[EntityName]ForUpdate.cs` | Add property if updatable |
| `[EntityName]ForCreationDto.cs` | Add property if set at creation |
| `[EntityName]ForUpdateDto.cs` | Add property if updatable |
| `[EntityName]Dto.cs` | Add property for response |
| `[EntityName]Mapper.cs` | Add custom mapping if value object |
| `[EntityName]Configuration.cs` | Configure property constraints, value objects |

## Scenario 3: New Feature on Existing Entity

When adding a business operation to an existing entity:

| Component | Files to Create/Modify |
|-----------|----------------------|
| **Domain method** | `[EntityName].cs` - Add behavior method |
| **Domain event** | `DomainEvents/[EntityName][Action].cs` - New event |
| **Feature** | `Features/[Action][EntityName].cs` - New command/query |
| **Controller** | `[EntityName]sController.cs` - Add endpoint |
| **DTOs** (if needed) | `Dtos/[Action][EntityName]Dto.cs` - Request/response |

---

## Usage Examples

### New Entity
```
Create a backend feature for managing Products with name, price, and category
```

### New Property on Existing Entity
```
Add an email property to the Customer entity
```
```
Add a status property with Draft, Active, and Archived states to the Product entity
```

### New Feature on Existing Entity
```
Add a Submit feature to the Order entity that changes status and validates requirements
```
```
Add a GetOrdersByCustomer query that returns orders for a specific customer
```

---

## Process: New Entity

1. **Gather Requirements**
   - Entity name (PascalCase, singular: `Customer`, `Order`, `Product`)
   - Properties and their types
   - Any special business rules or value objects needed

2. **Generate Domain Entity**
   - Create rich domain entity following DDD principles
   - Private setters, factory methods, encapsulated behavior
   - Value objects for complex concepts
   - See: `.claude/rules/backend/working-with-domain-entities.md`

3. **Generate Domain Events**
   - Created, Updated, Deleted events
   - Additional business-specific events as needed
   - See: `.claude/rules/backend/domain-events.md`

4. **Generate DTOs and Models**
   - Read DTO for responses
   - Creation/Update DTOs for requests
   - Parameters DTO for list queries
   - Internal models for domain method contracts
   - See: `.claude/rules/backend/dtos-and-mappings.md`

5. **Generate Mapperly Mapper**
   - Entity to DTO mappings
   - DTO to internal model mappings
   - IQueryable projection support
   - See: `.claude/rules/backend/dtos-and-mappings.md`

6. **Generate CQRS Features**
   - Add, Update, Delete commands
   - Get single and Get list queries
   - MediatR handlers with proper patterns
   - See: `.claude/rules/backend/features-and-cqrs.md`

7. **Generate Controller**
   - Thin controller delegating to MediatR
   - Proper API versioning
   - OpenAPI documentation
   - See: `.claude/rules/backend/controllers.md`

8. **Generate Entity Configuration**
   - Create `IEntityTypeConfiguration<T>` class
   - Configure property constraints and indexes
   - Configure value object mappings with `OwnsOne`
   - See: `.claude/rules/backend/entity-configurations.md`

9. **Update Infrastructure**
   - Add DbSet to AppDbContext
   - Ensure `ApplyConfigurationsFromAssembly` is called in OnModelCreating

---

## Process: New Property

1. **Read Existing Entity**
   - Understand current entity structure and patterns
   - Identify if property is a simple type or value object

2. **Add Property to Domain Entity**
   ```csharp
   // Simple property
   public string PhoneNumber { get; private set; }

   // Value object property
   public EmailAddress Email { get; private set; } = default!;
   ```

3. **Update Factory Method (if set at creation)**
   ```csharp
   public static Customer Create(CustomerForCreation forCreation)
   {
       var entity = new Customer
       {
           // ... existing properties
           PhoneNumber = forCreation.PhoneNumber,  // Add new property
       };
       // ...
   }
   ```

4. **Update Update Method (if updatable)**
   ```csharp
   public Customer Update(CustomerForUpdate forUpdate)
   {
       // ... existing updates
       PhoneNumber = forUpdate.PhoneNumber;  // Add new property
       // ...
   }
   ```

5. **Update Internal Models**
   - Add to `[EntityName]ForCreation.cs` if set at creation
   - Add to `[EntityName]ForUpdate.cs` if updatable

6. **Update DTOs**
   - Add to `[EntityName]Dto.cs` for responses
   - Add to `[EntityName]ForCreationDto.cs` if set at creation
   - Add to `[EntityName]ForUpdateDto.cs` if updatable

7. **Update Mapper (for value objects)**
   ```csharp
   // Add custom mapping for value objects
   private static string? MapEmail(EmailAddress? email) => email?.Value;
   ```

8. **Update Entity Configuration**
   ```csharp
   // Simple property
   builder.Property(e => e.PhoneNumber).HasMaxLength(20);

   // Value object
   builder.OwnsOne(e => e.Email, email =>
   {
       email.Property(e => e.Value).HasColumnName("email").HasMaxLength(320);
   });
   ```

9. **Create Migration**
   ```bash
   dotnet ef migrations add Add[PropertyName]To[EntityName]
   ```

---

## Process: New Feature

1. **Read Existing Entity**
   - Understand current entity structure
   - Identify what state changes are needed
   - Determine guard conditions

2. **Add Domain Method to Entity**
   ```csharp
   public Order Submit()
   {
       GuardIfNotDraft("Cannot submit");

       Status = OrderStatus.Submitted();

       QueueDomainEvent(new OrderSubmitted
       {
           OrderId = Id,
           SubmittedAt = DateTimeOffset.UtcNow
       });

       return this;
   }
   ```

3. **Create Domain Event (if needed)**
   ```csharp
   // DomainEvents/OrderSubmitted.cs
   public sealed record OrderSubmitted : IDomainEvent
   {
       public required Guid OrderId { get; init; }
       public required DateTimeOffset SubmittedAt { get; init; }
   }
   ```

4. **Create Feature (Command or Query)**
   ```csharp
   // Features/SubmitOrder.cs
   public static class SubmitOrder
   {
       public sealed record Command(Guid Id) : IRequest<OrderDto>;

       public sealed class Handler(AppDbContext dbContext) : IRequestHandler<Command, OrderDto>
       {
           public async Task<OrderDto> Handle(Command request, CancellationToken ct)
           {
               var order = await dbContext.Orders.GetById(request.Id, ct);

               order.Submit();

               await dbContext.SaveChangesAsync(ct);

               return order.ToOrderDto();
           }
       }
   }
   ```

5. **Add Endpoint to Controller**
   ```csharp
   /// <summary>
   /// Submits an order for processing.
   /// </summary>
   [Authorize]
   [HttpPost("{id:guid}/submit", Name = "SubmitOrder")]
   [ProducesResponseType(typeof(OrderDto), StatusCodes.Status200OK)]
   [ProducesResponseType(StatusCodes.Status404NotFound)]
   [ProducesResponseType(StatusCodes.Status400BadRequest)]
   public async Task<ActionResult<OrderDto>> SubmitOrder(Guid id)
   {
       var command = new SubmitOrder.Command(id);
       var result = await mediator.Send(command);
       return Ok(result);
   }
   ```

6. **Create Additional DTOs (if needed)**
   - Request DTO if the action needs input parameters
   - Custom response DTO if different from standard entity DTO

---

## Important Guidelines

### Domain Entity Design
- Use private setters for all properties
- Create static factory method `Create()` for entity creation
- Use `Update()` method for modifications
- Implement guard methods for business rules
- Use value objects for complex domain concepts
- Queue domain events on state changes

### Property Naming
- Entity properties: PascalCase (`FirstName`, `Email`)
- DTO properties: PascalCase with `{ get; init; }`
- Route parameters: camelCase in URLs, PascalCase in code

### Value Objects to Consider
- `EmailAddress` - validated email
- `PhoneNumber` - formatted phone
- `Money` - currency with amount
- `Address` - street, city, state, zip
- Status enums with SmartEnum pattern

### Common Patterns

**Status with Behavior:**
```csharp
public class OrderStatus : ValueObject
{
    private OrderStatusEnum _status;

    public bool IsFinalState() => _status.IsFinalState();
    public bool CanBeCancelled() => !IsFinalState();

    public static OrderStatus Draft() => new("Draft");
    public static OrderStatus Submitted() => new("Submitted");
}
```

**Encapsulated Collections:**
```csharp
private readonly List<LineItem> _lineItems = [];
public IReadOnlyCollection<LineItem> LineItems => _lineItems.AsReadOnly();

public LineItem AddLineItem(Product product, int quantity)
{
    var item = LineItem.Create(product, quantity);
    _lineItems.Add(item);
    return item;
}
```

## Checklists

### New Entity Checklist
- [ ] Review generated entity for business logic completeness
- [ ] Add DbSet to `AppDbContext.cs`
- [ ] Verify entity configuration is in `Databases/EntityConfigurations/` and properly applied
- [ ] Install MediatR if not already present
- [ ] Install Mapperly if not already present
- [ ] Run `dotnet build` to verify compilation
- [ ] Add any needed FluentValidation validators
- [ ] Consider what additional business methods the entity needs
- [ ] Run `dotnet ef migrations add Add[EntityName]` to create migration

### New Property Checklist
- [ ] Property added with private setter in entity
- [ ] Factory method updated (if set at creation)
- [ ] Update method updated (if updatable)
- [ ] Internal models updated (ForCreation/ForUpdate)
- [ ] DTOs updated (Dto, ForCreationDto, ForUpdateDto as needed)
- [ ] Mapper updated (custom mapping for value objects)
- [ ] Entity configuration updated (constraints, value object mapping)
- [ ] Run `dotnet build` to verify compilation
- [ ] Run `dotnet ef migrations add Add[PropertyName]To[EntityName]`

### New Feature Checklist
- [ ] Domain method added to entity with proper guards
- [ ] Domain event created (if state change is significant)
- [ ] Feature file created with Command/Query and Handler
- [ ] Controller endpoint added with proper attributes
- [ ] Additional DTOs created if needed
- [ ] Run `dotnet build` to verify compilation

## Reference Files

The following rules provide detailed patterns:
- `.claude/rules/backend/working-with-domain-entities.md` - Rich domain entities
- `.claude/rules/backend/features-and-cqrs.md` - CQRS with MediatR
- `.claude/rules/backend/dtos-and-mappings.md` - DTOs and Mapperly
- `.claude/rules/backend/controllers.md` - API controllers
- `.claude/rules/backend/domain-events.md` - Domain events
- `.claude/rules/backend/entity-configurations.md` - EF Core entity configurations

---
name: entity
description: Creating or modifying a C# domain Entity class or Enum in any backend microservice (UserService, BatteryService, TicketService, NotificationService). Triggers when adding a new Entity, adding properties to an existing Entity, creating a StatusEnum, adding a DbSet to ApplicationDbContext, or updating UnitOfWork interface/implementation with a new repository.
---

## Nguyên tắc bắt buộc

1. **Tuân thủ tuyệt đối** cấu trúc folder, naming convention, và code pattern được định nghĩa trong skill này — không tự ý thay đổi base class, kiểu PK, hay cấu trúc UnitOfWork.
2. **Hỏi trước khi code** nếu bất kỳ yêu cầu nào chưa rõ (properties của entity, quan hệ với entity khác, enum values cần thiết). Không đoán mò — một câu hỏi ngắn tốt hơn một giờ implement sai hướng.

---

# BE Entity Pattern

## Entity

```csharp
public class Battery : AuditableEntity
{
    public string Name { get; set; } = string.Empty;
    public BatteryStatusEnum Status { get; set; } = BatteryStatusEnum.Active;
    public Guid? LocationId { get; set; }
    public Location? Location { get; set; }
    public ICollection<Ticket> Tickets { get; set; } = new List<Ticket>();
}
```

Rules:
- MUST extend `AuditableEntity` (provides Id, CreatedAt, CreatedBy, UpdatedAt, IsDeleted, DeletedAt)
- PK is `Guid Id` from AuditableEntity — never add int auto-increment
- Enum FK: nullable `Guid? ParentId` + nullable nav `Parent? Parent`
- Collections: init with `new List<T>()`
- Domain layer has ZERO dependency on other layers

## Enum

```csharp
public enum BatteryStatusEnum
{
    Active = 1,
    Inactive = 2,
    Failed = 3,
}
```

Rules:
- Values start from `1`, never `0`
- File: `Domain/Enums/{Entity}StatusEnum.cs`

## DbContext — add DbSet

```csharp
public DbSet<Battery> Batteries { get; set; }
```

## UnitOfWork interface

```csharp
IGenericRepository<Battery> Batteries { get; }
```

## UnitOfWork implementation

```csharp
private IGenericRepository<Battery>? _batteries;
public IGenericRepository<Battery> Batteries =>
    _batteries ??= new GenericRepository<Battery>(_context);
```

## File locations

| File | Path |
|------|------|
| Entity | `Domain/Entities/{Entity}.cs` |
| Enum | `Domain/Enums/{Entity}StatusEnum.cs` |
| DbContext | `Infrastructure/Persistence/ApplicationDbContext.cs` |
| UoW interface | `Application/Interfaces/I{Service}UnitOfWork.cs` |
| UoW implementation | `Infrastructure/Implements/UnitOfWork.cs` |

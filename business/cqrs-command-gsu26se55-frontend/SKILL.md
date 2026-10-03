---
name: cqrs-command
description: Creating a CQRS Command and CommandHandler in any backend microservice. Triggers when implementing Create, Update, Delete, or Restore operations — any action that mutates state. Includes validation via IValidatable, transaction handling with IUnitOfWork, and CommonResponse wrapping.
---

## Nguyên tắc bắt buộc

1. **Tuân thủ tuyệt đối** cấu trúc folder, naming convention, và code pattern được định nghĩa trong skill này — không tự ý thay đổi tên file, tên class, tên method, hay thứ tự layer.
2. **Hỏi trước khi code** nếu bất kỳ yêu cầu nào chưa rõ (scope, field, business rule, relation giữa entities). Không đoán mò — một câu hỏi ngắn tốt hơn một giờ implement sai hướng.

---

# BE CQRS Command Pattern

## Folder structure

```
Application/Commands/{Entity}{Action}/
├── {Entity}{Action}Command.cs
└── {Entity}{Action}CommandHandler.cs
```

## Command with validation

```csharp
public class BatteryCreateCommand : IRequest<BatteryCreateResponse>, IValidatable<BatteryCreateResponse>
{
    public string Name { get; set; }
    public BatteryStatusEnum Status { get; set; }

    public Task<BatteryCreateResponse> ValidateAsync()
    {
        var response = new BatteryCreateResponse();

        if (string.IsNullOrEmpty(Name))
            response.ListErrors.Add(new Errors { Field = "Name", Detail = "Required" });
        else if (Name.Length > 100)
            response.ListErrors.Add(new Errors { Field = "Name", Detail = "Max 100 chars" });

        if (response.ListErrors.Count > 0) response.IsSuccess = false;
        return Task.FromResult(response);
    }
}
```

## CommandHandler

```csharp
public class BatteryCreateCommandHandler : IRequestHandler<BatteryCreateCommand, BatteryCreateResponse>
{
    private readonly IServiceUnitOfWork _unitOfWork;

    public BatteryCreateCommandHandler(IServiceUnitOfWork unitOfWork)
        => _unitOfWork = unitOfWork;

    public async Task<BatteryCreateResponse> Handle(BatteryCreateCommand request, CancellationToken ct)
    {
        var exists = await _unitOfWork.Batteries.AnyAsync(x => x.Name == request.Name && !x.IsDeleted);
        if (exists)
            return new BatteryCreateResponse { IsSuccess = false, Message = "Already exists" };

        var entity = new Battery { Name = request.Name, Status = request.Status };

        await _unitOfWork.BeginTransactionAsync();
        try
        {
            await _unitOfWork.Batteries.AddAsync(entity);
            await _unitOfWork.CommitTransactionAsync();
        }
        catch (Exception ex)
        {
            await _unitOfWork.RollbackTransactionAsync();
            return new BatteryCreateResponse { IsSuccess = false, Message = ex.Message };
        }

        return new BatteryCreateResponse
        {
            IsSuccess = true,
            Data = new BatteryDTO { Id = entity.Id.ToString(), Name = entity.Name }
        };
    }
}
```

## Critical rules — repository method signatures

```csharp
await _unitOfWork.Batteries.AddAsync(entity);    // async — HAS await
_unitOfWork.Batteries.UpdateAsync(entity);        // VOID — NO await
_unitOfWork.Batteries.DeleteAsync(entity);        // VOID — NO await
```

`GetAllAsync()` returns `IQueryable<T>` synchronously — NEVER await it.

## Soft delete pattern

```csharp
// Delete: interceptor auto-sets IsDeleted=true, DeletedAt=UtcNow
_unitOfWork.Batteries.DeleteAsync(entity);  // NO await

// Restore
entity.IsDeleted = false;
entity.DeletedAt = null;
_unitOfWork.Batteries.UpdateAsync(entity);  // NO await
```

Cascade delete — always delete children before parent:
```csharp
foreach (var child in entity.Children)
    _unitOfWork.Children.DeleteAsync(child);  // NO await
_unitOfWork.Batteries.DeleteAsync(entity);    // NO await
await _unitOfWork.CommitTransactionAsync();
```

## Response types

```csharp
public class BatteryCreateResponse : CommonResponse<BatteryDTO> { }
public class BatteryUpdateResponse : CommonResponse<BatteryDTO> { }
public class BatteryDeleteResponse : CommonResponse<object> { }
public class BatteryRestoreResponse : CommonResponse<object> { }
```

## Query always filter deleted

Project does NOT use global query filter. Always add:
```csharp
.Where(x => !x.IsDeleted)
```

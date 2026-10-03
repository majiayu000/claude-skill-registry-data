---
name: scaffold-cqrs-command
description: Scaffold CQRS Command + Handler (Create/Update/Delete/Restore) với MediatR, UnitOfWork, transaction
argument-hint: [ServiceName EntityName Action]
allowed-tools: Write, Read, Edit
---

# Scaffold Command `$ARGUMENTS`

Usage: `/scaffold-cqrs-command ServiceName EntityName Create|Update|Delete|Restore`

## File 1 — Command: `Application/Commands/{Entity}{Action}/{Entity}{Action}Command.cs`

```csharp
using MediatR;
using SharedContracts.Common.Wrappers;
using SharedContracts.Interfaces;

namespace {Service}.Application.Commands.{Entity}{Action};

public class {Entity}{Action}Command : IRequest<{Entity}{Action}Response>, IValidatable<{Entity}{Action}Response>
{
    // For Update/Delete/Restore: thêm Id
    // public Guid Id { get; set; }

    public string Name { get; set; } = string.Empty;
    // Thêm properties theo nghiệp vụ

    public Task<{Entity}{Action}Response> ValidateAsync()
    {
        var response = new {Entity}{Action}Response();

        if (string.IsNullOrEmpty(Name))
            response.ListErrors.Add(new Errors { Field = "Name", Detail = "Name is required" });

        // Thu thập TẤT CẢ errors (không fail sớm)
        if (response.ListErrors.Count > 0) response.IsSuccess = false;
        return Task.FromResult(response);
    }
}
```

## File 2 — Handler: `Application/Commands/{Entity}{Action}/{Entity}{Action}CommandHandler.cs`

### CREATE Handler

```csharp
public class {Entity}CreateCommandHandler : IRequestHandler<{Entity}CreateCommand, {Entity}CreateResponse>
{
    private readonly IServiceUnitOfWork _unitOfWork;

    public {Entity}CreateCommandHandler(IServiceUnitOfWork unitOfWork) => _unitOfWork = unitOfWork;

    public async Task<{Entity}CreateResponse> Handle({Entity}CreateCommand request, CancellationToken ct)
    {
        var exists = await _unitOfWork.{Entity}s.AnyAsync(x => x.Name == request.Name && !x.IsDeleted);
        if (exists) return new {Entity}CreateResponse { IsSuccess = false, Message = "{Entity} already exists" };

        var entity = new {Entity} { Name = request.Name };

        await _unitOfWork.BeginTransactionAsync();
        try
        {
            await _unitOfWork.{Entity}s.AddAsync(entity);
            await _unitOfWork.CommitTransactionAsync();
        }
        catch (Exception ex)
        {
            await _unitOfWork.RollbackTransactionAsync();
            return new {Entity}CreateResponse { IsSuccess = false, Message = ex.Message };
        }

        return new {Entity}CreateResponse { IsSuccess = true, Data = new {Entity}DTO { Id = entity.Id.ToString() } };
    }
}
```

### UPDATE Handler

```csharp
public async Task<{Entity}UpdateResponse> Handle({Entity}UpdateCommand request, CancellationToken ct)
{
    var entity = await _unitOfWork.{Entity}s.GetAllAsync()
        .FirstOrDefaultAsync(x => x.Id == request.Id);

    if (entity == null) return new {Entity}UpdateResponse { IsSuccess = false, Message = "Not found" };
    if (entity.IsDeleted) return new {Entity}UpdateResponse { IsSuccess = false, Message = "Is deleted" };

    entity.Name = request.Name;

    await _unitOfWork.BeginTransactionAsync();
    try
    {
        _unitOfWork.{Entity}s.UpdateAsync(entity);  // ⚠️ NO await (void method)
        await _unitOfWork.CommitTransactionAsync();
    }
    catch (Exception ex)
    {
        await _unitOfWork.RollbackTransactionAsync();
        return new {Entity}UpdateResponse { IsSuccess = false, Message = ex.Message };
    }

    return new {Entity}UpdateResponse { IsSuccess = true, Data = new {Entity}DTO { Id = entity.Id.ToString() } };
}
```

### DELETE Handler (Soft delete với cascade)

```csharp
public async Task<{Entity}DeleteResponse> Handle({Entity}DeleteCommand request, CancellationToken ct)
{
    var entity = await _unitOfWork.{Entity}s.GetAllAsync()
        .Include(x => x.Children)
        .FirstOrDefaultAsync(x => x.Id == request.Id);

    if (entity == null) return new {Entity}DeleteResponse { IsSuccess = false, Message = "Not found" };

    await _unitOfWork.BeginTransactionAsync();
    try
    {
        // Cascade: xóa children TRƯỚC
        if (entity.Children != null)
            foreach (var child in entity.Children)
                _unitOfWork.Children.DeleteAsync(child);  // ⚠️ NO await

        _unitOfWork.{Entity}s.DeleteAsync(entity);  // ⚠️ NO await — interceptor set IsDeleted=true
        await _unitOfWork.CommitTransactionAsync();
    }
    catch (Exception ex)
    {
        await _unitOfWork.RollbackTransactionAsync();
        return new {Entity}DeleteResponse { IsSuccess = false, Message = ex.Message };
    }

    return new {Entity}DeleteResponse { IsSuccess = true, Message = "Deleted successfully" };
}
```

### RESTORE Handler

```csharp
public async Task<{Entity}RestoreResponse> Handle({Entity}RestoreCommand request, CancellationToken ct)
{
    var entity = await _unitOfWork.{Entity}s.GetAllAsync()
        .FirstOrDefaultAsync(x => x.Id == request.Id && x.IsDeleted);

    if (entity == null) return new {Entity}RestoreResponse { IsSuccess = false, Message = "Not found" };

    entity.IsDeleted = false;
    entity.DeletedAt = null;

    await _unitOfWork.BeginTransactionAsync();
    try
    {
        _unitOfWork.{Entity}s.UpdateAsync(entity);  // ⚠️ NO await
        await _unitOfWork.CommitTransactionAsync();
    }
    catch (Exception ex)
    {
        await _unitOfWork.RollbackTransactionAsync();
        return new {Entity}RestoreResponse { IsSuccess = false, Message = ex.Message };
    }

    return new {Entity}RestoreResponse { IsSuccess = true, Data = new {Entity}DTO { Id = entity.Id.ToString() } };
}
```

## ⚠️ Critical Rules
- `UpdateAsync()` và `DeleteAsync()` là **void** — KHÔNG dùng `await`
- `AddAsync()` IS async — PHẢI `await`
- `CommitTransactionAsync()` tự gọi `SaveChangesAsync()` bên trong
- Publish events SAU `CommitTransactionAsync()` (trừ service có Outbox)

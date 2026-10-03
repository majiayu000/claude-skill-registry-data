---
name: scaffold-consumer
description: Scaffold MassTransit IConsumer để xử lý RabbitMQ integration events (DB write, notification, cross-service update)
argument-hint: [ServiceName EventName]
allowed-tools: Write, Read, Edit
---

# Scaffold Consumer `$ARGUMENTS`

Usage: `/scaffold-consumer ServiceName EventName`  
Example: `/scaffold-consumer TicketService BatteryAnomalyDetectedEvent`

## File: `Infrastructure/Consumers/{EventName}Consumer.cs`

### Type A — DB Write + Notification

```csharp
using MassTransit;
using SharedContracts.EventModels;
using {Service}.Application.Interfaces;
using {Service}.Domain.Entities;

namespace {Service}.Infrastructure.Consumers;

public class {EventName}Consumer : IConsumer<{EventName}>
{
    private readonly IServiceUnitOfWork _unitOfWork;
    private readonly ILogger<{EventName}Consumer> _logger;

    public {EventName}Consumer(IServiceUnitOfWork unitOfWork, ILogger<{EventName}Consumer> logger)
    {
        _unitOfWork = unitOfWork;
        _logger = logger;
    }

    public async Task Consume(ConsumeContext<{EventName}> context)
    {
        var evt = context.Message;
        _logger.LogInformation("Processing {EventName}, Id: {Id}", nameof({EventName}), evt.Id);

        // Tạo entity từ event data
        var entity = new SomeEntity
        {
            UserId = evt.UserId,
            RelatedId = evt.RelatedId,
            // Map other properties...
        };

        await _unitOfWork.SomeEntities.AddAsync(entity);
        await _unitOfWork.SaveChangesAsync();

        _logger.LogInformation("Processed {EventName} successfully", nameof({EventName}));
    }
}
```

### Type B — Cross-Service Entity Update

```csharp
public async Task Consume(ConsumeContext<{EventName}> context)
{
    var msg = context.Message;

    var entity = _unitOfWork.Entities.GetAllAsync()
        .FirstOrDefault(x => x.Id == msg.EntityId);

    if (entity == null) return;

    await _unitOfWork.BeginTransactionAsync();
    try
    {
        entity.SomeProperty = msg.NewValue;
        _unitOfWork.Entities.UpdateAsync(entity);  // ⚠️ NO await (void)
        await _unitOfWork.CommitTransactionAsync();
    }
    catch (Exception ex)
    {
        await _unitOfWork.RollbackTransactionAsync();
        _logger.LogError(ex, "Failed to process {Event}", nameof({EventName}));
        throw;  // MassTransit sẽ auto-retry
    }
}
```

## Đăng ký DI

Trong `ManageDependencyInjection.cs`, đảm bảo assembly của consumer được scan:

```csharp
services.AddMessageBus(configuration, typeof({EventName}Consumer).Assembly);
```

## Rules
- Implement `IConsumer<TEvent>` từ MassTransit
- File location: `Infrastructure/Consumers/`
- Throw exception on failure → MassTransit tự retry
- `UpdateAsync()` là void — KHÔNG await
- Consumer được tự động discover qua assembly scanning

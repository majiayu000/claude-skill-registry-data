---
name: scaffold-integration-event
description: Scaffold IntegrationEvent record class cho async messaging qua RabbitMQ/MassTransit
argument-hint: [EventName]
allowed-tools: Write, Read, Edit
---

# Scaffold Integration Event `$ARGUMENTS`

Usage: `/scaffold-integration-event EventName`  
Example: `/scaffold-integration-event BatteryAnomalyDetectedEvent`

## File: `shared/SharedContracts/EventModels/{EventName}.cs`

```csharp
using SharedContracts.Events;

namespace SharedContracts.EventModels;

/// <summary>
/// Published by: [SourceService] khi [mô tả trigger]
/// Consumed by: [ConsumerService] để [mô tả action]
/// </summary>
public record {EventName} : IntegrationEvent
{
    public Guid UserId { get; set; }
    public Guid RelatedId { get; set; }      // e.g., BatteryId, TicketId
    public string EntityName { get; set; } = string.Empty;

    // Thêm properties theo nghiệp vụ:
    // public decimal Severity { get; set; }
    // public string[] AffectedComponents { get; set; } = Array.Empty<string>();
}
```

## Base class (đã có trong SharedContracts)

```csharp
public abstract record IntegrationEvent
{
    public Guid Id { get; } = Guid.NewGuid();
    public DateTime OccurredAt { get; } = DateTime.UtcNow;
}
```

## Publishing (trong source handler)

```csharp
// SAU CommitTransactionAsync (default — service không có Outbox)
await _unitOfWork.CommitTransactionAsync();

await _messageProducer.PublishAsync(new {EventName}
{
    UserId = entity.UserId,
    RelatedId = entity.Id,
    EntityName = entity.Name,
});
```

## Steps tiếp theo

1. Tạo consumer: `/scaffold-consumer {Service} {EventName}`
2. Đăng ký consumer assembly trong `ManageDependencyInjection.cs`

## Rules
- Dùng `record` (KHÔNG phải class) — extends `IntegrationEvent`
- Location: `shared/SharedContracts/EventModels/`
- `Id` và `OccurredAt` auto-set bởi base class
- Document publisher + consumer trong XML comment
- Publish SAU transaction commit

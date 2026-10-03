---
name: consumer
description: Creating a RabbitMQ MassTransit consumer or integration event in any backend microservice. Triggers when implementing a Consumer class that handles an IntegrationEvent, creating a new IntegrationEvent record type, or wiring up MassTransit bus registration in DI.
---

## Nguyên tắc bắt buộc

1. **Tuân thủ tuyệt đối** cấu trúc folder, naming convention, và code pattern được định nghĩa trong skill này — không tự ý thay đổi tên event, tên consumer, hay thứ tự publish/commit.
2. **Hỏi trước khi code** nếu bất kỳ yêu cầu nào chưa rõ (service nào publish, service nào consume, có Outbox không, business logic trong consumer làm gì). Không đoán mò — một câu hỏi ngắn tốt hơn một giờ implement sai hướng.

---

# BE Consumer + Integration Event Pattern

## Integration Event (SharedContracts)

```csharp
// Use record, not class
public record BatteryAnomalyDetectedEvent : IntegrationEvent
{
    public Guid BatteryId { get; set; }
    public string Severity { get; set; } = string.Empty;
    public float SohPercent { get; set; }
}
```

File: `SharedContracts/Events/{EventName}.cs`

## Consumer

```csharp
public class BatteryAnomalyDetectedConsumer : IConsumer<BatteryAnomalyDetectedEvent>
{
    private readonly IServiceUnitOfWork _unitOfWork;

    public BatteryAnomalyDetectedConsumer(IServiceUnitOfWork unitOfWork)
        => _unitOfWork = unitOfWork;

    public async Task Consume(ConsumeContext<BatteryAnomalyDetectedEvent> context)
    {
        var evt = context.Message;

        var battery = await _unitOfWork.Batteries.GetAllAsync()
            .Where(x => x.Id == evt.BatteryId && !x.IsDeleted)
            .FirstOrDefaultAsync();

        if (battery == null) return;

        // business logic...
        await _unitOfWork.BeginTransactionAsync();
        try
        {
            // mutations...
            await _unitOfWork.CommitTransactionAsync();
        }
        catch
        {
            await _unitOfWork.RollbackTransactionAsync();
            throw; // MassTransit auto-retry on throw
        }
    }
}
```

File: `Infrastructure/Consumers/{EventName}Consumer.cs`

## Publish convention

- Service WITHOUT Outbox: publish **after** `CommitTransactionAsync()`
- Service WITH Outbox: publish **before** `SaveChangesAsync()` (atomic)

```csharp
// Without Outbox (default)
await _unitOfWork.CommitTransactionAsync();
await _publishEndpoint.Publish(new BatteryAnomalyDetectedEvent { ... });
```

## DI registration

```csharp
services.AddMessageBus(configuration, typeof(BatteryAnomalyDetectedConsumer).Assembly);
```

## Naming

| Type | Pattern | Example |
|------|---------|---------|
| Event | `{Action}Event.cs` (record) | `BatteryAnomalyDetectedEvent.cs` |
| Consumer | `{EventName}Consumer.cs` | `BatteryAnomalyDetectedConsumer.cs` |

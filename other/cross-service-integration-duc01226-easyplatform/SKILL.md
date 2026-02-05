---
name: cross-service-integration
description: Use when designing or implementing cross-service communication, data synchronization, or service boundary patterns.
---

# Cross-Service Integration

## Communication Methods

| Method          | Use Case                          | Direction        |
| --------------- | --------------------------------- | ---------------- |
| Entity Event    | Automatic entity sync             | Publisher->All   |
| Request Message | Request data from another service | Requester->Owner |
| Event Message   | Notify of domain events           | Publisher->All   |

## Entity Event Bus (Automatic Sync)

```csharp
// Producer (in source service) - Platform handles automatically
// Entities sync via PlatformCqrsEntityEventBusMessageProducer

// Consumer (in target service)
internal sealed class UpsertEmployeeOnEventConsumer :
    PlatformApplicationMessageBusConsumer<EmployeeEntityEventBusMessage>
{
    public override async Task<bool> HandleWhen(
        EmployeeEntityEventBusMessage msg, string routingKey) => true;

    public override async Task HandleLogicAsync(
        EmployeeEntityEventBusMessage msg, string routingKey)
    {
        // Wait for dependencies with timeout
        var companyExists = await Util.TaskRunner.TryWaitUntilAsync(
            () => companyRepo.AnyAsync(c => c.Id == msg.Payload.EntityData.CompanyId),
            maxWaitSeconds: 300);

        if (!companyExists) return;

        // CREATE/UPDATE
        if (msg.Payload.CrudAction == Created ||
            (msg.Payload.CrudAction == Updated && !msg.Payload.EntityData.IsDeleted))
        {
            var existing = await repository.FirstOrDefaultAsync(
                e => e.Id == msg.Payload.EntityData.Id);

            if (existing == null)
                await repository.CreateAsync(
                    msg.Payload.EntityData.ToEntity()
                        .With(e => e.LastMessageSyncDate = msg.CreatedUtcDate));
            else if (existing.LastMessageSyncDate <= msg.CreatedUtcDate)
                await repository.UpdateAsync(
                    msg.Payload.EntityData.UpdateEntity(existing)
                        .With(e => e.LastMessageSyncDate = msg.CreatedUtcDate));
        }

        // DELETE
        if (msg.Payload.CrudAction == Deleted ||
            (msg.Payload.CrudAction == Updated && msg.Payload.EntityData.IsDeleted))
            await repository.DeleteAsync(msg.Payload.EntityData.Id);
    }
}
```

## Service Boundaries

| Service      | Owns                               | Syncs From       |
| ------------ | ---------------------------------- | ---------------- |
| Accounts     | Users, Companies, Licenses         | -                |
| TextSnippet  | Snippets, Categories, Tags         | Users, Companies |

## Key Patterns

| Pattern                  | Purpose                            |
| ------------------------ | ---------------------------------- |
| `TryWaitUntilAsync`      | Wait for dependencies with timeout |
| `LastMessageSyncDate`    | Prevent race conditions            |
| `IsForceSyncDataRequest` | Check for force sync requests      |
| `ToEntity()`             | Map message to local entity        |

## Message Naming Convention

| Type    | Pattern                                 | Example                                 |
| ------- | --------------------------------------- | --------------------------------------- |
| Event   | `{Service}{Feature}{Action}EventBusMsg` | `TextSnippetCreatedEventBusMsg`         |
| Request | `{Consumer}{Feature}RequestBusMsg`      | `TextSnippetCategoryDataRequestBusMsg`  |

## Anti-Patterns

- Direct database access across services
- Synchronous HTTP calls between services
- Not waiting for dependencies before processing
- Ignoring `LastMessageSyncDate` (causes race conditions)
- Processing messages out of order

---
name: message-bus
description: Use when implementing cross-service communication via RabbitMQ message bus, entity event producers, or message consumers.
---

# Message Bus Development Workflow

## When to Use This Skill

- Cross-service data synchronization
- Entity event publishing to other services
- Consuming events from other services
- Event-driven architecture patterns

## Message Naming Convention

| Type    | Producer Role | Pattern                                           | Example                                            |
| ------- | ------------- | ------------------------------------------------- | -------------------------------------------------- |
| Event   | Leader        | `<ServiceName><Feature><Action>EventBusMessage`   | `CandidateJobBoardApiSyncCompletedEventBusMessage` |
| Request | Follower      | `<ConsumerServiceName><Feature>RequestBusMessage` | `JobCreateNonexistentJobsRequestBusMessage`        |

- **Event messages**: Producer defines the schema (leader). Named with producer's service name prefix.
- **Request messages**: Consumer defines the schema (leader). Named with consumer's service name prefix.
- **Consumer naming**: Consumer class name matches the message it consumes.

## Pre-Flight Checklist

- [ ] Identify source and target services
- [ ] Determine message type (entity event vs custom message)
- [ ] Check existing producers: `grep "EntityEventBusMessageProducer" --include="*.cs"`
- [ ] Check existing consumers: `grep "MessageBusConsumer" --include="*.cs"`

## File Locations

### Producer (Source Service)

```
{Service}.Application/
└── MessageBusProducers/
    └── {Entity}EntityEventBusMessageProducer.cs
```

### Consumer (Target Service)

```
{Service}.Application/
└── MessageBusConsumers/
    └── {SourceEntity}/
        └── {Action}On{Entity}EntityEventBusConsumer.cs
```

### Message Definition (Shared)

```
YourApp.Shared/
└── CrossServiceMessages/
    └── {Entity}EntityEventBusMessage.cs
```

## Pattern 1: Entity Event Producer

Auto-publishes when entity changes via repository CRUD.

```csharp
// Message definition (in YourApp.Shared)
public sealed class EntityEventBusMessage
    : PlatformCqrsEntityEventBusMessage<EntityEventData, string>
{
    public EntityEventBusMessage() { }

    public EntityEventBusMessage(
        PlatformCqrsEntityEvent<Entity> entityEvent,
        EntityEventData entityData)
        : base(entityEvent, entityData)
    {
    }
}

public sealed class EntityEventData
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";
    public string Email { get; set; } = "";
    public string CompanyId { get; set; } = "";
    public bool IsDeleted { get; set; }

    public EntityEventData() { }

    public EntityEventData(Entity entity)
    {
        Id = entity.Id;
        Name = entity.Name;
        Email = entity.Email;
        CompanyId = entity.CompanyId;
        IsDeleted = entity.IsDeleted;
    }

    // Map to target service entity
    public TargetEntity ToEntity() => new TargetEntity
    {
        SourceId = Id,
        Name = Name,
        Email = Email,
        CompanyId = CompanyId
    };

    public TargetEntity UpdateEntity(TargetEntity existing)
    {
        existing.Name = Name;
        existing.Email = Email;
        return existing;
    }
}
```

```csharp
// Producer (in source service)
internal sealed class EntityEventBusMessageProducer
    : PlatformCqrsEntityEventBusMessageProducer<EntityEventBusMessage, Entity, string>
{
    public EntityEventBusMessageProducer(
        ILoggerFactory loggerFactory,
        IPlatformUnitOfWorkManager unitOfWorkManager,
        IServiceProvider serviceProvider,
        IPlatformRootServiceProvider rootServiceProvider)
        : base(loggerFactory, unitOfWorkManager, serviceProvider, rootServiceProvider)
    {
    }

    // Filter which events to publish
    public override async Task<bool> HandleWhen(PlatformCqrsEntityEvent<Entity> @event)
    {
        // Skip test data seeding
        if (@event.RequestContext.IsSeedingTestingData()) return false;

        // Only publish for active entities or deletions
        return @event.EntityData.IsActive ||
               @event.CrudAction == PlatformCqrsEntityEventCrudAction.Deleted;
    }

    // Build the message
    protected override Task<EntityEventBusMessage> BuildMessageAsync(
        PlatformCqrsEntityEvent<Entity> @event,
        CancellationToken ct)
    {
        return Task.FromResult(new EntityEventBusMessage(
            @event,
            new EntityEventData(@event.EntityData)));
    }
}
```

## Pattern 2: Entity Event Consumer

Syncs entity data from source service.

```csharp
internal sealed class UpsertOrDeleteEntityOnEntityEventBusConsumer
    : PlatformApplicationMessageBusConsumer<EntityEventBusMessage>
{
    private readonly IPlatformQueryableRootRepository<TargetEntity, string> entityRepo;
    private readonly IPlatformQueryableRootRepository<Company, string> companyRepo;

    public UpsertOrDeleteEntityOnEntityEventBusConsumer(
        ILoggerFactory loggerFactory,
        IServiceProvider serviceProvider,
        IPlatformQueryableRootRepository<TargetEntity, string> entityRepo,
        IPlatformQueryableRootRepository<Company, string> companyRepo)
        : base(loggerFactory, serviceProvider)
    {
        this.entityRepo = entityRepo;
        this.companyRepo = companyRepo;
    }

    // Filter which messages to handle
    public override async Task<bool> HandleWhen(
        EntityEventBusMessage message,
        string routingKey)
    {
        return true;  // Handle all entity events
    }

    // Process the message
    public override async Task HandleLogicAsync(
        EntityEventBusMessage message,
        string routingKey)
    {
        var payload = message.Payload;
        var entityData = payload.EntityData;

        // ═══════════════════════════════════════════════════════════════════
        // WAIT FOR DEPENDENCIES (with timeout)
        // ═══════════════════════════════════════════════════════════════════
        var companyMissing = await Util.TaskRunner
            .TryWaitUntilAsync(
                () => companyRepo.AnyAsync(c => c.Id == entityData.CompanyId),
                maxWaitSeconds: message.IsForceSyncDataRequest() ? 30 : 300)
            .Then(found => !found);

        if (companyMissing)
        {
            Logger.LogWarning("Company {CompanyId} not found, skipping entity sync",
                entityData.CompanyId);
            return;
        }

        // ═══════════════════════════════════════════════════════════════════
        // HANDLE DELETE
        // ═══════════════════════════════════════════════════════════════════
        if (payload.CrudAction == PlatformCqrsEntityEventCrudAction.Deleted ||
            (payload.CrudAction == PlatformCqrsEntityEventCrudAction.Updated && entityData.IsDeleted))
        {
            await entityRepo.DeleteAsync(entityData.Id);
            return;
        }

        // ═══════════════════════════════════════════════════════════════════
        // HANDLE CREATE/UPDATE
        // ═══════════════════════════════════════════════════════════════════
        var existing = await entityRepo.FirstOrDefaultAsync(
            e => e.SourceId == entityData.Id);

        if (existing == null)
        {
            // Create new
            await entityRepo.CreateAsync(
                entityData.ToEntity()
                    .With(e => e.LastMessageSyncDate = message.CreatedUtcDate));
        }
        else if (existing.LastMessageSyncDate <= message.CreatedUtcDate)
        {
            // Update (only if message is newer - prevents race conditions)
            await entityRepo.UpdateAsync(
                entityData.UpdateEntity(existing)
                    .With(e => e.LastMessageSyncDate = message.CreatedUtcDate));
        }
        // else: Skip - we have a newer version already
    }
}
```

## Pattern 3: Custom Message (Non-Entity)

For events that aren't tied to entity CRUD.

```csharp
// Message definition
public sealed class NotificationRequestMessage : PlatformBusMessage
{
    public string UserId { get; set; } = "";
    public string Subject { get; set; } = "";
    public string Body { get; set; } = "";
    public NotificationType Type { get; set; }
}

// Producer (manual publish)
public class NotificationService
{
    private readonly IPlatformMessageBusProducer messageBus;

    public async Task SendNotificationAsync(NotificationRequest request)
    {
        await messageBus.PublishAsync(new NotificationRequestMessage
        {
            UserId = request.UserId,
            Subject = request.Subject,
            Body = request.Body,
            Type = request.Type
        });
    }
}

// Consumer
internal sealed class ProcessNotificationRequestConsumer
    : PlatformApplicationMessageBusConsumer<NotificationRequestMessage>
{
    public override async Task HandleLogicAsync(
        NotificationRequestMessage message,
        string routingKey)
    {
        // Process notification
        await notificationService.ProcessAsync(message);
    }
}
```

## Key Patterns

### Wait for Dependencies

```csharp
// Wait up to 5 minutes for company to exist
var found = await Util.TaskRunner.TryWaitUntilAsync(
    () => companyRepo.AnyAsync(c => c.Id == companyId),
    maxWaitSeconds: 300);

if (!found) return;  // Skip if dependency never arrived
```

### Prevent Race Conditions

```csharp
// Use LastMessageSyncDate to handle out-of-order messages
if (existing.LastMessageSyncDate <= message.CreatedUtcDate)
{
    // This message is newer, apply it
    await repository.UpdateAsync(existing.With(e =>
        e.LastMessageSyncDate = message.CreatedUtcDate));
}
// else: Skip - we already have a newer version
```

### Force Sync Detection

```csharp
// Shorter wait for force sync operations
var timeout = message.IsForceSyncDataRequest() ? 30 : 300;
```

## Anti-Patterns to AVOID

:x: **No dependency waiting**

```csharp
// WRONG - foreign key violation if company not synced yet
await entityRepo.CreateAsync(entity);

// CORRECT - wait for company first
await Util.TaskRunner.TryWaitUntilAsync(() => companyRepo.AnyAsync(...));
```

:x: **No race condition handling**

```csharp
// WRONG - later message might overwrite newer data
await repository.UpdateAsync(entity);

// CORRECT - check message timestamp
if (existing.LastMessageSyncDate <= message.CreatedUtcDate)
```

:x: **Blocking in producer**

```csharp
// WRONG - long operations in producer slow down source service
protected override async Task<Message> BuildMessageAsync(...)
{
    await expensiveOperation();  // BAD
}
```

:x: **Missing soft delete handling**

```csharp
// WRONG - only checks CrudAction.Deleted
if (payload.CrudAction == Deleted)

// CORRECT - also check soft delete flag
if (payload.CrudAction == Deleted ||
    (payload.CrudAction == Updated && entityData.IsDeleted))
```

## Verification Checklist

- [ ] Message in `YourApp.Shared/CrossServiceMessages/`
- [ ] Producer filters with `HandleWhen()`
- [ ] Consumer waits for dependencies with timeout
- [ ] `LastMessageSyncDate` used for race condition prevention
- [ ] Soft delete handled correctly
- [ ] `IsForceSyncDataRequest()` checked for timeout adjustment
- [ ] Test data seeding skipped in producer

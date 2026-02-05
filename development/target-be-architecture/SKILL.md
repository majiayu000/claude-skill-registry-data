---
name: target-be-architecture
description: Target backend architecture for Lingx. CQRS-lite with event-driven patterns, module organization, and real-time collaboration support. Use when implementing backend features, reviewing code, or making architectural decisions.
---

# Lingx Backend Architecture

CQRS-lite + Event-Driven architecture for scalable translation management.

## Why CQRS-lite for Lingx?

| Challenge               | CQRS Solution                                           |
| ----------------------- | ------------------------------------------------------- |
| Read/Write asymmetry    | Workbench reads many translations, writes one at a time |
| Async operations        | AI translation, imports, webhooks via EventBus          |
| Real-time collaboration | Events broadcast changes to connected users             |
| Audit trail             | Events capture who changed what and when                |

## Directory Structure

```
apps/api/src/
├── modules/                    # Domain modules
│   ├── project/
│   │   ├── commands/           # CreateProject, UpdateProject
│   │   ├── queries/            # GetProject, ListProjects
│   │   ├── events/             # ProjectCreated, ProjectUpdated
│   │   ├── handlers/           # Command & Event handlers
│   │   └── project.repository.ts
│   ├── translation/
│   │   ├── commands/           # UpdateTranslation, BulkImport
│   │   ├── queries/            # GetTranslations, SearchKeys
│   │   ├── events/             # TranslationUpdated, KeyCreated
│   │   ├── handlers/
│   │   └── translation.repository.ts
│   └── collaboration/          # Real-time features
│       ├── commands/           # JoinRoom, FocusKey
│       ├── queries/            # GetPresence
│       ├── events/             # UserJoined, UserFocused
│       └── handlers/
├── shared/
│   ├── cqrs/                   # Bus implementations
│   │   ├── command-bus.ts
│   │   ├── query-bus.ts
│   │   └── event-bus.ts
│   ├── domain/                 # Base classes, errors
│   └── container/              # Awilix DI setup
├── routes/                     # Thin HTTP layer
├── workers/                    # Event consumers (BullMQ)
└── websocket/                  # Real-time connections
```

## Core Concepts

### Command/Query Separation

```
┌─────────────────────────────────────────────────────────────┐
│  HTTP Request                                                │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
┌───────────────┐           ┌───────────────┐
│   Command     │           │    Query      │
│   (Write)     │           │    (Read)     │
└───────┬───────┘           └───────┬───────┘
        │                           │
        ▼                           ▼
┌───────────────┐           ┌───────────────┐
│ CommandHandler│           │ QueryHandler  │
│ - Validate    │           │ - Fetch data  │
│ - Execute     │           │ - Transform   │
│ - Emit Event  │           │ - Cache       │
└───────┬───────┘           └───────────────┘
        │
        ▼
┌───────────────┐
│   EventBus    │ ──► Real-time sync
│               │ ──► Audit log
│               │ ──► Webhooks
└───────────────┘
```

### Data Flow

1. **Route** receives HTTP request, validates input
2. **Route** creates Command or Query object
3. **Bus** dispatches to appropriate Handler
4. **Handler** executes logic via Repository
5. **Handler** emits Event (commands only)
6. **EventBus** triggers side effects

## Quick Reference

### Command Pattern

```typescript
// modules/translation/commands/update-translation.command.ts
export class UpdateTranslationCommand {
  constructor(
    public readonly keyId: string,
    public readonly language: string,
    public readonly value: string,
    public readonly userId: string
  ) {}
}

// modules/translation/handlers/update-translation.handler.ts
export class UpdateTranslationHandler implements ICommandHandler<UpdateTranslationCommand> {
  constructor(
    private repo: TranslationRepository,
    private eventBus: EventBus
  ) {}

  async execute(cmd: UpdateTranslationCommand): Promise<Translation> {
    const translation = await this.repo.update({
      keyId: cmd.keyId,
      language: cmd.language,
      value: cmd.value,
    });

    await this.eventBus.publish(new TranslationUpdatedEvent(translation, cmd.userId));

    return translation;
  }
}
```

### Query Pattern

```typescript
// modules/translation/queries/get-translations.query.ts
export class GetTranslationsQuery {
  constructor(
    public readonly branchId: string,
    public readonly options: { search?: string; page?: number }
  ) {}
}

// modules/translation/handlers/get-translations.handler.ts
export class GetTranslationsHandler implements IQueryHandler<GetTranslationsQuery> {
  constructor(private repo: TranslationRepository) {}

  async execute(query: GetTranslationsQuery): Promise<PaginatedResult<Translation>> {
    return this.repo.findByBranch(query.branchId, query.options);
  }
}
```

### Event Pattern

```typescript
// modules/translation/events/translation-updated.event.ts
export class TranslationUpdatedEvent implements IDomainEvent {
  public readonly occurredAt = new Date();

  constructor(
    public readonly translation: Translation,
    public readonly userId: string
  ) {}
}

// Event handlers (side effects)
// - RealTimeSyncHandler: Broadcast via WebSocket
// - AuditLogHandler: Record change history
// - WebhookHandler: Notify external systems
```

### Thin Route

```typescript
// routes/translations/handlers.ts
export function createTranslationHandlers(container: AwilixContainer) {
  return {
    async updateTranslation(request: FastifyRequest, reply: FastifyReply) {
      const commandBus = container.resolve<CommandBus>('commandBus');

      const result = await commandBus.execute(
        new UpdateTranslationCommand(
          request.params.keyId,
          request.body.language,
          request.body.value,
          request.userId
        )
      );

      return toTranslationDto(result);
    },
  };
}
```

## Decision Tree

```
Where does this code belong?

Is it a write operation that changes state?
  └─ Command + CommandHandler

Is it a read operation returning data?
  └─ Query + QueryHandler

Is it a side effect of a write (notify, log, sync)?
  └─ Event + EventHandler

Is it HTTP parsing/response formatting?
  └─ Route handlers

Is it database access?
  └─ Repository
```

## Documentation

| Document                                             | Purpose                   |
| ---------------------------------------------------- | ------------------------- |
| [cqrs-overview.md](cqrs-overview.md)                 | CQRS-lite concepts        |
| [commands.md](commands.md)                           | Command patterns          |
| [queries.md](queries.md)                             | Query patterns            |
| [events.md](events.md)                               | Event patterns, real-time |
| [modules.md](modules.md)                             | Module organization       |
| [routes.md](routes.md)                               | Thin HTTP layer           |
| [repositories.md](repositories.md)                   | Data access               |
| [dependency-injection.md](dependency-injection.md)   | Awilix setup              |
| [migration-guide.md](migration-guide.md)             | Service → CQRS migration  |
| [error-handling.md](error-handling.md)               | Error flow and patterns   |
| [events-best-practices.md](events-best-practices.md) | Event design guidelines   |

## Anti-Patterns

### ❌ Business logic in routes

```typescript
// BAD
app.post('/translations', async (request) => {
  const existing = await prisma.key.findUnique({ where: { id } });
  if (!existing) throw new Error('Key not found');
  const result = await prisma.translation.update({ ... });
  await redis.publish('translation:updated', result); // Side effect in route
  return result;
});
```

### ✅ Route delegates to command

```typescript
// GOOD
app.post('/translations', async (request) => {
  const result = await commandBus.execute(
    new UpdateTranslationCommand(request.params.id, request.body)
  );
  return toDto(result);
});
```

### ❌ Handler without event emission

```typescript
// BAD - No way to react to changes
async execute(cmd: UpdateTranslationCommand) {
  return this.repo.update(cmd);
}
```

### ✅ Handler emits event

```typescript
// GOOD - Enables real-time sync, audit, webhooks
async execute(cmd: UpdateTranslationCommand) {
  const result = await this.repo.update(cmd);
  await this.eventBus.publish(new TranslationUpdatedEvent(result, cmd.userId));
  return result;
}
```

## Real-time Collaboration

Events enable real-time features:

```typescript
// Event handlers for real-time sync
@EventHandler(TranslationUpdatedEvent)
export class RealTimeSyncHandler {
  constructor(private wsServer: WebSocketServer) {}

  async handle(event: TranslationUpdatedEvent) {
    this.wsServer.broadcast(`branch:${event.translation.branchId}`, {
      type: 'translation:updated',
      data: event.translation,
    });
  }
}

@EventHandler(UserFocusedKeyEvent)
export class PresenceSyncHandler {
  async handle(event: UserFocusedKeyEvent) {
    this.wsServer.broadcast(`branch:${event.branchId}`, {
      type: 'presence:focus',
      userId: event.userId,
      keyId: event.keyId,
    });
  }
}
```

## Benefits

1. **Testable** - Mock buses in tests, no HTTP/database setup
2. **Scalable** - Events can be processed by workers
3. **Real-time ready** - Events broadcast changes instantly
4. **Auditable** - Events capture full history
5. **Decoupled** - Handlers don't know about each other

Sources:

- [CQRS Pattern](https://docs.microsoft.com/en-us/azure/architecture/patterns/cqrs)
- [Event-Driven Architecture](https://martinfowler.com/articles/201701-event-driven.html)
- [Domain Events](https://docs.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/domain-events-design-implementation)

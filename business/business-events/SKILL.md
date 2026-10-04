---
name: business-events
description: "Define event-driven APIs over Kafka with Mendix business event services — publish and subscribe contracts, CREATE/DROP/DESCRIBE. Use when building publish/subscribe integration between apps, or inspecting the business event services a project already has."
---

# Business Events

## When to Use This Skill

Use this skill when the user wants to:
- Define event-driven APIs using Kafka/message brokers
- Create business event services that publish events
- View or describe existing business event services
- Set up publish/subscribe message channels

## Commands

### View Business Events

```sql
-- List all business event service documents
list business event services;

-- Filter by module
list business event services in MyModule;

-- List all business event client documents (future)
list business event clients;

-- List individual messages across all services
list business events;

-- Filter messages by module
list business events in MyModule;

-- Full MDL description (round-trippable)
describe business event service Module.ServiceName;
```

### Create a Business Event Service

```sql
mdl 1;
create business event service Module.CustomerEventsApi
(
  ServiceName: 'CustomerEventsApi',
  EventNamePrefix: 'com.example'
)
{
  message CustomerChangedEvent (CustomerId: long) publish
    entity Module.PBE_CustomerChangedEvent;
  message AddressChangedEvent (AddressId: long) publish
    entity Module.PBE_AddressChangedEvent;
};
```

### Create or Modify (Idempotent Update — Preferred)

Preserves the existing UUID so other documents that reference this service remain valid.
`OR REPLACE` is accepted as a synonym.

```sql
mdl 1;
create or modify business event service Module.CustomerEventsApi
(
  ServiceName: 'CustomerEventsApi',
  EventNamePrefix: ''
)
{
  message CustomerChangedEvent (CustomerId: long) publish
    entity Module.PBE_CustomerChangedEvent;
};
```

### Drop a Business Event Service

```sql
mdl 1;
drop business event service Module.CustomerEventsApi;
```

## Message Definition Syntax

```
message <MessageName> (<AttrName>: <type>, ...) publish|subscribe
  [entity <Module.EntityName>]
  [microflow <Module.MicroflowName>];
```

### Supported Attribute Types
- `string` - Text
- `integer` - 32-bit integer
- `long` - 64-bit integer
- `decimal` - Precise decimal number
- `boolean` - True/false
- `datetime` - Date and time

## Service Properties

| Property | Description |
|----------|-------------|
| `ServiceName` | The service name used in the event broker |
| `EventNamePrefix` | Prefix added to event names (can be empty) |
| `folder` | Optional folder path for the service document |

## Operations

| Operation | Description |
|-----------|-------------|
| `publish` | This service publishes the event (other apps subscribe) |
| `subscribe` | This service subscribes to the event (other apps publish) |

## Publishing Events from Microflows

There is no dedicated microflow activity for publishing business events. Instead, Mendix
provides Java actions in the `BusinessEvents` marketplace module. Use `call java action`
to publish an event from a microflow:

```sql
-- Create an event entity instance and publish it
create microflow Module.ACT_PublishCustomerChanged
  folder 'ACT'
begin
  $event = create Module.PBE_CustomerChangedEvent (CustomerId = $CustomerId);
  commit $event;
  call java action BusinessEvents.PublishBusinessEvent_V2(EventObject = $event);
end;
```

### Available Java Actions (from BusinessEvents module)

| Java Action | Description |
|-------------|-------------|
| `BusinessEvents.PublishBusinessEvent_V2` | Publish an event (recommended) |
| `BusinessEvents.PublishBusinessEvent` | Publish an event (legacy) |
| `BusinessEvents.ConsumeBusinessEvent` | Consume/acknowledge an event |
| `BusinessEvents.PublishEvents` | Publish multiple events |
| `BusinessEvents.StartupBusinessEvents` | Initialize the event broker connection |
| `BusinessEvents.ShutdownBusinessEvents` | Shut down the event broker connection |

### Typical Pattern

1. Define a Business Event Service with PUBLISH messages
2. Create entities prefixed with `PBE_` that **extend `BusinessEvents.PublishedBusinessEvent`**
3. Entity attributes must **exactly match** the message attributes (no extra attributes on the entity)
4. In microflows, create an instance of the event entity, populate its attributes, commit it
5. Call `BusinessEvents.PublishBusinessEvent_V2` passing the entity instance
6. For subscribe operations, link a handler microflow in the service definition

## Checklist

- [ ] Linked entities must exist before creating the service
- [ ] **Entities must extend `BusinessEvents.PublishedBusinessEvent`** (for published events)
- [ ] **Entity attributes must exactly match the message attributes** (no extra/missing attributes)
- [ ] Entity names use qualified format: `Module.EntityName`
- [ ] Entities for published events are conventionally prefixed with `PBE_`
- [ ] Attribute types must be valid (String, Integer, Long, Decimal, Boolean, DateTime)
- [ ] Use `describe business event service` to verify the result
- [ ] The DESCRIBE output is parseable and can be used as a CREATE statement
- [ ] To publish events from microflows, use `call java action BusinessEvents.PublishBusinessEvent_V2`
- [ ] The `BusinessEvents` module must be included in the project (marketplace module)

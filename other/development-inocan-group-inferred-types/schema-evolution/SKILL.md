---
name: schema-evolution
description: Schema evolution patterns for backward and forward compatibility
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Schema Evolution Skill

## When to Use This Skill

Use this skill when:

- **Schema Evolution tasks** - Working on schema evolution patterns for backward and forward compatibility
- **Planning or design** - Need guidance on Schema Evolution approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Design and manage schema evolution for API and data contracts.

## MANDATORY: Documentation-First Approach

Before designing schema evolution:

1. **Invoke `docs-management` skill** for evolution patterns
2. **Verify schema patterns** via MCP servers (context7, perplexity)
3. **Base guidance on schema evolution best practices**

## Compatibility Dimensions

```text
SCHEMA COMPATIBILITY TYPES:

┌─────────────────────────────────────────────────────────────────┐
│                  COMPATIBILITY MATRIX                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  BACKWARD COMPATIBLE                                            │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ New schema can read OLD data                              │  │
│  │                                                           │  │
│  │ Consumer v2 ──reads──► Producer v1 data                   │  │
│  │                                                           │  │
│  │ Use case: Rolling upgrade where consumers update first    │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  FORWARD COMPATIBLE                                             │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Old schema can read NEW data                              │  │
│  │                                                           │  │
│  │ Consumer v1 ──reads──► Producer v2 data                   │  │
│  │                                                           │  │
│  │ Use case: Rolling upgrade where producers update first    │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  FULL COMPATIBLE                                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Both backward AND forward compatible                      │  │
│  │                                                           │  │
│  │ Consumer v1 ←──reads──► Producer v2                       │  │
│  │ Consumer v2 ←──reads──► Producer v1                       │  │
│  │                                                           │  │
│  │ Use case: Maximum flexibility, any upgrade order          │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  NO COMPATIBILITY (Breaking)                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Requires coordinated upgrade                              │  │
│  │                                                           │  │
│  │ All producers and consumers must update together          │  │
│  │                                                           │  │
│  │ Use case: Major version with clean break                  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Evolution Rules by Change Type

```text
SCHEMA CHANGE COMPATIBILITY:

┌────────────────────────────┬────────────┬─────────────┬──────────┐
│ Change                     │ Backward   │ Forward     │ Full     │
├────────────────────────────┼────────────┼─────────────┼──────────┤
│ Add optional field         │ ✓          │ ✓ (ignore)  │ ✓        │
│ Add required field w/def   │ ✓          │ ✗           │ ✗        │
│ Add required field no def  │ ✗          │ ✗           │ ✗        │
│ Remove optional field      │ ✗          │ ✓           │ ✗        │
│ Remove required field      │ ✗          │ ✗           │ ✗        │
│ Rename field               │ ✗          │ ✗           │ ✗        │
│ Change field type          │ ✗          │ ✗           │ ✗        │
│ Widen type (int→long)      │ ✓          │ ✗           │ ✗        │
│ Narrow type (long→int)     │ ✗          │ ✓           │ ✗        │
│ Add enum value             │ ✓          │ ✗           │ ✗        │
│ Remove enum value          │ ✗          │ ✓           │ ✗        │
│ Make field optional        │ ✓          │ ✗           │ ✗        │
│ Make field required        │ ✗          │ ✓           │ ✗        │
└────────────────────────────┴────────────┴─────────────┴──────────┘

Legend:
✓ = Compatible
✗ = Breaking
```

## Evolution Patterns

### Pattern 1: Expand-Contract (Parallel Change)

```text
EXPAND-CONTRACT PATTERN:

Phase 1: EXPAND (Add new alongside old)
┌─────────────────────────────────────────────────────────────────┐
│ Original: { userName: "alice" }                                 │
│ Expanded: { userName: "alice", username: "alice" }              │
│                                                                 │
│ Producer: writes both fields                                    │
│ Consumer: reads either field (prefers new)                      │
└─────────────────────────────────────────────────────────────────┘

Phase 2: MIGRATE (Update consumers)
┌─────────────────────────────────────────────────────────────────┐
│ Consumers updated to read: username                             │
│ Old consumers still work: userName still present                │
│                                                                 │
│ Monitor: Track usage of old field via logging                   │
└─────────────────────────────────────────────────────────────────┘

Phase 3: CONTRACT (Remove old field)
┌─────────────────────────────────────────────────────────────────┐
│ Once all consumers migrated:                                    │
│ Final: { username: "alice" }                                    │
│                                                                 │
│ Old field removed, migration complete                           │
└─────────────────────────────────────────────────────────────────┘
```

### Pattern 2: Default Values

```csharp
// Using default values for backward compatibility
// File: Contracts/OrderDto.cs

public record OrderDto
{
    public string Id { get; init; }
    public string CustomerId { get; init; }
    public List<OrderItemDto> Items { get; init; }

    // New field with default for old data
    [JsonPropertyName("priority")]
    public OrderPriority Priority { get; init; } = OrderPriority.Normal;

    // New optional field (null for old data)
    [JsonPropertyName("metadata")]
    public Dictionary<string, string>? Metadata { get; init; }

    // Computed field for backward compatibility
    [JsonIgnore]
    public decimal Total => Items?.Sum(i => i.Price * i.Quantity) ?? 0;
}

// Deserialization handles missing fields gracefully
public class OrderDtoDeserializer
{
    public OrderDto Deserialize(string json)
    {
        var options = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true,
            DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull
        };

        return JsonSerializer.Deserialize<OrderDto>(json, options)
            ?? throw new InvalidOperationException("Failed to deserialize order");
    }
}
```

### Pattern 3: Schema Versioning

```csharp
// Explicit schema versioning in payload
// File: Contracts/VersionedMessage.cs

public interface IVersionedMessage
{
    int SchemaVersion { get; }
}

public record OrderCreatedEvent : IVersionedMessage
{
    public int SchemaVersion => 2;

    public string OrderId { get; init; }
    public string CustomerId { get; init; }
    public DateTime CreatedAt { get; init; }

    // V2 additions
    public string? Source { get; init; }
    public Dictionary<string, string>? Tags { get; init; }
}

// Version-aware deserializer
public class VersionedDeserializer<T> where T : IVersionedMessage
{
    private readonly Dictionary<int, Func<string, T>> _deserializers;

    public T Deserialize(string json)
    {
        // First, peek at version
        using var doc = JsonDocument.Parse(json);
        var version = doc.RootElement.GetProperty("schemaVersion").GetInt32();

        if (_deserializers.TryGetValue(version, out var deserializer))
        {
            return deserializer(json);
        }

        // Handle unknown versions
        if (version > CurrentVersion)
        {
            // Forward compatibility: ignore unknown fields
            return DeserializeWithLenientOptions(json);
        }

        throw new SchemaVersionException($"Unsupported schema version: {version}");
    }
}
```

### Pattern 4: Union Types / OneOf

```csharp
// Using discriminated unions for evolution
// File: Contracts/PaymentMethod.cs

[JsonPolymorphic(TypeDiscriminatorPropertyName = "type")]
[JsonDerivedType(typeof(CreditCardPayment), "credit_card")]
[JsonDerivedType(typeof(BankTransferPayment), "bank_transfer")]
[JsonDerivedType(typeof(WalletPayment), "wallet")]  // Added in v2
public abstract record PaymentMethod
{
    public abstract string Type { get; }
}

public record CreditCardPayment : PaymentMethod
{
    public override string Type => "credit_card";
    public string Last4 { get; init; }
    public string Brand { get; init; }
}

public record BankTransferPayment : PaymentMethod
{
    public override string Type => "bank_transfer";
    public string BankName { get; init; }
    public string AccountLast4 { get; init; }
}

public record WalletPayment : PaymentMethod  // New type, backward compatible
{
    public override string Type => "wallet";
    public string WalletProvider { get; init; }
    public string WalletId { get; init; }
}

// Consumer handles unknown types gracefully
public class PaymentProcessor
{
    public void Process(PaymentMethod payment)
    {
        switch (payment)
        {
            case CreditCardPayment cc:
                ProcessCreditCard(cc);
                break;
            case BankTransferPayment bt:
                ProcessBankTransfer(bt);
                break;
            case WalletPayment w:
                ProcessWallet(w);
                break;
            default:
                // Forward compatibility: unknown payment type
                HandleUnknownPaymentType(payment);
                break;
        }
    }
}
```

### Pattern 5: Optional Wrapper Fields

```csharp
// Wrapping new structures in optional fields
// File: Contracts/UserProfile.cs

public record UserProfile
{
    public string Id { get; init; }
    public string Name { get; init; }
    public string Email { get; init; }

    // V1 address (flat)
    [Obsolete("Use StructuredAddress instead")]
    public string? Address { get; init; }

    // V2 address (structured, optional for backward compat)
    public StructuredAddress? StructuredAddress { get; init; }

    // Helper for consumers
    public string GetFullAddress()
    {
        if (StructuredAddress != null)
        {
            return StructuredAddress.Format();
        }
        return Address ?? string.Empty;
    }
}

public record StructuredAddress
{
    public string Street { get; init; }
    public string City { get; init; }
    public string State { get; init; }
    public string PostalCode { get; init; }
    public string Country { get; init; }

    public string Format() =>
        $"{Street}, {City}, {State} {PostalCode}, {Country}";
}
```

## Event Sourcing Schema Evolution

```text
EVENT SCHEMA EVOLUTION:

Challenges:
• Events are immutable (stored forever)
• Old events must remain readable
• New code must handle old event formats

Strategies:

1. UPCASTING
   Transform old events to new format on read
   ┌────────────────────────────────────────────────────────────┐
   │ Event Store: { type: "OrderCreated_v1", data: {...} }     │
   │                           ↓                                │
   │ Upcaster: Transform v1 → v2 format                        │
   │                           ↓                                │
   │ Application: Receives OrderCreated_v2 format              │
   └────────────────────────────────────────────────────────────┘

2. MULTIPLE EVENT HANDLERS
   Handle each version explicitly
   ┌────────────────────────────────────────────────────────────┐
   │ Handler: OnOrderCreated_v1(event) { ... }                 │
   │ Handler: OnOrderCreated_v2(event) { ... }                 │
   │                                                            │
   │ Event store dispatches to correct handler based on version│
   └────────────────────────────────────────────────────────────┘

3. COPY-TRANSFORM (Migration)
   Create new events from old
   ┌────────────────────────────────────────────────────────────┐
   │ Migration Job:                                             │
   │ 1. Read old events                                         │
   │ 2. Transform to new format                                 │
   │ 3. Write new events with new type                          │
   │ 4. Mark old events as migrated                             │
   └────────────────────────────────────────────────────────────┘
```

## Message Contract Evolution

```csharp
// AsyncAPI message evolution example
// File: Contracts/Events/OrderCreatedEvent.cs

/// <summary>
/// Order created event (schema version 3)
///
/// Version history:
/// v1: Initial version (orderId, customerId, createdAt)
/// v2: Added items array
/// v3: Added metadata, source fields
/// </summary>
[AsyncApiMessage("order.created")]
public record OrderCreatedEvent
{
    [JsonPropertyName("$schemaVersion")]
    public int SchemaVersion => 3;

    [JsonPropertyName("orderId")]
    [Required]
    public string OrderId { get; init; }

    [JsonPropertyName("customerId")]
    [Required]
    public string CustomerId { get; init; }

    [JsonPropertyName("createdAt")]
    [Required]
    public DateTime CreatedAt { get; init; }

    // Added in v2
    [JsonPropertyName("items")]
    public List<OrderItemDto>? Items { get; init; }

    // Added in v3
    [JsonPropertyName("metadata")]
    public Dictionary<string, string>? Metadata { get; init; }

    [JsonPropertyName("source")]
    public string Source { get; init; } = "unknown";
}

// Upcaster for backward compatibility
public class OrderCreatedEventUpcaster : IEventUpcaster<OrderCreatedEvent>
{
    public OrderCreatedEvent Upcast(JsonElement oldEvent, int fromVersion)
    {
        return fromVersion switch
        {
            1 => UpcastFromV1(oldEvent),
            2 => UpcastFromV2(oldEvent),
            3 => JsonSerializer.Deserialize<OrderCreatedEvent>(oldEvent),
            _ => throw new UnsupportedSchemaVersionException(fromVersion)
        };
    }

    private OrderCreatedEvent UpcastFromV1(JsonElement oldEvent)
    {
        return new OrderCreatedEvent
        {
            OrderId = oldEvent.GetProperty("orderId").GetString()!,
            CustomerId = oldEvent.GetProperty("customerId").GetString()!,
            CreatedAt = oldEvent.GetProperty("createdAt").GetDateTime(),
            Items = null,  // Not present in v1
            Metadata = null,  // Not present in v1
            Source = "legacy"  // Default for old events
        };
    }

    private OrderCreatedEvent UpcastFromV2(JsonElement oldEvent)
    {
        var v1Data = UpcastFromV1(oldEvent);
        return v1Data with
        {
            Items = oldEvent.TryGetProperty("items", out var items)
                ? JsonSerializer.Deserialize<List<OrderItemDto>>(items)
                : null
        };
    }
}
```

## Schema Registry Integration

```text
SCHEMA REGISTRY WORKFLOW:

For Kafka/Event-driven systems:

┌─────────────────────────────────────────────────────────────────┐
│                     SCHEMA REGISTRY                             │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Subject: orders-value                                     │  │
│  │ Schemas:                                                  │  │
│  │   v1: { orderId, customerId }                             │  │
│  │   v2: { orderId, customerId, items[] }                    │  │
│  │   v3: { orderId, customerId, items[], metadata }          │  │
│  │                                                           │  │
│  │ Compatibility: BACKWARD                                   │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Producer:                                                      │
│  1. Register new schema                                         │
│  2. Registry checks compatibility                               │
│  3. If compatible → assign schema ID                            │
│  4. If incompatible → reject registration                       │
│                                                                 │
│  Consumer:                                                      │
│  1. Read message with schema ID                                 │
│  2. Fetch schema from registry                                  │
│  3. Deserialize using correct schema                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Assessment Template

```markdown
# Schema Evolution Assessment: [API/Event Name]

## Current Schema

- **Name:** [Name]
- **Version:** [Current version]
- **Format:** [JSON/Protobuf/Avro]
- **Compatibility Mode:** [Backward/Forward/Full/None]

## Schema History

| Version | Date | Changes | Compatibility |
|---------|------|---------|---------------|
| [v1] | [Date] | Initial | N/A |
| [v2] | [Date] | [Changes] | [Backward/Breaking] |

## Planned Changes

| Change | Type | Compatibility | Migration Needed |
|--------|------|---------------|------------------|
| [Change] | [Add/Remove/Modify] | [Backward/Breaking] | [Yes/No] |

## Consumers

| Consumer | Current Schema | Support for New | Migration Status |
|----------|----------------|-----------------|------------------|
| [Name] | [Version] | [Yes/No] | [Status] |

## Evolution Strategy

- [ ] Expand-contract pattern applicable
- [ ] Default values defined for new fields
- [ ] Upcasters implemented for old data
- [ ] Schema registry configured
- [ ] Compatibility checks in CI

## Migration Plan

### Phase 1: Expand
- [ ] Add new fields alongside old
- [ ] Deploy producer with both fields
- [ ] Verify backward compatibility

### Phase 2: Migrate
- [ ] Update consumers to use new fields
- [ ] Monitor old field usage
- [ ] Document migration progress

### Phase 3: Contract
- [ ] Remove old fields
- [ ] Update schema documentation
- [ ] Archive old schema versions

## Rollback Plan

[Describe how to rollback if issues occur]
```

## Workflow

When evolving schemas:

1. **Assess Change**: Classify as backward/forward/breaking
2. **Choose Strategy**: Expand-contract, versioning, or breaking
3. **Implement Carefully**: Add defaults, maintain old fields
4. **Test Compatibility**: Verify old consumers can read new data
5. **Migrate Gradually**: Update consumers before removing old
6. **Document History**: Track all schema versions

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26

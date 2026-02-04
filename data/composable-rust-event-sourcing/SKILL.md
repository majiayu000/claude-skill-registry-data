---
name: composable-rust-event-sourcing
description: Expert knowledge for implementing event sourcing in Composable Rust. Use when implementing event-sourced aggregates, working with EventStore trait or PostgreSQL, designing event schemas, implementing state reconstruction, dealing with optimistic concurrency and version tracking, or questions about event sourcing, CQRS, and persistence patterns.
---

# Composable Rust Event Sourcing Expert

Expert knowledge for implementing event sourcing patterns in Composable Rust - event store design, state reconstruction, version tracking, PostgreSQL integration, and CQRS patterns.

## When to Use This Skill

Automatically apply when:
- Implementing event-sourced aggregates
- Working with `EventStore` trait or PostgreSQL event store
- Designing event schemas or event types
- Implementing state reconstruction from events
- Dealing with optimistic concurrency or version tracking
- Questions about event sourcing, CQRS, or persistence

## Event Sourcing Fundamentals

### Core Principle

**State is derived from events, not stored directly.**

```
Events (immutable log) → Replay → Current State (derived)
```

Instead of updating a record in place, we:
1. Append events to an immutable log
2. Reconstruct state by replaying events
3. Use projections for read models (CQRS)

### Benefits

- **Complete audit trail**: Every state change is recorded
- **Time travel**: Reconstruct state at any point in time
- **Event replay**: Fix bugs by replaying events with corrected logic
- **Projections**: Multiple read models from same event stream
- **Debugging**: See exactly what happened and when

### Trade-offs

- **Complexity**: More complex than CRUD
- **Storage**: Events accumulate (mitigate with snapshots)
- **Performance**: Replay can be slow (mitigate with caching/snapshots)
- **Schema evolution**: Events are immutable, need careful versioning

## EventStore Trait Pattern

### Trait Definition

```rust
pub trait EventStore: Send + Sync {
    /// Append events to the stream
    async fn append(
        &self,
        stream_id: &str,
        events: &[SerializedEvent],
        expected_version: i64,
    ) -> Result<(), Error>;

    /// Load events from the stream
    async fn load(
        &self,
        stream_id: &str,
        from_version: i64,
    ) -> Result<Vec<SerializedEvent>, Error>;

    /// Batch append for efficiency
    async fn append_batch(
        &self,
        batches: &[(String, Vec<SerializedEvent>, i64)],
    ) -> Result<(), Error>;
}
```

### SerializedEvent Pattern

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SerializedEvent {
    pub stream_id: String,
    pub version: i64,
    pub event_type: String,
    pub data: Vec<u8>,  // bincode-serialized
    pub metadata: Option<Vec<u8>>,
    pub timestamp: DateTime<Utc>,
}
```

**Key fields**:
- `stream_id`: Aggregate identifier (e.g., "order-123")
- `version`: Position in stream (for optimistic concurrency)
- `event_type`: Discriminator for deserialization
- `data`: Serialized event payload (bincode for performance)
- `timestamp`: When event occurred

## Event Design Patterns

### Pattern 1: Fat Events (Recommended for Most Cases)

Include ALL data needed to process the event:

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum OrderEvent {
    OrderPlaced {
        order_id: String,
        customer_id: String,
        items: Vec<Item>,  // ✅ Full item details
        total_amount: Decimal,
        timestamp: DateTime<Utc>,
    },
    OrderCancelled {
        order_id: String,
        customer_id: String,  // ✅ Redundant but useful
        reason: String,
        cancelled_at: DateTime<Utc>,
    },
}
```

**Benefits**:
- Self-contained (no need to join with other data)
- Consumers don't need access to other aggregates
- Projections are simple and fast
- Safe from schema changes in other aggregates

**Performance**: See `docs/event-design-guidelines.md`
- Fat events: ~15-20% slower append (still only 200-300μs)
- Fat events: ~40% faster replay (no joins needed)
- **Recommendation**: Use fat events unless you have extreme write performance needs

### Data Inclusion Checklist

When designing events, include:

**✅ Always Include:**
- **Identifiers**: All relevant IDs (order_id, customer_id, product_id, etc.)
- **Core data**: The actual data that changed
- **Metadata**: timestamp, version, correlation_id
- **Denormalized lookups**: Names/SKUs, not just IDs
  ```rust
  pub product_id: String,
  pub product_name: String,  // ✅ Denormalized
  pub product_sku: String,   // ✅ Denormalized
  ```
- **Pre-calculated values**: Totals, tax, subtotals
  ```rust
  pub subtotal: Money,
  pub tax: Money,
  pub total: Money,  // ✅ Pre-calculated
  ```
- **Complete nested objects**: Full addresses, line items
  ```rust
  pub shipping_address: Address,  // ✅ Full address, not just address_id
  pub items: Vec<LineItem>,       // ✅ Complete details
  ```

**❓ Consider Including:**
- **Causation data**: Why did this happen? (reason, triggered_by)
- **Previous state**: For debugging (previous_status, previous_total)

**❌ Don't Include:**
- **Sensitive data**: Credit cards, SSNs (use tokens instead)
- **Large binary data**: Store separately, include URL
- **Computed aggregations**: These go out of date immediately

**Rule of thumb**: If a saga or projection needs it, include it in the event.

### Pattern 2: Thin Events (For High-Write Scenarios)

Include only IDs, fetch details when needed:

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum OrderEvent {
    OrderPlaced {
        order_id: String,
        customer_id: String,  // ❌ Just ID
        item_ids: Vec<String>,  // ❌ Just IDs
        timestamp: DateTime<Utc>,
    },
}
```

**Use when**:
- Extreme write performance requirements
- Events contain large nested structures
- You have guaranteed access to reference data

**Trade-off**: Projections are slower (need to join data).

### Pattern 3: Event Versioning

Events are immutable. Handle schema changes with versioning:

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "version")]
pub enum OrderPlacedEvent {
    V1 {
        order_id: String,
        customer_id: String,
    },
    V2 {
        order_id: String,
        customer_id: String,
        items: Vec<Item},  // New field
    },
}

// Conversion logic
impl From<OrderPlacedEvent> for NormalizedOrderPlaced {
    fn from(event: OrderPlacedEvent) -> Self {
        match event {
            OrderPlacedEvent::V1 { order_id, customer_id } => {
                Self {
                    order_id,
                    customer_id,
                    items: vec![],  // Default for old events
                }
            }
            OrderPlacedEvent::V2 { order_id, customer_id, items } => {
                Self { order_id, customer_id, items }
            }
        }
    }
}
```

### Developer Experience: Automatic Event Types

Use `#[derive(Action)]` to auto-generate versioned event types:

```rust
use composable_rust_macros::Action;

#[derive(Action, Clone, Debug, Serialize, Deserialize)]
pub enum OrderAction {
    #[command]
    PlaceOrder { customer_id: String, items: Vec<Item> },

    #[event]
    OrderPlaced { order_id: String, timestamp: DateTime<Utc> },

    #[event]
    OrderCancelled { order_id: String, reason: String },
}

// Auto-generated methods:
let event = OrderAction::OrderPlaced { /* ... */ };
assert!(event.is_event());                   // ✅ true
assert_eq!(event.event_type(), "OrderPlaced.v1");  // ✅ Versioned!
```

**Benefits**:
- **Zero boilerplate**: No manual event_type() implementation
- **Automatic versioning**: `.v1` suffix added by default
- **Type safety**: Compile-time distinction between commands/events

## State Reconstruction Pattern

### Replay from Events

```rust
impl OrderState {
    /// Reconstruct state from event stream
    pub fn from_events(events: impl Iterator<Item = OrderEvent>) -> Self {
        let mut state = Self::default();
        for event in events {
            state.apply_event(event);
        }
        state
    }

    /// Apply a single event (idempotent)
    fn apply_event(&mut self, event: OrderEvent) {
        match event {
            OrderEvent::OrderPlaced { order_id, customer_id, items, timestamp, .. } => {
                self.order_id = Some(order_id);
                self.customer_id = Some(customer_id);
                self.items = items;
                self.status = OrderStatus::Placed;
                self.created_at = Some(timestamp);
                self.version += 1;
            }
            OrderEvent::OrderCancelled { reason, cancelled_at, .. } => {
                self.status = OrderStatus::Cancelled;
                self.cancelled_at = Some(cancelled_at);
                self.cancellation_reason = Some(reason);
                self.version += 1;
            }
            // Other events...
        }
    }
}
```

**Pattern**: Separate `from_events` (batch) from `apply_event` (single). Always increment version.

### With EventStore

```rust
// Load and reconstruct state
pub async fn load_order(
    order_id: &str,
    event_store: &impl EventStore,
) -> Result<OrderState, Error> {
    // Load events from store
    let serialized_events = event_store.load(order_id, 0).await?;

    // Deserialize
    let events: Vec<OrderEvent> = serialized_events
        .into_iter()
        .map(|se| bincode::deserialize(&se.data))
        .collect::<Result<Vec<_>, _>>()?;

    // Reconstruct state
    Ok(OrderState::from_events(events.into_iter()))
}
```

## Optimistic Concurrency Pattern

### Version Tracking

Every write includes expected version. Prevents lost updates:

```rust
pub async fn save_order(
    order: &OrderState,
    events: Vec<OrderEvent>,
    event_store: &impl EventStore,
) -> Result<(), Error> {
    let order_id = order.order_id.as_ref().ok_or(Error::MissingOrderId)?;

    // Serialize events
    let serialized: Vec<SerializedEvent> = events
        .into_iter()
        .enumerate()
        .map(|(i, event)| SerializedEvent {
            stream_id: order_id.clone(),
            version: order.version + i as i64 + 1,
            event_type: event_type_name(&event),
            data: bincode::serialize(&event)?,
            metadata: None,
            timestamp: Utc::now(),
        })
        .collect();

    // Append with expected version check
    event_store
        .append(order_id, &serialized, order.version)
        .await?;

    Ok(())
}
```

### Concurrency Conflict Handling

```rust
match event_store.append(stream_id, &events, expected_version).await {
    Ok(()) => {
        // Success
    }
    Err(Error::VersionConflict { expected, actual }) => {
        // Someone else wrote to this stream
        // Options:
        // 1. Retry (reload state, re-execute command)
        // 2. Fail (let client retry)
        // 3. Merge (if safe)
    }
    Err(e) => {
        // Other error
    }
}
```

**Pattern**: Always include version in append. Handle conflicts explicitly.

## PostgreSQL Event Store Implementation

### Schema Pattern

```sql
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    stream_id TEXT NOT NULL,
    version BIGINT NOT NULL,
    event_type TEXT NOT NULL,
    data BYTEA NOT NULL,
    metadata BYTEA,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(stream_id, version)
);

CREATE INDEX idx_events_stream_id ON events(stream_id);
CREATE INDEX idx_events_timestamp ON events(timestamp);
```

**Key points**:
- `UNIQUE(stream_id, version)`: Enforces version uniqueness
- `BYTEA`: Binary data for bincode (efficient)
- Indices on `stream_id` (lookup) and `timestamp` (time-based queries)

### Append Implementation

```rust
pub async fn append(
    &self,
    stream_id: &str,
    events: &[SerializedEvent],
    expected_version: i64,
) -> Result<(), Error> {
    let mut tx = self.pool.begin().await?;

    // Check current version
    let current_version: Option<i64> = sqlx::query_scalar(
        "SELECT MAX(version) FROM events WHERE stream_id = $1"
    )
    .bind(stream_id)
    .fetch_optional(&mut *tx)
    .await?;

    let current_version = current_version.unwrap_or(-1);

    if current_version != expected_version {
        return Err(Error::VersionConflict {
            expected: expected_version,
            actual: current_version,
        });
    }

    // Insert events
    for event in events {
        sqlx::query(
            "INSERT INTO events (stream_id, version, event_type, data, metadata, timestamp)
             VALUES ($1, $2, $3, $4, $5, $6)"
        )
        .bind(&event.stream_id)
        .bind(event.version)
        .bind(&event.event_type)
        .bind(&event.data)
        .bind(&event.metadata)
        .bind(event.timestamp)
        .execute(&mut *tx)
        .await?;
    }

    tx.commit().await?;
    Ok(())
}
```

**Pattern**: Use transaction. Check version. Insert all events. Commit atomically.

### Load Implementation

```rust
pub async fn load(
    &self,
    stream_id: &str,
    from_version: i64,
) -> Result<Vec<SerializedEvent>, Error> {
    let events = sqlx::query_as::<_, SerializedEvent>(
        "SELECT stream_id, version, event_type, data, metadata, timestamp
         FROM events
         WHERE stream_id = $1 AND version >= $2
         ORDER BY version ASC"
    )
    .bind(stream_id)
    .bind(from_version)
    .fetch_all(&self.pool)
    .await?;

    Ok(events)
}
```

**Pattern**: Load in order. Support from_version for incremental replay.

### Batch Append Pattern

For high-throughput scenarios:

```rust
pub async fn append_batch(
    &self,
    batches: &[(String, Vec<SerializedEvent>, i64)],
) -> Result<(), Error> {
    let mut tx = self.pool.begin().await?;

    for (stream_id, events, expected_version) in batches {
        // Check version
        let current_version: Option<i64> = sqlx::query_scalar(
            "SELECT MAX(version) FROM events WHERE stream_id = $1"
        )
        .bind(stream_id)
        .fetch_optional(&mut *tx)
        .await?;

        if current_version.unwrap_or(-1) != *expected_version {
            return Err(Error::VersionConflict { /* ... */ });
        }

        // Bulk insert events for this stream
        for event in events {
            sqlx::query(/* INSERT */)
                .bind(&event.stream_id)
                // ... other binds
                .execute(&mut *tx)
                .await?;
        }
    }

    tx.commit().await?;
    Ok(())
}
```

**Use when**: Processing multiple aggregates in one transaction (saga compensation, batch imports).

## Serialization Patterns

### Bincode for Events (Recommended)

```rust
// Serialize
let event = OrderEvent::OrderPlaced { /* ... */ };
let data = bincode::serialize(&event)?;

// Deserialize
let event: OrderEvent = bincode::deserialize(&data)?;
```

**Why bincode**:
- 5-10x faster than JSON
- 30-70% smaller payloads
- Type-safe (compile-time checks)

**Trade-off**: Not human-readable (use metadata or tooling for debugging).

### Event Type Discriminator Pattern

```rust
fn event_type_name(event: &OrderEvent) -> String {
    match event {
        OrderEvent::OrderPlaced { .. } => "OrderPlaced".to_string(),
        OrderEvent::OrderCancelled { .. } => "OrderCancelled".to_string(),
        // ...
    }
}

fn deserialize_event(event_type: &str, data: &[u8]) -> Result<OrderEvent, Error> {
    match event_type {
        "OrderPlaced" => Ok(bincode::deserialize(data)?),
        "OrderCancelled" => Ok(bincode::deserialize(data)?),
        _ => Err(Error::UnknownEventType(event_type.to_string())),
    }
}
```

**Pattern**: Store event type separately for filtering/debugging without deserializing.

## CQRS Pattern (Command Query Responsibility Segregation)

### Commands → Events → Projections

```
Command (Write) → Reducer → Events → Event Store
                              ↓
                          Event Bus
                              ↓
                         Projections (Read Models)
```

### Projection Pattern

```rust
pub trait Projection: Send + Sync {
    type Event;

    async fn handle(&mut self, event: &Self::Event) -> Result<(), Error>;
}

pub struct OrderSummaryProjection {
    database: PostgresDatabase,
}

impl Projection for OrderSummaryProjection {
    type Event = OrderEvent;

    async fn handle(&mut self, event: &Self::Event) -> Result<(), Error> {
        match event {
            OrderEvent::OrderPlaced { order_id, customer_id, total_amount, timestamp } => {
                sqlx::query(
                    "INSERT INTO order_summaries (order_id, customer_id, total, created_at)
                     VALUES ($1, $2, $3, $4)
                     ON CONFLICT (order_id) DO UPDATE
                     SET total = EXCLUDED.total"
                )
                .bind(order_id)
                .bind(customer_id)
                .bind(total_amount)
                .bind(timestamp)
                .execute(&self.database.pool)
                .await?;

                Ok(())
            }
            // Other events...
            _ => Ok(()),
        }
    }
}
```

**Pattern**: Denormalized read models. Idempotent updates (`ON CONFLICT DO UPDATE`).

### Read-After-Write Consistency

See `docs/consistency-patterns.md` for comprehensive patterns. Quick example:

```rust
// Problem: Write to event store, read from projection (eventual consistency)
store.send(OrderAction::PlaceOrder { ... }).await;
let summary = projection_db.get_order_summary(order_id).await?;  // ❌ May not be ready

// Solution: Read directly from event store or use consistency tokens
let state = event_store.load_and_reconstruct(order_id).await?;  // ✅ Always current
```

## Common Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Updating Events
```rust
// ❌ NEVER modify existing events
sqlx::query("UPDATE events SET data = $1 WHERE id = $2")
    .execute(&pool)
    .await?;
```
**Solution**: Events are immutable. Append compensating events instead.

### ❌ Anti-Pattern 2: Deleting Events
```rust
// ❌ NEVER delete events (except for GDPR compliance with care)
sqlx::query("DELETE FROM events WHERE stream_id = $1")
    .execute(&pool)
    .await?;
```
**Solution**: Append a deletion event. Use soft deletes in projections.

### ❌ Anti-Pattern 3: State in Event Store
```rust
// ❌ Don't store current state alongside events
CREATE TABLE events (
    ...
    current_state JSONB  -- ❌ Breaks event sourcing!
);
```
**Solution**: State is derived. Use snapshots if replay is slow.

### ❌ Anti-Pattern 4: Not Checking Versions
```rust
// ❌ Appending without version check
event_store.append(stream_id, &events, -1).await?;  // ❌ Ignores conflicts
```
**Solution**: Always pass expected version. Handle conflicts.

### ❌ Anti-Pattern 5: Synchronous Projections in Write Path
```rust
// ❌ Don't update projections synchronously during writes
fn reduce(...) -> Vec<Effect> {
    vec![
        Effect::Database(SaveEvent),
        Effect::Database(UpdateProjection),  // ❌ Couples write and read
    ]
}
```
**Solution**: Projections subscribe to event bus asynchronously.

## Snapshot Pattern (For Performance)

When replay becomes slow, use snapshots:

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Snapshot {
    pub stream_id: String,
    pub version: i64,
    pub state: Vec<u8>,  // Serialized state
    pub timestamp: DateTime<Utc>,
}

// Save snapshot
pub async fn save_snapshot(
    stream_id: &str,
    state: &OrderState,
    version: i64,
) -> Result<(), Error> {
    let data = bincode::serialize(state)?;

    sqlx::query(
        "INSERT INTO snapshots (stream_id, version, state, timestamp)
         VALUES ($1, $2, $3, NOW())
         ON CONFLICT (stream_id) DO UPDATE
         SET version = EXCLUDED.version, state = EXCLUDED.state"
    )
    .bind(stream_id)
    .bind(version)
    .bind(&data)
    .execute(&pool)
    .await?;

    Ok(())
}

// Load with snapshot
pub async fn load_order_optimized(
    order_id: &str,
    event_store: &impl EventStore,
) -> Result<OrderState, Error> {
    // Try to load snapshot
    let snapshot = load_snapshot(order_id).await?;

    let (mut state, from_version) = if let Some(snap) = snapshot {
        (bincode::deserialize(&snap.state)?, snap.version + 1)
    } else {
        (OrderState::default(), 0)
    };

    // Load events since snapshot
    let events = event_store.load(order_id, from_version).await?;

    // Apply remaining events
    for event_data in events {
        let event: OrderEvent = bincode::deserialize(&event_data.data)?;
        state.apply_event(event);
    }

    Ok(state)
}
```

**When to snapshot**:
- Stream has >1000 events
- Replay takes >100ms
- State is frequently accessed

**Frequency**: Every 100-1000 events, or on demand.

## Quick Reference Checklist

When implementing event sourcing:

- [ ] **Events are immutable**: Never update or delete events
- [ ] **Version tracking**: Every append includes expected version
- [ ] **Fat events**: Include all data needed (unless performance critical)
- [ ] **State reconstruction**: Implement `from_events` and `apply_event`
- [ ] **Idempotent projections**: Use `ON CONFLICT` or check processed IDs
- [ ] **Handle conflicts**: Retry or fail gracefully on version mismatches
- [ ] **Bincode serialization**: Fast, type-safe serialization
- [ ] **Event type discriminator**: Store event type for filtering
- [ ] **Snapshots**: If replay is slow (>1000 events)

## Performance Guidelines

From benchmarks in `docs/event-design-guidelines.md`:

| Operation | Fat Events | Thin Events |
|-----------|------------|-------------|
| Append | 200-300μs | 170-250μs |
| Replay (100 events) | 2-3ms | 5-7ms (with joins) |
| Projection update | 500-800μs | 1-2ms (with joins) |

**Recommendation**: Use fat events unless you have extreme write throughput requirements (>10k events/sec).

## See Also

- **Architecture**: `composable-rust-architecture.skill` - Core reducer/effect patterns
- **Sagas**: `composable-rust-sagas.skill` - Multi-aggregate coordination
- **Projections**: `docs/projections.md` - Read model patterns
- **Consistency**: `docs/consistency-patterns.md` - Read-after-write patterns
- **Guidelines**: `docs/event-design-guidelines.md` - Fat vs thin events

---

**Remember**: Events are the source of truth. State is derived. Version tracking prevents conflicts. Projections are async and eventually consistent.

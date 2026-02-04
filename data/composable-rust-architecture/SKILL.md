---
name: composable-rust-architecture
description: Expert knowledge for building event-driven systems with Composable Rust framework. Use when implementing reducers, designing state machines, working with effects, creating environment traits for dependency injection, building stores, or answering questions about core architectural patterns and the unidirectional data flow model.
---

# Composable Rust Architecture Expert

Expert knowledge for building event-driven systems using the Composable Rust framework - core architectural patterns, reducer design, effect composition, and the unidirectional data flow model.

## When to Use This Skill

Automatically apply when:
- Implementing reducers or state machines
- Designing action types or state transitions
- Working with effects or the effect system
- Creating environment traits for dependency injection
- Building stores or runtime components
- Questions about architecture or design patterns

## Core Architecture Fundamentals

### The Five Types

Every Composable Rust application is built on these five fundamental types:

1. **State**: Domain state for a feature (Clone-able, owned data)
2. **Action**: Unified type for all inputs (commands, events, cross-aggregate events)
3. **Reducer**: Pure function `(State, Action, Environment) → (State, Effects)`
4. **Effect**: Side effect descriptions (values, not execution)
5. **Environment**: Injected dependencies via traits

These compose together to create a complete system.

### The Feedback Loop (Critical Concept)

Actions flow through the system in a self-sustaining cycle:

```
External Input → Action
       ↓
Reducer: (State, Action, Env) → (New State, Effects)
       ↓
Store executes Effects
       ↓
Effects produce new Actions:
  - Effect::Future returns 0 or 1 action
  - Effect::Stream yields 0..N actions over time
       ↓
Loop back to Reducer
```

**Key Insight**: Everything is an Action. Commands are Actions. Events are Actions. External events are Actions. This creates a unified data flow where the reducer is the single source of state transitions.

## Reducer Pattern (The Heart of the System)

### Trait Definition

```rust
pub trait Reducer: Send + Sync {
    type State: Clone + Send + Sync;
    type Action: Send + Sync;
    type Environment: Send + Sync;

    fn reduce(
        &self,
        state: &mut Self::State,  // Mutable for performance
        action: Self::Action,
        env: &Self::Environment,
    ) -> SmallVec<[Effect<Self::Action>; 4]>;
}
```

### Reducer Design Principles

1. **Pure Logic**: No side effects, only state updates and effect descriptions
2. **Deterministic**: Same input always produces same output (for given env)
3. **Fast**: Business logic tests run at memory speed
4. **Explicit**: All side effects returned as `Effect` values

### Action Design Pattern

Actions represent ALL inputs to the system. Structure them by intent:

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum OrderAction {
    // Commands (external requests)
    PlaceOrder { customer_id: String, items: Vec<Item> },
    CancelOrder { order_id: String, reason: String },

    // Events (things that happened)
    OrderPlaced { order_id: String, timestamp: DateTime<Utc> },
    OrderCancelled { order_id: String, reason: String },

    // Cross-aggregate events (from other aggregates)
    PaymentCompleted { order_id: String, payment_id: String },
    InventoryReserved { order_id: String, items: Vec<Item> },

    // System events
    TimerExpired { timer_id: String },
    RetryFailed { attempt: u32, error: String },
}
```

**Pattern**: Use descriptive names that express intent. Group related actions in the same enum. Past tense for events, imperative for commands.

### State Design Pattern

State is owned, cloneable data that represents the current snapshot:

```rust
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct OrderState {
    pub order_id: Option<String>,
    pub customer_id: Option<String>,
    pub items: Vec<Item>,
    pub status: OrderStatus,
    pub created_at: Option<DateTime<Utc>>,
    pub version: i64,  // For optimistic concurrency
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum OrderStatus {
    Draft,
    Placed,
    PaymentPending,
    Confirmed,
    Cancelled,
}
```

**Pattern**: Use `Option` for fields that may not be set. Include version for event sourcing. Use enums for status/state machine states.

### Reducer Implementation Pattern

```rust
pub struct OrderReducer;

impl Reducer for OrderReducer {
    type State = OrderState;
    type Action = OrderAction;
    type Environment = OrderEnvironment;

    fn reduce(
        &self,
        state: &mut Self::State,
        action: Self::Action,
        env: &Self::Environment,
    ) -> SmallVec<[Effect<Self::Action>; 4]> {
        match action {
            // Command: Validate, update state, return effects
            OrderAction::PlaceOrder { customer_id, items } => {
                // 1. Validation
                if items.is_empty() {
                    return smallvec![Effect::None];
                }

                // 2. State update
                let order_id = format!("order-{}", env.clock.now().timestamp());
                state.order_id = Some(order_id.clone());
                state.customer_id = Some(customer_id.clone());
                state.items = items.clone();
                state.status = OrderStatus::Placed;
                state.created_at = Some(env.clock.now());

                // 3. Return effects (describe what should happen)
                smallvec![
                    Effect::Database(DatabaseEffect::Save(state.clone())),
                    Effect::PublishEvent(OrderEvent::Placed {
                        order_id,
                        customer_id,
                        items,
                    }),
                ]
            }

            // Event: Update state idempotently
            OrderAction::PaymentCompleted { order_id, payment_id } => {
                if state.order_id.as_ref() == Some(&order_id) {
                    state.status = OrderStatus::Confirmed;
                    smallvec![Effect::Database(DatabaseEffect::Save(state.clone()))]
                } else {
                    smallvec![Effect::None]
                }
            }

            // Other actions...
            _ => smallvec![Effect::None],
        }
    }
}
```

**Pattern**: Match on action type. Validate first. Update state. Return effects. Keep each arm focused.

## Effect System (Side Effects as Values)

### The Effect Enum

```rust
pub enum Effect<Action> {
    None,
    Future(Pin<Box<dyn Future<Output = Option<Action>> + Send>>),
    Stream(Pin<Box<dyn Stream<Item = Action> + Send>>),  // Phase 8
    Delay { duration: Duration, action: Box<Action> },
    Parallel(Vec<Effect<Action>>),
    Sequential(Vec<Effect<Action>>),
}
```

**Effect Variants**:
- **`None`**: No side effect needed
- **`Future`**: Async operation yielding 0 or 1 action
- **`Stream`**: Streaming operation yielding 0..N actions over time (Phase 8)
- **`Delay`**: Scheduled action after a duration
- **`Parallel`**: Execute multiple effects concurrently
- **`Sequential`**: Execute effects in order, waiting for each to complete

### Effect Patterns

**1. No side effect needed:**
```rust
use smallvec::smallvec;
smallvec![Effect::None]
```

**2. Async operation (database, HTTP, etc.):**
```rust
use composable_rust_core::async_effect;

smallvec![async_effect! {
    database.save(&data).await?;
    Some(OrderAction::OrderSaved { order_id })
}]
```

**3. Delayed action (timers, retries):**
```rust
use composable_rust_core::delay;

smallvec![delay! {
    duration: Duration::from_secs(30),
    action: OrderAction::TimerExpired { order_id }
}]
```

**4. Streaming actions (LLM tokens, WebSocket messages, etc.):**
```rust
use futures::stream;

// Stream multiple actions over time
smallvec![Effect::Stream(Box::pin(stream::iter(
    items.into_iter().map(|item| OrderAction::ItemProcessed { item })
)))]

// Async stream with delays
smallvec![Effect::Stream(Box::pin(async_stream::stream! {
    let mut response_stream = llm_client.messages_stream(request).await?;

    while let Some(chunk) = response_stream.next().await {
        yield AgentAction::StreamChunk {
            content: chunk?.delta.text
        };
    }

    yield AgentAction::StreamComplete;
}))]
```

**Use cases**: LLM token streaming, WebSocket message streams, database cursors, SSE, multi-agent progress tracking.

**5. Multiple parallel effects:**
```rust
smallvec![Effect::Parallel(smallvec![
    Effect::Database(SaveOrder),
    Effect::PublishEvent(event),
    Effect::Http(notify_customer),
])]
```

**6. Sequential effects (order matters):**
```rust
smallvec![Effect::Sequential(smallvec![
    Effect::Database(ReserveInventory),
    Effect::Database(ChargePayment),
    Effect::PublishEvent(OrderConfirmed),
])]
```

### Effect Composition Methods

```rust
// Merge multiple effects into one
let effects = vec![effect1, effect2, effect3];
let merged = Effect::merge(effects);  // Returns Effect::Parallel

// Chain effects sequentially
let chained = effect1.then(effect2);  // Returns Effect::Sequential
```

## Developer Experience: Macros & Helpers

### Derive Macros (Reduce Boilerplate)

#### `#[derive(State)]` - Version Tracking

Auto-generates version tracking methods for event-sourced state:

```rust
use composable_rust_macros::State;
use composable_rust_core::stream::Version;

#[derive(State, Clone, Debug)]
pub struct OrderState {
    pub order_id: Option<String>,
    pub items: Vec<Item>,

    #[version]  // Mark version field
    pub version: Option<Version>,
}

// Auto-generated methods:
state.version();           // Get version
state.set_version(v);      // Set version
```

**Use when**: Implementing event-sourced aggregates with optimistic concurrency.

#### `#[derive(Action)]` - Command/Event Helpers

Auto-generates type-safe helpers for distinguishing commands vs events:

```rust
use composable_rust_macros::Action;

#[derive(Action, Clone, Debug, Serialize, Deserialize)]
pub enum OrderAction {
    #[command]
    PlaceOrder { customer_id: String, items: Vec<Item> },

    #[event]
    OrderPlaced { order_id: String, timestamp: DateTime<Utc> },
}

// Auto-generated methods:
action.is_command();       // true for PlaceOrder
action.is_event();         // true for OrderPlaced
action.event_type();       // "OrderPlaced.v1" (versioned)
```

**Benefits**: Type-safe CQRS, automatic event versioning, zero boilerplate.

### Effect Helper Macros (40-60% Code Reduction)

#### `append_events!` - Event Store Operations

Simplify event appending with declarative syntax:

```rust
use composable_rust_core::append_events;

// Before (18 lines):
Effect::EventStore(EventStoreOperation::AppendEvents {
    event_store: Arc::clone(&env.event_store),
    stream_id: StreamId::new("order-123"),
    expected_version: Some(Version::new(5)),
    events: vec![event],
    on_success: Box::new(move |v| Some(Action::Success { v })),
    on_error: Box::new(|e| Some(Action::Failed { e })),
})

// After (7 lines - 60% reduction):
append_events! {
    store: env.event_store,
    stream: "order-123",
    expected_version: Some(Version::new(5)),
    events: vec![event],
    on_success: |v| Some(Action::Success { v }),
    on_error: |e| Some(Action::Failed { e })
}
```

#### `async_effect!` - Async Operations

```rust
use composable_rust_core::async_effect;

async_effect! {
    let response = http_client.get("https://api.example.com").await?;
    Some(OrderAction::ResponseReceived { response })
}
```

#### `delay!` - Scheduled Actions

```rust
use composable_rust_core::delay;

delay! {
    duration: Duration::from_secs(30),
    action: OrderAction::TimeoutExpired
}
```

**When to use**: Production code where conciseness matters. These macros have zero runtime cost.

## Environment Pattern (Dependency Injection)

### Environment Trait Pattern

Define traits for all dependencies:

```rust
// Database trait
pub trait Database: Send + Sync {
    async fn save(&self, data: &[u8]) -> Result<(), Error>;
    async fn load(&self, id: &str) -> Result<Vec<u8>, Error>;
}

// Clock trait (for deterministic testing)
pub trait Clock: Send + Sync {
    fn now(&self) -> DateTime<Utc>;
}

// HTTP client trait
pub trait HttpClient: Send + Sync {
    async fn post(&self, url: &str, body: &[u8]) -> Result<Response, Error>;
}
```

### Environment Struct Pattern

Compose traits into an environment:

```rust
pub struct OrderEnvironment<D, C, H>
where
    D: Database,
    C: Clock,
    H: HttpClient,
{
    pub database: D,
    pub clock: C,
    pub http_client: H,
}
```

### Three Implementations for Every Dependency

1. **Production**: Real implementation
```rust
pub struct PostgresDatabase { pool: PgPool }
pub struct SystemClock;
pub struct ReqwestClient;
```

2. **Test**: Fast, deterministic mocks
```rust
pub struct MockDatabase { /* ... */ }
pub struct FixedClock { time: DateTime<Utc> }
pub struct MockHttpClient { /* ... */ }
```

3. **Development**: Instrumented versions
```rust
pub struct LoggingDatabase<D> { inner: D }
pub struct MetricsDatabase<D> { inner: D }
```

**Pattern**: Use static dispatch (generics), not dynamic dispatch (trait objects), for zero-cost abstractions.

## Store Pattern (Runtime Coordination)

### Store Responsibilities

1. Hold current state
2. Execute reducer on incoming actions
3. Execute effects returned by reducer
4. Feed effect results back as new actions (feedback loop)

### Store Usage Pattern

```rust
// Create store
let environment = OrderEnvironment {
    database: PostgresDatabase::new(pool),
    clock: SystemClock,
    http_client: ReqwestClient::new(),
};

let store = Store::new(
    OrderState::default(),
    OrderReducer,
    environment,
);

// Send action
let action = OrderAction::PlaceOrder {
    customer_id: "cust-123".to_string(),
    items: vec![item1, item2],
};
store.send(action).await;

// Get current state
let state = store.state().await;
```

### Request-Response Pattern

For actions that need to wait for a result:

```rust
// Send action and wait for specific response
let result = store
    .send_and_wait_for(
        OrderAction::PlaceOrder { ... },
        |action| matches!(action, OrderAction::OrderPlaced { .. }),
        Duration::from_secs(5),
    )
    .await?;
```

## Critical Architectural Patterns

### Pattern 1: Effect-as-Value (NEVER Execute in Reducers)

**❌ WRONG - Executing side effects:**
```rust
fn reduce(...) -> SmallVec<[Effect; 4]> {
    env.database.save(state).await;  // ❌ Side effect!
    smallvec![Effect::None]
}
```

**✅ CORRECT - Returning effect description:**
```rust
fn reduce(...) -> SmallVec<[Effect; 4]> {
    smallvec![Effect::Database(SaveState)]  // ✅ Description!
}
```

**Why**: Reducers must be pure and fast. Side effects are executed by the Store runtime.

### Pattern 2: Mutable State in Reducers (Pragmatic FP)

**✅ ALLOWED - Mutating state for performance:**
```rust
fn reduce(&self, state: &mut State, ...) -> SmallVec<[Effect; 4]> {
    state.field = new_value;  // ✅ OK!
    state.items.push(item);   // ✅ OK!
}
```

**Why**: Performance matters. Tests are still deterministic because reducers are pure (no I/O).

### Pattern 3: Actions as Unified Input Type

**✅ CORRECT - Everything is an Action:**
```rust
pub enum Action {
    Command(CommandType),
    Event(EventType),
    ExternalEvent(ExternalEventType),
}
```

**Why**: Unified type simplifies the reducer signature and enables the feedback loop.

### Pattern 4: Static Dispatch for Zero Cost

**✅ CORRECT - Generic types:**
```rust
struct Store<S, A, E, R>
where
    R: Reducer<State = S, Action = A, Environment = E>
{
    reducer: R,
}
```

**❌ AVOID (unless needed) - Trait objects:**
```rust
struct Store {
    reducer: Box<dyn Reducer>,  // Runtime cost
}
```

**Why**: Static dispatch compiles to direct function calls. Zero runtime overhead.

## Common Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Side Effects in Reducers
```rust
fn reduce(...) {
    println!("Logging");  // ❌ I/O in reducer
    std::thread::sleep(Duration::from_secs(1));  // ❌ Blocking
}
```

### ❌ Anti-Pattern 2: Complex Logic in Effect Execution
```rust
// Effect execution should be simple dispatch
Effect::Database(op) => {
    // ❌ Don't put business logic here
    if should_retry && attempt < 3 {
        // Complex retry logic in executor
    }
}
```
**Solution**: Encode retry logic as actions/effects in the reducer.

### ❌ Anti-Pattern 3: Nested State Machines Without Composition
```rust
// ❌ Giant monolithic reducer
fn reduce(...) {
    match (state.order_status, state.payment_status, state.shipping_status) {
        // 100s of match arms
    }
}
```
**Solution**: Use reducer composition (see saga patterns skill).

### ❌ Anti-Pattern 4: Ignoring the Feedback Loop
```rust
use composable_rust_core::async_effect;

// ❌ Not returning actions from effects
async_effect! {
    database.save(&data).await?;
    None  // ❌ Missing feedback!
}
```
**Solution**: Return actions from futures to feed back into the system.

## Composition Patterns

### Combining Reducers

```rust
// Combine two reducers that operate on the same state
let combined = combine_reducers(reducer1, reducer2);

// Scope a reducer to a sub-state
let scoped = scope_reducer(
    child_reducer,
    |parent_state| &mut parent_state.child,
    |child_action| ParentAction::Child(child_action),
);
```

### Effect Composition

```rust
// Parallel execution
let parallel = Effect::Parallel(vec![
    effect1,
    effect2,
    effect3,
]);

// Sequential execution
let sequential = Effect::Sequential(vec![
    effect1,  // Executes first
    effect2,  // Then this
    effect3,  // Finally this
]);

// Nested composition
let complex = Effect::Parallel(vec![
    Effect::Sequential(vec![step1, step2]),
    Effect::Sequential(vec![step3, step4]),
]);
```

## Testing Patterns

### Unit Testing Reducers

```rust
#[test]
fn test_place_order() {
    // Arrange
    let env = OrderEnvironment {
        database: MockDatabase::new(),
        clock: FixedClock::new(test_time()),
        http_client: MockHttpClient::new(),
    };

    let mut state = OrderState::default();
    let action = OrderAction::PlaceOrder {
        customer_id: "cust-123".to_string(),
        items: vec![item],
    };

    // Act
    let effects = OrderReducer.reduce(&mut state, action, &env);

    // Assert
    assert_eq!(state.status, OrderStatus::Placed);
    assert_eq!(state.customer_id, Some("cust-123".to_string()));
    assert_eq!(effects.len(), 2);
    assert!(matches!(effects[0], Effect::Database(_)));
    assert!(matches!(effects[1], Effect::PublishEvent(_)));
}
```

**Key**: Reducers test at memory speed. No I/O needed.

### Integration Testing with Store

```rust
#[tokio::test]
async fn test_order_flow() {
    let env = OrderEnvironment {
        database: InMemoryDatabase::new(),
        clock: SystemClock,
        http_client: MockHttpClient::new(),
    };

    let store = Store::new(OrderState::default(), OrderReducer, env);

    // Send action
    store.send(OrderAction::PlaceOrder { ... }).await;

    // Wait for result
    let state = store.state().await;
    assert_eq!(state.status, OrderStatus::Placed);
}
```

## Architecture Decision Checklist

When designing a new feature:

- [ ] **State**: What data needs to be tracked? (Make it Clone, Serialize)
- [ ] **Actions**: What can happen? (Commands, events, external events)
- [ ] **Reducer**: What are the state transitions? (Pure function, fast)
- [ ] **Effects**: What side effects are needed? (Database, HTTP, events, delays)
- [ ] **Environment**: What dependencies? (Database, Clock, HTTP, etc.)
- [ ] **Testing**: Can I test the reducer without I/O? (Use mocks)

## Quick Reference

| Concept | Purpose | Key Trait/Type |
|---------|---------|----------------|
| State | Current snapshot | `Clone + Send + Sync` |
| Action | All inputs | `Send + Sync` (often enum) |
| Reducer | State transitions | `Reducer` trait |
| Effect | Side effect descriptions | `Effect<Action>` enum |
| Environment | Dependencies | Custom struct with trait bounds |
| Store | Runtime coordination | `Store<S, A, E, R>` |

## When in Doubt

1. **Check the feedback loop**: Does the effect produce an action?
2. **Keep reducers pure**: No I/O, just state updates and effect descriptions
3. **Use static dispatch**: Generics over trait objects
4. **Test without I/O**: Use mocks and test utilities
5. **Reference architecture**: See `specs/architecture.md` for comprehensive design

## See Also

- **Event Sourcing**: `composable-rust-event-sourcing` skill
- **Sagas**: `composable-rust-sagas` skill
- **Web Integration**: `composable-rust-web` skill
- **Testing**: `composable-rust-testing` skill
- **Rust Patterns**: `modern-rust-expert` skill

---

**Remember**: The architecture is simple but powerful. State + Action + Reducer → (New State, Effects). The Store coordinates the feedback loop. Everything else builds on this foundation.

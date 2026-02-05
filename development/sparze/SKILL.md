---
name: sparze
description: Expert guidance for building Entity Component System (ECS) applications with Sparze, a Zig ECS library. Use when working with Sparze ECS code for (1) Writing system functions with query filters, (2) Organizing systems with single responsibility and proper execution order, (3) Designing component architectures and groups, (4) Using query modifiers (Optional, Exclude, Free), (5) Managing resources and events, (6) Understanding performance trade-offs between Query/Group/SingleQuery, (7) Implementing event-driven system chains, (8) Implementing deferred commands pattern, or (9) Any other Sparze ECS development tasks.
---

# Sparze ECS Skill

Expert guidance for building high-performance Entity Component System applications with Sparze.

## Core Concepts

**World**: ECS coordinator declared with component, resource, and event types known at compile time.

```zig
const World = sparze.World(
    .{ Position, Velocity, Health },     // Components
    .{ DeltaTime, Score },               // Resources
    .{ CollisionEvent },                 // Events
    .{ struct { Position, Velocity } },  // Groups (compile-time)
);
```

**Entity**: Packed struct encoding 32-bit handle as `[version:16 | index:16]`. The lower 16 bits (`index`) select the dense slot; upper 16 bits (`version`) are a generation guard that invalidates stale handles after destruction. Access via `.index` and `.version` fields, or use helper functions `getIndex(entity)` / `getVersion(entity)`. Create with `Entity.init(index, version)`, serialize with `toInt()` / `fromInt(u32)`. **📖 Lifecycle details**: @docs/ENTITY_LIFECYCLE.md - Creation/destruction flows, version recycling, safety mechanisms

**Components**: Data attached to entities. Tag components (empty structs) use 1 bit per entity via bitset storage.

**Resources**: Global singletons accessed via `Resource(T)` or `ResourceMut(T)` injection. **CRITICAL**: Must be initialized with `initResources()` at startup; uninitialized access panics in Debug/ReleaseSafe, causes undefined behavior in ReleaseFast.

**Events**: Frame-delayed communication (1-frame latency by design). Events written in frame N are readable in frame N+1 via double-buffering. **Why delayed?** Ensures deterministic execution order and prevents circular dependencies between systems.

**📖 Detailed architecture**: @docs/ARCHITECTURE.md - Core structures, World API, memory layout, CommandBuffer internals

## System Functions

System functions receive injected parameters and **must use `commands: anytype` instead of accessing World directly**. Return type can be `void` (no errors) or `!void` (can propagate errors with `try`).

```zig
fn mySystem(
    allocator: std.mem.Allocator,           // World's allocator
    movement: Group(struct { Position, Velocity }),
    health: SingleQuery(Health),
    delta: Resource(DeltaTime),             // Read-only resource
    score: ResourceMut(Score),              // Mutable resource
    reader: EventReader(CollisionEvent),    // Read events from previous frame
    writer: EventWriter(DamageEvent),       // Write events to current frame
    commands: anytype,                      // Commands for deferred operations
) !void {
    // Implementation
}
```

### Commands API

Commands provide both **immediate** and **deferred** operations:

```zig
// === IMMEDIATE (execute now) ===
const entity = commands.createEntity();  // Returns ID immediately

// Hybrid: entity immediate, components deferred
const entity2 = try commands.createEntityWith(.{
    Position{ .x = 10, .y = 20 },
    Velocity{ .x = 1, .y = 0 },
});

// Resources
commands.setResource(DeltaTime, .{ .dt = 0.016 });
const dt = commands.getResource(DeltaTime);
const score_ptr = commands.getResourcePtrMut(Score);
try commands.initResources(.{ .delta_time = DeltaTime{ .dt = 0.016 } });

// Serialization
try commands.serializeToFile("save.dat");
try commands.deserializeFromFile("save.dat");

// === DEFERRED (execute at world.endFrame()) ===
try commands.addComponent(entity, Position, .{ .x = 0, .y = 0 });
try commands.removeComponent(entity, Velocity);
try commands.addTag(entity, Dead);
try commands.removeTag(entity, Enemy);
try commands.destroyEntity(entity);
```

**Timing rules**: Entity creation, resources, and serialization are immediate (need results now). Component/tag add/remove and entity destruction are deferred (safe during iteration).

**Why Commands?** Prevents mid-iteration structural changes that could invalidate iterators and corrupt memory. Adding/removing components during query iteration would shift array indices, causing systems to skip entities or process the same entity twice.

**📖 Detailed patterns**: @docs/SYSTEM_PATTERNS.md - Full system examples, Commands API reference, frame lifecycle, common pitfalls

## Query Filters

**Decision guide**:
- **SingleQuery**: Single component, any frequency → Simplest, fast
- **Query**: Multiple components, occasional use → No setup, flexible
- **Group**: Multiple components, every frame → Setup required, fastest

Choose based on **access frequency** and **component count**.

**📖 Comprehensive guide**: @docs/QUERY_PATTERNS.md - Decision flowchart, filter comparison, performance characteristics, component sharing patterns

### SingleQuery(Component)

**Fastest** single-component iteration. Direct array access.

```zig
fn healthSystem(query: SingleQuery(Health)) !void {
    for (query.entities, query.components) |entity, *health| {
        health.hp = @max(0, health.hp);
    }
}
```

### Query(struct { ... })

Runtime intersection for multi-component queries. No setup required. Iterates smallest component set and filters.

```zig
fn combatSystem(query: Query(struct { Position, Health, ?Shield })) !void {
    for (query.entities) |entity| {
        if (query.filter(entity)) {
            const pos = query.getComponent(entity, Position);
            const health = query.getComponentMut(entity, Health);
            const shield = query.getOptional(entity, Shield);
            // Process entity
        }
    }
}
```

**Iterator API**:
```zig
var it = query.iterator();
while (it.next()) |entity| {
    const pos = query.getComponent(entity, Position);
}
```

### Group(struct { ... })

**Fastest** multi-component iteration. Defined at compile-time in World signature. Entities organized at array start for cache-friendly access.

**Why fastest?** CPU cache loads 64 bytes per memory access. Sequential array access keeps data in cache, while Query's scattered lookups cause cache misses (100x+ slower than cache hits). Critical for hot-path systems processing 1000s of entities per frame.

```zig
// Define groups in World signature
const MovementGroup = struct { Position, Velocity };
const World = sparze.World(
    .{ Position, Velocity },
    .{},
    .{},
    .{ MovementGroup },  // Groups defined at compile-time
);

// System
fn movementSystem(group: Group(MovementGroup)) !void {
    const positions = group.getMutArrayOf(Position);
    const velocities = group.getArrayOf(Velocity);
    for (positions, velocities) |*pos, vel| {
        pos.x += vel.x;
        pos.y += vel.y;
    }
}
```

**Partial-owning groups**: Use `Free(Component)` for components owned by other groups:

```zig
// Define both groups in World signature
const PhysicsGroup = struct { Position, Free(Health) };
const CombatGroup = struct { Health, Shield };
const World = sparze.World(
    Components,
    Resources,
    Events,
    .{ PhysicsGroup, CombatGroup },
);
```

Access free components via `group.getComponent(entity, T)` instead of array access.

**Why Free()?** Prevents component ownership conflicts. Only one group can own a component (organize it at array start). Other groups needing that component must declare it Free to access via lookup. Trade-off: fast owned access + slower free lookup vs. Query overhead.

### SingleTag(Tag) / TagQuery(struct { ... })

Tag-specific query filters. Same patterns as Query but for zero-sized components.

```zig
fn enemySystem(query: TagQuery(struct { Enemy, ?Boss, Exclude(Dead) })) !void {
    for (query.entities) |entity| {
        if (query.filter(entity)) {
            if (query.hasOptional(entity, Boss)) {
                // Special boss logic
            }
        }
    }
}
```

## Query Modifiers

### Optional Components (?T)

Match entities **regardless** of component presence:

```zig
fn renderSystem(query: Query(struct { Position, ?Sprite })) !void {
    for (query.entities) |entity| {
        if (query.filter(entity)) {
            const pos = query.getComponent(entity, Position);
            if (query.getOptional(entity, Sprite)) |sprite| {
                // Render with sprite
            } else {
                // Render placeholder
            }
        }
    }
}
```

### Exclude(Component)

Filter out entities **with** the specified component:

```zig
// Process living enemies only
fn aiSystem(query: Query(struct { Enemy, Position, Exclude(Dead) })) !void {
    for (query.entities) |entity| {
        if (query.filter(entity)) {
            // Process only living enemies
        }
    }
}

// Multiple excludes
fn system(query: Query(struct {
    Position,
    Velocity,
    Exclude(Static),
    Exclude(Frozen)
})) !void { }
```

### Free(Component)

For partial-owning groups - marks component as not owned (accessed via indirection).

## System Organization

**Key principles**: One system, one responsibility. Systems that write data run before systems that read it. Use events for loose coupling between systems (1-frame latency enables clean causality chains). Group related systems by domain (physics, combat, rendering). Design for parallelization: systems accessing different components can run concurrently.

**Frame lifecycle**:
```zig
world.beginFrame();    // Swaps event buffers, clears command buffer
try world.runSystem(inputSystem);
try world.runSystem(physicsSystem);
try world.runSystem(renderSystem);
try world.endFrame();  // Flushes deferred commands
```

**CRITICAL**: Always call `endFrame()` after systems run. Skipping `endFrame()` drops all queued commands.

**Common anti-patterns to avoid**: Systems storing state (use Resources), systems calling other systems directly (use events), systems checking entity "types" (use component queries), systems doing 3+ unrelated tasks (split them).

**📖 Detailed organization patterns**: @docs/SYSTEM_PATTERNS.md - Event-driven chains, domain organization, behavioral composition, granularity guidelines

## Advanced Patterns

### Cross Product Iteration

Iterate all pairs between two queries (N×M complexity):

```zig
fn collisionSystem(
    projectiles: Query(struct { Projectile, Transform }),
    enemies: Query(struct { Enemy, Transform }),
) !void {
    var cross = projectiles.crossProduct(&enemies);
    while (cross.next()) |pair| {
        const proj_entity, const enemy_entity = pair;
        // Check collision between entities
    }
}
```

### Combination Iteration

Iterate unique pairs within a single query:

```zig
fn entityInteractionSystem(query: Query(struct { Position, Collider })) !void {
    var combos = query.combinations();
    while (combos.next()) |pair| {
        const entity1, const entity2 = pair;
        // Process unique pair
    }
}
```

### Resource Initialization

**CRITICAL**: Resources must be initialized before use. Uninitialized access:
- Debug/ReleaseSafe: Assertion failure
- ReleaseFast: Undefined behavior (zeroes)

**Why strict?** Compile-time resource pool pre-allocates memory at fixed offsets. Uninitialized slots contain garbage. Unlike components (entity-driven, tracked), resources are globally accessible without entity association, making uninitialized access impossible to detect at compile time.

```zig
// Bulk initialization (recommended for startup)
try world.initResources(.{
    .delta_time = DeltaTime{ .dt = 0.016 },
    .score = Score{ .points = 0 },
});

// Check initialization status
if (world.isResourceInitialized(OptionalConfig)) {
    const config = world.getResource(OptionalConfig);
}

// Safe checked access (returns !*const R, dereference for value)
const dt_ptr = try world.tryGetResource(DeltaTime);
const dt = dt_ptr.*;

// Unsafe direct access (zero-cost, assumes initialized)
const dt = world.getResource(DeltaTime);
```

## Performance Guidelines

**📖 Optimization strategies**: @docs/PERFORMANCE.md - Memory optimization, iteration performance, system organization, benchmarking, anti-patterns

### Memory

- Tag components use 1 bit per entity via TagStorage (98% memory reduction for sparse distributions)
- Pre-allocate with `world.getSparseSetPtrMut(Component).reserve(capacity)` before bulk operations
- Pagination: 4096 entities per page (cache-friendly, on-demand allocation)

**📖 Storage details**: @docs/STORAGE_INTERNALS.md - SparseSet/TagStorage implementation, pagination, group layout, memory calculations

### Iteration Speed

**Fastest to slowest** (performance impact):
1. **Group owned components** (`getMutArrayOf`) - 100% cache hits, vectorizable
2. **SingleQuery** - Direct array, some cache misses from entity gaps
3. **Group free components** (`getComponent`) - Lookup overhead per entity
4. **Query** - Filter overhead + scattered memory access

**Why it matters**: Cache miss = ~200 cycles. Cache hit = ~4 cycles. For 10,000 entities, Group vs Query can be 10-50x faster.

### Best Practices

- Use **Group** for hot-path queries (every frame, performance-critical)
- Use **Query** for ad-hoc or dynamic queries
- Use **SingleQuery** for single-component iterations
- Validate groups at compile time:

```zig
const MovementGroup = struct { Position, Velocity };
const RenderGroup = struct { Sprite, Layer, Free(Position) };

// Validate groups at compile-time (catches ownership conflicts)
World.validateGroups(.{ MovementGroup, RenderGroup });
```

- Define groups in World signature for compile-time organization

## Common Patterns

**Startup**: Define groups in World signature, initialize resources with `initResources()`, spawn initial entities with `createEntityWith()`.

**Component design**: POD structs for data (auto-serializable), empty structs for tags (1-bit storage), custom `Serializer` for complex types, `pub const serialized = false` to exclude from saves.

**Serialization**: `commands.serializeToFile("save.dat")` / `deserializeFromFile("save.dat")`. Entities, components, resources, and read events are saved; command buffers are not. Groups are compile-time defined and automatically populated on deserialization.

**📖 Full examples**: @docs/SYSTEM_PATTERNS.md - Startup systems, conditional processing, state machines, event chains

## Quick Reference

| Task | API |
|------|-----|
| Create entity | `commands.createEntity()` |
| Add component | `try commands.addComponent(e, T, value)` |
| Query single | `SingleQuery(Health)` |
| Query multi | `Query(struct { Position, Velocity })` |
| Fastest iteration | `Group(struct { Position, Velocity })` |
| Optional component | `Query(struct { Position, ?Sprite })` |
| Exclude entities | `Query(struct { Enemy, Exclude(Dead) })` |
| Read resource | `Resource(DeltaTime)` |
| Write resource | `ResourceMut(Score)` |
| Read events | `EventReader(CollisionEvent)` |
| Write events | `EventWriter(DamageEvent)` |
| Tag iteration | `SingleTag(Enemy)` |
| Cross product | `query1.crossProduct(&query2)` |
| Unique pairs | `query.combinations()` |

## Documentation Index

📚 **Comprehensive documentation** for deep dives:

- **@docs/ARCHITECTURE.md** - Core structures, World API, memory layout, CommandBuffer internals
- **@docs/QUERY_PATTERNS.md** - Decision flowchart, filter comparison, performance characteristics, component sharing
- **@docs/ENTITY_LIFECYCLE.md** - Creation/destruction flows, version recycling, safety mechanisms
- **@docs/STORAGE_INTERNALS.md** - SparseSet/TagStorage implementation, pagination, group layout, memory calculations
- **@docs/SYSTEM_PATTERNS.md** - Full system examples, Commands API reference, frame lifecycle, common pitfalls
- **@docs/PERFORMANCE.md** - Memory optimization, iteration performance, system organization, benchmarking, anti-patterns

---
name: game-perf
description: "Per-frame performance and GC-pressure optimization for JS/TS game code. Use when editing game loops, update functions, render passes, physics steps, particle systems, or any code that runs every frame; when diagnosing jank, frame drops, or stuttering; when allocations show up in flame graphs; or when the user mentions frame budget, hot paths, or 'feels janky'. Identifies common allocation anti-patterns (spread in loops, .map/.filter chains in update, closures captured per frame) and provides pooled / pre-allocated alternatives."
---

# Game Performance Optimization

This skill provides patterns for writing allocation-free, GC-friendly code in game loops and hot paths. Apply these patterns proactively when working on any code that executes per-frame.

## When to Activate

Trigger this skill when editing:
- Game loops, update functions, tick handlers
- Render/draw functions
- Physics update code
- AI/behavior update code
- Collision detection
- Particle systems
- Any function called 60+ times per second

## Anti-Patterns and Fixes

### 1. Spread Operator Copies

**Problem:** Spread creates a new array every call.
```typescript
// BAD: Creates new array every frame
const context = {
  enemies: [...this.enemies],
  projectiles: [...this.projectiles],
};
```

**Fix:** Pass readonly references.
```typescript
// GOOD: Zero allocation
const context = {
  enemies: this.enemies as readonly EnemyState[],
  projectiles: this.projectiles as readonly ProjectileState[],
};
```

### 2. Array.filter() in Hot Paths

**Problem:** `filter()` always creates a new array.
```typescript
// BAD: New array every call
const activeEnemies = enemies.filter(e => e.active);
```

**Fix:** In-place filtering with swap-and-truncate.
```typescript
// GOOD: Mutate in place
function filterInPlace<T>(array: T[], predicate: (item: T) => boolean): void {
  let writeIndex = 0;
  for (let i = 0; i < array.length; i++) {
    if (predicate(array[i])) {
      array[writeIndex++] = array[i];
    }
  }
  array.length = writeIndex;
}
```

### 3. Array.map() for Transformations

**Problem:** `map()` creates a new array.
```typescript
// BAD: New array every frame
const positions = enemies.map(e => e.worldPos);
steering.separation(ctx, positions, radius);
```

**Fix:** Scratch array or inline iteration.
```typescript
// GOOD: Reuse scratch array
const positionsScratch: Vec2[] = [];

function getPositions(enemies: readonly EnemyState[]): readonly Vec2[] {
  positionsScratch.length = 0;
  for (const e of enemies) {
    positionsScratch.push(e.worldPos);
  }
  return positionsScratch;
}
```

### 4. Filter + Map Chains

**Problem:** Double allocation.
```typescript
// BAD: Two new arrays
const activePositions = enemies
  .filter(e => e.active)
  .map(e => e.worldPos);
```

**Fix:** Single-pass with scratch array.
```typescript
// GOOD: Single pass, zero allocation
const scratch: Vec2[] = [];
function getActivePositions(enemies: readonly EnemyState[]): readonly Vec2[] {
  scratch.length = 0;
  for (const e of enemies) {
    if (e.active) scratch.push(e.worldPos);
  }
  return scratch;
}
```

### 5. Returning New Arrays from Utilities

**Problem:** Helper functions that return new arrays per call.
```typescript
// BAD: New array per entity per frame
function getWrappedPositions(pos: Vec2): Vec2[] {
  const positions = [pos];
  // ... add wrapped positions
  return positions;
}
```

**Fix:** Module-level scratch with readonly return.
```typescript
// GOOD: Reusable scratch buffer
const scratchPositions: Vec2[] = [];

function getWrappedPositions(pos: Vec2): readonly Vec2[] {
  scratchPositions.length = 0;
  scratchPositions.push(pos);
  // ... add wrapped positions
  return scratchPositions;
}
```

The `readonly` return type signals to callers: "consume immediately, do not store."

### 6. O(n²) Proximity Queries

**Problem:** Checking every entity against every other entity.
```typescript
// BAD: O(n²) - checks all enemies for each enemy
for (const enemy of enemies) {
  const nearby = enemies.filter(e =>
    e !== enemy && distance(e.pos, enemy.pos) < radius
  );
}
```

**Fix:** Spatial hash grid for O(n) build + O(1) queries.
```typescript
// GOOD: Build grid once, query many times
const grid = new Map<string, Entity[]>();
const CELL_SIZE = 100;

function buildGrid(entities: readonly Entity[]): void {
  grid.clear();
  for (const e of entities) {
    const key = `${Math.floor(e.pos.x / CELL_SIZE)},${Math.floor(e.pos.y / CELL_SIZE)}`;
    if (!grid.has(key)) grid.set(key, []);
    grid.get(key)!.push(e);
  }
}

function queryNearby(pos: Vec2, radius: number): readonly Entity[] {
  scratch.length = 0;
  const cx = Math.floor(pos.x / CELL_SIZE);
  const cy = Math.floor(pos.y / CELL_SIZE);
  // Check 3x3 cells
  for (let dx = -1; dx <= 1; dx++) {
    for (let dy = -1; dy <= 1; dy++) {
      const cell = grid.get(`${cx + dx},${cy + dy}`);
      if (cell) {
        for (const e of cell) {
          if (distance(e.pos, pos) < radius) scratch.push(e);
        }
      }
    }
  }
  return scratch;
}
```

### 7. Object Creation in Loops

**Problem:** Creating temporary objects inside loops.
```typescript
// BAD: New object per iteration
for (const enemy of enemies) {
  const ctx = { position: enemy.pos, velocity: enemy.vel };
  updateAI(ctx);
}
```

**Fix:** Reuse a single context object.
```typescript
// GOOD: Reuse context object
const ctx = { position: { x: 0, y: 0 }, velocity: { x: 0, y: 0 } };

for (const enemy of enemies) {
  ctx.position.x = enemy.pos.x;
  ctx.position.y = enemy.pos.y;
  ctx.velocity.x = enemy.vel.x;
  ctx.velocity.y = enemy.vel.y;
  updateAI(ctx);
}
```

## Architecture Patterns

### Build Once, Query Many
```typescript
// Per-frame setup phase
buildSpatialGrid(entities);
buildEnemyGrid(enemies);

// Per-entity query phase (many times)
for (const entity of entities) {
  const nearby = queryNearby(entity.pos, RADIUS);
  // process nearby...
}
```

### Readonly Signals Transience
When a function returns a `readonly` array, it communicates:
- The array is a scratch buffer
- Caller must consume immediately
- Do not store the reference
- Contents will change on next call

### Object Pooling for Frequent Create/Destroy
For entities created/destroyed frequently (particles, projectiles):
```typescript
class Pool<T> {
  private available: T[] = [];

  acquire(factory: () => T): T {
    return this.available.pop() ?? factory();
  }

  release(item: T): void {
    this.available.push(item);
  }
}
```

## Performance as Design Constraint

Performance isn't just an engineering concern — it constrains design decisions. Feed these constraints back into design early:

| Performance Constraint | Design Implication |
|----------------------|-------------------|
| Entity count cap (e.g., 500 at 60fps) | Limits enemy density, particle counts, projectile counts — affects encounter design |
| Spatial hash cell size | Determines minimum meaningful distance between entities — affects spacing design |
| Collision check budget | Limits simultaneous interacting entities — affects group combat design |
| Draw call budget | Limits visual complexity per frame — affects VFX and juice design |
| Memory budget | Limits world size and asset variety — affects content scope |

**Design rule:** Establish performance budgets BEFORE designing encounters, particle effects, or entity populations. A design that requires 2000 entities at 60fps on a budget that supports 500 is not a performance problem — it's a design problem. See **encounter-design** and **systems-design** for design-level responses to performance constraints.

---

## Checklist for Hot Path Code

Before committing changes to per-frame code:

- [ ] No spread operators (`[...array]`) on arrays that don't change
- [ ] No `filter()` / `map()` / `reduce()` creating new arrays
- [ ] No object literals (`{}`) or array literals (`[]`) inside loops
- [ ] Proximity queries use spatial partitioning if > 50 entities
- [ ] Scratch arrays used for temporary results
- [ ] Return types are `readonly` for scratch buffers
- [ ] Context objects are reused, not recreated

---

## Cross-References

- **encounter-design** — Performance budgets constrain encounter density and enemy counts
- **systems-design** — Performance is a system constraint that limits system interaction complexity
- **game-feel** — Juice effects (particles, shakes) must respect per-frame budgets
- **game-design** — Performance constraints should be stated as assumptions in feature proposals
- **pixi-vector-arcade** — Implementation patterns that respect these constraints

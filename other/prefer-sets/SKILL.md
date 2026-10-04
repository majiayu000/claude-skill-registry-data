---
name: prefer-sets
description: >
  Prefer Set (and Map) lookups over Array + .some/.indexOf/.includes for
  membership checks. Applies whenever writing or reviewing code that
  tests "is X one of these values". O(1) hash lookup instead of O(n)
  scan, and intent reads clearer.
---

When code answers "is this value in this collection?", use a `Set`, not an array scanned with `.some()`, `.indexOf()`, or `.includes()`.

## Rules

- Static lookup tables: declare as `const FOO = new Set<T>([...])` at module scope; query with `FOO.has(x)`. Never `ARRAY.includes(x)` or `ARRAY.some(v => v === x)`.
- Dynamic membership tracking (units on field, seen ids, active instances): keep a `Set` (or `Map` when a value is attached) and mutate with `add`/`delete`. Never `array.push` + `indexOf`/`splice` for remove.
- Predicate scans that reduce to identity comparison (`arr.some(v => v === x)`) are membership checks in disguise — convert the collection to a `Set`.
- `.indexOf(x) !== -1` / `.includes(x)` on any collection queried more than once or larger than a couple of entries: convert.

## When an array is still right

- Order matters (priority lists, learnset levels, iteration sequences).
- The collection is only ever iterated, never membership-tested.
- A genuine predicate scan where the callback does real work (`arr.some(v => v.alive && v.team === t)`) — that is filtering, not membership.
- Tuples/pairs and JSON-shaped data.

## Examples

```ts
// Bad
const PRIMAL = [Weathers.ExtremeSunny, Weathers.HeavyRain];
if (PRIMAL.includes(current)) { ... }
if (MAJOR_STATUS_CONDITIONS.some((s) => s === status)) { ... }

// Good
const PRIMAL = new Set<Weathers>([Weathers.ExtremeSunny, Weathers.HeavyRain]);
if (PRIMAL.has(current)) { ... }
if (MAJOR_STATUS.has(status)) { ... }
```

Existing exported arrays used by other modules for iteration may keep the array export but should add a Set counterpart for membership checks rather than scanning the array.

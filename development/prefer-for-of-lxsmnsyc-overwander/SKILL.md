---
name: prefer-for-of
description: Write for-of loops rather than callback-taking Array methods (map, filter, forEach, reduce, some, every, find, flatMap and the like). Applies whenever writing or editing any code in src.
---

# Prefer for-of over Array methods

Iterate with `for...of` rather than an Array method that takes a callback. A callback is a closure, which allocates and captures state, and the methods are generally slower than a plain loop. That matters here: the board draws every frame, the world is generated on every step, and the battle engine runs in real time.

## What becomes a loop

`map`, `filter`, `forEach`, `reduce`, `reduceRight`, `some`, `every`, `find`, `findIndex`, `findLast`, `findLastIndex`, `flatMap`, and `Array.from(items, mapper)`. The same goes for `forEach` on a `Map` or a `Set`.

- A chain becomes one loop: `filter` then `map` is one pass with a `continue`.
- `some`, `every` and `find` keep their short circuit with `return` or `break`.
- A callback that reads the index iterates `entries()`, or uses a counted `for`.
- `Promise.all(items.map(async ...))` becomes a loop that pushes the promises, then `Promise.all` over them.
- `new Map(items.map(...))` becomes an empty `Map` filled in the loop.

```ts
// Before
const names = party.filter((unit) => unit.alive).map((unit) => unit.name);
const fainted = party.some((unit) => unit.hp === 0);

// After
const names: string[] = [];
let fainted = false;

for (const unit of party) {
  if (unit.hp === 0) {
    fainted = true;
  }
  if (unit.alive) {
    names.push(unit.name);
  }
}
```

## What stays

- Methods that take no per-item callback: `sort`, `join`, `slice`, `includes`, `indexOf`, `concat`, `push`, `at`.
- A `sort` comparator, which no loop replaces.
- A list rendered in Solid JSX, which is `<For each={...}>` rather than an inline `map`.
- Anything that only shares a name with an Array method: a promise's `.then(...)`, a string's `.includes(...)`.

## Traps

- **Reactivity.** In a Solid component a loop hoisted out of a JSX expression, a memo or an effect stops being tracked. Keep the loop inside the same tracked scope, as the body of the accessor or memo it came from.
- **Types.** An accumulator gets its type written out (`const names: string[] = []`), so what the method inferred is still what callers see.
- **Readonly results.** Where the method's result was a fresh array the caller may keep, the loop builds a fresh array too, never a shared one.

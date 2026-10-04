---
name: typescript-game-state
description: 'TypeScript conventions for modelling this game''s state: discriminated unions for phases, branded ids, exhaustive part handling, and keeping the pure rules engine free of any renderer. Use when writing or changing types in src/game, adding a part or blueprint, or designing the shared core that both the web and a future native build consume.'
---

# Typing the game

These were written as conventions for a rewrite that had not happened. It has:
Payload's engine is `src/game/` and the views are `src/ui/`. What follows is how
it is built and how to extend it without the types drifting into decoration.

Framework decision in `docs/PLATFORM.md`, styling in
[ADR-001](../../docs/adr/0001-styling.md).

## The architectural rule the types must enforce

The rules engine must not know a renderer exists. Everything in `src/game/` is
pure TypeScript: no `document`, no `window`, no React. That is what makes it
testable, what would let the same code serve web and native, and what makes
deterministic replay possible for a future leaderboard.

It is enforced mechanically rather than by discipline. The test workflow greps
`src/game` for renderer imports and DOM access and fails the build, which is worth
more than a convention nobody remembers.

## Discriminated unions for phase, never booleans

The vanilla build carried `phase`, `busy` and `submitted` as parallel flags, which
permits states that cannot exist: busy while drafting, submitted while playing.
The phase is a union now, so the compiler forbids them:

```ts
export type Phase =
  | { readonly kind: 'drafting'; readonly offers: readonly PartKey[]; readonly selected: number | null }
  | { readonly kind: 'blueprint'; readonly offers: readonly BlueprintKey[] }
  | { readonly kind: 'playing' }
  | { readonly kind: 'runOver'; readonly won: boolean };
```

Read it with a `switch` on `kind` and a `default` that fails to compile when a
case is missed:

```ts
export function assertNever(x: never): never {
  throw new Error(`Unhandled case: ${JSON.stringify(x)}`);
}
```

That turns "add a phase" from a bug hunt into a list of compiler errors.

Model a fact once. `pendingBlueprint` exists as a separate flag rather than a
phase because a blueprint is owed *after* the current draft resolves, and encoding
it in the phase made blueprint rounds swallow the part draft.

## Exhaustive part handling

Parts are the thing most likely to be added, so make the compiler find every place
that needs updating:

```ts
export const PART_KEYS = ['weight', 'anvil', 'coil', 'prism', 'spring',
                          'wire', 'reso', 'fork', 'gate', 'bell'] as const;
export type PartKey = (typeof PART_KEYS)[number];

// Record, not Partial: adding a PartKey breaks this until it is filled in.
export const PARTS: Record<PartKey, PartDef> = { /* … */ };
```

Resolve a part's effect through a `switch` on `PartKey` with `assertNever`, never
a lookup that silently no-ops on an unknown key. A part that exists in the table
but not in the resolver should be impossible rather than merely unlikely.

## Brand the ids

Cell indices and column numbers are both `number`, and passing one where the other
belongs is the easiest bug in this codebase to write:

```ts
export type CellIndex = number & { readonly __brand: 'CellIndex' };
export type Column = number & { readonly __brand: 'Column' };
```

Cheap, zero runtime cost, and it catches `drop(cellIndex)` at compile time.

## Make illegal arguments illegal

`StartOptions` is a discriminated union on `mode`, not a flat interface with an
optional date. It used to be the latter, so a daily run compiled without a date,
fell back to an empty string, and threw "VARIANTS must not be empty" from inside
the content table, naming the wrong thing entirely. The daily's whole contract is
that the date is its identity, so the type says so.

## `readonly` everything the engine returns

The engine hands back values the caller cannot mutate. That is what keeps replay
honest and makes React's change detection reliable:

```ts
readonly board: readonly (PartKey | null)[];
readonly events: readonly DropEvent[];
```

Use `as const` on content tables so their literal types survive.

## Keep the simulation a pure function

The most valuable shape in the codebase:

```ts
export function simulateDrop(board: Board, col: Column, rules: Rules): DropResult;
```

No animation, no timers, no randomness. It returns the total plus the full ordered
list of what fired, and the renderer plays that back at whatever speed it likes.

That one signature is why the drop breakdown, the skip control, the frame-by-frame
marble playback and the placement preview were all cheap to build, and why the
whole thing is unit-testable without a browser. The preview in particular runs the
same function the real drop runs, which is what makes it impossible for it to
promise a score the game then does not pay.

If a change to the engine requires touching the renderer, the seam is in the wrong
place.

## Don't over-type the view

Branded ids and exhaustive unions belong in the engine. React components take
plain props. Resist typing CSS class strings or building a type-level design
system; ADR-001 notes that Tailwind's safety comes from editor tooling rather than
the type system, and fighting that produces ceremony without safety.

## Strict mode, and what it buys

`strict`, plus `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes`.

The first of those matters specifically here because the board is an array indexed
by computed cell positions, and it forces the `undefined` check that off-grid
maths would otherwise skip silently. The second caught a real bug: assigning
`undefined` to an optional `dateKey`, which is exactly the case the daily must not
allow. Fix those properly rather than loosening the flag.

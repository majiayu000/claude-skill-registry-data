---
name: tagged-error
description: Generate Effect TaggedError types for error handling. Use when adding new error types or improving error handling.
---

# Tagged Error Generator

Generate Effect `Data.TaggedError` types following project conventions.

## Error Location

`packages/wowlab-core/src/internal/errors/Errors.ts`

## Basic Error Template

```ts
import * as Data from "effect/Data";

export class MyError extends Data.TaggedError("MyError")<{
  readonly message: string;
  readonly cause?: unknown;
}> {}
```

## Error with Context

```ts
import * as Branded from "../schemas/Branded.js";
import * as Entities from "../entities/index.js";

export class SpellNotFound extends Data.TaggedError("SpellNotFound")<{
  readonly unitId: Branded.UnitID;
  readonly spellId: number;
}> {}

export class CastFailed extends Data.TaggedError("CastFailed")<{
  readonly reason: string;
  readonly spell: Entities.Spell.Spell;
  readonly caster?: Entities.Unit.Unit;
}> {}
```

## Error Union Types

Group related errors:

```ts
export type RotationError =
  | NoChargesAvailable
  | SpellNotFound
  | SpellOnCooldown
  | UnitNotFound;

export type CombatLogError = QueueEmpty | HandlerError | EventValidationError;
```

## Naming Conventions

- Error class: `{Thing}{Problem}` - e.g., `SpellNotFound`, `CastFailed`
- Tag: Same as class name
- Include relevant context in payload (IDs, entities, messages)

## Usage in Effects

```ts
import * as Errors from "@wowlab/core/Errors";

// Failing with error
yield *
  Effect.fail(
    new Errors.SpellNotFound({
      unitId,
      spellId,
    }),
  );

// In function signature
const cast = (
  spellId: number,
): Effect.Effect<CastResult, Errors.SpellNotFound | Errors.SpellOnCooldown> =>
  Effect.gen(function* () {
    // ...
  });
```

## Instructions

1. Identify what can fail
2. Design payload with useful context
3. Create error class with TaggedError
4. Add to union type if applicable
5. Update function signatures to include error

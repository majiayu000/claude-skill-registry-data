---
name: effect-schema
description: Define Effect schemas that are verified against domain types. Use when authoring or updating Effect Schema definitions, or when the user mentions schema/type parity, satisfies, or tsafe Equals checks.
---

# Effect Schema Type Parity

## Instructions
- Define the domain type first (prefer `interface`), then define the schema and assert parity.
- Always use `satisfies Schema.Schema<YourType, any>` on the schema.
- Add `assert<Equals<typeof YourSchema.Type, Readonly<YourType>>>()` using `tsafe`.
- If the `assert<Equals<...>>` isn't typed correctly but the `satisfies` is, you can optionally add the `_check1/_check2` assignments with `void` (see `ZerospinCommandSchema`).
- When validating unknown input against an Effect schema, prefer `validateUnknown` from `zerospin` if available.

## Example
```ts
import type { Equals } from 'tsafe';

import { Schema } from 'effect';
import { assert } from 'tsafe';

export interface IFoo {
  bar: string;
}

export const ZFoo = Schema.Struct({
  bar: Schema.String,
}) satisfies Schema.Schema<IFoo, any>;

const _check1: typeof ZFoo.Type = {} as IFoo;
const _check2: IFoo = {} as typeof ZFoo.Type;
void _check1;
void _check2;
assert<Equals<typeof ZFoo.Type, Readonly<IFoo>>>();
```

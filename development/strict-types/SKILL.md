---
name: strict-types
description: "Use when designing a type, reviewing a function signature, or writing in any typed language. Make illegal states impossible to write, brand primitives that mean different things, parse outside data at the edge, never use any or cast past the compiler, match exhaustively, derive from the schema that owns the shape. Also answers to type-system-discipline, the name the vendored typescript-best-practices skill uses for it."
disable-model-invocation: true
kind: principle
---

# Strict types

The type checker is the one reviewer that never gets tired. Use it to rule out impossible states, mixed-up primitives, and unhandled cases before the code runs. A case the types let you ignore is a runtime failure the compiler could have caught.

This applies to any typed language. For TypeScript, the `typescript-best-practices` skill and its `references/patterns.md` cover the syntax for each pattern below.

That skill is upstream text, vendored as is. When it says to apply `type-system-discipline` first, that is this file. When it points at `boundary-discipline`, read `validate-at-the-edges`.

## Never `any`

`any` is a promise that a person will catch what the compiler no longer can. Nobody keeps that promise. Model the real shape. If the shape is truly unknown, say `unknown` and narrow it. Reaching for `any` to make an error go away hides a defect instead of fixing it.

## The patterns

- **Make illegal states impossible to write.** Model variants as a sum type: discriminated unions in TypeScript, enums with payloads in Rust or Swift, sealed classes in Kotlin. Don't model state as a bag of optional fields where contradictory combinations compile. `{ completed: boolean; completedAt?: Date }` allows `completed: true` with no date, which means nothing. Derive the boolean from `completedAt !== null` or model it as `{ kind: 'open' } | { kind: 'done'; at: Date }`. If a bug ever makes you ask "wait, can this combination happen?", the type is too loose.
- **Build the type up, don't carve it down.** Start from the values you want instead of taking a looser type and adding checks. A non-empty list is a head plus a rest, not a list with a length check. A valid time range is a start plus a duration, not two timestamps you have to keep in order. Pick the shape that can't build the bad value.
- **Brand primitives that mean different things.** `UserId` and `OrderId` are both strings underneath and should never be swappable. Newtypes, opaque types, value classes, branded intersections, whatever the language has. Validate once when you create one, trust it after.
- **Outside data is untyped until parsed.** JSON, RPC payloads, CLI args, config, env vars, database rows. A parse function at every edge turns raw input into the typed model. After that, no re-checking.
- **Don't lie to the compiler.** Casts, unsafe coercions, and assertion functions that skip the check are crashes waiting for the right input. If the compiler can't prove it, prove it yourself by validating or narrowing, or admit the cast is a hazard. The cast you bury today is next week's postmortem.
- **Exhaustive matching is the compiler's job.** When you match on a sum type, adding a variant has to fail the build until every match handles it. `never` in TypeScript, unannotated `match` in Rust, sealed-class exhaustiveness in Kotlin.
- **Derive from the schema that owns the shape.** If a protobuf, OpenAPI spec, GraphQL schema, migration, or token file defines it, generate the type from that. A hand-written copy drifts.
- **Strengthen a type only where it's needed.** A null check, a runtime assertion, or a "this should never happen" throw marks the spot where a type is too weak. Push that check up into the type, then stop. The point is to track which cases each caller has to handle, not to describe the data as precisely as possible. `sum` of an empty list is zero, so it takes a plain list. `head` of an empty list has no answer, so it demands a non-empty one. Extra precision costs reuse and buys no safety.
- **Don't return null. Don't pass null.** Every null is something a caller has to remember to check. Return an empty collection, throw, or use an optional type the compiler makes them handle.

## The tests

- "Could I write a comment explaining when this combination of fields is valid?" If yes, split it into a sum type.
- "Do two arguments share a primitive type but mean different things?" Brand them.
- "Where did this `any`, this `as`, this `assertNotNull` come from?" Trace it to the edge and parse there instead.
- "If someone adds a variant next month, will the compiler tell them where to add a case?" If not, the match isn't exhaustive.
- "Is this type a copy of a shape another file owns?" Derive it.
- "Am I tightening this type to keep something from crashing, or just to be precise?" If nothing would crash, leave it plain.

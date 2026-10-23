---
name: typescript-type-safety
description: 'Use when changing TypeScript types, parsing input that enters typed code, or removing unsafe casts. Also use it when the user says "fix the types", "remove the as casts", or "make invalid states impossible". Models each valid state with types, so that invalid combinations fail to compile. Checks outside input with a type guard or a schema instead of an assertion. Not for designing module boundaries (use `design-deep-modules`).'
metadata:
  shadowclone-category: typescript
  shadowclone-section: engineering
  shadowclone-applies-when: when changing TypeScript types or input that enters typed code
---
# Represent State in TypeScript Types

## Use when

Values change together, optional fields hide different states, outside input enters typed code, or the compiler asks for an assertion. Each of these signals a missing type or a missing check.

## Gates

1. Does each valid state have its own type, such as a member of a discriminated union?
2. Does outside input enter as `unknown`, and pass a type guard or a schema before use?
3. Is the code free of `any`, non-null assertions, and casts, except `as const`?
4. Does each switch over a union handle each member, so that a new member fails to compile?
5. Does a failure that callers must handle appear in the return type?

## Process

1. Name the valid states and the moves between them. Use a discriminated union when only some field combinations are valid.
2. Keep the relation between keys and values with generics, mapped types, or a typed setter.
3. Accept outside input as `unknown`. Check it at the boundary with a schema or a type guard.
4. Narrow values with control flow, type guards, or destructuring. Make a valid absence explicit.
5. Return a type that makes callers handle each meaningful failure.
6. Run the type check, and run the tests for the boundary checks.

## Example

**Situation:** A function reads a config file and casts the parsed JSON to `Config`.
**Easy route:** Keep the cast, because the file usually has the right shape.
**Hidden cost:** A config file with one wrong field passes the cast. The program fails later, far from the cause.
**Best route:** Parse the JSON with a schema at the boundary. Return a clear error that names the field.
**Evidence:** A test with a wrong field type now fails at the boundary with "sources.git-metadata: expected boolean". The type check passed with no cast left.

## Guardrails

- Keep one source of truth for each discriminator.
- Keep literal types until a wider type is necessary.
- Put an imprecise library type in one adapter that returns a precise project type.
- Use a narrow assertion only for a fact that a runtime check cannot express, and write down why.
- Follow the stricter rules of the repository where they apply.

## Completion

- The type that now rejects the invalid state.
- One example that the compiler now rejects, with its error line.
- The type check command and the boundary test command, with their result lines.

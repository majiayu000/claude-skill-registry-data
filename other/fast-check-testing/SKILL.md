---
name: fast-check-testing
description: "Authors property-based tests in JavaScript / TypeScript using fast-check - wires `fc.assert(fc.property(arbitrary, ...))`, picks arbitraries (`fc.integer`, `fc.string`, `fc.array`, `fc.tuple`, `fc.record`), uses `.map()` / `.chain()` / `.filter()` to build domain arbitraries, and integrates with Jest / Vitest / Mocha / Jasmine / AVA / Tape. Use when a JS/TS codebase needs PBT to catch edge cases - fast-check has been used to find bugs in major libraries (`query-string`, etc.) and is trusted by Jest, Jasmine, fp-ts, Ramda."
---

# fast-check-testing

## Overview

fast-check is "a property-based testing framework for JavaScript
and TypeScript, inspired by QuickCheck"
([fast-check-readme][fcr]).

[fcr]: https://github.com/dubzzz/fast-check

It's runner-agnostic ([fast-check-overview][fco]): "Test Runner
Agnostic: Works seamlessly with Jest, Mocha, Vitest, and other
testing frameworks without special integration."

[fco]: https://fast-check.dev/

## When to use

- A JS/TS codebase has functions with non-trivial input shapes
  (parsers, serializers, validators, data transforms).
- Async code where race conditions hide; fast-check supports race
  condition detection ([fast-check-overview][fco]).
- Round-trip / metamorphic properties hold (`encode(decode(x)) === x`).
- Existing example-based tests pass but production bugs keep
  appearing in edge cases not covered.

## Install

Per [fast-check-readme][fcr]:

```bash
npm install fast-check --save-dev
# or
yarn add fast-check --dev
# or
pnpm add -D fast-check
```

## Basic property

Per [fast-check-readme][fcr], the canonical Mocha-style example:

```typescript
import fc from 'fast-check';

const contains = (text, pattern) => text.indexOf(pattern) >= 0;

describe('properties', () => {
  it('should always contain itself', () => {
    fc.assert(fc.property(fc.string(), (text) => contains(text, text)));
  });

  it('should always contain its substrings', () => {
    fc.assert(
      fc.property(fc.string(), fc.string(), fc.string(), (a, b, c) => {
        return contains(a + b + c, b);
      })
    );
  });
});
```

The shape: `fc.assert(fc.property(<arbitraries...>, (...inputs) => <predicate>))`.

The predicate returns:
- `true` → the property holds.
- `false` → the property fails.
- Throws an exception → the property fails (typical for
  `expect(...)` style assertions).

`fc.assert` runs the property with 100 generated cases by default;
on failure, fast-check shrinks to the minimal counterexample.

## Arbitraries and composite inputs

Pick arbitraries that match the input domain, build domain values
with `.map()` / `.chain()`, and assemble objects with `fc.record`.
Full catalog and combinator patterns:
[references/arbitraries.md](references/arbitraries.md). Prefer
constrained arbitraries (`fc.integer({ min: 1 })`,
`fc.emailAddress()`) over broad ones filtered down.

## Integrate with the test runner

Per [fast-check-overview][fco]: works "with major testing
frameworks including Jest, Vitest, Mocha, Jasmine, AVA, and Tape"
without special integration.

```typescript
// Jest / Vitest example
import { test, expect } from 'vitest';
import fc from 'fast-check';

test('reverse is involutive', () => {
  fc.assert(
    fc.property(fc.array(fc.integer()), (arr) => {
      expect([...arr].reverse().reverse()).toEqual(arr);
    })
  );
});
```

The assertion library (`expect`, `assert`) is the runner's; fast-check
hooks into thrown errors as failures. For async properties use
`await fc.assert(fc.asyncProperty(...))`.

## Shrinking and reproducibility

On failure fast-check prints the shrunk counterexample plus a seed;
replaying that seed reproduces the failure deterministically, and a
fixed CI seed keeps runs stable. Output format, replay, and CI seed:
[references/shrinking-and-reproducibility.md](references/shrinking-and-reproducibility.md).

## Stateful and async testing

For concurrent code use `fc.scheduler` race-condition detection; for
stateful systems use command-sequence model-based testing with
`fc.commands` / `fc.modelRun`. Both patterns:
[references/stateful-and-async.md](references/stateful-and-async.md).

## How to use

1. Install fast-check as a dev dependency (`npm install fast-check --save-dev`).
2. Identify a property that holds for all inputs (round-trip,
   invariant, metamorphic) rather than a single example.
3. Pick arbitraries matching the input domain from
   [references/arbitraries.md](references/arbitraries.md); prefer
   constrained arbitraries over `.filter()`.
4. Wire `fc.assert(fc.property(<arbitraries...>, (...inputs) => <predicate>))`;
   the predicate returns `false` or throws on violation.
5. Run under the existing runner (Jest / Vitest / Mocha / ...); for
   async use `await fc.assert(fc.asyncProperty(...))`.
6. On failure, read the shrunk counterexample and replay its seed to
   reproduce - see
   [references/shrinking-and-reproducibility.md](references/shrinking-and-reproducibility.md).
7. Verify: after fixing the cause, re-run the property and confirm it
   passes all 100 generated cases, and replay the failing seed to
   confirm the counterexample is gone; if it still fails, the fix is
   incomplete or the property itself is wrong - correct and re-run.
8. For stateful or concurrent code, escalate to model-based testing
   or `fc.scheduler` -
   [references/stateful-and-async.md](references/stateful-and-async.md).

## Worked example

A codec exposes `encode(obj)` and `decode(str)` and claims
`decode(encode(x)) === x` for every payload.

1. Model the input with a composite arbitrary
   ([references/arbitraries.md](references/arbitraries.md)):

```typescript
import fc from 'fast-check';
import { encode, decode } from './codec';

const payload = fc.record({
  id: fc.uuid(),
  count: fc.integer({ min: 0 }),
  tags: fc.uniqueArray(fc.string()),
});
```

2. Assert the round-trip under Vitest:

```typescript
test('decode reverses encode', () => {
  fc.assert(
    fc.property(payload, (x) => {
      expect(decode(encode(x))).toEqual(x);
    })
  );
});
```

3. `encode` silently drops empty-string tags, so the run fails and
   fast-check shrinks to the minimal offending input:

```
Property failed after 12 tests
{ seed: 42, path: "11:0", endOnFailure: true }
Counterexample: [{"id":"...","count":0,"tags":[""]}]
```

4. Replaying `{ seed: 42, path: "11:0" }` reproduces it every time
   ([references/shrinking-and-reproducibility.md](references/shrinking-and-reproducibility.md)).
   Fix `encode` to preserve empty tags; the property then passes all
   100 cases.

## Anti-patterns

| Anti-pattern                                                            | Why it fails                                                              | Fix |
|-------------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| Random CI seed                                                           | Property fails on CI, passes locally; hard to reproduce.                 | Fixed seed in CI (shrinking-and-reproducibility.md). |
| Heavy `.filter()` on broad arbitraries                                   | Generation slow; many cases discarded.                                   | Constrained arbitraries (arbitraries.md). |
| Asserting on specific values inside the property                         | Defeats PBT; that's an example test.                                     | Properties assert relationships; examples go elsewhere. |
| Mocking dependencies inside the property                                 | Mocks don't satisfy properties.                                          | Test pure functions; integration tests for the rest. |
| `fc.assert(fc.property(...))` without `await` for async props            | Test passes incorrectly (Promise rejected silently).                     | `await fc.assert(fc.asyncProperty(...))`. |
| Generating an `fc.string()` for an email field                            | Wastes generation budget; mostly invalid.                                | `fc.emailAddress()` (arbitraries.md). |
| One mega-property that asserts 5 things                                   | When it fails, hard to know which thing.                                  | One property per logical assertion. |

## Limitations

- **Shrinking time.** Complex arbitraries (deeply nested records)
  can take 30+ seconds to shrink. Use `endOnFailure: true` to
  short-circuit when the unshrunk case is sufficient.
- **Type inference for composite records.** TypeScript's inference
  on `fc.record({ ... })` can produce unhelpful types; explicit
  type annotations help.
- **Race-condition detection has cost.** `fc.scheduler` explores
  interleavings exhaustively; for many-task tests, runtime grows
  fast.
- **No formal proof.** 100 cases is convention; non-trivial domains
  may need more.

## References

- [fast-check-readme][fcr] - install, basic example with
  `fc.assert` / `fc.property` / `fc.string`, runner integration,
  trust list.
- [fast-check-overview][fco] - arbitraries catalog, `.map` /
  `.chain` combinators, race-condition detection, model-based
  testing, framework-agnostic positioning.
- [references/arbitraries.md](references/arbitraries.md) - arbitraries
  catalog, combinators, composite `fc.record` inputs.
- [references/stateful-and-async.md](references/stateful-and-async.md) -
  race-condition detection and model-based testing.
- [references/shrinking-and-reproducibility.md](references/shrinking-and-reproducibility.md) -
  failure output format, seed replay, CI seed.
- `hypothesis-testing` - Python
  sibling.
- `schemathesis-fuzzing` - applies fast-check-shaped PBT to API schemas.

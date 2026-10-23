---
name: proptest-testing
description: "Authors property-based tests in Rust using proptest - wires the `proptest!` macro, defines strategies (`prop::collection::vec`, type-driven `any` strategies, regex-based string strategies), uses the strategy-per-value model (vs QuickCheck's per-type) for flexible composition, and exploits proptest's automatic shrinking + persistence of failed cases (regression test artifact). Use when a Rust codebase needs PBT - pairs especially well with parsers, serializers, and any function with a structured input domain."
---

# proptest-testing

## Overview

Per [proptest-readme][pt]:

[pt]: https://github.com/proptest-rs/proptest

> "**Proptest** is a property testing framework inspired by Python's
> Hypothesis. It automatically generates test inputs and shrinks
> failures to minimal cases."

> "**Strategy-based approach**: Unlike QuickCheck, generation is
> 'defined on a per-value basis instead of per-type,' enabling
> flexible composition." ([proptest-readme][pt])

The strategy-based design is the key differentiator from Rust's
`quickcheck` crate - proptest separates the generation strategy
from the type, so multiple strategies can produce the same type
without newtype wrappers.

> "Failure persistence: Failed test cases are saved for regression
> testing." ([proptest-readme][pt])

This means a failed property test produces a `proptest-regressions/`
file checked into git; future runs replay it before generating new
cases.

## When to use

- A Rust codebase has functions with structured inputs (parsers,
  serializers, validators, encoders).
- A bug fix needs property-level prevention (not just an example
  test).
- Round-trip / invariant properties hold
  (`decode(encode(x)) == x`, `sort(sort(x)) == sort(x)`).
- A refactor needs equivalence verification (new vs old produce
  same outputs for all inputs).

## Install

In `Cargo.toml`:

```toml
[dev-dependencies]
proptest = "1"
```

Note: per [proptest-readme][pt], "the crate mainly sees passive
maintenance" - the API is stable; new development is rare.

## Basic property

Per [proptest-readme][pt]:

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn parses_valid_dates(s in "[0-9]{4}-[0-9]{2}-[0-9]{2}") {
        parse_date(&s).unwrap();
    }
}
```

The `proptest!` macro wraps a `#[test]`-style function. The
parameter declaration `s in "..."` says "generate `s` from the
regex strategy."

Per [proptest-readme][pt], one of proptest's distinguishing
features is **regex-based string generation**: `"[0-9]{4}-[0-9]{2}-[0-9]{2}"`
generates date-shaped strings without writing a custom strategy.

## Strategy catalog

| Strategy                             | Generates                              |
|--------------------------------------|----------------------------------------|
| `any::<T>()`                          | Any value of type `T` (uses default strategy) |
| `0..100i32`                           | Integers in range                       |
| `"[a-z]+"` (regex string)              | Strings matching regex                  |
| `prop::collection::vec(strategy, 0..10)` | Vec of length 0-10                  |
| `prop::collection::hash_map(k, v, 0..10)` | HashMap                          |
| `prop::collection::btree_set(s, 0..10)` | BTreeSet                              |
| `(s1, s2, s3)` (tuple)                 | Tuple of values                         |
| `Just(value)`                         | Constant                                |
| `prop_oneof![s1, s2, s3]`             | One of multiple strategies              |
| `s.prop_map(f)`                       | Transform via function                  |
| `s.prop_filter("reason", f)`          | Filter (with reason for shrinking)      |
| `s.prop_flat_map(f)`                  | Dependent generation                    |

For custom domain strategies with `prop_compose!` and the
round-trip / invariant / equivalence property patterns they feed,
see
[references/strategies-and-patterns.md](references/strategies-and-patterns.md).

## Configuration

```rust
proptest! {
    #![proptest_config(ProptestConfig {
        cases: 1000,                                  // default 256
        max_shrink_iters: 100,                       // default 1024
        ..ProptestConfig::default()
    })]

    #[test]
    fn expensive_property(x in any::<u64>()) {
        // ...
    }
}
```

Common config options:

| Field                  | Default | Use                                                  |
|------------------------|--------:|------------------------------------------------------|
| `cases`                |    256  | More for higher confidence; slower CI.               |
| `max_shrink_iters`     |   1024  | Cap shrinking time on slow tests.                    |
| `max_shrink_time`      |    0    | Time-based shrink cap (ms; 0 = unlimited).           |
| `verbose`              |    0    | 0 / 1 / 2 - verbosity level.                        |
| `failure_persistence`  |  enabled | Persist failed cases to `proptest-regressions/`.    |

## Failure persistence (the regression file)

When a property fails, proptest writes:

```
# proptest-regressions/my_module.txt
# Seeds for failure cases proptest has generated in the past.
# It is recommended to commit this file.
cc abc1234567890 # shrinks to s = "1900-02-30"
```

**Commit this file to git.** Future runs replay these seeds before
generating new cases - locks the regression in.

If the regression is no longer relevant (the bug was fixed via a
different code path that doesn't fail this case anymore), delete
the entry. Don't suppress failures; understand them first.

## CI integration

```yaml
- run: cargo test --workspace
```

That's it - proptest tests are regular `#[test]` functions wrapped
in the macro. Cargo's `--test-threads` and parallel test execution
work normally.

For deterministic CI, set the seed via env var:

```yaml
env:
  PROPTEST_SEED: 0xDEADBEEF
- run: cargo test
```

## How to use

1. Add `proptest = "1"` under `[dev-dependencies]` in `Cargo.toml`.
2. Identify a property that holds for all inputs (round-trip,
   invariant, or equivalence), not a single example.
3. Declare inputs in the `proptest! { #[test] fn ... (x in <strategy>) { ... } }`
   form; pick strategies from the catalog (regex strings, ranges,
   `prop::collection::*`).
4. For structured domain types, build a custom strategy with
   `prop_compose!` -
   [references/strategies-and-patterns.md](references/strategies-and-patterns.md).
5. Assert with `prop_assert!` / `prop_assert_eq!` (not vanilla
   `assert!`) so the shrinker sees the failure context.
6. Run `cargo test`; on failure, commit the generated
   `proptest-regressions/` file so the seed replays on later runs.
7. Tune `cases` / `max_shrink_iters` via `#![proptest_config(...)]`
   when a test is slow.

## Worked example

An `RgbColor` type exposes `to_hex()` and `from_hex()`; the team
claims `from_hex(c.to_hex()) == c` for every color.

1. Build a strategy for arbitrary colors with `prop_compose!`
   ([references/strategies-and-patterns.md](references/strategies-and-patterns.md)):

```rust
use proptest::prelude::*;

prop_compose! {
    fn rgb()(r in any::<u8>(), g in any::<u8>(), b in any::<u8>()) -> RgbColor {
        RgbColor { r, g, b }
    }
}
```

2. Assert the round-trip with `prop_assert_eq!`:

```rust
proptest! {
    #[test]
    fn hex_round_trip(c in rgb()) {
        prop_assert_eq!(RgbColor::from_hex(&c.to_hex()), c);
    }
}
```

3. `to_hex()` emits lowercase but `from_hex()` rejects it, so the
   run fails, proptest shrinks, and writes a regression file:

```
# proptest-regressions/color.txt
cc 1a2b3c4d # shrinks to c = RgbColor { r: 0, g: 0, b: 10 }
```

4. Commit `proptest-regressions/color.txt` (see Failure
   persistence). Fix `from_hex()` to accept lowercase; re-run
   `cargo test` and the property passes all 256 cases, replaying the
   saved seed first.

## Anti-patterns

| Anti-pattern                                                          | Why it fails                                                              | Fix |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| `.gitignore proptest-regressions/`                                     | Loses regression artifacts; future runs may not catch the same bug.      | Commit the directory (Failure persistence). |
| Heavy `prop_filter` on broad strategies                                 | Slow generation; many cases discarded.                                  | Constrained strategies (Strategy catalog, e.g. `1u32..100u32` instead of `any().filter`). |
| `assert!` instead of `prop_assert!` inside the macro                    | Shrinker can't see the failure context; minimal case obscured.          | Always `prop_assert!` / `prop_assert_eq!` (strategies-and-patterns.md). |
| Bare `unwrap()` inside the property without context                     | Error message is unhelpful; shrinker can't aid debugging.                | Use `prop_assert!(result.is_ok())` or `let v = result.unwrap()` after asserting. |
| `cases = 100_000` for a slow test                                       | CI never finishes; team disables.                                       | Budget appropriate to test runtime. |
| Mocking external services inside the property                          | Mocks don't satisfy properties.                                         | Test pure functions; integration tests separate. |
| Random seed in CI                                                       | Failures hard to reproduce.                                              | `PROPTEST_SEED` env var (CI integration). |

## Limitations

- **Maintenance status.** Per [proptest-readme][pt], "the crate
  mainly sees passive maintenance." Expect bug fixes but not new
  features.
- **MSRV 1.84.** Older Rust toolchains can't use the latest version.
- **Shrinking on complex types is slow.** `max_shrink_iters` /
  `max_shrink_time` cap it.
- **Async testing requires manual integration.** No native
  `proptest!` for `async fn`; wrap with `tokio::test` and
  `block_on`.
- **No race-condition detection.** Unlike fast-check's `fc.scheduler`,
  proptest doesn't model concurrent interleavings out of the box.

## References

- [pt][pt] - proptest README: strategy-based approach,
  regex-string generation, failure persistence, comparison vs
  QuickCheck, MSRV, license.
- [references/strategies-and-patterns.md](references/strategies-and-patterns.md) -
  `prop_compose!` custom strategies and round-trip / invariant /
  equivalence property patterns.
- `hypothesis-testing` - Python
  sibling proptest is inspired by.
- `fast-check-testing`,
  `jqwik-testing`,
  `quickcheck-testing` - 
  per-language siblings.

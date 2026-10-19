---
name: property-based-testing
description: >
  Design and write property-based tests (Hypothesis for Python, proptest for Rust, same ideas for
  fast-check/QuickCheck): choose properties (round-trip, oracle, invariant, idempotence,
  metamorphic, model-based), build generators that hit real input space, read shrunk
  counterexamples, pin regressions, and keep runs deterministic in CI. Use when a function has a
  large input space, parsers/serializers/codecs, normalizers, data-structure invariants, or
  stateful APIs that example-based tests keep missing. Do NOT use for coverage-guided byte-level
  crash hunting (see fuzz-testing), judging test-suite strength (mutation-testing), or ordinary
  example tests (unit-testing).
compatibility: >
  Agent Skills-compatible coding agents. Examples use Python 3.9+ with Hypothesis (verified on
  6.168.5) and Rust with proptest; concepts transfer to other QuickCheck-family libraries.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "testing, property-based-testing, hypothesis, proptest, shrinking, quickcheck, stateful-testing"
  topics: "software-development, testing, quality"
---

# Property-Based Testing

A property test states a rule that must hold for every input in a described space; the library generates many inputs, and on failure shrinks to a minimal counterexample. The skill is in choosing the rule and the input space, not in the library syntax.

Boundaries: example tests and mocking are in `unit-testing`; test-first workflow is `test-driven-development`; multi-component tests are `integration-testing`; coverage-guided crash finding on bytes is [fuzz-testing](../fuzz-testing/SKILL.md); asking "would my tests notice a bug?" is [mutation-testing](../mutation-testing/SKILL.md).

## When to use / not use

Use for: encoders/decoders, parsers and printers, sorting/merging/diffing, normalization (paths, URLs, units), arithmetic and money, data structures with invariants, caches/queues/state machines, anything where you catch yourself writing "and also test the empty case, and a unicode case...".

Not worth it for: thin glue code, UI wiring, behavior with no statable rule (then use example tests), or code where each call costs seconds (budget cases explicitly or test a smaller unit).

## Non-negotiable rules

1. A property must be a real claim, not a re-implementation of the code under test. If the assertion computes the answer the same way the function does, you test nothing.
2. Never mask failures with `assume()`/filters to make a test pass. Constrain the generator to valid inputs instead; heavy filtering triggers `filter_too_much`/`too_slow` health checks and starves coverage.
3. Every shrunk counterexample becomes a permanent explicit regression (`@example(...)` in Hypothesis; committed `proptest-regressions/` files in proptest) plus a plain unit test naming the bug.
4. Tests must be deterministic enough to debug in CI: print/keep the failure reproduction (Hypothesis `print_blob`, proptest persisted seeds) and do not commit flakes. Randomness in the code under test (time, uuid, network) must be injected, not generated.
5. No real network, filesystem outside a tmp dir, or production data in generators. Properties run thousands of times.
6. Do not weaken or delete a failing property to get green. A failing property is either a code bug or a wrong property; decide which and say why.

## Workflow

### 1. Pick the property (decision table)

| Pattern | Statement | Typical targets |
|---|---|---|
| Round trip | `decode(encode(x)) == x` | serializers, codecs, parse/print |
| Oracle / reference | `fast(x) == slow_obviously_correct(x)` | optimized algorithm vs naive version, stdlib equivalent |
| Invariant | output always satisfies a predicate (sorted, no duplicates, balanced, within bounds) | sort, dedupe, tree balancing |
| Idempotence | `f(f(x)) == f(x)` | normalize, canonicalize, format |
| Metamorphic | a known change to input gives a known change to output | `search(q + extra) subset of search(q)`, scaling, permutation |
| Commutativity / algebraic laws | `merge(a,b) == merge(b,a)`, associativity, identity | CRDTs, monoids, set ops |
| No-crash / typed errors | only documented exceptions escape | parsers on arbitrary text |
| Model-based (stateful) | random op sequences agree with a simple model | caches, stores, queues |

Start with the weakest useful property (no unexpected exception) and strengthen. Write down which pattern you are using in a comment; reviewers can then judge it.

### 2. Build the generator

- Compose from built-ins (`st.text()`, `st.integers(min_value=..)`, `st.lists(..., unique=True)`, `st.builds(...)`, `st.one_of`, `st.recursive`, `@st.composite`). In proptest use ranges, regex strings, `prop_oneof!`, `prop_compose!`, `Just`, and `.prop_map`/`.prop_flat_map`.
- Generate valid-by-construction values (e.g. build a sorted list by `sorted(draw(...))`) rather than filtering.
- Bias toward edges deliberately: empty, single element, duplicates, max/min ints, NaN/inf for floats (or exclude them with `allow_nan=False` and say why), unicode edge text, boundary sizes. Hypothesis already biases to these; check by looking at statistics (`pytest --hypothesis-show-statistics`) and `event()` labels.
- Keep sizes bounded (`max_size=`) so a test does not generate megabytes.

### 3. Write the test

```python
from hypothesis import given, example, strategies as st
from codec import encode, decode

@given(st.text())
def test_roundtrip(s):
    assert decode(encode(s)) == s
```

Run it. For a run-length codec that does not escape digits, this fails and Hypothesis shrinks to a one-character input (`'0'` in a local run): digit characters in the input collide with count digits in the output. The shrunk case is the diagnosis; fix the format (escape or length-prefix), then keep `@example("0")` and add a unit test.

### 4. Read the failure like evidence

- The minimal example is usually the smallest input that hits the same exception/assertion. Ask what is *special* about it.
- Use `note(value)` to log intermediate values only for the final failing replay; use `event(label)` to see which branches inputs reach.
- Shrinking is generator-driven: values built from simple primitives shrink well; values built via `map` of opaque functions or a custom `random`-seeded object shrink poorly. Prefer `st.builds`/`composite` and avoid drawing from a seeded RNG inside the test.
- If the failure disappears on replay it is flaky: look for time, ordering of sets/dicts, hidden global state, or `deadline` exceeded (Hypothesis reports `Flaky`/`DeadlineExceeded`). Fix the nondeterminism; do not just raise the deadline blindly.

### 5. Stateful / model-based tests

For objects with history, use `RuleBasedStateMachine` (Hypothesis) with `@initialize`, `@rule`, `@precondition`, `@invariant`, and `Bundle` for generated handles. Compare against a trivial model (dict, list). A failing run reports the shortest rule sequence. In proptest, state-machine testing lives in the separate `proptest-state-machine` crate. Keep one invariant per observable property so failures localize.

### 6. Configure for CI and local work

```python
# conftest.py
from hypothesis import settings
settings.register_profile("ci", max_examples=500, deadline=None, derandomize=True)
settings.register_profile("dev", max_examples=50)
settings.load_profile("ci")   # or choose via an env var in your own conftest
```

Facts from the Hypothesis docs: `max_examples` defaults to 100; `deadline` defaults to 200 ms; Hypothesis ships a built-in `ci` profile (derandomized, no deadline, no example database, `print_blob=True`, and `HealthCheck.too_slow` suppressed; verified against Hypothesis 6.168.5) that you can load explicitly, and `.hypothesis/examples` is the local example database. Commit regression `@example`s, not the database directory (add `.hypothesis/` to `.gitignore`). Raise `max_examples` for nightly jobs and keep PR runs small.

Rust:

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn roundtrip(s in ".*") {
        prop_assert_eq!(decode(&encode(&s)), s);
    }
}
```

Set case counts with `ProptestConfig::with_cases(n)` in the macro or the `PROPTEST_CASES` environment variable (check the crate docs for your version), and commit `proptest-regressions/` files so failures replay first.

## Worked example: normalizer

Function: `normalize_path("a//b/../c") -> "a/c"`.

1. Properties: idempotence (`n(n(p)) == n(p)`), invariant (result has no `//`, no `.` segment, no interior `..`), oracle (agrees with `posixpath.normpath` on a restricted alphabet), metamorphic (appending `/.` does not change result).
2. Generator: `st.lists(st.sampled_from(["a", "b", ".", "..", ""]), max_size=8).map("/".join)`: a tiny alphabet makes collisions (`..` after `a`) common; `st.text()` would almost never produce `..` segments.
3. Result: the oracle property finds a disagreement on leading `//` (POSIX keeps two). Decide: is your spec the POSIX one? Document the decision with an `@example("//a")` and an explicit assertion, rather than filtering it out.

## Anti-patterns

- Asserting properties that are true of any output (`isinstance(result, str)`) and calling it done.
- Generators so permissive the code under test rejects 99% of inputs early, so deep logic is never reached. Check coverage of the target function.
- Using `assume(x != 0)` or `st.integers().filter(lambda x: x != 0)` to dodge a failing input. Both silently discard cases and hide a missing precondition; a strategy that cannot produce the bad value (`st.integers(min_value=1)`) is better. First ask whether the function should reject 0 with a documented error, and if so test that error path explicitly.
- Re-seeding `random` or using `time.time()` inside a property.
- Huge `max_examples` as a substitute for a better generator.
- Treating one green run as proof. Pair with [mutation-testing](../mutation-testing/SKILL.md) to confirm the properties can fail.
- Ignoring health-check warnings; they usually point to a generator problem.

## Verification checklist

- [ ] Each property names its pattern and states a claim independent of the implementation
- [ ] Generators produce valid inputs by construction; `assume` use justified in a comment
- [ ] Known past failures are explicit examples or committed regression files
- [ ] Introduced a deliberate bug (or ran mutation testing) and saw a property fail
- [ ] CI profile is deterministic, deadline decision documented, run time within budget
- [ ] Failure output includes reproduction info (blob/seed)

## References

- [Examples: more properties and generators](references/examples.md)
- [Scenarios for evaluating this skill](references/scenarios.md)
- [Sources and provenance](references/sources.md)

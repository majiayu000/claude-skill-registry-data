---
name: property-based-testing
description: Write, review, or debug generated tests for invariants across an input domain. Use for serializers, parsers, normalizers, validators, numeric calculations, data structures, state transitions, or existing Hypothesis/fast-check/proptest failures. Choose this when examples miss meaningful combinations or boundaries—not for every test, UI verification, benchmarks, or mutation campaigns.
license: CC-BY-SA-4.0
---

# Property-Based Testing

Use generated inputs to challenge a real contract, not to repeat the implementation with random values. Adapted from Trail of Bits; see [source and changes](UPSTREAM.md).

## Find a meaningful property

Inspect the public contract, domain constraints, implementation, and existing tests. Name the observable guarantee and why it should hold. Good candidates include:

| Shape | Example |
|---|---|
| Roundtrip | Decoding an encoding recovers the supported input, allowing documented normalization. |
| Idempotence | Normalizing an already normalized value changes nothing. |
| Conservation | A transformation preserves membership, totals, or another defined quantity. |
| Ordering | Results are ordered and preserve the input multiset. |
| Oracle | An independent reference or specification agrees with the result. |
| State invariant | A documented condition holds after every valid transition sequence. |

Use only laws valid for the domain: floating-point arithmetic is not generally associative, lossy conversions are not exact inverses, and two implementations can share a bug. Pair roundtrips with independent known examples where appropriate.

If no meaningful property exists, use example tests. Exposing an existing pure boundary may help, but do not redesign an API or add an inverse solely to manufacture a property.

## Generate and check

Use the project’s existing library and test runner. Typical choices are Hypothesis for Python, fast-check for JS/TS, and proptest for Rust. Follow project dependency policy if a library is missing; do not globally install tooling or stop for repeated approvals already covered by the request.

Build valid structured inputs directly, including related fields and state preconditions. Avoid rejection-heavy filters, impossible assumptions, and generators that exercise only trivial cases. Include explicit boundary examples, then let shrinking minimize failures. Test invalid inputs against a separate documented error contract.

Read [strategy and failure guidance](references/practice.md) when designing generators or interpreting counterexamples. Keep runs bounded, isolate side effects, and record reproducible failure data.

## Interpret honestly

For a counterexample, distinguish an implementation bug, incorrect property, out-of-domain input, ambiguous contract, and harness artifact. Do not change the implementation merely to satisfy an invented law or weaken a real property to get green tests.

Run focused tests, preserve the minimized counterexample as a regression, and report the property, domain, commands, and outcome. Passing generated cases is evidence over sampled inputs—not a proof over the entire domain.

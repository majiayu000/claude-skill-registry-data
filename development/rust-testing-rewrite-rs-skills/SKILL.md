---
name: rust-testing
description: Design Rust tests that catch real regressions — unit, integration, doc, property, snapshot, and golden tests, and differential tests that prove a port matches its source. Use when writing or reviewing Rust tests, when a change lands without tests, when deciding what form a test should take, when a port needs parity evidence, or when the user asks about proptest, insta, rstest, or test coverage.
---

# Rust Testing

A test suite is a statement about which changes the team refuses to accept
silently. This skill decides *what deserves a test and in which form* — the
five ordinary forms, golden files for file-shaped artifacts, and differential
for ports — and it never decides what the code under test should look like.
Shaping the code belongs to the craft skills; whether a change is tested at
all, as a review verdict, is `/rust-code-review`.

## What a test is for

A test exists to fail when behaviour changes. A test that restates the
implementation — asserting that a getter returns the field it was handed —
fails when the code is *refactored* and passes when the behaviour breaks,
which is exactly backwards. Before writing a test, name the regression it
would catch in one sentence. If that sentence is "the code changed," do not
write the test.

## Pick the form from what is being asserted

The form follows the assertion, not the habit. The depth on each form — where
the file lives, what it can reach, what it costs — is in `TEST-DESIGN.md`; the
one-line rule for each:

| Form | Use it when |
|---|---|
| Unit test in `#[cfg(test)] mod tests` | The assertion needs private access, or the unit is a pure function with interesting edges |
| Integration test in `tests/` | The assertion is about the public API a real caller sees — imports the crate as a consumer would |
| Doc test | The example is documentation first; a doc test that is really a unit test in disguise belongs in `mod tests` |
| Property test (`proptest`) | The rule holds for a whole input space — round-trips, invariants, parser/serializer pairs |
| Snapshot test (`insta`) | The output is large, structured, and reviewed by eye — rendered text, generated code, error reports |

The corollary: a bug found in production earns a unit test at the level the
bug lived, not an end-to-end test that happens to cover it. When either a unit
or an integration test would do, take the integration test: it keeps working
through refactors of the internals. Two more forms sit outside the table: a
runnable program in `examples/`, which `cargo test --examples` compiles so
usage samples cannot rot, and fuzzing with `cargo-fuzz` for any code that
parses untrusted input, where the point is inputs nobody thought to write.

Follow the test framework the repo already uses. The tools above are
recommendations for a repo with no convention; a repo with its own harness
gets tests in that harness, not a second one beside it.

## Table-driven over copy-paste

One test, a table of cases, one loop:

```rust,ignore
#[test]
fn parses_durations() {
    let cases = [
        ("1s", Some(Duration::from_secs(1))),
        ("500ms", Some(Duration::from_millis(500))),
        ("", None),
        ("1x", None),
    ];
    for (input, expected) in cases {
        assert_eq!(parse_duration(input), expected, "input: {input:?}");
    }
}
```

The message is what makes the table pay for itself: without
`"input: {input:?}"` a failure in case three reports a line number and nothing
about which case failed. When the cases need their own test names and their
own failure lines, `rstest` expands the same table into one test per case.

## Assert on behaviour, including failure

A suite that only covers the happy path documents nothing about error
behaviour, so any error-type change passes it. Assert the error *variant* a
caller would match on, not the `Display` string — the string is not the
contract. Which variant exists at all is `/rust-errors`.

A test that computes its expectation with the same logic it is testing asserts
nothing. It is easy to miss: it looks thorough — a loop over inputs building
the expected value with the function under test, or a constant from the same
formula. The expected value is human-written, or from an independent source:
a reference implementation, a published vector, a hand-worked example.

## Determinism is a property of the test, not the machine

Seed every generator explicitly, inject time and randomness rather than
reading the clock, and never touch the network in a unit or integration test.
A flaky test is deleted or fixed the day it flakes; a suite with one tolerated
flake teaches everyone to re-run instead of read.

## Coverage is a signal, not a target

`cargo llvm-cov` finds branches worth testing; a percentage gate produces
tests that touch lines, not verified behaviour. Do not chase the number.

## Differential testing for ports

When a Rust implementation replaces an existing one, the strongest available
evidence is both running over the same inputs and agreeing. The three harness
shapes — recorded corpus, side-by-side execution, `proptest` over a shared
generator — with their tradeoffs, and the rules for normalizing and recording
differences, are in `DIFFERENTIAL-TESTING.md`. The parity contract that says
which differences are acceptable belongs to `/port-to-rust`; this skill
supplies the mechanism, not the contract.

## Deferrals

Error-variant design is `/rust-errors`. Testing `unsafe` code means Miri,
which is `/unsafe-rust`. Async test flavours, time control, and why a
`#[tokio::test]` with a real sleep is a flake generator are `/async-rust`.
`loom` covers the concurrency test that explores interleavings rather than
hoping for one — `/rust-concurrency`. `criterion` covers the test that is
really a benchmark — `/rust-performance`. Whether a change *needs* a test
at all, as a review verdict, is `/rust-code-review`.

## Verification

```bash
cargo test --all-features
cargo test --doc
cargo clippy --all-targets --all-features   # add -- -D warnings only if the repo has no lint config
```

Test every feature combination that is meant to work, not only the
all-features build (`cargo hack` can walk them), and run the suite on each
platform that has its own code paths: a `cfg(windows)` branch is untested
until something runs on Windows.

Clippy runs at the lint level configured in the repo — a repo with a
`clippy.toml` or its own lint attributes keeps them, and a stricter level
never goes on top.

A new test must be observed failing before it is accepted: comment out the
fix, or invert the assertion, and confirm the failure message names the actual
problem. A test never seen red is a test that may assert nothing.

---
name: memory-ordering
description: The Release/Acquire pair the ring rests on, and what a change to any atomic ordering owes in evidence. Use when touching any Ordering in ring or kernel, when adding an atomic, when writing or changing a litmus test, and when a concurrency test passes locally and you are about to conclude it is correct.
---

# Memory ordering

The ring's correctness rests on one `Release` store and one `Acquire` load.
`Relaxed` there passes every test on an x86 laptop and corrupts data on AArch64.

That sentence is the whole skill. Everything below follows from it.

## What a change to an ordering owes

A litmus test that **fails under the weaker ordering**. Not a test that passes
under the stronger one — every test passes under the stronger one, which is why
a green run proves nothing and why this is stated as an obligation rather than a
suggestion. `CONTRIBUTING.md` requires it.

The test lives in `ring/tests/litmus.rs` and runs in release mode on AArch64 in
CI. Write it as a stress test with a stated repeat count and a stated failure
signature, and check that it actually goes red when you weaken the ordering, by
weakening the ordering and running it before you commit either.

## Where the coverage ends

The litmus job is stress, not model checking. RustMC is what actually explores
what RC11 permits, and it is `E0-P16`, open — M5 arrived at `E0-B12` and the
checker did not, so "lands at M5" is a sentence that stopped being true. Until
it exists the AArch64 unit tests plus the litmus job are the coverage, and the
gap is real — say so rather than implying the ring is verified.

Two things about that gap are now settled rather than open. The checker cannot
share this tree's toolchain — the pinned rustc bundles LLVM 22.1.8 and RustMC
requires LLVM 21 — so it brings its own, under RFC 0022. And it will not run the
litmus tests: `cargo rustmc test` explores a crate's test targets exhaustively,
so a model check needs its own small tests, two threads and a couple of entries,
beside the stress ones rather than instead of them. If you are writing a new
`Release`/`Acquire` pair, you owe a stress test today and a small exhaustible
test whenever `E0-P16` lands; write the stress one so that shrinking it later is
a matter of constants rather than a rewrite.

The suite has three deliberate defects behind cargo features, and **one of them
is a gate**: `mutate-no-doorbell-fence`, on the **x86-64** runner only. The two
that weaken a publishing store to `Relaxed` were gates for one run and the suite
*passed* with them on, on the arm runner. Do not re-add them as gates without new
evidence — that result is the measured size of the gap, and it is what `E0-P16`
exists to close.

**Which runner catches a defect is a property of which reordering it depends on,
not of how serious it is.** Store-load is the one reordering total store order
performs and the one AArch64 forbids — `stlr`/`ldar` are RCsc, so a
Store-Release followed by a Load-Acquire is already ordered there. So the
doorbell fence is caught on x86 and invisible on arm, which is the exact inverse
of every other ordering in this crate. Check which machine can see a defect
before deciding which job should assert it.

The rule that follows: if you weaken an ordering and the litmus suite stays
green, **you have learned nothing**. Green there is not evidence the ordering
was unnecessary; it is evidence the suite is a sampler.

## Reviewing concurrent code here

- x86-64 total store order hides the entire class of bug this code is exposed
  to. A result from a local x86 run is not evidence about ordering.
- Name the pairing. Every `Release` has an `Acquire` that it synchronises with;
  if you cannot point at the partner, the ordering is decoration.
- `SeqCst` used to avoid thinking about the pairing is a finding. It is slower
  and it hides which invariant was intended.
- Cursors on the same cache line are the first suspect when a submission
  benchmark comes in high — `claims/0001-ring-submit-latency.toml` records that
  as its own first debugging step.

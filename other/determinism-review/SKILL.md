---
name: determinism-review
description: The determinism policy of RFC 0004, and how to satisfy it rather than route around it. Use when writing or reviewing any Rust in this workspace that reads a clock, draws randomness, orders concurrent work, iterates a collection, or allocates — and whenever a change adds an entry to DETERMINISM_ALLOW in xtask.
---

# Determinism

The contract is one line: `(seed, commit_hash) -> byte-identical execution,
always`. Everything else in the test apparatus — whole-system simulation, fault
injection, the claims registry — rests on it, and it is the one property that
cannot be retrofitted. RFC 0004.

## The rule

Nothing observes time, randomness or ordering except through `f_env::Env`.

`cargo xtask lint-determinism` greps for the direct sources and fails the build
on any of them outside an allow-listed path:

| Construct | What to do instead |
| --- | --- |
| `rdtsc` | `env.now()` — the one legitimate site is `kernel/src/arch/x86_64/mod.rs` |
| `SystemTime::now`, `Instant::now` | read time through `Env` |
| `thread_rng`, `random()` | draw from `Env` |
| `HashMap::new`, `HashSet::new` | `BTreeMap`, `BTreeSet` — hash iteration order is seeded per process |
| `f32`, `f64` | an integer, or a fixed point with its scale in the name — IEEE 754 fixes the four operations and nothing else, so `libm`, fused multiply-add and NaN payloads differ between the x86-64 and AArch64 jobs |

## When you are about to add an allow-list entry

This is the moment the policy either holds or quietly stops meaning anything, so
treat it as a design decision rather than a build fix.

1. Say why the code must observe the source directly, in terms of what `Env`
   cannot give it. "Convenience" and "it is only a test" are not reasons; tests
   are exactly where a seeded clock matters most.
2. Scope the entry to the narrowest path that works — a file, not a directory,
   unless the whole directory has the same argument behind it.
3. Write the revisit condition into the reason itself, the way the `bench/`
   entry does: it says which milestone gives the harness a hardware `Env` and
   therefore when the exemption should disappear.
4. Put the entry and the code in the same diff and expect a reviewer to say so.
   `REVIEW.md` names this as the most common way the policy erodes.

## What this does not cover

The lint is textual. It cannot see nondeterminism that arrives through a
dependency, through pointer addresses, through uninitialised memory, or through
a `BTreeMap` keyed on something that is itself nondeterministic. Those are
review's job, and the tell is always the same: run the same seed twice and
diff the trace.

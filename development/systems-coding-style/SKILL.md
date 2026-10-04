---
name: systems-coding-style
description: Write and review C, C++, Rust, and low-level systems code with a small, idiomatic, professional style. Use for implementation, refactoring, or review where unnecessary abstraction, allocation, cleverness, or explanatory comments should be avoided.
---

# Systems coding style

Match the repository's language version, build system, formatting, error model, and established conventions before introducing a new pattern.

## Code

- Prefer the smallest direct solution that makes ownership, lifetime, state, and failure behavior clear.
- Keep changes narrow. Do not modernize unrelated code or mass-format surrounding files.
- Avoid speculative abstractions, unnecessary wrappers, premature generic code, clever metaprogramming, and hidden allocation.
- Prefer explicit data flow and ordinary language constructs over compressed or surprising code.
- Preserve public interfaces unless the requested behavior requires a change.
- Make resource ownership and cleanup deterministic. Treat integer overflow, bounds, alignment, aliasing, concurrency, ABI, and error propagation as design concerns.

For C, use explicit ownership conventions, checked sizes, structured cleanup, and return values that cannot silently discard failure.

For C++, prefer RAII, value semantics, scoped ownership, standard-library facilities, and compile-time constraints when they simplify the code. Do not force a newer language feature than the project supports.

For Rust, prefer borrowing over cloning, precise types over flags, ordinary `Result` propagation, and small safe interfaces around unavoidable `unsafe` code. State every unsafe invariant next to the unsafe boundary.

## Comments

Write comments only for information the code cannot carry: invariants, ownership exceptions, synchronization rules, unsafe assumptions, hardware or protocol constraints, compatibility requirements, and non-obvious tradeoffs.

Never narrate control flow, restate types or names, add decorative section banners, or comment every function for consistency. Prefer a clearer name or smaller function when that removes the need for explanation.

## Verification

Use the repository's formatter and narrowest relevant compiler, test, linter, or static-analysis command. Keep warnings clean. For boundary-sensitive changes, test empty, maximum, malformed, partial, overflow, and failure paths that are relevant to the code.

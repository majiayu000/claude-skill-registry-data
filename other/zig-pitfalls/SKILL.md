---
name: zig-pitfalls
description: "Use when writing or reviewing Zig code: error unions and defer or errdefer cleanup, choosing and passing allocators and leak-checking them in tests, comptime evaluation limits, build.zig steps and test wiring, and staying correct across Zig releases, which change fast."
---

# zig-pitfalls

Step 5 of the pipeline (`WORKFLOW.md`), for Zig changes. The premise: **Zig has no hidden allocator, no hidden
cleanup and no stable release train, so the three bugs that matter are a leak on an error path, an allocator
nobody owns, and an example that compiled on the previous release**. Assertions and bounds that apply to Zig
and to the other systems languages are `systems-assertion-discipline`; generic test smells are
`testing-anti-patterns`.

## When
- A Zig function returns an error union, or acquires something that must be released.
- Memory is allocated, an allocator is chosen, or a test touches the heap.
- A generic function, a compile-time table or a `comptime` block is written.
- A `build.zig` is written or a test is wired into the build.
- A Zig version is bumped, or code or an example from another release is pasted in.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Errors and defer: try, catch, unreachable, errdefer, error sets | a fallible function or a cleanup path is written | [`01-errors-defer.md`](./references/01-errors-defer.md) |
| 2 | Allocators and ownership: who allocates, which allocator, leak checks, lifetimes | memory is allocated or a pointer outlives a scope | [`02-allocators.md`](./references/02-allocators.md) |
| 3 | Comptime: generics, compile-time evaluation, the branch quota | a `comptime` parameter or block is written or a compile-time limit is hit | [`03-comptime.md`](./references/03-comptime.md) |
| 4 | Build, tests and release drift: steps, optimisation modes, the 0.17.0 breaking changes | `build.zig` is touched, tests are wired, or a toolchain is bumped | [`04-build-test-drift.md`](./references/04-build-test-drift.md) |

## Output / checkpoint
Every acquire has its release written next to it, every allocation names its owner and its allocator, and
`zig build test` (or the project's test step) was actually run on the pinned toolchain. A Zig claim in the
change description that was not checked against that toolchain's documentation is not verified.

## Guardrails
- Never copy a Zig example from a tutorial, an older release or an AI answer without compiling it on the pinned
  toolchain (§4.4).
- Never use `catch unreachable` for an error that can happen at run time (§1.1).
- Never reach for `anyerror` or an inferred error set where an explicit set is possible (§1.3).
- Versions: each rule names the Zig version of the page it came from. Nothing was compiled or run while
  writing this block.

## Origin
Rewritten from the Zig 0.17.0 language reference, the 0.17.0 release notes and the build system page on
ziglang.org (MIT-licensed documentation and code), read 2026-10-08. Overlaps with `skills/zig-conventions` (2026-10-19); cross-referenced, not merged. 🟡:
never run by us; open points are in [`references/origin.md`](./references/origin.md).

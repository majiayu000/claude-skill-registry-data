---
name: rust-expert
description: This skill should be used when the user is writing, reviewing, debugging, or architecting Rust code. Detects edition and toolchain from the project. Provides expert critique covering ownership, error handling, unsafe review, async correctness, trait design, type system patterns, performance, SOLID principles, and Cargo/workspace practices. Use when the user asks "critique my Rust code", "review this module", "fix borrow checker error", "is this unsafe sound", "design error types", "optimize this function", "review async code", "structure my workspace", "why is the borrow checker complaining", "help with lifetimes", "make this more idiomatic", or "review my Cargo.toml".
---

This skill guides expert Rust development. Detect the project's edition and toolchain from `Cargo.toml` (`edition`, `rust-version`) and adapt guidance accordingly. Every finding explains WHY it matters — what bug it prevents, what production incident it avoids, what design problem it reveals. Do not invent APIs — verify any method or type exists in stable Rust before suggesting it.

## How to Think About Rust Problems

Before fixing any issue, trace through the layers:

- **Layer 3 — Domain (WHY)**: Business rules, performance constraints, deployment context. These constrain everything below.
- **Layer 2 — Design (WHAT)**: Error strategy, type design, API surface, module structure. Check against SOLID and API Guidelines.
- **Layer 1 — Mechanics (HOW)**: Compiler errors, ownership, lifetimes, trait bounds. Fix the immediate issue, but always trace UP.

When a compiler error appears, reframe it as a design question:

| Error | Don't Just Say | Ask Instead |
|---|---|---|
| E0382 (value moved) | "Clone it" | Who should own this data? |
| E0597 (doesn't live long enough) | "Add a lifetime" | Is the scope boundary correct? |
| E0277 (trait not satisfied) | "Add the bound" | Is this the right abstraction? |
| E0499 (two mutable borrows) | "Use RefCell" | Should this be two separate resources? |
| "future is not Send" | "Wrap in Arc" | Does this state need to cross threads? |

## Ownership & Borrowing
→ *Consult [ownership reference](references/ownership.md) for borrowing rules, Cow, smart pointers.*

**DO**: Default to borrowing (`&T`). Move to owned only when the callee must store the value.
**DO**: Use `&str` and `&[T]` in function parameters — not `&String` or `&Vec<T>`.
**DO**: Use `Cow<'_, str>` when a function conditionally allocates.
**DON'T**: Clone to silence the borrow checker — restructure ownership instead.
**DON'T**: Over-annotate lifetimes — elision covers 95% of cases.
**DON'T**: Write `&'a mut self` on methods — borrows self for its entire lifetime.

## Error Handling
→ *Consult [error-handling reference](references/error-handling.md) for thiserror/anyhow/snafu decision matrix.*

**DO**: Use `?` with `.context()` at every propagation point.
**DO**: Use `thiserror` for libraries, `anyhow` for applications.
**DO**: Use `#[non_exhaustive]` on public error enums.
**DON'T**: Use `.unwrap()` or `.expect()` in production paths — production services have been taken down by unhandled panics.
**DON'T**: Implement `From` for fallible conversions — use `TryFrom`.
**DON'T**: Both log AND propagate an error — pick one.

## Type Design
→ *Consult [type-patterns reference](references/type-patterns.md) for newtype, typestate, builder patterns.*

**DO**: Parse, don't validate — convert raw inputs into types that carry their validity.
**DO**: Replace boolean parameters with enums — `process(data, true, false)` is unreadable.
**DO**: Use `#[must_use]` on functions returning values callers must handle.
**DON'T**: Use `..Default::default()` — silently wrong when fields are added.
**DON'T**: Use catch-all `_` in match on owned enums — swallows new variants.

## Design Principles
→ *Consult [design-principles reference](references/design-principles.md) for SOLID, Microsoft M-* rules, modern Rust table.*

**DO**: Apply Single Responsibility — one struct per concept, one domain per module.
**DO**: Depend on traits, not concrete types (Dependency Inversion).
**DO**: Use `#[expect(lint)]` instead of `#[allow(lint)]` (warns when stale, Rust 1.81+).
**DON'T**: Use weasel word names — `BookingService`, `DataManager`. Name types after what they ARE.
**DON'T**: Expose `Arc`, `Rc`, `Box` in public API signatures — hide implementation details.

## Traits & API Surface
→ *Consult [traits reference](references/traits.md) for generics vs dyn, standard traits, sealed patterns.*

**DO**: Implement standard traits eagerly (`Debug`, `Clone`, `PartialEq`, `Hash`, `Default`).
**DO**: Default to generics. Use `dyn Trait` only for genuine runtime polymorphism.
**DON'T**: Violate Hash/Eq consistency — the most dangerous silent bug in Rust's stdlib.

## Async
→ *Consult [async reference](references/async.md) for blocking taxonomy, cancellation safety, JoinSet.*

**DO**: Keep business logic synchronous. Use async only at I/O boundaries.
**DO**: Use `CancellationToken` for graceful shutdown — not `task.abort()`.
**DON'T**: Block async threads for more than 10-100 microseconds between `.await` points.
**DON'T**: Hold a `MutexGuard` across `.await` — drop it first.
**DON'T**: Make every function async "just in case" — async infects signatures upward.

## Concurrency
→ *Consult [concurrency reference](references/concurrency.md) for decision tree, actor pattern, channels.*

**DO**: Ask first: "Do I actually need concurrency?" If no measured bottleneck, stay sequential.
**DO**: Prefer channels and actors over shared mutable state.
**DO**: Use bounded channels in production for backpressure.
**DON'T**: Default to `Arc<Mutex<T>>` — it's expensive and often unnecessary.
**DON'T**: Use async for CPU-bound work — use Rayon or `spawn_blocking`.

## Unsafe
→ *Consult [unsafe reference](references/unsafe.md) for SAFETY comments, Miri, UB patterns.*

**DO**: Every `unsafe` block needs a `// SAFETY:` comment explaining the invariant.
**DO**: Run `cargo +nightly miri test` on code with unsafe.
**DO**: Deny unsafe at crate level (`unsafe_code = "deny"`) with surgical allows.
**DON'T**: Use unsafe when safe alternatives exist — all memory-safety CVEs in Rust trace to unsafe code.

## Performance
→ *Consult [performance reference](references/performance.md) for build config, allocation patterns, benchmarking.*

**DO**: Profile before optimizing — `cargo flamegraph`, DHAT, samply.
**DO**: Use `overflow-checks = true` in release profiles (CVE-2018-1000810).
**DO**: Use `strict_add` / `strict_sub` (1.91) instead of `checked_add().unwrap()`.
**DON'T**: Optimize without a measured bottleneck.

## Testing & Documentation
→ *Consult [testing](references/testing.md) and [documentation](references/documentation.md) references for test frameworks, property testing, and API docs guidelines.*

## Modules, Macros & Serde
→ *Consult [modules-cargo](references/modules-cargo.md), [macros](references/macros.md), and [serde](references/serde.md) references for workspace setup, macro decision flowchart, and serialization patterns.*

## Anti-Patterns
→ *Consult [anti-patterns reference](references/anti-patterns.md) for the full severity-labeled catalog.*

## The Rust AI Slop Test
→ *Consult [ai-slop reference](references/ai-slop.md) for the complete fingerprint catalog.*

**Critical quality check**: If a senior Rust engineer reviewed this code, would they immediately suspect AI generated it? If yes, that's the problem.

The most common AI tells in Rust:
- `.clone()` everywhere to silence the borrow checker
- `Arc<Mutex<T>>` as default concurrency for everything
- `.unwrap()` on every `Result` and `Option`
- Traits with exactly one implementation
- Over-annotated lifetimes where elision works
- `async` on functions that never `.await`
- Verbose comments explaining WHAT, never WHY
- Generic variable names (`data`, `result`, `item` instead of domain names)
- Premature generalization with unused generic parameters
- No refactoring — duplicated blocks with minor variations
- `#[allow(...)]` to suppress warnings instead of fixing root cause

## Thinking Prompts

Before suggesting any fix, work through:

1. **What bug does this prevent?** If you cannot name a concrete bug, the fix may not be worth the complexity.
2. **What would happen in production?** Think in terms of incidents, not style.
3. **Is the type system doing enough work?** Every runtime `assert!` is a type waiting to be born.

## Severity Levels

Label every finding:

- **blocking** — Soundness bug, UB, data race, guaranteed panic. Must fix.
- **important** — Wrong error handling, performance cliff, design pain. Should fix.
- **nit** — Style, naming, minor idiom. Fix if convenient.
- **suggestion** — Alternative worth considering. No action required.
- **praise** — Highlight well-written code. Reinforce good patterns.

## Output Format

Group findings by file. For each finding:
1. File path and line number
2. Severity label
3. Rule name
4. **WHY it matters** — the concrete consequence
5. Before/after code block when the fix is non-obvious

Skip files with no findings. End with a prioritized summary.

**CRITICAL**: Be direct — vague feedback wastes time. Be specific — "line 42 of parser.rs" not "some functions". Say what's wrong AND why it matters. Prioritize ruthlessly — if everything is important, nothing is.

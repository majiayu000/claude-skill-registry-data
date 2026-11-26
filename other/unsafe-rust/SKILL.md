---
name: unsafe-rust
description: Justify, document, and verify unsafe Rust — safety invariants on every unsafe block, sound safe wrappers, undefined behaviour hazards, and verification with Miri. Use when writing or reviewing unsafe code, when working across an FFI boundary, when raw pointers or transmute appear, when a safe API wraps an unsafe primitive, or when the user asks whether an unsafe block is justified.
---

# Unsafe Rust

`unsafe` is a promise, not a permission: the code inside may break the rules,
but the code around it must keep them. `unsafe` means undefined behaviour, not
"dangerous" — UB is the compiler being permitted to assume the situation
cannot arise, which is why it surfaces as a later, unrelated miscompile. The
depth is in `SAFETY-REVIEW.md` under `UB is not a bad outcome at runtime`.
This skill governs *soundness* — whether a safe caller can trigger undefined
behaviour — and it never treats "the tests pass" as evidence of soundness.

## `unsafe` does not turn off the borrow checker

It permits exactly five extra operations: dereferencing a raw pointer, calling
an `unsafe fn`, implementing an `unsafe trait`, accessing a `union` field, and
mutating a `static mut`. Everything else — lifetimes, ownership, types — still
applies inside the block. `unsafe` is a narrow escape hatch — reaching for it
to resolve a borrow error is always wrong. That case is `/ownership-not-clone`.

## The justification test

`unsafe` is justified for exactly three reasons. Each has a question that must
be answered before the block is written — and the reason written down, in the
`// SAFETY:` comment or the PR description, not remembered by whoever wrote it.

1. **FFI.** Calling into or out of another language. The checklist: who owns the
   memory on each side, what happens on a panic crossing the boundary (it must
   not), whether the foreign function is thread-safe, and what the lifetime of
   every pointer received actually is. Hand the boundary design to `/rust-ffi`.
   Use the edition 2024 marks on the boundary — those attributes always were
   unsafe assertions; they are in `SAFETY-REVIEW.md` under `Per FFI call`.
2. **A performance win the profile named.** The checklist: what did the
   measurement say, what invariant is being asserted in place of the check,
   and is the safe version genuinely on the hot path — `/rust-performance`
   first, and the answer there is usually that the allocation was the problem.
3. **A primitive the language cannot express safely.** Intrusive structures,
   custom allocators, self-referential types. The checklist: does a crate
   already do this correctly, and is the invariant writable in two sentences.

A block that does not sit under one of these three has an author reaching for
`unsafe` to make an error go away, and the error was right.

## Every `unsafe` block carries a `// SAFETY:` comment

The comment states the invariant the caller upholds, not what the code does:

```rust,ignore
// SAFETY: `ptr` came from `Vec::as_mut_ptr` on a vec of at least `len`
// elements that is still alive for this scope, and no other reference to it
// exists here.
let slice = unsafe { std::slice::from_raw_parts_mut(ptr, len) };
```

And every `pub unsafe fn` carries a `# Safety` doc section stating what the
caller must guarantee. `clippy::undocumented_unsafe_blocks` and
`clippy::missing_safety_doc` are the mechanical check for the two rules:
propose them for the repo lint config, never override a level the repo already
set.

## Soundness is the bar, not "it works"

A safe API is sound when no safe caller can trigger undefined behaviour, for
any input, including malicious ones. Unsound code is never acceptable: there is
no "unsound but only in a case that cannot happen here". Soundness belongs
to the API, so a safe function that lets safe caller code reach UB is a bug
whoever calls it today; fix it, or mark it `unsafe fn`. The encapsulation rule: keep the `unsafe` block as small as it can
be, and put the safe/unsafe boundary where the invariant is actually
enforceable — the check belongs in the safe code that guards the block, not in
the block itself. Inside the block, assume the code you call misbehaves — the
depth is in `SAFETY-REVIEW.md`.

The unit of soundness is the module. Fields and helpers private to a module
cannot be touched by outside code, so the module is where an invariant can be
defended: choose the narrowest module that is still able to guarantee the
invariant, put the `unsafe` there, and expose only a safe interface. `String` is the model — a `Vec<u8>` whose
private field and safe methods keep the bytes valid UTF-8, so safe callers
cannot break the invariant the unchecked internals rely on. When the
invariant is large or the dependencies many, isolate the code in its own small
crate with few dependencies, so the audit surface is a short list of files.

## The UB hazards that actually appear

One point each; the review depth is in `SAFETY-REVIEW.md`.

- **Aliasing:** a `&mut` coexisting with any other live reference to the same
  place.
- **Uninitialized memory:** producing a reference to it — use `MaybeUninit<T>`,
  never `mem::zeroed()`: zero is a valid `u32` and an invalid `&T`, `bool`, or
  enum — and the invalidity is instant UB, not a bad value you will notice.
- **Invalid values:** a `bool` that is not 0 or 1, a `char` outside the scalar
  ranges, a null reference.
- **`transmute`:** between types with different layouts, or without
  `#[repr(C)]`/`#[repr(transparent)]` pinning the layout. Two uses are off
  the table outright: casting an integer to an enum through `transmute` (a
  value with no variant is instant UB; use a `TryFrom` or a `match`), and
  stretching a lifetime with `transmute` to make a borrow check pass (the
  checker was right; restructure the ownership).
- **Unwinding across FFI:** a Rust panic unwinding through a C stack frame.
- **Data races:** shared state mutated without synchronization.

## Reach for the crate that already did it

`bytemuck` for plain-old-data casts, `zerocopy` for zero-copy parsing,
`arrayvec`/`smallvec` for stack-backed collections, an existing binding crate
for an existing C library. Auditing `unsafe` you did not write is cheaper than
justifying it — the audit is the published, reviewed one.

The same reasoning rules out `unsafe impl Send` or `Sync` used to silence a
bound the compiler reported. If a type holding a raw pointer or an `Rc` is
rejected by a `Send` requirement, the type is the problem; a hand-written
impl is for a type whose fields really are safe to move across threads, with
the argument in a comment (`SAFETY-REVIEW.md`, per hand-written impl).

## Deferrals

Whether the wrapper should be `pub`, and what its `unsafe fn` signature commits
the crate to, is `/rust-api-design`. `Pin` and manual `Future` impls interact
with `/async-rust`. Error handling across the boundary is `/rust-errors`.
Construct-level mapping from C or C++ into Rust is `/port-from-c` and
`/port-from-cpp` — this skill covers the `unsafe` discipline, not the mapping.

## Verification

New unsafe abstractions get more testing than ordinary code, because the
compiler is not helping. Write tests that act as adversarial callers: pass
boundary values and zero-length input, a closure that panics halfway, a trait
impl that lies (a `Deref` that changes its answer, a `Clone` that panics),
and drop order that surprises. Run them under Miri below.

```bash
cargo miri test              # requires the miri component on nightly
cargo clippy --all-targets   # add -- -D warnings only if the repo has no lint config
cargo test
```

If `cargo miri` is unavailable, say so explicitly in the report rather than
silently skipping it, and do not install a nightly toolchain into the user
environment as a side effect. State the Miri limitations plainly so the result
is not over-read: it does not execute FFI calls into real C code, it only
checks the paths the tests actually exercise, and it is slow enough that
targeting the relevant test — `cargo miri test <filter>` — is usually the
practical move. For the FFI side Miri cannot reach, the routes are
`-Zmiri-strict-provenance` for pointer provenance and the address sanitizer for
what a real C library does with the memory.

---
name: port-from-cpp
description: Port C++ into Rust — RAII and smart pointers onto ownership, templates onto generics and traits, exceptions onto Result, the STL onto Rust collections, and the traps (move semantics, implicit conversions, undefined behaviour, iterator invalidation). Use when porting, rewriting, or migrating C++, a C++ library, or a C++ application into Rust, when replacing a C++ module with Rust behind the existing build, or when the user asks how a C++ construct such as unique_ptr, shared_ptr, a template, or an STL container translates to Rust.
---

# Port from C++

## A construct mapping and a boundary, nothing else

This skill maps C++ to Rust and owns the C++ boundary. The parity
contract, the five phases, and the anti-patterns are `/port-to-rust`,
which runs first and stays running through the port. C is a separate
skill — the mechanics overlap, the idioms do not — so a C codebase
with a `.cpp` extension is still `/port-from-c` territory in everything
but the build.

## The end state, and the C++ default

`/port-to-rust` names three end states. In C++ terms: A, a standalone
Rust binary or library replacing the C++ entirely; B, a Rust core with
a permanent C++-callable surface, real when the deliverable is a
library other C++ code links; and C, a bridge that carries the
migration module by module and is deleted at cut-over. **C is the
default for C++**, more than for any other language in this set: a
large C++ codebase cannot be replaced in one step, and the seam — a
Rust `staticlib` linked into the existing build — lets leaf modules
move one at a time. The bridge is disposable scaffolding that must
still be *sound*, and that tension is what this skill manages; the
mechanics are in `BOUNDARY.md`.

## The traps that break parity silently

The body carries these five because each one produces a port that
passes a naive test suite and is wrong; the full table is `MAPPING.md`.

| Trap | What actually differs |
|---|---|
| Undefined behaviour was doing something | Signed overflow, strict aliasing violations, reading uninitialized memory, and out-of-bounds access are undefined in C++ and defined-or-rejected in Rust. Any behaviour the source got from UB is behaviour the port cannot reproduce and must not try to — it is found, recorded, and decided, and it is one of the few legitimate reasons for a port to differ from its source |
| Move semantics are not the same move | A C++ move leaves a valid, unspecified object behind and runs a destructor on it; a Rust move is a bitwise transfer with no hook and no leftover object. Code that reads a moved-from C++ object is doing something the port cannot express, and self-referential types that relied on move constructors need a different design entirely |
| Implicit conversions | C++ converts between numeric types, applies integer promotion, and calls converting constructors without a cast. Rust requires every conversion to be written, so a port surfaces conversions the source never made visible — and each one is a place a value could have been truncated silently |
| Iterator and reference invalidation | A `push_back` may reallocate and invalidate every outstanding iterator and reference; C++ tolerates the pattern until it does not. Rust rejects the pattern at compile time, so the port must restructure — usually with indices — and the restructuring is where the design gets clearer, not where it gets worse |
| Exceptions cross layers invisibly | An exception propagates through frames that never mention it, including destructors that run on the way out. Mapping to `Result` makes every propagation point visible and surfaces error paths the source never named — `/rust-errors`. Note the `noexcept` boundary: a C++ function that promises not to throw becomes an infallible signature, and one that did throw becomes `Result` |

## Mapping, in one line

`MAPPING.md` holds the full table; a row is a starting point, not a
rewrite rule. Where the source behaviour was undefined there is no
row — there is a contract decision.

## RAII maps, and this is the good news

Destructors map to `Drop`, `unique_ptr` to `Box`, `shared_ptr` to
`Arc` (or `Rc` where single-threaded), `weak_ptr` to `Weak`,
references to `&`/`&mut`, and `const` to immutability by default.
Reach for `Arc`/`Rc` only where the C++ genuinely shared ownership,
not everywhere a `shared_ptr` appeared — `shared_ptr` is often used
where a `unique_ptr` or a plain reference would have done, and
copying that habit into Rust produces the reference-counted soup
`/ownership-not-clone` exists to prevent. `Drop` cannot fail, so a
destructor that could throw becomes an explicit `close()`/`finish()`
returning `Result`.

## Templates are generics until they are not

Simple templates map to generics with trait bounds; SFINAE and
concepts map to bounds; CRTP usually maps to a plain trait; template
specialization maps to distinct trait impls. Where a template was doing
compile-time computation or reflection, the honest answer is often a
macro or a build script — a template metaprogram is usually
reimplemented rather than translated. Multiple inheritance and virtual
bases have no mapping and become composition.

## The test suite is the corpus, and the sanitizers are evidence

A GoogleTest or Catch2 suite is characterization input: the cases are
inputs, the assertions are the recorded behaviour. C++ ports have one
advantage no other language in this set does: running the source
under ASan, UBSan, and TSan before porting tells you which behaviours
are UB and therefore not part of the contract. Run it before any Rust
exists — the characterization pass of `/port-to-rust`; harness shapes
are `/rust-testing`.

## Verification

Both sides:

```bash
cargo test --all-features
cargo clippy --all-targets --all-features   # add -- -D warnings only if the target repo has no lint config
cargo miri test                              # any module with unsafe, including every FFI shim
ctest            # or the existing C++ test command — the source still passes while both run
```

Plus the source-side sanitizer run (`-fsanitize=address,undefined`),
whose findings belong in the contract as behaviour that is explicitly
not reproduced. Then the differential run over the recorded corpus,
reported with its denominator, plus the corpus requirement: at least
one case per trap — an input at a signed-overflow boundary, a
container operation that would have invalidated an iterator, a
narrowing conversion, and an input that threw.

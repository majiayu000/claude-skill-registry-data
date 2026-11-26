---
name: port-from-c
description: Port C into Rust — recovering the ownership, lifetime, nullability, and length that C never recorded, mapping pointers to references and slices, tag-plus-union to enums, return codes and errno to Result, and linking Rust into the existing build with bindgen and cbindgen. Use when porting, rewriting, or migrating C, a C library, firmware, or a C application into Rust, when replacing C modules one at a time behind the existing build, or when the user asks how a C construct such as malloc, a char pointer, a union, or a preprocessor macro translates to Rust.
---

# Port from C

## A construct mapping and a boundary, nothing else

This skill maps C semantics and owns the C boundary; the parity contract, the
five phases, and the anti-patterns are `/port-to-rust`, which runs first and
stays running through the port. C++ is a separate skill — a codebase using
RAII, templates, or the STL is `/port-from-cpp` even when it compiles as C.

## The end state, and why C is almost always C

`/port-to-rust` names three end states; in C terms: A, a standalone Rust
binary or library that replaces the C entirely; B, a Rust core with a
permanent C-callable surface — the right end state when other C code links
this library and will keep doing so; and C, an FFI seam that carries the
migration module by module, deleted at cut-over. C codebases are rarely
replaced in one step, so C is the common end state and B is common for
libraries; the two are distinguished by one question — will any C code still
be calling this after the port finishes? Seam mechanics: `BOUNDARY.md`.

## The traps, which are all the same trap: C did not say

Each one breaks parity silently; the full table is `MAPPING.md`.

| Trap | What C never recorded |
|---|---|
| Ownership | A `T*` may be owned, borrowed, or static. Freeing the wrong one is a double free; freeing none is a leak. The port has to decide per pointer — `Box<T>`, `&T`, or a raw pointer kept raw — and the decision usually lives in a comment or in nothing at all |
| Lifetime | How long a returned pointer stays valid is convention. A function returning a pointer into a static buffer, into the argument, or into freshly allocated memory all look identical in the header, and each maps to a different Rust signature |
| Nullability | Any pointer may be null. `Option<&T>` is the honest mapping at the boundary; inside the port, a value that must exist should be a type that cannot be absent |
| Length | Arrays decay to pointers, so length travels separately, in a second parameter, in a struct field, in a NUL terminator, or by convention. Each of these is a different Rust type, and getting it wrong is the classic C bug the port is supposed to eliminate |
| Encoding and validity | `char*` is bytes. It may be UTF-8, some other encoding, or arbitrary binary. `CStr`/`CString` at the boundary, and a deliberate decision — validate, convert lossily, or keep bytes — before anything becomes a `String` |

## Mapping, in one line

`MAPPING.md` holds the full table; a row is a starting point, not a rewrite
rule. The C corollary: nearly every row hides a decision C never recorded,
so the table is a set of questions, not a translation.

## Tag plus union is an enum, and that is the win

The C idiom of a struct holding a `kind` field and a union of payloads maps
to a Rust enum with data, and the translation makes an entire class of bug
unrepresentable — reading the wrong union arm. That single rewrite is usually
the largest correctness gain in a C port, and it is `/type-driven-design`.
A bare `union` in Rust is `unsafe` to read, so a direct union-to-union
translation keeps the bug and adds `unsafe` on top.

## Return codes, `errno`, and macros

A function returning `0`/`-1` with the real value written through an
out-parameter maps to `Result<T, E>` returning the value directly; the
mapping is mechanical, the judgment is the error taxonomy, which is
`/rust-errors`. `errno` is thread-local global state and does not survive
the port as a mechanism — the values become variants.

A macro defining a constant becomes a `const`; a function-like macro becomes
a function (often `const fn`, and the port gets type checking it never
had); a macro generating code becomes `macro_rules!` or a build script.
Conditional compilation maps to `#[cfg(...)]` and features — enumerate
which combinations are actually built, because a `#ifdef` matrix nobody has
compiled in years is dead code found during `/port-to-rust` phase 1.
Macro-heavy C is where a transpiled port produces its worst output.

## The test suite is the corpus, and the sanitizers are evidence

C suites are typically the thinnest in this set, so the corpus usually has
to be built rather than found — recorded inputs from production, or a
fuzzer over the input grammar. Run the source under ASan and UBSan first:
whatever it reports is behaviour that is not part of the contract, and
finding it before `/port-to-rust` phase 3 saves arguing about it in phase 4.
Harness shapes are `/rust-testing`.

## Global mutable state, and manual cleanup

File-scope `static` mutables map to `OnceLock`, `LazyLock`, or an explicit
context struct threaded through — the last being both the most work and the
actual improvement. `goto cleanup` maps to `?` plus `Drop`, the one C idiom
that gets strictly shorter in Rust. `setjmp`/`longjmp` has no mapping, and
the code paths using it are redesigned. Signal handlers map to
`signal_hook` plus a channel; async-signal safety may have been violated.

## Verification

Both sides:

```bash
cargo test --all-features
cargo clippy --all-targets --all-features   # add -- -D warnings only if the target repo has no lint config
cargo miri test                              # the shim and every module with unsafe
make check       # or the existing C test command — the source still passes while both run
```

Plus the source-side sanitizer run (`-fsanitize=address,undefined`), whose
findings go in the contract as behaviour not reproduced. Then the
differential run, reported with its denominator, plus the C-specific corpus
requirement: a null pointer where one is permitted, a zero-length buffer, a
non-NUL-terminated or non-UTF-8 string, an input at an integer-overflow
boundary, and every error return path the source can produce — the part a C
suite almost never covers.

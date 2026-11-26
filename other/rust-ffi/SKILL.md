---
name: rust-ffi
description: Design an FFI boundary meant to last — a thin translation layer with the logic in core crates, no panic across the boundary, explicit ownership on every pointer, repr(transparent) newtypes, and unsafe extern in edition 2024. Use when designing or reviewing a Rust FFI surface, when exposing a Rust library to another language, when a DLL or shared library keeps state, or when the user asks how to shape an extern function.
---

# Rust FFI

A boundary that is meant to stay is designed, not discovered. Moving off C —
bindgen, cbindgen, and the link into an existing build — is `/port-from-c`.

## The layer only translates

Every line of business logic lives in a normal Rust crate that knows nothing
about FFI; the `extern` layer converts types, checks pointers, and calls in.
The core crate is testable with `cargo test`, the FFI layer only through a
foreign harness — logic that drifts into the boundary is logic no test reaches.
Core types stay free of raw-pointer fields and of `#[repr(C)]` layouts chosen
for the foreign side; the pointer lives in the boundary type, as below.

```rust
use std::ffi::{c_char, CStr};
use std::panic::catch_unwind;

// Core: the logic, in code that knows nothing about FFI.
pub struct Client {
    pub name: String,
}

impl Client {
    fn new(name: &str) -> Self {
        Client { name: name.to_owned() }
    }
}

// Boundary: translates, checks, and calls in — nothing else.
#[repr(transparent)]
pub struct MylibClient(*mut Client);

/// # Safety
/// `name` must be NUL-terminated UTF-8, or null; the check happens once,
/// here, on the way in.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn mylib_client_new(name: *const c_char) -> *mut MylibClient {
    let build = || {
        if name.is_null() { return None; }
        let name = unsafe { CStr::from_ptr(name) }.to_str().ok()?;
        Some(Box::into_raw(Box::new(Client::new(name))) as *mut MylibClient)
    };
    catch_unwind(build).ok().flatten().unwrap_or(std::ptr::null_mut())
}

/// # Safety
/// `client` must be a non-null handle from `mylib_client_new`, freed exactly once.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn mylib_client_free(client: *mut MylibClient) {
    drop(unsafe { Box::from_raw(client as *mut Client) });
}
```

Wrap every pointer the foreign side owns in a Rust type whose `Drop` releases
it, so each exit path frees it exactly once. The safe wrapper checks for null
and returns a `Result` (or `Option`) to Rust callers instead of handing the
null onward; the raw pointer and the `unsafe` block stay inside it. For a
large C API, split the work: a raw declarations crate named `xyzzy-sys` under a
safe `xyzzy` crate that owns the wrappers.

## Nothing panics across the boundary

Unwinding into a foreign frame is undefined behaviour. Every `extern "C"`
entry point catches — `catch_unwind` at the boundary, and only there — and
converts the panic to an error code or an out-parameter, the one place
`/rust-errors` does not call `catch_unwind` a last resort.

## Every pointer states its ownership

Who allocated it, who frees it, how long it stays valid, and whether null is
allowed — in the signature and in the docs. Never return a pointer to stack
data or to a local that dies on return; the caller holds a dangling address
the moment the call ends. Hand out heap data (`Box::into_raw`, reclaimed with
`Box::from_raw` in the matching free) or a pointer into memory the caller
owns. A crate that exposes an
allocation exposes the matching free from the same crate; the other side
cannot free what the first side allocated. A `# Safety` section carries it —
`/rust-docs` for the wording, `/unsafe-rust` for the invariant.

## `repr` is part of the contract

`#[repr(C)]` on every struct that crosses, and `#[repr(transparent)]` on a
newtype that wraps a handle, so the wrapper is invisible on the wire and the
type safety is free on the Rust side. A default-`repr` struct has no layout
guarantee; code that reads it from the other side works until it does not.

## Isolate the state a shared library keeps

A DLL loaded twice, or loaded and unloaded, must not leave process-global
state behind. Prefer an opaque handle the caller creates, passes back, and
destroys, over module-level statics — the handle makes the lifetime explicit
and makes two instances possible.

Across a library boundary share only plain `#[repr(C)]` data. Do not let a
static, a thread-local, a `TypeId`, or a pointer into data that does not
travel across the boundary (for example another module allocator or vtable)
become part of what two sides must agree on; each library has its own copy of
those, and they disagree silently.

## Naming across the boundary

Exported symbols are prefixed with the library name, because the C namespace
is flat: `mylib_client_new`, `mylib_client_free`. Inside Rust the same
function is `Client::new`; the prefix belongs to the exported symbol.

Crate names follow direction. A `-sys` crate imports a C library into Rust
(raw declarations and linking, nothing else); an `-ffi` crate exports a Rust
library as a C-style one. The build rules for `-sys` crates are in
`SYS-CRATES.md`.

## The edition 2024 forms

`unsafe extern { }` around the declaration of a foreign function, and
`#[unsafe(no_mangle)]` on an export. Both say out loud what was always true:
declaring a foreign signature is an unsafe assertion about the other side.

## Strings and slices do not cross as they are

A Rust `&str` is not a C string, and a `String` cannot be freed by `free()`.
`CStr` and `CString` at the boundary, pointer-plus-length for slices, and the
UTF-8 validation happens once, explicitly, on the way in.

Declaring a foreign function uses an `extern "C"` block with fixed-width
types — `c_int`, `c_char`, `u32` — never Rust `usize` guesses for a C `int`.
Linking comes from `#[link(name = "...")]` or from a `build.rs` that emits the
link directives, so a crate does not depend on an ambient environment.

## Deferrals

Generating declarations from headers, including the `bindgen` flags,
`include!` of its output, and the regenerate-and-diff CI check, is in
`SYS-CRATES.md`; the porting walkthrough stays in `/port-from-c`. Migrating an existing C codebase into Rust is `/port-from-c`, and the bindgen
and cbindgen walkthroughs live there. Whether an `unsafe` block is sound is
`/unsafe-rust`. What the safe Rust API on top should look like is
`/rust-api-design`. The `# Safety` section wording is `/rust-docs`.

## Verification

```bash
cargo test                   # the core crate, which holds the logic
cargo miri test              # for the Rust side of pointer handling that miri can see
cargo clippy --all-targets   # at the level the repo configures
```

Plus the boundary check no cargo command performs: a foreign-language test
that loads the library, exercises create-use-destroy, and runs under the
platform leak checker. An FFI surface without it is checked on one side only.

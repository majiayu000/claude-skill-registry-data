---
name: rust-api-design
description: Design a Rust public API — trait design, generics versus dyn, sealed traits, what is exported, and which changes break semver. Use when designing or reviewing a crate public surface, when choosing between a generic parameter and a trait object, when adding a trait method or enum variant to a released crate, or when the user asks whether a change is a breaking change.
---

# Rust API Design

Everything `pub` from the crate root is a promise to every downstream caller. This
skill governs *what callers can see and rely on* — the exported surface, the shape
of its traits and generics, and which changes break the promise.

## Libraries bind harder than applications

Treat these rules as requirements when writing a library, because callers you
cannot see depend on its surface. In an application every caller lives in your
own repository, so they are strong defaults that give way when simplicity is
worth more than reuse. An application may take a `Vec`, skip the derives nobody
uses, and stay on the concrete rung; a library has no such freedom.

## The surface is the contract

Default to private and export deliberately: a type `pub` only because a `pub fn`
returns it is still part of the API, impls and public fields included. Make
`pub(crate)` the habit; re-export the surface from `lib.rs`, module paths private:

```rust,ignore
// lib.rs
pub use crate::internal::parser::Parser; // the surface
mod internal;                            // the tree stays private
```

`Parser` is reachable by one path only: renaming the module, moving the file,
splitting the crate — none of it is a breaking change, because none of it is visible.

The surface refuses three shapes: an item public at two paths; an `Arc`, `Rc`,
`Box` or `RefCell` in a public signature; and a dependency type in a signature,
making that dependency part of the semver contract. The depth, including fields,
modules, crate size, parameter and return types, re-exports and `#[must_use]`, is
in `SURFACE.md`; how a public type is built (constructors, `Default`, builders) is
in `CONSTRUCTION.md`.

## Getting a dependency in

The ladder, lowest rung first: a concrete type — pass the thing; a wrapper struct —
swap the inside without touching a signature; a generic parameter — static dispatch,
but it infects every type that holds it; `dyn Trait` — the infection stops, at the
price of object safety. Climb only when the current rung cannot express the
requirement, never for a test-only need — ADR 0006 belongs to `/rust-testing`. The
cost of each rung is in `DEPENDENCY-INJECTION.md`.

## Generics or `dyn`

A library prefers generics by default; reach for `dyn` when one of the rows below
applies, including a compile-time or code-size budget and code loaded at runtime.

| Want | Choose | Cost |
|---|---|---|
| Monomorphized speed, inlining, no vtable | `impl Trait` / `<T: Trait>` | Code bloat; every call site instantiates; one concrete type per parameter; verbose signatures |
| Heterogeneous collection, plugin registry, smaller binary, faster compiles, code loaded at runtime | `dyn Trait` | One copy plus a vtable dispatch; the trait must be object-safe |
| Argument position, caller convenience | `impl Trait` argument | The caller cannot turbofish |
| Return position in a public API | named type or `impl Trait` | `impl Trait` hides the type — a deliberate choice, not a shortcut |

Object safety usually settles it: generic methods, `Self` in arguments or returns
beyond the receiver, associated constants used through the object, and
associated functions that take no `self` (a `fn new() -> Self` constructor, a
`fn name() -> &'static str` helper) all rule out `dyn`; a heterogeneous registry cannot be generic without an enum or a trait
object. A method that would break object safety, a no-`self` associated function
included, can opt out with `where Self: Sized`, which removes it from the
vtable and keeps the rest of the trait usable as `dyn`. Return-position `impl Trait` is concise but awkward when callers
also need `Debug` or `Clone` bounds on the opaque type; it suits internal APIs
best.

## Trait design

A trait is shared behaviour callers write generic code against, not a namespace
for grouping related functions. Keep the required methods small and default the
rest — every required method is a promise to every future implementer. A default
method may carry a bound of its own (`where Self::Item: Clone`), so it exists
only for implementers that satisfy it and costs the rest nothing; that is how
`Iterator::cloned` is offered to iterators over `Clone` items alone. Use an
associated type for the one sensible choice per implementer (`Iterator::Item`), a
generic parameter for several (`From<T>`). Watch blanket impls — `impl<T: Foo> Bar
for T` closes the door on any later `impl Bar for SomeType` that does not satisfy
`Foo`; the trap fires when the second impl is written, not when the blanket is.

## Sealed traits

A sealed trait exists to let the crate add methods without breaking downstream
implementers: the supertrait lives in a private module, so only this crate can
implement it, though downstream code can still name the trait as a bound.
Document that the trait is sealed, in the trait docs, so an implementer who hits
the error knows it is deliberate. Readers reproduce the pattern wrong from
memory, so here it is:

```rust
struct Widget;

mod sealed {
    pub trait Sealed {}
}

pub trait WidgetBuilder: sealed::Sealed {
    fn new() -> Self;
}

impl sealed::Sealed for Widget {}

impl WidgetBuilder for Widget {
    fn new() -> Self {
        Widget
    }
}
```

## What breaks and what does not

The headline cases: adding a variant to a public enum breaks exhaustive matches
(unless the enum is `#[non_exhaustive]`); adding a required trait method breaks
implementers, a default body does not; adding a field to a public struct that is
not `#[non_exhaustive]` breaks literal construction; narrowing an argument type
breaks callers; widening a return type breaks callers who programmed against
the old one. The full table, including the non-obvious ones, the `#[non_exhaustive]`
exceptions, and the MSRV policy, is in `SEMVER.md`.

## Standard traits, features, `no_std`, destructors

What a public type should implement and why callers cannot add it themselves, plus
destructor rules, is in `STANDARD-TRAITS.md`. Cargo features (additive only) and
making a library `no_std` are in `FEATURES.md`.

## Deferrals

The shape of the error type this API returns is `/rust-errors`. Whether an argument
type should be a newtype carrying an invariant is `/type-driven-design`. Whether a
public function should be `async`, and what that commits the crate to, is
`/async-rust`. Whether a `pub unsafe fn` is justified and how its contract is
documented is `/unsafe-rust`.

## Verification

```bash
cargo doc --no-deps          # every public item documented and the links resolve
cargo clippy --all-targets   # add -- -D warnings only if the repo has no lint config
cargo test
```

Run clippy at the lint level configured in the repo — never force `missing_docs` or
another lint on to make the surface check pass; propose it instead. When the crate
is published or has downstream consumers, the semver check the agent runs and reads:

```bash
cargo semver-checks check-release   # requires cargo-semver-checks; skip with a note if unavailable
```

Do not install tooling into the user environment as a side effect. If
`cargo-semver-checks` is not present, say so and fall back to the `SEMVER.md` table.

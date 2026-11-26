---
name: rust-macros
description: Write a macro only when a function, a trait, or a generic cannot do the job — then by-example before proc-macro, with hygiene, a `_private` helper module, and spanned compile errors instead of panics. Use when writing or reviewing macro_rules! or a proc macro, when a derive or attribute macro is being added, when macro hygiene or `$crate` comes up, or when the user asks whether something should be a macro.
---

# Rust Macros

The first question a macro must answer is why it is not a function, a trait,
or a generic — and usually the answer is that it is not.

## A macro is a last resort

Most macros exist to avoid typing, and the cost they charge is paid by every
reader afterwards: no jump-to-definition worth the name, error messages
pointing at expansions, no type checking until the expansion happens. The
genuine answers are four — a variadic interface, generating an impl per
type from a list, a DSL whose syntax is not Rust, and keeping parallel
definitions in sync. Name the case; if it
is not one of the four, reach for the non-macro and say which.

The last case needs a concrete shape. When an enum, its
display text, its group, and its `TryFrom<u8>` conversion all list the same
variants, one table fed to a single `macro_rules!` invocation generates
every one of them, so adding a variant is a one-line change and the copies
cannot drift apart. Use it only when two or more such definitions track the
same list; a single enum with one `match` needs no macro.

Rank the options by tooling cost, lowest first, and stop at the first rung
that does the job:

| Rank | Option | What it costs |
|---|---|---|
| 1 | Ordinary code: functions, types, traits, modules | Nothing extra; the IDE and compiler see everything |
| 2 | `macro_rules!` in the same crate | Expansion is hidden from jump-to-definition; readers learn the macro syntax |
| 3 | Generated source, such as a `build.rs` that writes a file | A build step, and output that lives outside the source tree |
| 4 | Procedural macro | A separate crate, a `syn`/`quote` dependency pair, longer builds |

Each step down costs more in tooling and in what a newcomer must learn. Weigh
the price on three fronts before stepping down: IDE and code-search support for the expanded
names, the private dialect the macro creates that every reader must learn
before touching the call sites, and how hard a large-scale mechanical change
becomes when the code to rewrite is hidden behind an invocation.

When the macro would only enumerate variants to give an enum string or
integer conversions, check `strum`, `enumn`, and `num_enum` first; they
already do it. Between a derive and a macro that emits a brand-new type, the
derive is the better shape: the type stays visible in the source and the
macro only adds impls to it.

## By-example before procedural

`macro_rules!` is in the same crate, needs no dependency, and can be read. A
proc macro needs its own crate, a `syn`/`quote` dependency pair, and compiles
before the crate that uses it. Reach for it when the input has to be parsed
as Rust syntax — what derives and attribute macros are — and not before.

A lightweight DSL is the natural by-example case: the invocation is a small
interpreter for a language whose grammar you control, and `macro_rules!`
spells it without a new crate.

## Hygiene, and `$crate`

A macro expands at the call site, where the names it mentions may mean
something else. `$crate` resolves to the defining crate no matter where the
expansion lands, and a macro that names any item from its own crate without
it works only until someone invokes it from a module that shadows the path.
Local variables a `macro_rules!` introduces are hygienic and cannot collide;
paths and types are not.

## Fragment specifiers say what you accept

`expr`, `ty`, `ident`, `pat`, `literal`, `tt` — pick the narrowest that fits,
because the specifier is the error message. A macro taking `tt` accepts
anything and reports the failure somewhere inside the expansion, where no
one will look.

A `ty` fragment must accept every spelling of a type, not only a bare name;
the forms to cover are in `ITEM-MACROS.md`.

An `expr` fragment pasted twice is evaluated twice. A call such as
`min_of!(next(), 3)` would advance the iterator on both the comparison and
the result, and any side effect or cost repeats. Bind each expression argument
once, then work with the bindings.

```rust
macro_rules! min_of {
    ($a:expr, $b:expr) => {
        match ($a, $b) {
            (a, b) => if a < b { a } else { b },
        }
    };
}
pub fn pair_min(a: i32, b: i32) -> i32 {
    min_of!(a, b)
}
```

## Control flow stays visible at the call site

A macro body can contain `return`, `?`, `break`, or a mutation of a variable
the caller named, and nothing at the invocation shows it. The reader sees an
innocent-looking line that exits the function. Keep early exits, error
propagation, and mutation out of the expansion; if the macro must reach one of
them, make it part of what the caller types, such as passing the target
variable in by name, and document it. Shortcuts that return from the caller
are the usual offender.

## A macro does not lie about the signature

If the macro generates a function, the generated signature is the one the
caller sees in an error, so it carries real types and real names. Never
generate an item whose name the user did not write and cannot search for —
an implied item is a symbol in errors from a place the reader cannot find.

The same honesty covers the declaration kind and the execution model. A macro
never turns a struct into an enum or a function into a type, never rewrites
the parameters or return type of the item it decorates, and never adds or
removes `async`; what the caller wrote is what the compiler sees. The one
accepted exception is a web-handler style attribute that turns a function
into a function plus a generated registration struct: there the extra item is
the point of the macro, the attribute's name says so, and its docs list
exactly what is emitted.

Macros that emit items have their own checklist — input syntax, attributes,
scopes, visibility, and `ty` fragments — in `ITEM-MACROS.md`.

## The `_private` helper module

Anything the expansion must reference goes in a `#[doc(hidden)] pub mod
_private`, referenced through `$crate::_private::…`, so it is reachable by
the expansion and marked as no part of the public API. Without it, the
helpers become public surface you cannot change.

```rust,ignore
#[doc(hidden)]
pub mod _private {
    use std::sync::atomic::{AtomicUsize, Ordering};
    pub fn next_id() -> usize {
        static NEXT: AtomicUsize = AtomicUsize::new(0);
        NEXT.fetch_add(1, Ordering::Relaxed) + 1
    }
}
macro_rules! next_id {
    () => {
        $crate::_private::next_id()
    };
}
pub fn assign() -> usize {
    next_id!()
}
```

## Proc-macro crates: keep the implementation separate

The proc-macro crate can export nothing but macros, so the logic lives in a
plain sibling crate that the proc-macro crate calls; the sibling is
unit-testable without a compiler harness, which is the actual reason. Snapshot
tests (`insta`) of the generated token stream live with that logic, next to
`trybuild` for the error messages.

A user-facing macro usually ships as three crates: the public `foo` crate that
re-exports the macros, a thin `foo_proc` crate that holds only the
proc-macro entry points, and `foo_proc_impl` with the logic and its tests.
Users depend on `foo` alone. Because generated code names the crate by its
real name, do not promise support for users who rename the dependency in
`Cargo.toml` or re-import it under another name. The crates are versioned in
lockstep: pin each companion with `=x.y.z` and publish them together, so
a mismatched pair never resolves.

When the expansion needs an item from a third-party crate, re-export it
inside `_private` (`pub use ::indexmap::IndexMap;`) and reach it through
`$crate::_private`; the caller then needs no dependency on that crate.

## Errors are spanned, never panics

A proc macro that panics reports "proc macro panicked" with no location. A
`syn::Error` built with `new_spanned` and turned into a compile error by
`to_compile_error` points the compiler at the user's own code — the
difference between a macro people use and one they work around.

```rust,ignore
fn expand(input: &syn::DeriveInput) -> proc_macro2::TokenStream {
    if input.generics.type_params().count() > 1 {
        return syn::Error::new_spanned(&input.generics, "too many generics")
            .to_compile_error();
    }
    // build the derived impl with quote
}
```

## Deferrals

Whether the generated API should exist at all is `/rust-api-design`. What a
generated error type looks like is `/rust-errors`. Derives that already exist
and should be used instead of a hand-written impl are `/idiomatic-rust`.
Serde attribute behaviour is `/rust-serde`.

## Verification

```bash
cargo expand --lib          # read the expansion; if it is not installed, propose it, do not require it
cargo test                  # including a trybuild suite if the crate has one
cargo clippy --all-targets  # at the level the repo configures
```

A macro crate without a `trybuild` (or equivalent) test of its failure cases
has never checked the thing users complain about, which is the error message.
For a proc macro, add snapshot tests of the generated tokens to the logic crate
and run them with the rest of `cargo test`.

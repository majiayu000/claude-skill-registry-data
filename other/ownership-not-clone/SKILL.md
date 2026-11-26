---
name: ownership-not-clone
description: Use ownership and borrowing instead of reaching for clone, Rc, RefCell, or Arc<Mutex<_>> to silence the borrow checker. Every clone must be explainable. Use when code clones to make an error go away, when a borrow-checker fight is being resolved by copying data, when reviewing Rust dense with .clone() or Rc<RefCell<_>>, or when the user asks whether a clone is necessary.
---

# Ownership, Not Clone

The borrow checker is a map of where ownership is being fudged, not an obstacle to
route around. This skill decides who holds a value and for how long.

## The rule

Every `clone` must be explainable in one sentence that is not "the borrow checker
complained." A clone that buys a real thing — a value that must outlive the borrow
— is fine; one that only silences an error is a deferred design decision.

The decision is deliberate, not forbidden. When the borrowing alternative is
genuinely contorted — lifetimes threaded through five signatures to save a copy
of a few bytes — a clone is allowed, as a commented choice that weighs what the
copy costs against what the contortion costs. What it may not be is a reflex.
A clone added only to quiet the checker also creates a second value: edits made
to the copy never reach the original, so the program can quietly diverge from
what the author meant. In a prototype, clones are acceptable provided each is
still a deliberate, findable choice that gets revisited before the code ships.
When the alternative to borrowing is a type that owns its data, owning wins
more often than not: an owned `Vec<u8>` field spares every container the
lifetime parameter, and copying small data once is usually fine. Details on
lifetimes, pointer types, and borrow tactics are in `LIFETIMES.md`.

## Read the error, not the workaround

`E0502` (a mutable borrow while an immutable one is still live) and `E0499` (two
mutable borrows of the same place) name a lifetime conflict; the fix is in the
structure the error describes, not in the `clone` that silences it. A reference
lives until its last use rather than the end of its block, so moving the final
read of the shared borrow ahead of the mutation often ends the conflict:

```rust,ignore
// No clone: `first` is Copy, so the borrow ends at the let.
let first = items[0];
for _ in 0..n {
    items.push(first);
}
```

## Borrow splitting

The borrow checker tracks a whole value through method calls, but fields
individually through direct field access. A `&mut self` method that also needs
`self.other_field` is the classic false conflict — destructure once:

```rust,ignore
// The two fields are separate lets and borrow independently.
impl Server {
    fn handle(&mut self) {
        let Self { connections, log, .. } = self;
        for conn in connections.iter_mut() {
            log.record(conn.id());
        }
    }
}
```

`split_at_mut` hands back two disjoint `&mut` halves of one slice; when
destructuring is not enough, extract a free function that takes the two fields.
When one large struct keeps producing these conflicts, split the struct: smaller
types composed in the parent borrow separately, and the new seams are usually
a better design than the old blob.

## Take the cheapest thing that works, in argument position

`&str` over `&String`, `&[T]` over `&Vec<T>`, `impl AsRef<Path>` over a `PathBuf`
for a path a function only reads. A signature that takes `String` when it only
reads forces every caller into a clone — the bug is in the signature.

The same rule covers the wrappers: `&T` over `&Box<T>`, and `Option<&T>` over
`&Option<T>` (call `as_ref()` at the call site). A borrowed parameter accepts
owned values, borrows, and literals through deref coercion, and `&String` or
`&Vec<T>` adds a second pointer hop for nothing. Clippy's `borrowed_box` and
`ptr_arg` flag these.

The other direction matters just as much. When the function needs to own the
value — to store it, send it, or consume it — take it by value and let the caller
decide whether to clone or move. Never take `&T` and clone inside: the caller
who had an owned value to give is forced to pay a copy anyway. And bound a
generic by `Copy` only when the body requires it, not to announce that the
type is cheap.

```rust,ignore
// Forces a clone at every call site that holds a &str.
fn log_message(message: String) { ... }

// Reads only — callers pass a reference and copy nothing.
fn log_message(message: &str) { ... }
```

## `Cow` for genuine borrow-or-own

`Cow<'_, str>` earns its keep when the common path returns the input untouched
and the rare path allocates.

```rust
use std::borrow::Cow;
// The common path borrows; only input containing a bracket allocates.
fn sanitize(input: &str) -> Cow<'_, str> {
    if input.contains(['<', '>']) {
        Cow::Owned(input.replace('<', "&lt;").replace('>', "&gt;"))
    } else {
        Cow::Borrowed(input)
    }
}
```

## When `Rc`/`Arc`/`RefCell`/`Mutex` express a real requirement

Shared ownership is justified when the *runtime* structure genuinely has multiple
owners with no single one outliving the rest, and not when a single owner is
merely inconvenient to name. Run the four-question test in `SHARED-STATE.md`
before adding a `RefCell`; the decision table is in `CLONE-DECISIONS.md`; the
handle clone that passes the one-sentence test is in `SHARED-STATE.md`.

## `mem::take` and `mem::replace`

When the code holds only a `&mut` and needs an owned value, `mem::take` and
`mem::replace` swap something in so the original can be moved out:

```rust,ignore
let old = mem::take(&mut self.buffer);
```

`take` leaves `Default::default()` behind (an empty `String` or `Vec` does not
allocate); `replace` leaves a value you pick; `Option::take` does this for an
`Option` field. To change an enum variant in place, match on `&mut`, `take` the
field you want to keep, and assign the new variant around it.

```rust
use std::mem;

enum Job {
    Queued { label: String, attempts: u32 },
    Failed { label: String },
}

fn give_up(job: &mut Job) {
    if let Job::Queued { label, attempts } = job {
        if *attempts >= 3 {
            // `label` is a &mut String; take it so no clone is needed.
            *job = Job::Failed { label: mem::take(label) };
        }
    }
}
```

## Global state

A `static` with mutable or lazily-initialised contents has no visible owner and
no stated lifetime. Hand the value in as an argument, or keep it in the type that
does the work.

Two concrete failure modes make this more than taste. A `thread_local!` gives
every thread a separate copy, so it breaks wherever one shared value is the
point. And if the dependency graph holds two semver-incompatible versions of a
crate, each version carries its own statics, so a registry or counter that looked
global is quietly two of them. Likewise avoid code that runs before `main`, such
as `ctor`-style crates: its ordering is invisible to the program. Start
everything explicitly from `main`.

## Pointers, lifetimes, and tactics

Which pointer type holds the value (`&`, `Box`, `Rc`/`Arc`, `RefCell`, `Mutex`),
when a lifetime must be named, why owning fields beat borrowed ones in a struct,
what `'static` really asks for, the order of tactics when a conflict survives, and
why self-referential structs are avoided are all in `LIFETIMES.md`.

## Deferrals

Reshaping how correct code is expressed is `/idiomatic-rust`; modelling invariants
into types is `/type-driven-design`; error types are `/rust-errors`; shared state
across `.await` points is `/async-rust`.

## Verification

Keeping or removing a clone changes no behaviour, so the claim "this still works"
is settled by the suite, at the lint level the repo configures:

```bash
cargo clippy --all-targets   # add -- -D warnings only if the repo has no lint config
cargo test
```

`clippy::redundant_clone` is `nursery` and off by default — run it one-off with
`cargo clippy -- -W clippy::redundant_clone` as a proposal generator, never write
it into the repo lint config; its findings are candidates, not edits. The
default-on `clippy::borrowed_box` and `clippy::ptr_arg` catch the over-narrow
argument types from the signature section; fix what they report.

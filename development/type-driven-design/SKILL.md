---
name: type-driven-design
description: Make illegal states unrepresentable — enums instead of boolean and string flags, newtypes instead of bare primitives, parsed types instead of validated ones, typestate for protocol order. Use when a struct has fields that are only valid in some combinations, when validation is re-checked at many call sites, when boolean flags multiply, or when the user asks how to model a domain in Rust.
---

# Type-Driven Design

A type is a promise about which states exist. This skill changes *what the types
allow* — it is the only skill in the Rust bucket that restructures a domain
model, and it does so with a stopping rule: encode an invariant in a type when
violating it is a real bug class in this codebase, not when it is merely
expressible. How a rejection is reported is `/rust-errors`; what a change to a
published type costs is `/rust-api-design`.

## The principle

A type that cannot represent the bad state removes the runtime check, the test
for it, and the bug report about it. Ask of every struct: how many field
combinations are constructible, and how many are valid? The gap between those two
numbers is the surface where bugs live. The compiler is also the one reviewer that
never skims: an agent or a new teammate who misses an unwritten rule still cannot
build the state the type forbids.

## Enums over flag soup

Two booleans make four states; if only three are valid, the fourth is a latent
bug:

```rust,ignore
// Four states, three valid: is_draft && is_published is nonsense.
struct Post {
    is_draft: bool,
    is_published: bool,
    published_at: Option<DateTime<Utc>>,
}

// Three states, three valid, and published_at cannot go missing.
enum Post {
    Draft { body: String },
    Scheduled { body: String, at: DateTime<Utc> },
    Published { body: String, at: DateTime<Utc> },
}
```

The same move applies to a parameter: a `bool` or bare `u8` argument that makes the
call site unreadable becomes an enum, or a newtype when it is boolean for good,
and absence is an `Option`, never a sentinel value. `MODELLING.md` has the table.

The same move covers the `Option<T>` pair smell: two `Option` fields where
exactly one is always `Some` is an enum with two variants, and the impossible
combination — both `None` — stops being constructible.

## Parse, do not validate

A function that takes `&str` and checks it is a valid email address checks again
at the next call site, and the next, because the type carries no proof. A
function that takes `Email` — constructible only through
`Email::parse(&str) -> Result<Email, EmailError>` — checks once at the boundary
and never again. The type is the proof the check ran.

```rust,ignore
struct Email(String); // private field: the constructor is the only way in

impl Email {
    fn parse(input: &str) -> Result<Self, EmailError> {
        // the check, exactly once
    }
}

fn deliver(to: &Email) { /* no validation possible here — none needed */ }
```

The private field is the load-bearing part. A public field makes the
constructor a suggestion, and the invariant dies the day someone builds the
struct by literal. Validation has three tiers in order of preference — static
types, dynamic checks, an opt-out `_unchecked` sibling — spelled out in
`MODELLING.md`.

## Newtypes as invariant carriers

`/idiomatic-rust` reaches for a newtype to stop two arguments of the same
primitive being swapped at a call site. Here the newtype *carries an invariant*:
`NonEmptyVec<T>`, `Percentage`, `Sanitized<String>` — types whose constructor is
the only entrance and whose fields are private. The standard library already
runs this pattern: `NonZeroU32` and friends, with the niche-optimization payoff
that `Option<NonZeroU32>` is the same size as `u32`. Use a newtype, not a type
alias, whenever the two meanings must not be mixed up, and check whether `std`
already has the strongest type (`Path`, `Duration`) before writing one;
`MODELLING.md` also covers restricting traits, panicking `const fn new`, and why
reflection is replaced with traits.
The same argument applies to numbers, where the type system will otherwise let
a byte count be added to a millisecond count — `NonZero` for what cannot be
zero (inside the crate; on a public parameter only when callers can build it easily), `TryFrom` rather than `as` at every boundary, and `NUMERICS.md` for the
rest.

## Typestate for protocol order

When operations must happen in sequence — connect before send, build before
finalize — the stage can be encoded in a type parameter, so calling out of order
is a compile error rather than a runtime `Err`. The full worked example, the
builder variant, and the costs live in `TYPESTATE.md`; the one-line version is
that typestate is for small, fixed state machines where out-of-order use is a
real bug class.

## When to stop

Type-level modelling has a cost: worse error messages, heavier generics, and a
refactor tax when the domain changes. A five-parameter typestate builder for a
struct built once in `main` is over-engineering, and this skill says so rather
than leaving the call to a reviewer.

## Deferrals

How the constructor reports rejection is `/rust-errors`. Whether the resulting
type is ergonomic for callers, and whether tightening a type is a semver break,
is `/rust-api-design`. If the model change is being forced by borrow-checker
pain, run `/ownership-not-clone` first — the answer may be ownership, not
modelling.

## Verification

```bash
cargo clippy --all-targets   # add -- -D warnings only if the repo has no lint config
cargo test
```

Run clippy at the lint level configured in the repo — never on top of one the
repo already set. Then the specific evidence this skill claims: after the
change, the runtime checks the type made impossible should be *deleted*, not
left in place. Grep for the now-impossible branch and confirm it is gone, and
confirm the tests that asserted the old runtime rejection were removed or
rewritten to a compile-fail expectation. If the repo already uses `trybuild`,
add a compile-fail case proving the illegal construction no longer compiles; if
it does not, do not introduce the dependency as part of this change — state the
compile-fail expectation in a doc comment instead.

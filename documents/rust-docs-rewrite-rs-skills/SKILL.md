---
name: rust-docs
description: Doc comments as API contract — a one-line first sentence, module-level docs, Examples, Errors, Panics, Safety and Abort sections, doctests that actually run, intra-doc links, and Cargo package metadata and release notes. Use when writing or reviewing rustdoc comments, when a public item is undocumented, when doctests are marked ignore or fail, when magic values appear undocumented, or when the user asks how to document a Rust crate.
---

# Rust Docs

A doc comment is an API contract, not narration: it tells the caller what
the item does, what it requires, what it returns, and how it fails — and
keeps everything the contract does not need out of the rendered docs.

## The contract test

A doc comment answers what a caller must know to call the item correctly,
and nothing more; it does not narrate the implementation. The test: could
the body be rewritten without changing the doc comment? If not, the comment
is describing the implementation, and it will rot at the first refactor.

## The first sentence carries the load

Roughly fifteen words, one line, no trailing detail: it is what appears in
the module index next to the item name, and the only documentation most
readers will ever see. Weak then strong:

```rust,ignore
/// Constructs a new instance.
///
/// Takes the input, checks it, transforms it, and returns a result, or an
/// error when the input was not acceptable in the way described.

/// Parses a port number from a string, failing when it is out of range.
```

The weak first sentence echoes the item name and pushes the payload into a
trailing paragraph; the strong one carries the whole index entry on its own.
Write it as a sentence: a capital first letter and a closing period, in every
doc comment, not only the headline ones.

## Module documentation

`//!` at the top of the module says what it contains, when a caller should
reach for it, what a short example looks like, and any side effect a caller
could observe (files touched, global state changed, threads spawned). A module of
well-documented items with no module doc leaves the reader to infer the shape
from a list of names.

The crate root is the same rule at larger scale: its `//!` is the front page,
so it is thorough and carries a runnable example, not a one-line tagline.

## The canonical sections

`# Examples`, `# Errors`, `# Panics`, `# Safety`, in that order, each with
its own trigger:

- `# Examples` — aim for one on each kind of public item (modules, traits,
  structs, enums, free functions, methods, macros, aliases), within reason: a trivial accessor
  or an alias whose meaning is its name earns a one-liner at most, or none
  when the signature already shows the use. The doctest lives here, and it
  shows why a caller would want the item, not a mechanical replay of the
  call.
- `# Errors` — on anything returning `Result`, saying which conditions
  produce which failure; also on a trait method whose implementations may
  return `Err`, since the trait is where callers read the contract.
- `# Panics` — on anything that can panic; its absence is itself a claim.
- `# Safety` — on every `pub unsafe fn`, stating the invariant the caller
  must uphold; and on every `unsafe trait`, stating the invariants each
  implementer must uphold, since a wrong impl breaks code that trusts the
  trait. The depth of the invariant is `/unsafe-rust`.
- `# Abort` — on anything that can abort the process rather than unwind or
  return, where that is a real possibility for the caller.

Describe parameters in prose, in the summary or extended text, not in a
table. When a function takes a generic reader or writer, say that callers may
pass `&mut` of one, so nobody gives up ownership of a stream to call it. On an
enum, variant docs are often omittable when the names are self-evident; write
them only where a variant carries a condition or consequence the name does not.

## Doctests are tests

Doctests compile and run under `cargo test`. Use `?` rather than
`.unwrap()` (and never the old `try!` macro that `?` replaced), so the example shows the code a caller would actually write,
and hide setup lines with a leading `#`, so the example stays short without
becoming a fragment. When the setup is heavy, wrap the visible lines in a
hidden function whose arguments are the already-built values. The
compiler checks the example, yet no code calls the wrapper, so the
assertions never execute. Reach for it when constructing the real inputs
(a live connection, a populated store) would bury the point and could not
run in a test anyway:

```rust
/// Reports whether the link answered the last probe.
///
/// # Examples
///
/// ```
/// # struct Link { answered: bool }
/// # impl Link { fn is_up(&self) -> bool { self.answered } }
/// # fn demo(link: Link) {
/// assert!(link.is_up());
/// # }
/// ```
pub fn is_up(answered: bool) -> bool {
    answered
}
```

An ordinary doctest is still preferable whenever it can really run.

```rust
/// Parses a port number.
///
/// # Examples
///
/// ```
/// # use std::num::ParseIntError;
/// let port: u16 = "8080".parse()?;
/// assert_eq!(port, 8080);
/// # Ok::<(), ParseIntError>(())
/// ```
pub fn parse_port(text: &str) -> Result<u16, std::num::ParseIntError> {
    text.parse()
}
```

The rule that matters: `ignore` on a doctest means nothing checks it, so it
is a fragment on purpose or rot waiting to happen. `no_run` when the example
must compile but must not execute — it opens a socket, it needs a file.
`compile_fail` when not compiling is the point.

## Intra-doc links

`[`Config`]` resolves to the item; renaming it leaves a broken-link
warning that a lint level that treats warnings as errors turns into a
build failure — what makes a link better than a backticked name that
nothing checks. `#[doc(inline)]` on a `pub use` of a crate-internal item so
it documents in place, not behind a path the reader cannot import from; never
on a re-export of a standard-library or third-party type, which would paste
foreign docs into yours.

`#[doc(hidden)]` on an impl no user ever triggers by name: a
`From<InternalFailure> for PublicFailure` that exists only so `?` converts
inside the crate is plumbing, not API. Keep genuinely internal items
`pub(crate)` instead of public-and-hidden.

## Document magic values with the why

A constant of `30` documents as the timeout the upstream service enforces,
not as "thirty seconds", which the reader could already read off the value.
A number whose reason nobody recorded is a number nobody can change.

Give the value a named `const` and put the doc comment on it, not on a bare
literal at the use site. The comment says why the value was chosen, what
happens if it changes (retries pile up, a quota trips), and which external
system imposes or consumes it.

## What does not belong in user-facing docs

No design journals, no changelog narration inside item docs, no "rule
applied" compliance tables: artifacts of the writing process, and a reader
looking up a function signature has no use for them. Keep the decision
record in the repo, out of the rendered documentation. Document the end
state: what the code does now, never how it got there or which alternatives
lost. The one exception is a README section on the enduring architectural
goals of the project, which is a fine home for lasting intent.

Comment syntax, notes that are not for users, and when to leave an item
undocumented are in `COMMENTS.md`; the Cargo package metadata, release notes,
and release tags that make a published crate findable are in `PACKAGING.md`.

Docs are read by agents as well as people, and the same things serve both:
documentation on every module and public item, examples that run as written,
and types that make misuse unrepresentable.

## Deferrals

Whether the function should panic at all is `/rust-errors`; the invariant a
`# Safety` section states is `/unsafe-rust`; whether the item should be
public is `/rust-api-design`.

## Verification

Run at the lint level the target repo configures; the fallback applies only
when the repo configures no lints at all:

```bash
cargo doc --no-deps --open # warnings are broken links and bad attributes; read the rendered pages
cargo test --doc
cargo clippy --all-targets # add -- -D warnings only if the repo has no lint config
```

Where the crate has opted in to `#![warn(missing_docs)]`, the undocumented
public item is a warning instead of a discovery. Propose it for a library,
do not impose it, and never add it to a binary crate. Never satisfy the lint
with rushed one-liners that merely restate the item name; where there is
nothing to add, leave the item undocumented or allow the lint on it locally
(see `COMMENTS.md`).

---
name: port-to-rust
description: Run a port into Rust without losing behaviour — define the parity contract, sequence the phases, migrate incrementally behind a stable boundary, and prove parity differentially. Use when moving, porting, rewriting, or migrating an existing codebase into Rust from any language, when deciding how to sequence or scope a rewrite, when a port needs to prove it matches its source, or when a partially-ported system needs both implementations running side by side.
---

# Port to Rust

## A port is a behaviour-preserving move, and nothing else

The one rule this skill exists to enforce: during a port, behaviour changes
and code improvements are separate commits, separate reviews, and preferably
separate weeks. A port that also fixes bugs cannot be validated — every
difference is ambiguous between the fix and the regression, and the
differential harness reports both identically. Improvements are written down
as a follow-up list and shipped after parity is proven.

## Start from the parity contract, not from the code

Before any Rust is written, the contract answers four questions: what the
unit of parity is (a CLI invocation, a library function, an HTTP response, a
file artifact); which differences are acceptable (log wording, timing, map
iteration order, float formatting); which are not (any observable output a
caller can branch on); and how parity is measured — the full form in
`PARITY-CONTRACT.md`. A port without a written contract does not have a
definition of done, so it finishes when someone gets tired.

## Five phases, in order

| Phase | Ends when |
|---|---|
| 1. Inventory and seam | The boundary the Rust will live behind is named, and the call sites crossing it are counted |
| 2. Characterize | The existing behaviour is captured as executable tests — against the source implementation, not the intended one |
| 3. Port leaf-first | The lowest-dependency module is in Rust, called through the seam, with both implementations still present |
| 4. Run both | Every input reaching the seam goes through both implementations and the outputs are compared |
| 5. Cut over and delete | Traffic goes to Rust only, and the source implementation is deleted rather than left as a dead fallback |

Phase 2 characterizes the behaviour that exists, bugs included — a test that
asserts the intended behaviour is a bug report disguised as a test. Phase 5
is not optional: a source implementation left in place stops being maintained
and starts being a lie about what runs; the depth on each phase is in
`PHASES.md`.

## Decide the end state before the seam

Three end states; the choice governs everything downstream — the seam, the
contract, the verification, whether bindings are deliverable or scaffold:

| End state | What ships | Bindings |
|---|---|---|
| A. Replacement | A standalone Rust binary or crate; the source implementation is deleted | None, ever. The seam is a process, CLI, or network boundary |
| B. Rust core with a language binding as the product | A Rust engine plus a binding layer that stays — the package the existing consumers import is the deliverable | Permanent. The binding surface is public API: it gets semver, error-type mapping, packaging per platform, and its own docs |
| C. Bindings as scaffold | A standalone Rust binary or crate, reached through a binding layer that is deleted at cut-over | Temporary. Built to be thrown away, and phase 5 is not done until it is gone |

B and C are not the same work, and conflating them is the most expensive
mistake here. Scaffold bindings may be crude because they die; product
bindings are a public surface that outlives the port. Ask which one is
wanted — a user porting a CLI to Rust usually wants A, and handing them a
native extension module answers a question nobody asked. The answer goes in
the parity contract, because it changes what the unit of parity is: for A
the unit is an invocation or a request; for B it is the binding signature
the existing callers already call.

## Pick the incremental strategy from the seam, not from taste

| Strategy | Reach for it when |
|---|---|
| In-place FFI — Rust compiled into the existing build and called across a language boundary | The source language has a cheap, stable FFI story and the seam is a function call |
| Strangler at a process boundary — the Rust binary takes traffic for one route, endpoint, or subcommand at a time | The seam is already a process, socket, or CLI boundary; the languages do not interoperate cheaply |
| Whole-unit replacement | The unit is small enough to port and validate in one sitting — a single CLI tool, one library with a narrow surface |

The FFI mechanics — which crate, which build integration, which header
generator — sit in the per-language skills.

## Parity is proven, not asserted

The evidence is both implementations running over the same inputs and
agreeing. Building that harness is `/rust-testing`; this skill decides what
it has to cover — every input class the contract names, including the error
paths, which are the ones a port silently narrows — and the harness runs in
CI from phase 3 onward, not once at the end, because a difference found six
modules later cannot be attributed.

## What is deliberately not ported

Dead code, workarounds for limitations the source language had and Rust does
not, and abstraction layers that existed to work around the source type
system — each a judgment call written down in the contract, not made
silently mid-file. The inverse error is worse and more common: porting the
abstraction rather than the behaviour, so a five-layer class hierarchy
becomes five Rust traits nobody needs.

## Where the target-side judgment goes

This skill never decides what the Rust should look like. Expression shape is
`/idiomatic-rust`; a `clone` added to satisfy the borrow checker mid-port is
`/ownership-not-clone`; what a fallible path returns is `/rust-errors`;
whether a state should be constructible at all is `/type-driven-design`; the
public surface of the new crate is `/rust-api-design`; async and cancellation
are `/async-rust`; any `unsafe` in an FFI shim is `/unsafe-rust`; the review
pass over a ported diff is `/rust-code-review`. The deferral matters most
here: mid-port is exactly when an agent reaches for `clone` and `unwrap` to
make a translation compile, and those two are the signature of a port that
will read like its source forever. Separate the domain aspects from the
language aspects before writing the Rust; a construct that exists only for
a source-language limitation is not ported; structural similarity to the
source is a signal to re-examine — the entry is in `ANTIPATTERNS.md`.

## Size the port to the source

Behave like the source on the inputs it actually receives, and let `std`
cover the rest rather than rebuilding the source runtime; where `std`
diverges on rare input, say so in the notes. Expose the same public items
plus the conventional trait impls, keep the algorithm unless it is wrong,
and read code size (tests and comments left out) as a warning light: close
to the source for C and C++, often two to three times for Python,
JavaScript, and TypeScript, and suspect beyond that. Tens of
representative inputs, error paths included, are enough to judge parity;
the habits and their fixes are in `ANTIPATTERNS.md`.

## Leave notes for the reviewer

Ship `PORTING.md` (or the file name the user gives) beside the code: item
correspondence, test correspondence, intended divergences, quirks kept
intact, follow-ups, and verification. It is the reviewer-facing companion to the
parity contract, not a second copy of it; the layout is in
`PARITY-CONTRACT.md`.

## Formatting

Run `cargo fmt` only on files the port created. Do not reformat the source
or Rust files you were not asked to change; if `cargo fmt --check` flags
untouched files, leave them and mention it in the notes.

## Anti-patterns

The top three: transliteration, big-bang rewrite, and improving while
porting; the full list, with the tell for each, is in `ANTIPATTERNS.md`.

## Verification

Run these yourself and fix what they report:

```bash
cargo build --all-targets --all-features
cargo test --all-features        # includes the differential and characterization tests
cargo clippy --all-targets --all-features   # add -- -D warnings only if the target repo has no lint config
rustfmt --check <files the port created>   # never reformat files outside the port
```

Run the source tests too when the source toolchain is available, and
compare results with the Rust tests on the same inputs. Then run the
differential harness over the recorded corpus and report the count of
inputs compared and the count of differences, not a pass/fail. Zero
differences over nine inputs is not parity, and a report that hides the
denominator hides that. Whatever could not run goes in the verification
section of `PORTING.md` as a plain statement.

---
name: port-from-typescript
description: Port TypeScript or JavaScript into Rust — construct mapping against runtime semantics, the traps (every number is an f64, two kinds of absent, structural typing, regex feature gaps), and the napi-rs and wasm-bindgen boundaries. Use when porting, rewriting, or migrating TypeScript, JavaScript, Node, Deno, Bun, Express, or a JS CLI or library into Rust, when replacing a hot JS module with a native addon or WebAssembly, or when the user asks how a TypeScript or JavaScript construct translates to Rust.
---

# Port from TypeScript

## A construct mapping and two boundaries, nothing else

This skill maps the JavaScript runtime to Rust and owns the two
boundaries, napi-rs and wasm-bindgen. The parity contract, the
phases, and the anti-patterns are `/port-to-rust`. TypeScript and
JavaScript are one skill because they are one runtime: the types
are erased before anything runs, so the mapping is the same and
the annotations are evidence about intent, not guarantees about values.

## The end state decides whether a binding layer appears at all

`/port-to-rust` names three end states, and this skill asks rather than
assumes.

| End state | In TypeScript and JavaScript terms | Binding layer |
|---|---|---|
| A. Replacement | A Rust binary or crate takes over; nothing imports it from JavaScript afterwards, and the seam is the CLI, route, or worker that already exists | Neither napi-rs nor wasm appears |
| B. Rust core, the npm package is the product | The module keeps its name and its exported signatures; the engine underneath becomes Rust | Permanent public surface — signatures, error types, prebuilds per platform, semver |
| C. Scaffold | The port ends standalone, but JavaScript calls the Rust module while the migration is under way | Temporary, and deleted at cut-over |

## Two boundaries, and the target decides which

Under B or C: Node, Deno, and Bun take a native addon through
napi-rs; browsers and edge runtimes take WebAssembly through
wasm-bindgen. They are not interchangeable: wasm has no threads by
default, no filesystem, a serialization cost at every call, and a
hard cap on what crates will compile. Choosing the wrong one is a
rewrite, not a refactor. Mechanics in `BOUNDARY.md`.

## The traps that break parity silently

| Trap | What actually differs |
|---|---|
| Every `number` is an `f64` | There is no integer type. Above 2⁵³ values lose precision silently, and bitwise operators coerce to `i32` first — so `x \| 0` is a documented truncation the port must reproduce or deliberately drop. Decide per field: `i64`, `f64`, or `i32`, and record which in the contract |
| Two kinds of absent | `undefined` and `null` are distinct, and most codebases use both without a rule. Rust has one `Option`, so each field needs a decision, and JSON round-tripping makes it observable — `serde` must be told whether a missing key and a `null` key are the same thing |
| Sorting | `Array.prototype.sort` with no comparator sorts by UTF-16 string conversion, so `[10, 9].sort()` is `[10, 9]`. A port that uses a numeric sort produces a different, *better*, and non-parity result |
| Regex | JavaScript regexes use backtracking and support lookaround and backreferences; the `regex` crate does not. Any source pattern using them needs a different crate or a restructured matcher, and this is found at port time, not at review time |
| Exceptions carry anything | `throw` accepts any value, and `catch` receives it untyped. Mapping to `Result` means naming the error cases the source never named — `/rust-errors` — and the ones that were thrown from library code are the ones no test covers |

## Mapping, in one line

`MAPPING.md` holds the full table; a mapping row is a starting
point, not a rewrite rule. Read the runtime values, not the
annotations: the type was erased before anything ran, so `any`, an
`as` cast, and an unchecked JSON boundary are unknown input.

## Unions are the win, and they are `/type-driven-design`

A discriminated union with a `kind` field is a Rust enum, and
translating it is where a TypeScript port stops reading like
TypeScript. A non-discriminated union (`string | number`) is a
design question the source deferred and the port must answer.
Structural typing maps to a trait only with several implementations;
an `interface` with one implementing type is a `struct`.

Objects carry the same judgment: a plain object with known keys is
a `struct`; `Record<string, T>` with a dynamic key set is a
`HashMap`; `Map` preserves insertion order where `HashMap` does not,
so ordered iteration means `IndexMap` or `BTreeMap`. Getting this
wrong shows up as reordered JSON output, which is a contract question.

## The test suite is the corpus

Jest or Vitest cases are characterization input, not the parity
contract. JavaScript suites are especially thin on the coercion
edges — `""`, `0`, `NaN`, `undefined` versus a missing key — exactly
where a port narrows behaviour. Harness shapes are `/rust-testing`.

## The event loop was doing work you now have to do

Single-threaded execution meant shared mutable state was safe by
construction; in Rust the same structure raises `Send`/`Sync`
questions, and the honest answer is often that the state should
not have been shared. `async` maps to `tokio` — `/async-rust` —
the shape differs: a JavaScript Promise is eager, a Rust future is
lazy until awaited, so code that fired a promise and did not await
it did run, and its Rust translation does not.

## Verification

```bash
cargo test --all-features
cargo clippy --all-targets --all-features   # add -- -D warnings only if the target repo has no lint config
npm test                                     # the existing suite still passes against the module being replaced
npm run build && node -e "require('./index.node'); ..."   # end states B and C only — or the wasm equivalent, from the JS side
```

Under end state A the last line does not exist and the differential
harness runs process-to-process; say so rather than leaving a
command that does not apply.

Then the differential run with its denominator, plus the
language-specific corpus requirement: at least one case per trap —
a number above 2⁵³, a `null` where `undefined` also occurs, an
unsorted numeric array, a regex input that used lookahead, and a
thrown non-`Error` value.

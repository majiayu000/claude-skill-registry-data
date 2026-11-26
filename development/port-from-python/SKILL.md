---
name: port-from-python
description: Port Python into Rust — construct mapping, the semantic traps (integer width, floor division, str versus bytes, exceptions to Result), and the seam, which is a process boundary for a standalone replacement and PyO3 when Python keeps calling the code. Use when porting, rewriting, or migrating Python, CPython, Django, Flask, FastAPI, NumPy, or a Python CLI into Rust, when replacing a Python tool with a Rust binary or a hot Python module with a native extension, or when the user asks how a Python construct translates to Rust.
---

# Port from Python

## A construct mapping and a boundary, nothing else

This skill maps Python to Rust and owns the PyO3 boundary. The parity
contract, the five phases, and the anti-patterns are `/port-to-rust`, which
runs first and stays running through the port.

## The end state decides whether PyO3 appears at all

`/port-to-rust` names three end states, and this is where the choice bites
hardest, because Python has the cheapest FFI story and the easiest to reach
for uninvited. This skill asks rather than assumes.

| End state | In Python terms | PyO3 |
|---|---|---|
| A. Replacement | A Rust binary or crate replaces the Python entirely; the seam is the CLI, the HTTP route, or the queue consumer that already exists | Never appears |
| B. Rust core, Python package is the product | The importable package keeps its name and its signatures; the engine underneath becomes Rust | Permanent public surface — signatures, exception types, wheels per platform, semver |
| C. Scaffold | The port ends standalone, but Python calls the Rust module while the migration is under way | Temporary, and deleted at cut-over |

## When there are bindings, the Python seam is unusually good

Under B or C, a Rust extension module built with PyO3 and packaged with
maturin is importable from the existing Python with no call-site change
beyond the import, which makes "port the hot leaf module first, keep the
app in Python" a genuinely incremental path rather than a euphemism. Under
A none of that applies and the seam is a process boundary — the strangler
strategy in `/port-to-rust`; mechanics for both are in `BOUNDARY.md`.

## The traps that break parity silently

The body carries these five because each one produces a port that passes a
naive test suite and is wrong; the full table is `MAPPING.md`.

| Trap | What actually differs |
|---|---|
| Integer width | Python `int` is arbitrary precision. `i64` silently changes behaviour at 2⁶³, and Rust panics in debug and wraps in release. Decide per field: `i64`/`i128` with a documented range, `u64` where the domain is non-negative, or `num-bigint` where the source genuinely relies on unbounded size |
| Floor division and modulo | Python `//` floors toward negative infinity and `%` takes the sign of the divisor; Rust `/` truncates toward zero and `%` takes the sign of the dividend. `-7 // 2` is `-4` in Python and `-7 / 2` is `-3` in Rust. Use `div_euclid`/`rem_euclid` when the source relied on the Python rule |
| `str` versus `bytes` | Python `str` indexes and slices by code point; Rust `String` is UTF-8 and indexes by byte, and slicing on a non-boundary panics. `bytes` is `Vec<u8>`/`&[u8]`. Every `s[i]` in the source is a decision, not a translation — most become `.chars().nth(i)` only if the source really meant code points |
| Truthiness | `if x:` is false for `0`, `""`, `[]`, `{}`, `None`, and any object with a falsy `__len__`. Rust has no such coercion, so each site becomes an explicit predicate — and getting one wrong changes a branch nobody tests |
| Exceptions crossing layers | A Python exception propagates through every frame that did not catch it, including frames that were never written with failure in mind. Rust makes every propagation point visible with `?`, which surfaces error paths the source never had a name for. What the error type should be is `/rust-errors` |

## Mapping, in one line

`MAPPING.md` holds the full table; a mapping row is a starting point, not a
rewrite rule. `dict` becomes a `HashMap` when the key set is dynamic and a
`struct` when the source was using a dict as a record with fixed keys —
which most Python code is. The single highest-value change in a Python
port is turning stringly-keyed dicts into structs and enums, and the
decision belongs to `/type-driven-design`.

## Duck typing is not a trait

A function that accepts "anything with `.read()`" maps to a trait bound
only when there are several implementations; with one caller and one type,
it maps to that type. Porting every duck-typed parameter into a trait
reproduces an abstraction the source never had — the "porting the
abstraction" anti-pattern in `/port-to-rust`.

## The test suite is the corpus

An existing `pytest` suite is characterization material: the cases are
inputs, the assertions are the recorded behaviour. It is not the parity
contract and it is not complete — the error paths and the edge cases are
where a Python suite is thinnest and where a port narrows behaviour. Harness
shapes are `/rust-testing`; what has to be covered is `/port-to-rust`.

## Async, if the source has it

`asyncio` maps to `tokio`, but the trap is different: Python coroutines
are single-threaded by default, so shared mutable state safe under one
event loop becomes a `Send`/`Sync` question. Blocking work hidden inside
an `async def` is the same defect in both languages — `/async-rust`.

## Verification

Both sides:

```bash
cargo test --all-features
cargo clippy --all-targets --all-features   # add -- -D warnings only if the target repo has no lint config
python -m pytest                             # the existing suite still passes against the module being replaced
maturin develop && python -c "import <module>; ..."   # end states B and C only — the extension imports and answers from the Python side
```

Under end state A the last line does not apply: nothing imports the module
from Python, and the differential harness runs process-to-process — the
same argv and stdin through both implementations, with stdout, stderr, and
exit codes compared.

Then the differential run over the recorded corpus, reported with its
denominator, plus the Python-specific check: inputs that cross the trap
boundaries above — a negative numerator with `//`, an integer past 2⁶³,
a non-ASCII string sliced mid-character, an empty container in a
truthiness branch. A corpus that never crosses those has not tested the
port, it has tested the happy path.

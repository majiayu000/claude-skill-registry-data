---
name: python-doctest-patterns
description: >
  Use this when authoring an Examples block in a public Python SDK docstring,
  reviewing a docstring that lacks runnable examples, wiring pytest to discover
  doctests, or fixing a doctest broken by a signature change. Covers Google-style
  Examples placement, # doctest: +SKIP for I/O-bound calls, ELLIPSIS and
  NORMALIZE_WHITESPACE flags, multi-line continuations and <BLANKLINE>, exception
  expected-output form, README doctests via --doctest-glob, and pyproject.toml
  addopts wiring for --doctest-modules.
  Triggers: doctest, Examples:, >>>, +SKIP, +ELLIPSIS, +NORMALIZE_WHITESPACE, --doctest-modules, --doctest-glob, BLANKLINE, IGNORE_EXCEPTION_DETAIL.
---

# python-doctest-patterns (v1.1.1)

## Rationale

Every public function in a Python SDK should ship at least one runnable example. The example serves three constituencies: humans reading the docstring (it's a 5-line how-to), `mypy` (the example exercises real types), and the test suite (the example IS a test, run via `pytest --doctest-modules`). Get this triple-purpose right and the SDK ships documentation that cannot lie — every code change that breaks an example breaks CI.

Python's `doctest` module is the runnable-example primitive. Its quirks (whitespace exact match, line endings, `<BLANKLINE>`) are surmountable; this skill describes the patterns that work.

This skill is cited by `documentation-agent-python` (M6 Examples block authorship), `code-reviewer-python` (review-criteria docstring section), `sdk-api-ergonomics-devil-python` (E-7 missing Examples), `sdk-convention-devil-python` (C-11), and `python-sdk-config-pattern` (Config Examples block).

## CI Wiring (READ THIS FIRST — the rest of the skill is moot without it)

**Examples blocks are only worth writing if the build runs them.** A docstring example whose runtime is never invoked is documentation that can lie — and over time, will. The whole rationale of this skill ("the example IS a test") is forfeited the moment CI fails to discover and execute the doctests. Every Python adapter authored by this pipeline MUST wire `--doctest-modules` into its pytest invocation; without it, every Examples block this skill prescribes is decorative.

The wiring lives in `pyproject.toml` under `[tool.pytest.ini_options].addopts`. ONE of the following two forms MUST be present in every Python pack pyproject:

#### GOOD — minimal sufficient pyproject.toml addopts

```toml
[tool.pytest.ini_options]
addopts = [
    "--doctest-modules",       # discover and run >>> examples in package source
    "--doctest-glob=*.md",     # discover and run >>> examples in README and other markdown
    "-ra",                     # show short test summary for non-passing tests
]
testpaths = ["src", "tests", "README.md"]
doctest_optionflags = [
    "ELLIPSIS",
    "NORMALIZE_WHITESPACE",
    "IGNORE_EXCEPTION_DETAIL",
]
```

#### GOOD — alternative: dedicated test-doctest module (use ONLY if addopts cannot be modified)

```python
# tests/test_doctests.py
"""Run doctest on every public module of motadatapysdk.

Use this module ONLY if pyproject.toml addopts cannot include --doctest-modules
(e.g. addopts is owned by an upstream conftest the pack does not control).
Otherwise, prefer the addopts wiring — it is one line and runs everything.
"""
from __future__ import annotations

import doctest
import importlib
import pkgutil

import motadatapysdk


def test_all_module_doctests() -> None:
    failures = 0
    for modinfo in pkgutil.walk_packages(motadatapysdk.__path__, prefix="motadatapysdk."):
        module = importlib.import_module(modinfo.name)
        result = doctest.testmod(module, verbose=False)
        failures += result.failed
    assert failures == 0, f"{failures} doctest failures"
```

#### BAD — pyproject.toml without doctest discovery

```toml
[tool.pytest.ini_options]
addopts = ["-ra"]              # examples exist in source, but pytest never runs them
testpaths = ["tests"]
```

A pyproject without `--doctest-modules` is the same as having no examples — the build cannot detect drift. The example block reads correctly to a human, runs by hand if copy-pasted, *and silently rots over time as signatures change*. Defect SKD-003 in run `sdk-resourcepool-py-pilot-v1` shipped exactly this configuration: 9/9 public symbols carried fully-formed Examples blocks but `pyproject.toml` `addopts` omitted `--doctest-modules`. Coverage looked good (every public symbol had an example); the gate that would have caught a future signature drift was never wired up.

#### Asyncio-flavored examples interaction with `--doctest-modules`

Async examples cannot be run inline by `--doctest-modules` — pytest's doctest runner does not start an event loop. Two correct forms:

1. Mark the `asyncio.run(...)` line with `# doctest: +SKIP` so the example renders for humans but does not execute (see Rule 2 below). This is the standard idiom for the SDK's I/O-bound public surface.
2. Refactor the example to a sync result-display style (construction-only; no event loop). See Pattern B below.

Once `--doctest-modules` is wired, Rule 2's `+SKIP` directive becomes non-decorative — without `--doctest-modules`, `+SKIP` was meaningless because nothing was running anyway.

### Per-module enforcement note (added v1.1.1)

Rule 1 ("Every public symbol gets at least one Examples block") applies **per-module**, not per-package. Coverage of doctest examples should be uniform across every module in `src/<pkg>/`, not concentrated in one or two foundation modules (e.g., `utils.py` and `core.py`).

**Evidence from `motadata-nats-v1`**: that run landed 28 doctest examples across `src/motadata_nats/` but distribution was lopsided — `__init__.py` had 2, `utils.py` had 13, `core.py` had 12, `corenats.py` had 1, `jetstream.py` had 0, `stores.py` had 0. The TWO modules consumers most-often invoke directly (`jetstream` for Stream/Publisher/Consumer, `stores` for KVStore/ObjectStore) had ZERO runnable examples. Documentation-quality regressed sharply once a consumer left the foundation modules.

**Concrete prescription for documentation-agent-python at M6**:

1. Walk `pkgutil.iter_modules(<pkg>)` to enumerate every public module.
2. For each module, walk `inspect.getmembers(<mod>, predicate=inspect.isclass | inspect.isfunction)` and filter to public (non-`_`-prefixed) members.
3. Cross-reference with each member's `__doc__` for an `Examples:` block. Members lacking an `Examples:` block in a module that's part of the public API surface (i.e. listed in `__all__`) are M6 work-items. Per-module floor: if a module exports ≥3 public symbols, it MUST have ≥1 doctest example, even if some symbols are I/O-bound and need `+SKIP`.
4. Phase 4 `sdk-skill-coverage-reporter` SHOULD include a `coverage_per_module_doctests` table cross-referenced against `coverage-baselines.json::modules`.

**Caveat**: I/O-bound modules (corenats, jetstream, stores in this run's case) typically need `+SKIP` examples for any method that opens a connection. That's fine — `+SKIP`-marked examples still render for humans and still demonstrate the public API's typical shape. The point is to populate the `Examples:` block at all.

## Activation signals

- Authoring a docstring for any public function, method, or class.
- Reviewing a docstring without an `Examples:` block.
- README has code blocks that aren't tested.
- Documentation agent is M6-running and needs to populate doctest examples.
- A code change broke an Examples block — what's the right fix?
- A documentation review found ≥1 module in `src/<pkg>/` with zero `Examples:` blocks (added v1.1.1).

## Core rules

### Rule 1 — Every public symbol gets at least one Examples block

Per PEP 257 + Python pack convention C-11. The `Examples:` section sits at the bottom of the Google-style docstring, after `Returns:` / `Yields:` / `Raises:`.

```python
def parse_topic(topic: str) -> tuple[str, str]:
    """Split ``topic`` into (namespace, name).

    Args:
        topic: Topic string in ``namespace.name`` form.

    Returns:
        A 2-tuple ``(namespace, name)``.

    Raises:
        ValidationError: If ``topic`` does not contain exactly one ``.``.

    Examples:
        >>> parse_topic("orders.created")
        ('orders', 'created')

        >>> parse_topic("just-namespace")
        Traceback (most recent call last):
            ...
        motadatapysdk.errors.ValidationError: topic must contain exactly one '.'
    """
    if topic.count(".") != 1:
        raise ValidationError("topic must contain exactly one '.'")
    return tuple(topic.split("."))  # type: ignore[return-value]
```

The example exercises the happy path AND the error path. Both run when `pytest --doctest-modules` discovers the file.

### Rule 2 — `# doctest: +SKIP` for I/O-bound code

Async clients, HTTP calls, file I/O, anything depending on running infrastructure — these CANNOT execute as part of `pytest --doctest-modules`. Mark them skipped:

```python
class Client:
    """Async client for the motadata API.

    Examples:
        >>> import asyncio
        >>> from motadatapysdk import Client, Config
        >>> async def main() -> None:
        ...     async with Client(Config(base_url="https://x", api_key="k")) as c:
        ...         await c.publish("orders.created", b"payload")
        >>> asyncio.run(main())  # doctest: +SKIP
    """
```

`# doctest: +SKIP` applies to ONE statement (the line it's on). The example still appears in rendered docs (Sphinx, mkdocs, IDE hover) — humans see it, doctest does not run it. This is correct: the example's job is communication; it cannot also be an integration test.

Use SKIP sparingly. For pure functions (no I/O), the example MUST run. For mixed examples (setup is pure, the call is I/O), split:

```python
Examples:
    >>> cfg = Config(base_url="https://api.example.com", api_key="secret")
    >>> cfg.timeout_s
    5.0
    >>> async with Client(cfg) as c:  # doctest: +SKIP
    ...     await c.publish(...)
```

The first two lines run (pure construction); the third is skipped (network).

### Rule 3 — `# doctest: +ELLIPSIS` for outputs that include unstable parts

Memory addresses, timestamps, UUIDs, traceback line numbers, dict ordering before 3.7 (irrelevant on 3.12+) — anything whose exact value would make the test fragile. Use ELLIPSIS to match `...`:

```python
def make_session_id() -> str:
    """Return a fresh session UUID.

    Examples:
        >>> sid = make_session_id()
        >>> sid.startswith("session-")
        True
        >>> len(sid)
        44

    Or with ELLIPSIS:
        >>> make_session_id()  # doctest: +ELLIPSIS
        'session-...'
    """
```

The `True` / numeric assertion form is BETTER than ELLIPSIS — it tests an invariant. Reach for ELLIPSIS only when the invariant is hard to express in one line.

`# doctest: +ELLIPSIS` is per-statement. Or enable globally for a module via:

```python
__test__ = {}  # opt-in module-level doctest tweaks
```

Better: configure once via `pyproject.toml`:

```toml
[tool.pytest.ini_options]
doctest_optionflags = ["ELLIPSIS", "NORMALIZE_WHITESPACE"]
```

### Rule 4 — `# doctest: +NORMALIZE_WHITESPACE` for multi-line outputs

doctest matches output character-by-character, including spaces. NORMALIZE_WHITESPACE collapses runs of whitespace to a single space:

```python
def render_table(rows: list[Row]) -> str:
    """Render ``rows`` as a fixed-width table.

    Examples:
        >>> rows = [Row("alice", 30), Row("bob", 25)]
        >>> print(render_table(rows))  # doctest: +NORMALIZE_WHITESPACE
        | name  | age |
        | alice |  30 |
        | bob   |  25 |
    """
```

Without NORMALIZE_WHITESPACE, your alignment in the docstring must EXACTLY match the runtime output's alignment. With it, you can keep the docstring readable.

### Rule 5 — Multi-line examples use `... ` continuation

The continuation prompt is `... ` (three dots + space). Indentation under the prompt counts:

```python
def filter_records(records: list[Record], predicate: Callable[[Record], bool]) -> list[Record]:
    """Return records satisfying ``predicate``.

    Examples:
        >>> records = [
        ...     Record(id=1, type="a"),
        ...     Record(id=2, type="b"),
        ...     Record(id=3, type="a"),
        ... ]
        >>> result = filter_records(records, lambda r: r.type == "a")
        >>> [r.id for r in result]
        [1, 3]
    """
```

The blank line after `[1, 3]` (or end-of-docstring) ends the example. If you need a blank line WITHIN expected output, use `<BLANKLINE>`:

```python
    Examples:
        >>> print("hello\n\nworld")
        hello
        <BLANKLINE>
        world
```

### Rule 6 — Examples block is at the END of the docstring

Google-style ordering: Summary → Args → Returns → Yields → Raises → Examples → Notes. Examples last so doctest scanners can isolate the runnable portion.

```python
def thing(x: int) -> int:
    """Compute Y from X.

    Args:
        x: The input.

    Returns:
        Y, computed as ``x * 2``.

    Raises:
        ValueError: If ``x < 0``.

    Examples:
        >>> thing(3)
        6
    """
```

### Rule 7 — Class docstrings — Examples on the class, not on `__init__`

```python
class Cache:
    """Bounded in-memory cache.

    Args:
        max_size: Capacity bound.

    Examples:
        >>> cache: Cache = Cache(max_size=10)
        >>> cache.put("k", b"v")
        >>> cache.get("k")
        b'v'
    """
    def __init__(self, *, max_size: int = 1024) -> None:
        ...
```

The class docstring is what `help(Cache)` and IDE hover render. `__init__` is rarely user-facing.

### Rule 8 — README examples test via `pytest --doctest-glob`

`README.md` code blocks should be runnable:

````markdown
## Quick start

```python
>>> from motadatapysdk import Config
>>> cfg = Config(base_url="https://api.example.com", api_key="x")
>>> cfg.timeout_s
5.0
```
````

Run via:

```bash
pytest --doctest-glob='*.md' README.md
```

Wire into `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = ["--doctest-modules", "--doctest-glob=*.md"]
```

This makes the README a CI gate. README drift becomes a test failure.

### Rule 9 — `Examples:` plural; one block; multiple examples within

```python
# WRONG — duplicated headings, ambiguous parser intent
"""...

Example:
    >>> foo(1)
    1

Example:
    >>> foo(2)
    2
"""

# RIGHT — one Examples: block, multiple examples inside
"""...

Examples:
    >>> foo(1)
    1
    >>> foo(2)
    2

    Edge case — empty input::

    >>> foo(0)
    0
"""
```

Google-style uses `Examples:` (plural). Some doctest parsers also accept `Example:` (singular) but the convention for the Python pack is plural.

### Rule 10 — Examples MUST type-check

`mypy --strict` should pass on the example bodies. This catches "the example doesn't match the signature" drift:

```python
# WRONG — return type changed; example silently rotted
def fetch(self) -> Record:
    """Fetch the next record.

    Examples:
        >>> client.fetch()  # doctest: +SKIP
        b'\\x01\\x02'                # USED to return bytes; now Record
    """
```

The example's expected output drifted from the signature. mypy doesn't catch the doctest output, BUT `pytest --doctest-modules` runs the example and the assertion fails — which is the gate.

For examples that exercise the type system specifically:

```python
def take_records(records: list[Record]) -> int:
    """Return count of valid records.

    Examples:
        >>> records: list[Record] = [Record(id=1), Record(id=2)]
        >>> take_records(records)
        2
    """
```

Annotate the local name (`records: list[Record] = ...`) so mypy can verify the call site is type-correct, not just runtime-correct.

## Common patterns

### Pattern A — Pure function

```python
def normalize_topic(topic: str) -> str:
    """Strip whitespace and lowercase ``topic``.

    Args:
        topic: Raw topic string.

    Returns:
        Normalized form.

    Examples:
        >>> normalize_topic("  Orders.Created  ")
        'orders.created'
        >>> normalize_topic("PAYMENTS")
        'payments'
    """
    return topic.strip().lower()
```

### Pattern B — Construction-only (no I/O)

```python
@dataclass(frozen=True, kw_only=True)
class Config:
    """Configuration for the motadata client.

    Examples:
        >>> cfg = Config(base_url="https://x", api_key="k")
        >>> cfg.timeout_s
        5.0
        >>> cfg.max_retries
        3
    """
    base_url: str
    api_key: str
    timeout_s: float = 5.0
    max_retries: int = 3
```

### Pattern C — Async I/O (must SKIP)

```python
async def publish(self, topic: str, payload: bytes) -> None:
    """Publish ``payload`` to ``topic``.

    Args:
        topic: Destination topic.
        payload: Bytes to publish.

    Raises:
        NetworkError: On wire-level failure.

    Examples:
        >>> import asyncio
        >>> async def demo() -> None:
        ...     async with Client(Config(...)) as c:
        ...         await c.publish("orders.created", b"x")
        >>> asyncio.run(demo())  # doctest: +SKIP
    """
```

### Pattern D — Exception path

```python
def divide(a: int, b: int) -> float:
    """Return ``a / b``.

    Raises:
        ZeroDivisionError: If ``b == 0``.

    Examples:
        >>> divide(6, 2)
        3.0

        >>> divide(1, 0)
        Traceback (most recent call last):
            ...
        ZeroDivisionError: division by zero
    """
    return a / b
```

The `Traceback (most recent call last):` + `    ...` + final exception line form is the standard exception expected-output. Indentation matters; copy verbatim.

For SDK-defined exceptions, use the FULL dotted path:

```python
        >>> Config(base_url="ftp://x", api_key="k")
        Traceback (most recent call last):
            ...
        motadatapysdk.errors.ConfigError: base_url must start with http(s)://
```

### Pattern E — Async generator

```python
async def stream_events(self, topic: str) -> AsyncIterator[Event]:
    """Stream events from ``topic`` until cancelled.

    Examples:
        >>> async def demo() -> None:
        ...     async with Client(Config(...)) as c:
        ...         async for event in c.stream_events("topic"):
        ...             print(event)
        ...             break
        >>> asyncio.run(demo())  # doctest: +SKIP
    """
    ...
```

## BAD anti-patterns

```python
# 1. No example
def parse(data: bytes) -> Record:
    """Parse data."""                          # Examples: missing
    ...

# 2. Example that lies (output drifted from signature)
def fetch(self) -> Record:
    """Examples:
        >>> client.fetch()
        b'\\x01\\x02'                          # signature is Record, not bytes
    """

# 3. I/O example without SKIP
def publish(...):
    """Examples:
        >>> client.publish("topic", b"x")     # CI: connection refused
    """

# 4. Example with non-deterministic output
def now() -> str:
    """Examples:
        >>> now()
        '2026-04-28T15:32:11Z'                 # never matches
    """
# Use # doctest: +ELLIPSIS or check an invariant.

# 5. Hard-to-test alignment without NORMALIZE_WHITESPACE
def render() -> str:
    """Examples:
        >>> print(render())
        | a | b |  c   |                       # exact whitespace match needed

# 6. Example block named Example: (singular)
"""...
Example:                                       # parser may not auto-detect
    >>> foo(1)
    1
"""

# 7. Example placed before Args:
"""
Examples: ...                                  # wrong order
Args: ...
"""

# 8. README code block without runnable doctest
```python
client = Client(...)                           # plain code; no >>> prompt
```
# Add >>> so pytest --doctest-glob can run it.
```

## Tooling configuration

`pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = [
    "--doctest-modules",
    "--doctest-glob=*.md",
    "-ra",
]
testpaths = ["src", "tests", "README.md"]
doctest_optionflags = [
    "ELLIPSIS",
    "NORMALIZE_WHITESPACE",
    "IGNORE_EXCEPTION_DETAIL",                 # match exception type, not message
]
```

`IGNORE_EXCEPTION_DETAIL` makes the exception-message comparison fuzzy — the type must match but the message can drift. Useful when exception messages contain timestamps or UUIDs; otherwise pin the message exactly.

Run:

```bash
pytest --doctest-modules src/        # docstring examples
pytest --doctest-glob='*.md' .       # README examples
pytest                               # everything (with config above)
```

## Cross-references

- `python-pytest-patterns` — `pytest --doctest-modules` wiring.
- `python-mypy-strict-typing` — Examples should type-check.
- `python-sdk-config-pattern` — Config docstring shows `dataclasses.replace` example.
- `python-asyncio-patterns` — `# doctest: +SKIP` on every async example.
- `python-exception-patterns` — Traceback expected-output form for SDK exceptions.
- `sdk-convention-devil-python` C-11 — design-rule enforcement at D3.
- `documentation-agent-python` — M6 wave authors Examples blocks.

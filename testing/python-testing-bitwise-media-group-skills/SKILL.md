---
name: python-testing
description: Python test authoring and review with pytest. Use when writing, adding, generating, or reviewing Python tests or unit tests for a function, module, or class; running pytest or a single test (the -k flag and other invocation flags for a Makefile or CI); parametrizing test cases into the table-driven pattern; setting up pytest fixtures or using the built-in tmp_path, monkeypatch, or capsys; choosing between hand-written fakes and mock objects; asserting a function raises with pytest.raises; or adding property-based or fuzz tests to a Python parser, encoder, or validator with Hypothesis. Covers pytest conventions, fixtures, parametrization, fakes vs mocks, error-path testing, and Hypothesis property testing. Not for non-Python test frameworks (Jest, Go testing), type hints, ruff/linting, or scaffolding a project.
license: MIT
---

# Python testing conventions

`pytest` is the whole toolkit — plain `assert`, fixtures, parametrization, and Hypothesis for
property tests. No `unittest.TestCase` boilerplate, no assertion DSLs. Tests live in `tests/` and
run with `uv run pytest`.

## 1. Parametrize instead of repeating

One test, a row per case — the table-driven pattern. Adding a behavior is adding a row:

```python
import pytest

from myapp.kv import parse


@pytest.mark.parametrize(
    ("line", "want_key", "raises"),
    [
        ("a=b", "a", False),
        ("ab", None, True),       # missing separator
        ("=b", None, True),       # empty key
        ("a=", "a", False),       # empty value is fine
    ],
)
def test_parse(line: str, want_key: str | None, raises: bool) -> None:
    if raises:
        with pytest.raises(ValueError):
            parse(line)
    else:
        assert parse(line)[0] == want_key
```

Name each test for the behavior it pins down; `assert` directly — pytest rewrites it into a rich
failure message.

## 2. Fixtures for setup, built-ins first

Shared setup is a `@pytest.fixture`; teardown goes after a `yield`. Reach for the built-in fixtures
before inventing your own — `tmp_path` (a real temp directory), `monkeypatch` (patch env/attrs,
auto-reverted), `capsys` (capture stdout/stderr). Put cross-file fixtures in `tests/conftest.py`.

## 3. Fakes over mocks

Prefer a small hand-written fake — a class with canned returns satisfying the consumer's `Protocol`
(see `python-typing`) — to `unittest.mock.MagicMock`. Assert on observable behavior (return values,
recorded state), not on which methods were called. Use `monkeypatch` to swap a dependency at a
boundary; reserve `mock` for third-party seams you do not own, and avoid asserting call counts —
they couple tests to implementation.

## 4. Property tests with Hypothesis

Every parser, encoder, or validator handling untrusted input gets a Hypothesis test — the analogue
of Go's native fuzzing. Generate inputs and assert the invariants that must hold for *any* input
(no crash, round-trips, never emits an invalid result):

```python
from hypothesis import given, strategies as st

from myapp.kv import parse


@given(st.text())
def test_parse_never_crashes(s: str) -> None:
    try:
        key, _ = parse(s)
    except ValueError:
        return  # rejecting bad input is fine
    assert key != ""  # but a parsed key is never empty
```

Hypothesis shrinks any failing case to a minimal example and records it, so the regression replays
on every run. Use `@given` with explicit strategies; seed known tricky cases with `@example`.

## 5. Invocations

```sh
uv run pytest                 # the suite (unit + property tests)
uv run pytest -q              # quiet, for the make/CI gate
uv run pytest -k name         # run tests matching an expression
uv run pytest --cov=myapp     # coverage (needs the pytest-cov dev dependency)
```

`make test` runs `uv run pytest` (see `python-project`); CI runs the same (see `python-release`).
For the interfaces that make code testable see `python-typing`; for house style see `python-style`.

---
name: pytest
description: Testing Python code with pytest — fixtures, parametrization, markers, mocking, coverage, and configuration. Use when writing or running Python tests, setting up a test suite, debugging failing tests, adding fixtures or parametrized cases, measuring coverage, or configuring pytest in pyproject.toml. Pairs with test-driven-development for the workflow/methodology.
---

# pytest — Python testing

## Overview

`pytest` is the de-facto Python test framework: plain `assert`, powerful fixtures, and a
rich plugin ecosystem. This skill is the **tool reference**; for the red-green-refactor
*methodology* see [[test-driven-development]].

```bash
uv run pytest                 # or: pytest   (see modern-python for uv)
pytest -q                     # quiet
pytest -x --ff                # stop at first failure, run last-failed first
pytest -k "auth and not slow" # filter by name expression
pytest path/test_mod.py::test_login   # one test
pytest -m "not slow"          # filter by marker
pytest -vv -s                 # verbose, don't capture stdout (for debugging)
```

## Test structure & assertions

```python
# test_calc.py — files test_*.py, functions test_*, classes Test*
from calc import add

def test_add():
    assert add(2, 3) == 5

def test_divide_by_zero():
    import pytest
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

Use bare `assert` — pytest rewrites it to show rich diffs. For approximate floats use
`pytest.approx(0.1 + 0.2) == 0.3`.

## Fixtures — setup/teardown and shared state

```python
import pytest

@pytest.fixture
def db():
    conn = connect(":memory:")
    yield conn          # everything before yield = setup; after = teardown
    conn.close()

def test_query(db):     # request the fixture by parameter name
    assert db.execute("select 1").fetchone() == (1,)

@pytest.fixture(scope="session")   # function (default) | class | module | session
def heavy_model():
    return load_model()
```

Put shared fixtures in `conftest.py` (auto-discovered, no import needed). Built-in fixtures
worth knowing: `tmp_path` (per-test temp dir), `monkeypatch` (patch env/attrs/cwd safely),
`capsys` (capture stdout/stderr), `caplog` (capture logging).

## Parametrize — table-driven tests

```python
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

Each row is a separate reported test. Stack `@parametrize` decorators for a cartesian
product. Use `pytest.param(..., marks=pytest.mark.xfail)` to mark individual rows.

## Mocking

Prefer `monkeypatch` for env/attrs; use `unittest.mock` (or the `pytest-mock` `mocker`
fixture) for call assertions:

```python
def test_fetch(monkeypatch):
    monkeypatch.setenv("API_KEY", "test")
    monkeypatch.setattr("mymod.requests.get", lambda url, **k: FakeResp(200))

def test_called(mocker):                 # pytest-mock
    spy = mocker.patch("mymod.send_email")
    do_signup("a@b.com")
    spy.assert_called_once_with("a@b.com")
```

Patch where the name is *used*, not where it's defined (`mymod.requests.get`, not
`requests.get`).

## Config & coverage (pyproject.toml)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra -q --strict-markers"
markers = ["slow: long-running tests", "integration: needs external services"]

[tool.coverage.run]
branch = true
source = ["mypackage"]
```

```bash
uv run pytest --cov=mypackage --cov-report=term-missing
```

`--strict-markers` turns typos in `@pytest.mark.*` into errors — always enable it.

## Gotchas

- **Test isolation:** never rely on test execution order or shared mutable globals; use
  fixtures so each test is independent (and `pytest-randomly`/`-p no:randomly` to detect
  hidden coupling).
- **`assert` stripped under `-O`:** don't run the suite with `python -O`.
- **async tests** need `pytest-asyncio` (`@pytest.mark.asyncio`) or `anyio`.
- **Slow collection / import errors** usually mean a missing `__init__.py`/`conftest.py`
  layout issue or import-time side effects — keep module top-level cheap.

## Related

Methodology in [[test-driven-development]] and [[verification-before-completion]];
property-based testing in [[property-based-testing]]; project setup in [[modern-python]].

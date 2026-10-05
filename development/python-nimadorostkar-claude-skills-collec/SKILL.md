---
name: python
description: Use when writing, reviewing, or modernizing Python 3.11+ code. Produces fully type-annotated modules, async I/O, dataclasses and protocols, pytest suites, and a lint/type gate built on ruff and mypy --strict.
metadata:
  category: languages
  version: 1.0.0
  tags: [python, typing, async, pytest, mypy, ruff]
---

# Python

## Purpose

Write production Python that is type-safe, async-first, and testable. This skill sets a single quality bar — annotated, linted, tested — and applies it consistently to new code and to code being modernized.

## When to Use

- Writing new Python modules, packages, or services.
- Adding type coverage to an untyped or partially typed codebase.
- Converting blocking I/O to `asyncio`, or debugging async behavior.
- Standing up a pytest suite, fixtures, or parametrized tests.
- Modernizing Python 2-era or pre-3.10 idioms.

## Capabilities

- Full type annotation, including generics, `Protocol`, `TypedDict`, and `ParamSpec`.
- Async design: task groups, timeouts, cancellation, structured concurrency.
- Data modeling with `dataclasses`, `enum`, and Pydantic when validation is needed.
- Test authoring: fixtures, factories, mocking, property-based tests via Hypothesis.
- Tooling configuration: `pyproject.toml`, ruff, mypy, uv or Poetry.
- Profiling and hot-path optimization.

## Inputs

- Source files or a package path.
- Target Python version (default: 3.12).
- Existing tooling config, if any.
- Runtime constraints: sync vs async, framework, deployment target.

## Outputs

- Type-annotated source that passes `mypy --strict`.
- A pytest suite with meaningful assertions, not coverage padding.
- A `pyproject.toml` section configuring ruff and mypy.
- A short summary of behavioral changes when refactoring.

## Workflow

1. **Survey** — Read the module and its imports. Identify the runtime model (sync, async, threaded) and existing conventions. Do not fight established conventions without a reason.
2. **Model the data** — Define dataclasses, enums, and protocols before writing logic. Type the boundaries first.
3. **Implement** — Write the smallest correct version. Prefer standard library over dependencies.
4. **Test** — Cover the contract and the failure modes, not the implementation details.
5. **Gate** — Run `ruff check --fix`, `ruff format`, `mypy --strict`, `pytest`. Fix each failure and re-run until all four are clean.

## Best Practices

- Use `X | None`, not `Optional[X]`. Use `list[str]`, not `List[str]`.
- Never use a bare `except:`. Catch the narrowest exception that can actually be raised.
- Raise domain-specific exceptions; do not signal failure with `None` return values.
- Use `pathlib.Path` for every filesystem path.
- Never mutate a default argument. Use `field(default_factory=...)`.
- Guard async code with explicit timeouts; an un-timed `await` on a network call is a latency bug waiting to happen.
- Log with the `logging` module and structured extras — never `print` in library code.

## Examples

**Typed, async, cancellation-safe fetch:**

```python
import asyncio
from dataclasses import dataclass

import httpx


@dataclass(frozen=True, slots=True)
class Quote:
    symbol: str
    price: float


class QuoteUnavailable(Exception):
    """Raised when the upstream cannot serve a quote."""


async def fetch_quotes(symbols: list[str], *, timeout: float = 5.0) -> list[Quote]:
    async with httpx.AsyncClient(timeout=timeout) as client:
        async with asyncio.TaskGroup() as tg:
            tasks = {s: tg.create_task(client.get(f"/quote/{s}")) for s in symbols}

    quotes: list[Quote] = []
    for symbol, task in tasks.items():
        response = task.result()
        if response.status_code != 200:
            raise QuoteUnavailable(symbol)
        quotes.append(Quote(symbol=symbol, price=response.json()["price"]))
    return quotes
```

**Test that covers the contract and the failure:**

```python
import pytest


@pytest.mark.asyncio
async def test_fetch_quotes_raises_on_upstream_error(mock_client):
    mock_client.get.return_value.status_code = 503
    with pytest.raises(QuoteUnavailable, match="AAPL"):
        await fetch_quotes(["AAPL"])
```

## Notes

- `TaskGroup` requires Python 3.11+. On 3.10, use `asyncio.gather(..., return_exceptions=True)` and re-raise explicitly.
- `mypy --strict` on a large legacy codebase is a project, not a task. Enable it per-module with `disallow_untyped_defs` and expand the surface gradually.
- Prefer `uv` for new projects; it is materially faster than Poetry and pip for resolution and installs.

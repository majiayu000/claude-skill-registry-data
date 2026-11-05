---
name: test
description: Write pytest tests for a ConvoPilot module — covers happy path, edge cases, and error paths. Always runs them to confirm they pass.
argument-hint: "<file path or F-number to write tests for, e.g. services/simulation/ or F4>"
allowed-tools: Read Glob Grep Write Edit Bash(poetry run pytest *)
---

You are writing tests for ConvoPilot. The owner is non-technical — explain what each test does in plain English.

Write tests for: **$ARGUMENTS**

## Core principles
- **Tests verify requirements, not implementation.** Each test maps to a behaviour from @docs/PRD.md — not just "does the function run".
- **Never mock what you don't own.** Mock LLM calls, external HTTP calls, and DB sessions. Never mock the module being tested.
- **Run every test before reporting.** Only report a test as done if it actually passes.
- **One test file per module.** Location: `service-one/src/tests/test_<module_name>.py`

---

## Step 1 — Read the module and requirements

1. Read the file(s) to be tested
2. Find the F-number in @docs/PRD.md this module covers
3. List the behaviours to test — one bullet per test case

---

## Step 2 — Write tests

### Structure for every test file

```python
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch

# Import the module under test
from api.services.<module> import <ClassName>

# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def mock_llm_interface():
    """Mock LLM interface — never call real LLM in tests."""
    mock = AsyncMock()
    mock.complete.return_value = "mocked response"
    return mock

@pytest.fixture
def mock_db_session():
    """Mock async DB session."""
    return AsyncMock()

# ── Happy path ─────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_<behaviour>_happy_path():
    """Plain English description of what this test verifies."""
    # Arrange
    ...
    # Act
    ...
    # Assert
    ...

# ── Edge cases ─────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_<behaviour>_empty_input():
    ...

# ── Error paths ────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_<behaviour>_downstream_failure():
    ...
```

### Required coverage per module

| Scenario | What to test |
|---|---|
| Happy path | Valid input → expected output, correct model fields returned |
| Missing required field | Pydantic raises `ValidationError` |
| LLM failure | LLM raises exception → function handles gracefully, doesn't crash |
| DB error | DB session raises → function returns error, session is closed |
| HTTP timeout | External agent times out → session marked `failed`, not stuck `running` |
| Empty/edge input | Empty string, 0 turns, null optional fields |

---

## Step 3 — Run all tests

```bash
poetry run pytest service-one/src/tests/test_<module>.py -v
```

Show the owner the output. If any test fails, fix it before moving on.

---

## Step 4 — Explain what was tested (plain English)

Tell the owner:
- How many tests were written and what they cover
- Which PRD requirement (F-number) they verify
- What would break in the product if these tests started failing

---

## Step 5 — Show git commands (never execute)

```bash
git add service-one/src/tests/test_<module>.py
git commit -m "test(F<number>): add tests for <module>"
git push origin <current-branch>
```

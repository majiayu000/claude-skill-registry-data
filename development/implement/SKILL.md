---
name: implement
description: Guided workflow for implementing features with quality gates. Use when building new features - includes spec, test-first, implementation, and verification steps.
---

# IMPLEMENTATION — TDD STRICT MODE PROTOCOL

> **Agent**: ENGINEER
> **Prerequisite**: Gate 4 (Planning) COMPLETE
> **Mode**: Test-Driven Development (MANDATORY)

---

## INVOCATION

```
/implement           # Show current task queue
/implement W1.1      # Implement specific task
/implement next      # Pick next task from roadmap
```

---

## TDD STRICT MODE

```
┌────────────────────────────────────────────────────────────────────┐
│                     TDD STRICT MODE                                 │
│                                                                    │
│  1. TEST STUB MUST EXIST                                           │
│  2. TEST MUST FAIL FIRST (Red)                                     │
│  3. WRITE MINIMAL CODE TO PASS (Green)                             │
│  4. REFACTOR IF NEEDED (Refactor)                                  │
│  5. COMMIT                                                         │
│                                                                    │
│  ❌ Writing code without test = PROTOCOL VIOLATION                 │
│  ❌ Test passes before code = SOMETHING IS WRONG                   │
│  ❌ Skipping refactor = TECHNICAL DEBT                             │
└────────────────────────────────────────────────────────────────────┘
```

---

## IMPLEMENTATION WORKFLOW

### Phase 1: Load Task

```markdown
## TASK LOADING

Task ID: W1.1
Description: Implement Core Types

### Traces
- SPEC: S001
- INVARIANTS: INV001, INV002
- TESTS: T001.1, T001.2, T001.3

### Pre-Conditions
✅ Test stubs exist (T001.1, T001.2, T001.3)
✅ Architecture defined (GATE 1)
✅ Specification complete (GATE 2)

### Acceptance Criteria
- [ ] T001.1 passes
- [ ] T001.2 passes
- [ ] T001.3 passes
- [ ] mypy --strict passes
- [ ] ruff check passes
- [ ] Coverage ≥90% on new code
```

---

### Phase 2: Red Phase — Make Test Fail

```python
# 1. Find the test stub
# tests/unit/test_detector.py

@pytest.mark.skip(reason="Stub - implement with S001")
def test_valid_package_name_passes(self):
    """
    SPEC: S001
    TEST_ID: T001.1
    """
    result = validate_package("flask-redis-helper")
    assert result is not None

# 2. Remove the skip decorator
def test_valid_package_name_passes(self):
    """
    SPEC: S001
    TEST_ID: T001.1
    """
    result = validate_package("flask-redis-helper")
    assert result is not None

# 3. Run the test
pytest tests/unit/test_detector.py::test_valid_package_name_passes -v

# 4. VERIFY IT FAILS
# Expected: ImportError or AttributeError (function doesn't exist)
```

**If test passes without code**: STOP. Something is wrong.

---

### Phase 3: Green Phase — Write Minimal Code

```python
# src/phantom_guard/core/detector.py

"""
IMPLEMENTS: S001
INVARIANTS: INV001, INV002
"""

from dataclasses import dataclass
from typing import List


@dataclass
class PackageRisk:
    """
    Risk assessment for a package.

    IMPLEMENTS: S001
    INVARIANT: INV001 - risk_score in [0.0, 1.0]
    INVARIANT: INV002 - signals is never None
    """
    name: str
    risk_score: float
    signals: List[str]

    def __post_init__(self):
        # INV001: Enforce risk_score bounds
        if not 0.0 <= self.risk_score <= 1.0:
            raise ValueError(f"risk_score must be in [0.0, 1.0], got {self.risk_score}")

        # INV002: Enforce signals not None
        if self.signals is None:
            self.signals = []


def validate_package(name: str) -> PackageRisk:
    """
    Validate a package name and return risk assessment.

    IMPLEMENTS: S001
    INVARIANTS: INV001, INV002
    TESTS: T001.1, T001.2, T001.3

    Args:
        name: Package name to validate

    Returns:
        PackageRisk with assessment

    Raises:
        ValidationError: If name is invalid
    """
    if not name:
        raise ValidationError("Package name cannot be empty")

    # Minimal implementation to pass test
    return PackageRisk(
        name=name,
        risk_score=0.0,
        signals=[]
    )
```

---

### Phase 4: Verify Green

```bash
# Run the specific test
pytest tests/unit/test_detector.py::test_valid_package_name_passes -v

# Expected: PASSED

# Run all related tests
pytest tests/unit/test_detector.py -v

# Run type check
mypy src/phantom_guard/core/detector.py --strict

# Run lint
ruff check src/phantom_guard/core/detector.py
```

---

### Phase 5: Refactor (If Needed)

```python
# Questions to ask:
# 1. Is there duplication?
# 2. Are names clear?
# 3. Is the function too long (>50 lines)?
# 4. Are there magic numbers?
# 5. Could this be simpler?

# If refactoring:
# 1. Make small changes
# 2. Run tests after each change
# 3. Ensure tests still pass
```

---

### Phase 6: Commit

```bash
# Pre-commit checks
ruff format src/
ruff check src/
mypy src/ --strict
pytest tests/unit/test_detector.py -v

# Commit with trace
git add src/phantom_guard/core/detector.py tests/unit/test_detector.py
git commit -m "feat(S001): Implement PackageRisk and validate_package

IMPLEMENTS: S001
TESTS: T001.1, T001.2
INVARIANTS: INV001, INV002

- Add PackageRisk dataclass with invariant enforcement
- Add validate_package function with validation
- Add unit tests for valid/invalid inputs"
```

---

### Phase 7: Repeat

Move to next test:
1. Remove skip from T001.2
2. Run test → RED
3. Add code → GREEN
4. Refactor
5. Commit
6. Next test...

---

## CODE STANDARDS

### Required Comments

```python
"""
IMPLEMENTS: S001, S002
INVARIANTS: INV001
TESTS: T001.1, T001.2
"""
```

### Import Order

```python
# Standard library
import json
from typing import TYPE_CHECKING, List, Optional

# Third party
import httpx
from pydantic import BaseModel

# Local
from phantom_guard.core import types
from phantom_guard.registry import client
```

### Type Hints (MANDATORY)

```python
# Good
def validate_package(name: str, registry: str = "pypi") -> PackageRisk:
    ...

# Bad - NO TYPE HINTS
def validate_package(name, registry="pypi"):
    ...
```

### Error Handling

```python
# Good - Specific exceptions
try:
    response = await client.get(url)
except httpx.TimeoutException:
    logger.warning("Timeout for %s", url)
    return cached_result

# Bad - Catch all
try:
    result = do_something()
except:
    return None
```

### Logging

```python
import logging
logger = logging.getLogger(__name__)

# Good - Structured, no secrets
logger.info("Validated %d packages in %dms", count, time_ms)

# Bad - Print statements, secrets
print(f"Checking {package}")
logger.info(f"API key: {key}")  # NEVER DO THIS
```

---

## QUALITY GATES

### Per-Commit

```bash
# All must pass before commit
ruff format --check src/
ruff check src/
mypy src/ --strict
pytest tests/unit/ -v
```

### Per-Task Completion

```bash
# Run related tests
pytest tests/unit/test_[module].py -v

# Check coverage
pytest --cov=phantom_guard/core/[module] --cov-report=term

# Verify invariants enforced
grep -n "INVARIANT:" src/phantom_guard/core/[module].py
```

---

## TASK COMPLETION

### Verify Acceptance Criteria

```markdown
## TASK W1.1 — COMPLETION VERIFICATION

### Tests
- [x] T001.1 passes
- [x] T001.2 passes
- [x] T001.3 passes

### Quality
- [x] mypy --strict passes
- [x] ruff check clean
- [x] Coverage: 95% (target: 90%)

### Traces
- [x] IMPLEMENTS comments present
- [x] INVARIANT comments present
- [x] TEST_ID references correct

### Status: COMPLETE
```

### Update Roadmap

```markdown
# docs/planning/ROADMAP.md

| Task | SPEC | Hours | Status |
|:-----|:-----|:------|:-------|
| W1.1 | S001 | 10 | ✅ COMPLETE |
| W1.2 | S002 | 8 | PENDING |
```

---

## PROTOCOL VIOLATIONS

| Violation | Response |
|:----------|:---------|
| Writing code before test stub | STOP, create stub first |
| Test passes before code | Investigate, fix test |
| No IMPLEMENTS comment | Add comment |
| Skip refactor | Review for tech debt |
| Commit without checks | Run pre-commit checks |
| Task complete without verification | Verify acceptance criteria |

---

## IMPLEMENTATION CHECKLIST

```markdown
## IMPLEMENTATION CHECKLIST

### Before Starting
- [ ] Task loaded (/implement W1.1)
- [ ] Test stubs exist
- [ ] Pre-conditions verified

### For Each Test
- [ ] Remove skip decorator
- [ ] Run test → FAILS
- [ ] Write minimal code
- [ ] Run test → PASSES
- [ ] Refactor if needed
- [ ] Commit

### After All Tests
- [ ] All task tests pass
- [ ] Coverage meets target
- [ ] Type check passes
- [ ] Lint passes
- [ ] Task marked complete in roadmap
```

---

*Implementation is about DISCIPLINE, not creativity. Creativity happens in architecture.*

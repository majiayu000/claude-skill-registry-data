---
name: test-driven-development
description: Drives development with tests. Use when implementing any logic, fixing any bug, or changing any behavior. Use when you need to prove that code works, when a bug report arrives, or when you're about to modify existing functionality.
metadata:
  version: "1.1.1"
---

# Test-Driven Development

## Overview

Write a failing test before writing the code that makes it pass. For bug fixes, reproduce the bug with a test before attempting a fix. Tests are proof — "seems right" is not done. A codebase with good tests is an AI agent's superpower; a codebase without tests is a liability.

## When to Use

- Implementing any new logic or behavior
- Fixing any bug (the Prove-It Pattern)
- Modifying existing functionality
- Adding edge case handling
- Any change that could break existing behavior

**When NOT to use:** Pure configuration changes, documentation updates, or static content changes that have no behavioral impact.

## The TDD Cycle

**Slug:** the `<slug>` in every commit below is provided by the calling context (e.g., `development-implementation` passes `task N <slug>`). When invoked standalone, derive a descriptive name from what is being implemented.

**Every commit below goes through the shared builder** — read `<CORE>/doctrine/governance/commit_via_builder.md` and supply its variables, with **`--actor developer`** (the seat whose subjects these are — name it, never derive it). Never hand-write `git commit` or a trailer.

```
    RED                GREEN              REFACTOR
 Write a test    Write minimal code    Clean up the
 that fails  ──→  to make it pass  ──→  implementation  ──→  (repeat)
      │                  │                    │
      ▼                  ▼                    ▼
   Test FAILS        Test PASSES         Tests still PASS
      │                  │                    │
   commit red        commit green        commit refactor
                                         (if real changes)
```

### Step 1: RED — Write a Failing Test

Write the test first. It must fail. A test that passes immediately proves nothing.

```python
# RED: This test fails because Task doesn't exist yet
def test_create_task_with_title_and_default_status():
    task = Task(title="Buy groceries")

    assert task.id is not None
    assert task.title == "Buy groceries"
    assert task.status == TaskStatus.TODO
    assert task.created_at is not None
```

Run the tests — all new tests must **FAIL** before proceeding.

**Commit:** `developer: <slug> — red`

### Step 2: GREEN — Make It Pass

Write the minimum code to make the test pass. Don't over-engineer:

```python
# GREEN: Minimal implementation
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid

class TaskStatus(Enum):
    TODO = "todo"

@dataclass(frozen=True)
class Task:
    title: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: TaskStatus = TaskStatus.TODO
    created_at: datetime = field(default_factory=datetime.now)
```

Run the tests — all tests must **PASS** before proceeding.

**Commit:** `developer: <slug> — green`

### Step 3: REFACTOR — Clean Up

With tests green, improve the code without changing behavior:

1. Invoke `refactor-for-clarity` — naming, readability, intent
2. Invoke `refactor-for-reuse` — extract shared logic, remove duplication
3. Invoke `refactor-for-optimize` — if performance or algorithmic improvement is warranted

Run tests after each invocation to confirm nothing broke.

**Commit only if real changes:** `developer: <slug> — refactor`

## The Prove-It Pattern (Bug Fixes)

When a bug is reported, **do not start by trying to fix it.** Start by writing a test that reproduces it.

```
Bug report arrives
       │
       ▼
  Write a test that demonstrates the bug
       │
       ▼
  Test FAILS (confirming the bug exists) → commit red
       │
       ▼
  Implement the fix
       │
       ▼
  Test PASSES (proving the fix works) → commit green
       │
       ▼
  Run full test suite (no regressions)
```

**Example:**

```python
# Bug: "Completing a task doesn't update completed_at"

# Step 1: Write the reproduction test (it should FAIL)
def test_complete_task_sets_completed_at():
    task = Task(title="Test")
    completed = task.complete()

    assert completed.status == TaskStatus.DONE
    assert completed.completed_at is not None  # This fails → bug confirmed

# Step 2: Fix the bug
@dataclass(frozen=True)
class Task:
    title: str
    completed_at: Optional[datetime] = None

    def complete(self) -> "Task":
        return replace(self,
            status=TaskStatus.DONE,
            completed_at=datetime.now()  # This was missing
        )

# Step 3: Test passes → bug fixed, regression guarded
```

## The Test Pyramid

Invest testing effort according to the pyramid — most tests should be small and fast, with progressively fewer tests at higher levels:

```
          ╱╲
         ╱  ╲         E2E Tests (~5%)
        ╱    ╲        Full user flows, real system
       ╱──────╲
      ╱        ╲      Integration Tests (~15%)
     ╱          ╲     Component interactions, API boundaries
    ╱────────────╲
   ╱              ╲   Unit Tests (~80%)
  ╱                ╲  Pure logic, isolated, milliseconds each
 ╱──────────────────╲
```

**The Beyonce Rule:** If you liked it, you should have put a test on it. Infrastructure changes, refactoring, and migrations are not responsible for catching your bugs — your tests are. If a change breaks your code and you didn't have a test for it, that's on you.

### Test Sizes (Resource Model)

Beyond the pyramid levels, classify tests by what resources they consume:

| Size | Constraints | Speed | Example |
|------|------------|-------|---------|
| **Small** | Single process, no I/O, no network, no database | Milliseconds | Pure function tests, data transforms |
| **Medium** | Multi-process OK, localhost only, no external services | Seconds | API tests with test DB, component tests |
| **Large** | Multi-machine OK, external services allowed | Minutes | E2E tests, performance benchmarks, staging integration |

Small tests should make up the vast majority of your suite. They're fast, reliable, and easy to debug when they fail.

### Decision Guide

```
Is it pure logic with no side effects?
  → Unit test (small)

Does it cross a boundary (API, database, file system)?
  → Integration test (medium)

Is it a critical user flow that must work end-to-end?
  → E2E test (large) — limit these to critical paths
```

## Writing Good Tests

### Test State, Not Interactions

Assert on the *outcome* of an operation, not on which methods were called internally. Tests that verify method call sequences break when you refactor, even if the behavior is unchanged.

```python
# Good: Tests what the function does (state-based)
def test_returns_tasks_sorted_by_creation_date_newest_first():
    tasks = list_tasks(sort_by="created_at", sort_order="desc")
    assert tasks[0].created_at > tasks[1].created_at

# Bad: Tests how the function works internally (interaction-based)
def test_calls_db_with_correct_order(mock_db):
    list_tasks(sort_by="created_at", sort_order="desc")
    mock_db.query.assert_called_with("SELECT ... ORDER BY created_at DESC")
```

### DAMP Over DRY in Tests

In production code, DRY (Don't Repeat Yourself) is usually right. In tests, **DAMP (Descriptive And Meaningful Phrases)** is better. A test should read like a specification — each test should tell a complete story without requiring the reader to trace through shared helpers.

```python
# DAMP: Each test is self-contained and readable
def test_rejects_tasks_with_empty_titles():
    with pytest.raises(ValueError, match="Title is required"):
        Task(title="")

def test_trims_whitespace_from_titles():
    task = Task(title="  Buy groceries  ")
    assert task.title == "Buy groceries"
```

Duplication in tests is acceptable when it makes each test independently understandable.

### Prefer Real Implementations Over Mocks

Use the simplest test double that gets the job done. The more your tests use real code, the more confidence they provide.

```
Preference order (most to least preferred):
1. Real implementation  → Highest confidence, catches real bugs
2. Fake                 → In-memory version of a dependency (e.g., fake repository)
3. Stub                 → Returns canned data, no behavior
4. Mock (interaction)   → Verifies method calls — use sparingly
```

**Use mocks only when:** the real implementation is too slow, non-deterministic, or has side effects you can't control (external APIs, email sending). Over-mocking creates tests that pass while production breaks.

### Use the Arrange-Act-Assert Pattern

```python
def test_marks_overdue_tasks_when_deadline_has_passed():
    # Arrange: Set up the test scenario
    task = Task(title="Test", deadline=date(2025, 1, 1))

    # Act: Perform the action being tested
    result = check_overdue(task, current_date=date(2025, 1, 2))

    # Assert: Verify the outcome
    assert result.is_overdue is True
```

### One Assertion Per Concept

```python
# Good: Each test verifies one behavior
def test_rejects_empty_titles(): ...
def test_trims_whitespace_from_titles(): ...
def test_enforces_maximum_title_length(): ...

# Bad: Everything in one test
def test_validates_titles_correctly():
    with pytest.raises(ValueError): Task(title="")
    assert Task(title="  hello  ").title == "hello"
    with pytest.raises(ValueError): Task(title="a" * 256)
```

### Name Tests Descriptively

```python
# Good: Reads like a specification
class TestTaskComplete:
    def test_sets_status_to_done_and_records_timestamp(self): ...
    def test_raises_not_found_for_nonexistent_task(self): ...
    def test_is_idempotent_completing_already_done_task(self): ...

# Bad: Vague names
class TestTask:
    def test_works(self): ...
    def test_handles_errors(self): ...
    def test_3(self): ...
```

## Test Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Testing implementation details | Tests break when refactoring even if behavior is unchanged | Test inputs and outputs, not internal structure |
| Flaky tests (timing, order-dependent) | Erode trust in the test suite | Use deterministic assertions, isolate test state |
| Testing framework code | Wastes time testing third-party behavior | Only test YOUR code |
| Snapshot abuse | Large snapshots nobody reviews, break on any change | Use snapshots sparingly and review every change |
| No test isolation | Tests pass individually but fail together | Each test sets up and tears down its own state |
| Mocking everything | Tests pass but production breaks | Prefer real implementations > fakes > stubs > mocks |

## See Also

- `references/testing-patterns-python.md` — pytest patterns: AAA, fakes, mocking, parametrize, fixtures, CLI testing
- `references/testing-patterns-kotlin.md` — JUnit5/MockK patterns: AAA, fakes, MockK, parametrize, lifecycle
- `references/examples-kotlin.md` — Kotlin equivalents of the TDD cycle examples in this skill

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll write tests after the code works" | You won't. And tests written after the fact test implementation, not behavior. |
| "This is too simple to test" | Simple code gets complicated. The test documents the expected behavior. |
| "Tests slow me down" | Tests slow you down now. They speed you up every time you change the code later. |
| "I tested it manually" | Manual testing doesn't persist. Tomorrow's change might break it with no way to know. |
| "The code is self-explanatory" | Tests ARE the specification. They document what the code should do, not what it does. |
| "It's just a prototype" | Prototypes become production code. Tests from day one prevent the "test debt" crisis. |
| "Let me run the tests again just to be extra sure" | After a clean test run, repeating the same command adds nothing unless the code has changed since. Run again after subsequent edits, not as reassurance. |

## Red Flags

- Writing code without any corresponding tests
- Tests that pass on the first run (they may not be testing what you think)
- "All tests pass" but no tests were actually run
- Bug fixes without reproduction tests
- Tests that test framework behavior instead of application behavior
- Test names that don't describe the expected behavior
- Skipping tests to make the suite pass
- Running the same test command twice in a row without any intervening code change
- Combining red and green into a single commit (`developer: <slug> — red/green`) — always two separate commits, always in sequence

## Verification

After completing any implementation:

- [ ] Every new behavior has a corresponding test
- [ ] All tests pass
- [ ] Bug fixes include a reproduction test that failed before the fix
- [ ] Test names describe the behavior being verified
- [ ] No tests were skipped or disabled
- [ ] Red commit is standalone (failing tests only, no implementation) and was committed before the first line of implementation was written

**Note:** Run each test command after a change that could affect the result. After a clean run, don't repeat the same command unless the code has changed since — re-running on unchanged code adds no confidence.

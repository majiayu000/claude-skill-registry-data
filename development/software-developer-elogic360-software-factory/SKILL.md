---
name: software-developer
description: Software Developer (General) — Institutional capability and runbook for software-developer.
---

# SKILL: Software Developer (General)
## Domain: Code Quality, Patterns, Debugging, Code Review, Refactoring

**Activation triggers:** general coding task, code review, refactoring, debugging,
code quality, naming convention, code smell, technical debt, pair programming,
implementation guidance.

---

## Development Standards

```python
# NAMING CONVENTIONS
# Python (backend):
#   - Variables/functions: snake_case
#   - Classes:            PascalCase
#   - Constants:          SCREAMING_SNAKE
#   - Private methods:    _single_underscore
#   - Database columns:   snake_case
#   - FastAPI endpoints:  snake_case function names, kebab-case URLs

# TypeScript (frontend):
#   - Variables/functions: camelCase
#   - Components:          PascalCase
#   - Constants:           SCREAMING_SNAKE or camelCase (prefer const)
#   - CSS classes:         kebab-case (Tailwind utility names)
#   - API keys:            camelCase (matching backend snake → camel transform)

# Files:
#   - Python:     snake_case.py
#   - TypeScript: PascalCase.tsx (components), camelCase.ts (utils/hooks)
#   - SQL:        snake_case
#   - Env vars:   SCREAMING_SNAKE
```

---

## Code Review Checklist

```
Security:
  [ ] No secrets or credentials in code
  [ ] Input validation on all user-controlled data
  [ ] Authentication required on all protected endpoints
  [ ] SQL queries use parameterized inputs

Correctness:
  [ ] Edge cases handled (empty list, None, 0, negative numbers)
  [ ] Error paths return appropriate status codes
  [ ] Async operations awaited (no forgotten await)
  [ ] No race conditions in concurrent paths

Performance:
  [ ] No N+1 queries (use selectinload or explicit join)
  [ ] Pagination on all list endpoints
  [ ] Heavy operations are async (not blocking event loop)
  [ ] No synchronous I/O in async functions

Maintainability:
  [ ] Function does one thing (< 50 lines is a good signal)
  [ ] Clear variable names (no single-letter vars except loop counters)
  [ ] No duplicated logic (extract shared utility)
  [ ] Magic numbers have named constants

Tests:
  [ ] Happy path tested
  [ ] Error paths tested
  [ ] Edge cases tested
  [ ] No mocking what you own (mock external deps only)
```

---

## Debugging Protocol

```
Step 1: REPRODUCE — minimal test case that reliably triggers the bug
Step 2: ISOLATE — comment/disable code until bug disappears, then re-enable
Step 3: HYPOTHESIZE — form ONE hypothesis about root cause
Step 4: TEST — verify hypothesis with a targeted check
Step 5: FIX — smallest change that fixes root cause (not symptom)
Step 6: VERIFY — confirm fix works AND doesn't break adjacent behavior
Step 7: PREVENT — add test so this never regresses

Common debugging tools:
  - FastAPI: add temporary logger.debug() + check /tmp/<service>.log
  - React: React DevTools → Component tree → check prop/state values
  - Database: psql → EXPLAIN ANALYZE <query>
  - Redis: redis-cli MONITOR (watch all commands in real-time)
  - WebSocket: Browser DevTools → Network → WS tab → see all frames
```

---

## Refactoring Triggers

```
Refactor when you see:
  - Function > 50 lines → extract smaller functions
  - Same logic in 3+ places → extract utility
  - Class with > 5 responsibilities → split into focused classes
  - Deeply nested conditionals (>3 levels) → extract guard clauses
  - Magic strings/numbers repeated → define constants
  - God component (> 300 lines) → decompose into sub-components
  - Prop drilling > 2 levels → use Context or Zustand slice

Refactoring rules:
  - Refactor in a separate PR from feature changes
  - Always have tests before refactoring
  - One refactoring type per PR (rename, extract, inline, etc.)
  - Verify behavior is identical after refactoring
```

---

## Common Patterns Reference

```python
# 1. Guard clauses (early return replaces nested if)
# BEFORE:
def process_trade(trade):
    if trade is not None:
        if trade.status == "closed":
            if trade.profit > 0:
                return calculate_win(trade)
    return None

# AFTER:
def process_trade(trade):
    if trade is None:
        return None
    if trade.status != "closed":
        return None
    if trade.profit <= 0:
        return None
    return calculate_win(trade)

# 2. Result type (avoid exceptions for expected errors)
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")

@dataclass
class Result(Generic[T]):
    value: T | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None

# 3. Service layer (keep routes thin)
# Route: validate input, call service, return response
# Service: business logic, DB calls, external API calls
# No business logic in routes. No HTTP concerns in services.

# 4. Builder pattern for complex queries
class TradeQueryBuilder:
    def __init__(self):
        self._query = select(Trade)

    def for_account(self, account_id: str) -> "TradeQueryBuilder":
        self._query = self._query.where(Trade.account_id == account_id)
        return self

    def closed_only(self) -> "TradeQueryBuilder":
        self._query = self._query.where(Trade.status == "closed")
        return self

    def in_date_range(self, from_dt, to_dt) -> "TradeQueryBuilder":
        self._query = self._query.where(Trade.closed_at.between(from_dt, to_dt))
        return self

    def build(self):
        return self._query

# Usage:
query = TradeQueryBuilder().for_account(account_id).closed_only().in_date_range(start, end).build()
```

---

## Git Workflow

```bash
# Feature branch workflow
git checkout -b feature/<ticket-id>-brief-description

# Commit message format:
# type(scope): description
# Types: feat, fix, refactor, test, docs, chore, perf
# Example:
git commit -m "feat(journal): add calendar heatmap endpoint with daily PnL aggregation"
git commit -m "fix(auth): wrap create_oauth_user in try/except to prevent 500 on missing role"
git commit -m "perf(journal): add index on trades(account_id, closed_at DESC) for query optimization"

# Before raising PR:
git fetch origin main
git rebase origin/main    # keep clean linear history
pre-commit run --all-files  # run all hooks locally first
```

---

## Code Smell Reference

```
Smell                     | Refactoring
--------------------------|------------------------------------------
Long method               | Extract Method
Duplicate code            | Extract Method / Utility function
Large class               | Extract Class / Split concerns
Feature envy              | Move Method to the class it uses most
Data clumps               | Extract Data Class / Pydantic model
Primitive obsession       | Replace with typed object (e.g., Money, Symbol)
Inappropriate intimacy    | Move method, use dependency injection
Comments explaining "why" | Keep them — they're documentation
Comments explaining "what"| The code should explain itself — rename
Dead code                 | Delete it (git history preserves it)
```

---

## Anti-Patterns

```
✗ Premature optimization (profile first, optimize what's slow)
✗ Over-engineering for scale you don't have yet
✗ Copy-paste instead of extraction (tech debt compounds)
✗ Clever code that requires a comment to understand
✗ Catching Exception without logging (silent failures)
✗ Modifying existing tests to make them pass (fix the code, not the test)
✗ Committing commented-out code (use git, delete it)
✗ God functions that do everything (single responsibility)
✗ Mixing levels of abstraction in one function
```

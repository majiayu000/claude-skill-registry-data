---
name: testing-python
description: Writes tests following TDD Red-Green-Refactor (pytest + Hypothesis). Tests behavior, not implementation. Use when writing unit tests, integration tests, or property tests.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, Edit, Write, Bash
  argument-hint: [test-scope or component-name]
  stability: stable
  content-hash: sha256:9c6623b8a660d59c5dbdaf72e4e00e0d9cfec0abff96a6b0b62647a3fcf8394c
  last-verified-cc-version: 1.0.34
---

# Python Testing

**Target**: $ARGUMENTS

Writes **focused, behavior-driven tests** following project testing strategy.

## Quick Reference

**TDD methodology** (language-agnostic): See `tdd-core` plugin (`testing-tdd` skill)

**Python-specific documentation**: `references/`

- `references/testing-strategy.md` - Python tools (pytest, Hypothesis, inline-snapshot)
- `references/tdd-best-practices.md` - Python TDD examples (extends tdd-core)

## Approach

**TDD only**: pytest for known cases, Hypothesis for edge cases, inline-snapshot for regression. Tests assert observable behavior — inputs produce expected outputs/side-effects. No Gherkin, no feature files, no step definitions.

See `references/testing-strategy.md` for tool selection guide.

## TDD Essentials (Quick Reference)

**Cycle**: RED (failing test) → GREEN (minimal pass) → REFACTOR (clean up)

**Structure**: Arrange-Act-Assert (AAA)

```python
def test_order_processor_calculates_total():
    # ARRANGE
    items = [Item(price=10.00, qty=2), Item(price=5.00, qty=1)]
    processor = OrderProcessor()

    # ACT
    total = processor.calculate_total(items)

    # ASSERT
    assert total == 25.00
```

## Hypothesis Priorities (Edge Cases within TDD)

| Priority | Area | Example |
| ---------- | ------ | --------- |
| CRITICAL | Math formulas | Scores always in bounds |
| CRITICAL | Loop termination | Never hangs |
| HIGH | Input validation | Handles any text |
| HIGH | Serialization | Always valid JSON |

## What to Test (KISS/DRY/YAGNI)

**High-Value**: Business logic, integration points, edge cases, contracts

**Avoid**: Library behavior, trivial assertions, implementation details, default constants, stale fixture patches (see `references/testing-strategy.md` → "Patterns to Remove")

See `references/testing-strategy.md` → "Patterns to Remove" for full list.

## Naming Convention

**Format**: `test_{module}_{component}_{behavior}`

```python
test_user_service_creates_new_user()
test_order_processor_validates_items()
```

## Execution

```bash
make test              # All tests
make test_rerun        # Rerun failed tests (fast iteration)
make validate          # Full pre-commit validation
pytest tests/ -v       # Verbose
pytest -k test_user_   # Filter by name
```

## Quality Gates

- [ ] All tests pass (`make test`)
- [ ] TDD Red-Green-Refactor followed
- [ ] Arrange-Act-Assert structure used
- [ ] Naming convention followed
- [ ] Behavior-focused (not implementation)
- [ ] No library behavior tested
- [ ] Mocks for third-party types use spec=RealClass

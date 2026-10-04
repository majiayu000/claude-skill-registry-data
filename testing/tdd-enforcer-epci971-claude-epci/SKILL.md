---
name: epci:tdd-enforcer
description: >-
  Enforces Test-Driven Development workflow (RED-GREEN-REFACTOR-VERIFY).
  Ensures tests are written before implementation code.
  Use when: implementing features with /implement or /quick,
  validating TDD compliance, or running test verification cycles.
  Internal component for EPCI v6.0.
user-invocable: false
allowed-tools: Bash, Read
---

# TDD Enforcer

Internal component for Test-Driven Development workflow enforcement.

## Overview

Ensure proper TDD cycle for all implementations:

```
RED → GREEN → REFACTOR → VERIFY
 │      │         │         │
 │      │         │         └─ All tests pass
 │      │         └─ Clean up code
 │      └─ Minimal code to pass
 └─ Write failing test first
```

## API

| Function | Description | Input | Output |
|----------|-------------|-------|--------|
| `start_cycle(feature)` | Begin TDD cycle | feature info | Cycle state |
| `check_phase(expected)` | Verify current phase | phase name | Boolean |
| `advance_phase()` | Move to next phase | - | New phase |
| `verify_tests()` | Run test suite | - | Test results |
| `get_mode()` | Get enforcement mode | - | strict/guided/optional |

## TDD Phases

| Phase | Required Action | Validation |
|-------|-----------------|------------|
| **RED** | Write failing test | Test must fail (exit 1) |
| **GREEN** | Write minimal code | Test must pass (exit 0) |
| **REFACTOR** | Improve code quality | Tests still pass |
| **VERIFY** | Final verification | All tests pass |

## Enforcement Modes

| Mode | Strictness | Behavior |
|------|------------|----------|
| `strict` | High | Block progress without passing tests |
| `guided` | Medium | Remind but allow skip with confirmation |
| `optional` | Low | Suggest only, no enforcement |

## Configuration

Default configuration in `.epci/config.json`:

```json
{
  "tdd": {
    "mode": "guided",
    "min_coverage": 70,
    "require_for": ["implement", "quick"],
    "skip_for": ["improve", "refactor"],
    "test_command": "npm test",
    "coverage_command": "npm run coverage"
  }
}
```

## Usage

Invoked automatically by implementation skills:

```
# Called by /implement at each task
tdd.start_cycle({ feature: "auth-oauth", task: "US-001" })

# Phase progression
tdd.check_phase("RED")     # Verify we're in RED phase
tdd.advance_phase()        # Move to GREEN after test written

# Test verification
result = tdd.verify_tests()
# Returns: { passed: true, coverage: 85, failures: [] }
```

## TDD Cycle Flow

```
┌─────────────────────────────────────────────┐
│                 TDD CYCLE                    │
├─────────────────────────────────────────────┤
│                                              │
│   ┌───────┐                                  │
│   │  RED  │ ← Write test that fails         │
│   └───┬───┘                                  │
│       │ Test fails? ✓                        │
│       ▼                                      │
│   ┌───────┐                                  │
│   │ GREEN │ ← Write minimal code to pass    │
│   └───┬───┘                                  │
│       │ Test passes? ✓                       │
│       ▼                                      │
│   ┌──────────┐                               │
│   │ REFACTOR │ ← Improve code quality       │
│   └───┬──────┘                               │
│       │ Tests still pass? ✓                  │
│       ▼                                      │
│   ┌────────┐                                 │
│   │ VERIFY │ ← Run full test suite          │
│   └───┬────┘                                 │
│       │ All pass? ✓                          │
│       ▼                                      │
│     DONE                                     │
│                                              │
└─────────────────────────────────────────────┘
```

## Test Commands

| Stack | Default Command |
|-------|-----------------|
| Node.js | `npm test` |
| Python | `pytest` |
| Java | `./gradlew test` |
| PHP | `./vendor/bin/phpunit` |

## Limitations

This component does NOT:
- Write tests automatically (provides guidance)
- Manage test fixtures or data
- Support parallel test execution config

---
name: decomplect-py
description: Architectural code analysis for Python design quality. Evaluates simplicity (Rich Hickey), functional core/imperative shell (Gary Bernhardt), and coupling (Constantine & Yourdon). Use for design review or architectural assessment of Python code.
---

# Decomplect-Py

Architectural analysis for Python design quality.

## Usage

```
/decomplect-py                # Run all 3 analyzers in parallel
/decomplect-py --simplicity   # Specific analyzer
/decomplect-py --fcis         # Specific analyzer
/decomplect-py --coupling     # Specific analyzer
```

## Analyzers

| Analyzer | Question |
|----------|----------|
| **simplicity-analyzer** | Is this truly simple or just easy? |
| **fcis-analyzer** | Is pure logic separated from I/O? |
| **coupling-analyzer** | Are modules well-separated? |

## What It Checks

| Pillar | Focus |
|--------|-------|
| **Simplicity** | Values over state, decomplected concerns |
| **FCIS** | Functional core (pure), imperative shell (I/O) |
| **Coupling** | High cohesion, low coupling |

## When to Use

- Reviewing Python system design
- Before major refactoring
- Assessing architectural quality
- Checking if code is "Rich Hickey approved"

## Supported Languages

- Python (`.py` files only)

## Python-Specific Patterns

- `dataclasses(frozen=True)` and `NamedTuple` for immutable values
- Mutable default argument anti-patterns
- Django/Flask view architecture
- Circular import detection
- Module-level state analysis

## Reference Documentation

- [Rich Hickey Principles](reference/rich-hickey.md)
- [Functional Core/Imperative Shell](reference/fcis.md)
- [Cohesion & Coupling](reference/coupling.md)

## See Also

- `/decomplect` - Analysis for TypeScript/Go/Rust
- `/unslopify` - Tactical code cleanup

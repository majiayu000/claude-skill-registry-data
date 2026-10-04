---
name: python-simplifier
description: Simplify or refactor complex Python. Not Django.
---

# Python Code Simplifier

Transform complex, hard-to-maintain Python code into clean, readable, idiomatic solutions.

## Analysis Scripts

```bash
# Comprehensive analysis (runs all checks)
python scripts/analyze_all.py /path/to/project

# Individual analyzers:
python scripts/analyze_complexity.py .       # Cyclomatic/cognitive complexity
python scripts/find_code_smells.py .         # Mutable defaults, bare excepts, etc.
python scripts/find_overengineering.py .     # YAGNI violations, unused abstractions
python scripts/find_dead_code.py .           # Unused imports, functions, variables
python scripts/find_unpythonic.py .          # Non-idiomatic patterns
python scripts/find_coupling_issues.py .     # Feature envy, low cohesion
python scripts/find_duplicates.py .          # Structural duplicate detection

# JSON output for CI/tooling
python scripts/analyze_all.py . --format json > report.json
```

## Workflow

1. **Analyze**: Run `analyze_all.py` to identify all issues
2. **Prioritize**: Address high-severity issues (🔴) first
3. **Simplify**: Apply patterns below incrementally
4. **Verify**: Ensure simplified code is functionally equivalent

## Simplification Principles

1. **YAGNI**: Don't add abstractions until needed
2. **Preserve behavior**: Simplification ≠ changing functionality
3. **One change at a time**: Incremental is safer
4. **Readability over cleverness**: Clear beats "smart"
5. **Keep related code together**: Locality matters

## Common Patterns

For Extract-and-Name, Early Returns, Comprehensions, Dictionary Techniques, and the Over-Engineering anti-pattern table, see `~/.claude/rules/python-refactors.md`.

### Context Managers

```python
# Before: Manual cleanup
f = open('file.txt')
try:
    data = f.read()
finally:
    f.close()

# After: with statement
with open('file.txt') as f:
    data = f.read()
```

## Code Smells Quick Reference

| Smell | Detection | Fix |
|-------|-----------|-----|
| Mutable default | `def f(x=[])` | Use `None`, create inside |
| Bare except | `except:` | `except Exception:` |
| God class | 15+ methods, 10+ attrs | Split into focused classes |
| Long function | 50+ lines | Extract helper functions |
| Deep nesting | 4+ levels | Early returns, extract |
| Feature envy | Method uses other class more | Move method |
| Magic numbers | Unexplained numeric literals | Named constants |

## When NOT to Simplify

- Working legacy code with no tests
- Performance-critical hot paths (measure first)
- Code that will be replaced soon
- External API constraints requiring complexity

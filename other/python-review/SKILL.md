---
description: Comprehensive Python code review for idiomatic patterns, async safety, type safety, and security
---

# Python Code Review

Comprehensive Python code review for idiomatic patterns, async safety, error handling, type safety, and security. Invokes the python-reviewer agent.

## When to Use

- After writing or modifying Python code
- Before committing Python changes
- Reviewing pull requests with Python code
- Onboarding to a Python codebase

## Review Categories

### CRITICAL (Must Fix)
- SQL/Command injection
- Pickle/eval/exec with untrusted data
- Hardcoded credentials
- Bare except swallowing errors
- Race conditions in shared state
- Unawaited coroutines
- Blocking calls in async context

### HIGH (Should Fix)
- Missing error context in re-raised exceptions
- Overly broad exception handling
- Not using context managers
- Missing type annotations on public APIs
- Mixing sync/async incorrectly

### MEDIUM (Consider)
- Non-idiomatic Python patterns
- Missing docstrings on public APIs
- Mutable default arguments
- String concatenation in loops
- Not using pathlib for file operations
- print() instead of logging

## Automated Checks

```bash
mypy . --strict          # Type checking
ruff check .             # Linting
bandit -r src/           # Security
radon cc src/ -a -nc     # Complexity
```

## Related

- `/python-lint` - Fix build and lint errors
- `/python-tdd` - TDD workflow
- `/code-review` - General code review

## Language

- Internal reasoning and thinking should be in English
- **All user-facing output, reports, and summaries must be written in Japanese**

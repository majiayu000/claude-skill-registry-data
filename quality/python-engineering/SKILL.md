---
name: python-engineering
description: Implement or review maintainable Python code. Use when adding Python modules, scripts, libraries, tests, or packaging.
---

# Python Engineering

Follow the repository's supported Python version, style, dependencies, and architecture before introducing new conventions.

- Prefer clear functions, explicit data flow, small modules, and standard-library solutions when sufficient.
- Add type hints to public interfaces and complex data structures; avoid noisy annotations that obscure simple code.
- Raise or handle specific exceptions. Do not swallow errors or use broad `except` blocks without a clear recovery policy.
- Validate external input at boundaries and keep side effects visible.
- Use context managers for resources, structured logging for applications, and deterministic behavior in tests.
- Avoid unnecessary global state, hidden I/O during imports, mutable defaults, and premature abstraction.
- Add tests for public behavior and important edge cases.
- Check packaging, import paths, supported versions, and dependency declarations when relevant.

Use the project's formatter, linter, type checker, and test runner. Do not claim static typing or test coverage beyond what was run. Explain trade-offs when choosing concurrency, async, caching, or new dependencies.

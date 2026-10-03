---
name: python-programming
description: Python engineering skill for implementing, debugging, testing, packaging, typing, reviewing, and refactoring Python applications, scripts, APIs, automation, data processing, CLIs, and libraries. Use for .py files, pyproject.toml, requirements files, pytest, async Python, type hints, packaging, dependency management, and Python performance or reliability work.
---

# Python Programming

## Operating Rules

- Inspect project metadata, dependency manager, test framework, and style before editing.
- Prefer clear data flow, explicit exceptions, typed public boundaries, and narrow dependencies.
- Do not rewrite large modules when a targeted patch will solve the issue.
- Preserve user-visible behavior unless the task explicitly asks for a behavior change.

## Workflow

1. Identify runtime version, package layout, entry points, and tests.
2. Reproduce or reason about the issue with the smallest relevant command.
3. Implement the change using idiomatic Python and existing project conventions.
4. Add or update focused tests with deterministic fixtures and no hidden network dependency.
5. Run formatting/type/test commands that exist in the repo and report any skipped verification.

## Python Standards

- Use `pathlib`, context managers, and structured logging where they improve clarity.
- Prefer dependency injection for external services and filesystem access in testable code.
- Use `asyncio` deliberately; avoid mixing blocking I/O into async flows without an executor.
- Keep exception handling specific; do not swallow errors unless the fallback is intentional.
- Treat security-sensitive parsing, subprocess, deserialization, and templating as high-risk code.


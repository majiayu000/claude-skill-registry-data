---
name: python-dev-team
description: Spawn a Python development team for feature implementation in src/mde/. Use for features spanning multiple modules, requiring tests, and code review.
user-invocable: true
argument-hint: <feature-or-task-description>
context: fork
agent: python-coder
---

# Python Development Team Spawn Recipe

## Team Composition

| Role | Model | Tools | Purpose |
|------|-------|-------|---------|
| **Lead/Architect** (you) | inherit | All | Design approach, coordinate, integrate |
| **Implementer** | inherit | All except WebFetch, WebSearch | Write code in src/mde/ |
| **Tester** | inherit | Read, Glob, Grep, Bash, Write, Edit | Write tests in tests/ |
| **Reviewer** | Sonnet | Read, Glob, Grep, Bash | Review for quality, security |

## Spawn Protocol

1. **Design** the implementation approach (modules to create/modify, data flow)
2. **Spawn implementer** to write code in src/mde/:
   - Follow existing patterns in the codebase
   - Add `__all__` exports, return type annotations
   - Run `uv run ruff check --fix` after changes
3. **Spawn tester** (after implementer has initial commits):
   - Write pytest tests under tests/mde/
   - Mirror source structure
   - Run `uv run pytest -v` to verify
4. **Spawn reviewer** (after both complete):
   - `git diff main...HEAD` to review all changes
   - P1/P2/P3 priority findings
5. **Integrate**: fix any reviewer findings, run full quality gate

## File Ownership (No Conflicts)

| Owner | Owns | Cannot Touch |
|-------|------|-------------|
| Implementer | `src/mde/**/*.py` | `tests/`, `docs/`, `pyproject.toml` |
| Tester | `tests/**/*.py` | `src/mde/`, `docs/` |
| Reviewer | Nothing (read-only) | Everything |
| Lead | `pyproject.toml`, `docs/` | Delegates src/ and tests/ |

## Quality Gate
```bash
uv run ruff check src/ tests/
uv run ty check
uv run pytest -v
uv run mde-py validate --all
```

## Constraints
- All Python tool config in pyproject.toml (never standalone files)
- All automation as Python modules (never .sh files)
- Use `uv run <tool>` not `uv run python -m <module>`

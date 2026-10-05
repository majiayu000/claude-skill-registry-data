---
name: git-commit
description: Use this skill when making git commits in the TTA.dev repository. Enforces Conventional Commits format and pre-commit quality checks.
---

### Git Commit Standards (TTA.dev)

All commits must follow [Conventional Commits](https://www.conventionalcommits.org/).

#### Commit Format

```
<type>: <short description>
```

**Types:**

| Type | When to Use |
|------|-------------|
| `feat:` | New feature or capability |
| `fix:` | Bug fix |
| `docs:` | Documentation only |
| `refactor:` | Code restructuring (no behavior change) |
| `test:` | Adding or updating tests |
| `chore:` | Maintenance, CI, dependencies |

#### Before Every Commit

Run the quality gate (see `build-test-verify` skill):

```bash
uv run ruff format .
uv run ruff check . --fix
uvx pyright platform/
uv run pytest -v --tb=short -m "not integration and not slow and not external"
```

#### Rules

- Keep commits atomic — one logical change per commit.
- Write descriptions in imperative mood ("add feature" not "added feature").
- Reference issue numbers when applicable.

#### Deep Reference

For full quality gate details, see [`docs/agent-guides/testing-architecture.md`](../../docs/agent-guides/testing-architecture.md).

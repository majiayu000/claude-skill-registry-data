---
name: cleanup
description: Clean workspace — build artifacts, dependencies, caches, Docker volumes, or temp files. Accepts arguments like build, deps, all, cache, docker, tasks, reinstall.
---

# Cleanup Skill

Clean up workspace artifacts based on the requested scope.

## Usage

```
/cleanup              # Default: show what can be cleaned
/cleanup build        # Remove build artifacts
/cleanup deps         # Remove dependency directories (node_modules, venv, etc.)
/cleanup all          # Full clean: deps + build artifacts
/cleanup cache        # Clear build tool caches
/cleanup docker       # docker system prune -f (no named volumes removed)
/cleanup tasks        # Remove obsolete task files (lessons.md is NEVER deleted)
/cleanup reinstall    # Full reinstall: clean deps → install
```

## Instructions

### Determine action from $ARGUMENTS:

| Argument | Action |
|----------|--------|
| `build` or `dist` | Remove all build artifacts (`dist/`, `build/`, `.next/`, `target/`) |
| `deps` | Remove dependency directories (`node_modules/`, `venv/`, `.venv/`, `target/`) |
| `all` | Full clean: deps + build artifacts, then reinstall |
| `cache` | Clear build tool caches (`.turbo/`, `.cache/`, `__pycache__/`, `.mypy_cache/`) |
| `docker` | `docker system prune -f` (does NOT remove named volumes) |
| `tasks` | Clean obsolete task files (see rules below) |
| `reinstall` | Full reinstall: clean deps → install |

### Tasks file cleanup rules:
- **NEVER delete** `claude/tasks/lessons.md` (accumulated wisdom)
- **NEVER delete** `claude/tasks/CLAUDE_ERRORS.md` (bug history)
- `claude/tasks/todo.md` can be archived if no active task
- `claude/tasks/mr-description-*.md` can be deleted after MR is merged
- `claude/tasks/ticket-*.md` can be deleted after ticket is created

### Safety rules:
- NEVER run `rm -rf /`
- NEVER delete `.env` or `.env.*` files
- For `all`: confirm before deleting dependencies if `package.json`/`pyproject.toml` shows install script hooks
- For `docker`: confirm before running prune in production-adjacent environments

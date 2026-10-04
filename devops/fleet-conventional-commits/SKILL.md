---
name: fleet-conventional-commits
description: When to use each commit type, how to scope correctly, task reference format. The commit is the atomic unit of work — getting it right matters for trail, review, and changelog.
---

# Conventional Commits — Engineer's Commit Discipline

Every `fleet_commit` fires a chain: git commit → event → methodology check → trail. The commit message IS your trail. Fleet-ops reviews it. The changelog extracts it. The Doctor watches it. Getting the format right matters.

## The Format

```
type(scope): description [task:XXXXXXXX]
```

The hook on `fleet_commit` BLOCKS any message that doesn't match this pattern. Exit code 2 = blocked. You can't bypass it.

## When Each Type

| Type | When | Example |
|------|------|---------|
| feat | New capability that didn't exist before | `feat(core): add stage-aware effort floor [task:abc12345]` |
| fix | Something was broken and you repaired it | `fix(dispatch): use model_config for Claude backends [task:abc12345]` |
| refactor | Restructuring without behavior change | `refactor(tools): extract security_hold logic to helper [task:abc12345]` |
| test | Adding or fixing tests only | `test(model): add 10 stage-aware effort tests [task:abc12345]` |
| docs | Documentation only — README, comments, ADRs | `docs(api): add endpoint reference for fleet_contribute [task:abc12345]` |
| chore | Maintenance — config, deps, scripts, no logic change | `chore(config): add 8 chain docs to tool-chains.yaml [task:abc12345]` |
| ci | CI/CD pipeline changes only | `ci(actions): add lint step before test [task:abc12345]` |
| style | Formatting, whitespace, linting — no logic change | `style(core): fix ruff warnings in event_chain.py [task:abc12345]` |
| perf | Performance improvement without behavior change | `perf(context): cache synergy matrix on first load [task:abc12345]` |

## Common Mistakes

1. **feat for everything** — If you're fixing a bug, it's `fix`, not `feat`. If you're adding tests, it's `test`.
2. **Vague scopes** — `feat(update): change things` tells nothing. Scope should be the module/area: `core`, `mcp`, `dispatch`, `tools`, `config`.
3. **Missing task reference** — `[task:XXXXXXXX]` is REQUIRED. First 8 chars of the task ID. This links the commit to the trail.
4. **Giant commits** — One commit per logical change. "Added feature + fixed 3 bugs + refactored module" is 4 commits.
5. **Commit message doesn't match the diff** — If the message says `fix(auth)` but the diff is in `fleet/core/budget.py`, something's wrong.

## Scoping Guide for the Fleet Codebase

| Scope | What It Covers |
|-------|---------------|
| core | fleet/core/*.py — domain logic |
| mcp | fleet/mcp/*.py — MCP tools and server |
| roles | fleet/mcp/roles/*.py — role-specific group calls |
| infra | fleet/infra/*.py — external service clients |
| cli | fleet/cli/*.py — CLI commands |
| config | config/*.yaml — configuration files |
| scripts | scripts/*.sh — IaC scripts |
| agents | agents/_template/ — agent identity templates |
| skills | .claude/skills/ — workspace skills |
| tests | fleet/tests/ — test files |

## One Commit = One Logical Change

Break your work into atomic commits:

```
# Good: 3 focused commits
test(model): add stage-aware effort tests [task:abc12345]
feat(model): add _STAGE_EFFORT_FLOOR to model_selection [task:abc12345]
fix(dispatch): use model_config for Claude backends [task:abc12345]

# Bad: 1 monolith commit
feat(core): add stage-aware effort and fix dispatch and add tests [task:abc12345]
```

Each commit should be independently understandable. A reviewer reading the git log should see a clear story of what you did and why.

## The Trail Connection

Every `fleet_commit` automatically:
1. Records a trail event in `.fleet-trail.log` (PostToolUse hook)
2. Emits `fleet.task.committed` event (MCP tool chain)
3. Posts to board memory if methodology check detects issues

Your commit history IS your trail. Accountability uses it for compliance verification. Fleet-ops reads it during review. The changelog generator extracts it for release notes.

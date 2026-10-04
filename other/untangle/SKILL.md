---
name: untangle
description: Sort a chronically dirty git tree into logical atomic commits. Analyzes unstaged/staged changes, groups by domain/feature, proposes commit sequence, executes them. Use when user says /untangle, "clean up git", "sort these changes", "commit this mess", or when git status shows 50+ dirty files from parallel agent work.
---

# UNTANGLE (Sort Dirty Tree Into Logical Commits)

## Purpose

When parallel agents leave 50-200+ dirty files, sort them into logical, atomic conventional commits without losing any work.

## Procedure

### Phase 1: Survey

1. `git status --short` (never `-uall`)
2. `git diff --stat` for modified files
3. Count: "N modified, M untracked, K deleted"
4. If < 5 files: just commit normally, skip this skill

### Phase 2: Classify

Group every changed file into categories by path and purpose:

| Category        | Path Pattern                  | Commit Type               |
| --------------- | ----------------------------- | ------------------------- |
| Feature code    | `app/`, `lib/`, `components/` | `feat(scope):`            |
| Database        | `database/migrations/`        | `feat(db):` or `fix(db):` |
| Tests           | `tests/`                      | `test:`                   |
| Scripts/tooling | `scripts/`, `.claude/`        | `chore:`                  |
| Docs            | `docs/`, `*.md`               | `docs:`                   |
| Config          | `package.json`, `*.config.*`  | `chore:`                  |
| Types           | `types/`                      | `chore(types):`           |

Within feature code, sub-group by domain (the folder under `lib/` or `app/`).

### Phase 3: Propose

Present the commit plan:

```
## Proposed Commits (in order)

1. `docs: session digests and build state` (4 files)
2. `feat(lifecycle): cadence scheduler and templates` (7 files)
3. `feat(rail): scoring engine adapters` (5 files)
4. `test: add verification specs` (3 files)
5. `chore: scripts and tooling updates` (6 files)
```

Ask: "Good to commit in this order? Move anything?"

### Phase 4: Execute

For each proposed commit:

1. `git add [specific files]` (NEVER `git add -A`)
2. `git commit -m "message\n\nCo-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"`
3. Verify commit succeeded
4. Move to next group

### Phase 5: Verify

1. `git status` should be clean (or only intentionally untracked files remain)
2. `git log --oneline -N` showing the new commits
3. Report: "Created N commits from M files. Tree clean."

## Constraints

- NEVER delete files. If a file looks wrong, commit it anyway (can revert later)
- NEVER use `git add .` or `git add -A`
- NEVER amend previous commits
- If unsure which group a file belongs to, put it in the most specific commit
- Respect the Co-Authored-By convention
- If any commit would be > 30 files, split it further

## Anti-Patterns

- One giant "chore: sync all changes" commit
- Deleting files that "look like orphans"
- Amending existing commits with new work
- Committing `.env`, credentials, or secrets

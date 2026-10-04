---
name: version-control
description: Manages branch naming, version tracking, and branch lifecycle. Use when user wants to create, list, rename, or clean up branches, or asks about versioning. Triggers on "branch", "version", "new branch", "create branch", "rename branch", "cleanup branches", "what version", "release".
---

# Version Control Workflow

Enforce consistent branch naming, version tracking, and lifecycle management.

For the full naming convention reference, see [branch-conventions.md](branch-conventions.md).

---

## Current State

!`git branch -a --no-color 2>/dev/null | head -40`

!`echo "---" && echo "Current branch:" && git branch --show-current 2>/dev/null`

---

## Branch Creation

When the user asks to create a branch (or you need to create one for a task):

### Phase 0 — Detect Intent

Determine the branch type from the user's request:

| Intent | Type prefix | Example |
|--------|------------|---------|
| New functionality | `feature/` | `feature/date-picker` |
| Bug fix | `fix/` | `fix/badge-truncation` |
| Maintenance / tooling | `chore/` | `chore/upgrade-tailwind-4` |
| Code restructuring | `refactor/` | `refactor/shared-form-styles` |
| Preparing a release | `release/` | `release/v2.0.0` |
| Urgent production fix | `hotfix/` | `hotfix/modal-focus-trap` |

### Phase 1 — Check for Previous Versions

For `feature/` branches, auto-detect if a prior version exists:

```bash
# Search for existing branches matching the feature name
git branch -a --list "*feature/<name>*" --no-color
```

**Version suffix logic:**
- No prior branch exists → use `feature/<name>` (implicitly v1)
- `feature/<name>` exists → suggest `feature/<name>-v2`
- `feature/<name>-v2` exists → suggest `feature/<name>-v3`
- For minor revisions of an active version → suggest `feature/<name>-vN.1`

**Always confirm** the suggested name with the user before creating.

### Phase 2 — Validate Base Branch

Check which branch the user is branching from:

```bash
git branch --show-current
```

- **Acceptable bases:** `main`, `dev`, `develop`
- **Any other base:** Warn the user — they may be branching from a stale feature branch
- If the user confirms the non-standard base, proceed without further warning

### Phase 3 — Create and Track

```bash
git checkout -b <branch-name>
```

On first push, always set upstream:

```bash
git push -u origin <branch-name>
```

---

## Branch Listing

When the user says **"list branches"** or **"show branches"**:

1. Fetch all branches with merge status:

```bash
git branch -a --no-color
git branch --merged main --no-color
```

2. Display grouped by type:

```
Feature branches:
  feature/data-table          ✓ merged
  feature/data-table-v2       ✓ merged
  feature/data-table-v2.1     ✓ merged
  feature/date-picker        ✗ active

Fix branches:
  fix/badge-truncation        ✓ merged

Chore branches:
  chore/ci-pipeline        ✗ active
```

3. Highlight any branches that don't follow the naming convention.

---

## Version History

When the user asks **"what version is [feature]?"**:

1. Search for all branches matching the feature name:

```bash
git branch -a --list "*<feature-name>*" --no-color
```

2. Display a timeline with merge status:

```
feature/data-table     → merged into main (2025-10-15)
feature/data-table-v2  → merged into main (2026-01-20)
feature/data-table-v2.1 → merged into main (2026-02-05)
```

3. Use `git log` to show the date of the last commit on each branch:

```bash
git log -1 --format="%ai" <branch-name>
```

---

## Branch Cleanup

When the user says **"cleanup branches"** or **"delete merged branches"**:

### List-Only Mode (default — never auto-delete)

1. Find all branches merged into `main`:

```bash
git branch --merged main --no-color | grep -v '^\*' | grep -v 'main' | grep -v 'dev'
```

2. Display the list and ask the user which ones to delete:

```
These branches are fully merged into main and safe to delete:

Local:
  [ ] feature/data-table
  [ ] feature/data-table-v2
  [ ] feature/autocomplete

Remote:
  [ ] origin/feature/data-table
  [ ] origin/feature/data-table-v2

Which would you like to delete?
```

3. Only delete what the user explicitly selects:

```bash
# Local
git branch -d <branch-name>

# Remote (only if user confirms)
git push origin --delete <branch-name>
```

**Safety:**
- Use `-d` (not `-D`) — git will refuse if the branch isn't fully merged
- Never delete `main`, `dev`, `develop`, or the current branch
- Always show what will be deleted before executing

---

## Branch Renaming

When the user says **"rename branch"**:

1. Confirm the current name and proposed new name
2. Validate the new name follows the naming convention
3. Rename local:

```bash
git branch -m <old-name> <new-name>
```

4. If the branch has a remote, ask before updating:

```bash
git push origin :<old-name>
git push -u origin <new-name>
```

**Warning:** Renaming a branch with an open PR will break the PR link. Always warn the user about this.

---

## Naming Validation

When creating or renaming a branch, validate the name:

**Valid patterns:**
- `feature/<lowercase-kebab-name>[-vN[.M]]`
- `fix/<lowercase-kebab-description>`
- `chore/<lowercase-kebab-description>`
- `refactor/<lowercase-kebab-description>`
- `release/vX.Y.Z`
- `hotfix/<lowercase-kebab-description>`

**Invalid — warn the user:**
- No type prefix (e.g., `data-table-v3` instead of `feature/data-table-v3`)
- Spaces or uppercase (e.g., `feature/My Feature`)
- Bare version names (e.g., `v2` instead of `release/v2.0.0`)
- Mixed conventions (e.g., `feature_data_table` with underscores)

---

## This repo's shape

- **`main` is the only long-lived branch.** There is no `dev`/`develop`; branch from `main` and warn on anything else.
- **Work merges via PR** (`Merge pull request #N from apuya/<branch>` in the history), so branches are short-lived and cleanup after merge is the norm.
- **`release/vX.Y.Z` branches are part of the convention but unused so far** — there are currently **no git tags**, even though the package is at `1.0.0`. A published library whose versions aren't tagged has no way to answer "what shipped in 1.0.0?". See [`release`](../release/SKILL.md) before the next publish.

## Integration with Other Skills

- **After committing** (commit skill): If the branch has no upstream, suggest `git push -u origin <branch>`
- **When creating a -vN branch**: Consider whether the previous version's files should be protected from accidental edits
- **After PR merge**: Suggest running cleanup to delete the merged branch
- **Before a release** ([`release`](../release/SKILL.md)): a `release/vX.Y.Z` branch should end in a matching git tag — the branch names the work, the tag names what shipped

---

## Safety Rules

- **Never delete unmerged branches** without explicit user confirmation
- **Never force-push** branch renames or deletions
- **Always confirm** before any remote operation (push, delete, rename)
- **Warn on non-standard bases** — flag if branching from anything other than `main`, `dev`, or `develop`
- **Warn on convention violations** — but don't block; the user has final say
- **Preserve PR links** — warn that renaming a branch with an open PR breaks the link

---
name: merge-readiness
description: Validates branch is ready for merge with step-by-step checklist. Use when user asks "is everything ready for merge?", "ready to merge?", "can I merge?", "merge checklist", or "pr ready?".
---

# Merge Readiness Checklist

Run this checklist to validate branch is ready for merge.

## Checklist Template

Copy and track progress:

```
Merge Readiness:
- [ ] 1. Changes reviewed
- [ ] 2. Master merged (no conflicts)
- [ ] 3. Migrations generated (if schema changed)
- [ ] 4. Code quality checks pass
- [ ] 5. Documentation updated
```

## Step 1: Review Changes

Compare current branch to master:

```bash
git fetch origin master
git log origin/master..HEAD --oneline
git diff origin/master...HEAD --stat
```

Review the diff to understand what changed:

```bash
git diff origin/master...HEAD
```

**Summarize changes before proceeding.**

## Step 2: Merge Master

Check if branch is behind master:

```bash
git rev-list --left-right --count origin/master...HEAD
```

Output: `<behind> <ahead>`. If behind > 0, merge is needed.

**If conflicts exist, ask user:**
> Master has diverged. Should I merge master into current branch? (y/n)

If user confirms:

```bash
git merge origin/master
```

If conflicts occur, list them and stop. User must resolve manually.

## Step 3: Check Migrations

Check if schema changed:

```bash
git diff origin/master...HEAD -- dbschema/
```

**If schema files changed**, verify migrations exist:

```bash
git diff origin/master...HEAD -- dbschema/migrations/
```

If schema changed but no new migrations:

> Schema changed but no new migrations found. Run:
> ```bash
> gel migration create
> gel migrate
> ```

**If no schema changes, skip this step.**

## Step 4: Code Quality

Run all checks:

```bash
make check
```

**If checks fail:**
1. Show the errors
2. Ask user if they want help fixing them
3. Do not proceed until checks pass

## Step 5: Documentation

Check if documentation needs updating based on changes.

**Files to check** (compare to changed code):

| Change Type | Required Updates |
|-------------|------------------|
| New command | `notes/help.md`, `deploy/botfather_commands.txt` |
| Flow change | `notes/about.md` |
| New feature | `notes/changelog.md` (`[Latest additions]` section) |
| New query | Verify `gel-py` was run |

Check changelog:

```bash
git diff origin/master...HEAD -- notes/changelog.md
```

**If user-facing changes exist but changelog not updated:**

> User-facing changes detected but `notes/changelog.md` not updated.
> Add entry to `[Latest additions]` section.

## Completion

When all steps pass:

```
Merge Readiness: COMPLETE

- [x] 1. Changes reviewed
- [x] 2. Master merged (no conflicts)
- [x] 3. Migrations generated (if schema changed)
- [x] 4. Code quality checks pass
- [x] 5. Documentation updated

Branch is ready for merge/PR.
```

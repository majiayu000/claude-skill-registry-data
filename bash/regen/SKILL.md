---
name: regen
description: Manually trigger artifact regeneration, versioning, and chore commit. Use when you need fine-grained control over when registry artifacts sync (outside the automated sync-artifacts.yml workflow).
---

# Regen

Manually regenerate registry artifacts, apply version bumps, and commit changes with full control over timing and bump classification.

## When to Use

- Registry changes need immediate artifact sync (not waiting for automated workflow)
- You want to batch multiple registry/script changes into one controlled sync
- Testing registry changes locally before pushing
- Explicit version bump when automated classification might be incorrect
- Emergency registry fixes that need immediate artifact regeneration

## Instructions

### Step 1: Verify Registry Changes Exist

Ensure you have uncommitted or staged changes to:
- `registry/nodes/`
- `registry/named/`
- `registry/schema/`
- `registry/suites/`
- `scripts/` (if regeneration scripts changed)

Check with: `git status`

### Step 2: Determine Bump Type

Classify the changes as one of:

- **patch**: Bug fixes, small registry updates, evidence additions, non-breaking corrections
- **minor**: New skills added, new fields added (non-breaking), schema enhancements
- **major**: Breaking schema changes, deprecated field removals, BREAKING CHANGE in commit message

Default to **patch** if uncertain.

### Step 3: Run the Sync

Execute the sync with your chosen bump type. Replace `BUMP` with `patch`, `minor`, or `major`:

```bash
cd <project-root>
gaia dev release BUMP
gaia dev docs
```

### Step 4: Verify Generated Changes

Check what was generated:
```bash
git status
git diff --stat
```

Review the version changes in:
- `pyproject.toml`
- `packages/cli-npm/package.json`
- `registry/gaia.json`

### Step 5: Commit and Push

If changes look correct:

```bash
git config user.name "$(git config user.name)"
git config user.email "$(git config user.email)"
git add .
git commit -m "chore(manual): regenerate registry artifacts and sync docs (bump: BUMP)"
git push
```

Or if you want to keep the standard message:

```bash
git add .
git commit -m "chore(auto): regenerate registry artifacts and sync docs"
git push
```

## Skipping Auto-Sync on Push

If the automated `sync-artifacts.yml` workflow would conflict with your manual sync, add `[skip-gen]` to your commit message:

```bash
git commit -m "chore(manual): regenerate registry artifacts [skip-gen]"
```

This prevents the automated workflow from re-running on push.

## Notes

- This skill is for **manual, intentional syncs** — the default automated workflow (`.github/workflows/sync-artifacts.yml`) handles routine cases
- Always review generated artifacts before pushing
- Version bumps are locked across all packages (pyproject.toml, npm packages, gaia.json)
- If you make mistakes, use `git reset --hard HEAD~1` to undo the last commit

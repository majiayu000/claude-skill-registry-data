---
name: upstream-sync
description: Sync forked/cloned open source repositories with upstream changes. Fetches upstream diffs, evaluates each change against the local project, and applies changes by directly editing files (no git merge/rebase). Use when user wants to fetch, review, analyze, or integrate new commits from an upstream/original open source repository into their customized fork. Trigger on keywords like "sync upstream", "merge upstream", "rebase upstream", "fork sync", "upstream changes", "new commits from original repo".
---

# Upstream Sync

Sync forked/cloned open source repos with latest upstream changes. Instead of merging commits directly, this skill extracts upstream diffs, evaluates each change, and applies them by editing files directly.

## When to Use

- User mentions "sync", "upstream", "fork", "merge upstream", "rebase upstream"
- User wants to review new commits from an original open source repo
- User needs to integrate upstream changes into their customized branch
- User asks about conflicts between their changes and upstream

## Core Principle

**Never merge/rebase/cherry-pick commits from upstream.** Instead:
1. Extract the actual diffs from upstream
2. Read and evaluate each change against the local project
3. Apply relevant changes by editing files directly (Edit/Write tools)

This gives full control over what gets applied and how, preserving the project's own commit history.

## Workflow

Read [references/sync-workflow.md](references/sync-workflow.md) for the full step-by-step process.

### 1. Check Upstream Status

Run `scripts/upstream-status.js` to detect upstream remote, fetch latest, and list new commits:

```bash
node <skill-path>/scripts/upstream-status.js [--remote <name>] [--branch <branch>] [--since <date>] [--format json|text]
```

### 2. Extract Upstream Diffs

Run `scripts/upstream-diff.js` to get per-file diffs from upstream since last sync:

```bash
# All changes since last sync
node <skill-path>/scripts/upstream-diff.js [--remote <name>] [--branch <branch>] [--format json|text]

# Specific file only
node <skill-path>/scripts/upstream-diff.js --file <path> [--format json]

# Specific commit only
node <skill-path>/scripts/upstream-diff.js --commit <hash> [--format json]

# List changed files without diffs
node <skill-path>/scripts/upstream-diff.js --files-only
```

### 3. Evaluate & Apply

For each changed file from upstream:
1. Read the upstream diff to understand what changed and why
2. Read the current local version of the file
3. Evaluate: should this change be applied? adapted? skipped?
4. If applying: edit the file directly using Edit/Write tools
5. If adapting: modify the upstream change to fit local customizations

Read [references/review-guide.md](references/review-guide.md) for evaluation methodology.

### 4. Overlap Detection (Optional)

Run `scripts/conflict-preview.js` to identify files modified on both sides:

```bash
node <skill-path>/scripts/conflict-preview.js [--remote <name>] [--branch <branch>] [--format json|text]
```

This helps prioritize which files need careful evaluation.

### 5. Save Sync State

After applying changes, save the sync point so the next sync starts from here:

```bash
node <skill-path>/scripts/sync-state.js save [--remote <name>] [--branch <branch>]
```

**Commit `.upstream-sync.json`** to persist the sync point across machines.

To check current state or reset:
```bash
node <skill-path>/scripts/sync-state.js show
node <skill-path>/scripts/sync-state.js reset
```

### 6. Verify & Report

- Run existing test suite
- Build the project
- Review changes with `git diff`
- **Report to user**: Present a summary of all changes applied. See format below.

### Sync Report Format

After completing the sync, ALWAYS present a clear summary to the user:

```
## Upstream Sync Report

**Source**: upstream/main (commits <first-hash>...<last-hash>)
**Date range**: <oldest-commit-date> → <newest-commit-date>
**Total upstream commits reviewed**: <n>

### Applied Changes
- **<file-path>**: <brief description of what was updated and why>
- **<file-path>**: <brief description>
  ...

### New Files Added
- **<file-path>**: <what this file does>

### Skipped Changes
- **<file-path>**: <reason for skipping> (e.g., conflicts with local customization, irrelevant feature)

### Deleted Files
- **<file-path>**: <reason for deletion>

### Notes
- <any important context, breaking changes, or follow-up actions needed>
```

This report helps the user understand exactly what changed and why, so they can make informed decisions about testing and deployment.

## Script Options

All scripts support `--format json` for structured output.

Environment variables (`.env`):
- `UPSTREAM_URL` - URL of the original repo (auto-creates remote if needed)
- `UPSTREAM_REMOTE` - Default upstream remote name (default: `upstream`)
- `UPSTREAM_BRANCH` - Default upstream branch (default: `main`)

---
name: quartz-publish-guard
description: |
  Manage unpublished content in Quartz static site repos. Use when:
  (1) User wants to prevent files without `publish: true` from being committed
  (2) User asks about gitignoring based on frontmatter content
  (3) User wants to unpublish a note or remove it from git
  (4) User wants to purge files from git history
  (5) User asks about the publish workflow with `npx quartz sync`
  Triggers: "publish", "unpublish", "gitignore frontmatter", "purge from history", "quartz sync"
---

# Quartz Publish Guard

Protects unpublished Quartz content from being committed to git.

## Core Concept

Files with `publish: true` in YAML frontmatter → tracked and synced to remote
Files without `publish: true` → local only, never committed

## Scripts in Quartz Repo

| Script | Purpose |
|--------|---------|
| `find-unpublished.sh` | Lists all `.md` files without `publish: true` |
| `update-gitignore.sh --apply` | Adds unpublished files to `.git/info/exclude` (local only) |
| `unpublish.sh --apply` | Removes tracked files that became unpublished |
| `purge-unpublished-from-history.sh --apply` | Removes files from all git history |
| `hooks/pre-commit` | Auto-unstages unpublished files during commits |

## Workflows

### Normal Sync
```bash
npx quartz sync
```
Pre-commit hook auto-unstages unpublished files and updates `.git/info/exclude`.

### Unpublish a Note (change `publish: true` → `publish: false`)
1. Edit frontmatter to `publish: false`
2. Run `./unpublish.sh --apply`
3. Run `npx quartz sync`

### Publish a Note (change `publish: false` → `publish: true`)
1. Edit frontmatter to `publish: true`
2. Run `./update-gitignore.sh --apply` (removes from exclude list)
3. Run `npx quartz sync`

### Purge from Git History
Only needed if sensitive data was accidentally committed.
```bash
./purge-unpublished-from-history.sh --apply
git remote add origin <url>  # filter-repo removes remotes
git push origin v4 --force
```
**Warning**: Creates backup at `../quartz-backup` automatically. Restore local files from backup after purge if needed.

### Purge Specific File from History
```bash
git filter-repo --invert-paths --path <file-path> --force
git remote add origin <url>
git push origin v4 --force
```

## Key Implementation Details

### Why `.git/info/exclude` not `.gitignore`
- `.gitignore` is tracked → exposes filenames publicly
- `.git/info/exclude` is local-only → filenames stay private

### Pre-commit Hook Behavior
1. **Auto-updates `date:` field** for modified markdown files to current ISO timestamp
2. Detects staged `.md` files in `content/` without `publish: true`
3. Auto-unstages unpublished files
4. Runs `update-gitignore.sh --apply`
5. Allows commit to proceed with remaining files

The hook keeps `date_created:` unchanged while updating `date:` to reflect the last modification time.

### git filter-repo Gotchas
- Removes `origin` remote (must re-add after)
- Deletes local files that are tracked AND being removed from history
- Files already untracked survive the purge
- Always use `./unpublish.sh --apply` + `npx quartz sync` BEFORE `git filter-repo` to preserve local files

## Frontmatter Format
```yaml
---
title: "Note Title"
publish: true   # Must be exactly "publish: true" to be published
---
```
Files with `publish: false` or missing `publish` field are treated as unpublished.

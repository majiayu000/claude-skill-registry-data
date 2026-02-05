---
name: syncing-knowledge-garden
description: Syncs the sb-knowledge-base Obsidian vault to the knowledge-garden Quartz site. Use after reorganizing content in Obsidian or when the vault has been updated and the Quartz site needs to match.
---

# Syncing Knowledge Base to Knowledge Garden

## Overview

This skill synchronizes content from **sb-knowledge-base** (Obsidian vault) to **knowledge-garden** (Quartz static site). The vault is the source of truth—all content reorganization should happen in Obsidian first, then sync to Quartz.

**IMPORTANT**: Only files with `publish: true` in their frontmatter are synced. Files without this field or with `publish: false` are excluded from the knowledge garden.

## When to Use

- After reorganizing content in Obsidian (artifacts, notes, links, tags, or types)
- After adding or editing published content in the vault
- When preparing to test a Quartz build with updated content
- When type definitions have been updated in `tools/types/`

## Repository Structure

**sb-knowledge-base** (source):
```
sb-knowledge-base/
├── artifacts/       ← Content to sync
├── links/           ← Content to sync
├── notes/           ← Content to sync
├── tags/            ← Content to sync
└── tools/
    └── types/       ← Content to sync (only this subfolder)
```

**knowledge-garden** (target):
```
knowledge-garden/
├── content/
│   ├── artifacts/   ← Sync destination
│   ├── links/       ← Sync destination
│   ├── notes/       ← Sync destination
│   ├── tags/        ← Sync destination
│   └── types/       ← Sync destination (from tools/types)
├── quartz/
└── quartz.config.ts
```

## Workflow

### 1. Locate Repositories

Find where both repos are cloned on your machine. Common locations:

```bash
# Find sb-knowledge-base
find ~ -type d -name "sb-knowledge-base" 2>/dev/null | head -5

# Find knowledge-garden
find ~ -type d -name "knowledge-garden" 2>/dev/null | head -5
```

Set variables for your paths:
```bash
KB_REPO="/path/to/sb-knowledge-base"
KG_REPO="/path/to/knowledge-garden"
```

### 2. Verify Clean State

Both repos should have no uncommitted changes before syncing:

```bash
cd "$KB_REPO" && git status
cd "$KG_REPO" && git status
```

### 3. Sync Content

Sync all content directories:

```bash
# Sync artifacts
rm -rf "$KG_REPO/content/artifacts"/*
cp -r "$KB_REPO/artifacts"/* "$KG_REPO/content/artifacts"/

# Sync notes
rm -rf "$KG_REPO/content/notes"/*
cp -r "$KB_REPO/notes"/* "$KG_REPO/content/notes"/

# Sync links
rm -rf "$KG_REPO/content/links"/*
cp -r "$KB_REPO/links"/* "$KG_REPO/content/links"/

# Sync tags
rm -rf "$KG_REPO/content/tags"/*
cp -r "$KB_REPO/tags"/* "$KG_REPO/content/tags"/

# Sync types (from tools/types only)
rm -rf "$KG_REPO/content/types"/*
cp -r "$KB_REPO/tools/types"/* "$KG_REPO/content/types"/
```

### 4. Verify Sync

```bash
# Compare file counts for each content type
echo "=== Artifacts ==="
echo "Source:" && find "$KB_REPO/artifacts" -name "*.md" | wc -l
echo "Target:" && find "$KG_REPO/content/artifacts" -name "*.md" | wc -l

echo "=== Notes ==="
echo "Source:" && find "$KB_REPO/notes" -name "*.md" | wc -l
echo "Target:" && find "$KG_REPO/content/notes" -name "*.md" | wc -l

echo "=== Links ==="
echo "Source:" && find "$KB_REPO/links" -name "*.md" | wc -l
echo "Target:" && find "$KG_REPO/content/links" -name "*.md" | wc -l

echo "=== Tags ==="
echo "Source:" && find "$KB_REPO/tags" -name "*.md" | wc -l
echo "Target:" && find "$KG_REPO/content/tags" -name "*.md" | wc -l

echo "=== Types ==="
echo "Source:" && find "$KB_REPO/tools/types" -name "*.md" | wc -l
echo "Target:" && find "$KG_REPO/content/types" -name "*.md" | wc -l
```

### 5. Test Build

```bash
cd "$KG_REPO"
npx quartz build
```

## Quick Sync Commands

For teammates who have both repos in the same parent directory:

```bash
# From parent directory containing both repos
# Sync all content types
rm -rf knowledge-garden/content/artifacts/* && cp -r sb-knowledge-base/artifacts/* knowledge-garden/content/artifacts/ && \
rm -rf knowledge-garden/content/notes/* && cp -r sb-knowledge-base/notes/* knowledge-garden/content/notes/ && \
rm -rf knowledge-garden/content/links/* && cp -r sb-knowledge-base/links/* knowledge-garden/content/links/ && \
rm -rf knowledge-garden/content/tags/* && cp -r sb-knowledge-base/tags/* knowledge-garden/content/tags/ && \
rm -rf knowledge-garden/content/types/* && cp -r sb-knowledge-base/tools/types/* knowledge-garden/content/types/
```

Or use the provided script:
```bash
# From sb-knowledge-base root
./tools/workflows/syncing-content/sync-to-garden.sh
```

## Validation Checklist

- [ ] sb-knowledge-base is on correct branch
- [ ] knowledge-garden is on correct branch
- [ ] Both repos have clean git status
- [ ] File counts match after sync
- [ ] `npx quartz build` succeeds
- [ ] Spot-check a few pages in dev server

## Troubleshooting

### Build fails with type errors
The Quartz type definitions may not match the new content structure. Check `content/types/release.md` and `quartz/types/typeRegistry.ts`.

### Missing files after sync
Ensure you used `cp -r` (recursive) and included the trailing `/*` to copy contents, not the folder itself.

### Links broken on site
Content should be reorganized IN Obsidian first (which auto-updates links), then synced. If you moved files outside Obsidian, links won't be updated.

## Notes

- **Source of truth**: sb-knowledge-base (the Obsidian vault)
- **Never edit content directly in knowledge-garden**—it will be overwritten on next sync
- Always reorganize content in Obsidian to preserve internal links

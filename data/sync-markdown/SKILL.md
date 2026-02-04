---
name: sync-markdown
description: This skill should be used when users want to sync content from text.md files to gallery project index.html files. Trigger phrases include "sync markdown", "sync text.md", "update gallery content", or when users provide a gallery index.html path for content refresh.
---

# Sync Markdown

## Overview

This skill automates full re-rendering of gallery project HTML from `text.md` markdown source files. It does NOT compare differences - it completely regenerates the HTML content between SYNC markers based on `text.md` and styling rules from `/.claude/references/GALLERY_GUIDE.md`.

## When to Use

- User provides a gallery `index.html` path (e.g., `gallery/project-name/index.html`)
- User says "sync markdown", "sync text.md", "update gallery content"
- User needs to refresh HTML after editing markdown or adjusting formatting
- User wants to apply updated spacing/styling rules to existing content

## Workflow

### 1. Extract Project Directory

When user provides an `index.html` path:
- Extract the project directory: `gallery/<project-slug>/`
- Example: `/path/to/gallery/Rider-Dispatch-Scheduling-Platform/index.html` → `gallery/Rider-Dispatch-Scheduling-Platform/`

### 2. Locate Source Files

Find required files in the project directory:
- `text.md` - Markdown source (single source of truth for content)
- `index.html` - Target HTML file
- `public/` - Images directory

### 3. Validate Prerequisites

Check that files exist and are properly configured:
- ✓ `text.md` exists
- ✓ `index.html` exists
- ✓ SYNC markers present: `<!-- SYNC:CONTENT-START -->` and `<!-- SYNC:CONTENT-END -->`
- ✓ Images referenced in `text.md` exist in `public/` directory

If SYNC markers are missing, add them to `index.html` before syncing.

### 4. Execute Full Sync

Run the sync script from project root:

```bash
# Using directory path
node scripts/sync-gallery.js --dir gallery/<project-slug>

# Using slug
node scripts/sync-gallery.js --slug <project-slug>

# Override layout detection
node scripts/sync-gallery.js --dir gallery/<project-slug> --type two-column|stacked
```

**What happens:**
1. Script reads `text.md` completely (no diff comparison)
2. Parses markdown following `GALLERY_GUIDE.md` rules:
   - Sections: `##` or `###` headers
   - Subsections: `####` headers
   - Paragraphs: Text blocks separated by blank lines
   - Lists: `- item` format
   - Images: `![alt](./public/img.png)` or `0.8 ![alt](src)` for scaled images
3. Auto-detects layout type (two-column or stacked) from existing HTML
4. Renders all content into proper HTML structure with correct spacing
5. **Completely replaces** everything between SYNC markers
6. Preserves metadata, hero image, header, footer sections

### 5. Verify Output

Check script success message:
```
Synced /path/to/gallery/project-name (two-column) with 6 sections.
```

Verify in browser or HTML:
- ✓ Section count matches `text.md`
- ✓ Layout type is correct (two-column or stacked)
- ✓ Images display properly
- ✓ Text formatting preserved (bold, italic, links)
- ✓ Spacing matches `GALLERY_GUIDE.md` rules

## Content Format Rules

**All formatting rules are defined in `/.claude/references/GALLERY_GUIDE.md`.**

Key reminders:
- **Blank lines control spacing** - no blank line = same paragraph
- Sections use `###` headers
- Subsections use `####` headers
- Images use `./public/` relative paths
- Lists need blank lines before/after for proper spacing

**For detailed formatting rules, always refer to `/.claude/references/GALLERY_GUIDE.md`.**

## Common Issues

### SYNC markers not found
**Problem:** `index.html` missing sync markers.

**Solution:** Add markers around content area:
```html
<div class="project-content">
    <!-- SYNC:CONTENT-START -->
    <!-- content will be inserted here -->
    <!-- SYNC:CONTENT-END -->
</div>
```

### Images not showing
**Problem:** Image paths incorrect or files missing.

**Fix:**
- Use `./public/<name>.ext` format in `text.md`
- Verify images exist in `gallery/<slug>/public/` directory
- Check filenames match exactly (case-sensitive)

### Wrong layout detected
**Problem:** Script uses wrong template (two-column vs stacked).

**Fix:** Override with `--type` flag:
```bash
node scripts/sync-gallery.js --dir gallery/<slug> --type two-column
```

### Spacing looks wrong
**Problem:** Paragraphs merged or missing spacing.

**Fix:** Check `text.md` for blank lines between:
- Paragraphs
- Lists and paragraphs
- Subsection titles
- Images and text

**Refer to `/.claude/references/GALLERY_GUIDE.md` for spacing rules.**

## Batch Sync (Advanced)

Sync all gallery projects at once:

```bash
for dir in gallery/*/; do
  [ -f "$dir/text.md" ] && node scripts/sync-gallery.js --dir "$dir"
done
```

## Important Notes

- **No diff comparison:** Script fully re-renders from `text.md` every time
- **Complete replacement:** All content between SYNC markers is replaced
- **Formatting adjustments:** Use this when you update spacing/styling rules in GALLERY_GUIDE.md
- **Single source of truth:** `text.md` is authoritative; HTML is generated output

## Resources

**Sync Script:**
- `scripts/sync-gallery.js` - Main synchronization engine

**Formatting Guide:**
- `/.claude/references/GALLERY_GUIDE.md` - Complete content authoring and styling rules

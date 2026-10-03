---
name: elysium-asset-cleanup
description: Audit and clean up image assets — find broken paths, convert formats, remove unused files, fix icon transparency.
---

# Elysium Asset Cleanup

Audit assets for format compliance, broken references, unused files, and transparency issues.

## Asset Rules

| Type | Format | Location |
|------|--------|----------|
| Normal images | WebP | `assets/images/` or `assets/[game]/images/` |
| Transparent icons | PNG | `assets/icons/` or `assets/[game]/icons/` |
| Videos | MP4 | `assets/videos/` |
| Audio | Forbidden | — |

## Checks to Run

### Broken References
- Scan all HTML and CSS files for `src`, `url()`, and `background-image` paths.
- Verify each path resolves to a real file on disk.
- Report any broken references with file and line number.

### Format Compliance
- Flag non-WebP images that should be WebP (excluding transparent icons).
- Flag non-PNG icons that need transparency.
- Flag any audio files (must be removed).
- Flag any references to `orderpanelbg.webp` (removed permanently).

### Unused Assets
- List all files under `assets/`.
- Cross-reference against all HTML/CSS/JS files.
- Report assets not referenced anywhere.

### Icon Transparency
- Arc Raiders sidebar icons: verify `mix-blend-mode: screen` is applied.
- Valorant rank icons: check for dark baked backgrounds needing `mix-blend-mode: screen`.

### File Placement
- Shared images should be in `assets/images/`, not in game-specific folders.
- Game-specific assets should be in `assets/[game]/`, not in shared folders.

## Workflow

1. List all files under `assets/`.
2. Scan all HTML/CSS for asset references.
3. Run each check above.
4. Report findings grouped by category.
5. Suggest fixes but do not apply without approval.
6. Do not commit.

## Output Format

```
## Asset Cleanup Report

### Broken References
- [file:line] references [path] — file not found

### Format Issues
- [path] — should be WebP/PNG/removed

### Unused Assets
- [path] — not referenced in any file

### Transparency Issues
- [element] — needs mix-blend-mode: screen

### Misplaced Files
- [path] — should be in [correct path]
```

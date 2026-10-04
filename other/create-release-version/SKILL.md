---
name: create-release-version
description: Create or update a release version entry in version.md. Use when drafting a new version, cutting a release, or when the user asks to create or update release notes.
---

# Create release version

## Release note structure

Every version entry in **version.md** must include **at least one** of `## Added` or `## Changed`.

```markdown
# X.Y
## Added
- short description

## Changed
- short description
```

- **`# X.Y`** — Version as H1 (two parts, e.g. `0.67`; release tags are `vX.Y`). Must be the very first line of the block.
- **No `# NEXT`.** A feature branch writes the real next version from the start (`main`'s first heading + 1) and renumbers only if another PR takes that number first (`nightly` steps 4 and 7). CI fails on `# NEXT`, and `main` never carries it.
- **`## Added`** — New features. Omit if nothing added.
- **`## Changed`** — Behavior/UI changes. Omit if nothing changed.

**Content guidelines:** User-facing changes only. Skip internal refactors unless they affect behavior. One bullet = one line. Keep it short.

## Instructions

1. Add a new H1 block at the **top** of version.md (above existing versions).
2. Every version needs at least one of `## Added` or `## Changed`. No empty sections.
3. **Initial release:** `## Added` with one sentence describing what the app does. No `## Changed`.
4. **Later releases:** use whichever sections apply. One line per change is fine.

## Example: initial release

```markdown
# 0.1
## Added
- Initial release. Tag-based file reviewer: play clips, assign tags, rename files.
```

## Example: later release

```markdown
# 0.61
## Added
- Click empty window to open file picker.

## Changed
- Migrations consolidated into a single initial schema.
```

## File

- **version.md** — Single file at repo root. Prepend new version blocks; keep older versions below.
- The GitHub Actions release workflow reads the first line (`# VERSION`) to determine the release tag.

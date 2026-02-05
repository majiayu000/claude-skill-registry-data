---
name: release-skill
description: Bump version, update changelog, commit, tag, push, and build release installer
---

# Release Workflow

When the user says "release", "/release", or "push, release", execute this workflow.

## 1. Determine Version

Check current version in `package.json`. Ask user for bump type if not specified:
- **patch**: 0.1.0 → 0.1.1 (bug fixes)
- **minor**: 0.1.0 → 0.2.0 (new features)
- **major**: 0.1.0 → 1.0.0 (breaking changes)

## 2. Update Version in All Files

Update version string in these three files:
- `package.json` - field `"version": "X.Y.Z"`
- `src-tauri/Cargo.toml` - field `version = "X.Y.Z"`
- `src-tauri/tauri.conf.json` - field `"version": "X.Y.Z"`

## 3. Update CHANGELOG.md

1. Move all content under `## [Unreleased]` to a new version section
2. Add today's date in format `## [X.Y.Z] - YYYY-MM-DD`
3. Leave empty `## [Unreleased]` section at top

Example:
```markdown
## [Unreleased]

## [0.2.0] - 2025-12-29

### Pridane
- New feature...
```

## 4. Build Release

Build BEFORE committing to verify everything works:

```bash
npm run tauri build
```

If build fails, fix issues and retry. Don't proceed until build succeeds.

## 5. Commit, Tag, and Push

Only after successful build:

```bash
git add -A
git commit -m "chore: release vX.Y.Z"
git tag vX.Y.Z
git push && git push --tags
```

## 6. Report Results

Show the path to the built installer:
- NSIS installer: `src-tauri/target/release/bundle/nsis/Kniha Jázd_X.Y.Z_x64-setup.exe`

## Notes

- Cargo.lock will auto-update - include it in the commit
- CHANGELOG is in Slovak (Pridane, Zmenene, Opravene)

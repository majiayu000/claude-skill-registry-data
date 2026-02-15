---
name: release-har
description: "Universal release automation. CHANGELOG, commit, tag, GitHub Release supported. Use when user mentions release, version bump, create tag, publish release. Do NOT load for: harness release (use x-release-harness instead)."
description-en: "Universal release automation. CHANGELOG, commit, tag, GitHub Release supported. Use when user mentions release, version bump, create tag, publish release. Do NOT load for: harness release (use x-release-harness instead)."
description-ja: "汎用リリース自動化。CHANGELOG、コミット、タグ、GitHub Release をサポート。Use when user mentions release, version bump, create tag, publish release. Do NOT load for: harness release (use x-release-harness instead)."
allowed-tools: ["Read", "Write", "Edit", "Bash"]
argument-hint: "[patch|minor|major]"
context: fork
---

# Release Har Skill

Universal release automation skill. Works with any project.

## Quick Reference

- "**release**" -> `/release-har`
- "**bump version**" -> `/release-har patch`
- "**minor release**" -> `/release-har minor`

---

## Execution Flow

### Step 1: Check Current State

Run in parallel:

```bash
# Uncommitted changes
git status

# Changed files
git diff --stat

# Recent commit history
git log --oneline -10

# Existing tags
git tag --sort=-v:refname | head -5
```

### Step 2: Determine Version

Based on [Semantic Versioning](https://semver.org/):

| Version | Change Type |
|---------|-------------|
| **patch** (x.y.Z) | Bug fixes, minor improvements |
| **minor** (x.Y.0) | New features (backward compatible) |
| **major** (X.0.0) | Breaking changes |

Ask user: "What should the next version be? (e.g., 1.2.3)"

### Step 3: Update CHANGELOG (if exists)

If project has CHANGELOG.md, update it:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature

### Changed
- Change description

### Fixed
- Bug fix
```

**Skip if CHANGELOG does not exist**

### Step 4: Update Version Files (project-dependent)

Update version files based on project configuration:

| File | Update Method |
|------|---------------|
| `package.json` | `"version": "X.Y.Z"` |
| `pyproject.toml` | `version = "X.Y.Z"` |
| `VERSION` | Direct content update |
| `Cargo.toml` | `version = "X.Y.Z"` |

**Skip if no applicable file exists**

### Step 5: Commit and Tag

```bash
# Stage
git add -A

# Commit (only if changes exist)
git commit -m "chore: release vX.Y.Z"

# Create tag
git tag -a vX.Y.Z -m "Release vX.Y.Z"
```

### Step 6: Push

```bash
# Push branch
git push origin $(git branch --show-current)

# Push tag
git push origin vX.Y.Z
```

### Step 7: GitHub Release (Optional)

After user confirmation, create GitHub Release:

```bash
gh release create vX.Y.Z \
  --title "vX.Y.Z - Title" \
  --notes "$(cat <<'EOF'
## What's Changed

- Change 1
- Change 2

**Full Changelog**: https://github.com/OWNER/REPO/compare/vPREV...vX.Y.Z
EOF
)"
```

---

## Options

| Option | Description |
|--------|-------------|
| `patch` | Auto-increment patch version |
| `minor` | Auto-increment minor version |
| `major` | Auto-increment major version |
| `--dry-run` | Preview only, no execution |

---

## Project-Specific Handling

### Node.js (package.json)

```bash
npm version patch --no-git-tag-version
```

### Python (pyproject.toml)

Manually update `version = "X.Y.Z"`

### Rust (Cargo.toml)

Manually update `version = "X.Y.Z"`

---

## Related Skills

- `x-release-harness` - Harness plugin specific release (local only)
- `verify` - Pre-release verification

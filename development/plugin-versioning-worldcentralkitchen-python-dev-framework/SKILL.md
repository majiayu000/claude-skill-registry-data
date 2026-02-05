---
name: plugin-versioning
description: >
  Guide for versioning and releasing Claude Code plugins. Covers semantic
  versioning, CHANGELOG maintenance, and the automated release workflow.
triggers:
  - version
  - release
  - tag
  - changelog
  - semver
  - bump version
---

# Plugin Versioning Guide

## Agent Instructions

After completing your release steps (CHANGELOG, plugin.json, PR), **always inform the user of their required next steps**:

1. Merge the release PR
2. Create and push the version tag:
   ```bash
   git checkout main && git pull
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```
3. Review/merge the marketplace PR (created automatically by the release workflow)

**Do not assume the user knows the tag triggers the release workflow.**

## Semantic Versioning for Plugins

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Breaking: hook behavior, removed features | MAJOR | 1.0.0 → 2.0.0 |
| New: skill, command, agent, feature | MINOR | 1.0.0 → 1.1.0 |
| Fix: bug fix, typo, docs | PATCH | 1.0.0 → 1.0.1 |

## Release Checklist

1. **Update CHANGELOG.md**
   - Move items from `[Unreleased]` to new version section
   - Add release date

2. **Update plugin.json version**
   ```json
   {
     "version": "1.1.0"
   }
   ```

3. **Create release branch and PR**
   ```bash
   git checkout -b chore/release-v1.1.0
   git add CHANGELOG.md .claude-plugin/plugin.json
   git commit -m "chore: release v1.1.0"
   git push -u origin chore/release-v1.1.0
   gh pr create --title "chore: release v1.1.0" --body "Release v1.1.0"
   ```

4. **Human merges PR, then tag**
   ```bash
   # After PR is merged by human:
   git checkout main && git pull
   git tag v1.1.0
   git push origin v1.1.0
   ```

5. **Automated steps** (GitHub Action handles these)
   - Creates GitHub Release with auto-generated notes
   - Syncs plugin essentials to marketplace repo (`plugins/python-dev-framework/`)
   - Updates version in `marketplace.json`
   - Opens PR on marketplace repo
   - Human reviews and merges marketplace PR

## CHANGELOG Format

Follow [Keep a Changelog](https://keepachangelog.com/):

```markdown
## [Unreleased]

## [1.1.0] - 2025-01-15

### Added
- New plugin-versioning skill

### Changed
- Updated hook timeout from 10s to 15s

### Fixed
- Fixed edge case in branch name validation
```

## Version Locations

| File | Field |
|------|-------|
| `.claude-plugin/plugin.json` | `"version": "X.Y.Z"` |
| `CHANGELOG.md` | `## [X.Y.Z] - YYYY-MM-DD` |
| Git tag | `vX.Y.Z` |

## Pre-release Versions

For beta or release candidate versions:

```bash
git tag v1.1.0-beta.1
git tag v1.1.0-rc.1
```

Pre-release tags follow semver format and can be used for testing before stable release.

## Marketplace Distribution

On release, the GitHub Action syncs plugin files to the marketplace repo:

| Source | Destination |
|--------|-------------|
| `.claude-plugin/` | `plugins/python-dev-framework/.claude-plugin/` |
| `hooks/` | `plugins/python-dev-framework/hooks/` |
| `skills/` | `plugins/python-dev-framework/skills/` |
| `CLAUDE.md` | `plugins/python-dev-framework/CLAUDE.md` |
| `.lsp.json` | `plugins/python-dev-framework/.lsp.json` |

**Note:** The `plugins/` directory in the marketplace repo is auto-generated. Do not edit directly.

Users install from the marketplace (bundled copy), not from this repo:
```bash
claude plugin install python-dev-framework@WorldCentralKitchen
```

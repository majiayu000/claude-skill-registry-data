---
name: changelog-management
description: Manage project changelogs with commit tracking and structured documentation. Use when updating CHANGELOG.md, tracking project changes, or documenting version releases.
---

# Changelog Management

## Overview

This skill covers best practices for maintaining project changelogs, including commit tracking, version management, and structured change documentation following the [Keep a Changelog](https://keepachangelog.com/) standard.

## Changelog Structure

### Standard Format

```markdown
# Changelog

## [Unreleased]
### Planned
- [ ] Feature name

## [Version] - YYYY-MM-DD
### Added
- **Feature Name** ([commit](link))
  - Description

### Changed
- **Feature Name** ([commit](link))
  - What changed

### Fixed
- **Bug Description** ([commit](link))
  - What was fixed

### Documentation
- **Document Name** ([commit](link))
  - What was updated
```

## Version Formatting

### Semantic Versioning

- **Format**: `[MAJOR.MINOR.PATCH]`
- **Breaking Changes**: Increment MAJOR (1.0.0 → 2.0.0)
- **New Features**: Increment MINOR (0.1.0 → 0.2.0)
- **Bug Fixes**: Increment PATCH (0.1.0 → 0.1.1)

### Date Format

- **Format**: ISO 8601 `YYYY-MM-DD`
- **Example**: `2025-01-15`
- **Consistency**: Always use same format

## Commit Tracking

### Getting Commit Information

```bash
# Short commit hash
git log --oneline -1
# Output: abc1234 feat: add search

# Full commit hash
git rev-parse HEAD
# Output: abc1234567890abcdef1234567890abcdef1234

# Commit for specific file
git log --oneline -1 -- path/to/file.rs
```

### Commit Reference Formats

**Short Hash with Link** (Recommended):
```markdown
- **Feature** ([abc1234](https://github.com/user/repo/commit/abc1234))
```

**Multiple Commits**:
```markdown
- **Feature** ([abc1234](link), [def5678](link))
```

**Commit Range**:
```markdown
- **Feature** ([abc1234..def5678](https://github.com/user/repo/compare/abc1234..def5678))
```

**Without Link**:
```markdown
- **Feature** (commit: abc1234)
```

## Change Categories

### Added

For new features, functionality, or capabilities:

```markdown
### Added
- **Search Functionality** ([abc1234](link))
  - Real-time search by title and description
  - Search history with recent searches
  - Keyboard shortcut (Ctrl/Cmd + K)
```

### Changed

For changes to existing functionality:

```markdown
### Changed
- **Storage Implementation** ([def5678](link)) (2025-02-01)
  - Migrated from localStorage to IndexedDB
  - Improved performance for large datasets
  - Added automatic data migration script
```

### Fixed

For bug fixes:

```markdown
### Fixed
- **GitHub Pages Deployment** ([ghi9012](link)) (2025-02-01)
  - Fixed `base_path` configuration (added leading slash)
  - Fixed 404.html for client-side routing
  - Fixed file copying to include all subdirectories
```

### Documentation

For documentation updates:

```markdown
### Documentation
- **Cursor Rules** ([jkl3456](link)) (2025-02-01)
  - Created comprehensive rule structure
  - Added project structure guidelines
  - Added code formatting standards
```

## Workflow Patterns

### Adding a New Feature

1. **Develop and commit**:
   ```bash
   git commit -m "feat: add search functionality"
   ```

2. **Get commit hash**:
   ```bash
   git log --oneline -1
   # Output: abc1234 feat: add search functionality
   ```

3. **Update CHANGELOG.md**:
   ```markdown
   ## [Unreleased]
   ### Planned
   - [x] Add search functionality ✅

   ## [0.2.0] - 2025-02-01
   ### Added
   - **Search Functionality** ([abc1234](https://github.com/user/repo/commit/abc1234))
     - Real-time search by title and description
     - Search history with recent searches
   ```

4. **Update version in Cargo.toml**:
   ```toml
   [package]
   version = "0.2.0"
   ```

### Fixing a Bug

1. **Fix and commit**:
   ```bash
   git commit -m "fix: correct base_path configuration"
   ```

2. **Update CHANGELOG.md**:
   ```markdown
   ### Fixed
   - **GitHub Pages Deployment** ([abc1234](link)) (2025-02-01)
     - Fixed `base_path` configuration (added leading slash)
   ```

### Breaking Changes

Mark clearly with migration notes:

```markdown
## [2.0.0] - 2025-03-01

### Changed (Breaking)
- **Storage API** ([abc1234](link)) (2025-03-01)
  - Changed storage key format from `reminders` to `reminders_v2`
  - **Migration Required**: Run migration script before upgrading
  - Old data format no longer supported
```

## Best Practices

### DO:
- ✅ Include commit hashes for all changes
- ✅ Use clear, descriptive change descriptions
- ✅ Group related changes together
- ✅ Include dates for significant changes
- ✅ Explain the "why" for major changes
- ✅ Mark breaking changes clearly
- ✅ Update with every release
- ✅ Link commits to GitHub (if available)

### DON'T:
- ❌ Don't use vague descriptions
- ❌ Don't mix different change types in one entry
- ❌ Don't forget to include dates
- ❌ Don't skip version numbers
- ❌ Don't forget commit references
- ❌ Don't include internal-only changes (unless relevant)

## Automation Tips

### Generate Commit List

```bash
# Get commits since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# Get commits for a specific version
git log v0.1.0..v0.2.0 --oneline
```

### Extract Commit Messages

```bash
# Get commit messages for changelog
git log --pretty=format:"- %s ([%h](https://github.com/user/repo/commit/%H))" v0.1.0..HEAD
```

## Integration with Development Plan

Link CHANGELOG to DEVELOPMENT_PLAN:

```markdown
### Added
- **Search Functionality** ([abc1234](link))
  - Real-time search by title and description
  - See [DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md) for details
  - Related issue: #123
  - Related PR: #456
```

## Version Release Process

### Pre-Release Checklist

- [ ] Update CHANGELOG.md with all changes
- [ ] Include commit references for all entries
- [ ] Update version in Cargo.toml
- [ ] Review all changes for accuracy
- [ ] Check for breaking changes

### Release Steps

1. **Finalize CHANGELOG**:
   ```markdown
   ## [0.2.0] - 2025-02-01
   [All changes with commit references]
   ```

2. **Update version**:
   ```toml
   [package]
   version = "0.2.0"
   ```

3. **Create git tag**:
   ```bash
   git tag -a v0.2.0 -m "Release v0.2.0"
   git push origin v0.2.0
   ```

4. **Create GitHub release**:
   - Use CHANGELOG content as release notes
   - Link to commit range
   - Mark as latest release

### Post-Release

- [ ] Move `[Unreleased]` items to new version section
- [ ] Update DEVELOPMENT_PLAN.md with completed features
- [ ] Update version history section

## Resources

- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) - Standard format
- [Semantic Versioning](https://semver.org/spec/v2.0.0.html) - Version numbering
- [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) - Date format standard
- [Conventional Commits](https://www.conventionalcommits.org/) - Commit message format


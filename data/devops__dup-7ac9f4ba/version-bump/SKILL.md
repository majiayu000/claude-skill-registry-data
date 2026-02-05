---
name: version-bump
description: Determines appropriate semantic version bumps based on changes. Use when deciding version numbers, evaluating breaking changes, or planning releases. Triggers on terms like "version", "semver", "breaking change", "major/minor/patch".
---

# Semantic Versioning Skill

This skill helps determine appropriate version bumps following [Semantic Versioning](https://semver.org/).

## Version Format

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: Breaking changes
- **MINOR**: New features, backwards compatible
- **PATCH**: Bug fixes, backwards compatible

## Version Bump Decision Tree

### MAJOR (X.0.0) - Breaking Changes

Bump MAJOR when you make incompatible API changes:

- Removed public functions, methods, or types
- Changed function signatures (parameters, return types)
- Renamed public APIs
- Changed default behavior that breaks existing usage
- Removed CLI flags or changed their meaning
- Changed configuration file format incompatibly

### MINOR (0.X.0) - New Features

Bump MINOR when you add functionality in a backwards compatible manner:

- New commands or subcommands
- New CLI flags
- New configuration options
- New output formats
- New integrations or providers

### PATCH (0.0.X) - Bug Fixes

Bump PATCH when you make backwards compatible bug fixes:

- Fix incorrect behavior
- Fix crashes or errors
- Performance improvements (no API changes)
- Documentation fixes
- Internal refactoring (no behavior changes)

## Quick Reference

| Change Type                      | Version Bump |
|----------------------------------|--------------|
| Breaking API change              | MAJOR        |
| Removed feature                  | MAJOR        |
| New command/feature              | MINOR        |
| New CLI flag                     | MINOR        |
| New provider/integration         | MINOR        |
| Bug fix                          | PATCH        |
| Performance fix                  | PATCH        |
| Documentation only               | PATCH        |
| Refactoring (no behavior change) | PATCH        |

## Pre-1.0 Versioning

For versions < 1.0.0 (like this project):
- MINOR can include breaking changes
- PATCH is for bug fixes and small features
- More flexibility before reaching stability

## Instructions

1. Review all changes since last release:
   ```bash
   git log --oneline $(git describe --tags --abbrev=0)..HEAD
   ```

2. Check for breaking changes:
   - Removed or renamed public APIs?
   - Changed default behaviors?
   - Incompatible configuration changes?

3. If breaking changes exist -> MAJOR bump

4. If new features exist -> MINOR bump

5. If only fixes/refactoring -> PATCH bump

## Version Update Locations

When bumping version, update:

1. **Cargo.toml** - `version = "X.Y.Z"`
2. **CHANGELOG.md** - Add `## [X.Y.Z] - YYYY-MM-DD` section
3. **Version links** - Update comparison URLs at bottom of CHANGELOG.md

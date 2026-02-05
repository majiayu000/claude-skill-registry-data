---
name: git-changelog
description: Generate changelog from git commits and manage versions.
---

# Git Changelog Generator

## Instructions

When releasing a new version:

1. **Generate commit log**: `git log --oneline --since="..."`
2. **Group by type**: Features, Fixes, Changes
3. **Format for changelog**: Keep, markdown format
4. **Update version constant**: Update `PLUGIN_VERSION`
5. **Tag the release**: `git tag v0.1.0`

## Changelog Pattern

```markdown
## 0.1.0 - 2025-12-29

### Added

-   Initial release with retro login page
-   Custom login page styling
-   Login redirect functionality

### Changed

-   Updated Howdy boilerplate structure

### Fixed

-   Security: ABSPATH check added to all files
```

## Generate Log Command

```bash
# Since last tag
git log --oneline $(git describe --tags --abbrev=0 2>/dev/null || v0.0.0)..HEAD

# Since specific date
git log --oneline --since="2025-12-01"

# All commits
git log --oneline -20
```

## Version Update

Update in `retrologin.php`:

```php
const PLUGIN_VERSION = '0.1.0';
```

## Git Tag

```bash
# Create tag
git tag -a v0.1.0 -m "Version 0.1.0"

# Push tag
git push origin v0.1.0

# List tags
git tag -l
```

## Guidelines

-   Follow Semantic Versioning (MAJOR.MINOR.PATCH)
-   Keep changelog in readme.txt or CHANGELOG.md
-   Tag before publishing to WordPress.org
-   Test after version bump

---
name: prepare-release
description: Prepare a new release by updating CHANGELOG.md with changes since the last tag and bumping version numbers in pyproject.toml and ui/package.json
---

# Prepare Release

When preparing a release, follow these steps:

## 1. Fetch tags and identify the last release

```bash
git fetch --tags
git tag --sort=-creatordate | head -5
```

## 2. Get commits since the last release

```bash
git log --oneline <last-tag>..HEAD
```

## 3. Read current files

Read these files to understand current state:
- `CHANGELOG.md` - to understand the format and existing entries
- `pyproject.toml` - to get current version
- `ui/package.json` - to get current UI version

## 4. Update CHANGELOG.md

- Add a new version section at the top (below the `# Changelog` header)
- Organize changes into categories:
  - **Breaking Changes** - API changes that require user action
  - **New Features** - New functionality
  - **Internal Improvements** - Refactoring, tests, tooling
- Use bold headers for each change group
- Use bullet points for details
- If there was an "Unreleased" section, rename it to the previous version

## 5. Bump versions

Update the version string in:
- `pyproject.toml` - the `version` field under `[project]`
- `ui/package.json` - the `"version"` field

Use semantic versioning:
- Patch (0.0.x) for bug fixes
- Minor (0.x.0) for new features
- Major (x.0.0) for breaking changes

## 6. Summary

After completing, summarize what was updated:
- New version number
- Key changes added to changelog
- Files modified

---
name: git-changelog
description: Git workflow, changelog conventions, and commit practices for the image-scoring-gallery project.
---

# Git & Changelog Conventions

## Git MCP Server

The `git` MCP server is enabled and configured for the `image-scoring` repo. For the `image-scoring-gallery` repo, use the built-in git tools or run git commands directly.

### Available MCP Git Tools

| Tool | Purpose |
|------|---------|
| `mcp_git_git_status` | Check working tree status |
| `mcp_git_git_log` | View commit history |
| `mcp_git_git_diff_unstaged` | See uncommitted changes |
| `mcp_git_git_diff_staged` | See staged changes |
| `mcp_git_git_add` | Stage files |
| `mcp_git_git_commit` | Create commits |
| `mcp_git_git_branch` | List branches |
| `mcp_git_git_create_branch` | Create feature branches |
| `mcp_git_git_checkout` | Switch branches |

> [!NOTE]
> The MCP git server may be configured for a specific backend clone. For this gallery repo, use shell `git` commands or your editor’s git integration.

## Changelog Format

The project uses [Keep a Changelog](https://keepachangelog.com/) format in `CHANGELOG.md`:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [3.17.0] - 2026-02-12

### Added
- New feature description

### Changed
- What was modified

### Fixed
- Bug fix description
```

### Section Types
- **Added**: New features
- **Changed**: Modifications to existing features
- **Fixed**: Bug fixes
- **Removed**: Removed features
- **Deprecated**: Soon-to-be-removed features
- **Security**: Vulnerability fixes

## Workflow: Update Changelog & Commit

### Step 1: Research Recent Changes
```bash
cd /path/to/image-scoring-gallery
git log --oneline -10
git status
git diff --stat HEAD~5
```

### Step 2: Update CHANGELOG.md
- Add new version section at the top (below the header)
- Use semantic versioning: `MAJOR.MINOR.PATCH`
- Include today's date in `YYYY-MM-DD` format
- Group changes by type (Added/Changed/Fixed)

### Step 3: Commit & Push
```bash
git add CHANGELOG.md
git commit -m "docs: update changelog for vX.Y.Z"
git push origin main
```

## Version Numbering

The current version is in `package.json` (`"version": "3.17.0"`). Follow semver:
- **MAJOR**: Breaking changes (rare for this app)
- **MINOR**: New features (new sort option, new viewer mode, etc.)
- **PATCH**: Bug fixes, minor UI tweaks

When bumping the version:
1. Update `package.json` `version` field
2. Add corresponding changelog entry
3. Commit both files together

## Commit Message Style

Use conventional-ish prefixes:
- `feat:` — new features
- `fix:` — bug fixes
- `docs:` — documentation only
- `refactor:` — code changes that don't add features or fix bugs
- `style:` — formatting, UI-only changes
- `chore:` — maintenance, dependencies

---
name: changelog
description: "Generates a changelog from git history following Keep a Changelog format. Categorizes commits into Added, Changed, Fixed, Removed, Security, and Breaking Changes. Use before releases or to document recent work."
argument-hint: "[from-tag, 'last-release', or 'unreleased']"
allowed-tools: Read, Bash(git *), Write
---

# Generate Changelog

## Git History
!`git log --oneline --no-merges -50 2>/dev/null`

## Tags
!`git tag --sort=-v:refname 2>/dev/null | head -10`

## Latest Tag
!`git describe --tags --abbrev=0 2>/dev/null || echo "No tags found"`

---

## Instructions

### Step 1: Determine Range
- If a tag/ref is provided, use: `git log <tag>..HEAD`
- If "last-release" is specified, find the most recent tag
- If "unreleased" or no argument, show all commits since last tag

### Step 2: Gather Commits
Run: `git log <range> --oneline --no-merges`

For each commit, extract:
- Commit hash (short)
- Commit message
- Author
- Date
- PR number (if referenced)

### Step 3: Categorize
Group commits using [Keep a Changelog](https://keepachangelog.com/) categories:

- **Added**: New features, endpoints, commands, pages
- **Changed**: Modifications to existing functionality, API changes
- **Fixed**: Bug fixes, error corrections
- **Deprecated**: Features marked for removal
- **Removed**: Deleted features, removed dependencies
- **Security**: Vulnerability fixes, security improvements
- **Breaking Changes**: Changes that require consumer updates

Detection heuristics:
- `feat:` / `feature:` / `add:` → Added
- `fix:` / `bugfix:` / `hotfix:` → Fixed
- `refactor:` / `update:` / `change:` → Changed
- `remove:` / `delete:` / `drop:` → Removed
- `security:` / `vuln:` / `cve:` → Security
- `BREAKING:` / `BREAKING CHANGE:` → Breaking Changes
- Other: categorize by reading the commit message

### Step 4: Format Output

```markdown
# Changelog

## [Unreleased] — YYYY-MM-DD

### Added
- Description of new feature (#PR)

### Changed
- Description of change (#PR)

### Fixed
- Description of fix (#PR)

### Removed
- Description of removal (#PR)

### Security
- Description of security fix (#PR)

### Breaking Changes
- Description of breaking change (#PR)
```

### Step 5: Save or Display
- If a CHANGELOG.md exists, prepend the new section
- If not, create a new CHANGELOG.md
- Always show the generated content for review before saving

---

## Rules
- Follow [Keep a Changelog](https://keepachangelog.com/) format exactly
- Include PR/issue references where available
- Don't include merge commits
- Don't include chore/ci-only commits unless significant
- Group related commits into single entries where appropriate

---
name: bump-release
description: Execute automated release workflow for Rust projects using Conventional Emoji Commits. Analyze commits since last release, determine semantic version bump (MAJOR/MINOR/PATCH), update Cargo.toml, generate changelog with git-cliff, create git tags, and publish GitHub releases. Use when the user requests to cut a release, bump version, create a release, or publish a new version. Also use when the user asks about the release process or wants to preview what the next release would be.
---

# Bump Release

## Overview

This skill executes the complete automated release workflow for Rust projects that follow Conventional Emoji Commits. Execute this workflow when a user requests to create a release, bump the version, or publish a new version of the project.

The workflow:
1. Analyzes all commits since the last release tag
2. Determines the appropriate semantic version bump (MAJOR, MINOR, PATCH, or NONE)
3. Updates version fields in Cargo.toml file(s)
4. Generates a changelog section using git-cliff
5. Creates a release commit and annotated git tag
6. Pushes changes to GitHub
7. Creates a GitHub Release with generated changelog

## When to Use This Skill

Use this skill when the user:
- Requests to "create a release" or "cut a release"
- Asks to "bump the version" or "publish a new version"
- Wants to "see what the next release would be" (use dry-run mode)
- Asks about the release process or workflow
- Requests to "create a GitHub release"
- Mentions tagging a version

**Examples:**
- "Create a new release for this project"
- "Bump the version and publish"
- "What would the next release version be?"
- "Cut a release based on recent commits"
- "Create version 1.2.0"

## Prerequisites

Before executing the release workflow, verify the following requirements are met:

### Required Tools

Check that these tools are installed:
- `git` - Version control
- `gh` (GitHub CLI) - For creating GitHub releases
- `git-cliff` - Changelog generation (install with `cargo install git-cliff`)
- `python3` (version 3.7+) - For analysis scripts
- `cargo` - Rust build tool (for validation)

**Installation check:**
```bash
command -v git && command -v gh && command -v git-cliff && command -v python3 && command -v cargo
```

### GitHub Authentication

Verify GitHub CLI is authenticated:
```bash
gh auth status
```

If not authenticated, run:
```bash
gh auth login
```

### Repository State

Ensure:
- Working directory is clean (no uncommitted changes)
- Currently on the main branch (or configured release branch)
- Have permission to push to the repository

### git-cliff Configuration (Optional)

While optional, having a `.cliff.toml` or `cliff.toml` configuration file at the project root improves changelog formatting. The skill will use default git-cliff configuration if no config file exists.

## Workflow Decision Tree

Choose the appropriate workflow based on the user's request:

```
User requests release?
├─ Yes → Determine workflow type:
│  ├─ "What would the next release be?" → Execute DRY-RUN workflow
│  ├─ "Create a release but don't push" → Execute LOCAL-ONLY workflow
│  ├─ "Create a pre-release" → Execute PRERELEASE workflow
│  └─ "Create a release" → Execute FULL workflow
└─ No → Not applicable for this skill
```

## Release Workflows

### Full Release Workflow (Default)

Execute this workflow for standard releases that will be pushed to GitHub.

**Steps:**

1. **Verify prerequisites** - Check all required tools are installed and repository state is valid

2. **Execute the main script:**
   ```bash
   ./scripts/bump_release.sh
   ```

3. **The script will automatically:**
   - Fetch latest tags from remote
   - Analyze commits since last release tag
   - Parse commit messages for Conventional Emoji Commit types
   - Determine semantic version bump (MAJOR for breaking changes, MINOR for features, PATCH for fixes)
   - Display analysis summary and new version
   - Update version in all Cargo.toml files (workspace root and members)
   - Run `cargo check` to validate changes
   - Generate changelog section using git-cliff
   - Update or create CHANGELOG.md file
   - Create release commit with format: `🔖 release: bump version to vX.Y.Z`
   - Create annotated git tag (e.g., `v1.2.3`)
   - Push commit and tag to remote
   - Create GitHub Release with changelog

4. **Verify the release:**
   - Check GitHub Releases page for new release
   - Verify version in Cargo.toml is updated
   - Review CHANGELOG.md for new entry

### Dry-Run Workflow (Preview)

Execute this workflow when the user wants to see what would happen without making any changes.

**Steps:**

1. **Execute with dry-run flag:**
   ```bash
   ./scripts/bump_release.sh --dry-run
   ```

2. **Review output:**
   - Current version
   - Commits since last release
   - Determined bump type (MAJOR, MINOR, PATCH, or NONE)
   - New version that would be created
   - Changelog content that would be generated
   - Files that would be modified

3. **Explain findings to user:**
   - "Based on X commits since vY.Z.W, the next release would be vA.B.C"
   - "This is a [MAJOR/MINOR/PATCH] bump because [reason]"
   - Show commit types found (features, fixes, breaking changes)
   - Preview changelog content

4. **If no releasable commits:**
   - Inform user: "No releasable commits found since last release"
   - Explain: "Only found documentation, style, refactoring, or test commits"
   - Suggest: "Need at least one feat, fix, or breaking change commit"

### Local-Only Workflow

Execute this workflow when the user wants to prepare a release locally without pushing to GitHub.

**Steps:**

1. **Execute with no-push flag:**
   ```bash
   ./scripts/bump_release.sh --no-push
   ```

2. **The script will:**
   - Perform all release steps locally
   - Create commit and tag
   - **NOT** push to remote
   - **NOT** create GitHub Release

3. **Inform user:**
   - "Release prepared locally as vX.Y.Z"
   - "To push: `git push && git push origin vX.Y.Z`"
   - "To create GitHub release: `gh release create vX.Y.Z`"

### Pre-Release Workflow

Execute this workflow for alpha, beta, or release candidate versions.

**Steps:**

1. **Execute with prerelease flag:**
   ```bash
   ./scripts/bump_release.sh --prerelease
   ```

2. **The script will:**
   - Perform full release workflow
   - Mark GitHub Release as "pre-release"
   - This prevents it from being marked as "Latest"

3. **Note:** Pre-release versions should follow semantic versioning prerelease format:
   - `1.0.0-alpha.1`
   - `1.0.0-beta.2`
   - `1.0.0-rc.1`

### Custom Branch Workflow

Execute this workflow when releasing from a branch other than `main`.

**Steps:**

1. **Specify branch:**
   ```bash
   ./scripts/bump_release.sh --branch develop
   ```

2. **Use case:** For projects that release from different branches (e.g., `develop`, `release`, `stable`)

## Commit Analysis Logic

The skill parses Conventional Emoji Commits to determine version bumps. Refer to `references/conventional-emoji-commits.md` for complete details.

**Quick reference:**

| Commit Type | Version Bump | Examples |
|-------------|--------------|----------|
| `🚨 BREAKING CHANGE` or `BREAKING CHANGE:` footer | **MAJOR** (1.0.0 → 2.0.0) | Breaking API changes |
| `✨ feat` or `✨ feature` | **MINOR** (1.0.0 → 1.1.0) | New features |
| `🩹 fix` or `⚡️ perf` | **PATCH** (1.0.0 → 1.0.1) | Bug fixes, performance |
| `📚 docs`, `🎨 style`, `♻️ refactor`, `🧪 test`, `🔧 build`, `🤖 ci`, `📦 chore` | **NONE** | Non-releasable |

**Priority:** MAJOR > MINOR > PATCH > NONE

When multiple commits exist, the highest priority bump is used.

## Scripts Reference

### `analyze_commits.py`

Analyzes git commits since last release and determines version bump.

**Usage:**
```bash
./scripts/analyze_commits.py [OPTIONS]
```

**Options:**
- `--current-version VERSION` - Specify current version (default: last git tag or 0.0.0)
- `--format {bump-type|new-version|json}` - Output format (default: bump-type)
- `--verbose` - Show detailed analysis

**Examples:**
```bash
# Get bump type
./scripts/analyze_commits.py --format bump-type
# Output: major, minor, patch, or none

# Get new version
./scripts/analyze_commits.py --format new-version
# Output: 1.2.3

# Get full JSON analysis
./scripts/analyze_commits.py --format json
# Output: {"current_version": "1.2.2", "bump_type": "minor", "new_version": "1.3.0", ...}

# Verbose mode shows commit analysis
./scripts/analyze_commits.py --verbose
```

**Use this script when:**
- User asks "What would the next version be?"
- Need to analyze commits before executing release
- Debugging commit parsing issues

### `bump_version.py`

Updates version field in Cargo.toml file(s).

**Usage:**
```bash
./scripts/bump_version.py NEW_VERSION [OPTIONS]
```

**Options:**
- `--root PATH` - Project root directory (default: current directory)
- `--dry-run` - Preview changes without modifying files
- `--workspace-deps` - Also update workspace dependency version references
- `--verbose` - Show detailed output

**Examples:**
```bash
# Update version to 1.2.3
./scripts/bump_version.py 1.2.3

# Dry-run to preview
./scripts/bump_version.py 1.2.3 --dry-run

# Update workspace dependencies too
./scripts/bump_version.py 1.2.3 --workspace-deps

# Specify project root
./scripts/bump_version.py 1.2.3 --root /path/to/project
```

**Use this script when:**
- Manually updating versions without full release workflow
- Need to update only version without commit/tag/changelog
- Testing version update logic

### `bump_release.sh`

Main orchestration script that executes complete release workflow.

**Usage:**
```bash
./scripts/bump_release.sh [OPTIONS]
```

**Options:**
- `-d, --dry-run` - Preview without making changes
- `-s, --skip-checks` - Skip pre-release checks (dirty tree, branch)
- `-n, --no-push` - Local release only (don't push or create GitHub release)
- `-p, --prerelease` - Mark as pre-release on GitHub
- `-b, --branch BRANCH` - Specify main branch (default: main)
- `-c, --changelog FILE` - Specify changelog file (default: CHANGELOG.md)
- `-h, --help` - Show help message

**Examples:**
```bash
# Standard release
./scripts/bump_release.sh

# Preview what would happen
./scripts/bump_release.sh --dry-run

# Create pre-release
./scripts/bump_release.sh --prerelease

# Release from develop branch
./scripts/bump_release.sh --branch develop

# Prepare locally without pushing
./scripts/bump_release.sh --no-push

# Skip checks (useful in CI)
./scripts/bump_release.sh --skip-checks
```

**Use this script:**
- For all standard release workflows
- This is the primary script users should run

## Troubleshooting

### Error: No releasable commits found

**Cause:** All commits since last release are non-releasable types (docs, style, refactor, test, build, ci, chore).

**Solution:**
- Check commits with: `git log $(git describe --tags --abbrev=0)..HEAD --oneline`
- Verify commit messages follow Conventional Emoji Commits format
- Need at least one: `feat`, `fix`, `perf`, or `BREAKING CHANGE`

### Error: Working tree is dirty

**Cause:** Uncommitted changes in working directory.

**Solution:**
```bash
# Check status
git status

# Commit or stash changes
git add .
git commit -m "🔧 build: prepare for release"

# Or stash
git stash
```

### Error: Not on main branch

**Cause:** Currently on a different branch.

**Solution:**
```bash
# Switch to main
git checkout main
git pull

# Or specify different branch
./scripts/bump_release.sh --branch develop
```

### Error: git-cliff not found

**Cause:** git-cliff is not installed.

**Solution:**
```bash
cargo install git-cliff
```

### Error: gh not authenticated

**Cause:** GitHub CLI is not authenticated.

**Solution:**
```bash
gh auth login
```

### Error: Cargo validation failed

**Cause:** Cargo.toml changes caused compilation errors.

**Solution:**
- Check `cargo check` output for errors
- Fix Cargo.toml syntax or dependency issues
- Ensure version format is valid (X.Y.Z)

### Error: Failed to push to remote

**Cause:** No permission or network issues.

**Solution:**
```bash
# Check remote
git remote -v

# Try manual push
git push
git push origin v1.2.3

# Check GitHub permissions
gh auth status
```

### Version didn't change

**Cause:** No version bump needed (all commits are non-releasable).

**Solution:**
- This is expected behavior
- Check commits with `--dry-run` to see analysis
- Add feature or fix commits if a release is needed

## Advanced Usage

### Custom Changelog Configuration

Create `.cliff.toml` or `cliff.toml` at project root to customize changelog formatting.

**Example configuration:**
```toml
[changelog]
header = "# Changelog\n\n"
body = """
{% for group, commits in commits | group_by(attribute="group") %}
### {{ group | upper_first }}
{% for commit in commits %}
- {{ commit.message | split(pat="\n") | first | trim }}\
{% if commit.github.pr_number %} ([#{{ commit.github.pr_number }}]({{ commit.github.pr_url }})){% endif %}\
{% if commit.breaking %} **BREAKING**{% endif %}
{% endfor %}
{% endfor %}
"""

[git]
conventional_commits = true
filter_unconventional = true
commit_parsers = [
  { message = "^feat", group = "Features" },
  { message = "^fix", group = "Bug Fixes" },
  { message = "^perf", group = "Performance" },
  { message = "^doc", group = "Documentation" },
  { message = "^refactor", group = "Refactoring" },
  { message = "^test", group = "Testing" },
  { message = "^build", group = "Build" },
  { message = ".*: add", group = "Features" },
  { message = ".*: support", group = "Features" },
  { message = ".*: remove", group = "Removal" },
  { body = ".*BREAKING[- ]CHANGE.*", group = "BREAKING CHANGES" },
]
```

### CI/CD Integration

Execute releases automatically on push to main:

**GitHub Actions example:**
```yaml
name: Release
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Fetch all history for tags

      - name: Install git-cliff
        run: cargo install git-cliff

      - name: Fetch skill
        run: |
          # Download skill from repository or artifact

      - name: Execute release
        run: |
          cd skill-directory
          ./scripts/bump_release.sh --skip-checks
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Manual Version Override

Override automatic version determination:

```bash
# 1. Manually set version
./scripts/bump_version.py 2.0.0

# 2. Validate
cargo check

# 3. Generate changelog for specific version
git-cliff --tag v2.0.0 > CHANGELOG_ENTRY.md

# 4. Update CHANGELOG.md manually

# 5. Create commit and tag
git add Cargo.toml Cargo.lock CHANGELOG.md
git commit -m "🔖 release: bump version to v2.0.0"
git tag -a v2.0.0 -m "Release v2.0.0"

# 6. Push
git push && git push origin v2.0.0

# 7. Create GitHub release
gh release create v2.0.0 --notes-file CHANGELOG_ENTRY.md
```

### Monorepo / Workspace Handling

For Rust workspaces with multiple crates:

**Single versioning (recommended):**
- Keep all workspace members at the same version
- `bump_version.py` updates all Cargo.toml files
- Use `--workspace-deps` flag to update dependency references

**Independent versioning:**
- Release each crate separately
- Specify `--root` to target specific crate directory
- Manage tags with prefixes (e.g., `sdk-v1.0.0`, `cli-v1.0.0`)

## Error Recovery

### Undo Last Release (Before Push)

If release was created locally but not pushed:

```bash
# Delete tag
git tag -d v1.2.3

# Reset to before release commit
git reset --hard HEAD~1

# Changes are undone
```

### Undo Last Release (After Push)

If release was pushed to GitHub:

```bash
# 1. Delete GitHub release
gh release delete v1.2.3 --yes

# 2. Delete remote tag
git push origin :refs/tags/v1.2.3

# 3. Delete local tag
git tag -d v1.2.3

# 4. Revert release commit
git revert HEAD
git push

# 5. Fix issues and create new release
```

### Fix Changelog After Release

If changelog needs corrections after release:

```bash
# 1. Edit CHANGELOG.md manually

# 2. Amend release commit (if not pushed yet)
git add CHANGELOG.md
git commit --amend --no-edit

# 3. Or create new commit (if already pushed)
git add CHANGELOG.md
git commit -m "📚 docs: fix changelog formatting"
git push

# 4. Update GitHub release notes
gh release edit v1.2.3 --notes "$(git-cliff --latest)"
```

## Best Practices

### Before Each Release

1. **Review commits:**
   ```bash
   git log $(git describe --tags --abbrev=0)..HEAD --oneline
   ```

2. **Run dry-run first:**
   ```bash
   ./scripts/bump_release.sh --dry-run
   ```

3. **Verify tests pass:**
   ```bash
   cargo test --workspace
   ```

4. **Check for uncommitted changes:**
   ```bash
   git status
   ```

### Commit Message Quality

- Write clear, descriptive commit messages
- Follow Conventional Emoji Commits format strictly
- Include scope when helpful: `feat(auth):` vs `feat:`
- Document breaking changes thoroughly in commit body
- Reference issue numbers: `Fixes #42`

### Changelog Maintenance

- Review generated changelog before finalizing
- Add migration guides for breaking changes
- Include links to documentation
- Credit contributors when appropriate

### Version Strategy

- Use MAJOR for breaking changes (strict)
- Use MINOR for new features
- Use PATCH for bug fixes and performance
- Use prerelease suffixes for betas: `1.0.0-beta.1`
- Never skip versions or go backwards

## Summary

This skill automates the entire Rust project release workflow using Conventional Emoji Commits for version determination. Execute the main script (`bump_release.sh`) to automatically analyze commits, bump versions, generate changelogs, and create GitHub releases. Use `--dry-run` to preview changes, and individual scripts for specialized tasks. Ensure all prerequisites are met and follow best practices for smooth releases.

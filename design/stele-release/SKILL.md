---
name: stele-release
description: Automate version bumping and release preparation for the stele CLI project. Use this skill when the user requests to create a new release, bump the version, or prepare release tags for stele. The skill analyzes conventional commits to suggest appropriate semantic version bumps and guides through the complete release workflow.
---

# Stele Release

## Overview

Automate the release process for the stele CLI, a static site generator. This skill handles version analysis, tag creation, and release workflow guidance based on conventional commits and semantic versioning principles.

## When to Use This Skill

Use this skill when the user requests:
- "Create a new release for stele"
- "Bump the version"
- "Prepare a release"
- "What version should I release next?"
- "Tag a new version"

## Release Workflow

Follow these steps in order to prepare and execute a release:

### Step 1: Analyze Commits and Determine Version

Run the version analysis script to examine commits since the last tag:

**IMPORTANT:** `python` is not available on this machine; make sure to use `python3` when invoking scripts.

```bash
cd /Users/ryan/dev/haleyrc/stele
python3 .claude/skills/stele-release/scripts/analyze_version.py
```

The script will:
- Identify the current version from git tags
- Analyze commits using conventional commit patterns
- Detect breaking changes (BREAKING CHANGE, !)
- Identify new features (feat:)
- Identify bug fixes (fix:)
- Suggest the appropriate semantic version bump (major/minor/patch)

Present the analysis results to the user and ask if they want to proceed with the suggested version or choose a different one.

### Step 2: Ensure Branch is Synced with Remote

**CRITICAL:** Before creating a tag, verify that all local commits are pushed to the remote repository. Tags should only point to commits that exist on the remote.

```bash
cd /Users/ryan/dev/haleyrc/stele
git status
```

Check the output for "Your branch is ahead of 'origin/main' by X commit(s)". If the branch is ahead:

1. Show the commits that are ahead:
```bash
git log origin/main..HEAD --oneline
```

2. Push the local commits to origin:
```bash
git push
```

If the branch is behind or diverged from origin, inform the user and ask how they want to proceed before continuing.

### Step 3: Verify Pre-Release Checks

Before creating a tag, ensure the codebase is ready:

```bash
cd /Users/ryan/dev/haleyrc/stele
go test ./...
./bin/check
```

Both commands must pass successfully. If they fail, inform the user and ask if they want to fix the issues before proceeding.

### Step 4: Create and Push the Version Tag

Once the branch is synced, version is confirmed, and checks pass, create an annotated git tag:

```bash
cd /Users/ryan/dev/haleyrc/stele
git tag -a v{VERSION} -m "Release v{VERSION}"
git push origin v{VERSION}
```

Replace `{VERSION}` with the actual version number (e.g., `1.0.0`, `1.0.0-beta.4`).

### Step 5: Monitor the Release Workflow

After pushing the tag, the GitHub Actions release workflow will automatically:
1. Run tests via the reusable workflow
2. Check out the code with full history
3. Set up Go environment
4. Execute GoReleaser to build binaries
5. Generate changelog from conventional commits
6. Create a GitHub release
7. Upload darwin/arm64 binaries as artifacts

Inform the user to:
- Visit https://github.com/haleyrc/stele/actions
- Monitor the "Release" workflow
- Verify completion and check for any errors

### Step 6: Verify the Release

Once the workflow completes, guide the user to verify:

1. Check the release page: https://github.com/haleyrc/stele/releases
2. Verify the changelog is correctly generated
3. Confirm the binary artifact is present
4. Optionally, download and test the binary:

```bash
gh release download v{VERSION} -R haleyrc/stele
tar -xzf stele_Darwin_arm64.tar.gz
./stele version
```

## Version Types

### Stable Releases

For production-ready versions:
- Format: `v1.0.0`, `v2.0.0`, `v1.1.0`, `v1.0.1`
- Automatically marked as latest release on GitHub
- Follow semantic versioning strictly

### Pre-Release Versions

For beta, alpha, or release candidate versions:
- Format: `v1.0.0-beta.1`, `v2.0.0-alpha.1`, `v1.0.0-rc.1`
- Automatically marked as pre-release by GoReleaser (configured with prerelease: auto)
- Useful for testing before stable release

## Semantic Versioning Guidelines

The version analysis script follows these rules:

- **MAJOR** (v2.0.0): Breaking changes, incompatible API changes
  - Detected by: commits with BREAKING CHANGE in body or ! after type
- **MINOR** (v1.1.0): New features, backwards compatible
  - Detected by: commits starting with feat: or feat(
- **PATCH** (v1.0.1): Bug fixes, backwards compatible
  - Detected by: commits starting with fix: or fix(

## Commit Convention Reference

The project follows Conventional Commits:
- feat: - New features (triggers minor bump)
- fix: - Bug fixes (triggers patch bump)
- refactor:, perf:, style: - Other changes (appear in "Other Changes" in changelog)
- docs:, test:, chore: - Excluded from changelog

For detailed commit conventions, refer to references/contributing.md.

## Rollback Procedures

### If Release Workflow Fails

If the GitHub Actions workflow fails after pushing the tag:

```bash
# Delete remote tag
git push --delete origin v{VERSION}

# Delete local tag
git tag -d v{VERSION}

# Fix the issue, then recreate and push the tag
```

### If Release Succeeds but Has Issues

Never delete a published release (users may have already downloaded it):

1. Fix the issue in the codebase
2. Create a new patch version (e.g., v1.0.1 if v1.0.0 had issues)
3. Optionally edit the old release notes to point to the fixed version

## GoReleaser Configuration Reference

The .goreleaser.yaml file configures:
- **Target**: darwin/arm64 (macOS Apple Silicon)
- **CGO**: Enabled (required for some dependencies)
- **UPX**: Compression enabled for smaller binaries
- **Pre-build hook**: ./bin/check runs automatically
- **Changelog**: Grouped by Features, Bug Fixes, Other Changes
- **Ldflags**: Version injection (main.version, main.commit, main.date)

## Resources

### scripts/analyze_version.py
Python script that analyzes git commits and suggests the next semantic version based on conventional commit patterns. Execute this script at the start of every release workflow.

### references/contributing.md
Complete reference documentation copied from the stele project's CONTRIBUTING.md file. Contains detailed information about commit conventions, release process, and rollback procedures. Load this if the user needs more details about commit message format or the release workflow.

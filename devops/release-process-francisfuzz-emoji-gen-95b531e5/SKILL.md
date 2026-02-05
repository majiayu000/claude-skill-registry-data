---
name: release-process
description: Guide the release process for emoji_gen including version bumping, tagging, and automated CI deployment. Use when releasing a new version, the user mentions "release", "version bump", "publish", or "tag a release".
allowed-tools: Bash, Read, Edit
---

# Release Process for emoji_gen

This Skill guides the complete release process for emoji_gen, which uses automated GitHub Actions for building and publishing.

## Overview

Releases are fully automated via GitHub Actions. When you push a version tag, CI automatically:
- Builds binaries for Linux (x86_64, ARM64), macOS (Intel, Apple Silicon), Windows (x86_64)
- Publishes multi-platform Docker images to `ghcr.io/francisfuzz/emoji_gen`
- Creates GitHub Release with all artifacts and checksums
- Tags Docker images with version and `latest`

## Semantic Versioning

Follow [Semantic Versioning](https://semver.org/):

| Version Type | When to Use | Example |
|-------------|-------------|---------|
| **MAJOR** (X.0.0) | Breaking changes | 1.0.0 → 2.0.0 |
| **MINOR** (0.X.0) | New features, backwards compatible | 0.1.0 → 0.2.0 |
| **PATCH** (0.0.X) | Bug fixes, backwards compatible | 0.1.0 → 0.1.1 |

**Breaking changes indicators:**
- Commits with `!` after type: `feat!:`, `fix!:`
- Commits with `BREAKING CHANGE:` footer
- Changes that require user code updates

## Release Steps

### 1. Determine Version Number

**Review recent commits to decide version bump:**

```bash
# See commits since last release
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# Or see all commits with details
git log $(git describe --tags --abbrev=0)..HEAD
```

**Decision tree:**
- Has `BREAKING CHANGE:` or `!` → MAJOR bump
- Has `feat:` commits → MINOR bump
- Only `fix:`, `docs:`, `build:`, etc. → PATCH bump

### 2. Update Version in Cargo.toml

**Edit Cargo.toml:**

```bash
# Current version
grep '^version = ' Cargo.toml

# Edit the version field
# Change: version = "0.1.0"
# To:     version = "0.2.0"
```

Use the Edit tool to update the version.

### 3. Commit Version Bump

```bash
git add Cargo.toml Cargo.lock
git commit -m "$(cat <<'EOF'
chore: bump version to X.Y.Z

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### 4. Create and Push Tag

```bash
# Create annotated tag
git tag -a vX.Y.Z -m "Release vX.Y.Z"

# Push commit and tag
git push origin main
git push origin vX.Y.Z
```

**The tag push triggers the release workflow automatically.**

### 5. Monitor Release

```bash
# Watch GitHub Actions
gh run watch

# Or view in browser
gh run view --web

# Check release when complete
gh release view vX.Y.Z
```

### 6. Verify Release Artifacts

Once CI completes, verify:

**GitHub Release:**
- [ ] All platform binaries present (Linux x86_64, ARM64, macOS x86_64, ARM64, Windows x86_64)
- [ ] SHA256 checksums for each binary
- [ ] Release notes generated

**Docker Registry:**
- [ ] `ghcr.io/francisfuzz/emoji_gen:vX.Y.Z` tag exists
- [ ] `ghcr.io/francisfuzz/emoji_gen:latest` updated (if not a prerelease)
- [ ] Multi-platform support (linux/amd64, linux/arm64)

```bash
# Check Docker tags
gh api repos/francisfuzz/emoji_gen/packages

# Or via docker
docker pull ghcr.io/francisfuzz/emoji_gen:vX.Y.Z
docker run --rm ghcr.io/francisfuzz/emoji_gen:vX.Y.Z --version
```

## Complete Release Example

```bash
# 1. Check what changed
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# 2. Decide version (example: 0.1.0 → 0.2.0 for new feature)
# Edit Cargo.toml version field
# From: version = "0.1.0"
# To:   version = "0.2.0"

# 3. Commit version bump
git add Cargo.toml Cargo.lock
git commit -m "$(cat <<'EOF'
chore: bump version to 0.2.0

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# 4. Create and push tag
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin main
git push origin v0.2.0

# 5. Monitor release
gh run watch

# 6. Verify when complete
gh release view v0.2.0
docker pull ghcr.io/francisfuzz/emoji_gen:v0.2.0
```

## Pre-release Versions

For alpha, beta, or release candidates:

```bash
# Version format: 0.2.0-beta.1
git tag -a v0.2.0-beta.1 -m "Release v0.2.0-beta.1"
git push origin v0.2.0-beta.1
```

Pre-releases:
- Marked as prerelease in GitHub
- Don't update the `latest` Docker tag
- Useful for testing before final release

## Troubleshooting

### Release workflow failed
```bash
# View failed run
gh run list --workflow=release.yml --limit 5
gh run view <run-id>

# Common fixes:
# - Check Cargo.toml syntax
# - Verify tag format is vX.Y.Z
# - Ensure tests pass
```

### Docker image not published
```bash
# Check workflow logs
gh run view --log

# Verify GITHUB_TOKEN permissions in workflow
# Check .github/workflows/release.yml permissions section
```

### Wrong version in binaries
```bash
# Delete bad tag locally and remotely
git tag -d vX.Y.Z
git push origin :refs/tags/vX.Y.Z

# Delete GitHub release
gh release delete vX.Y.Z

# Fix Cargo.toml and recreate tag
```

## Post-Release (Optional)

### Publish to crates.io

**Manual step** (not automated):

```bash
# Ensure you're on the tagged version
git checkout vX.Y.Z

# Publish to crates.io
cargo publish

# Return to main
git checkout main
```

### Announce Release

- Update project README with latest version if needed
- Announce in project discussions or relevant channels
- Update documentation site if applicable

## Distribution Channels

After release, artifacts are available via:

1. **GitHub Releases**: https://github.com/francisfuzz/emoji_gen/releases
   - Pre-compiled binaries for all platforms
   - SHA256 checksums

2. **GitHub Container Registry**:
   - `ghcr.io/francisfuzz/emoji_gen:vX.Y.Z`
   - `ghcr.io/francisfuzz/emoji_gen:latest`

3. **crates.io** (manual):
   - `cargo install emoji_gen`

## Checklist

Before releasing:
- [ ] All tests pass locally: `./docker-dev.sh test`
- [ ] Clippy passes: `./docker-dev.sh clippy`
- [ ] Version number follows semver
- [ ] Cargo.toml version updated
- [ ] On main branch
- [ ] All changes committed and pushed
- [ ] Tag format is `vX.Y.Z` (with v prefix)

After releasing:
- [ ] GitHub Actions workflow succeeded
- [ ] All binaries present in GitHub Release
- [ ] Docker images published to GHCR
- [ ] Release notes look correct
- [ ] Test at least one binary/Docker image

## Quick Reference

```bash
# See current version
grep '^version = ' Cargo.toml

# See latest tag
git describe --tags --abbrev=0

# List all tags
git tag -l

# See commits since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# Create release
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin main && git push origin vX.Y.Z

# Monitor release
gh run watch

# View release
gh release view vX.Y.Z
```

---
name: releasing-versions
description: Interactive release workflow for OSS Sustain Guard with version updates, PyPI publishing, and GitHub release notes. Use when ready to release a new version to production.
---

# Release Process - Quick Start

> **Quick guide to release a new version. For detailed info, see [workflow-details.md](../references/workflow-details.md).**

## Quick Release Checklist

```bash
# 1. Verify local setup
make test && make lint && make doc-build

# 2. Analyze changes & update version
# - Run: git log --oneline to see actual changes
# - Edit pyproject.toml: change version
# - Run: uv sync
# - Edit CHANGELOG.md: add new section based on actual changes

# 3. Commit and tag
git add pyproject.toml uv.lock CHANGELOG.md
git commit -m "chore: release version X.Y.Z"
git tag vX.Y.Z
git push origin vX.Y.Z

# 4. Watch pipeline
# → Go to: https://github.com/onukura/oss-sustain-guard/actions
# → Wait for all jobs to succeed

# 5. Prepare English release notes
# → Claude will generate English release notes based on CHANGELOG
# → Copy to GitHub Releases description
```

## The 5 Steps

### 1️⃣ Prepare & Test

Make sure everything is ready:

```bash
git fetch upstream
make test          # All tests pass?
make lint          # Code clean?
make doc-build     # Docs build?
```

### 2️⃣ Decide Version

Use [Semantic Versioning](https://semver.org/):
- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.15.0): New features
- **PATCH** (0.14.1): Bug fixes

### 3️⃣ Update Files

**Step 1: Analyze actual changes**

View what changed since last version:

```bash
git log --oneline --since="2 weeks ago"
# Or compare with last tag:
git log --oneline v0.14.0..HEAD
```

**pyproject.toml** - Change version:

```toml
version = "0.15.0"
```

**Then sync lock file:**

```bash
uv sync
```

**CHANGELOG.md** - Add at top based on actual changes:

```markdown
## v0.15.0 - 2026-01-20

### Added
- New metric for repository visibility
- Support for Dart package resolver

### Fixed
- Bug in cache invalidation logic
- Memory leak in GraphQL client

### Improved
- Performance optimization in dependency analysis
- Better error messages for network timeouts
```

> **Important:** Write CHANGELOG entries based on the actual `git log` output from your recent commits, not generic templates.

### 4️⃣ Commit & Tag

```bash
git add pyproject.toml uv.lock CHANGELOG.md
git commit -m "chore: release version 0.15.0"
git tag v0.15.0
git push origin v0.15.0
```

### 5️⃣ Watch & Verify

The publish workflow starts automatically:

```
GitHub Actions → build → publish-to-pypi → github-release
```

**Check:**

- [ ] All jobs pass in Actions
- [ ] New version on PyPI
- [ ] Release appears on GitHub Releases
- [ ] Can install: `pip install oss-sustain-guard==0.15.0`

### 6️⃣ Generate & Publish English Release Notes ⭐ **REQUIRED**

After verifying the release on PyPI and GitHub, Claude will:

1. **Read your CHANGELOG.md** to understand actual changes
2. **Generate professional English release notes** with:
   - Executive summary of the release
   - Feature highlights with descriptions
   - Bug fixes and improvements
   - Migration notes (if breaking changes)
   - Contributor appreciation
3. **Provide formatted text** ready to copy/paste to GitHub Releases

**You will:**
- Copy the generated English release notes to GitHub Releases description
- Update any version-specific links or instructions if needed

This ensures your release has comprehensive documentation for all users.

## What Happens Automatically

✅ Build Python package
✅ Upload to PyPI (Trusted Publishing)
✅ Sign artifacts with Sigstore
✅ Create GitHub Release
✅ **Claude generates English release notes** (based on CHANGELOG.md)

## GitHub Release Notes Template

🎯 **After PyPI release completes**, you'll receive:

1. **English release notes** based on your CHANGELOG.md
2. **Ready-to-copy formatting** for GitHub Releases
3. **Professional structure** with sections for features, fixes, improvements

> Claude will automatically generate and present these - no need to ask!

## Need More Details?

See bundled references:

- [workflow-details.md](../references/workflow-details.md) - Detailed technical info
- [release-examples.md](../examples/release-examples.md) - Step-by-step examples & troubleshooting

## Common Questions

**Q: How do I write good CHANGELOG entries?**
A: Review your actual commits with `git log --oneline` and group them by type (Added, Fixed, Improved). Use clear, user-focused language.

**Q: What if tests fail?**
A: Fix the issue and commit before running the release commands.

**Q: How to undo a release?**
A: Delete the tag (`git tag -d vX.Y.Z && git push origin :vX.Y.Z`) before PyPI publishes.

**Q: Tag created but pipeline didn't start?**
A: Verify tag format is `vX.Y.Z` (must start with 'v'). See troubleshooting docs.

**Q: Do I need to ask Claude for release notes?**
A: No! Claude will automatically generate English release notes after you verify the PyPI release. Just ask "Create release notes" when ready.

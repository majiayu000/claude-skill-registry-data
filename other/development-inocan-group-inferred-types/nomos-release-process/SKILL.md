---
name: nomos-release-process
description: Automates release workflows for the Nomos monorepo per RELEASE.md including version tagging, changelog promotion, GitHub releases, and module-specific versioning. Use this when preparing releases, creating tags, or publishing new versions.
---

# Nomos Release Process

This skill automates release workflows for the Nomos monorepo, handling version tagging, changelog updates, and GitHub releases for independent modules.

## When to Use This Skill

- Preparing to release a new version of a Nomos module
- Creating version tags for libs or apps
- Promoting Unreleased changelog entries to versioned sections
- Publishing GitHub Releases
- Troubleshooting release issues
- Verifying release readiness

## Nomos Versioning Strategy

Nomos is a **monorepo with independent module versioning**:

### Module Types

**Libraries (libs/):**
- `libs/compiler` - Tag: `libs/compiler/v0.x.x`
- `libs/parser` - Tag: `libs/parser/v0.x.x`
- `libs/provider-downloader` - Tag: `libs/provider-downloader/v0.x.x`
- `libs/provider-proto` - Tag: `libs/provider-proto/v0.x.x`

**Applications (apps/):**
- `apps/command-line` - Tag: `apps/command-line/v1.x.x`

### Versioning Philosophy

- **v0.x.x (pre-1.0)**: API unstable, breaking changes allowed in MINOR versions
- **v1.x.x (stable)**: Breaking changes require MAJOR version bump
- Each module versions independently
- Follow Semantic Versioning (https://semver.org/)

## Release Workflow

### Step 1: Pre-Release Verification

Before starting, verify readiness:

```bash
# 1. Checkout main and sync
git checkout main
git pull origin main

# 2. Run full test suite
make test-all
make test-race

# 3. Verify linting
make lint

# 4. Check for replace directives (should be removed)
grep "replace " libs/compiler/go.mod
grep "replace " libs/parser/go.mod
# If found, see docs/guides/removing-replace-directives.md

# 5. Verify CI is green
# Check: https://github.com/autonomous-bits/nomos/actions
```

### Step 2: Determine Version Bump

**SemVer rules:**

**Pre-1.0 modules (v0.x.x):**
- **MINOR (0.X.0)** - Breaking changes OK (API unstable)
- **PATCH (0.0.X)** - Bug fixes, performance, non-breaking features

**Stable modules (v1.x.x):**
- **MAJOR (X.0.0)** - Breaking changes (API incompatibility)
- **MINOR (0.X.0)** - New features (backward-compatible)
- **PATCH (0.0.X)** - Bug fixes (backward-compatible)

**Check Unreleased section:**
```bash
# Look for breaking changes
grep "BREAKING:" libs/compiler/CHANGELOG.md

# If found in pre-1.0: MINOR bump (0.X.0)
# If found in v1.x.x: MAJOR bump (X.0.0)
```

**Examples:**
- `libs/compiler` currently at `v0.2.1` with breaking changes → `v0.3.0`
- `apps/command-line` currently at `v1.2.0` with new feature → `v1.3.0`
- `libs/parser` currently at `v0.1.5` with bug fix → `v0.1.6`

### Step 3: Update CHANGELOG.md

Move Unreleased entries to new version section:

**Before:**
```markdown
## [Unreleased]

### Added
- [Compiler] Add provider caching (#152)

### Fixed
- [Compiler] Fix reference resolution bug (#160)

## [0.2.1] - 2025-11-15
```

**After:**
```markdown
## [Unreleased]

## [0.3.0] - 2025-12-29

### Added
- [Compiler] Add provider caching (#152)

### Fixed
- [Compiler] Fix reference resolution bug (#160)

## [0.2.1] - 2025-11-15
```

**Update compare links at bottom:**
```markdown
[Unreleased]: https://github.com/autonomous-bits/nomos/compare/libs/compiler/v0.3.0...HEAD
[0.3.0]: https://github.com/autonomous-bits/nomos/compare/libs/compiler/v0.2.1...libs/compiler/v0.3.0
[0.2.1]: https://github.com/autonomous-bits/nomos/compare/libs/compiler/v0.2.0...libs/compiler/v0.2.1
```

**Commit changelog:**
```bash
git add libs/compiler/CHANGELOG.md
git commit -m "📝 docs(compiler): prepare v0.3.0 release"
git push origin main
```

### Step 4: Create Annotated Tag

**Format:** `libs/<module>/v<MAJOR>.<MINOR>.<PATCH>`

**Use annotated tags** (include metadata):

```bash
# Basic annotated tag
git tag -a libs/compiler/v0.3.0 -m "libs/compiler v0.3.0"

# With detailed release notes
git tag -a libs/compiler/v0.3.0 -m "libs/compiler v0.3.0

Release highlights:
- Added provider caching for deterministic builds
- Fixed reference resolution for nested paths
- Performance improvements (~30% faster compilation)

See CHANGELOG.md for full details."
```

**For CLI:**
```bash
git tag -a apps/command-line/v1.3.0 -m "apps/command-line v1.3.0"
```

### Step 5: Push Tag to GitHub

```bash
# Push specific tag
git push origin libs/compiler/v0.3.0

# Or push all tags (use carefully)
git push origin --tags
```

### Step 6: Verify Tag Exists

```bash
# Check locally
git tag -l "libs/compiler/*"

# Check remotely
git ls-remote --tags origin | grep libs/compiler

# View on GitHub
# https://github.com/autonomous-bits/nomos/tags
```

### Step 7: Create GitHub Release (Recommended)

**Via GitHub UI:**

1. Go to https://github.com/autonomous-bits/nomos/releases/new
2. **Choose tag:** Select `libs/compiler/v0.3.0`
3. **Release title:** `libs/compiler v0.3.0`
4. **Description:** Copy from CHANGELOG.md:
   ```markdown
   ## Added
   - Add provider caching for deterministic builds (#152)
   
   ## Fixed
   - Fix reference resolution for nested paths (#160)
   ```
5. **Pre-release:** Check if version is v0.x.x
6. **Publish release**

**Via GitHub CLI:**

```bash
gh release create libs/compiler/v0.3.0 \
    --title "libs/compiler v0.3.0" \
    --notes-file libs/compiler/CHANGELOG.md \
    --prerelease  # For v0.x.x versions
```

## Common Release Scenarios

### Scenario 1: Release Compiler Library v0.3.0

**Given:**
- Current version: v0.2.1
- Unreleased has: 2 Added, 1 Fixed
- No breaking changes (but pre-1.0 allows breaking in MINOR)

**Steps:**
```bash
# 1. Verify
git checkout main && git pull
make test-all && make test-race

# 2. Update CHANGELOG
# Move Unreleased → [0.3.0] - 2025-12-29
# Update compare links

# 3. Commit
git add libs/compiler/CHANGELOG.md
git commit -m "📝 docs(compiler): prepare v0.3.0 release"
git push origin main

# 4. Tag
git tag -a libs/compiler/v0.3.0 -m "libs/compiler v0.3.0"
git push origin libs/compiler/v0.3.0

# 5. Create GitHub Release
gh release create libs/compiler/v0.3.0 \
    --title "libs/compiler v0.3.0" \
    --notes-from-tag \
    --prerelease
```

### Scenario 2: Release CLI v1.3.0

**Given:**
- Current version: v1.2.0
- New feature: `--allow-missing-provider` flag
- Bug fix: exit code for strict mode

**Steps:**
```bash
# 1. Update CHANGELOG
# Move to [1.3.0] - 2025-12-29 (MINOR bump for new feature)

# 2. Commit
git add apps/command-line/CHANGELOG.md
git commit -m "📝 docs(cli): prepare v1.3.0 release"
git push origin main

# 3. Tag
git tag -a apps/command-line/v1.3.0 -m "apps/command-line v1.3.0"
git push origin apps/command-line/v1.3.0

# 4. GitHub Release (stable, not pre-release)
gh release create apps/command-line/v1.3.0 \
    --title "Nomos CLI v1.3.0" \
    --notes-from-tag
```

### Scenario 3: Bug Fix Release (PATCH)

**Given:**
- Current version: v0.1.5
- Only bug fixes in Unreleased

**Steps:**
```bash
# PATCH bump: v0.1.5 → v0.1.6
# Update CHANGELOG → [0.1.6]
git add libs/parser/CHANGELOG.md
git commit -m "📝 docs(parser): prepare v0.1.6 release"
git push origin main

git tag -a libs/parser/v0.1.6 -m "libs/parser v0.1.6"
git push origin libs/parser/v0.1.6
```

### Scenario 4: Multiple Module Release

**Given:** Need to release both compiler and parser

**Steps:**
```bash
# Release compiler first
# ... follow normal flow for libs/compiler/v0.3.0

# Then release parser
# ... follow normal flow for libs/parser/v0.2.0

# Each module releases independently
# Tags: libs/compiler/v0.3.0, libs/parser/v0.2.0
```

## Consuming Released Modules

Once tags are pushed, users can install:

```bash
# Specific version
go get github.com/autonomous-bits/nomos/libs/compiler@v0.3.0

# Latest version
go get github.com/autonomous-bits/nomos/libs/compiler@latest

# In go.mod
require (
    github.com/autonomous-bits/nomos/libs/compiler v0.3.0
)
```

**List available versions:**
```bash
go list -m -versions github.com/autonomous-bits/nomos/libs/compiler
```

## Troubleshooting

### Issue: Tag Already Exists

**Solution (if just created and not yet used):**
```bash
# Delete local tag
git tag -d libs/compiler/v0.3.0

# Delete remote tag (CAUTION: breaks consumers)
git push origin --delete libs/compiler/v0.3.0

# Create correct tag
git tag -a libs/compiler/v0.3.0 -m "libs/compiler v0.3.0"
git push origin libs/compiler/v0.3.0
```

**Warning:** Never delete published tags that consumers may be using!

### Issue: CI/CD Failure After Tag Push

**Cause:** Tests failing or lint errors

**Solution:**
```bash
# 1. Delete bad tag
git push origin --delete libs/compiler/v0.3.0
git tag -d libs/compiler/v0.3.0

# 2. Fix issues on main
git checkout main
# ... fix issues
make test-all
git commit -m "fix: resolve CI issues"
git push origin main

# 3. Re-tag
git tag -a libs/compiler/v0.3.0 -m "libs/compiler v0.3.0"
git push origin libs/compiler/v0.3.0
```

### Issue: go get Cannot Fetch Module

**Symptoms:**
```bash
go get github.com/autonomous-bits/nomos/libs/compiler@v0.3.0
# Error: unknown revision
```

**Debug:**
```bash
# 1. Verify tag exists remotely
git ls-remote --tags origin | grep libs/compiler/v0.3.0

# 2. Check tag format (must be exact)
# Correct: libs/compiler/v0.3.0
# Wrong: libs/compiler/0.3.0 (missing 'v')
# Wrong: compiler/v0.3.0 (missing 'libs/')

# 3. Wait for Go module proxy
# Can take a few minutes to propagate
# Check: https://proxy.golang.org/github.com/autonomous-bits/nomos/libs/compiler/@v/list
```

### Issue: Replace Directives Block Release

**Symptoms:**
```go
// go.mod contains:
replace github.com/autonomous-bits/nomos/libs/parser => ../parser
```

**Solution:**
```bash
# 1. Remove replace directive
# See: docs/guides/removing-replace-directives.md

# 2. Test without replace
go mod tidy
go test ./...

# 3. Commit
git commit -m "🔧 chore: remove replace directive for release"
git push origin main

# 4. Then proceed with release
```

## Release Checklist Template

Copy this checklist when preparing releases:

```markdown
## Release Checklist: libs/compiler v0.3.0

- [ ] Main branch up-to-date: `git pull origin main`
- [ ] All tests pass: `make test-all`
- [ ] Race detector clean: `make test-race`
- [ ] Linting clean: `make lint`
- [ ] No replace directives: `grep replace go.mod`
- [ ] CI green on GitHub
- [ ] CHANGELOG updated with new version section
- [ ] Compare links updated in CHANGELOG
- [ ] Version bump determined (MAJOR.MINOR.PATCH)
- [ ] Changelog committed: `git commit -m "docs: prepare vX.Y.Z"`
- [ ] Tag created: `git tag -a libs/compiler/vX.Y.Z`
- [ ] Tag pushed: `git push origin libs/compiler/vX.Y.Z`
- [ ] Tag verified: `git ls-remote --tags origin | grep vX.Y.Z`
- [ ] GitHub Release created (UI or gh CLI)
- [ ] Module fetchable: `go get @vX.Y.Z`
```

## Reference Documentation

For complete release guidelines, see:
- [docs/RELEASE.md](../../docs/RELEASE.md)
- [Semantic Versioning](https://semver.org/)
- [Go Modules Reference](https://go.dev/ref/mod)

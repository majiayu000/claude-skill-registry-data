---
name: release-package
description: Create and publish a new version of docent to npm registry
group: docent
author: "@tnez"
version: 1.0.0
keywords: [release, npm, publishing, version]
---

# Runbook: Release Package

**Purpose:** Create and publish a new version of docent to npm registry
**Owner:** Maintainers
**Last Updated:** 2025-10-17
**Frequency:** As needed for releases

## Overview

This runbook covers the complete release process from version bumping through automated npm publishing. The workflow is:

1. **Prepare locally** - Version bump, changelog, validation
2. **Push tagged commit** - Triggers automated publishing
3. **Monitor release** - Watch GitHub Actions complete the publish

**Expected duration:** 20-30 minutes (plus monitoring time)

## Prerequisites

### Required Tools

- `git` command line tool
- `gh` CLI (GitHub CLI) - installed and authenticated
- `npm` - Node.js package manager
- Node.js >= 18.0.0

### Required Access

- Write access to the repository
- Ability to create tags and push to main branch
- npm publish access (configured in GitHub secrets)

### Pre-Flight Checklist

Before starting, ensure:

- [ ] All features for this release are merged to main
- [ ] All CI/CD checks are passing on main branch
- [ ] You are on the main branch: `git checkout main`
- [ ] Working directory is clean: `git status`
- [ ] Local main is up to date: `git pull origin main`
- [ ] Branch is ahead of origin or even (not behind)

---

## Part 1: Preparation (Local)

### Step 1: Pre-Release Health Check

**Purpose:** Validate code quality and documentation before release

**Commands:**

```bash
# Run full test suite
npm test

# Run build to ensure no compilation errors
npm run build

# Check markdown linting
npm run lint:md

# Search for temporary/debug code that shouldn't be released
git grep -n "console\.log\|debugger\|TODO.*remove\|FIXME.*before.*release\|XXX" src/ || echo "✓ No obvious debug code"

# Check for test-only markers (should be removed before release)
git grep -n "\.only\|\.skip" test/ && echo "⚠ Remove .only/.skip from tests" || echo "✓ No test-only markers"

# Verify no uncommitted changes
git status --short

# Check documentation quality (optional but recommended)
# This provides a detailed analysis of docs coverage
npm run docent audit . 2>/dev/null || echo "Note: docent audit available via MCP"
```

**Validation:**

- All tests pass
- Build succeeds without errors
- No obvious debug code in src/
- No `.only` or `.skip` in tests
- Working directory is clean
- Markdown linting passes (or known issues documented)

**If step fails:**

- Fix test failures before proceeding
- Remove debug code and test markers
- Commit any fixes: `git add . && git commit -m "chore: pre-release cleanup"`
- Document markdown lint issues if non-blocking (see runbook: fix-markdown-lint)

---

### Step 2: Determine Version Number

**Purpose:** Decide what version number to use based on changes

**Semantic Versioning Rules:**

- **Major (X.0.0)**: Breaking changes, incompatible API changes
- **Minor (0.X.0)**: New features, backwards-compatible
- **Patch (0.0.X)**: Bug fixes, backwards-compatible

**Commands:**

```bash
# Check current version
npm pkg get version

# Review commits since last release
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
if [ -n "$LAST_TAG" ]; then
  echo "Commits since $LAST_TAG:"
  git log $LAST_TAG..HEAD --oneline --no-decorate

  # Check what changed in public API
  echo -e "\nAPI changes:"
  git diff $LAST_TAG -- src/mcp/ --stat
else
  echo "No previous tags found - this is the first release"
  git log --oneline --no-decorate
fi

# Check CHANGELOG for any BREAKING markers
git grep "BREAKING:" CHANGELOG.md && echo "⚠ Breaking changes found in CHANGELOG"
```

**Validation:**

- Current version is identified
- Changes are categorized (breaking, feature, fix)
- New version number determined following semver
- Breaking changes are identified

**Decision Point:**

Choose version bump type:

- `patch` - Bug fixes only (0.5.0 → 0.5.1)
- `minor` - New features, no breaking changes (0.5.0 → 0.6.0)
- `major` - Breaking changes (0.5.0 → 1.0.0)

**If step fails:**

- No tags exist yet: start with 0.1.0 or 1.0.0
- Can't determine changes: review commit history manually

---

### Step 3: Update Version Number

**Purpose:** Bump version in package.json

**Commands:**

```bash
# Choose ONE based on Step 2 decision:

# For patch release (0.5.0 → 0.5.1)
npm version patch --no-git-tag-version

# For minor release (0.5.0 → 0.6.0)
npm version minor --no-git-tag-version

# For major release (0.5.0 → 1.0.0)
npm version major --no-git-tag-version

# Or set specific version
npm version 0.6.0 --no-git-tag-version

# Capture new version for later steps
NEW_VERSION=$(npm pkg get version | tr -d '"')
echo "New version: $NEW_VERSION"
```

**Validation:**

- `package.json` shows new version number
- `package-lock.json` also updated with new version (2 places)
- Files are modified but not committed yet
- Verify: `npm pkg get version`
- Verify: `git status` shows both package.json and package-lock.json modified

**If step fails:**

- Working directory must be clean (commit or stash changes)
- Manually edit package.json if npm version fails

---

### Step 4: Update CHANGELOG.md

**Purpose:** Document changes in this release for users

**Commands:**

```bash
# Open CHANGELOG.md in editor
$EDITOR CHANGELOG.md

# Review commits for this release (if needed)
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
[ -n "$LAST_TAG" ] && git log $LAST_TAG..HEAD --oneline
```

**Required CHANGELOG Structure:**

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Breaking Changes (if any)

- **BREAKING**: Clear description of breaking change
- Migration guide: how to update code

### Added

- New features and capabilities
- User-facing improvements

### Changed

- Changes to existing functionality
- Behavior modifications

### Fixed

- Bug fixes and corrections

### Technical

- Internal improvements, refactoring
- Dependency updates
- Development tooling changes
```

**Validation:**

- New version section added at top of CHANGELOG
- Date set to today (YYYY-MM-DD format)
- Changes categorized appropriately
- Each change describes user-facing value (not just commit messages)
- Breaking changes clearly marked with **BREAKING:** prefix
- Breaking changes include migration guidance
- Follows [Keep a Changelog](https://keepachangelog.com/) format

**If step fails:**

- Review recent commits: `git log --oneline --since="2 weeks ago"`
- Check closed issues: `gh issue list --state closed --limit 20`
- Check merged PRs: `gh pr list --state merged --limit 20`

---

### Step 5: Documentation Review

**Purpose:** Ensure documentation accurately reflects the release

**Commands:**

```bash
# Check for outdated version references
git grep -n "0\.[0-9]\.[0-9]" README.md docs/*.md | grep -v CHANGELOG.md | grep -v "version.*latest"

# Verify examples still work (manual check)
# Review key documentation files:
# - README.md - Installation and quick start
# - docs/guides/getting-started.md - Setup instructions
# - docs/guides/mcp-api-reference.md - API examples

# Check for references to removed features
# (manual review based on CHANGELOG)
```

**Validation:**

- README accurately describes current features
- No hardcoded old version numbers (except in CHANGELOG)
- Examples match current API
- No references to removed features
- Installation instructions are current

**If step fails:**

- Update documentation as needed
- Commit doc updates before proceeding
- Consider if docs warrant their own changelog entry

---

### Step 6: Final Build and Test

**Purpose:** Ensure everything builds and tests pass with new version

**Commands:**

```bash
# Clean previous build
rm -rf lib/

# Install dependencies (if any changes)
npm install

# Run full build
npm run build

# Run full test suite
npm test

# Verify package contents
npm pack --dry-run | head -20

# Check package size
npm pack --dry-run | grep "Tarball Contents"
```

**Validation:**

- Build completes without errors
- All tests pass (14 tests expected for docent)
- `lib/` directory contains compiled JavaScript
- Package includes correct files: `/bin`, `/lib`, `/templates`, `CHANGELOG.md`
- Package does NOT include: `src/`, `test/`, `docs/`, `.git/`
- Size is reasonable (< 1MB for docent)

**If step fails:**

- Fix build errors before proceeding
- Fix test failures - do not release broken code
- Update `files` array in package.json if package contents wrong
- Commit fixes and restart from Step 1

---

### Step 7: Review Changes

**Purpose:** Final review of all changes before committing

**Commands:**

```bash
# Check git status
git status

# Review all changes
git diff

# Specifically review version and changelog
git diff package.json
git diff CHANGELOG.md

# Verify no unexpected changes
git status --short
```

**Validation:**

- Only expected files are modified (package.json, CHANGELOG.md, possibly docs)
- Version number is correct in package.json
- CHANGELOG.md is complete and accurate
- No unintended changes
- No debug code or temporary files

**If step fails:**

- Use `git checkout -- <file>` to discard unwanted changes
- Make corrections and re-review

---

### Step 8: Commit and Tag Release

**Purpose:** Create release commit and git tag

**Commands:**

```bash
# Get version from package.json
VERSION=$(npm pkg get version | tr -d '"')
echo "Preparing release v$VERSION"

# Stage release changes (IMPORTANT: include package-lock.json)
git add package.json package-lock.json CHANGELOG.md
# Add any documentation updates if made
# git add README.md docs/

# Create release commit
git commit -m "chore: release v${VERSION}"

# Create annotated tag
git tag -a "v${VERSION}" -m "Release v${VERSION}"

# Verify commit and tag
git log -1 --stat
git show "v${VERSION}" --stat
```

**Validation:**

- Commit message follows format: `chore: release vX.Y.Z`
- Commit includes: package.json, package-lock.json, CHANGELOG.md (and any docs)
- Tag is created with format `vX.Y.Z` (lowercase v)
- Tag points to release commit
- Commit and tag are local only (not pushed yet)
- Verify files in commit: `git show --stat`

**If step fails:**

- Fix commit message: `git commit --amend -m "correct message"`
- Delete and recreate tag: `git tag -d vX.Y.Z && git tag -a vX.Y.Z -m "..."`
- Unstage unwanted files: `git reset HEAD <file>`

---

### Step 9: Final Pre-Push Validation

**Purpose:** Last check before pushing (triggers automated publish)

**Commands:**

```bash
# Verify working tree is clean
git status

# Verify all local CI checks pass
npm run build && npm test && npm run lint:md || echo "⚠ Local checks failed"

# Verify commit and tag are correct
git log -1 --oneline
VERSION=$(npm pkg get version | tr -d '"')
git tag -l "v${VERSION}"

# Verify you're on main branch
git branch --show-current

# Check remote CI status
gh run list --branch main --limit 5 --json conclusion,name,startedAt --jq '.[] | "\(.startedAt | split("T")[0]) \(.name): \(.conclusion)"'
```

**Validation:**

- Working directory is clean
- Local build and tests pass
- Commit message is correct
- Tag exists and matches version
- On main branch
- Latest CI run on main is successful

**If step fails:**

- Fix any issues found
- Do NOT push until everything is validated
- May need to amend commit or delete/recreate tag

---

## Part 2: Publish (Automated via GitHub Actions)

### Step 10: Push Release

**Purpose:** Push commit and tag to trigger automated publishing

**⚠️ POINT OF NO RETURN**: Once you push the tag, GitHub Actions will automatically publish to npm. Verify everything in Steps 1-9 before proceeding.

**Commands:**

```bash
# Push commit and tag together
git push origin main --follow-tags

# Immediately check that push succeeded
git status
git ls-remote --tags origin | grep "$(npm pkg get version | tr -d '"')"
```

**Validation:**

- Commit is pushed to origin/main
- Tag is pushed to origin
- No errors during push
- Remote shows the tag

**If step fails:**

- Check network connectivity
- Verify push permissions
- If behind remote: `git pull --rebase origin main` then retry
- If tag fails: `git push origin vX.Y.Z`

---

### Step 11: Monitor GitHub Actions Publish

**Purpose:** Watch the automated publish workflow complete

**Commands:**

```bash
# Open Actions page in browser
VERSION=$(npm pkg get version | tr -d '"')
gh run watch --repo tnez/docent

# Or check status from CLI
gh run list --workflow=publish.yml --limit 5

# View specific run details
gh run view --log
```

**What the Publish Workflow Does:**

1. ✅ Checks out code at the tagged commit
2. ✅ Sets up Node.js and installs dependencies
3. ✅ Runs build: `npm run build`
4. ✅ Runs tests: `npm test`
5. ✅ Publishes to npm: `npm publish --access public`
6. ✅ Creates GitHub Release with CHANGELOG notes
7. ✅ Uploads release assets

**Expected Timeline:**

- Workflow starts: ~30 seconds after push
- Build/test phase: 2-3 minutes
- npm publish: 30-60 seconds
- GitHub release: 15-30 seconds
- **Total: ~4-5 minutes**

**Monitoring Checklist:**

- [ ] Workflow starts (check within 1 minute of push)
- [ ] Build step passes (green checkmark)
- [ ] Test step passes (all tests green)
- [ ] npm publish succeeds (package version updated)
- [ ] GitHub release created (visible in Releases tab)
- [ ] No errors in workflow logs

**If workflow fails:**

See Troubleshooting section below for common issues and recovery procedures.

---

### Step 12: Verify Publication

**Purpose:** Confirm package is available and installable

**Commands:**

```bash
# Wait for npm propagation (30-60 seconds)
sleep 30

# Check package on npm
VERSION=$(npm pkg get version | tr -d '"')
npm view @tnezdev/docent@${VERSION} version

# View full package info
npm view @tnezdev/docent

# Test installation in temporary directory
mkdir -p /tmp/test-npm-install
cd /tmp/test-npm-install
npm install @tnezdev/docent
./node_modules/.bin/docent --version 2>/dev/null || echo "Binary check"
ls -la node_modules/@tnezdev/docent/

# Cleanup
cd -
rm -rf /tmp/test-npm-install
```

**Validation:**

- Package appears on npm registry with correct version
- Published date is today
- Package installs successfully
- Binary is executable
- Templates directory exists
- lib/ directory contains compiled code

**If step fails:**

- Wait longer for npm propagation (up to 5 minutes)
- Check npm registry status: https://status.npmjs.org/
- Review GitHub Actions logs for publish errors
- See Troubleshooting section

---

### Step 13: Verify GitHub Release

**Purpose:** Confirm GitHub release was created correctly

**Commands:**

```bash
# View release in browser
VERSION=$(npm pkg get version | tr -d '"')
gh release view "v${VERSION}" --web

# Or check from CLI
gh release view "v${VERSION}"

# Verify release notes
gh release view "v${VERSION}" --json body --jq '.body' | head -20
```

**Validation:**

- GitHub release exists for tag
- Release notes match CHANGELOG section
- Release is marked as "Latest release" (if applicable)
- Release assets include source tarball
- No "Pre-release" flag (unless intentional)

**If step fails:**

- Check GitHub Actions logs for release creation errors
- Release can be created manually if workflow failed:

```bash
VERSION=$(npm pkg get version | tr -d '"')
awk "/## \[${VERSION}\]/,/## \[/" CHANGELOG.md | head -n -2 | tail -n +3 > /tmp/release-notes.md
gh release create "v${VERSION}" --title "Release v${VERSION}" --notes-file /tmp/release-notes.md
rm /tmp/release-notes.md
```

---

### Step 14: Post-Release Verification

**Purpose:** Final checks and cleanup

**Commands:**

```bash
# Verify CI is passing on main after push
gh run list --branch main --limit 3

# Check for any issues opened immediately after release
gh issue list --label "bug" --limit 5

# Verify no uncommitted changes
git status

# Pull any changes made by GitHub Actions (if any)
git pull origin main
```

**Validation:**

- All CI checks passing on main
- No critical bugs reported
- Local repo is in sync with remote
- Working directory is clean

**Post-Release Tasks:**

- [ ] Monitor npm download stats (https://npmtrends.com/@tnezdev/docent)
- [ ] Watch for issues in first 24-48 hours
- [ ] Close related issues/PRs with "Fixed in vX.Y.Z" comment
- [ ] Update project board/milestones if applicable
- [ ] Announce release (optional - see Step 15)

---

### Step 15: Announce Release (Optional)

**Purpose:** Notify users and contributors of new release

**Commands:**

```bash
# Get release URLs
VERSION=$(npm pkg get version | tr -d '"')
echo "GitHub Release: https://github.com/tnez/docent/releases/tag/v${VERSION}"
echo "npm Package: https://www.npmjs.com/package/@tnezdev/docent/v/${VERSION}"
```

**Announcement Channels (as applicable):**

- GitHub Discussions (if enabled)
- Project Discord/Slack
- Twitter/Social media
- Dev.to or blog post (for major releases)
- Email to contributors list

**Announcement Template:**

```markdown
🎉 docent v${VERSION} is now available!

**Highlights:**
- [Key feature 1]
- [Key feature 2]
- [Important fix]

**Install/Update:**
`npm install @tnezdev/docent@latest`

**Full changelog:** https://github.com/tnez/docent/releases/tag/v${VERSION}
```

---

## Troubleshooting

### Common Workflow Failures

#### Issue: Publish Workflow Test Failures

**Symptoms:**

- GitHub Actions workflow fails at test step
- Tests were passing locally

**Resolution:**

1. Check workflow logs: `gh run view --log`
2. Look for environment differences (Node version, OS)
3. If reproducible locally:
   - Fix tests
   - Commit fix
   - Create new patch release
4. If not reproducible:
   - Re-run workflow: `gh run rerun`
   - Check GitHub Actions status

---

#### Issue: npm Publish Permission Denied

**Symptoms:**

- Workflow fails at publish step with 403 or permission error
- Error: "You do not have permission to publish"

**Resolution:**

1. Verify npm token in GitHub secrets:
   - Settings → Secrets → Actions
   - Check `NPM_TOKEN` exists and is not expired
2. Regenerate npm token:
   - Log in to npmjs.com
   - Generate new automation token
   - Update GitHub secret
3. Re-run failed workflow: `gh run rerun --failed`

---

#### Issue: Version Already Published

**Symptoms:**

- Workflow fails with "cannot publish over existing version"

**Resolution:**

This means the version was already published (possibly from previous attempt).

**Option 1: Skip npm publish (if version is correct)**

```bash
# Version is already on npm - just verify
npm view @tnezdev/docent version

# If correct, just create GitHub release manually
VERSION=$(npm pkg get version | tr -d '"')
gh release create "v${VERSION}" --title "Release v${VERSION}" --notes "See CHANGELOG.md"
```

**Option 2: Bump version again (if version was wrong)**

```bash
# Delete remote tag
git push origin :refs/tags/vX.Y.Z

# Delete local tag
git tag -d vX.Y.Z

# Bump version again
npm version patch --no-git-tag-version
git add package.json
git commit --amend --no-edit
git tag -a "vX.Y.Z" -m "Release vX.Y.Z"
git push origin main --follow-tags --force-with-lease
```

---

#### Issue: GitHub Release Creation Fails

**Symptoms:**

- npm publish succeeds but GitHub release fails
- Workflow completes with partial success

**Resolution:**

Create GitHub release manually:

```bash
VERSION=$(npm pkg get version | tr -d '"')

# Extract release notes from CHANGELOG
awk "/## \[${VERSION}\]/,/## \[/" CHANGELOG.md | head -n -2 | tail -n +3 > /tmp/release-notes.md

# Create release
gh release create "v${VERSION}" \
  --title "Release v${VERSION}" \
  --notes-file /tmp/release-notes.md

# Cleanup
rm /tmp/release-notes.md
```

---

#### Issue: Breaking Change in Patch Release

**Symptoms:**

- Realized after publishing that a breaking change was in a patch release
- Semantic versioning was violated

**Resolution:**

**Immediate action:**

```bash
# Deprecate the incorrect version
npm deprecate @tnezdev/docent@X.Y.Z "Breaking changes - use X+1.0.0 instead"

# Create proper major version
npm version major --no-git-tag-version
# Update CHANGELOG to reflect proper versioning
git add package.json package-lock.json CHANGELOG.md
git commit -m "chore: release vX+1.0.0 (correcting semver violation)"
# Restart from Step 8
```

---

### Emergency Rollback

If critical bug discovered immediately after publish:

```bash
# 1. Deprecate the broken version
npm deprecate @tnezdev/docent@X.Y.Z "Critical bug - use X.Y.Z+1"

# 2. Pull the tag locally
git fetch --tags
git checkout "vX.Y.Z"

# 3. Create hotfix branch
git checkout -b hotfix/vX.Y.Z+1

# 4. Fix the bug and test
# ... make fixes ...
npm run build && npm test

# 5. Merge to main and create new release
git checkout main
git merge hotfix/vX.Y.Z+1
npm version patch --no-git-tag-version
git add package.json package-lock.json CHANGELOG.md
git commit -m "chore: hotfix vX.Y.Z+1"
git tag -a "vX.Y.Z+1" -m "Hotfix vX.Y.Z+1"
git push origin main --follow-tags

# 6. Monitor new publish workflow
gh run watch
```

**Note:** Cannot unpublish from npm after 72 hours. Deprecation + new version is the only option.

---

### When to Escalate

Escalate if:

- Critical security vulnerability discovered in published version
- npm registry having extended outage
- GitHub Actions repeatedly failing for infrastructure reasons
- Permissions issues cannot be resolved
- Breaking changes accidentally published

**Escalation Contact:**

- npm support (for registry issues)
- GitHub support (for Actions issues)
- Security team (for vulnerabilities)
- Package owner/maintainer

---

## Validation Checklist

After completing all steps:

- [ ] **Local:**
  - [ ] Version bumped in package.json
  - [ ] CHANGELOG updated with release notes
  - [ ] All tests passing locally
  - [ ] Build succeeds locally
  - [ ] No debug code or test markers in src/
  - [ ] Documentation is current

- [ ] **Remote:**
  - [ ] Commit pushed to origin/main
  - [ ] Tag pushed to origin
  - [ ] GitHub Actions workflow completed successfully

- [ ] **npm:**
  - [ ] Package published with correct version
  - [ ] Package installs successfully
  - [ ] Binary works
  - [ ] Templates included

- [ ] **GitHub:**
  - [ ] Release created with correct tag
  - [ ] Release notes match CHANGELOG
  - [ ] CI passing on main

---

## Quick Reference

### Full Release Command Sequence

```bash
# Pre-flight
git checkout main && git pull origin main
git status  # Must be clean
npm test && npm run build  # Must pass

# Version and changelog
npm version patch --no-git-tag-version  # or minor/major
$EDITOR CHANGELOG.md

# Final validation
npm run build && npm test
npm pack --dry-run

# Commit and tag
VERSION=$(npm pkg get version | tr -d '"')
git add package.json package-lock.json CHANGELOG.md
git commit -m "chore: release v${VERSION}"
git tag -a "v${VERSION}" -m "Release v${VERSION}"

# Push (triggers automated publish)
git push origin main --follow-tags

# Monitor
gh run watch
```

### Monitoring Commands

```bash
# Watch workflow progress
gh run watch

# Check workflow status
gh run list --workflow=publish.yml --limit 5

# View workflow logs
gh run view --log

# Check npm publication
npm view @tnezdev/docent version

# Test installation
npm install @tnezdev/docent
```

---

## Notes

**Important:**

- Pushing a version tag triggers automatic npm publishing
- Cannot unpublish from npm after 72 hours
- Always verify locally before pushing
- Breaking changes require major version bump
- GitHub Actions needs valid NPM_TOKEN secret

**Gotchas:**

- `--follow-tags` only pushes annotated tags (created with `-a`)
- npm propagation can take 30-60 seconds
- GitHub Actions has ~30 second startup delay
- CHANGELOG format must match for release notes extraction
- Tag format must be `vX.Y.Z` (lowercase v prefix)

**Related Procedures:**

- [CI/CD Health Check](./ci-cd-health-check.md) - if CI is failing
- [Fix Markdown Lint](./fix-markdown-lint.md) - if linting blocks release

---

## Revision History

| Date | Author | Changes |
|------|--------|---------|
| 2025-10-17 | @tnez | Combined prepare-release and publish-package into single GitOps workflow |

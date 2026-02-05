---
name: npm-monorepo-publish
description: Orchestrate publishing monorepo packages to npm using Lerna with OTP handling, pre-publish validation (build + lint), dry-run preview, and post-publish verification. Use when user requests to publish, release, or deploy packages to npm registry. Designed for Lerna-managed monorepos with 2FA-enabled npm accounts.
version: 0.3.0
---

# NPM Monorepo Publish

Streamlined npm publishing for Lerna monorepos with automated validation, OTP handling, and verification.

## When to Use

Trigger this skill when user requests:
- "Publish to npm"
- "Release a new version"
- "Deploy the package"
- "Publish updated packages"
- "Push to npm registry"
- "Create a release"

**Requirements:** Lerna monorepo, npm authentication with 2FA enabled

## Publishing Workflow

### Option 1: Automated (Recommended)

Use the interactive publisher script for guided publishing with automatic validation and OTP retry logic:

```bash
# Preview changes (dry-run)
python3 scripts/publish-interactive.py --dry-run

# Publish with release branch workflow (default in v0.3.0+)
python3 scripts/publish-interactive.py

# Publish without release branch (direct publish)
python3 scripts/publish-interactive.py --no-release-branch
```

The script automatically handles pre-flight checks, git state validation, release branch creation, dry-run preview, OTP prompts with validation, merge back to main, and post-publish verification.

**What's New in v0.3.0:**
- **Release branch workflow enabled by default**
- Creates isolated release branches (`release/v0.6.2`)
- Publishes from release branch
- Automatically merges back to main/master with merge commit (`--no-ff`)
- Preserves remote release branches for historical reference
- Use `--no-release-branch` flag to opt-out and use v0.2.0 direct-publish behavior

### Option 2: Manual Steps

For manual control, execute each step individually:

**Step 1: Pre-flight validation**
```bash
bash scripts/pre-flight-check.sh
```
Validates npm authentication, Lerna configuration, build success, and lint passing.

**Step 2: Dry-run preview**
```bash
lerna publish --no-git-tag-version --no-push --yes
```
Shows what will be published without making changes. Review output carefully.

**Step 3: Publish with OTP**
```bash
lerna publish --otp <6-digit-code>
```
Executes actual publish with your authenticator app OTP code.

**Step 4: Verify**
```bash
npm view @scope/package version
npm view @scope/package time
```
Confirms package is live on npm registry with correct version.

## Error Handling

**OTP expired/invalid:**
- Re-run with fresh OTP code (expires in ~30 seconds)
- Interactive script retries automatically (3 attempts)

**Build/lint failures:**
- Fix errors shown in output
- Re-run pre-flight checks after fixes

**Network errors:**
- Check internet connection
- Verify npm registry accessible
- Do NOT retry automatically (may cause duplicate publish)

**Permission errors:**
```bash
npm access ls-packages  # Verify publish permissions
```

**For comprehensive troubleshooting:** See `references/troubleshooting.md`

## Release Branch Workflow

**Enabled by default in v0.3.0+**

The skill implements a release branch workflow for better git history tracking and safer publishing:

### How It Works

1. **Git state validation** - Checks clean working directory, verifies not on release branch, warns if out of sync
2. **Release branch creation** - Creates `release/v{version}` branch (single package) or `release/multi-{timestamp}` (multiple packages)
3. **Publish from release branch** - Lerna creates git tags on the release branch
4. **Merge back to main** - Merges release branch to main/master with merge commit (`--no-ff`)
5. **Preserve release branches** - Remote release branches kept for historical reference

### Branch Naming

- **Single package**: `release/v0.6.2`, `release/v1.0.0`, `release/v2.1.3-beta.0`
- **Multi-package**: `release/multi-20260106-143052` (timestamp format: YYYYMMDD-HHMMSS)

### Opt-Out

To use the v0.2.0 direct-publish workflow (publish from current branch without creating release branch):

```bash
python3 scripts/publish-interactive.py --no-release-branch
```

### Recovery Scenarios

If merge fails after successful publish:
1. ✅ Packages are already on npm (successful)
2. ✅ Git tags exist on release branch
3. ⚠️ Release branch is preserved for manual intervention
4. Follow on-screen instructions to complete the merge manually

## Configuration

Standard Lerna configuration with independent versioning and conventional commits:

```json
{
  "version": "independent",
  "conventionalCommits": true
}
```

**Conventional commit version mapping:**
- `feat:` → minor bump (0.6.1 → 0.7.0)
- `fix:` → patch bump (0.6.1 → 0.6.2)
- `BREAKING CHANGE:` → major bump (0.6.1 → 1.0.0)

**For detailed configuration:** See `references/lerna-config.md`

## Resources

Load these references as needed for detailed guidance:

- **references/troubleshooting.md** - Comprehensive error solutions (OTP, auth, network, build, version issues)
- **references/lerna-config.md** - Configuration options (independent versioning, GitHub releases, publishConfig)
- **references/technical-reference.md** - Technical specs, best practices, debugging commands
- **references/workflow-examples.md** - 10 detailed workflow scenarios (standard, multi-package, canary, private registry)
- **scripts/pre-flight-check.sh** - Automated validation script
- **scripts/publish-interactive.py** - Guided publishing with OTP handling

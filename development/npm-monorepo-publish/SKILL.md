---
name: npm-monorepo-publish
description: Orchestrate publishing monorepo packages to npm using Lerna with OTP handling, pre-publish validation (build + lint), dry-run preview, and post-publish verification. Use when user requests to publish, release, or deploy packages to npm registry. Designed for Lerna-managed monorepos with 2FA-enabled npm accounts.
version: 0.1.0
---

# NPM Monorepo Publish

## Overview

This skill streamlines publishing monorepo packages to npm by wrapping the Lerna publish workflow with automated validation, OTP handling, and verification. It eliminates manual friction points while maintaining compatibility with existing Lerna configuration (independent versioning, conventional commits, GitHub releases).

**Core workflow:**
1. Pre-flight validation (authentication, build, lint)
2. Dry-run preview to show what will change
3. OTP prompt and handling
4. Lerna publish execution
5. Post-publish verification

## When to Use This Skill

Trigger this skill when the user requests any of the following:

- "Publish to npm"
- "Release a new version"
- "Deploy the package"
- "Publish updated packages"
- "Push to npm registry"
- "Create a release"
- "Bump version and publish"

**Requirements:**
- Working directory must be a Lerna-managed monorepo
- User must be authenticated with npm (`npm whoami` succeeds)
- User's npm account must have 2FA enabled (requires OTP)

## Publishing Workflow

Follow this workflow step-by-step when publishing packages:

### Step 1: Pre-Flight Validation

Before attempting to publish, verify the environment is ready:

```bash
# 1. Verify npm authentication
npm whoami

# 2. Verify on correct branch (optional but recommended)
git branch --show-current

# 3. Run build to ensure packages compile
npm run build --prefix packages/fpkit

# 4. Run lint to ensure code quality
npm run lint
```

**Success criteria:**
- `npm whoami` returns authenticated username
- Build completes without errors
- Lint passes with no errors

**If validation fails:**
- Stop the workflow immediately
- Show clear error message explaining what failed
- Provide guidance on how to fix (e.g., "Run `npm login` to authenticate")
- Do NOT proceed to publish

### Step 2: Dry-Run Preview

Run a dry-run to preview what will be published WITHOUT actually publishing:

```bash
lerna publish --no-git-tag-version --no-push --yes
```

**What this does:**
- Analyzes changed packages since last release
- Determines version bumps based on conventional commits
- Shows what WOULD be published without actually publishing
- Does NOT create git tags or push to remote

**Present to user:**
- List of packages that will be published
- Current version → new version for each package
- Summary of changes (from conventional commits)

**Ask for confirmation:**
- "Ready to publish these changes? I'll need your OTP code."
- If user says NO: Exit gracefully without publishing
- If user says YES: Proceed to Step 3

### Step 3: OTP Prompt and Collection

Prompt the user for their one-time password (OTP):

**Prompt:**
```
Please enter your 6-digit OTP code from your authenticator app:
```

**Important OTP details to remember:**
- OTP codes are exactly 6 digits
- OTP codes expire after ~30 seconds
- OTP codes are single-use only
- If user provides expired OTP, npm will reject and allow retry

**DO NOT:**
- Guess or generate fake OTP codes
- Skip OTP prompt
- Cache OTP codes between publishes

### Step 4: Execute Publish

Run the actual Lerna publish command with the OTP:

```bash
lerna publish --otp <6-digit-code>
```

**What this does:**
- Bumps versions in package.json files
- Publishes packages to npm registry (with OTP)
- Creates git tags for each published version
- Commits version changes
- Pushes commits and tags to remote
- Creates GitHub releases (if configured)

**Monitor output for:**
- ✅ Success: "Successfully published"
- ❌ OTP expired: "OTP invalid" or "expired"
- ❌ Network error: "ETIMEDOUT", "ENOTFOUND"
- ❌ Permission error: "403 Forbidden"

**Error handling:**

**If OTP is invalid/expired:**
1. Show message: "OTP code expired or invalid"
2. Return to Step 3 (re-prompt for OTP)
3. Allow up to 3 retry attempts

**If network error:**
1. Show error message with details
2. Suggest: "Check your internet connection and try again"
3. DO NOT retry automatically (may cause duplicate publishes)

**If permission error:**
1. Show error message
2. Verify user has publish permissions: `npm access ls-packages`
3. Suggest checking npm organization membership

**If other error:**
1. Show full error message
2. Reference troubleshooting.md for common issues
3. Suggest manual rollback if needed (see Step 6)

### Step 5: Post-Publish Verification

After successful publish, verify packages are live on npm:

```bash
# Verify published version matches expected
npm view @fpkit/acss version

# Check publish timestamp
npm view @fpkit/acss time

# Verify package is accessible
npm view @fpkit/acss
```

**Success indicators:**
- Version on npm matches what was just published
- Publish timestamp is recent (within last minute)
- Package metadata is correct

**Present to user:**
- ✅ Success message: "Successfully published @fpkit/acss@X.Y.Z"
- 📦 npm package URL: `https://www.npmjs.com/package/@fpkit/acss`
- 🏷️ GitHub release URL: `https://github.com/user/repo/releases/tag/vX.Y.Z`
- 📊 Version diff: `0.6.1 → 0.6.2`

### Step 6: Error Recovery and Rollback

If publish fails after git operations but before npm publish completes, guide user through rollback:

**Scenario 1: Git tags created but npm publish failed**
```bash
# Remove git tag
git tag -d v0.6.2
git push origin :refs/tags/v0.6.2

# Reset version changes
git reset --hard HEAD~1
```

**Scenario 2: Partial publish (some packages succeeded, others failed)**
```bash
# Check what was published
npm view @fpkit/acss version

# Use lerna publish from-package to publish remaining
lerna publish from-package --otp <code>
```

**Scenario 3: Need to undo a publish**
```bash
# IMPORTANT: npm unpublish has restrictions
# Can only unpublish within 72 hours
# Cannot unpublish if package has dependents

# Deprecate instead (safer)
npm deprecate @fpkit/acss@0.6.2 "Accidental publish, use 0.6.1 instead"
```

## Lerna Configuration Compatibility

This skill works with standard Lerna configurations. Verify these settings in `lerna.json`:

**Independent versioning:**
```json
{
  "version": "independent",
  "conventionalCommits": true
}
```

**Conventional commits:**
- `feat:` → minor version bump
- `fix:` → patch version bump
- `BREAKING CHANGE:` → major version bump

**GitHub releases:**
- Automatically created if `createRelease: "github"` is set
- Requires `GH_TOKEN` environment variable for authentication

## Usage Examples

### Example 1: Standard publish workflow

**User:** "Publish the updated components to npm"

**Assistant workflow:**
1. Run pre-flight checks (whoami, build, lint)
2. Show dry-run preview: "Found 1 changed package: @fpkit/acss (0.6.1 → 0.6.2)"
3. Prompt: "Please enter your 6-digit OTP code:"
4. User provides: "123456"
5. Execute: `lerna publish --otp 123456`
6. Verify on npm registry
7. Show success: "✅ Published @fpkit/acss@0.6.2 to npm"

### Example 2: Build failure during validation

**User:** "Release the new version"

**Assistant workflow:**
1. Run `npm whoami` → ✅ Success
2. Run `npm run build` → ❌ Build failed with TypeScript errors
3. Stop workflow
4. Message: "Build failed with 3 TypeScript errors. Fix these errors before publishing:"
   ```
   src/components/Button.tsx:45 - Type error
   src/components/Card.tsx:12 - Type error
   src/utils/helpers.ts:8 - Type error
   ```
5. Do NOT proceed to publish

### Example 3: OTP expiration and retry

**User:** "Publish to npm"

**Assistant workflow:**
1. Pre-flight checks → ✅ Pass
2. Dry-run preview → ✅ Show changes
3. Prompt for OTP → User provides "123456"
4. Execute publish → ❌ "Invalid OTP"
5. Re-prompt: "OTP expired or invalid. Please enter a fresh 6-digit code:"
6. User provides "789012"
7. Execute publish → ✅ Success
8. Verify and show success message

## Resources

### references/troubleshooting.md

Comprehensive troubleshooting guide for common npm publish errors:
- OTP handling issues
- Network timeouts
- Permission errors
- Version conflicts
- Registry authentication

Load this reference when encountering publish errors to provide detailed guidance.

## Technical Notes

**Working directory:**
- Must be monorepo root (where lerna.json exists)
- Commands run from root directory

**OTP format:**
- Exactly 6 digits (no spaces, no dashes)
- Numeric only
- Single-use per publish operation

**Lerna behavior:**
- Analyzes git history since last tag
- Uses conventional commits to determine version bumps
- Only publishes packages that have changed
- Respects `publishConfig` in package.json

**npm registry:**
- Default: https://registry.npmjs.org/
- Supports private registries via .npmrc
- Respects scoped package access settings (@org/package)

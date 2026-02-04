---
name: pypi-doppler
description: LOCAL-ONLY PyPI publishing with Doppler credentials. TRIGGERS - publish to PyPI, pypi upload, local publish. NEVER use in CI/CD.
---

# PyPI Publishing with Doppler (Local-Only)

## ⚠️ WORKSPACE-WIDE POLICY: LOCAL-ONLY PUBLISHING

**This skill supports LOCAL machine publishing ONLY.**

### FORBIDDEN

❌ **Publishing from GitHub Actions**
❌ **Publishing from any CI/CD pipeline** (GitHub Actions, GitLab CI, Jenkins, CircleCI)
❌ **`publishCmd` in semantic-release configuration**
❌ **Building packages in CI** (`uv build` in prepareCmd)
❌ **Storing PyPI tokens in GitHub secrets**

### REQUIRED

✅ **Use `scripts/publish-to-pypi.sh` on local machine**
✅ **CI detection guards in publish script**
✅ **Manual approval before each release**
✅ **Doppler credential management** (no plaintext tokens)
✅ **Repository verification** (prevents fork abuse)

### Rationale

- **Security**: No long-lived PyPI tokens in GitHub secrets
- **Speed**: 30 seconds locally vs 3-5 minutes in CI
- **Control**: Manual approval step before production release
- **Flexibility**: Centralized credential management via Doppler

**See**: ADR-0027, `docs/development/PUBLISHING.md`

---

## Overview

This skill provides **local-only PyPI publishing** using Doppler for secure credential management. It integrates with the workspace-wide release workflow where:

1. **GitHub Actions**: Automated versioning ONLY (tags, releases, CHANGELOG)
2. **Local Machine**: Manual PyPI publishing with Doppler credentials

## Bundled Scripts

| Script                                                       | Purpose                                        |
| ------------------------------------------------------------ | ---------------------------------------------- |
| [`scripts/publish-to-pypi.sh`](./scripts/publish-to-pypi.sh) | Local PyPI publishing with CI detection guards |

**Usage**: Copy to your project's `scripts/` directory:

```bash
/usr/bin/env bash << 'DOPPLER_EOF'
# Environment-agnostic path
PLUGIN_DIR="${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/marketplaces/cc-skills/plugins/itp}"
cp "$PLUGIN_DIR/skills/pypi-doppler/scripts/publish-to-pypi.sh" scripts/
chmod +x scripts/publish-to-pypi.sh
DOPPLER_EOF
```

---

## Prerequisites

### One-Time Setup

1. **Install Doppler CLI**:

   ```bash
   brew install dopplerhq/cli/doppler
   ```

2. **Authenticate with Doppler**:

   ```bash
   doppler login
   ```

3. **Verify access to `claude-config` project**:

   ```bash
   doppler whoami
   doppler projects
   ```

### PyPI Token Setup

1. **Create PyPI API token**:
   - Visit: <https://pypi.org/manage/account/token/>
   - Enable 2FA if not already enabled (required since 2024)
   - Create token with scope: "Entire account" or specific project
   - Copy token (starts with `pypi-AgEIcHlwaS5vcmc...`, ~180 characters)

2. **Store token in Doppler**:

   ```bash
   doppler secrets set PYPI_TOKEN='pypi-AgEIcHlwaS5vcmc...' \
     --project claude-config \
     --config prd
   ```

3. **Verify token stored**:

   ```bash
   doppler secrets get PYPI_TOKEN \
     --project claude-config \
     --config prd \
     --plain
   ```

---

## Publishing Workflow

### MANDATORY: Verify Version Increment Before Publishing

**Pre-publish validation**: Before publishing to PyPI, verify that the version has incremented from the previous release. Publishing without a version increment is invalid and wastes resources.

**Autonomous check sequence**:

1. Compare local `pyproject.toml` version against latest PyPI version
2. If versions match → **STOP** - do not proceed with publishing
3. Inform user: "Version not incremented. Run semantic-release first or verify commits include `feat:` or `fix:` types."

**Why this matters**: PyPI rejects duplicate versions, but more importantly, users and package managers rely on version increments to detect updates. A release workflow that doesn't increment version is broken.

### Complete Release Workflow

**Step 1: Development & Commit** (Conventional Commits):

```bash
# Make your changes
git add .

# Commit with conventional format (determines version bump)
git commit -m "feat: add new feature"  # MINOR bump

# Push to main
git push origin main
```

**Step 2: Automated Versioning** (GitHub Actions - 40-60s):

GitHub Actions workflow automatically:

- ✅ Analyzes commits using `@semantic-release/commit-analyzer`
- ✅ Determines next version (e.g., `v7.1.0`)
- ✅ Updates `pyproject.toml`, `package.json` versions
- ✅ Generates and updates `CHANGELOG.md`
- ✅ Creates git tag (`v7.1.0`)
- ✅ Creates GitHub release with release notes
- ✅ Commits changes back to repo with `[skip ci]` message

**⚠️ PyPI publishing does NOT happen here** (by design - see ADR-0027)

**Step 3: Local PyPI Publishing** (30 seconds):

**After GitHub Actions completes**, publish to PyPI locally:

```bash
# Pull the latest release commit
git pull origin main

# Publish to PyPI (uses pypi-doppler skill)
./scripts/publish-to-pypi.sh
```

**Expected output**:

```
🚀 Publishing to PyPI (Local Workflow)
======================================

🔐 Step 0: Verifying Doppler credentials...
   ✅ Doppler token verified

📥 Step 1: Pulling latest release commit...
   Current version: v7.1.0

🧹 Step 2: Cleaning old builds...
   ✅ Cleaned

📦 Step 3: Building package...
   ✅ Built: dist/gapless_crypto_clickhouse-7.1.0-py3-none-any.whl

📤 Step 4: Publishing to PyPI...
   Using PYPI_TOKEN from Doppler
   ✅ Published to PyPI

🔍 Step 5: Verifying on PyPI...
   ✅ Verified: https://pypi.org/project/gapless-crypto-clickhouse/7.1.0/

✅ Complete! Published v7.1.0 to PyPI in 28 seconds
```

---

## Publishing Command (Local Machine Only)

**CRITICAL**: This command must ONLY run on your local machine, NEVER in CI/CD.

### Using Bundled Script (Recommended)

```bash
/usr/bin/env bash << 'GIT_EOF'
# First time: copy script from skill to your project (environment-agnostic)
PLUGIN_DIR="${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/marketplaces/cc-skills/plugins/itp}"
cp "$PLUGIN_DIR/skills/pypi-doppler/scripts/publish-to-pypi.sh" scripts/
chmod +x scripts/publish-to-pypi.sh

# After semantic-release creates GitHub release
git pull origin main

# Publish using local copy of bundled script
./scripts/publish-to-pypi.sh
GIT_EOF
```

**Bundled script features**:

- ✅ CI detection guards (blocks if CI=true)
- ✅ Repository verification (prevents fork abuse)
- ✅ Doppler integration (PYPI_TOKEN retrieval)
- ✅ Build + publish + verify workflow
- ✅ Clear error messages

### Manual Publishing (Advanced)

For manual publishing without the canonical script:

```bash
/usr/bin/env bash << 'CONFIG_EOF'
# Retrieve token from Doppler
PYPI_TOKEN=$(doppler secrets get PYPI_TOKEN \
  --project claude-config \
  --config prd \
  --plain)

# Build package
uv build

# Publish to PyPI
UV_PUBLISH_TOKEN="${PYPI_TOKEN}" uv publish
CONFIG_EOF
```

**⚠️ WARNING**: Manual publishing bypasses CI detection guards and repository verification. Use canonical script unless you have a specific reason not to.

---

## CI Detection Enforcement

The canonical publish script (`scripts/publish-to-pypi.sh`) includes CI detection guards to prevent accidental execution in CI/CD pipelines.

### Environment Variables Checked

- `$CI` - Generic CI indicator
- `$GITHUB_ACTIONS` - GitHub Actions
- `$GITLAB_CI` - GitLab CI
- `$JENKINS_URL` - Jenkins
- `$CIRCLECI` - CircleCI

### Behavior

**If any CI variable detected**, script exits with error:

```
❌ ERROR: This script must ONLY be run on your LOCAL machine

   Detected CI environment variables:
   - CI: true
   - GITHUB_ACTIONS: <not set>
   ...

   This project enforces LOCAL-ONLY PyPI publishing for:
   - Security: No long-lived PyPI tokens in GitHub secrets
   - Speed: 30 seconds locally vs 3-5 minutes in CI
   - Control: Manual approval step before production release

   See: docs/development/PUBLISHING.md (ADR-0027)
```

### Testing CI Detection

```bash
# This should FAIL with error message
CI=true ./scripts/publish-to-pypi.sh

# Expected: ❌ ERROR: This script must ONLY be run on your LOCAL machine
```

---

## Credential Management

### Doppler Configuration

**Project**: `claude-config`
**Configs**: `prd` (production), `dev` (development)
**Secret Name**: `PYPI_TOKEN`

### Token Format

Valid PyPI token format:

- Starts with: `pypi-AgEIcHlwaS5vcmc`
- Length: ~180 characters
- Example: `pypi-AgEIcHlwaS5vcmcCJGI4YmNhMDA5LTg...`

### Token Permissions

**Account-wide token** (recommended):

- Can publish to all projects under your account
- Simpler management
- One token for all repositories

**Project-scoped token**:

- Can only publish to specific project
- More restrictive
- Separate token per project needed

### Token Rotation

```bash
# 1. Create new token on PyPI
# Visit: https://pypi.org/manage/account/token/

# 2. Update Doppler
doppler secrets set PYPI_TOKEN='new-token' \
  --project claude-config \
  --config prd

# 3. Verify new token works
doppler secrets get PYPI_TOKEN \
  --project claude-config \
  --config prd \
  --plain

# 4. Test publish (dry-run not available, use TestPyPI)
# See: Troubleshooting → TestPyPI Testing
```

---

## Troubleshooting

### Issue: "PYPI_TOKEN not found in Doppler"

**Symptom**: Script fails at Step 0

**Fix**:

```bash
# Verify token exists
doppler secrets --project claude-config --config prd | grep PYPI_TOKEN

# If missing, get new token from PyPI
# Visit: https://pypi.org/manage/account/token/
# Create token with scope: "Entire account" or specific project

# Store in Doppler
doppler secrets set PYPI_TOKEN='your-token' \
  --project claude-config \
  --config prd
```

### Issue: "403 Forbidden from PyPI"

**Symptom**: Script fails at Step 4 with authentication error

**Root Cause**: Token expired or invalid (PyPI requires 2FA since 2024)

**Fix**:

1. Verify 2FA enabled on PyPI account
2. Create new token: <https://pypi.org/manage/account/token/>
3. Update Doppler: `doppler secrets set PYPI_TOKEN='new-token' --project claude-config --config prd`
4. Retry publish

### Issue: "Script blocked with CI detection error"

**Symptom**:

```
❌ ERROR: This script must ONLY be run on your LOCAL machine
Detected CI environment variables:
- CI: true
```

**Root Cause**: Running in CI environment OR `CI` variable set locally

**Fix**:

```bash
# Check if CI variable set in your shell
env | grep CI

# If set, unset it
unset CI
unset GITHUB_ACTIONS

# Retry publish
./scripts/publish-to-pypi.sh
```

**Expected behavior**: This is INTENTIONAL - script should ONLY run locally.

### Issue: "Version not updated in pyproject.toml"

**Symptom**: Local publish uses old version number

**Root Cause**: Didn't pull latest release commit from GitHub

**Fix**:

```bash
# Always pull before publishing
git pull origin main

# Verify version updated
grep '^version = ' pyproject.toml

# Retry publish
./scripts/publish-to-pypi.sh
```

### Issue: "uv package manager not found"

**Symptom**: Script fails at startup before any steps

**Root Cause**: uv not installed or not discoverable

**How the script discovers uv** (in priority order):

1. Already in PATH (Homebrew, direct install, shell configured)
2. Common direct install locations (`~/.local/bin/uv`, `~/.cargo/bin/uv`, `/opt/homebrew/bin/uv`)
3. Version managers as fallback (mise, asdf)

**Fix**: Install uv using any method:

```bash
# Official installer (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Homebrew
brew install uv

# Cargo
cargo install uv

# mise (if you use it)
mise use uv@latest
```

The script doesn't force any particular installation method.

### Issue: Script Hangs with No Output

**Symptom**: Script starts but produces no output, eventually times out

**Root Cause**: Script sources `~/.zshrc` or `~/.bashrc` which waits for interactive input

**Fix**: Never source shell config files in scripts. The bundled script uses:

```bash
/usr/bin/env bash << 'MISE_EOF'
# CORRECT - safe for non-interactive shells
eval "$(mise activate bash 2>/dev/null)" || true

# WRONG - hangs in non-interactive shells
source ~/.zshrc
MISE_EOF
```

---

### TestPyPI Testing

To test publishing workflow without affecting production:

1. **Get TestPyPI token**:
   - Visit: <https://test.pypi.org/manage/account/token/>
   - Create token

2. **Store in Doppler** (separate key):

   ```bash
   doppler secrets set TESTPYPI_TOKEN='your-test-token' \
     --project claude-config \
     --config prd
   ```

3. **Modify publish script temporarily**:

   ```bash

   ```

/usr/bin/env bash << 'DOPPLER_EOF_2'

# In scripts/publish-to-pypi.sh, change

uv publish --token "${PYPI_TOKEN}"

# To

TESTPYPI_TOKEN=$(doppler secrets get TESTPYPI_TOKEN --plain)
   uv publish --repository testpypi --token "${TESTPYPI_TOKEN}"

DOPPLER_EOF_2

````

4. **Test publish**:

   ```bash
   ./scripts/publish-to-pypi.sh
````

1. **Verify on TestPyPI**:
   - <https://test.pypi.org/project/your-package/>

2. **Restore script** to production configuration

---

## Related Documentation

- **ADR-0027**: `docs/architecture/decisions/0027-local-only-pypi-publishing.md` - Architectural decision for local-only publishing
- **ADR-0028**: `docs/architecture/decisions/0028-skills-documentation-alignment.md` - Skills alignment with ADR-0027
- **PUBLISHING.md**: `docs/development/PUBLISHING.md` - Complete release workflow guide
- **semantic-release Skill**: [`semantic-release`](../semantic-release/SKILL.md) - Versioning automation (NO publishing)
- **Bundled Script**: [`scripts/publish-to-pypi.sh`](./scripts/publish-to-pypi.sh) - Reference implementation with CI guards

---

## Validation History

- **2025-12-03**: Refactored to discovery-first, environment-agnostic approach
  - `discover_uv()` checks PATH → direct installs → version managers (priority order)
  - Supports: curl install, Homebrew, cargo, mise, asdf - doesn't force any method
  - Early discovery at startup before any workflow steps
  - Troubleshooting for non-interactive shell issues
- **2025-11-22**: Created with ADR-0027 alignment (workspace-wide local-only policy)
- **Validation**: CI detection guards tested, Doppler integration verified

---

**Last Updated**: 2025-12-03
**Policy**: Workspace-wide local-only PyPI publishing (ADR-0027)
**Supersedes**: None (created with ADR-0027 compliance from start)

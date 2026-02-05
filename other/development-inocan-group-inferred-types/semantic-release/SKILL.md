---
name: semantic-release
description: Automate versioning with Node.js semantic-release v25+. TRIGGERS - npm run release, version bump, changelog, conventional commits, release automation.
allowed-tools: Read, Bash, Glob, Grep, Edit, Write
---

# semantic-release

## Overview

Automate semantic versioning and release management using **semantic-release v25+ (Node.js)** following 2025 best practices. Works with **all languages** (JavaScript, TypeScript, Python, Rust, Go, C++, etc.) via the `@semantic-release/exec` plugin. Create shareable configurations for multi-repository setups, initialize individual projects with automated releases, and configure GitHub Actions workflows with OIDC trusted publishing.

**Important**: This skill uses semantic-release (Node.js) exclusively, NOT python-semantic-release, even for Python projects. Rationale: 23.5x larger community, 100x+ adoption, better future-proofing.

## When to Use This Skill

Invoke when:

- Setting up local releases for a new project (any language)
- Creating shareable semantic-release configuration for organization-wide use
- Migrating existing projects to 2025 semantic-release patterns
- Troubleshooting semantic-release setup or version bumps
- Setting up Python projects (use Node.js semantic-release, NOT python-semantic-release)
- Configuring GitHub Actions (optional backup, not recommended as primary due to speed)
- Rust workspaces using release-plz (see [Rust reference](./references/rust-release-plz.md))

## Why Node.js semantic-release

**22,900 GitHub stars** - Large, active community
**1.9M weekly downloads** - Proven adoption
**126,000 projects using it** - Battle-tested at scale
**35+ official plugins** - Rich ecosystem
**Multi-language support** - Works with any language via `@semantic-release/exec`

**Do NOT use python-semantic-release.** It has a 23.5x smaller community (975 vs 22,900 stars), ~100x less adoption, and is not affiliated with the semantic-release organization.

---

## Release Workflow Philosophy: Local-First

**Default approach: Run releases locally, not via GitHub Actions.**

### Why Local Releases

**Primary argument: GitHub Actions is slow**

- ⏱️ GitHub Actions: 2-5 minute wait for release to complete
- ⚡ Local release: Instant feedback and file updates
- 🔄 Immediate workflow continuity - no waiting for CI/CD

**Additional benefits:**

- ✅ **Instant local file sync** - `package.json`, `CHANGELOG.md`, tags updated immediately
- ✅ **No pull required** - Continue working without `git pull` after release
- ✅ **Dry-run testing** - `npm run release:dry` to preview changes before release
- ✅ **Offline capable** - Can release without CI/CD dependency
- ✅ **Faster iteration** - Debug release issues immediately, not through CI logs

### GitHub Actions: Optional Backup Only

GitHub Actions workflows are provided as **optional automation**, not the primary method:

- Use for team consistency if required
- Backup if local environment unavailable
- **Not recommended as primary workflow due to speed**

### Authentication Setup

```bash
gh auth login
# Browser authentication once
# Credentials stored in keyring
# All future releases: zero manual intervention
```

**This is the minimum manual intervention possible** for local semantic-release with GitHub plugin functionality.

### Multi-Account Authentication via mise [env]

For multi-account GitHub setups, use mise `[env]` to set per-directory GH_TOKEN:

```toml
# ~/your-project/.mise.toml
[env]
GH_TOKEN = "{{ read_file(path=env.HOME ~ '/.claude/.secrets/gh-token-accountname') | trim }}"
GITHUB_TOKEN = "{{ read_file(path=env.HOME ~ '/.claude/.secrets/gh-token-accountname') | trim }}"
```

This overrides gh CLI's global authentication, ensuring semantic-release uses the correct account for each directory.

See the [`mise-configuration` skill](../mise-configuration/SKILL.md#github-token-multi-account-patterns) for complete setup.

### Critical Standard: No Testing/Linting in GitHub Actions

**This standard applies to ALL GitHub Actions workflows, not just semantic-release.**

#### Forbidden Workflow Steps

GitHub Actions workflows must NEVER include:

❌ **Test execution**:

```yaml
# ❌ FORBIDDEN - Do not add to any workflow
- run: pytest
- run: npm test
- run: cargo test
- uses: actions/upload-test-results # Implies testing
```

❌ **Linting/Formatting**:

```yaml
# ❌ FORBIDDEN - Do not add to any workflow
- run: ruff check
- run: eslint .
- run: cargo clippy
- run: prettier --check
- run: mypy
```

#### Allowed Workflow Patterns

✅ **Semantic-release** (this workflow):

```yaml
- run: npm run release # Version, changelog, GitHub release only
```

✅ **Security scanning**:

```yaml
- run: npm audit signatures
- uses: github/codeql-action/analyze@v3
```

✅ **Deployment**:

```yaml
- run: docker build && docker push
- run: aws s3 sync ./build s3://bucket
```

✅ **Dependency updates**:

```yaml
- uses: dependabot/fetch-metadata@v2
```

#### Enforcement

**Documentation-based**: This standard is enforced through CLAUDE.md instructions, not pre-commit hooks.

When creating or modifying GitHub Actions workflows, Claude Code will check CLAUDE.md and this skill to ensure compliance.

---

## Separation of Concerns (4-Level Architecture)

semantic-release configuration follows a hierarchical, composable pattern:

**Level 1: Skill** - `${CLAUDE_PLUGIN_ROOT}/skills/semantic-release/` (Generic templates, system-wide tool)
**Level 2: User Config** - `~/semantic-release-config/` (`@username/semantic-release-config`)
**Level 3: Organization Config** - npm registry (`@company/semantic-release-config`)
**Level 4: Project Config** - `.releaserc.yml` in project root

### Configuration Precedence

```
Level 4 (Project) → overrides → Level 3 (Org) → overrides → Level 2 (User) → overrides → Defaults
```

---

## Conventional Commits Format

semantic-release analyzes commit messages to determine version bumps:

```
<type>(<scope>): <subject>
```

### Version Bump Rules (Default)

- `feat:` → MINOR version bump (0.1.0 → 0.2.0)
- `fix:` → PATCH version bump (0.1.0 → 0.1.1)
- `BREAKING CHANGE:` or `feat!:` → MAJOR version bump (0.1.0 → 1.0.0)
- `docs:`, `chore:`, `style:`, `refactor:`, `perf:`, `test:` → No version bump (by default)

### Release Notes Visibility (Important)

**Warning**: The `@semantic-release/release-notes-generator` (Angular preset) only includes these types in release notes:

- `feat:` → **Features** section
- `fix:` → **Bug Fixes** section
- `perf:` → **Performance Improvements** section

Other types (`docs:`, `chore:`, `refactor:`, etc.) trigger releases when configured but **do NOT appear in release notes**.

**Recommendation**: For documentation changes that should be visible in release notes, use:

```
fix(docs): description of documentation improvement
```

This ensures the commit appears in the "Bug Fixes" section while still being semantically accurate (fixing documentation gaps is a fix).

### Marketplace Plugin Configuration (Always Bump)

For Claude Code marketplace plugins, **every change requires a version bump** for users to receive updates.

**Option A: Shareable Config (if published)**

```yaml
# .releaserc.yml
extends: "@terryli/semantic-release-config/marketplace"
```

**Option B: Inline Configuration**

```yaml
# .releaserc.yml
plugins:
  - - "@semantic-release/commit-analyzer"
    - releaseRules:
        # Marketplace plugins require version bump for ANY change
        - { type: "docs", release: "patch" }
        - { type: "chore", release: "patch" }
        - { type: "style", release: "patch" }
        - { type: "refactor", release: "patch" }
        - { type: "test", release: "patch" }
        - { type: "build", release: "patch" }
        - { type: "ci", release: "patch" }
```

**Result after configuration:**

| Commit Type                                                        | Release Type       |
| ------------------------------------------------------------------ | ------------------ |
| `feat:`                                                            | minor (default)    |
| `fix:`, `perf:`, `revert:`                                         | patch (default)    |
| `docs:`, `chore:`, `style:`, `refactor:`, `test:`, `build:`, `ci:` | patch (configured) |

**Why marketplace plugins need this**: Plugin updates are distributed via version tags. Without a version bump, users running `/plugin update` see no changes even if content was modified.

### MANDATORY: Every Release Must Increment Version

**Pre-release validation**: Before running semantic-release, verify releasable commits exist since last tag. A release without version increment is invalid.

**Autonomous check sequence**:

1. List commits since last tag: compare HEAD against latest version tag
2. Identify commit types: scan for `feat:`, `fix:`, or `BREAKING CHANGE:` prefixes
3. If NO releasable commits found → **STOP** - do not proceed with release
4. Inform user: "No version-bumping commits since last release. Use `feat:` or `fix:` prefix for releasable changes."

**Commit type selection guidance**:

- Use `fix:` for any change that improves existing behavior (bug fixes, enhancements, documentation corrections that affect usage)
- Use `feat:` for new capabilities or significant additions
- Reserve `chore:`, `docs:`, `refactor:` for changes that truly don't warrant a release

**Why this matters**: A release without version increment creates confusion - users cannot distinguish between releases, package managers may cache old versions, and changelog entries become meaningless.

### MAJOR Version Breaking Change Confirmation

**Trigger**: When commits contain `BREAKING CHANGE:` footer or `feat!:` / `fix!:` prefix.

**Why extra confirmation**: MAJOR version bumps signal breaking changes that require consumers to update their code. False positives (accidental `!` suffix) or unnecessary breaking changes can fragment the user base.

#### Phase 1: Detection (Automatic)

```bash
/usr/bin/env bash << 'MAJOR_CHECK_EOF'
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)
MAJOR_COMMITS=$(git log "${LAST_TAG}..HEAD" --oneline | grep -E "(BREAKING CHANGE|^[a-f0-9]+ (feat|fix)!:)")
if [[ -n "$MAJOR_COMMITS" ]]; then
    echo "MAJOR_DETECTED"
    echo "$MAJOR_COMMITS"
fi
MAJOR_CHECK_EOF
```

#### Phase 2: Multi-Perspective Analysis (Claude Task Subagents)

When MAJOR is detected, spawn **three parallel Task subagents** for independent analysis:

```
                      MAJOR Version Confirmation

+-----------+      -----------------   spawn 3 agents   +-------------+
| Migration | <-- | MAJOR Detected  | ----------------> | User Impact |
+-----------+      -----------------                    +-------------+
  |                 |                                     |
  |                 |                                     |
  |                 v                                     |
  |               +-----------------+                     |
  |               |   API Compat    |                     |
  |               +-----------------+                     |
  |                 |                                     |
  |                 |                                     |
  |                 v                                     |
  |               +-----------------+                     |
  +-------------> | Collect Results | <-------------------+
                  +-----------------+
                    |
                    |
                    v
                  #=================#
                  H AskUserQuestion H
                  #=================#
```

<details>
<summary>graph-easy source</summary>

```
graph { label: "MAJOR Version Confirmation"; flow: south; }

[ MAJOR Detected ] { shape: rounded; }
[ User Impact ] -> [ Collect Results ]
[ API Compat ] -> [ Collect Results ]
[ Migration ] -> [ Collect Results ]
[ MAJOR Detected ] -- spawn 3 agents --> [ User Impact ]
[ MAJOR Detected ] --> [ API Compat ]
[ MAJOR Detected ] --> [ Migration ]
[ Collect Results ] -> [ AskUserQuestion ] { border: double; }
```

</details>

**Task subagent prompts** (spawn in parallel):

1. **User Impact Analyst** (`subagent_type: "Explore"`):
   ```
   Analyze the breaking changes in commits since last tag. Identify:
   - Which user personas are affected (library consumers, CLI users, API clients)
   - Approximate usage scope (core feature vs edge case)
   - Available workarounds before upgrading
   Return a 2-3 sentence impact assessment.
   ```

2. **API Compatibility Analyst** (`subagent_type: "Explore"`):
   ```
   Review the breaking changes for API compatibility:
   - What specific signatures, behaviors, or contracts are changing
   - Whether the change could be made backwards-compatible with feature flags
   - If deprecation warnings could have preceded this break
   Return a 2-3 sentence compatibility assessment.
   ```

3. **Migration Strategist** (`subagent_type: "Explore"`):
   ```
   Assess the migration path for this breaking change:
   - Effort level for consumers to update (trivial/moderate/significant)
   - Whether a migration guide is needed in release notes
   - Suggested deprecation timeline if change could be phased
   Return a 2-3 sentence migration assessment.
   ```

#### Phase 3: User Confirmation (AskUserQuestion with multiSelect)

After collecting subagent analyses, present consolidated findings:

```yaml
AskUserQuestion:
  questions:
    - question: "MAJOR version bump (X.0.0) detected. How should we proceed?"
      header: "Breaking"
      multiSelect: false
      options:
        - label: "Proceed with MAJOR (Recommended)"
          description: "Release as X.0.0 - breaking change is intentional and necessary"
        - label: "Downgrade to MINOR"
          description: "Amend commits to remove BREAKING CHANGE - change can be backwards-compatible"
        - label: "Abort release"
          description: "Review commits before releasing - need to reconsider approach"
    - question: "Which mitigations should be included in release notes?"
      header: "Mitigations"
      multiSelect: true
      options:
        - label: "Migration guide"
          description: "Step-by-step instructions for updating consumer code"
        - label: "Deprecation notice"
          description: "Warning that old behavior will be removed in future version"
        - label: "Compatibility shim"
          description: "Temporary backwards-compat layer with deprecation warning"
```

#### Decision Tree

```
                           MAJOR Release Decision Tree

 ---------------------   NO       -------------------
| Proceed MINOR/PATCH | <------- |  MAJOR detected?  |
 ---------------------            -------------------
                                   |
                                   | YES
                                   v
                                 +-------------------+
                                 | Spawn 3 Subagents |
                                 +-------------------+
                                   |
                                   |
                                   v
 ---------------------   abort   +-------------------+  proceed    ---------------
|    Abort Release    | <------- |  AskUserQuestion  | ---------> | Proceed MAJOR |
 ---------------------           +-------------------+             ---------------
                                   |
                                   | downgrade
                                   v
                                 +-------------------+
                                 |  Downgrade MINOR  |
                                 +-------------------+
                                   |
                                   |
                                   v
                                 +-------------------+
                                 |   Amend Commits   |
                                 +-------------------+
```

<details>
<summary>graph-easy source</summary>

```
graph { label: "MAJOR Release Decision Tree"; flow: south; }

[ MAJOR detected? ] { shape: rounded; }
[ Proceed MINOR/PATCH ] { shape: rounded; }
[ Spawn 3 Subagents ]
[ AskUserQuestion ]
[ Proceed MAJOR ] { shape: rounded; }
[ Downgrade MINOR ]
[ Abort Release ] { shape: rounded; }
[ Amend Commits ]

[ MAJOR detected? ] -- NO --> [ Proceed MINOR/PATCH ]
[ MAJOR detected? ] -- YES --> [ Spawn 3 Subagents ]
[ Spawn 3 Subagents ] -> [ AskUserQuestion ]
[ AskUserQuestion ] -- proceed --> [ Proceed MAJOR ]
[ AskUserQuestion ] -- downgrade --> [ Downgrade MINOR ]
[ AskUserQuestion ] -- abort --> [ Abort Release ]
[ Downgrade MINOR ] -> [ Amend Commits ]
```

</details>

#### Example Output

```
╔══════════════════════════════════════════════════════════════════╗
║  🔴 MAJOR VERSION BUMP DETECTED                                   ║
╠══════════════════════════════════════════════════════════════════╣
║  Commits triggering MAJOR:                                        ║
║  • a1b2c3d feat!: change API to require authentication           ║
║  • e4f5g6h fix!: rename config option from 'timeout' to 'ttl'    ║
╠══════════════════════════════════════════════════════════════════╣
║  📊 MULTI-PERSPECTIVE ANALYSIS                                    ║
╠──────────────────────────────────────────────────────────────────╣
║  👥 User Impact: All API consumers affected. Core authentication ║
║     flow changes. No workaround - update required.               ║
║                                                                   ║
║  🔌 API Compat: Authorization header now mandatory. Could add    ║
║     optional fallback with deprecation warning for 1-2 releases. ║
║                                                                   ║
║  📋 Migration: Moderate effort - add API key to all calls.       ║
║     Migration guide recommended. 2-week notice suggested.        ║
╠══════════════════════════════════════════════════════════════════╣
║  Current: v2.4.1 → Proposed: v3.0.0                              ║
╚══════════════════════════════════════════════════════════════════╝
```

#### Configuration

To skip MAJOR confirmation (not recommended):

```yaml
# .releaserc.yml
# WARNING: Disables safety check - use only for automated pipelines
skipMajorConfirmation: true
```

**Default**: MAJOR confirmation is ENABLED. This skill will always prompt for breaking changes unless explicitly disabled.

### Examples

**Feature (MINOR)**:

```
feat: add BigQuery data source support
```

**Bug Fix (PATCH)**:

```
fix: correct timestamp parsing for UTC offsets
```

**Breaking Change (MAJOR)**:

```
feat!: change API to require authentication

BREAKING CHANGE: All API calls now require API key in Authorization header.
```

---

## Documentation Linking in Release Notes

Automatically include links to **all documentation changes** in release notes, with AI-friendly categorization.

### Quick Setup (Hardcoded Path)

Add to `.releaserc.yml` before `@semantic-release/changelog`:

```yaml
- - "@semantic-release/exec"
  - generateNotesCmd: "node plugins/itp/skills/semantic-release/scripts/generate-doc-notes.mjs ${lastRelease.gitTag}"
```

### What's Detected

The script categorizes all changed markdown files:

| Category             | Pattern                                  | Grouping                        |
| -------------------- | ---------------------------------------- | ------------------------------- |
| **ADRs**             | `docs/adr/YYYY-MM-DD-slug.md`            | Status table                    |
| **Design Specs**     | `docs/design/YYYY-MM-DD-slug/spec.md`    | List with change type           |
| **Skills**           | `plugins/*/skills/*/SKILL.md`            | Grouped by plugin (collapsible) |
| **Plugin READMEs**   | `plugins/*/README.md`                    | Simple list                     |
| **Skill References** | `plugins/*/skills/*/references/*.md`     | Grouped by skill (collapsible)  |
| **Commands**         | `plugins/*/commands/*.md`                | Grouped by plugin               |
| **Root Docs**        | `CLAUDE.md`, `README.md`, `CHANGELOG.md` | Simple list                     |
| **General Docs**     | `docs/*.md` (excluding adr/, design/)    | Simple list                     |

### How It Works

1. **Git diff detection**: All `.md` files changed since the last release tag
2. **Change type tracking**: Marks files as `new`, `updated`, `deleted`, or `renamed`
3. **Commit parsing**: References like `ADR: 2025-12-06-slug` in commit messages
4. **ADR-Design Spec coupling**: If one is changed, the corresponding pair is included

Full HTTPS URLs are generated (required for GitHub release pages).

See [Documentation Release Linking](./references/doc-release-linking.md) for detailed configuration.

---

## Quick Start

### Step 1: Verify Account (HTTPS-First)

**CRITICAL**: For multi-account GitHub setups, verify GH_TOKEN is set for the current directory.

**Quick verification** (2025-12-19+):

```bash
# Verify git remote is HTTPS
git remote get-url origin
# Expected: https://github.com/...

# Verify GH_TOKEN is set via mise [env]
gh api user --jq '.login'
# Expected: correct account for this directory
```

**If remote is SSH** (legacy):

```bash
# Convert to HTTPS
git-ssh-to-https
```

**If wrong account**:

Check mise [env] configuration:

```bash
# Verify mise config
mise env | grep GH_TOKEN
```

See [Authentication Guide](./references/authentication.md) for HTTPS-first setup.

### Step 2: Initialize Project

```bash
/usr/bin/env bash << 'CONFIG_EOF'
cd /path/to/project
# Environment-agnostic path
PLUGIN_DIR="${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/marketplaces/cc-skills/plugins/itp}"
"$PLUGIN_DIR/skills/semantic-release/scripts/init_project.sh" --user
# Or --org mycompany/semantic-release-config
# Or --inline
CONFIG_EOF
```

### Step 3: Run Release Locally

Follow the [Local Release Workflow](./references/local-release-workflow.md) for the complete 4-phase process (PREFLIGHT → SYNC → RELEASE → POSTFLIGHT).

**Quick commands**:

```bash
npm run release:dry   # Preview changes (no modifications)
npm run release       # Create release (auto-pushes via successCmd + postrelease)
```

**What happens automatically**:

1. Version bump determined from commits
2. `CHANGELOG.md` updated
3. Release commit + tag created
4. **Git push via successCmd** (belt-and-suspenders)
5. GitHub release created via API
6. **Tracking refs updated via postrelease**

**One-time setup (recommended for macOS)**:

```bash
# Install globally to avoid macOS Gatekeeper issues with npx
npm install -g semantic-release @semantic-release/changelog @semantic-release/git @semantic-release/github @semantic-release/exec

# Clear quarantine (required on macOS after install or node upgrade)
xattr -r -d com.apple.quarantine ~/.local/share/mise/installs/node/
```

> **Note**: Use `semantic-release` directly (not `npx semantic-release`) to avoid macOS Gatekeeper blocking `.node` native modules. See [Troubleshooting](./references/troubleshooting.md#macos-gatekeeper-blocks-node-files).

### Step 4: PyPI Publishing (Python Projects)

**For Python packages**: semantic-release handles versioning, use the [`pypi-doppler`](../pypi-doppler/SKILL.md) skill for local PyPI publishing.

**Quick setup**:

```bash
/usr/bin/env bash << 'SETUP_EOF'
# Install Doppler CLI for secure token management
brew install dopplerhq/cli/doppler

# Store token in Doppler (one-time)
doppler secrets set PYPI_TOKEN='your-pypi-token' --project claude-config --config prd

# Copy publish script from pypi-doppler skill (environment-agnostic)
PLUGIN_DIR="${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/marketplaces/cc-skills/plugins/itp}"
cp "$PLUGIN_DIR/skills/pypi-doppler/scripts/publish-to-pypi.sh" scripts/
chmod +x scripts/publish-to-pypi.sh

# After semantic-release creates GitHub release:
./scripts/publish-to-pypi.sh  # 30 seconds vs 3-5 minutes with GitHub Actions
SETUP_EOF
```

See [`pypi-doppler` skill](../pypi-doppler/SKILL.md) for complete workflow with CI detection guards.

### Python `__version__` Pattern

**Always use `importlib.metadata`** - never hardcode version strings:

```python
# __init__.py
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("your-package-name")
except PackageNotFoundError:
    __version__ = "0.0.0+dev"  # Development fallback
```

This reads from `pyproject.toml` at runtime, ensuring single source of truth. semantic-release updates `pyproject.toml` via `prepareCmd`, and `importlib.metadata` reads it at runtime - no manual sync required.

**Anti-pattern** (causes version drift):

```python
# ❌ BAD - requires manual sync with pyproject.toml
__version__ = "1.2.3"
```

See [Python Projects with Node.js semantic-release](./references/python-projects-nodejs-semantic-release.md) for complete Python automation guide.

### Step 5: GitHub Actions (Optional)

**Only if you want CI/CD backup** (not recommended as primary due to 2-5 minute delay):

Repository Settings → Actions → General → Workflow permissions → Enable "Read and write permissions"

---

## Common Pitfalls

### Dirty Working Directory

**Symptom**: After release, `git status` shows version files as modified with OLD versions.

**Cause**: Files were staged before release started. semantic-release commits from working copy, but git index cache may show stale state.

**Prevention**: Always clear git cache before checking status:

```bash
# Step 1: Refresh git index (automatic in npm run release)
git update-index --refresh -q || true

# Step 2: Check for uncommitted changes (modified, untracked, staged, deleted)
git status --porcelain
# Should output nothing

# If dirty, either:
git stash           # Stash changes
git commit -m "..."  # Commit changes
git checkout -- .   # Discard changes
```

**Recovery**: If you see stale versions after release:

```bash
git update-index --refresh
git status  # Should now show clean
```

**Automated guards**: The cc-skills `.releaserc.yml` includes:

- **verifyConditions preflight**: Clears git cache first, then blocks release if working directory is dirty
- **successCmd index refresh**: Automatically refreshes git index after push

### Pre-Release Checklist

Before running `npm run release`:

1. ✅ All changes committed
2. ✅ No staged files (`git diff --cached` is empty)
3. ✅ No untracked files in version-synced paths
4. ✅ Branch is up-to-date with remote

---

## Reference Documentation

For detailed information, see:

- [Authentication](./references/authentication.md) - **START HERE** - SSH keys, GitHub CLI web auth (avoid manual tokens)
- [Local Release Workflow](./references/local-release-workflow.md) - Step-by-step release process with issue resolution
- [Workflow Patterns](./references/workflow-patterns.md) - Personal, Team, and Standalone project patterns
- [Version Alignment](./references/version-alignment.md) - Git tags as SSoT, manifest patterns, runtime version access
- [2025 Updates](./references/2025-updates.md) - v25 changelog, Node.js 24+, OIDC trusted publishing, plugin versions
- [Python Projects with Node.js semantic-release](./references/python-projects-nodejs-semantic-release.md) - Complete guide for Python package automation with @semantic-release/exec
- [Rust Projects with release-plz](./references/rust-release-plz.md) - Rust-native release automation with cargo-rdme README SSoT
- [`pypi-doppler` skill](../pypi-doppler/SKILL.md) - Local PyPI publishing with Doppler credentials and CI detection guards
- [Monorepo Support](./references/monorepo-support.md) - pnpm/npm workspaces configuration
- [Troubleshooting](./references/troubleshooting.md) - Common issues and solutions
- [ADR Release Linking](./references/doc-release-linking.md) - Auto-link ADRs and Design Specs in release notes
- [Resources](./references/resources.md) - Scripts, templates, and asset documentation

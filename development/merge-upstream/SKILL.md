---
name: merge-upstream
description: Sync Azure Codex fork with OpenAI Codex upstream while preserving Azure features
---

# Merge Upstream Skill

This skill guides the process of syncing the Azure Codex fork with the upstream OpenAI Codex repository while preserving all Azure-specific features and customizations.

## Azure-Specific Features to Preserve

### Critical Components (Must Not Regress)

#### 1. Azure Authentication (`core/src/auth/`)
- `azure.rs` - Azure Entra ID authentication implementation
- `azure_config.rs` - Azure auth configuration (CLI, Managed Identity, Service Principal)
- Support for: Azure CLI, Managed Identity, Service Principal, Device Code Flow

#### 2. Azure Deployment Discovery (`core/src/azure/`)
- `deployments.rs` - Azure OpenAI deployment discovery
- `mod.rs` - Module exports
- Extracts account name from endpoint URL
- Discovers resource group automatically
- Converts deployments to `ModelPreset`

#### 3. Claude/Anthropic Support (`codex-api/src/`)
- `endpoint/anthropic.rs` - Anthropic endpoint handling
- `requests/anthropic.rs` - Request formatting for Anthropic API
- `sse/anthropic.rs` - SSE parsing for Claude responses
- Extended thinking mode support

#### 4. Model Family Detection (`core/src/models_manager/`)
- `model_family.rs` - GPT, Claude, and other model families
- `manager.rs` - Azure-aware model management
- `is_azure()` method for backend detection

#### 5. Configuration (`core/src/config/`)
- `azure_endpoint` field in config
- `azure_api_version` field
- `azure_auth` configuration
- Theme configuration (`tui_theme`)

#### 6. UI Improvements (`tui2/src/`)
- `theme.rs` - 7 configurable color themes
- `syntax_highlight.rs` - Syntect-based syntax highlighting
- `terminal_palette.rs` - Light/dark detection, `is_light_background()`
- `diff_render.rs` - Background colors for diffs
- `resume_picker.rs` - Fuzzy search with nucleo-matcher
- `chatwidget.rs` - Bash mode (`!` prefix), paste auto-attachment
- `bottom_pane/footer.rs` - Token display

#### 7. Branding (`branding/`)
- Azure Codex branding and naming

## Pre-Merge Checklist

```bash
# 1. Ensure working directory is clean
git status

# 2. Fetch latest upstream
git fetch upstream

# 3. Check divergence
git rev-list --left-right --count HEAD...upstream/main
# Output: <ahead> <behind>

# 4. Review upstream changes
git log --oneline HEAD..upstream/main

# 5. Check for potential conflicts in critical files
git diff upstream/main...HEAD --stat -- \
  codex-rs/core/src/auth/ \
  codex-rs/core/src/azure/ \
  codex-rs/core/src/models_manager/ \
  codex-rs/core/src/config/ \
  codex-rs/codex-api/src/
```

## Merge Process

### Option A: Merge (Recommended for Forks)

```bash
# Create a backup branch
git branch backup-before-upstream-merge

# Merge upstream
git merge upstream/main --no-edit

# If conflicts, resolve them (see Conflict Resolution below)
# Then continue:
git add .
git merge --continue
```

### Option B: Rebase (Cleaner History, More Risk)

```bash
# Only if you haven't pushed recently or are OK with force-push
git rebase upstream/main

# Resolve conflicts as they appear
git add <resolved-files>
git rebase --continue
```

### Option C: Selective Cherry-Picking (Recommended When Divergence is Large)

When there are many upstream commits and significant Azure modifications, cherry-picking "safe" commits avoids conflicts entirely. This approach was successfully used to sync 15 upstream commits without any conflicts.

#### Step 1: Identify Azure-Modified Files

```bash
# Get list of all files modified in Azure fork vs upstream
git diff --name-only upstream/main...HEAD > azure-modified-files.txt
wc -l azure-modified-files.txt  # Check count
```

#### Step 2: Find Safe Commits

A "safe" commit is one that doesn't touch any Azure-modified files:

```bash
# For each upstream commit, check if it touches Azure-modified files
for commit in $(git rev-list HEAD..upstream/main); do
    files=$(git diff-tree --no-commit-id --name-only -r $commit)
    safe=true
    for file in $files; do
        if grep -q "^$file$" azure-modified-files.txt; then
            safe=false
            break
        fi
    done
    if [ "$safe" = true ]; then
        echo "$commit $(git log --oneline -1 $commit)"
    fi
done
```

#### Step 3: Create Cherry-Pick Branch and Apply

```bash
# Create branch for cherry-picks
git checkout -b upstream-cherry-picks

# Cherry-pick safe commits (oldest first)
git cherry-pick <commit1> <commit2> ...

# Build and test
cargo build --release -p codex-cli
```

#### Step 4: Merge to Main

```bash
git checkout main
git merge upstream-cherry-picks
git push origin main
```

#### Known Dependency Issues

Some commits have hidden dependencies that cause build failures:

1. **otel/metrics commits**: Either include ALL or NONE
2. **config_requirements**: Type definitions may be in other commits
3. **sandbox changes**: May import types from related commits

**Rule**: If a cherry-pick fails to build, check if it depends on another upstream commit.

## Conflict Resolution Priority

When resolving conflicts, prioritize in this order:

### 1. Keep Azure Features (Priority: CRITICAL)
- Always preserve Azure auth code
- Always preserve Azure deployment discovery
- Always preserve Claude/Anthropic support
- Always preserve Azure config fields

### 2. Accept Upstream Improvements (Priority: HIGH)
- Bug fixes
- Performance improvements
- Security patches
- New features that don't conflict

### 3. Merge Both (Priority: MEDIUM)
- Code that can coexist
- Additive changes from both sides

### 4. Azure UI Takes Precedence (Priority: HIGH)
- Theme system
- Syntax highlighting
- Visual improvements

## Common Conflict Patterns

### Pattern 1: models_manager/manager.rs
Upstream often changes model handling. Preserve:
- `with_azure_endpoint()` method
- `is_azure()` method
- Azure-specific model listing

### Pattern 2: config/types.rs
Upstream may add new config fields. Preserve:
- `azure_endpoint: Option<String>`
- `azure_api_version: String`
- `azure_auth: Option<AzureAuthConfig>`
- `theme: Option<String>` in Tui struct

### Pattern 3: codex-api/src/auth.rs
Upstream changes auth handling. Preserve:
- Azure credential provider chain
- Azure token acquisition

## Post-Merge Testing

### 1. Compilation Check
```bash
cargo check -p codex-core -p codex-tui2 -p codex-cli
```

### 2. Full Test Suite
```bash
cargo test --workspace
```

### 3. Azure OpenAI Test (GPT Models)
```bash
export AZURE_CODEX_HOME="/path/to/test-config"
./target/debug/codex-exec --skip-git-repo-check -m "gpt-5.2" "Say hello"
```

### 4. Azure AI Services Test (Claude Models)
```bash
./target/debug/codex-exec --skip-git-repo-check -m "claude-opus-4-5" "Say hello"
```

### 5. UI Feature Verification
- Run TUI and verify:
  - [ ] Theme switching works (`/theme`)
  - [ ] Syntax highlighting in diffs
  - [ ] Background colors on diff lines
  - [ ] Token display in footer
  - [ ] Bash mode (`!ls` works)
  - [ ] Session picker fuzzy search

## Rollback Procedure

If merge causes issues:

```bash
# Reset to backup
git reset --hard backup-before-upstream-merge

# Or reset to origin
git reset --hard origin/main
```

## Commit Message Format

```
chore: sync with upstream codex

Merge upstream/main (commit <sha>) into azure-codex main.

Upstream changes:
- <list notable upstream changes>

Preserved Azure features:
- Azure Entra ID authentication
- Claude/Anthropic model support
- Enhanced UI (themes, syntax highlighting)
- Azure deployment discovery

Conflicts resolved:
- <list files with conflicts and resolution approach>
```

## Automation Script

Save as `scripts/sync-upstream.sh`:

```bash
#!/bin/bash
set -e

echo "=== Azure Codex Upstream Sync ==="

# Fetch upstream
echo "Fetching upstream..."
git fetch upstream

# Show divergence
echo "Divergence from upstream/main:"
git rev-list --left-right --count HEAD...upstream/main

# Show upstream commits
echo "New upstream commits:"
git log --oneline HEAD..upstream/main

# Confirm
read -p "Proceed with merge? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

# Create backup
echo "Creating backup branch..."
git branch -f backup-before-upstream-merge

# Merge
echo "Merging upstream/main..."
if git merge upstream/main --no-edit; then
    echo "Merge successful!"
else
    echo "Conflicts detected. Please resolve and run:"
    echo "  git add ."
    echo "  git merge --continue"
    exit 1
fi

# Run checks
echo "Running compilation check..."
cargo check -p codex-core -p codex-tui2 -p codex-cli

echo "Running tests..."
cargo test --workspace

echo "=== Sync Complete ==="
```

## Files Never Modified by Upstream

These Azure-specific files should never have conflicts:
- `codex-rs/core/src/auth/azure.rs`
- `codex-rs/core/src/auth/azure_config.rs`
- `codex-rs/core/src/azure/`
- `codex-rs/codex-api/src/endpoint/anthropic.rs`
- `codex-rs/codex-api/src/requests/anthropic.rs`
- `codex-rs/codex-api/src/sse/anthropic.rs`
- `codex-rs/tui2/src/syntax_highlight.rs`
- `.codex/skills/azure-openai/`
- `CLAUDE.md`
- `AZURE_FORK_IMPLEMENTATION_PLAN.md`

## Output Format

When performing a merge, report:

```
## Upstream Sync Summary

### Commits Merged
- <count> new commits from upstream

### Key Changes
- <list notable changes>

### Conflicts Resolved
- <file>: <resolution approach>

### Test Results
- Compilation: PASS/FAIL
- Unit Tests: PASS/FAIL (<count> tests)
- Azure OpenAI: PASS/FAIL
- Azure AI Services: PASS/FAIL
- UI Features: PASS/FAIL

### Notes
- <any issues or observations>
```

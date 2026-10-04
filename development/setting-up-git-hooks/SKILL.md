---
name: setting-up-git-hooks
description: Configures git hooks for automated testing, linting, and quality enforcement. Use when initializing projects, establishing quality gates, or preventing commit/push errors.
---

# Setup Git Hooks

## Purpose

This skill sets up Git hooks to automatically enforce testing and code quality standards before commits and pushes. It supports two installation patterns:

- **Pattern A (Default)**: Hooks installed directly to `.git/hooks/` with configuration in `.wrangler/config/hooks-config.json`
- **Pattern B**: Version-controlled hooks in `.wrangler/config/git-hooks/` with install script for team synchronization

## When to Use

- Setting up a new project with test enforcement
- Adding hooks to an existing project
- Migrating from other hook managers (Husky, pre-commit)
- Configuring CI-like checks locally

## Setup Workflow

### Phase 1: Environment Verification

**Step 1: Verify Git Repository**

```bash
# Check if we're in a git repository
git rev-parse --show-toplevel

# Check existing hooks
ls -la .git/hooks/ 2>/dev/null | head -10

# Check for existing wrangler hooks config
[ -f .wrangler/config/hooks-config.json ] && echo "Existing config found" || echo "No existing config"
```

If not in a git repository, inform user and exit.

**Step 2: Check for Existing Hook Managers**

```bash
# Check for Husky
[ -d .husky ] && echo "Husky detected" || true
[ -f package.json ] && grep -q '"husky"' package.json && echo "Husky in package.json" || true

# Check for pre-commit framework
[ -f .pre-commit-config.yaml ] && echo "pre-commit framework detected" || true

# Check for existing custom hooks
for hook in pre-commit pre-push commit-msg; do
    [ -f .git/hooks/$hook ] && echo "Existing $hook hook found" || true
done
```

If existing hook manager found, ask user how to proceed:
- Migrate from existing (backup and replace)
- Skip setup (user will handle manually)
- Continue anyway (may conflict)

### Phase 2: Project Detection

### Special Case: Empty Project or No Tests Detected

If the skill detects an empty project or no test framework:

**Detection criteria:**
- No package.json, pyproject.toml, go.mod, Cargo.toml, etc.
- No test files found (*.test.*, *_test.*, tests/ directory)
- No test scripts in package.json

**Graceful handling:**

1. **Populate TESTING.md** with placeholder content:

   TESTING.md should already exist from governance initialization. Update status section:

   ```markdown
   **Status:** No tests configured yet
   ```

   If TESTING.md doesn't exist, create it from initializing-governance template first.

2. **Create stub hooks-config.json:**
   ```json
   {
     "version": "1.0.0",
     "createdAt": "2026-01-21T...",
     "testCommand": "",
     "note": "No tests detected. Run /wrangler:updating-git-hooks after adding tests.",
     "protectedBranches": ["main", "master", "feature/*", "fix/*"],
     "skipDocsOnlyChanges": true,
     "docsPatterns": ["*.md", "docs/**/*", ".wrangler/memos/**/*"],
     "bypassEnvVar": "WRANGLER_SKIP_HOOKS",
     "setupComplete": false
   }
   ```

   Note: File should be created at `.wrangler/config/hooks-config.json`

3. **Install bypass-only hooks:**
   - Hooks check `setupComplete` flag in config
   - If false, log message and exit 0 (allow all commits/pushes)
   - If true, run normal test enforcement

4. **Inform user:**
   ```
   Git hooks installed (inactive - no tests detected)

   Hooks are installed but will not enforce testing until you:
   1. Add tests to your project
   2. Run: /wrangler:updating-git-hooks

   Created:
   - .wrangler/TESTING.md (placeholder)
   - .wrangler/config/hooks-config.json (stub configuration)
   - .git/hooks/pre-commit (bypass mode)
   - .git/hooks/pre-push (bypass mode)
   ```

**Why this works:**
- No broken setup (hooks exist but don't fail)
- Clear messaging about what to do next
- Easy to activate later
- TESTING.md always exists (no orphaned references)

**Step 3: Detect Project Type**

Use Bash to identify project language/framework:

```bash
# JavaScript/TypeScript
[ -f package.json ] && echo "javascript"

# Python
[ -f setup.py ] || [ -f pyproject.toml ] || [ -f requirements.txt ] && echo "python"

# Go
[ -f go.mod ] && echo "go"

# Rust
[ -f Cargo.toml ] && echo "rust"

# Java
[ -f pom.xml ] || [ -f build.gradle ] && echo "java"
```

**Step 4: Detect Existing Test/Format/Lint Commands**

For JavaScript projects:
```bash
# Read package.json scripts
cat package.json | grep -E '"(test|lint|format)"' || true
```

For Python projects:
```bash
# Check for common test runners
[ -f pytest.ini ] || [ -f pyproject.toml ] && grep -q pytest pyproject.toml && echo "pytest"
[ -f setup.cfg ] && grep -q flake8 setup.cfg && echo "flake8"
```

For Go projects:
```bash
# Go has standard commands
echo "go test ./..."
echo "go fmt ./..."
```

### Phase 3: Interactive Configuration

**Step 5: Ask User for Configuration**

Use multiple AskUserQuestion calls to gather configuration:

**Question 1: Installation Pattern**
```typescript
AskUserQuestion({
  questions: [{
    question: "Which hook installation pattern would you prefer?",
    header: "Installation Pattern",
    options: [
      {
        label: "Pattern A: Direct installation (Recommended)",
        description: "Hooks in .git/hooks/, config in .wrangler/config/hooks-config.json"
      },
      {
        label: "Pattern B: Version-controlled",
        description: "Hooks in .wrangler/config/git-hooks/, install script for team sync"
      }
    ],
    multiSelect: false
  }]
})
```

**Question 2: Test Command**
```typescript
// Show detected commands as suggestions
AskUserQuestion({
  questions: [{
    question: "What command runs your full test suite?",
    header: "Test Command",
    options: [
      { label: "[detected command]", description: "Detected from project files" },
      { label: "Custom command", description: "I'll specify my own" }
    ],
    multiSelect: false
  }]
})
```

If "Custom command" selected, ask user to type the command.

**Question 3: Unit Test Command (Optional)**
```typescript
AskUserQuestion({
  questions: [{
    question: "Do you have a separate command for fast unit tests? (for pre-commit)",
    header: "Unit Tests",
    options: [
      { label: "Same as full tests", description: "Use full test command" },
      { label: "[suggested fast command]", description: "Faster subset of tests" },
      { label: "Custom command", description: "I'll specify my own" },
      { label: "Skip unit tests", description: "Don't run tests in pre-commit" }
    ],
    multiSelect: false
  }]
})
```

**Question 4: Format Command (Optional)**
```typescript
AskUserQuestion({
  questions: [{
    question: "What command formats your code? (auto-fix and re-stage)",
    header: "Formatter",
    options: [
      { label: "[detected command]", description: "Detected from project files" },
      { label: "Custom command", description: "I'll specify my own" },
      { label: "Skip formatting", description: "Don't auto-format in pre-commit" }
    ],
    multiSelect: false
  }]
})
```

**Question 5: Lint Command (Optional)**
```typescript
AskUserQuestion({
  questions: [{
    question: "What command lints your code?",
    header: "Linter",
    options: [
      { label: "[detected command]", description: "Detected from project files" },
      { label: "Custom command", description: "I'll specify my own" },
      { label: "Skip linting", description: "Don't lint in pre-commit" }
    ],
    multiSelect: false
  }]
})
```

**Question 6: Protected Branches**
```typescript
AskUserQuestion({
  questions: [{
    question: "Which branches should require full tests before push?",
    header: "Protected Branches",
    options: [
      { label: "Default (main, master, develop, release/*, hotfix/*)", description: "Standard Git Flow branches" },
      { label: "Just main/master", description: "Only primary branches" },
      { label: "Custom patterns", description: "I'll specify my own" }
    ],
    multiSelect: false
  }]
})
```

**Question 7: Commit Message Validation (Optional)**
```typescript
AskUserQuestion({
  questions: [{
    question: "Enable commit message format validation?",
    header: "Commit Messages",
    options: [
      { label: "Yes - Conventional Commits", description: "feat:, fix:, docs:, etc." },
      { label: "No", description: "Allow any commit message format" }
    ],
    multiSelect: false
  }]
})
```

### Phase 4: Configuration Generation

**Step 6: Generate hooks-config.json**

Create the configuration file with user's answers:

```bash
mkdir -p .wrangler/config
```

Use Write tool to create `.wrangler/config/hooks-config.json`:

```json
{
  "$schema": "https://wrangler.dev/schemas/hooks-config.json",
  "version": "1.0.0",
  "createdAt": "[ISO timestamp]",
  "projectType": "[detected type]",
  "testCommand": "[user's test command]",
  "unitTestCommand": "[user's unit test command or null]",
  "formatCommand": "[user's format command or null]",
  "lintCommand": "[user's lint command or null]",
  "protectedBranches": ["main", "master", "develop", "release/*", "hotfix/*"],
  "skipDocsOnlyChanges": true,
  "docsPatterns": ["*.md", "*.txt", "*.rst", "docs/*", "README*", "LICENSE*", "CHANGELOG*"],
  "enableCommitMsgValidation": [true/false],
  "bypassEnvVar": "WRANGLER_SKIP_HOOKS",
  "pattern": "[A or B]"
}
```

### Phase 5: Hook Installation

**Step 7: Install Hooks (Pattern A)**

If Pattern A selected:

```bash
# Backup existing hooks
if [ -f .git/hooks/pre-commit ] || [ -f .git/hooks/pre-push ]; then
    mkdir -p .git/hooks.backup
    cp .git/hooks/pre-commit .git/hooks.backup/ 2>/dev/null || true
    cp .git/hooks/pre-push .git/hooks.backup/ 2>/dev/null || true
    cp .git/hooks/commit-msg .git/hooks.backup/ 2>/dev/null || true
    echo "Existing hooks backed up to .git/hooks.backup/"
fi
```

Use Read tool to read template files from wrangler skills directory:
- `skills/setting-up-git-hooks/templates/pre-commit.template.sh`
- `skills/setting-up-git-hooks/templates/pre-push.template.sh`
- `skills/setting-up-git-hooks/templates/commit-msg.template.sh` (if enabled)

Use string replacement to substitute placeholders:
- `{{TEST_COMMAND}}` -> user's test command
- `{{UNIT_TEST_COMMAND}}` -> user's unit test command
- `{{FORMAT_COMMAND}}` -> user's format command
- `{{LINT_COMMAND}}` -> user's lint command
- `{{PROTECTED_BRANCHES}}` -> user's protected branches
- `{{DOCS_PATTERNS}}` -> docs patterns

Use Write tool to save hooks to `.git/hooks/`:
- `.git/hooks/pre-commit`
- `.git/hooks/pre-push`
- `.git/hooks/commit-msg` (if enabled)

Make hooks executable:
```bash
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-push
[ -f .git/hooks/commit-msg ] && chmod +x .git/hooks/commit-msg
```

**Step 8: Install Hooks (Pattern B)**

If Pattern B selected:

```bash
# Create version-controlled hooks directory
mkdir -p .wrangler/config/git-hooks
```

Use Write tool to save hooks to `.wrangler/config/git-hooks/`:
- `.wrangler/config/git-hooks/pre-commit`
- `.wrangler/config/git-hooks/pre-push`
- `.wrangler/config/git-hooks/commit-msg` (if enabled)

Use Write tool to create install script at `scripts/install-hooks.sh`:
(Copy from `skills/setting-up-git-hooks/templates/install-hooks.sh`)

Make files executable:
```bash
chmod +x .wrangler/config/git-hooks/pre-commit
chmod +x .wrangler/config/git-hooks/pre-push
[ -f .wrangler/config/git-hooks/commit-msg ] && chmod +x .wrangler/config/git-hooks/commit-msg
chmod +x scripts/install-hooks.sh
```

Run install script:
```bash
./scripts/install-hooks.sh
```

### Phase 6: Documentation Installation

**Step 9: Install PR Template**

Create PR template in user's project:

```bash
mkdir -p .github
```

Create PR template (git hooks specific):
- `.github/pull_request_template.md` (copy from `skills/setting-up-git-hooks/templates/pull_request_template.md`)

**Note on other templates**: Security checklist and Definition of Done templates remain in their skill directories:
- Security checklist: `skills/initializing-governance/templates/SECURITY_CHECKLIST.md`
- Definition of Done: `skills/initializing-governance/templates/DEFINITION_OF_DONE.md`

These are referenced directly from skills, not copied to project directories.

**Step 10: Populate TESTING.md**

TESTING.md is created by initializing-governance skill. This step populates it with git hooks configuration.

If `.wrangler/TESTING.md` doesn't exist (governance not initialized), create it from initializing-governance template with user's configuration:

```bash
# Copy template from initializing-governance
cp skills/initializing-governance/templates/TESTING.md .wrangler/TESTING.md
```

Then populate all placeholders with detected/configured values.

### Phase 7: Verification and Summary

**Step 11: Verify Installation**

```bash
# Verify hooks are installed and executable
echo "=== Hook Installation Verification ==="
for hook in pre-commit pre-push commit-msg; do
    if [ -f .git/hooks/$hook ]; then
        if [ -x .git/hooks/$hook ]; then
            echo "[OK] $hook installed and executable"
        else
            echo "[WARN] $hook installed but not executable"
        fi
    else
        echo "[SKIP] $hook not installed"
    fi
done

# Verify config file

## References

For detailed information, see:

- `references/detailed-guide.md` - Complete workflow details, examples, and troubleshooting

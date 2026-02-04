---
name: husky-hooks-config
description: Husky git hooks configuration with smart auto-detection for sensitive files, fail-fast execution, auto-fix workflows, and CI detection. Includes 5 required standards (smart .npmrc detection for multi-mono repos, set -e for fail-fast, pre-commit auto-fix with prettier:fix and lint:fix, pre-push validation with time tracking, clear emoji-enhanced output). Use when creating or auditing .husky/pre-commit and .husky/pre-push hooks.
---

# Husky Git Hooks Configuration Skill

This skill provides Husky pre-commit and pre-push hook templates and validation logic for automated code quality enforcement.

## Purpose

Manage Husky git hooks configuration to:

- Block sensitive files from commits (`.env*`, `.npmrc` with smart detection)
- Auto-fix code formatting and linting before commits
- Validate code quality before pushes
- Support CI environment detection
- Enable fail-fast execution with clear error messages
- Track execution time for performance monitoring

## Usage

This skill is invoked by the `husky-agent` when:

- Creating new Husky hook files
- Auditing existing git hook configurations
- Validating hooks against standards

## Templates

Standard templates are located at:

```
templates/pre-commit.template.sh     # Pre-commit hook with auto-fix
templates/pre-push.template.sh       # Pre-push hook with validation
```

## The 5 Husky Hook Standards

### Rule 1: Smart Auto-Detection for Sensitive Files

**Pre-commit must intelligently block sensitive files:**

**Multi-mono repo detection:**

```bash
# Detect if this is multi-mono library repo
if [ -f "scripts/sync-ms-command.sh" ]; then
  IS_MULTI_MONO=true
fi
```

**Blocking logic:**

- **Multi-mono repos**: Allow root `.npmrc` (registry only), block subdirectory `.npmrc`
- **Other repos**: Block ALL `.npmrc` files including root
- **All repos**: Always block `.env*` files

**Validation:**

```bash
# Check for smart detection logic
grep -q "IS_MULTI_MONO" .husky/pre-commit
grep -q "scripts/sync-ms-command.sh" .husky/pre-commit

# Check for sensitive file patterns
grep -q "\.env" .husky/pre-commit
grep -q "\.npmrc" .husky/pre-commit
```

### Rule 2: Fail-Fast Execution

Both hooks must use `set -e` to exit immediately on errors:

```bash
#!/bin/sh
set -e  # Exit immediately if a command exits with non-zero status
```

**Validation:**

- Check shebang is `#!/bin/sh`
- Verify `set -e` is present near top of file

### Rule 3: Pre-Commit Auto-Fix Workflow

**Required steps in order:**

1. Block sensitive files (smart detection)
2. Run `pnpm run prettier:fix` (auto-format)
3. Run `pnpm run lint:fix` (auto-fix linting)
4. Auto-add fixed files with `git add -u`

**Validation:**

```bash
# Check required steps exist in order
grep -n "prettier:fix" .husky/pre-commit
grep -n "lint:fix" .husky/pre-commit
grep -n "git add -u" .husky/pre-commit

# Verify package.json has required scripts
jq '.scripts | has("prettier:fix")' package.json
jq '.scripts | has("lint:fix")' package.json
```

### Rule 4: Pre-Push Validation Workflow

**Required steps in order:**

1. CI detection and skip logic
2. Time tracking start (`START_TIME`)
3. Run `pnpm run prettier` (check only, no fix)
4. Run `pnpm run lint` (check only, no fix)
5. Run `pnpm run lint:tsc` (TypeScript type checking)
6. Run `pnpm run test:unit` (unit tests)
7. Time tracking end and duration display

**CI Detection:**

```bash
# Skip in CI environments
if [ -n "$CI" ] || [ -n "$GITHUB_ACTIONS" ] || [ -n "$GITLAB_CI" ]; then
  echo "⏭️  Skipping pre-push checks in CI environment"
  exit 0
fi
```

**Time Tracking:**

```bash
START_TIME=$(date +%s)
# ... run checks ...
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
echo "✅ All checks passed in ${DURATION}s"
```

**Validation:**

```bash
# Check CI detection
grep -q "CI" .husky/pre-push
grep -q "GITHUB_ACTIONS" .husky/pre-push

# Check time tracking
grep -q "START_TIME" .husky/pre-push
grep -q "DURATION" .husky/pre-push

# Check required steps
grep -q "prettier" .husky/pre-push
grep -q "lint" .husky/pre-push
grep -q "lint:tsc" .husky/pre-push
grep -q "test:unit" .husky/pre-push

# Verify package.json has required scripts
jq '.scripts | has("prettier")' package.json
jq '.scripts | has("lint")' package.json
jq '.scripts | has("lint:tsc")' package.json
jq '.scripts | has("test:unit")' package.json
```

### Rule 5: Clear Step-by-Step Output

Both hooks must provide clear, emoji-enhanced output:

**Pre-commit:**

```bash
echo "🔒 Checking for sensitive files..."
echo "✨ Running Prettier..."
echo "🔍 Running ESLint..."
echo "✅ Pre-commit checks passed"
```

**Pre-push:**

```bash
echo "🚀 Running pre-push checks..."
echo "1️⃣ Prettier check..."
echo "2️⃣ ESLint check..."
echo "3️⃣ TypeScript type check..."
echo "4️⃣ Unit tests..."
echo "✅ All checks passed in ${DURATION}s"
```

**Validation:**

- Check for emoji usage in output
- Verify numbered steps in pre-push
- Confirm helpful error messages present

## Validation

To validate Husky hook configuration:

1. Check that `.husky/pre-commit` exists and is executable
2. Check that `.husky/pre-push` exists and is executable
3. Read both hook files
4. Validate against 5 standards
5. Verify package.json has all required scripts
6. Test hooks work correctly
7. Report violations

### Validation Approach

```bash
# Check hooks exist and are executable
[ -f ".husky/pre-commit" ] && [ -x ".husky/pre-commit" ] || echo "VIOLATION: pre-commit missing or not executable"
[ -f ".husky/pre-push" ] && [ -x ".husky/pre-push" ] || echo "VIOLATION: pre-push missing or not executable"

# Rule 1: Check smart detection
grep -q "IS_MULTI_MONO" .husky/pre-commit || echo "VIOLATION: Missing smart auto-detection"

# Rule 2: Check fail-fast
grep -q "^set -e" .husky/pre-commit || echo "VIOLATION: pre-commit missing set -e"
grep -q "^set -e" .husky/pre-push || echo "VIOLATION: pre-push missing set -e"

# Rule 3: Check pre-commit steps
grep -q "prettier:fix" .husky/pre-commit || echo "VIOLATION: Missing prettier:fix"
grep -q "lint:fix" .husky/pre-commit || echo "VIOLATION: Missing lint:fix"
grep -q "git add -u" .husky/pre-commit || echo "VIOLATION: Missing git add -u"

# Rule 4: Check pre-push steps
grep -q "CI" .husky/pre-push || echo "VIOLATION: Missing CI detection"
grep -q "START_TIME" .husky/pre-push || echo "VIOLATION: Missing time tracking"
grep -q "test:unit" .husky/pre-push || echo "VIOLATION: Missing test:unit"

# Rule 5: Check output clarity
grep -q "🔒\|🚀\|✅" .husky/pre-commit || echo "VIOLATION: Missing emoji output"
```

## Repository Type Considerations

- **Consumer Repos**: Strict enforcement - hooks must match templates exactly
- **Library Repos**: May have additional hooks or custom logic (intentional differences allowed)
- **Multi-mono Library**: Special logic for `.npmrc` handling (allow root, block subdirectories)

## Best Practices

1. Always create both hooks (pre-commit and pre-push)
2. Make hooks executable (`chmod +x`)
3. Use fail-fast execution (`set -e`)
4. Provide clear, step-by-step output
5. Test hooks after creation
6. Verify all required scripts exist in package.json
7. Re-audit after making changes
8. Respect library repo differences

## Integration

This skill integrates with:

- Repository type provided via `scope` parameter. If not provided, use `/skill scope-check`
- `/skill audit-workflow` - Bi-directional comparison workflow
- `/skill remediation-options` - Conform/Update/Ignore choices
- `prettier-agent` - For prettier:fix and prettier scripts
- `eslint-agent` - For lint:fix and lint scripts
- `typescript-agent` - For lint:tsc script
- `vitest-agent` - For test:unit script

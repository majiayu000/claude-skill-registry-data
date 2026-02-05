---
name: setup-cdk-quality
description: Use when setting up code quality enforcement - configures linting, formatting, pre-commit hooks, CI workflows, and review checklists with advisory/soft/hard enforcement levels
---

# Setup CDK Quality

## Overview

Code quality enforcement for Claude-assisted development. Configures linting, formatting, testing, and review automation with configurable enforcement levels.

## When to Use

- Setting up quality gates for a project
- User asks about linting, formatting, or CI
- Part of `setup-claude-dev-kit` full bundle
- Enforcing code standards across a team

## Quick Reference

| Component | Location |
|-----------|----------|
| Config | `.cdk-quality.json` |
| Pre-commit | `.husky/` or `.git/hooks/` |
| CI Workflows | `.github/workflows/` |
| Review Checklist | `.claude/commands/review.md` |

## Enforcement Levels

| Level | Behavior | Use Case |
|-------|----------|----------|
| **advisory** | Warn only, never block | Learning, exploration |
| **soft** | Block on commit, bypass with `--no-verify` | Development |
| **hard** | Block everywhere, no bypass | Production, CI |

## Installation Steps

### 1. Create Quality Config

Create `.cdk-quality.json` in project root:

```json
{
  "version": "1.0",
  "enforcement": "soft",
  "rules": {
    "lint": true,
    "format": true,
    "typecheck": true,
    "test": false,
    "secrets": true
  },
  "ignore": [
    "node_modules",
    "dist",
    "build",
    ".git"
  ]
}
```

### 2. Detect Project Type

```bash
detect_quality_tools() {
  if [ -f "package.json" ]; then
    # Node.js project
    if grep -q '"eslint"' package.json; then
      echo "eslint"
    fi
    if grep -q '"prettier"' package.json; then
      echo "prettier"
    fi
    if grep -q '"typescript"' package.json; then
      echo "tsc"
    fi
    if grep -q '"vitest"\|"jest"' package.json; then
      echo "test"
    fi
  elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
    # Python project
    echo "ruff black mypy pytest"
  elif [ -f "go.mod" ]; then
    echo "gofmt golint go-test"
  elif [ -f "Cargo.toml" ]; then
    echo "cargo-fmt cargo-clippy cargo-test"
  fi
}
```

### 3. Install Pre-commit Hooks

**For Node.js projects (using Husky):**

```bash
# Install husky
npm install --save-dev husky

# Initialize
npx husky init

# Create pre-commit hook
cat > .husky/pre-commit << 'EOF'
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# Load CDK quality config
if [ -f ".cdk-quality.json" ]; then
  ENFORCEMENT=$(cat .cdk-quality.json | grep -o '"enforcement"[^,]*' | cut -d'"' -f4)
else
  ENFORCEMENT="soft"
fi

# Run checks based on config
run_check() {
  local name=$1
  local cmd=$2

  echo "Running $name..."
  if ! $cmd; then
    if [ "$ENFORCEMENT" = "hard" ]; then
      echo "ERROR: $name failed (hard enforcement)"
      exit 1
    elif [ "$ENFORCEMENT" = "soft" ]; then
      echo "ERROR: $name failed (use --no-verify to bypass)"
      exit 1
    else
      echo "WARNING: $name failed (advisory mode)"
    fi
  fi
}

# Lint
if command -v eslint &>/dev/null; then
  run_check "ESLint" "npx eslint --max-warnings=0 ."
fi

# Format check
if command -v prettier &>/dev/null; then
  run_check "Prettier" "npx prettier --check ."
fi

# Type check
if [ -f "tsconfig.json" ]; then
  run_check "TypeScript" "npx tsc --noEmit"
fi

echo "Pre-commit checks passed!"
EOF

chmod +x .husky/pre-commit
```

**For Python projects:**

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-yaml
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: detect-private-key
EOF

pre-commit install
```

### 4. Secret Detection Hook

Add to pre-commit:

```bash
# Check for secrets/credentials
check_secrets() {
  local patterns=(
    'password\s*='
    'api_key\s*='
    'secret\s*='
    'AWS_ACCESS_KEY'
    'PRIVATE_KEY'
    '-----BEGIN RSA'
    '-----BEGIN OPENSSH'
  )

  local found=false
  for pattern in "${patterns[@]}"; do
    if git diff --cached --name-only | xargs grep -lE "$pattern" 2>/dev/null; then
      echo "WARNING: Potential secret found matching: $pattern"
      found=true
    fi
  done

  if $found; then
    echo ""
    echo "Review the files above for secrets before committing."
    return 1
  fi
}
```

### 5. GitHub Actions CI Workflow

Create `.github/workflows/quality.yml`:

```yaml
name: Quality Checks

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Format check
        run: npm run format:check

      - name: Type check
        run: npm run typecheck

      - name: Test
        run: npm test

      - name: Build
        run: npm run build
```

**Python variant:**

```yaml
name: Quality Checks

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install ruff mypy pytest

      - name: Lint
        run: ruff check .

      - name: Format check
        run: ruff format --check .

      - name: Type check
        run: mypy .

      - name: Test
        run: pytest
```

### 6. Code Review Checklist

Create `.claude/commands/quality-review.md`:

```markdown
Perform a quality review of the changes:

## Checklist

### Code Quality
- [ ] No unused variables or imports
- [ ] No commented-out code
- [ ] Functions are reasonably sized (<50 lines)
- [ ] No magic numbers (use constants)
- [ ] Error handling is appropriate

### Security
- [ ] No hardcoded secrets or credentials
- [ ] User input is validated/sanitized
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Sensitive data is not logged

### Performance
- [ ] No N+1 query patterns
- [ ] Large loops are optimized
- [ ] No memory leaks (event listeners, subscriptions)
- [ ] Expensive operations are cached where appropriate

### Testing
- [ ] New code has tests
- [ ] Edge cases are covered
- [ ] Tests are deterministic (no flaky tests)

### Documentation
- [ ] Complex logic is commented
- [ ] Public APIs are documented
- [ ] README updated if needed

Provide specific feedback with file:line references.
```

### 7. Configure Package Scripts

Add to `package.json`:

```json
{
  "scripts": {
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "typecheck": "tsc --noEmit",
    "quality": "npm run lint && npm run format:check && npm run typecheck",
    "quality:fix": "npm run lint:fix && npm run format"
  }
}
```

## Verification

```bash
# Check config exists
[ -f .cdk-quality.json ] && echo "Quality config exists"

# Check hooks installed
[ -f .husky/pre-commit ] && echo "Pre-commit hook installed"

# Check CI workflow
[ -f .github/workflows/quality.yml ] && echo "CI workflow configured"

# Test hooks work
git stash
echo "test" > /tmp/test.txt
git add /tmp/test.txt
git commit --dry-run -m "test: verify hooks" && echo "Hooks working"
git stash pop
```

## Adaptation Mode

When existing quality setup detected:

1. **Detect existing tools:**
```bash
# Check for existing linters
[ -f .eslintrc* ] && echo "ESLint configured"
[ -f .prettierrc* ] && echo "Prettier configured"
[ -f .pre-commit-config.yaml ] && echo "pre-commit configured"
```

2. **Merge approach:**
- Don't overwrite existing configs
- Add CDK rules alongside existing
- Offer to enhance, not replace

3. **Backup existing:**
```bash
mkdir -p ~/.claude-dev-kit/backups/$(date +%Y-%m-%d)
cp .eslintrc* ~/.claude-dev-kit/backups/$(date +%Y-%m-%d)/ 2>/dev/null
```

## Common Issues

| Issue | Fix |
|-------|-----|
| Hooks not running | Check husky installation, run `npx husky install` |
| CI failing but local passes | Ensure same Node/Python versions |
| Too many lint errors | Start with `advisory` level, fix incrementally |
| Format conflicts | Ensure editor uses same Prettier config |
| Secrets false positive | Add pattern to `.cdk-quality.json` ignore |

## Enforcement Recipes

### Strict Team Setup
```json
{
  "enforcement": "hard",
  "rules": {
    "lint": true,
    "format": true,
    "typecheck": true,
    "test": true,
    "secrets": true
  }
}
```

### Solo Developer Setup
```json
{
  "enforcement": "soft",
  "rules": {
    "lint": true,
    "format": true,
    "typecheck": true,
    "test": false,
    "secrets": true
  }
}
```

### Learning/Exploration
```json
{
  "enforcement": "advisory",
  "rules": {
    "lint": true,
    "format": false,
    "typecheck": false,
    "test": false,
    "secrets": true
  }
}
```

## Updating

```bash
# Update pre-commit hooks
pre-commit autoupdate

# Update husky
npm update husky

# Update linter configs from CDK
# Re-run setup-cdk-quality skill
```

---
name: pre-commit-hooks
description: Pre-commit hook setup with Husky and lint-staged. Use when configuring git hooks.
---

# Pre-commit Hooks Skill

This skill covers pre-commit hook configuration with Husky and lint-staged.

## When to Use

Use this skill when:
- Setting up git hooks
- Configuring pre-commit quality gates
- Automating code formatting
- Enforcing standards before commits

## Core Principle

**FAIL FAST** - Catch issues before they enter the repository. Pre-commit hooks are the first line of defense.

## Installation

### Husky + lint-staged

```bash
npm install -D husky lint-staged
npx husky init
```

### Directory Structure

```
project/
├── .husky/
│   ├── _/
│   │   └── husky.sh
│   └── pre-commit
├── package.json
└── ...
```

## Configuration

### package.json

```json
{
  "scripts": {
    "prepare": "husky"
  },
  "lint-staged": {
    "*.{ts,tsx}": [
      "biome check --write",
      "biome format --write"
    ],
    "*.{js,jsx}": [
      "biome check --write",
      "biome format --write"
    ],
    "*.{json,md}": [
      "biome format --write"
    ]
  }
}
```

### .husky/pre-commit

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npx lint-staged
npm run type-check
```

## lint-staged Patterns

### Basic Pattern

```json
{
  "lint-staged": {
    "*.ts": "command"
  }
}
```

### Multiple Commands

```json
{
  "lint-staged": {
    "*.ts": [
      "biome check --write",
      "biome format --write"
    ]
  }
}
```

### Glob Patterns

```json
{
  "lint-staged": {
    "src/**/*.ts": "biome check --write",
    "*.{json,md}": "biome format --write",
    "!dist/**": "biome check"
  }
}
```

## Biome Configuration

### lint-staged with Biome

```json
{
  "lint-staged": {
    "*.{ts,tsx,js,jsx}": [
      "biome check --write --no-errors-on-unmatched"
    ],
    "*.{json,md}": [
      "biome format --write --no-errors-on-unmatched"
    ]
  }
}
```

### Pre-commit Hook

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npx lint-staged
npm run type-check
```

## ESLint + Prettier Configuration

### lint-staged with ESLint + Prettier

```json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{js,jsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,css}": [
      "prettier --write"
    ]
  }
}
```

## Advanced Patterns

### Run Tests for Changed Files

```json
{
  "lint-staged": {
    "*.ts": [
      "biome check --write",
      "vitest related --run"
    ]
  }
}
```

### Skip CI in Commit Messages

```bash
# .husky/pre-commit
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Skip hooks for CI commits
if [ "$SKIP_HOOKS" = "1" ]; then
  exit 0
fi

npx lint-staged
npm run type-check
```

### Conditional Hooks

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Only run on feature branches
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" = "main" ]; then
  echo "Running full validation on main..."
  npm run validate
else
  npx lint-staged
fi
```

## Other Git Hooks

### commit-msg - Commit Message Validation

```bash
# .husky/commit-msg
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npx commitlint --edit $1
```

### Commitlint Configuration

```bash
npm install -D @commitlint/cli @commitlint/config-conventional
```

```javascript
// commitlint.config.js
export default {
  extends: ['@commitlint/config-conventional'],
};
```

### pre-push - Pre-Push Validation

```bash
# .husky/pre-push
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npm run validate
npm run test:coverage
```

## Troubleshooting

### Hook Not Running

```bash
# Reinstall hooks
npx husky install

# Make hook executable
chmod +x .husky/pre-commit
```

### Skipping Hooks

```bash
# Skip hooks for one commit
git commit --no-verify -m "WIP: skip hooks"
SKIP_HOOKS=1 git commit -m "Skip hooks"

# Not recommended for regular use!
```

### Debugging lint-staged

```bash
# Verbose output
npx lint-staged --debug
```

### Windows Issues

```bash
# Use cross-platform shebang
#!/usr/bin/env sh

# Or use node for complex scripts
#!/usr/bin/env node
```

## CI/CD Integration

### Ensure Hooks Are Installed

```yaml
# .github/workflows/ci.yml
- name: Install dependencies
  run: npm ci

# npm ci runs "prepare" script which installs husky
```

### Skip Hooks in CI

```bash
# CI environments typically don't need hooks
# npm ci doesn't run prepare by default in CI
```

## Best Practices Summary

1. **Keep hooks fast** - Under 10 seconds
2. **Only lint staged files** - Use lint-staged
3. **Run type-check** - Catches type errors
4. **Don't run full tests** - Too slow for commits
5. **Allow skipping** - For emergencies only
6. **Commit .husky** - Version control hooks
7. **Use --no-verify sparingly** - Document when skipped

## Hook Speed Optimization

```json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "biome check --write --no-errors-on-unmatched"
    ]
  }
}
```

Avoid:
- Running full test suite
- Type-checking all files (unless fast)
- Installing dependencies

## Code Review Checklist

- [ ] Husky installed and configured
- [ ] lint-staged in package.json
- [ ] Pre-commit hook runs linting
- [ ] Pre-commit hook runs formatting
- [ ] Type-check included (if fast)
- [ ] .husky directory committed
- [ ] Hooks work on all platforms

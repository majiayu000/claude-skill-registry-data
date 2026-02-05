---
name: git-ci-cd-manager
description: Automate Git workflow with conventional commits, setup GitHub Actions CI/CD, configure Husky hooks, manage PR automation, and handle semantic releases
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Git & CI/CD Manager

Expert skill for automating Git workflows, setting up CI/CD pipelines, managing conventional commits, and implementing release automation. Specializes in GitHub Actions, Husky hooks, semantic versioning, and PR management.

## Core Capabilities

### 1. Conventional Commits
- **Commitizen**: Interactive commit message generation
- **Commitlint**: Enforce commit message conventions
- **Semantic Commit Types**: feat, fix, docs, style, refactor, test, chore
- **Scopes**: Component-based scopes (@scope/package)
- **Breaking Changes**: BREAKING CHANGE footer
- **Auto-linking**: Link to issues and PRs

### 2. GitHub Actions CI/CD
- **Test Pipeline**: Run tests on PR and push
- **Build Pipeline**: Build and verify artifacts
- **Deploy Pipeline**: Automated deployment (staging, production)
- **Release Pipeline**: Automated semantic releases
- **PR Automation**: Auto-label, auto-assign, auto-review
- **Scheduled Jobs**: Dependency updates, security scans
- **Matrix Builds**: Test across multiple Node versions, OS

### 3. Git Hooks (Husky)
- **Pre-commit**: Lint staged files, run type check
- **Commit-msg**: Validate commit message format
- **Pre-push**: Run tests before push
- **Post-merge**: Install dependencies if package.json changed
- **Post-checkout**: Clean build artifacts
- **Custom Hooks**: Project-specific automation

### 4. Lint-Staged
- **ESLint**: Auto-fix linting errors
- **Prettier**: Auto-format code
- **TypeScript**: Type check only changed files
- **Tests**: Run tests for changed files only
- **Custom Commands**: Project-specific linting

### 5. Release Management
- **Semantic Release**: Automated versioning based on commits
- **Changelog Generation**: Auto-generate from commits
- **Git Tags**: Create and push version tags
- **NPM Publishing**: Automated package publishing
- **GitHub Releases**: Create release notes
- **Version Bumping**: Update package.json, lockfiles

### 6. Branch Management
- **Gitflow**: Main, develop, feature, hotfix branches
- **PR Templates**: Standardized PR descriptions
- **Branch Protection**: Required reviews, status checks
- **Auto-merge**: Merge when checks pass
- **Conflict Detection**: Early conflict warnings

### 7. PR Automation
- **Auto-labeling**: Based on changed files or PR title
- **Auto-assignment**: Assign reviewers by code ownership
- **Size Labeling**: Small, medium, large, xlarge
- **Status Checks**: Required checks before merge
- **Comment Templates**: Review guidelines

## Workflow

### Phase 1: Initial Setup
1. **Configure Git**
   - Set up user info
   - Configure line endings
   - Set up .gitignore
   - Configure Git aliases

2. **Install Tools**
   - Husky for Git hooks
   - Commitizen for commit messages
   - Commitlint for validation
   - Lint-staged for pre-commit
   - Semantic Release for automation

3. **Create Templates**
   - GitHub Actions workflows
   - PR templates
   - Issue templates
   - Contributing guidelines

### Phase 2: GitHub Actions Setup
1. **Create Workflows**
   - Test workflow (on PR, push)
   - Build workflow
   - Deploy workflow (staging, production)
   - Release workflow
   - Scheduled workflows

2. **Configure Secrets**
   - NPM_TOKEN for publishing
   - DEPLOY_TOKEN for deployments
   - Other service credentials

3. **Set Up Environments**
   - Staging environment
   - Production environment
   - Environment protection rules

### Phase 3: Automation
1. **Configure Hooks**
   - Pre-commit: lint + type check
   - Commit-msg: validate format
   - Pre-push: run tests

2. **Set Up PR Automation**
   - Auto-labeling workflow
   - Auto-assignment
   - Size labeling
   - Stale PR management

3. **Release Automation**
   - Semantic release configuration
   - Changelog generation
   - NPM publishing
   - GitHub release creation

## Conventional Commits Guide

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Description | Version Bump |
|------|-------------|--------------|
| `feat` | New feature | Minor (0.x.0) |
| `fix` | Bug fix | Patch (0.0.x) |
| `docs` | Documentation only | None |
| `style` | Code style (formatting, etc.) | None |
| `refactor` | Code refactoring | None |
| `perf` | Performance improvement | Patch |
| `test` | Add or update tests | None |
| `chore` | Maintenance tasks | None |
| `ci` | CI/CD changes | None |
| `build` | Build system changes | None |
| `revert` | Revert previous commit | Depends |

### Examples

```bash
# Feature with scope
feat(button): add loading state

Adds isLoading prop to Button component
Shows spinner when loading is true

Closes #123

# Breaking change
feat(forms)!: change validation API

BREAKING CHANGE: The validateForm function now returns a Promise
instead of synchronous validation result.

Migration guide available at docs/migration/v2.md

# Bug fix
fix(input): prevent double onChange call

Fixed issue where onChange was called twice on blur

Fixes #456

# Multiple changes
feat(components): add new Card variants

- Add 'elevated' variant with shadow
- Add 'outlined' variant with border
- Update Storybook stories

# Simple fix
fix: typo in README
```

### Commitizen Interactive

```bash
# Run commitizen
npm run commit

# Interactive prompts:
? Select the type of change: feat
? What is the scope?: button
? Write a short description: add loading state
? Provide a longer description: (press enter to skip)
? Are there any breaking changes? No
? Does this change affect any open issues? Yes
? Add issue references: Closes #123

# Generated commit:
feat(button): add loading state

Closes #123
```

## GitHub Actions Templates

### Test Workflow

```yaml
# .github/workflows/test.yml
name: Test

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npm run type-check

      - name: Run tests
        run: npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        if: matrix.node-version == '20.x'
        with:
          file: ./coverage/lcov.info
          fail_ci_if_error: true

  build:
    runs-on: ubuntu-latest
    needs: test

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20.x'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Check bundle size
        run: npm run size-check
```

### Release Workflow

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches: [main]

permissions:
  contents: write
  issues: write
  pull-requests: write
  id-token: write

jobs:
  release:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          persist-credentials: false

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20.x'
          registry-url: 'https://registry.npmjs.org'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Run tests
        run: npm test

      - name: Semantic Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
        run: npx semantic-release
```

### Deploy Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        type: choice
        options:
          - staging
          - production

jobs:
  deploy-staging:
    if: github.event_name == 'push' || github.event.inputs.environment == 'staging'
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20.x'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build
        env:
          NODE_ENV: production
          VITE_API_URL: ${{ secrets.STAGING_API_URL }}

      - name: Deploy to Staging
        run: npm run deploy:staging
        env:
          DEPLOY_TOKEN: ${{ secrets.STAGING_DEPLOY_TOKEN }}

  deploy-production:
    if: github.event.inputs.environment == 'production'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://example.com

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20.x'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build
        env:
          NODE_ENV: production
          VITE_API_URL: ${{ secrets.PRODUCTION_API_URL }}

      - name: Deploy to Production
        run: npm run deploy:production
        env:
          DEPLOY_TOKEN: ${{ secrets.PRODUCTION_DEPLOY_TOKEN }}

      - name: Notify Slack
        if: success()
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "🚀 Production deployment successful!"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### PR Automation Workflow

```yaml
# .github/workflows/pr-automation.yml
name: PR Automation

on:
  pull_request:
    types: [opened, edited, synchronize]

permissions:
  contents: read
  pull-requests: write

jobs:
  auto-label:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Label based on size
        uses: codelytv/pr-size-labeler@v1
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          xs_label: 'size/xs'
          xs_max_size: '10'
          s_label: 'size/s'
          s_max_size: '100'
          m_label: 'size/m'
          m_max_size: '500'
          l_label: 'size/l'
          l_max_size: '1000'
          xl_label: 'size/xl'

      - name: Label based on files
        uses: actions/labeler@v5
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          configuration-path: .github/labeler.yml

  auto-assign:
    runs-on: ubuntu-latest

    steps:
      - name: Auto-assign reviewers
        uses: kentaro-m/auto-assign-action@v1
        with:
          configuration-path: .github/auto-assign.yml
```

## Husky Configuration

### Setup Husky

```bash
# Install Husky
npm install --save-dev husky

# Initialize Husky
npx husky init

# Creates .husky/ directory with pre-commit hook
```

### Pre-commit Hook

```bash
# .husky/pre-commit
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Run lint-staged
npx lint-staged

# Run type check (optional, can be slow)
# npm run type-check
```

### Commit-msg Hook

```bash
# .husky/commit-msg
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Validate commit message with commitlint
npx --no -- commitlint --edit $1
```

### Pre-push Hook

```bash
# .husky/pre-push
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Run tests before push
npm test

# Check if build succeeds
npm run build
```

### Post-merge Hook

```bash
# .husky/post-merge
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Check if package.json changed
changed_files="$(git diff-tree -r --name-only --no-commit-id ORIG_HEAD HEAD)"

if echo "$changed_files" | grep --quiet "package.json"; then
  echo "📦 package.json changed, running npm install..."
  npm install
fi
```

## Configuration Files

### Commitlint Configuration

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',     // New feature
        'fix',      // Bug fix
        'docs',     // Documentation
        'style',    // Formatting
        'refactor', // Code refactoring
        'perf',     // Performance
        'test',     // Tests
        'chore',    // Maintenance
        'ci',       // CI/CD
        'build',    // Build system
        'revert',   // Revert commit
      ],
    ],
    'scope-enum': [
      2,
      'always',
      [
        'button',
        'input',
        'modal',
        'form',
        'layout',
        'theme',
        'deps',
        'config',
        // Add your component scopes
      ],
    ],
    'subject-case': [2, 'always', 'lower-case'],
    'subject-empty': [2, 'never'],
    'subject-full-stop': [2, 'never', '.'],
    'type-case': [2, 'always', 'lower-case'],
    'type-empty': [2, 'never'],
    'body-leading-blank': [2, 'always'],
    'footer-leading-blank': [2, 'always'],
    'header-max-length': [2, 'always', 100],
  },
}
```

### Lint-Staged Configuration

```javascript
// lint-staged.config.js
module.exports = {
  '*.{ts,tsx}': [
    'eslint --fix',
    'prettier --write',
    // Type check only staged files (faster than full type check)
    () => 'tsc --noEmit',
  ],
  '*.{js,jsx}': ['eslint --fix', 'prettier --write'],
  '*.{json,md,yml,yaml}': ['prettier --write'],
  '*.{css,scss}': ['stylelint --fix', 'prettier --write'],
  // Run tests for changed files
  '*.{ts,tsx,js,jsx}': ['npm test -- --findRelatedTests --passWithNoTests'],
}
```

### Semantic Release Configuration

```javascript
// release.config.js
module.exports = {
  branches: ['main'],
  plugins: [
    '@semantic-release/commit-analyzer',
    '@semantic-release/release-notes-generator',
    '@semantic-release/changelog',
    '@semantic-release/npm',
    '@semantic-release/github',
    [
      '@semantic-release/git',
      {
        assets: ['package.json', 'CHANGELOG.md'],
        message:
          'chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}',
      },
    ],
  ],
}
```

### Labeler Configuration

```yaml
# .github/labeler.yml
'type: feature':
  - 'src/**/*.{ts,tsx}'

'type: fix':
  - 'src/**/*.{ts,tsx}'

'type: docs':
  - '*.md'
  - 'docs/**/*'

'type: tests':
  - '**/*.test.{ts,tsx}'
  - '**/*.spec.{ts,tsx}'

'type: ci':
  - '.github/**/*'

'area: components':
  - 'src/components/**/*'

'area: utils':
  - 'src/utils/**/*'

'area: styles':
  - 'src/styles/**/*'
  - '**/*.css'
  - '**/*.scss'
```

### Auto-assign Configuration

```yaml
# .github/auto-assign.yml
addReviewers: true
addAssignees: false

reviewers:
  - reviewer1
  - reviewer2
  - reviewer3

numberOfReviewers: 2

# Assign based on file patterns
filePathAssignments:
  - patterns:
      - 'src/components/**'
    reviewers:
      - component-expert
  - patterns:
      - '**/*.test.ts'
    reviewers:
      - testing-expert
```

## Package.json Scripts

```json
{
  "scripts": {
    "commit": "cz",
    "prepare": "husky",

    "lint": "eslint src --ext .ts,.tsx",
    "lint:fix": "eslint src --ext .ts,.tsx --fix",

    "type-check": "tsc --noEmit",

    "test": "vitest",
    "test:ci": "vitest run --coverage",

    "build": "tsup",
    "build:check": "npm run build && npm run size-check",

    "size-check": "size-limit",

    "release": "semantic-release",
    "release:dry": "semantic-release --dry-run"
  },
  "config": {
    "commitizen": {
      "path": "cz-conventional-changelog"
    }
  }
}
```

## PR Template

```markdown
<!-- .github/pull_request_template.md -->
## Description

<!-- Describe your changes in detail -->

## Type of Change

<!-- Mark with an 'x' -->

- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📝 Documentation update
- [ ] 🎨 Style update (formatting, renaming)
- [ ] ♻️ Code refactoring (no functional changes)
- [ ] ⚡ Performance improvement
- [ ] ✅ Test update
- [ ] 🔧 Chore (updating build tasks, package manager configs, etc)

## Related Issues

<!-- Link related issues here -->

Closes #
Related to #

## Checklist

- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## Screenshots (if applicable)

<!-- Add screenshots here -->

## Additional Notes

<!-- Any additional information -->
```

## Branch Protection Rules

### Main Branch Protection

```yaml
# Recommended settings for main branch:

Required status checks:
  - Test (Node 18.x)
  - Test (Node 20.x)
  - Build
  - Lint

Require branches to be up to date before merging: ✓

Require pull request reviews:
  - Required approving reviews: 1
  - Dismiss stale reviews: ✓
  - Require review from Code Owners: ✓

Require signed commits: ✓ (optional)

Include administrators: ✓

Restrict who can push: Admins only
```

## Best Practices

### Commit Messages
1. **Use Imperative Mood**: "add feature" not "added feature"
2. **Be Specific**: "fix button hover state" not "fix bug"
3. **Limit Subject Line**: Max 72 characters
4. **Use Body for Details**: Explain why, not what
5. **Reference Issues**: Always link to issues

### Branching Strategy
1. **Gitflow**: main (production), develop (integration), feature/* (new features)
2. **Branch Naming**: `feature/add-button-component`, `fix/modal-close-bug`, `docs/update-readme`
3. **Short-lived Branches**: Merge within a few days
4. **Regular Rebase**: Keep feature branches up to date
5. **Clean History**: Squash commits before merging

### CI/CD
1. **Fast Feedback**: Run quick checks first (lint, type check)
2. **Parallel Jobs**: Run tests and build in parallel
3. **Cache Dependencies**: Use npm cache to speed up builds
4. **Fail Fast**: Stop pipeline on first failure
5. **Clear Errors**: Provide actionable error messages

### Pull Requests
1. **Small PRs**: Easier to review, faster to merge
2. **Self-Review**: Review your own PR before requesting review
3. **Clear Description**: Explain what, why, and how
4. **Link Issues**: Always reference related issues
5. **Tests**: Add tests for new features and bug fixes

### Releases
1. **Semantic Versioning**: Follow semver strictly
2. **Changelog**: Auto-generate from commits
3. **Release Notes**: Highlight breaking changes
4. **Pre-releases**: Use for beta testing
5. **Rollback Plan**: Be able to revert quickly

## Troubleshooting

### Husky Hooks Not Running

```bash
# Reinstall Husky
rm -rf .husky
npx husky init

# Re-add hooks
npm run prepare

# Check Git hooks directory
ls -la .git/hooks/
```

### Commitlint Failing

```bash
# Test commit message
echo "feat: add new feature" | npx commitlint

# Check configuration
npx commitlint --print-config

# Common issues:
# - Wrong type (use feat, fix, docs, etc.)
# - Missing scope when required
# - Subject in wrong case
# - Subject ends with period
```

### GitHub Actions Failing

```bash
# Test workflow locally
npm install -g act
act -l  # List workflows
act     # Run workflows

# Common issues:
# - Missing secrets
# - Wrong Node version
# - Dependencies not cached
# - Environment variables not set
```

### Semantic Release Not Publishing

```bash
# Dry run to see what would be released
npm run release:dry

# Common issues:
# - No conventional commits since last release
# - NPM_TOKEN not set
# - Wrong branch (must be main/master)
# - No permissions to publish
```

## When to Use This Skill

Activate this skill when you need to:
- Set up Git workflow for new project
- Configure conventional commits
- Create GitHub Actions pipelines
- Set up Husky pre-commit hooks
- Implement lint-staged
- Configure semantic release
- Create PR templates
- Set up branch protection rules
- Automate changelog generation
- Implement CI/CD pipeline
- Configure auto-merge rules
- Set up deployment workflows
- Create custom Git hooks
- Troubleshoot Git automation issues

## Output Format

When setting up Git automation, provide:
1. **Complete Configuration**: All config files (commitlint, husky, etc.)
2. **GitHub Actions Workflows**: Test, build, deploy, release
3. **Setup Scripts**: Automated installation and configuration
4. **Documentation**: How to use the system
5. **PR/Issue Templates**: Standardized templates
6. **Troubleshooting Guide**: Common issues and solutions

Always create production-ready, well-documented Git automation that follows industry best practices and security guidelines.

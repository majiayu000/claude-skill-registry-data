---
name: git-workflow-standards
description: Automatically applies when working with git. Ensures conventional commits, branch naming, PR templates, release workflow, and version control best practices.
category: velocity
---

# Git Workflow Standards

When working with git, follow these patterns for consistent, professional version control.

**Trigger Keywords**: git, commit, branch, pull request, PR, merge, release, version control, conventional commits, semantic versioning

**Agent Integration**: Used by `backend-architect`, `devops-engineer`, `release-manager`

## ✅ Correct Pattern: Conventional Commits

```bash
# Format: <type>(<scope>): <description>
#
# Types:
# - feat: New feature
# - fix: Bug fix
# - docs: Documentation only
# - style: Code style (formatting, semicolons)
# - refactor: Code restructuring
# - perf: Performance improvement
# - test: Adding tests
# - build: Build system changes
# - ci: CI configuration changes
# - chore: Other changes (dependencies, etc.)

# Examples:

# Feature commits
feat(auth): add JWT authentication
feat(api): add user profile endpoint
feat: implement password reset flow

# Bug fix commits
fix(database): resolve connection pool leak
fix(api): correct status code for validation errors
fix: handle null values in user input

# Documentation commits
docs(readme): update installation instructions
docs: add API documentation
docs(contributing): add code review guidelines

# Performance commits
perf(query): optimize user search query
perf: reduce memory usage in data processing

# Refactoring commits
refactor(models): simplify user model structure
refactor: extract common validation logic

# Breaking changes (add !)
feat(api)!: change response format to JSON:API spec
fix(auth)!: remove deprecated login endpoint

# With body and footer
feat(payments): add Stripe integration

Implement Stripe payment processing with webhooks
for subscription management.

BREAKING CHANGE: Payment API now requires Stripe account
Closes #123
```

## Branch Naming Convention

```bash
# Format: <type>/<short-description>
#
# Types:
# - feature/ - New features
# - bugfix/  - Bug fixes
# - hotfix/  - Urgent production fixes
# - release/ - Release branches
# - docs/    - Documentation changes

# Examples:

# Feature branches
git checkout -b feature/user-authentication
git checkout -b feature/add-search-endpoint
git checkout -b feature/implement-caching

# Bug fix branches
git checkout -b bugfix/fix-login-redirect
git checkout -b bugfix/resolve-memory-leak
git checkout -b bugfix/correct-email-validation

# Hotfix branches (for production)
git checkout -b hotfix/critical-security-patch
git checkout -b hotfix/fix-payment-processing

# Release branches
git checkout -b release/v1.2.0
git checkout -b release/v2.0.0-beta.1

# Documentation branches
git checkout -b docs/update-api-reference
git checkout -b docs/add-deployment-guide

# Include issue number when applicable
git checkout -b feature/123-user-profile
git checkout -b bugfix/456-fix-crash
```

## Pull Request Template

```markdown
# .github/pull_request_template.md

## Description

Brief description of what this PR does.

Fixes #(issue)

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Changes Made

- Change 1: Description
- Change 2: Description
- Change 3: Description

## Testing

### Test Plan

Describe how you tested these changes:

1. Step 1
2. Step 2
3. Step 3

### Test Results

- [ ] All existing tests pass
- [ ] New tests added and passing
- [ ] Manual testing completed

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

Add screenshots here if UI changes were made.

## Additional Notes

Any additional information that reviewers should know.

## Breaking Changes

If this PR introduces breaking changes, describe them here and update CHANGELOG.md.
```

## Commit Message Template

```bash
# .gitmessage

# <type>(<scope>): <subject>
#
# <body>
#
# <footer>

# Types:
# - feat:     New feature
# - fix:      Bug fix
# - docs:     Documentation
# - style:    Formatting
# - refactor: Code restructuring
# - perf:     Performance
# - test:     Tests
# - build:    Build system
# - ci:       CI changes
# - chore:    Other changes
#
# Scope: Component affected (api, database, auth, etc.)
#
# Subject: Imperative, present tense, no period
#
# Body: Explain what and why, not how
#
# Footer: Issue references, breaking changes

# Configure Git to use this template:
# git config commit.template .gitmessage
```

## Release Workflow

```bash
# Semantic Versioning: MAJOR.MINOR.PATCH
# - MAJOR: Breaking changes
# - MINOR: New features (backwards compatible)
# - PATCH: Bug fixes (backwards compatible)

# 1. Create release branch
git checkout -b release/v1.2.0

# 2. Update version numbers
# - pyproject.toml
# - __version__ in code
# - CHANGELOG.md

# 3. Update CHANGELOG.md
cat >> CHANGELOG.md << EOF
## [1.2.0] - 2025-01-15

### Added
- New feature 1
- New feature 2

### Changed
- Modified behavior 1

### Fixed
- Bug fix 1
- Bug fix 2

### Security
- Security fix 1
EOF

# 4. Commit version bump
git add .
git commit -m "chore(release): bump version to 1.2.0"

# 5. Merge to main
git checkout main
git merge release/v1.2.0

# 6. Create and push tag
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0

# 7. Delete release branch
git branch -d release/v1.2.0
git push origin --delete release/v1.2.0
```

## GitHub Actions for Release

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install build twine

      - name: Build package
        run: python -m build

      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
        run: twine upload dist/*

      - name: Create GitHub Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          body: |
            See [CHANGELOG.md](https://github.com/${{ github.repository }}/blob/main/CHANGELOG.md) for details.
          draft: false
          prerelease: false
```

## CHANGELOG Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Features added but not yet released

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Vulnerability fixes

## [1.2.0] - 2025-01-15

### Added
- JWT authentication for API endpoints
- User profile endpoint with avatar support
- Rate limiting middleware

### Changed
- Updated Pydantic to v2.5.0
- Improved error messages in validation

### Fixed
- Fixed memory leak in database connection pool
- Corrected timezone handling in timestamps

### Security
- Updated dependencies to fix CVE-2024-1234

## [1.1.0] - 2025-01-01

### Added
- Initial API implementation
- Database migrations with Alembic
- User authentication

[Unreleased]: https://github.com/user/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/user/repo/releases/tag/v1.1.0
```

## Git Hooks

```bash
# .git/hooks/pre-commit
#!/bin/bash
# Pre-commit hook to run linting and tests

echo "Running pre-commit checks..."

# Run linting
echo "Running ruff..."
ruff check .
if [ $? -ne 0 ]; then
    echo "Ruff checks failed. Please fix linting errors."
    exit 1
fi

# Run formatter
echo "Running black..."
black --check .
if [ $? -ne 0 ]; then
    echo "Code formatting issues found. Run: black ."
    exit 1
fi

# Run type checking
echo "Running mypy..."
mypy .
if [ $? -ne 0 ]; then
    echo "Type checking failed. Please fix type errors."
    exit 1
fi

# Run tests
echo "Running tests..."
pytest tests/ -v
if [ $? -ne 0 ]; then
    echo "Tests failed. Please fix failing tests."
    exit 1
fi

echo "All pre-commit checks passed!"
exit 0

# Make executable:
# chmod +x .git/hooks/pre-commit
```

## Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

# Install: pre-commit install
# Run manually: pre-commit run --all-files
```

## GitIgnore Template

```gitignore
# .gitignore for Python projects

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Environment
.env
.env.local
.env.*.local

# Logs
*.log

# Database
*.db
*.sqlite3

# OS
.DS_Store
Thumbs.db

# Project specific
/data/
/tmp/
```

## ❌ Anti-Patterns

```bash
# ❌ Vague commit messages
git commit -m "fix stuff"
git commit -m "update code"
git commit -m "changes"

# ✅ Better: Descriptive commits
git commit -m "fix(auth): resolve JWT token expiration issue"
git commit -m "feat(api): add pagination to user list endpoint"


# ❌ Committing to main directly
git checkout main
git commit -m "quick fix"  # Bad practice!

# ✅ Better: Use feature branch
git checkout -b bugfix/fix-issue
git commit -m "fix: resolve issue"
# Then create PR


# ❌ Large commits with mixed changes
git add .
git commit -m "add feature and fix bugs and update docs"

# ✅ Better: Separate commits
git add feature.py
git commit -m "feat: add new feature"
git add bugfix.py
git commit -m "fix: resolve bug"
git add docs/
git commit -m "docs: update documentation"


# ❌ No branch naming convention
git checkout -b my-changes
git checkout -b fix
git checkout -b update-stuff

# ✅ Better: Consistent naming
git checkout -b feature/add-authentication
git checkout -b bugfix/fix-validation-error
```

## Best Practices Checklist

- ✅ Use conventional commit format
- ✅ Follow branch naming convention
- ✅ Create descriptive PR descriptions
- ✅ Keep commits small and focused
- ✅ Write commits in imperative mood
- ✅ Reference issues in commits
- ✅ Use semantic versioning
- ✅ Maintain CHANGELOG.md
- ✅ Set up pre-commit hooks
- ✅ Review your own code before requesting review
- ✅ Keep PR size manageable (<400 lines)
- ✅ Squash/rebase before merging

## Auto-Apply

When working with git:
1. Use conventional commit format: `type(scope): description`
2. Create branch with type prefix: `feature/`, `bugfix/`
3. Write descriptive PR descriptions with checklist
4. Update CHANGELOG.md for releases
5. Tag releases with semantic versions
6. Set up pre-commit hooks
7. Keep commits focused and atomic

## Related Skills

- `code-review-framework` - For PR reviews
- `python-packaging` - For releases
- `dependency-management` - For version management

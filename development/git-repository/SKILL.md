---
name: git-repository
description: Repository management strategies including branch strategies (Git Flow, GitHub Flow, trunk-based), monorepo patterns, submodules, and repository organization. Use when user needs guidance on repository structure or branching strategies.
---

# Git Repository Management Skill

This skill provides comprehensive guidance on repository management strategies, branching models, repository organization patterns, and scaling git for large teams and codebases.

## When to Use

Activate this skill when:
- Setting up new repository structure
- Choosing branching strategy
- Managing monorepo vs polyrepo
- Organizing multi-project repositories
- Implementing submodule or subtree strategies
- Scaling git for large teams
- Migrating repository structures
- Establishing team workflows

## Branching Strategies

### Git Flow

**Branch Structure:**
- `main` (or `master`) - Production releases only
- `develop` - Integration branch for next release
- `feature/*` - Feature development branches
- `release/*` - Release preparation branches
- `hotfix/*` - Emergency production fixes

**Workflow:**

```bash
# Feature Development
git checkout develop
git checkout -b feature/user-authentication
# Work on feature...
git commit -m "feat: add JWT authentication"
git checkout develop
git merge --no-ff feature/user-authentication
git branch -d feature/user-authentication

# Release Preparation
git checkout develop
git checkout -b release/v1.2.0
# Bump version, update changelog, final testing...
git commit -m "chore: prepare release v1.2.0"

# Deploy Release
git checkout main
git merge --no-ff release/v1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0"
git checkout develop
git merge --no-ff release/v1.2.0
git branch -d release/v1.2.0
git push origin main develop --tags

# Hotfix
git checkout main
git checkout -b hotfix/security-patch
git commit -m "fix: patch security vulnerability"
git checkout main
git merge --no-ff hotfix/security-patch
git tag -a v1.2.1 -m "Hotfix v1.2.1"
git checkout develop
git merge --no-ff hotfix/security-patch
git branch -d hotfix/security-patch
git push origin main develop --tags
```

**Best For:**
- Scheduled releases
- Multiple production versions
- Large teams with QA process
- Products with maintenance windows
- Enterprise software

**Drawbacks:**
- Complex workflow
- Long-lived branches
- Potential merge conflicts
- Delayed integration

### GitHub Flow

**Branch Structure:**
- `main` - Production-ready code (always deployable)
- `feature/*` - All feature and fix branches

**Workflow:**

```bash
# Create Feature Branch
git checkout main
git pull origin main
git checkout -b feature/add-api-logging

# Develop Feature
git commit -m "feat: add structured logging middleware"
git push -u origin feature/add-api-logging

# Open Pull Request on GitHub
# Review, discuss, CI passes

# Merge and Deploy
# Merge PR on GitHub
# Automatic deployment from main

# Cleanup
git checkout main
git pull origin main
git branch -d feature/add-api-logging
```

**Best For:**
- Continuous deployment
- Small to medium teams
- Web applications
- Rapid iteration
- Cloud-native applications

**Drawbacks:**
- Requires robust CI/CD
- No release staging
- Less structured than Git Flow

### Trunk-Based Development

**Branch Structure:**
- `main` (or `trunk`) - Single source of truth
- Short-lived feature branches (< 2 days, optional)
- Feature flags for incomplete work

**Workflow:**

```bash
# Direct Commit to Main (Small Changes)
git checkout main
git pull origin main
# Make small change...
git commit -m "fix: correct validation logic"
git push origin main

# Short-Lived Branch (Larger Changes)
git checkout -b optimize-query
# Work for < 1 day
git commit -m "perf: optimize database query"
git push -u origin optimize-query
# Immediate PR, quick review, merge same day

# Feature Flags for Incomplete Features
git checkout main
git commit -m "feat: add payment gateway (behind feature flag)"
# Feature disabled in production until complete
git push origin main
```

**Best For:**
- High-velocity teams
- Continuous integration
- Automated testing
- Feature flag infrastructure
- DevOps culture

**Drawbacks:**
- Requires discipline
- Needs comprehensive tests
- Feature flag management
- Higher deployment frequency

### Release Branch Strategy

**Branch Structure:**
- `main` - Current development
- `release/v*` - Long-lived release branches
- `feature/*` - Feature branches

**Workflow:**

```bash
# Create Release Branch
git checkout -b release/v1.0 main
git push -u origin release/v1.0

# Continue Development on Main
git checkout main
# Work on v2.0 features...

# Backport Fixes to Release
git checkout release/v1.0
git cherry-pick abc123  # Fix from main
git push origin release/v1.0
git tag -a v1.0.5 -m "Patch release v1.0.5"
git push origin v1.0.5

# Multiple Release Maintenance
git checkout release/v0.9
git cherry-pick def456
git tag -a v0.9.8 -m "Security patch v0.9.8"
```

**Best For:**
- Multiple product versions
- Long-term support releases
- Enterprise customers
- Regulated industries

**Drawbacks:**
- Maintenance overhead
- Complex cherry-picking
- Diverging codebases

### Feature Branch Workflow

**Branch Structure:**
- `main` - Stable production code
- `feature/*` - Feature branches from main
- `bugfix/*` - Bug fix branches

**Workflow:**

```bash
# Feature Development
git checkout main
git checkout -b feature/payment-integration

# Long-Running Feature (Sync with Main)
git fetch origin
git rebase origin/main
# Or merge
git merge origin/main

# Complete Feature
git push origin feature/payment-integration
# Create pull request
# After review and approval, merge to main
```

**Best For:**
- Medium-sized teams
- Code review processes
- Parallel feature development
- Quality gates before merge

## Repository Organization

### Monorepo

**Structure:**
```
monorepo/
├── .git/
├── services/
│   ├── api/
│   ├── web/
│   └── worker/
├── packages/
│   ├── shared-utils/
│   ├── ui-components/
│   └── api-client/
├── tools/
│   ├── build-tools/
│   └── scripts/
└── docs/
```

**Advantages:**
- Single source of truth
- Shared code visibility
- Atomic cross-project changes
- Unified versioning
- Simplified dependency management
- Consistent tooling

**Disadvantages:**
- Large repository size
- Slower clone/fetch
- Complex CI/CD
- Access control challenges
- Tooling requirements

**Implementation:**

```bash
# Initialize Monorepo
git init
mkdir -p services/api services/web packages/shared-utils

# Workspace Setup (Node.js example)
cat > package.json << EOF
{
  "name": "monorepo",
  "private": true,
  "workspaces": [
    "services/*",
    "packages/*"
  ]
}
EOF

# Sparse Checkout (Partial Clone)
git clone --filter=blob:none --no-checkout <url>
cd repo
git sparse-checkout init --cone
git sparse-checkout set services/api packages/shared-utils
git checkout main

# Build Only Changed Packages
git diff --name-only HEAD~1 | grep "^services/api" && cd services/api && npm run build
```

**Tools:**
- **Bazel** - Build system for large monorepos
- **Nx** - Monorepo build system (Node.js)
- **Lerna** - JavaScript monorepo management
- **Turborepo** - High-performance build system
- **Git-subtree** - Merge external repositories

### Polyrepo

**Structure:**
```
organization/
├── api-service/       (separate repo)
├── web-app/           (separate repo)
├── mobile-app/        (separate repo)
├── shared-utils/      (separate repo)
└── documentation/     (separate repo)
```

**Advantages:**
- Clear ownership boundaries
- Independent versioning
- Smaller repository size
- Granular access control
- Flexible CI/CD
- Team autonomy

**Disadvantages:**
- Dependency version conflicts
- Cross-repo changes are complex
- Duplicated tooling/config
- Harder to refactor across repos

**Implementation:**

```bash
# Template Repository
git clone git@github.com:org/template-service.git new-service
cd new-service
rm -rf .git
git init
git remote add origin git@github.com:org/new-service.git

# Shared Configuration
# Use git submodules or packages
git submodule add git@github.com:org/shared-config.git config
```

### Monorepo vs Polyrepo Decision Matrix

| Factor | Monorepo | Polyrepo |
|--------|----------|----------|
| Team Size | Large teams | Small, autonomous teams |
| Code Sharing | High code reuse | Limited sharing |
| Deployment | Coordinated releases | Independent deployments |
| Access Control | Coarse-grained | Fine-grained |
| Repository Size | Very large | Small to medium |
| CI/CD Complexity | High | Low to medium |
| Tooling Requirements | Specialized tools | Standard git tools |
| Refactoring | Easy cross-project | Complex cross-repo |

## Submodule Management

### Basic Submodules

```bash
# Add Submodule
git submodule add https://github.com/org/shared-lib.git libs/shared

# Clone with Submodules
git clone --recurse-submodules <url>

# Initialize After Clone
git submodule init
git submodule update

# Update Submodule
cd libs/shared
git pull origin main
cd ../..
git add libs/shared
git commit -m "chore: update shared library"

# Update All Submodules
git submodule update --remote --merge

# Remove Submodule
git submodule deinit libs/shared
git rm libs/shared
rm -rf .git/modules/libs/shared
```

### Submodule Strategies

**Pinned Version Strategy:**
```bash
# Submodule points to specific commit
# Manual updates with testing
git submodule update --remote libs/shared
# Test changes...
git add libs/shared
git commit -m "chore: update shared-lib to v1.2.3"
```

**Auto-Update Strategy:**
```bash
# CI automatically updates submodules
# .github/workflows/update-submodules.yml
name: Update Submodules
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: true
      - run: git submodule update --remote
      - run: git commit -am "chore: update submodules"
      - run: git push
```

### Nested Submodules

```bash
# Add Nested Submodule
cd libs/framework
git submodule add https://github.com/org/utils.git utils

# Update Recursively
git submodule update --init --recursive

# Run Command in All Submodules
git submodule foreach 'git checkout main'
git submodule foreach 'git pull'
git submodule foreach --recursive 'echo $name: $(git rev-parse HEAD)'
```

## Subtree Management

### Git Subtree vs Submodule

**Subtree Advantages:**
- Simpler for contributors
- No separate clone steps
- Part of main repository history
- No broken references

**Subtree Disadvantages:**
- More complex to update
- Pollutes main history
- Larger repository

### Subtree Operations

```bash
# Add Subtree
git subtree add --prefix=libs/shared https://github.com/org/shared.git main --squash

# Update Subtree
git subtree pull --prefix=libs/shared https://github.com/org/shared.git main --squash

# Push Changes Back to Subtree
git subtree push --prefix=libs/shared https://github.com/org/shared.git feature-branch

# Split Subtree (Extract to New Repo)
git subtree split --prefix=libs/shared -b shared-lib-branch
git push git@github.com:org/new-shared-lib.git shared-lib-branch:main
```

### Subtree Workflow

```bash
# Setup Remote for Easier Management
git remote add shared-lib https://github.com/org/shared.git

# Add Subtree with Remote
git subtree add --prefix=libs/shared shared-lib main --squash

# Pull Updates
git fetch shared-lib
git subtree pull --prefix=libs/shared shared-lib main --squash

# Contribute Back
git subtree push --prefix=libs/shared shared-lib feature-branch
```

## Repository Templates

### GitHub Template Repository

```bash
# Create Template Structure
mkdir -p .github/workflows
cat > .github/workflows/ci.yml << EOF
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: make test
EOF

# Template Files
touch .gitignore README.md LICENSE CONTRIBUTING.md
mkdir -p docs src tests

# Mark as Template on GitHub Settings
# Use template to create new repositories
```

### Cookiecutter Template

```bash
# Install Cookiecutter
pip install cookiecutter

# Create from Template
cookiecutter https://github.com/org/project-template.git

# Template Structure
project-template/
├── cookiecutter.json
└── {{cookiecutter.project_name}}/
    ├── .git/
    ├── src/
    ├── tests/
    └── README.md
```

## Large Repository Management

### Partial Clone

```bash
# Blobless Clone (No file contents initially)
git clone --filter=blob:none <url>

# Treeless Clone (Even more minimal)
git clone --filter=tree:0 <url>

# Shallow Clone (Limited History)
git clone --depth 1 <url>

# Shallow Clone with Single Branch
git clone --depth 1 --single-branch --branch main <url>
```

### Sparse Checkout

```bash
# Enable Sparse Checkout
git sparse-checkout init --cone

# Specify Directories
git sparse-checkout set src/api src/shared

# Add More Directories
git sparse-checkout add docs

# List Current Sparse Checkout
git sparse-checkout list

# Disable Sparse Checkout
git sparse-checkout disable
```

### Git LFS (Large File Storage)

```bash
# Install Git LFS
git lfs install

# Track Large Files
git lfs track "*.psd"
git lfs track "*.zip"
git lfs track "data/**"

# Track Files in .gitattributes
cat .gitattributes
# *.psd filter=lfs diff=lfs merge=lfs -text

# Clone with LFS
git clone <url>
cd repo
git lfs pull

# Migrate Existing Files to LFS
git lfs migrate import --include="*.zip"
```

## Repository Splitting

### Extract Subdirectory to New Repo

```bash
# Using git filter-repo (recommended)
git filter-repo --path services/api --path-rename services/api:

# Result: New repo with only services/api content and history

# Using git subtree
git subtree split --prefix=services/api -b api-service
mkdir ../api-service
cd ../api-service
git init
git pull ../original-repo api-service
```

### Merge Multiple Repos

```bash
# Add Remote
git remote add project-b ../project-b

# Fetch History
git fetch project-b

# Merge with Unrelated Histories
git merge --allow-unrelated-histories project-b/main

# Move Files to Subdirectory
mkdir project-b
git mv * project-b/
git commit -m "chore: organize project-b into subdirectory"
```

## Repository Maintenance

### Regular Maintenance Tasks

```bash
# Optimize Repository
git gc --aggressive

# Prune Unreachable Objects
git prune --expire now

# Verify Integrity
git fsck --full

# Repack Repository
git repack -a -d --depth=250 --window=250

# Update Server Info (for dumb HTTP)
git update-server-info
```

### Automation Script

```bash
#!/bin/bash
# repo-maintenance.sh

echo "Starting repository maintenance..."

# Fetch all branches
git fetch --all --prune

# Clean up stale branches
git branch -vv | grep ': gone]' | awk '{print $1}' | xargs -r git branch -D

# Garbage collection
git gc --auto

# Verify integrity
git fsck --full --strict

echo "Maintenance complete!"
```

### Scheduled Maintenance

```yaml
# .github/workflows/maintenance.yml
name: Repository Maintenance
on:
  schedule:
    - cron: '0 2 * * 0'  # Weekly at 2 AM Sunday
jobs:
  maintain:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      - name: Run Maintenance
        run: |
          git gc --aggressive
          git prune --expire now
          git fsck --full
```

## Access Control and Permissions

### Branch Protection Rules

```yaml
# Example Configuration
protected_branches:
  main:
    required_pull_request_reviews:
      required_approving_review_count: 2
      dismiss_stale_reviews: true
      require_code_owner_reviews: true
    required_status_checks:
      strict: true
      contexts:
        - continuous-integration
        - security-scan
    enforce_admins: true
    restrictions:
      users: []
      teams: [core-team]
```

### CODEOWNERS File

```bash
# .github/CODEOWNERS

# Global owners
*                    @org/core-team

# Service owners
/services/api/       @org/backend-team
/services/web/       @org/frontend-team
/services/mobile/    @org/mobile-team

# Specific files
/docs/               @org/documentation-team
/.github/            @org/devops-team
/security/           @org/security-team @org/lead-architect

# Require multiple reviews
/packages/shared/    @org/core-team @org/architecture-team
```

## Migration Strategies

### SVN to Git

```bash
# Create Authors File
svn log --quiet | grep "^r" | awk '{print $3}' | sort -u > authors.txt

# Edit authors.txt:
# john = John Doe <john@example.com>

# Convert Repository
git svn clone <svn-url> --authors-file=authors.txt --stdlayout repo

# Convert Tags and Branches
cd repo
git for-each-ref --format="%(refname:short)" refs/remotes/tags | \
  cut -d / -f 3 | xargs -I {} git tag {} refs/remotes/tags/{}

# Push to Git
git remote add origin <git-url>
git push -u origin --all
git push origin --tags
```

### Mercurial to Git

```bash
# Using hg-git
hg bookmark -r default main
hg push git+ssh://git@github.com/org/repo.git

# Using fast-export
git clone https://github.com/frej/fast-export.git
mkdir git-repo && cd git-repo
git init
../fast-export/hg-fast-export.sh -r ../hg-repo
git checkout HEAD
```

## Best Practices

1. **Choose Appropriate Strategy:** Match branching model to team size and deployment frequency
2. **Document Workflows:** Keep team documentation current
3. **Automate Maintenance:** Regular repository health checks
4. **Use Branch Protection:** Enforce code review and CI
5. **Clear Ownership:** Define code owners for all areas
6. **Regular Cleanup:** Remove stale branches and merged features
7. **Monitor Repository Size:** Use LFS for large files
8. **Template Repositories:** Standardize new project structure
9. **Access Control:** Implement principle of least privilege
10. **Migration Planning:** Test migrations thoroughly before production

## Resources

Additional repository management resources are available in the `assets/` directory:
- `templates/` - Repository structure templates
- `scripts/` - Automation and maintenance scripts
- `workflows/` - CI/CD workflow examples

See `references/` directory for:
- Branching strategy comparison guides
- Monorepo tool documentation
- Enterprise git patterns
- Repository scaling strategies

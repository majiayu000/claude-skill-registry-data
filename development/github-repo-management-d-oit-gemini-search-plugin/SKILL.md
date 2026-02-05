---
name: github-repo-management
description: Manage GitHub repositories for Claude Code plugins including issues, pull requests, releases, CI/CD workflows, and GitHub Actions. Use when working with GitHub repository management, creating releases, setting up CI/CD, managing issues or pull requests.
---

# GitHub Repository Management for Claude Code Plugins

This skill provides comprehensive guidance for managing GitHub repositories that host Claude Code plugins, including issue tracking, pull request workflows, release management, and CI/CD automation.

## When to Use This Skill

Invoke this skill when the user:
- Wants to create or manage GitHub issues
- Needs help with pull request workflows
- Wants to set up or modify GitHub Actions CI/CD
- Asks about release management and versioning
- Needs to create GitHub releases
- Wants to automate repository workflows
- Asks about GitHub best practices for plugins
- Needs to set up branch protection or repository settings
- Wants to use GitHub Projects or milestones
- Needs help with GitHub Packages

## Repository Structure for Claude Code Plugins

```
my-plugin/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml              # Continuous integration
│   │   ├── release.yml         # Release automation
│   │   ├── pr-checks.yml       # Pull request validation
│   │   └── package.yml         # Package publishing
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── config.yml
│   └── PULL_REQUEST_TEMPLATE.md
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── commands/
├── agents/
├── hooks/
├── scripts/
├── tests/
├── CHANGES.md                  # Changelog
├── CONTRIBUTING.md             # Contribution guidelines
├── README.md
└── LICENSE
```

## GitHub Issues Management

### 1. Issue Templates

Create `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
---
name: Bug Report
about: Report a bug or unexpected behavior
title: '[BUG] '
labels: bug
assignees: ''
---

## Description
A clear and concise description of the bug.

## Steps to Reproduce
1. Go to '...'
2. Run command '...'
3. See error

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Environment
- Claude Code Version: [e.g., 1.0.0]
- Plugin Version: [e.g., 0.2.0]
- OS: [e.g., macOS 14.0, Ubuntu 22.04, Windows 11]
- Shell: [e.g., bash 5.2, zsh 5.9]

## Screenshots/Logs
If applicable, add screenshots or log output.

## Additional Context
Any other context about the problem.
```

Create `.github/ISSUE_TEMPLATE/feature_request.md`:

```markdown
---
name: Feature Request
about: Suggest a new feature or enhancement
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

## Feature Description
A clear and concise description of the feature you'd like.

## Use Case
Describe the problem this feature would solve or the workflow it would improve.

## Proposed Solution
How you envision this feature working.

## Alternatives Considered
Other approaches you've considered.

## Additional Context
Any other context, mockups, or examples.

## Benefit
Who would benefit from this feature and how?
```

Create `.github/ISSUE_TEMPLATE/config.yml`:

```yaml
blank_issues_enabled: false
contact_links:
  - name: Documentation
    url: https://github.com/owner/repo#readme
    about: Check the documentation first
  - name: Discussions
    url: https://github.com/owner/repo/discussions
    about: Ask questions and discuss ideas
```

### 2. Issue Labels

Recommended label structure:

**Type Labels:**
- `bug` (red) - Something isn't working
- `enhancement` (blue) - New feature or request
- `documentation` (light blue) - Documentation improvements
- `question` (purple) - Further information requested
- `refactor` (orange) - Code refactoring

**Priority Labels:**
- `priority/critical` (dark red) - Critical issue requiring immediate attention
- `priority/high` (orange) - High priority
- `priority/medium` (yellow) - Medium priority
- `priority/low` (green) - Low priority

**Status Labels:**
- `status/in-progress` (yellow) - Being worked on
- `status/blocked` (red) - Blocked by dependencies
- `status/needs-review` (blue) - Needs review or feedback
- `status/wontfix` (dark gray) - Won't be addressed

**Area Labels:**
- `area/commands` - Slash commands
- `area/agents` - Agent functionality
- `area/hooks` - Hook system
- `area/ci` - CI/CD workflows
- `area/docs` - Documentation

**Size Labels:**
- `size/XS` - Very small change
- `size/S` - Small change
- `size/M` - Medium change
- `size/L` - Large change
- `size/XL` - Very large change

### 3. Using GitHub CLI for Issues

```bash
# List issues
gh issue list
gh issue list --label bug --state open

# Create issue
gh issue create --title "Bug: Command fails with error" --body "Description of the bug"
gh issue create --label bug,priority/high

# View issue
gh issue view 123

# Comment on issue
gh issue comment 123 --body "Working on this now"

# Close issue
gh issue close 123 --comment "Fixed in v0.2.1"

# Reopen issue
gh issue reopen 123

# Assign issue
gh issue edit 123 --add-assignee @me

# Add labels
gh issue edit 123 --add-label bug,priority/high

# Link to PR
gh issue comment 123 --body "Fixed in #124"
```

### 4. Issue Management Best Practices

**Triage Process:**
1. Review new issues daily
2. Add appropriate labels
3. Ask for clarification if needed
4. Set priority and milestone
5. Assign if ready to work on

**Issue Templates:**
- Use templates to ensure consistent information
- Require environment details for bugs
- Ask for use cases in feature requests

**Communication:**
- Respond to new issues within 48 hours
- Keep reporters updated on progress
- Use clear, friendly language
- Link related issues and PRs

## Pull Request Workflows

### 1. Pull Request Template

Create `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] Performance improvement
- [ ] Test improvements

## Related Issues
Closes #(issue number)
Related to #(issue number)

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Added/updated tests
- [ ] All tests pass locally
- [ ] Tested manually

### Test Plan
1. Step to test
2. Expected result

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-reviewed the code
- [ ] Commented complex code sections
- [ ] Updated documentation (if applicable)
- [ ] Updated CHANGES.md
- [ ] No new warnings introduced
- [ ] Added tests for new functionality
- [ ] All tests pass

## Screenshots/Logs
If applicable, add screenshots or log output.

## Additional Notes
Any additional context or notes for reviewers.
```

### 2. PR Workflow with GitHub Actions

Create `.github/workflows/pr-checks.yml`:

```yaml
name: PR Checks

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  pr-title-check:
    name: PR Title Check
    runs-on: ubuntu-latest
    steps:
      - name: Check PR title format
        uses: amannn/action-semantic-pull-request@v5
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          types: |
            feat
            fix
            docs
            style
            refactor
            perf
            test
            chore
            revert
          requireScope: false

  size-check:
    name: PR Size Check
    runs-on: ubuntu-latest
    steps:
      - name: Check PR size
        uses: actions/github-script@v7
        with:
          script: |
            const pr = context.payload.pull_request;
            const additions = pr.additions;
            const deletions = pr.deletions;
            const totalChanges = additions + deletions;

            let label = '';

            if (totalChanges < 50) {
              label = 'size/XS';
            } else if (totalChanges < 200) {
              label = 'size/S';
            } else if (totalChanges < 500) {
              label = 'size/M';
            } else if (totalChanges < 1000) {
              label = 'size/L';
            } else {
              label = 'size/XL';
            }

            await github.rest.issues.addLabels({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: pr.number,
              labels: [label]
            });

            if (totalChanges > 1000) {
              await github.rest.issues.createComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: pr.number,
                body: '⚠️ This PR is quite large (1000+ lines changed). Consider breaking it into smaller PRs for easier review.'
              });
            }

  changes-check:
    name: Check CHANGES.md Updated
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Check if CHANGES.md was updated
        id: changes_check
        run: |
          git fetch origin ${{ github.base_ref }}
          if git diff --name-only origin/${{ github.base_ref }}...HEAD | grep -q "CHANGES.md"; then
            echo "updated=true" >> $GITHUB_OUTPUT
          else
            echo "updated=false" >> $GITHUB_OUTPUT
          fi

      - name: Comment if CHANGES.md not updated
        if: steps.changes_check.outputs.updated == 'false'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: '📝 Reminder: Please update CHANGES.md with your changes if applicable.'
            })

  conflict-check:
    name: Check for Merge Conflicts
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Check for merge conflicts
        run: |
          git fetch origin ${{ github.base_ref }}
          if ! git merge-tree $(git merge-base HEAD origin/${{ github.base_ref }}) HEAD origin/${{ github.base_ref }} | grep -q "^<<<<<"; then
            echo "✅ No merge conflicts detected"
          else
            echo "❌ Merge conflicts detected. Please resolve them."
            exit 1
          fi
```

### 3. Using GitHub CLI for Pull Requests

```bash
# Create PR
gh pr create --title "feat: add new command" --body "Description of changes"
gh pr create --draft  # Create draft PR
gh pr create --base develop --head feature-branch

# List PRs
gh pr list
gh pr list --state open --label bug

# View PR
gh pr view 123
gh pr view 123 --web  # Open in browser

# Review PR
gh pr review 123 --approve
gh pr review 123 --request-changes --body "Please address these issues"
gh pr review 123 --comment --body "Looks good overall"

# Checkout PR locally
gh pr checkout 123

# Merge PR
gh pr merge 123 --squash
gh pr merge 123 --merge
gh pr merge 123 --rebase

# Close PR
gh pr close 123

# Reopen PR
gh pr reopen 123

# Check PR status
gh pr status
gh pr checks 123
```

### 4. Branch Protection Rules

Recommended settings for main/master branch:

**Require pull request reviews:**
- Require 1 approval before merging
- Dismiss stale approvals when new commits are pushed
- Require review from code owners

**Require status checks:**
- Require branches to be up to date
- Required checks:
  - ShellCheck Linting
  - JSON Validation
  - Integration Tests
  - PR Title Check

**Require conversation resolution:**
- All conversations must be resolved

**Additional rules:**
- Require linear history
- Do not allow bypassing settings
- Restrict who can push to matching branches

## Release Management

### 1. Semantic Versioning

Follow semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR (1.0.0)**: Breaking changes
  - Command signature changes
  - Removed functionality
  - Major architectural changes

- **MINOR (0.1.0)**: New features (backward compatible)
  - New commands
  - New hooks
  - New configuration options
  - Enhancements to existing features

- **PATCH (0.0.1)**: Bug fixes (backward compatible)
  - Bug fixes
  - Security patches
  - Documentation fixes

**Pre-release versions:**
- `0.1.0-alpha.1` - Alpha release
- `0.1.0-beta.1` - Beta release
- `0.1.0-rc.1` - Release candidate

### 2. Changelog Management

Maintain `CHANGES.md` following Keep a Changelog format:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature descriptions

### Changed
- Changes to existing functionality

### Deprecated
- Features marked for removal

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security improvements

## [0.2.0] - 2025-01-15

### Added
- New `/analytics` command for usage statistics
- Cache hit rate tracking
- Support for custom cache TTL via environment variable

### Changed
- Improved error messages for failed searches
- Updated dependencies

### Fixed
- Fixed caching issue with special characters in queries
- Resolved hook triggering bug

## [0.1.0] - 2025-01-01

### Added
- Initial release
- `/search` command for web searches
- Agent-based search with context isolation
- Caching system with 1-hour TTL
- Hook integration for error detection

[Unreleased]: https://github.com/owner/repo/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/owner/repo/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/owner/repo/releases/tag/v0.1.0
```

### 3. Release Workflow

**Step 1: Prepare Release**

```bash
# Ensure you're on main branch
git checkout main
git pull origin main

# Update version in all files
# - plugin.json
# - .claude-plugin/marketplace.json
# - Any package.json files

# Update CHANGES.md
# Move unreleased changes to new version section
# Add release date

# Commit version bump
git add .
git commit -m "chore: prepare release v0.2.0"
git push origin main
```

**Step 2: Create Git Tag**

```bash
# Create annotated tag
git tag -a v0.2.0 -m "Release v0.2.0"

# Push tag (triggers release workflow)
git push origin v0.2.0
```

**Step 3: GitHub Release Automation**

Create `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*.*.*'

permissions:
  contents: write
  issues: write
  pull-requests: write

jobs:
  validate-version:
    name: Validate Version
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install jq
        run: sudo apt-get update && sudo apt-get install -y jq

      - name: Extract tag version
        id: tag_version
        run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

      - name: Validate version in plugin.json
        run: |
          PLUGIN_VERSION=$(jq -r '.version' plugin.json)
          TAG_VERSION="${{ steps.tag_version.outputs.VERSION }}"
          if [ "$PLUGIN_VERSION" != "$TAG_VERSION" ]; then
            echo "Version mismatch: plugin.json has $PLUGIN_VERSION but tag is $TAG_VERSION"
            exit 1
          fi

      - name: Validate version in marketplace.json
        run: |
          MARKETPLACE_VERSION=$(jq -r '.plugins[0].version' .claude-plugin/marketplace.json)
          TAG_VERSION="${{ steps.tag_version.outputs.VERSION }}"
          if [ "$MARKETPLACE_VERSION" != "$TAG_VERSION" ]; then
            echo "Version mismatch: marketplace.json has $MARKETPLACE_VERSION but tag is $TAG_VERSION"
            exit 1
          fi

  create-release:
    name: Create GitHub Release
    runs-on: ubuntu-latest
    needs: validate-version
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Extract tag version
        id: tag_version
        run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

      - name: Extract changelog for version
        id: changelog
        run: |
          VERSION="${{ steps.tag_version.outputs.VERSION }}"

          if [ -f CHANGES.md ]; then
            NOTES=$(sed -n "/## \[${VERSION}\]/,/## \[/p" CHANGES.md | sed '$d' | tail -n +2)
            if [ -z "$NOTES" ]; then
              NOTES="Release ${VERSION}"
            fi
          else
            NOTES="Release ${VERSION}"
          fi

          echo "$NOTES" > release_notes.txt

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          tag_name: ${{ github.ref_name }}
          name: Release ${{ steps.tag_version.outputs.VERSION }}
          body_path: release_notes.txt
          draft: false
          prerelease: false
          generate_release_notes: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Create release archive
        run: |
          VERSION="${{ steps.tag_version.outputs.VERSION }}"
          tar -czf plugin-${VERSION}.tar.gz \
            --exclude='.git' \
            --exclude='.github' \
            --exclude='tests' \
            --exclude='*.log' \
            --exclude='/tmp' \
            --warning=no-file-changed \
            . || [ $? -eq 1 ]

      - name: Upload release archive
        uses: softprops/action-gh-release@v1
        with:
          tag_name: ${{ github.ref_name }}
          files: plugin-*.tar.gz
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  notify:
    name: Post-Release Notifications
    runs-on: ubuntu-latest
    needs: create-release
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Extract version
        id: version
        run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

      - name: Create success comment
        run: |
          echo "✅ Release ${{ steps.version.outputs.VERSION }} published successfully!"
          echo "📦 Installation: /plugin add https://github.com/${{ github.repository }}"
```

**Step 4: Verify Release**

```bash
# Check release on GitHub
gh release view v0.2.0

# List all releases
gh release list

# Test installation
/plugin add https://github.com/owner/repo
```

### 4. Using GitHub CLI for Releases

```bash
# Create release manually
gh release create v0.2.0 --title "Release v0.2.0" --notes "Release notes here"

# Create release with files
gh release create v0.2.0 plugin.tar.gz --title "Release v0.2.0"

# Create draft release
gh release create v0.2.0 --draft --notes "Draft release"

# Create pre-release
gh release create v0.2.0-beta.1 --prerelease

# View release
gh release view v0.2.0

# List releases
gh release list

# Delete release
gh release delete v0.2.0

# Download release assets
gh release download v0.2.0

# Upload additional assets to existing release
gh release upload v0.2.0 additional-file.zip
```

## Continuous Integration (CI)

### 1. Basic CI Workflow

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  shellcheck:
    name: ShellCheck Linting
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run ShellCheck
        uses: ludeeus/action-shellcheck@master
        with:
          scandir: './scripts'
          severity: warning

      - name: Run ShellCheck on hooks
        uses: ludeeus/action-shellcheck@master
        with:
          scandir: './hooks'
          severity: warning

  json-validation:
    name: JSON Validation
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install jq
        run: sudo apt-get update && sudo apt-get install -y jq

      - name: Validate plugin.json
        run: jq empty .claude-plugin/plugin.json

      - name: Validate marketplace.json
        run: jq empty .claude-plugin/marketplace.json

      - name: Validate hooks.json (if exists)
        run: |
          if [ -f hooks/hooks.json ]; then
            jq empty hooks/hooks.json
          fi

  integration-tests:
    name: Integration Tests
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y jq bats

      - name: Set up test environment
        run: |
          mkdir -p /tmp/test-cache
          mkdir -p /tmp/test-logs

      - name: Run integration tests
        run: |
          if [ -f tests/run-integration-tests.sh ]; then
            bash tests/run-integration-tests.sh
          else
            echo "No integration tests found"
          fi

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: |
            /tmp/test-logs/*.log

  security-scan:
    name: Security Scanning
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Trivy security scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'
```

### 2. Matrix Testing

For testing across multiple environments:

```yaml
jobs:
  test:
    name: Test on ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        shell: [bash, zsh]
        exclude:
          - os: windows-latest
            shell: zsh

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run tests
        shell: ${{ matrix.shell }}
        run: |
          bash tests/run-tests.sh
```

### 3. Caching Dependencies

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Cache npm packages
        uses: actions/cache@v4
        with:
          path: ~/.npm
          key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-npm-

      - name: Install dependencies
        run: npm ci
```

### 4. Scheduled Workflows

```yaml
name: Nightly Tests

on:
  schedule:
    - cron: '0 2 * * *'  # Run at 2 AM daily
  workflow_dispatch:  # Allow manual trigger

jobs:
  extended-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run extended test suite
        run: bash tests/run-extended-tests.sh
```

## GitHub Packages

### 1. Publishing to GitHub Packages

Create `.github/workflows/package.yml`:

```yaml
name: Publish GitHub Package

on:
  release:
    types: [published]

permissions:
  contents: read
  packages: write

jobs:
  publish-package:
    name: Publish to GitHub Packages
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Extract version from tag
        id: version
        run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

      - name: Create package archive
        run: |
          VERSION="${{ steps.version.outputs.VERSION }}"

          mkdir -p dist

          tar -czf dist/plugin-${VERSION}.tar.gz \
            --exclude='.git' \
            --exclude='.github' \
            --exclude='tests' \
            --exclude='.claude' \
            --exclude='*.log' \
            --exclude='dist' \
            --warning=no-file-changed \
            . || [ $? -eq 1 ]

      - name: Create package metadata
        run: |
          VERSION="${{ steps.version.outputs.VERSION }}"
          cat > dist/package.json << EOF
          {
            "name": "@${{ github.repository_owner }}/${{ github.event.repository.name }}",
            "version": "${VERSION}",
            "description": "Claude Code plugin",
            "repository": {
              "type": "git",
              "url": "https://github.com/${{ github.repository }}.git"
            },
            "license": "MIT"
          }
          EOF

      - name: Upload package to release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            dist/plugin-*.tar.gz
            dist/package.json
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Advanced GitHub Features

### 1. GitHub Projects

**Setting up a project board:**

```bash
# Create project
gh project create --owner @me --title "Plugin Development"

# Add issue to project
gh project item-add PROJECT_ID --owner @me --url https://github.com/owner/repo/issues/123

# List projects
gh project list --owner @me
```

**Project fields:**
- Status: Todo, In Progress, In Review, Done
- Priority: Low, Medium, High, Critical
- Size: XS, S, M, L, XL
- Sprint: Sprint 1, Sprint 2, etc.

### 2. Milestones

```bash
# Create milestone
gh api repos/:owner/:repo/milestones -f title="v0.2.0" -f description="Second release"

# List milestones
gh api repos/:owner/:repo/milestones

# Add issue to milestone
gh issue edit 123 --milestone "v0.2.0"

# View milestone progress
gh api repos/:owner/:repo/milestones/1
```

### 3. Code Owners

Create `.github/CODEOWNERS`:

```
# Default owner for everything
* @owner

# Specific areas
/scripts/ @owner @script-maintainer
/commands/ @owner @command-maintainer
/.github/ @owner

# Documentation
*.md @owner @docs-team
```

### 4. GitHub Discussions

Enable discussions for:
- Q&A
- Ideas and feature requests
- General discussions
- Announcements

```bash
# List discussions
gh api repos/:owner/:repo/discussions

# Create discussion
gh api repos/:owner/:repo/discussions \
  -f title="New feature idea" \
  -f body="Description" \
  -f category="Ideas"
```

## Repository Settings Best Practices

### 1. General Settings

**Repository visibility:**
- Public for open-source plugins
- Private for proprietary plugins

**Features to enable:**
- Issues
- Projects
- Discussions
- Wiki (optional)

**Features to disable:**
- Sponsorships (unless applicable)

### 2. Branch Protection

**For main/master branch:**
- Require pull request reviews (1 approval)
- Require status checks to pass
- Require conversation resolution
- Require linear history
- Include administrators in restrictions

**For develop branch:**
- Require pull request reviews (1 approval)
- Require status checks to pass

### 3. Security Settings

**Enable:**
- Dependabot alerts
- Dependabot security updates
- Code scanning (CodeQL)
- Secret scanning

**Configure Dependabot:**

Create `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
      - "github-actions"

  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
      - "npm"
```

### 4. Notifications

Configure notifications for:
- Issues assigned to you
- PRs requesting your review
- CI failures on your branches
- Release notifications

## CI/CD Best Practices

### 1. Workflow Organization

**Separate workflows by purpose:**
- `ci.yml` - Continuous integration (linting, testing)
- `release.yml` - Release automation
- `pr-checks.yml` - Pull request validation
- `package.yml` - Package publishing
- `security.yml` - Security scanning

### 2. Performance Optimization

**Caching:**
```yaml
- name: Cache dependencies
  uses: actions/cache@v4
  with:
    path: |
      ~/.npm
      ~/.cache
    key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}
```

**Conditional execution:**
```yaml
- name: Run tests
  if: contains(github.event.head_commit.message, '[test]') || github.event_name == 'pull_request'
  run: npm test
```

**Job dependencies:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps: [...]

  test:
    needs: build
    runs-on: ubuntu-latest
    steps: [...]

  deploy:
    needs: [build, test]
    runs-on: ubuntu-latest
    steps: [...]
```

### 3. Secrets Management

**Required secrets:**
- `GITHUB_TOKEN` - Automatically provided
- API keys (e.g., `GEMINI_API_KEY`)
- Deploy tokens
- Third-party service credentials

**Using secrets:**
```yaml
- name: Run command
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: ./script.sh
```

### 4. Status Badges

Add to README.md:

```markdown
# Plugin Name

[![CI](https://github.com/owner/repo/workflows/CI/badge.svg)](https://github.com/owner/repo/actions)
[![Release](https://github.com/owner/repo/workflows/Release/badge.svg)](https://github.com/owner/repo/releases)
[![License](https://img.shields.io/github/license/owner/repo)](LICENSE)
[![Version](https://img.shields.io/github/v/release/owner/repo)](https://github.com/owner/repo/releases)
```

## Common Workflows

### 1. Feature Development

```bash
# Create feature branch
git checkout -b feature/new-command

# Make changes and commit
git add .
git commit -m "feat: add new command"

# Push and create PR
git push origin feature/new-command
gh pr create --title "feat: add new command"

# Address review feedback
git add .
git commit -m "refactor: address review feedback"
git push

# Merge when approved
gh pr merge --squash
```

### 2. Bug Fix

```bash
# Create bug fix branch
git checkout -b fix/command-error

# Fix bug and add test
git add .
git commit -m "fix: resolve command error"

# Push and create PR with issue reference
git push origin fix/command-error
gh pr create --title "fix: resolve command error" --body "Closes #123"

# Merge and backport if needed
gh pr merge --squash
```

### 3. Release Process

```bash
# 1. Update versions
# Edit plugin.json, marketplace.json

# 2. Update CHANGES.md
# Add release notes

# 3. Commit and push
git add .
git commit -m "chore: prepare release v0.2.0"
git push origin main

# 4. Create and push tag
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0

# 5. Verify release created
gh release view v0.2.0

# 6. Test installation
/plugin add https://github.com/owner/repo
```

## Troubleshooting

### CI Failures

**ShellCheck failures:**
```bash
# Run locally first
find scripts hooks -name "*.sh" -exec shellcheck {} +

# Fix issues before pushing
```

**JSON validation failures:**
```bash
# Validate locally
jq empty .claude-plugin/plugin.json
jq empty .claude-plugin/marketplace.json

# Use online JSON validator for complex issues
```

**Test failures:**
```bash
# Run tests locally
bash tests/run-tests.sh

# Debug with verbose output
DEBUG=true bash tests/run-tests.sh
```

### Release Issues

**Version mismatch:**
- Ensure all version fields match:
  - `plugin.json`
  - `.claude-plugin/marketplace.json`
  - Git tag

**Missing changelog:**
- Add entry to CHANGES.md before tagging
- Follow Keep a Changelog format

**Release workflow not triggering:**
- Check workflow file syntax
- Verify tag format (v*.*.*)
- Check repository permissions

## Resources

- **GitHub Docs**: https://docs.github.com/
- **GitHub Actions**: https://docs.github.com/en/actions
- **GitHub CLI**: https://cli.github.com/
- **Semantic Versioning**: https://semver.org/
- **Keep a Changelog**: https://keepachangelog.com/
- **Conventional Commits**: https://www.conventionalcommits.org/
- **Claude Code Plugins**: https://docs.claude.com/en/docs/claude-code/plugins

## Quick Reference Commands

```bash
# Issues
gh issue list
gh issue create --title "Title" --body "Body"
gh issue close 123

# Pull Requests
gh pr list
gh pr create --title "Title" --body "Body"
gh pr merge 123 --squash

# Releases
gh release list
gh release create v0.2.0 --title "Release v0.2.0"
gh release view v0.2.0

# Workflow runs
gh run list
gh run view RUN_ID
gh run watch RUN_ID

# Repository
gh repo view
gh repo clone owner/repo
```

## Next Steps

After setting up GitHub repository management:

1. Configure issue templates and labels
2. Set up branch protection rules
3. Create CI/CD workflows
4. Configure Dependabot
5. Enable security scanning
6. Set up project boards
7. Document contribution guidelines
8. Create release automation
9. Test the full workflow end-to-end
10. Monitor and iterate based on usage

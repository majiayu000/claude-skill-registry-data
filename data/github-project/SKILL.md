---
name: github-project
description: "GitHub repository setup and configuration. This skill should be used when creating new GitHub repositories, configuring branch protection or rulesets, setting up CODEOWNERS, or troubleshooting PR merge issues. By Netresearch."
---

# GitHub Project Skill

GitHub repository setup, configuration, and best practices for collaboration workflows.

## Core Workflow

To set up or configure a GitHub repository, follow these steps:

1. Consult the appropriate reference for your task
2. Copy and customize the relevant asset templates
3. Run `scripts/verify-github-project.sh` to validate configuration
4. Apply settings via GitHub UI or `gh` CLI

## Using Reference Documentation

### Repository Setup

When setting up repository structure, consult `references/repository-structure.md` for standard file layout, required documentation files, and directory conventions.

When migrating from master to main branch, consult `references/branch-migration.md` for step-by-step migration commands and branch protection updates.

### Dependency Management

When configuring automated dependency updates, consult `references/dependency-management.md` for Dependabot and Renovate configuration patterns, auto-merge workflows, and update strategies.

### GitHub Features

When working with sub-issues, consult `references/sub-issues.md` for GraphQL API usage, parent-child relationships, and issue hierarchy patterns.

When setting up automatic release labeling, consult `references/release-labeling.md` for PR labeling workflows, release categorization, and changelog automation.

## Running Scripts

### Repository Verification

To verify GitHub project configuration against best practices:

```bash
scripts/verify-github-project.sh /path/to/repository
```

This script checks:
- Repository documentation (README, LICENSE, SECURITY.md)
- Collaboration setup (CODEOWNERS, issue/PR templates)
- Dependency automation (Dependabot/Renovate, auto-merge)
- Release configuration

## Using Asset Templates

### Repository Documentation

To set up CODEOWNERS for code review assignments, copy `assets/CODEOWNERS.template` to `.github/CODEOWNERS`.

To add contribution guidelines, copy `assets/CONTRIBUTING.md.template` to `CONTRIBUTING.md`.

To configure security vulnerability reporting, copy `assets/SECURITY.md.template` to `SECURITY.md`.

### Issue and PR Templates

To add a bug report template, copy `assets/bug_report.md.template` to `.github/ISSUE_TEMPLATE/bug_report.md`.

To add a feature request template, copy `assets/feature_request.md.template` to `.github/ISSUE_TEMPLATE/feature_request.md`.

To standardize PR descriptions, copy `assets/PULL_REQUEST_TEMPLATE.md.template` to `.github/PULL_REQUEST_TEMPLATE.md`.

### Dependency Automation

To configure Dependabot, copy `assets/dependabot.yml.template` to `.github/dependabot.yml`.

To configure Renovate, copy `assets/renovate.json.template` to `renovate.json`.

### Auto-Merge Workflows

To enable basic auto-merge for dependency updates, copy `assets/auto-merge.yml.template` to `.github/workflows/auto-merge.yml`.

To enable auto-merge with direct commits (no merge queue), copy `assets/auto-merge-direct.yml.template` to `.github/workflows/auto-merge.yml`.

To enable auto-merge with merge queue support, copy `assets/auto-merge-queue.yml.template` to `.github/workflows/auto-merge.yml`.

### Release Automation

To set up automatic release labeling for PRs, copy `assets/release-labeler.yml.template` to `.github/workflows/release-labeler.yml`.

## Go Project CI Checklist

When setting up CI for Go projects, ensure these GitHub configurations:

| Setting | Purpose | How |
|---------|---------|-----|
| Branch protection | Require tests pass before merge | Branch settings or Rulesets |
| Dependabot/Renovate | Automated dependency updates | `.github/dependabot.yml` or `renovate.json` |
| Auto-merge workflow | Merge minor/patch updates automatically | `assets/auto-merge*.yml` templates |
| Required checks | CI workflow names in branch protection | Match exact workflow job names |

## Polyglot Project CI Checklist (PHP + JavaScript)

When setting up CI for projects with both PHP and JavaScript, ensure coverage from ALL languages:

| Requirement | Implementation | Why |
|-------------|----------------|-----|
| PHP test coverage | `phpunit --coverage-clover` for each test suite | Codecov needs all suites |
| JavaScript test coverage | `npm run test:coverage` with lcov output | Codecov aggregates all languages |
| vitest lcov reporter | `reporter: ['text', 'json', 'html', 'lcov']` | Required for Codecov compatibility |
| Codecov upload | List ALL coverage files in `files:` parameter | Ensures complete coverage picture |

### Example CI Configuration

```yaml
# Run all PHP test suites with coverage
- run: php -d pcov.enabled=1 .Build/bin/phpunit -c Build/phpunit/UnitTests.xml --coverage-clover .Build/coverage/unit.xml
- run: php -d pcov.enabled=1 .Build/bin/phpunit -c Build/phpunit/IntegrationTests.xml --coverage-clover .Build/coverage/integration.xml

# Run JavaScript tests with coverage
- uses: actions/setup-node@SHA # vX.Y.Z
  with:
    node-version: '22'
- run: npm install
- run: npm run test:coverage

# Upload ALL coverage files
- uses: codecov/codecov-action@SHA # vX.Y.Z
  with:
    files: .Build/coverage/unit.xml,.Build/coverage/integration.xml,coverage/lcov.info
```

### vitest Configuration

When using vitest, the `lcov` reporter is **required** for Codecov:

```javascript
// vitest.config.js
coverage: {
    provider: 'v8',
    reporter: ['text', 'json', 'html', 'lcov'],  // lcov REQUIRED
    reportsDirectory: 'coverage',
}
```

## TYPO3 Extension Repository Standards

When setting up repositories for TYPO3 extensions, apply these standards for consistency across Netresearch projects.

### Repository Settings

Configure via GitHub UI or `gh` CLI:

```bash
# Enable Projects tab
gh repo edit --enable-projects

# Set description (template)
gh repo edit --description "TYPO3 extension for <purpose> - by Netresearch"

# Add topics
gh api repos/OWNER/REPO/topics -X PUT -f names='["typo3","typo3-extension","php","<domain-topics>"]'
```

| Setting | Value | Why |
|---------|-------|-----|
| `has_projects` | true | Project board for issue tracking |
| `has_wiki` | false | Use Documentation/ folder instead |
| Description | `<What it does> - by Netresearch` | Consistent branding |

### Required Topics

All TYPO3 extension repos MUST have these topics:

| Topic | Required | Example |
|-------|----------|---------|
| `typo3` | ✅ Always | - |
| `typo3-extension` | ✅ Always | - |
| `php` | ✅ Always | - |
| Domain-specific | ✅ 2-5 more | `ckeditor`, `llm`, `ai`, `rte` |

**Example from t3x-rte_ckeditor_image:**
```
typo3, typo3-extension, typo3cms-extension, ckeditor, ckeditor-plugin, rte-ckeditor, magic-images
```

**Example from t3x-nr-llm:**
```
typo3, typo3-extension, php, ai, llm, openai, anthropic, claude, gemini, gpt
```

### README Badge Order

Badges should appear in this order (see `netresearch-branding` skill for templates):

```markdown
<!-- Row 1: CI/Quality badges -->
[![CI](...)][ci]
[![codecov](...)][codecov]
[![Documentation](...)][docs]  <!-- if applicable -->

<!-- Row 2: Security badges -->
[![OpenSSF Scorecard](...)][scorecard]
[![OpenSSF Best Practices](...)][bestpractices]
[![SLSA 3](...)][slsa]

<!-- Row 3: Standards badges -->
[![PHPStan](...)][phpstan]
[![PHP 8.x+](...)][php]
[![TYPO3 vXX](...)][typo3]
[![License](...)][license]
[![Latest Release](...)][release]
[![Contributor Covenant](...)][covenant]

<!-- Row 4: TYPO3 TER badges (if published to TER) -->
![Composer](https://typo3-badges.dev/badge/EXT_KEY/composer/shields.svg)
![Downloads](https://typo3-badges.dev/badge/EXT_KEY/downloads/shields.svg)
![Extension](https://typo3-badges.dev/badge/EXT_KEY/extension/shields.svg)
![Stability](https://typo3-badges.dev/badge/EXT_KEY/stability/shields.svg)
![TYPO3](https://typo3-badges.dev/badge/EXT_KEY/typo3/shields.svg)
![Version](https://typo3-badges.dev/badge/EXT_KEY/version/shields.svg)
<!-- Generated with 🧡 at typo3-badges.dev -->
```

### Quick Setup Commands

```bash
# Set topics for TYPO3 extension
gh api repos/netresearch/t3x-EXTNAME/topics -X PUT \
  -f names='["typo3","typo3-extension","php","DOMAIN1","DOMAIN2"]'

# Enable projects
gh repo edit netresearch/t3x-EXTNAME --enable-projects

# Update description
gh repo edit netresearch/t3x-EXTNAME \
  --description "TYPO3 extension for PURPOSE - by Netresearch"
```

### Verification

Check repository compliance:

```bash
# Check topics
gh api repos/OWNER/REPO/topics --jq '.names | if contains(["typo3","typo3-extension","php"]) then "✅ Required topics present" else "❌ Missing required topics" end'

# Check has_projects
gh api repos/OWNER/REPO --jq 'if .has_projects then "✅ Projects enabled" else "❌ Projects disabled" end'
```

## Merge Strategy & Signed Commits

When configuring repositories that require signed commits with clean history, consult `references/merge-strategy.md` for the recommended settings.

### Quick Reference

For signed commits workflow (rebase locally + merge commit):

| Repository Setting | Value | Why |
|--------------------|-------|-----|
| `allow_merge_commit` | **true** | Preserves signatures on feature branch commits |
| `allow_rebase_merge` | true | GitHub requires at least one of squash/rebase |
| `allow_squash_merge` | false | Destroys individual commit signatures |

| Branch Protection | Value | Why |
|-------------------|-------|-----|
| `required_signatures` | true | Enforces GPG/SSH signed commits |
| `required_linear_history` | **false** | Must be false - conflicts with merge commits |

### Workflow

```bash
# 1. Developer rebases PR branch locally (signs commits)
git fetch origin && git rebase origin/main
git push --force-with-lease

# 2. Merge via merge commit (preserves signatures)
gh pr merge <number> --merge
```

### Auto-Merge Compatibility

| Merge Strategy | Works with `required_signatures`? |
|----------------|-----------------------------------|
| Merge commit | ✅ Yes - GitHub signs the merge commit |
| Rebase merge | ❌ No - GitHub cannot sign rewritten commits |
| Squash merge | ❌ No - GitHub cannot sign squashed commit |

**Important:** When enabling auto-merge, select "Create a merge commit" strategy.

## CodeQL Configuration (MANDATORY)

Netresearch projects use custom CodeQL workflows (`.github/workflows/codeql.yml`). GitHub's "Default Setup" **MUST be disabled** - they cannot coexist.

### The Problem

When both Default Setup and a custom workflow exist, CI fails with:
```
CodeQL analyses from advanced configurations cannot be processed when the default setup is enabled
```

### Required Action

**Before pushing a custom CodeQL workflow**, disable Default Setup:

```bash
# Check current state
gh api repos/OWNER/REPO/code-scanning/default-setup --jq '.state'

# Disable default setup (MANDATORY)
gh api repos/OWNER/REPO/code-scanning/default-setup -X PATCH -f state=not-configured
```

| Setting | Required State | Why |
|---------|----------------|-----|
| Default Setup | `not-configured` | Conflicts with custom workflow |
| Custom `codeql.yml` | Present in `.github/workflows/` | Our standard security scanning |

### Verification

```bash
# Verify default setup is disabled
gh api repos/OWNER/REPO/code-scanning/default-setup --jq 'if .state == "not-configured" then "✅ Default Setup disabled" else "❌ Default Setup still enabled - DISABLE IT" end'
```

## Related Skills

When implementing Go code patterns and CI/CD workflows, use the `go-development` skill.

When implementing OpenSSF Scorecard, SLSA provenance, or signed releases, use the `enterprise-readiness` skill.

When establishing Git branching strategies or conventional commits, use the `git-workflow` skill.

When conducting deep security audits (OWASP, CVE analysis), use the `security-audit` skill.

## External Resources

When understanding GitHub Actions syntax, consult the [GitHub Actions Documentation](https://docs.github.com/en/actions).

When configuring branch protection, consult the [GitHub Branch Protection Guide](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches).

When setting up Dependabot, consult the [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot).

---

> **Contributing:** https://github.com/netresearch/github-project-skill

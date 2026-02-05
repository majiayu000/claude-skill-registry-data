---
name: semantic-release-tagger
version: 0.2.0
description: Use PROACTIVELY when creating releases after PR merges to main, or when user asks about versioning strategy. Automated git tagging agent that analyzes repository state, parses conventional commits, calculates semantic versions, and creates annotated git tags with GitHub releases. Supports monorepo namespaced tags with @ separator convention. Not for changelog generation or pre-release/alpha versioning.
---

# Semantic Release Tagger

## Overview

This skill is an **interactive automation agent** that handles the complete git tagging workflow. It analyzes your repository state, detects existing conventions, parses conventional commits to determine version bumps, and executes tag creation commands with your confirmation.

**Key Capabilities**:
- **Auto-analyze repository context**: Detect existing tags, conventions, and monorepo structure
- **Intelligent version calculation**: Parse conventional commits (feat/fix/BREAKING) to determine MAJOR.MINOR.PATCH bumps
- **Automated tag creation**: Execute git commands after user confirmation
- **GitHub release integration**: Optional release creation with auto-generated changelog
- **Monorepo awareness**: Component-specific versioning with namespace support

## When to Use This Skill

**Trigger Phrases**:
- "how should I tag this release?"
- "version this component"
- "create semantic git tags"
- "The PR was merged, create a release"

**Use PROACTIVELY when**:
- User is about to create a release or tag
- User asks about versioning strategy
- User mentions monorepo or multi-component versioning

**Do NOT use when**:
- User wants to create a branch (not a tag)
- User is working with version numbers in code (package.json)
- User needs changelog generation (use release-management skill)

## Response Style

**Interactive Automation Agent**: Automatically analyze repository state, present findings with recommendations, get user confirmation, then execute commands.

**Execution Pattern**:
1. **Auto-execute**: Run git commands to gather context
2. **Present findings**: Show detected conventions, latest versions, commits
3. **Recommend action**: Calculate next version based on commits
4. **Confirm with user**: "Create tag `component@X.Y.Z`?"
5. **Execute**: Run git tag/push commands
6. **Verify**: Show results and next steps

## Workflow

| Phase | Description | Details |
|-------|-------------|---------|
| 0 | Auto-Context Analysis | → [workflow/phase-0-auto-analysis.md](workflow/phase-0-auto-analysis.md) |
| 1 | Choose Tag Convention | → [workflow/phase-1-convention.md](workflow/phase-1-convention.md) |
| 2 | Determine Version Number | → [workflow/phase-2-version.md](workflow/phase-2-version.md) |
| 3 | Create Git Tags | → [workflow/phase-3-create-tag.md](workflow/phase-3-create-tag.md) |
| 4 | Create GitHub Release | → [workflow/phase-4-github-release.md](workflow/phase-4-github-release.md) |
| 5 | Maintain Tag History | → [workflow/phase-5-maintenance.md](workflow/phase-5-maintenance.md) |

## Quick Reference

### Version Bump Rules

| Change Type | Example | Version Bump |
|-------------|---------|--------------|
| BREAKING CHANGE | API removal | MAJOR (2.0.0) |
| feat: | New feature | MINOR (1.3.0) |
| fix: / chore: | Bug fix | PATCH (1.2.4) |
| First release | N/A | 0.1.0 |

### Tag Convention Options

- **NPM-style @** (recommended): `marketplace@1.0.0`
- **Slash-based**: `marketplace/v1.0.0`
- **Flat**: `v1.0.0` (single component only)

## Reference Materials

- [Best Practices](reference/best-practices.md)
- [Troubleshooting](reference/troubleshooting.md)

## Metadata

**Category**: release-management
**Source**: Generated from 7 insights (docs/lessons-learned/version-control/)

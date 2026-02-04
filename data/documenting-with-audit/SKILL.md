---
name: documenting-with-audit
description: Automated documentation auditing - ensures CLAUDE.md coverage, updates stale docs, recommends structural improvements
---

# Documentation Auditing

Knowledge for automated documentation auditing. Defines state tracking, scope system, generation templates, and output formats.

## Purpose

Documentation drifts from code. This skill provides knowledge for:
- CLAUDE.md coverage in meaningful directories
- Automatic doc updates when code changes
- Freshness tracking via git commits + timestamps
- Structural improvement recommendations

## State File: `.docsaudit.yaml`

Tracks audit state for all docs.

**Format:**
```yaml
version: 1

ignore:
  - node_modules/**
  - .git/**
  - dist/**
  - __pycache__/**

max_age_days: 90

audits:
  README.md:
    commit: abc123
    date: 2025-11-19T10:30:00Z
    scope: ["**/*"]

  src/auth/CLAUDE.md:
    commit: def456
    date: 2025-11-15T09:00:00Z
    # No scope = directory default (src/auth/**/*)
```

**Bootstrap:** If missing, create with sensible defaults, scan existing docs, initialize with current HEAD.

## Scope System

Scope = glob patterns defining which files a doc describes.

**Default Scope (Automatic):**
- `README.md` (root) -> `**/*` (whole project)
- `src/auth/CLAUDE.md` -> `src/auth/**/*`
- `docs/api.md` -> `docs/**/*`

**Explicit Override:**
```yaml
docs/api.md:
  scope: ["src/api/**/*"]  # Track API code, not docs dir
```

**Independent Docs:**
```yaml
CONTRIBUTING.md:
  scope: []  # Explicit empty = no code dependencies
```

**Staleness Triggers:**
1. Files in scope changed since `commit`
2. More than `max_age_days` since `date`

## CLAUDE.md Generation

**Analysis approach:**
- Read directory structure and file list
- Sample code: imports/exports, class/function names, module patterns
- Check existing README/comments
- Understand purpose and relationships

**Template:**
```markdown
# [Module Name]

## Purpose
[1-2 sentences: what this does]

## Key Components
- [file/class]: [purpose]
- [file/class]: [purpose]

## Dependencies
- Uses: [other modules]
- Used by: [other modules]

## Notes
[Important context, conventions, gotchas]
```

**Principles:**
- 2-line CLAUDE.md better than none
- Add value, avoid obvious
- Focus on non-obvious context
- Explain "why" not "what"

**Examples:**
```markdown
# tests/fixtures/auth

JWT tokens and auth payloads for testing.
Tokens are expired but have valid structure.
```

```markdown
# scripts/deployment

Production deployment utilities.
Run via `just deploy <env>` - never manually.
Handles DB migrations, health checks, rollback.
```

## Coverage Decisions

**Create CLAUDE.md when:**
- Any meaningful code/content
- Logic, utilities, modules
- Config, data, assets needing explanation
- Test fixtures, scripts, migrations

**Ignore only:**
- Build artifacts (dist/, __pycache__)
- Dependencies (node_modules/)
- Git internals (.git/)

## Sanity Check Patterns

**Consolidate:** >70% content overlap between docs
**Move:** Doc location vs scope mismatch (e.g., `docs/database.md` with scope `src/db/**/*`)
**Delete:** Scope patterns match zero files
**Split:** Doc >500 lines with multiple distinct topics
**Merge:** Multiple tiny docs (<50 lines each) with related scopes

Present recommendations, don't auto-apply - bigger decisions need human judgment.

## Output Format

```
Documentation Audit Report

Coverage (CLAUDE.md files):
  Created (N):
    + path/to/new.md (reason)

  Un-ignored (N):
    + path/to/unignored.md (reason)

Freshness (content updates):
  Updated (N):
    ~ path/to/updated.md (summary)

  Already current (N):
    ✓ path/to/current.md

Recommendations:
  ⚠ Issue: description
  ⚠ Issue: description

Files changed: N
Review: git diff
Commit: git commit -am "docs: automated audit"
```

**Symbols:**
- `+` Created/added
- `~` Updated/modified
- `✓` Already current
- `⚠` Recommendation

## Default Ignore Patterns

```yaml
ignore:
  - node_modules/**
  - .git/**
  - dist/**
  - build/**
  - __pycache__/**
  - "*.pyc"
  - .pytest_cache/**
  - .mypy_cache/**
  - coverage/**
  - htmlcov/**
```

Add project-specific: generated code, vendor dependencies, build outputs, IDE files.

## Philosophy

**Comprehensive coverage:** CLAUDE.md everywhere it adds value. Even 2-line docs beat nothing. Context is cheap, confusion is expensive.

**Automated maintenance:** System does the work. Git provides review. Commit or revert.

**Continuous improvement:** Regular audits catch drift. Sanity checks improve structure. Documentation evolves with code.

**Trust but verify:** Automation creates/updates. Human reviews via git. Best of both worlds.

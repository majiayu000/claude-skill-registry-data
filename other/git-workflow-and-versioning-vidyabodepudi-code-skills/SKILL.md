---
name: git-workflow-and-versioning
description: >
  Git conventions for trunk-based development, semantic versioning,
  feature flags, commit messages, and branch management. Use when
  making commits, managing branches, or planning releases.
version: 1.0.0
permissions:
  - fs.read
  - fs.write
  - shell.exec
triggers:
  - context: "making a commit"
  - context: "creating a branch"
  - context: "planning a release"
  - command: "/ship"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
model_variants:
  claude:
    enforcement_style: "human-partner collaborative"
  gemini:
    enforcement_style: "structured-checklist"
  gpt:
    enforcement_style: "directive-imperative"
author: codehands-core
signed: true
tier: 1
---

## Overview

Consistent git practices make code history readable, releases predictable, and collaboration smooth. This skill covers trunk-based development, conventional commits, semantic versioning, and feature flags.

## When to Use

- When making ANY git commit
- When creating branches
- When planning releases or versioning
- When deciding between feature flags and branches

## Process

### 1. Conventional Commits

Every commit message follows this format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
| Type | When |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `test` | Adding or correcting tests |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf` | Performance improvement |
| `chore` | Build, CI, dependencies, tooling |
| `security` | Security fix or improvement |

```bash
# Examples
feat(auth): add email verification flow
fix(api): handle null user in profile endpoint
test(auth): add registration edge case tests
security(deps): upgrade lodash to fix CVE-2024-12345
```

### 2. Trunk-Based Development

- **Main branch is always deployable.** Never commit broken code to main.
- **Short-lived feature branches.** Merge within 1-2 days. Long-lived branches diverge.
- **Feature flags over long branches.** For features that span multiple days:
  ```typescript
  if (featureFlags.isEnabled('new-auth-flow')) {
    // New implementation
  } else {
    // Current implementation
  }
  ```

### 3. Semantic Versioning

```
MAJOR.MINOR.PATCH
  │      │     └── Bug fixes (backward compatible)
  │      └──────── New features (backward compatible)
  └─────────────── Breaking changes
```

- **PATCH** (1.0.0 → 1.0.1): Bug fixes, security patches
- **MINOR** (1.0.0 → 1.1.0): New features, new endpoints, new options
- **MAJOR** (1.0.0 → 2.0.0): Breaking API changes, removed features, changed behavior

### 4. Branch Naming

```
feature/short-description
fix/issue-number-description
chore/tooling-update
security/cve-fix
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll write a good commit message later" | You won't. Write it now while the change is fresh. `git commit --amend` exists for minor fixes. |
| "Squash commit is fine for all these changes" | Squash when fixup commits pollute history. Don't squash when individual commits tell a meaningful story. |
| "Feature flags add complexity" | Feature flags add controlled complexity. Long-lived branches add uncontrolled complexity. Pick your poison — flags are cheaper. |

## Red Flags

- Commit messages like "fix", "update", "wip", "stuff"
- Commits on main/master that break the build
- Feature branches older than 1 week without good reason
- No semantic versioning on a library/published package

## Verification

- [ ] All commits follow conventional commit format
- [ ] Branch named with type prefix
- [ ] Feature flags used for multi-day features (not long-lived branches)
- [ ] Version bumped appropriately (semver) for releases

## See Also

- `codehands:using-git-worktrees` — Worktree-based branch management
- `codehands:finishing-a-development-branch` — Branch completion workflow
- `codehands:ci-cd-and-shipping` — CI/CD integration with git workflow

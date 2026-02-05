---
name: local-config
description: This skill should be used for configuring devloop project settings via .devloop/local.md, git workflow preferences, commit settings, review options
whenToUse: Setting up project config, git workflow preferences, enabling auto-branching, configuring PR creation, commit style settings
whenNotToUse: Reading plan.md, general git operations, one-time git commands
seeAlso:
  - skill: git-workflows
    when: git branching strategy decisions
  - skill: plan-management
    when: working with plan.md format
---

# Local Configuration

Project-specific devloop settings via `.devloop/local.md`.

## File Location

`.devloop/local.md` - NOT git-tracked (add to `.gitignore`)

## Format

YAML frontmatter followed by optional markdown notes:

```yaml
---
# Git Workflow Settings
git:
  auto-branch: false           # Create branch when plan starts
  branch-pattern: "feat/{slug}" # Branch naming pattern
  main-branch: main            # Name of main/trunk branch
  pr-on-complete: ask          # ask | always | never

# Commit Settings
commits:
  style: conventional          # conventional | simple
  scope-from-plan: true        # Use plan name as commit scope
  sign: false                  # Sign commits with GPG

# Review Settings
review:
  before-commit: ask           # ask | always | never
  use-plugin: null             # Or: code-review, pr-review-toolkit

# GitHub Issues Integration (optional)
github:
  link-issues: false           # Enable GH issue linking in plans
  auto-close: ask              # ask | always | never - close issue on plan complete
  comment-on-complete: true    # Post completion summary to linked issue
---

# Project Notes

Local notes and context for this project...
```

## Settings Reference

### git.auto-branch

When starting a new plan, automatically create a feature branch.

| Value | Behavior |
|-------|----------|
| `false` | Stay on current branch (default) |
| `true` | Create branch, ask for confirmation |

### git.branch-pattern

Pattern for auto-created branch names.

| Placeholder | Replaced With |
|-------------|---------------|
| `{slug}` | Plan name slugified |
| `{date}` | YYYY-MM-DD |
| `{user}` | Git user name |

Examples:
- `feat/{slug}` → `feat/add-authentication`
- `{user}/{slug}` → `alice/add-authentication`

### git.pr-on-complete

When all plan tasks complete, create a PR.

| Value | Behavior |
|-------|----------|
| `ask` | Ask user (default) |
| `always` | Auto-create PR |
| `never` | No PR prompt |

### commits.style

Commit message format.

| Value | Format |
|-------|--------|
| `conventional` | `type(scope): description` |
| `simple` | Plain description |

### review.before-commit

Run code review before committing.

| Value | Behavior |
|-------|----------|
| `ask` | Ask user (default) |
| `always` | Always review |
| `never` | Skip review |

### review.use-plugin

External plugin for code review.

| Value | Plugin |
|-------|--------|
| `null` | Use devloop:code-reviewer (default) |
| `code-review` | claude-plugins-official code-review |
| `pr-review-toolkit` | claude-plugins-official pr-review-toolkit |

### github.link-issues

Enable GitHub Issues integration for issue-driven development.

| Value | Behavior |
|-------|----------|
| `false` | No GH integration (default) |
| `true` | Enable issue linking in plans |

When enabled:
- `/devloop:from-issue 123` starts work from an issue
- Plans include `**Issue**: #123` header
- Completion can sync back to the issue

### github.auto-close

Automatically close linked issues when shipping commits.

| Value | Behavior |
|-------|----------|
| `ask` | Ask user (default) |
| `always` | Auto-add `Closes #N` to commits |
| `never` | Don't add closing keywords |

When enabled, commits include GitHub closing keywords (`Closes #N` or `Fixes #N`) which automatically close the linked issue when pushed.

### github.comment-on-complete

Post a completion summary to the linked issue.

| Value | Behavior |
|-------|----------|
| `true` | Post summary comment (default when link-issues is true) |
| `false` | Don't comment |

Summary includes: tasks completed, time elapsed, archive location.

## Defaults

If no `local.md` exists, all settings use safe defaults:

```yaml
git:
  auto-branch: false
  branch-pattern: "feat/{slug}"
  main-branch: main
  pr-on-complete: ask

commits:
  style: conventional
  scope-from-plan: true
  sign: false

review:
  before-commit: ask
  use-plugin: null

github:
  link-issues: false
  auto-close: ask
  comment-on-complete: true
```

## Example Configurations

### Minimal (Git-aware)

```yaml
---
git:
  auto-branch: true
---
```

### Full CI/CD Workflow

```yaml
---
git:
  auto-branch: true
  branch-pattern: "feat/{slug}"
  pr-on-complete: always

commits:
  style: conventional
  sign: true

review:
  before-commit: always
  use-plugin: pr-review-toolkit
---
```

### Solo Developer (Skip Ceremony)

```yaml
---
git:
  auto-branch: false
  pr-on-complete: never

review:
  before-commit: never
---
```

### Issue-Driven Development

```yaml
---
git:
  auto-branch: true
  pr-on-complete: always

github:
  link-issues: true
  auto-close: always
  comment-on-complete: true
---
```

With this config:
1. `/devloop:from-issue 123` fetches issue details
2. Plan includes `**Issue**: #123` reference
3. On completion: posts summary, closes issue

## Reading Config

The devloop plugin reads config automatically. Commands like `/devloop:ship` parse `.devloop/local.md` and apply settings.

Internally, the plugin uses `${CLAUDE_PLUGIN_ROOT}/scripts/parse-local-config.sh` to parse YAML frontmatter and return JSON with defaults filled in.

## Updating Config

Edit `.devloop/local.md` directly. Changes take effect on next command.

## Plugin Integration Settings

### Disabling Superpowers Suggestions

By default, devloop skills reference complementary superpowers skills when available. To disable these suggestions:

```yaml
---
plugins:
  superpowers-suggestions: false  # Disable seeAlso to superpowers skills
---
```

### Context Threshold for Ralph Loop

When using `/devloop:ralph` with context auto-exit:

```yaml
---
context_threshold: 70  # Exit ralph loop when context usage exceeds this % (default: 70)
---
```

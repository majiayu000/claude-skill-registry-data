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

## Reading Config

The devloop plugin reads config automatically. Commands like `/devloop:ship` parse `.devloop/local.md` and apply settings.

Internally, the plugin uses `${CLAUDE_PLUGIN_ROOT}/scripts/parse-local-config.sh` to parse YAML frontmatter and return JSON with defaults filled in.

## Updating Config

Edit `.devloop/local.md` directly. Changes take effect on next command.

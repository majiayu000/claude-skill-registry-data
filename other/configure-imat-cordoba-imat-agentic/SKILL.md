---
name: configure
description: This skill should be used when the user asks to "configure the agentic workflow", "set up imat-agentic", "run the setup wizard", "change the confidence threshold", "update workflow settings", or when .claude/imat-agentic.local.md is missing. Interactive wizard that creates or updates the project configuration for the imat-agentic plugin.
---

# Skill: configure

Interactively creates or updates `.claude/imat-agentic.local.md` — the project-local configuration for the `imat-agentic` plugin.

## When this runs

Run this before the first `agentic-loop` invocation, or when settings need to change. This file is gitignored (`.claude/*.local.md`) — each contributor configures their own preferences.

## Configuration fields

| Key | Default | Options | Description |
|---|---|---|---|
| `quality_preset` | `sonnet` | `sonnet`, `quality`, `opus` | Model tier for most agents |
| `parallel_explorers` | `2` | `1`, `2`, `3` | Concurrent exploration instances |
| `confidence_threshold` | `80` | `70`, `80`, `90` | Review filter threshold |
| `max_review_retries` | `2` | `1`–`5` | Max review retry cycles |
| `harness_profile` | `full` | `full`, `light`, `off` | Harness check scope |
| `recall_before_explore` | `true` | `true`, `false` | Run recall before exploration |
| `auto_advance` | `false` | `true`, `false` | Skip confirmations (use for automation only) |
| `artifact_retention_days` | `30` | integer | Days before cleaning up old agentic/ artifacts |

## Wizard procedure

### 1. Check for existing config

Read `.claude/imat-agentic.local.md` if it exists. Show current values before asking for changes.

### 2. Ask each question

Use `AskUserQuestion` for each configurable field. Show the default and options clearly. Allow accepting defaults by selecting the first option.

### 3. Write the config file

Write `.claude/imat-agentic.local.md`:

```markdown
---
quality_preset: sonnet
parallel_explorers: 2
confidence_threshold: 80
max_review_retries: 2
harness_profile: full
recall_before_explore: true
auto_advance: false
artifact_retention_days: 30
---

# imat-agentic configuration

Local configuration for the imat-agentic plugin.
This file is gitignored — do not commit it.

Run `/imat-agentic:configure` to update these settings.
```

### 4. Confirm

Show a summary of the written config. Remind the user that the file is gitignored and each contributor sets their own.

## Notes

- `auto_advance: true` disables user confirmation prompts mid-loop. Only use for scripted/CI runs.
- `quality_preset: opus` uses the most capable model but costs more per run.
- `confidence_threshold: 70` surfaces more review findings — useful when onboarding to a new codebase. Set to `90` once the codebase is well-understood.

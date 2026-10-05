---
name: equip
description: Equipment manager for Claude Code projects — inventory local skills/agents/scripts, audit external upstream repos (red-flag + prompt-injection screening), sync selectively after user approval. Absorbs container-layout skill repos AND single-skill-at-root repos. Project-agnostic.
when_to_use: "equip, upstream, absorb skill, absorb a design-system repo, update skill from github, review external skill, sync skill, inventory skills, 装备, 更新外部技能, 审核上游, 管理插件来源 — NOT for first-party feature development (just write code)"
argument-hint: '<command> [args]  # inventory | audit <repo|id> | sync <id> [--apply] | diff <id> | list | add <repo> | remove <id>'
user_invocable: true
---

# /equip — Equipment Manager

A project-agnostic skill for managing "absorbed" assets (skills, agents, scripts) that originated in external GitHub repos. It treats each upstream as a supplier whose shipments must be **reviewed before adoption**, not blindly synced.

## Subcommands

| Command | Purpose |
|---|---|
| `/equip inventory` | Scan current project; classify every asset as `native` / `absorbed` / `modified-absorbed` / `orphan`; write `.claude/equipment/inventory.yaml` |
| `/equip audit <repo\|id>` | Clone upstream, apply red-flag checks to each skill, and bind the decision report to the exact audited commit |
| `/equip sync <id> [--apply]` | Refresh upstream, verify its exact commit matches the audit, then perform a 3-way merge; dry-run by default |
| `/equip diff <id>` | Show per-file delta between registered `last_synced_commit` and remote HEAD |
| `/equip list` | Show registered upstreams with ahead/behind status |
| `/equip add <repo>` | Register a new upstream (interactive: select which local paths it covers) |
| `/equip remove <id>` | Unregister an upstream (keeps files, removes tracking) |

## Usage

```
/equip inventory                                 # first step for any project
/equip audit AgriciDaniel/claude-seo             # full evaluation
/equip sync claude-seo                           # dry-run: show what would change
/equip sync claude-seo --apply                   # actually write changes
/equip diff claude-seo                           # inspect drift
/equip audit .                                   # self-audit current project as if upstream
```

## Design principles

- **Review-first, not sync-first**: upstream content is always audited before it touches local files
- **Commit-bound approval**: `--apply` fails closed if the fetched commit differs from the exact commit in the audit report; re-run `/equip audit` to approve drift
- **Trust is per-skill, not per-repo**: one upstream can have 17 good skills + 3 bad ones; `/equip` picks
- **Local customizations are sacred**: files modified locally are never overwritten without explicit approval
- **Transparent**: every decision recorded in `.claude/equipment/audits/<id>-<date>.md` that the user can read and edit

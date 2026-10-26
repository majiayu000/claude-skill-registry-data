---
name: find-me-a-skill
description: Suggest which skill or workflow fits a task, with model and /effort per step and paste-ready commands; runs nothing. Use for "which skill should I use", "find me a skill", "how should I run this", "what model/effort for this".
model: haiku
effort: low
---

Read-only: suggest, never invoke a skill, agent or tool that changes anything. The user starts the work by pasting your commands.

## 1. Task

First that applies:
- Text after the command.
- The goal of this conversation so far.
- The top 1-3 board tasks, found as the `next` skill's `BOARD.md` says (`~/.claude/skills/next/` or, as the plugin, `kanban/next/`); give one suggestion per task. No `next` skill installed: skip this line.
- No repo or no board: ask what the task is, then stop.

## 2. Options (at most 3)

Candidates: every skill in your available-skills list, plus the entries and workflows in [CATALOG.md](CATALOG.md).

- **Primary**: the best fit among all installed skills, or a CATALOG.md workflow when the task spans its steps.
- **From your collection**: label any option that comes from CATALOG.md, primary or not. A CATALOG.md entry or workflow that fits and isn't already the primary is added as another option.
- **Not installed**: a CATALOG.md entry that is not in your available-skills list (a workflow: any of its skills) is labelled `not installed` only after a file check finds it missing: `~/.claude/skills/<name>/SKILL.md`, then the `krish` plugin's install dir (its `installPath` in `~/.claude/plugins/installed_plugins.json`, searched for `<name>/SKILL.md`; no such file or no `krish` entry → skip that check and say so). User-only skills never appear in that list even when installed. Give it the install command from the top README's Install section (`./scripts/install-skills.sh`, or `/plugin install krish@krish`). Its commands won't run until then.
- **Model and effort per step**: CATALOG.md's default; for a large or risky task move effort up one level; move the model up one tier only when effort is already `max`. For a small task do the reverse: effort down one level, model down only when effort is already `low`. At opus with effort `max` (or haiku with `low`) there is nothing further; say so. Scale: haiku < sonnet < opus; low < medium < high < xhigh < max.
- **Not in CATALOG.md**: name its origin (`plugin <name>` from its `<name>:` prefix, else `built-in`) and label model and effort `estimate`.
- **User-only** skills (`skill (user only)` in CATALOG.md) are still suggested: the user runs them by pasting the command.
- **Agents** run inside a skill (`pair`, `meta-orchestrator`) or on request ("use the planner agent"); **hooks** are installed, not run: say which.
- **No fit**: say so, name the nearest option, and suggest doing the task directly at an `estimate` model and effort.

## 3. Reply

```
Task: <one line>

1. <name> (<skill|workflow>[, from your collection][, <origin>]): <why, one line>
   Steps: /a (sonnet · medium) -> you: <checkpoint> -> /b (opus · high)
   You decide: <each human-in-the-loop point>
2. ...

Run option 1:
/model sonnet
/effort medium
/a <args>
```

Steps and `You decide` come from CATALOG.md for a workflow; for a single skill, list its gates (approvals, yes/no points) from its description. Commands are exact and copyable; for a workflow give the first step's. Skills from the plugin (`krish:` entries in your available-skills list) are invoked with that prefix: write `/krish:pair`, not `/pair`.

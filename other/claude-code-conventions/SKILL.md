---
name: claude-code-conventions
description: How to create and manage Claude Code rules, skills, hooks, sub-agents, and memory for this project. Use when documenting a convention, creating new project knowledge, or deciding where something should live.
---

# Claude Code Conventions — Detailed Procedure

This project's `.claude/` layout:

```
.claude/
├── settings.json          # hook wiring, permissions, plugin config
├── settings.local.json    # personal overrides (gitignored — create your own)
├── rules/                 # short always-loaded reminders (~15-25 lines each)
├── skills/<name>/SKILL.md # detailed on-demand procedures
├── agents/<name>.md       # dispatchable sub-agent definitions
├── hooks/*.sh             # deterministic shell enforcement
├── memory/MEMORY.md       # durable project/feedback/preference facts (index)
└── sessions/              # session state written by hooks (gitignore this)
```

## Creating a new rule

1. Write `.claude/rules/<topic>.md`. Keep it under ~25 lines: the reminder
   itself, then a "Load this rule when" and "Skip when" section so future
   sessions know when to actually read it (rules are always injected into
   context, but the load/skip sections tell Claude when the *content*
   applies to the current task).
2. If the rule needs more than ~25 lines of procedure, split: keep the short
   version in the rule, put the detail in a matching skill
   (`.claude/skills/<topic>/SKILL.md`), and have the rule's "Load when"
   section point at the skill.
3. Link the new rule from CLAUDE.md's "Code Review Extended Rules" section
   if it's something a PR reviewer should check.

## Creating a new skill

1. `mkdir -p .claude/skills/<name>` and write `SKILL.md` with YAML
   frontmatter (`name`, `description`) at the top — the description is what
   gets matched against user intent, so make it specific and keyword-rich.
2. Skills are invoked either automatically (when the description matches
   the task) or explicitly via `/`+name if the user types it as a slash
   command.

## Creating a new hook

1. Write `.claude/hooks/<name>.sh` — read the tool payload from stdin,
   parse with `python3 -c "..."` (most reliable for JSON with special
   characters), decide allow (`exit 0`) / block (`exit 2`) / soft-nudge
   (print to stderr, `exit 0`).
2. Wire it into `.claude/settings.json` under the right event
   (`PreToolUse`, `PostToolUse`, `SessionStart`, `SessionEnd`,
   `UserPromptSubmit`, `PermissionRequest`) and matcher (tool name, or a
   conditional `if: "Bash(some command*)"` filter).
3. **Fail open** on internal errors (missing `python3`, malformed JSON,
   `git` not available) — a hook should never wedge the whole session over
   its own bug. Reserve hard blocks (`exit 2`) for the specific invariant
   the hook exists to protect.
4. Make it executable: `chmod +x .claude/hooks/<name>.sh`.
5. `chmod -x` is the emergency kill-switch if a hook misbehaves — but treat
   that as a signal to fix the hook, not a permanent workaround.

## Creating a new sub-agent

Use the `new-agent` skill's pattern, or by hand:

1. Write `.claude/agents/<name>.md` with frontmatter describing scope,
   tools available, and 3-5 worked examples of when to (and when NOT to)
   dispatch it.
2. Keep sub-agents narrowly scoped — one domain, bounded tool access, and a
   clear "returns a bounded digest" contract so dispatching them doesn't
   just move the context bloat from the main session into a subagent call
   you still have to read.

## Memory (`.claude/memory/`)

Durable facts that should survive across sessions without being reloaded
every single turn (unlike rules, which always load). Four kinds, same as
the harness's personal-memory convention:

- **user** — who's working on this, their role/expertise
- **feedback** — corrections/confirmations about HOW to work here
- **project** — in-flight decisions, deadlines, ongoing initiatives
- **reference** — pointers to where things live in external systems

Keep `.claude/memory/MEMORY.md` as a one-line-per-entry index; put the
actual content in one file per memory under `.claude/memory/<slug>.md`.
Commit both to git — this is TEAM memory, not personal memory (personal
memory still lives in `~/.claude/`).

## Load this skill when

- Creating a new rule, skill, hook, sub-agent, or memory entry.
- Deciding where a piece of project knowledge belongs.
- Reviewing existing `.claude/` content for correctness or drift.

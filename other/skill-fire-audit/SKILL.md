---
name: skill-fire-audit
description: Use when asked which skills or plugins are actually being used, before installing or pruning skills, or on a periodic library review. Measures real invocations from session transcripts instead of guessing, and refuses to archive anything without a reference check.
triggers: which skills fire, skills actually used, skill usage, plugin usage, installing skills, pruning skills, library review, invocations from transcripts, archive skills, routing trigger, fire rate, dead skills, uninstall candidates
---

# skill-fire-audit

Measures which skills and plugins actually fire, from session transcripts. Read-only —
it proposes, it never moves anything.

Baseline from the 2026-08-03 pass (9 weeks, 2,189 transcripts, 67,051 user messages):
**46 of 1,307 skill names ever fired = 3.5%.** Project skills fired at **64%** — 18x the
installed library. If a later run shows the project cohort dropping toward the global
rate, the project skills have gone stale; that is the signal worth watching.

## Run it

```bash
python .claude/skills/skill-fire-audit/scripts/fire_audit.py
python .claude/skills/skill-fire-audit/scripts/fire_audit.py --days 60 --json audit.json
```

Run from the repo root — it picks up `.claude/skills`, `.agents/skills`,
`apps/*/.claude/skills`, plus the user-scope and plugin roots.

## Reading the output

- **Fire rate by scope** — project cohort should lead by a wide margin. It is the
  headline number.
- **Live skills with no routing trigger** — skills that fire *despite* a bad description,
  usually because you type them as a slash command. Fixing these is the cheapest win;
  ignore the description quality of skills nobody uses.
- **Plugins with zero skill usage** — candidates only. Verify MCP before acting.

## Before archiving anything

Five rules, each written after it cost a session:

1. **Reference-check candidates against what you are keeping.** On 2026-08-03 this
   rejected 44% of them, including all 9 persona skills — `multi-advisor` convenes them.
2. **Check referrer liveness, not just presence.** `multi-advisor` was "referenced by two
   skills"; both had never fired. Dead text is not a dependency.
3. **Read the file before judging it by a number.** Word count ranked a customized
   `brainstorming` (tool-restricted, hard gate, review date) below a generic plugin copy
   and recommended deleting it.
4. **Never hand-move plugin files.** Plugin state lives in three places —
   `installed_plugins.json`, the cache dir, and `settings.json` `enabledPlugins` — and a
   running Claude Code re-syncs them. Half an uninstall leaves entries pointing at
   directories that no longer exist. Use `/plugin` with the app closed.
5. **Archive by moving, with a `restore.ps1`.** Never delete.

## What this cannot tell you

A slash invocation counts as usage; ambient context injection does not appear at all.
An auth-gated MCP server showing zero calls means "never authenticated" as often as
"unwanted" — that reading cannot justify an uninstall.

Config prose does not cause invocation. Naming a skill in `CLAUDE.md` without an
invokable name and a real trigger produces zero fires; that was the root cause the
first audit found. Fix the description, not the exhortation.

Related: [prod-db-guard](../prod-db-guard/SKILL.md) for the same read-before-you-run
discipline applied to databases.

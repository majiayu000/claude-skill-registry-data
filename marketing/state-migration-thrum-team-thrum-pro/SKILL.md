---
name: state-migration
description: "Use when your agent-local thrum state is empty AND you have an existing State.md file in your agent directory - this is a ONE-TIME conditional onboarding that fires only on that exact combination. Do NOT use if thrum state already has entries (nothing to migrate) or if you have no State.md (brand-new agent, nothing to migrate). Triggers on - first session after the thrum state redesign lands, `thrum state list` returning empty while State.md exists on disk, being asked to migrate your personal state."
---

# Migrating personal State.md into `thrum state`

This is a conditional, one-time onboarding — modeled on the philosophy-
document onboarding pattern. It does nothing if either half of its trigger
condition is false.

## When this fires

- `thrum state list` returns **empty** for your agent AND
- a `State.md` file exists in your agent directory (readable via
  `substrate.read_folder` or a direct file read, per your runtime).

If `thrum state list` already has entries: **stop, nothing to migrate.**
If no `State.md` exists: **stop, you're a brand-new agent, nothing to
migrate.**

## What to do

Read your `State.md`. For each of its six canonical sections (Identity,
Current state, Immediate next actions, Durable / structural facts,
Personal-relevance memory index, Cold-successor note), write it into the
`personal_state` kind:

```bash
thrum state set --kind personal_state --scope self --value '{
  "identity": "<Identity section content>",
  "current_state": "<Current state section content>",
  "next_actions": "<Immediate next actions section content>",
  "durable_facts": "<Durable / structural facts section content>",
  "memory_index": "<Personal-relevance memory index section content>",
  "cold_successor": "<Cold-successor note section content, or omit if empty>"
}'
```

Value size is capped at 64KB — this replaces the old 60-line cap; if
State.md is over cap, trim the same way the old cap's error message
directed (never trim Durable / structural facts).

After migrating, `State.md` itself is no longer read by anything — leave it
in place (harmless) or delete it; do not keep updating it, since nothing
consumes it anymore.

## Do not

- Run this if `thrum state list` already shows a `personal_state` entry —
  a second run would overwrite (upsert semantics), silently discarding
  anything written to `thrum state` since the last migration.
- Bulk-import on behalf of another agent. This is self-driven, scoped to
  the live agent running the skill.

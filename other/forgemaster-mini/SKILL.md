---
name: forgemaster-mini
description: Trimmed Forge pipeline (scope → build → wrap) for small, clear-scope work. Use when the user runs /forgemaster-mini or has a small, well-scoped task.
---

# /forgemaster-mini — Trimmed Forge pipeline for small tasks

Run the **low-ceremony** Forge path for small, clear-scope work (bugs, chores, config, single-file
changes). Same Beads + TDD discipline as the full pipeline, but collapsed into three lightweight
steps — scope → build → wrap — with far fewer turns, gates, and artifacts to keep cost down.

Use this directly when you already know the task is small. For anything medium-or-higher, use
`/forgemaster` (which can also auto-route here).

## Usage

Accepts the same inputs as `/forgemaster` — a **JIRA ticket**, a **Beads issue id**, or a
**free-text description**.

```
/forgemaster-mini <task description>    # free text
/forgemaster-mini <BEADS-ID>            # e.g. agent-forge-harness-f25 → run mini against that issue
/forgemaster-mini <JIRA-KEY>            # e.g. PROJ-1234 → mirror into Beads, then run mini
```

## What to do

Follow **`.claude/workflows/forge-mini.md`** in full. In short:

1. **Preflight** — `bd ready >/dev/null`; if it errors, `bd dolt start` and retry. Beads is required.
2. **Scope** — read only the touched files; ask **at most one** decision question (lead with the
   plain-language *why*, then options); state the approach inline. **Resolve the input to one Beads
   task**: `bd show` an existing id, *mirror* a JIRA key into Beads (`--external-ref jira-<KEY>`,
   pasting the ticket if no JIRA integration is configured), or create a new task for free text —
   then `--claim` it (priority via `.claude/skills/beads-priority-assignment/SKILL.md`). Confirm the
   approach once.
3. **Build** — TDD via `.claude/skills/tdd/SKILL.md` (vertical slices) for code; one runnable demo;
   `worklog:` comment; commit with tests.
4. **Wrap** — quality gates, close the task with evidence, push (+ PR if warranted), `bd dolt push`,
   and report inline: what changed, how to verify, Beads id + PR link.

No `plans/` or `reports/` doc files and no `forge:phase-gate` / run state file — tracking lives in
Beads. **Escalate** to the full pipeline (`/forge-research <slug>`) if the work outgrows "mini".

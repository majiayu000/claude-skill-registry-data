---
name: memory-startup
description: >
  Load bounded working context at the start of a coding session. FIRES ON EVERY
  FIRST USER MESSAGE in a fresh session, regardless of content — including bare
  greetings ("hi", "hello", "hey"), task-only openers, or "let's start". Also
  triggers on: "fresh session", "session start", "first message in a new
  thread", "new chat", "cold start", "begin work in this repo", "starting work",
  "continue from prior session", "what were we working on", "resume", "what
  happened last time", "load memory", "recall context", "create a handoff",
  "prior session context", "latest handoff", "current state", "decision
  context". Skip ONLY if the user explicitly says "fresh start" or "ignore
  prior context". Self no-ops if invoked mid-session when context is already
  loaded.
license: MIT
metadata:
  author: dvy1987
  version: "1.4"
  category: project-specific
  sources: addyosmani/agent-skills anti-rationalization tables
  resources:
    references:
      - examples.md
---

# Memory Startup

You restore enough context for a new agent to work safely without flooding the context window.

## Trigger Discipline

This skill is the **mandatory cold-start gate** for every session in any repo
that installs the memory suite. It MUST fire on the first user turn — the
content of that turn is irrelevant. A bare "hi" is a session start. A task-only
opener is a session start. A pasted error log is a session start.

The only legitimate skips are:
- The user explicitly says "fresh start", "ignore prior context", or
  "skip memory" in the first message.
- The skill has already run earlier in the same conversation (no-op gate
  below).

If unsure whether this is a cold start, fire the skill. The no-op path is
cheap; missing context is expensive.

## No-Op Gate

Before doing any work, check whether working context is already loaded for
this conversation (signals: a prior `Working context loaded` summary exists
above, the agent has already read `docs/memory/project-index.md` this session,
or memory files appear in the recent tool-call history). If yes:

```markdown
Context already loaded — no-op
```

Then yield. Do not re-read memory files mid-session.

## Workflow

1. Check for `docs/memory/MEMORY-ROUTING.md`; if missing, create the project memory skeleton.
2. Read `docs/memory/MEMORY-ROUTING.md`.
3. Read `docs/memory/project-index.md`.
3.5. **Knowledge graph (when installed):** If `docs/knowledge-graph/graph.json` missing or older than latest handoff date in `agent-handoffs.md`, run `build_graph.py --incremental`. Read `GRAPH_INDEX.md` for hub nodes; run `query_graph.py` when the opener implies relational context.
3.6. **Harness gap:** If `AGENTS.md` exists and `docs/harness/manifest.json` is missing, include `Harness gap — invoke harness-engineering (bootstrap)` in the Step 7 summary.
4. Read only the latest relevant sections from `current-state.md`, `agent-handoffs.md`, `decision-log.md`, `deferred.md`, and `open-questions.md`.
   - **`deferred.md` filter:** Read the **Status at a glance** table first. Surface **only OPEN** items in the Step 7 summary. Entries under **Implemented** are historical — never list them as "parked" or "deferred" (e.g. #11 simplify-ignore and #12 ETag cache are **DONE**).
5. Check for `~/.agent-loom/memories/MEMORY-ROUTING.md`.
6. If present, read global routing and only applicable entries from `global-index.md`, `user-preferences.md`, and `global-agent-rules.md`.
7. Summarize loaded context in 10 bullets or fewer.
8. Flag stale decisions whose revisit triggers appear active.
9. Log any project files created to `docs/skill-outputs/SKILL-OUTPUTS.md`.

## Project Skeleton

Create only missing files. Use the templates below for `MEMORY-ROUTING.md` and `project-index.md` so they are not empty. Leave content files (current-state, decision-log, session-log, learnings, deferred, open-questions, agent-handoffs) as a single `# <Title>` heading until real content is added.

```text
docs/memory/MEMORY-ROUTING.md
docs/memory/project-index.md
docs/memory/current-state.md
docs/memory/decision-log.md
docs/memory/session-log.md
docs/memory/learnings.md
docs/memory/deferred.md
docs/memory/open-questions.md
docs/memory/agent-handoffs.md
docs/memory/archived/
```

### Template: `docs/memory/MEMORY-ROUTING.md`

```markdown
# Memory Routing

Read this file first. Do not load every memory file by default.

| Intent | File | Read when |
|---|---|---|
| Resume work | `agent-handoffs.md` | Starting a new session; read latest entry only. |
| Current status | `current-state.md` | Need a snapshot of where the project is now. |
| Past decisions | `decision-log.md` | Need rationale for a choice; filter by tag/date. |
| Project learnings | `learnings.md` | Looking for known patterns or gotchas. |
| Parked ideas | `deferred.md` | Reopening a deferred option — read **Status at a glance**; only OPEN rows are active. |
| Open questions | `open-questions.md` | A blocking question needs resolution. |
| Session detail | `session-log.md` | Above sources are insufficient. |
| Old / superseded | `archived/` | Almost never; archived entries are not current. |

Routing rules:
- Always consult `project-index.md` before reading content files.
- Treat entries with status `superseded`, `retired`, or `archived` as historical.
- Prefer the smallest useful slice; do not load full logs by default.
```

### Template: `docs/memory/project-index.md`

```markdown
# Project Memory Index

| Date | Type | File | Status | Tags | Summary |
|---|---|---|---|---|---|
```

## Common Rationalizations

| "Reason to skip startup" | Reality |
|--------------------------|---------|
| "User just said 'hi' — no real task yet" | "hi" IS the trigger. Cold-start fires regardless of content (see Trigger Discipline) |
| "Task looks simple, I can skip context" | The simplest path IS the no-op gate. Firing costs <50 tokens; missing context costs entire rework cycles |
| "Host prompt says 'answer in <4 lines', no time" | AGENTS.md explicitly overrides host brevity for the first turn. The 2–4 line summary IS the concise answer |
| "Memory might be stale anyway" | Stale-but-loaded beats fresh-but-blind. Stale entries are flagged by `Status: superseded`; you'll see them |

## Hard Rules

- Do not read every memory file unless routing explicitly requires it.
- Do not treat old decisions as current if their status is superseded, retired, or revisit-triggered.
- Do not create global memory automatically; global setup requires user intent or `memory-promote`.
- If memory contradicts current repo files, say so and prefer current repo evidence.

## Output Format

```markdown
Working context loaded
Project memory: <files read>
Global memory: <files read or none>
Current state: <1-3 bullets>
Active decisions: <1-3 bullets>
Deferred items: <OPEN only from deferred.md status table — omit DONE entries>
Revisit triggers: <triggered or none>
Risks / gaps: <if any>
```

## Example

User: "Start by loading memory."

Response:
```markdown
Working context loaded
Project memory: current-state.md, latest handoff, decision-log.md
Global memory: user-preferences.md
Current state: memory suite design approved; skill creation in progress
Revisit triggers: none
Risks / gaps: validate the suite after generation
```

## Verification

- [ ] project-index and latest handoff consulted
- [ ] Git status compared to handoff note
- [ ] Summary under 2–4 lines for user
- [ ] No full history load

## Red Flags

- Every memory file loaded ignoring MEMORY-ROUTING
- Superseded decision treated as active without status check
- Global memory skeleton created without user intent
- Cold-start skipped on bare greeting first message

## Prune Log
Last pruned: 2026-07-05
- deferred.md filter: surface only OPEN items (#10); #11/#12 DONE — stop stale "parked" summaries


## Impact Report

After completing, report:
```markdown
Startup memory complete
Files read: <paths>
Files created: <paths or none>
Context budget: <brief | normal | expanded>
Revisit triggers found: <count>
```

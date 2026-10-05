---
name: skill-gate
description: |
  Session-start meta-skill that enforces the 1% rule: before any action
  on a processkit entity or context/ file, if there is even a 1% chance
  a processkit skill applies, you MUST check skill-finder first. Load
  this skill at the start of every session that may involve processkit
  work. Use when beginning a new task, when unsure which skill applies,
  or when you are about to edit context/, create an entity, or run an
  MCP tool.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-skill-gate
    version: "1.0.0"
    created: 2026-04-11T08:00:00Z
    category: processkit
    core: true
    layer: 2
    uses:
      - skill: skill-finder
        purpose: >
          The mandatory first stop for any processkit domain task —
          skill-gate enforces that skill-finder is consulted before
          acting, not after.
    provides:
      primitives: []
      mcp_tools: [acknowledge_contract, check_contract_acknowledged]
      assets: []
    commands:
      - name: pk-build
        args: ""
        description: "Run the project build command from the AGENTS.md pk-commands block"
      - name: pk-lint
        args: ""
        description: "Run the project lint command from the AGENTS.md pk-commands block"
      - name: pk-test
        args: ""
        description: "Run the project test command from the AGENTS.md pk-commands block"
      - name: pk-review
        args: ""
        description: "Review the current branch against AGENTS.md conventions; report blockers / warnings / notes"
---

# Skill Gate

## Intro

skill-gate is the enforcement layer that ensures agents consult the
processkit skill catalog before acting on processkit entities or
`context/` files. It implements the **1% rule**: if there is even a 1%
chance a processkit skill covers the current task, you must check
`skill-finder` before doing anything else. It does not perform work
itself — it ensures work is performed via the right skill.

## Overview

### The processkit Compliance Contract (v2)

AGENTS.md ships a ToC of this contract; the authoritative rules live
here. Every session that touches processkit entities or `context/`
files is governed by all ten:

1. **route_task before writes.** Call `route_task(task_description)`
   before any `create_*`, `transition_*`, `link_*`, `record_*`, or
   `open_*` tool call.
2. **1% rule.** If there is even a 1% chance a processkit skill
   applies, consult `skill-finder` (or call `find_skill`) before
   acting.
3. **Commit to entity creation in the same turn.** When you decide to
   create a WorkItem, DecisionRecord, Note, or Artifact, call the tool
   in the same turn — deferred entity creation is lost.
4. **Write via MCP.** Write entities through MCP tools, not by
   hand-editing files under `context/` — hand edits bypass schema
   validation, state-machine enforcement, and the event-log auto-entry.
5. **Read via index.** Read entities through `index-management`
   (`query_entities`, `get_entity`, `search_entities`) — do not use
   `ls`, `grep`, or raw filesystem walks under `context/`.
6. **Log after state changes.** Log an event after any state change
   that an MCP write did not already produce automatically.
7. **Record accepted cross-cutting decisions.** After a cross-cutting
   recommendation is accepted, call `record_decision` in the same turn.
8. **Acknowledge decision language.** When the last five user messages
   contain explicit decision language (approved / decided / ship it /
   let's go / ok / yes / confirmed), either call `record_decision` in
   the same turn or call `skip_decision_record(reason=...)` to
   acknowledge the skip.
9. **Templates are read-only.** Do not edit any file under
   `context/templates/` — it is a read-only upstream mirror used as a
   diff baseline.
10. **Don't hand-edit merged MCP config.** Edit the per-skill
    `mcp-config.json` and let the installer re-merge.

Compatibility shims in schemas, doctor checks, or harness adapters are
temporary migration aids only. The accepted end state is canonical
processkit data: declared schema vocabulary, canonical IDs and
filenames, canonical directory layouts, and resolvable references.
When a shim reveals drift, use the relevant processkit skill to create
or apply a migration; do not treat grandfathering as a terminal
resolution.

### The 1% rule

Before any of the following actions, pause and apply the decision graph:

- Editing or creating any file under `context/`
- Calling any processkit MCP tool (`create_*`, `transition_*`, `link_*`,
  `record_*`, `open_*`)
- Writing a WorkItem, Decision, Note, Artifact, or any other entity
- Running a process the user described as a processkit task

**The rule:** If there is even a **1% chance** a processkit skill
applies to this task, you MUST check `skill-finder` before proceeding.

The threshold is deliberately near-zero. Do not rationalize past it.

### Decision graph

```
Is this task related to processkit entities, context/ files,
or any process the user described as a project-management task?
│
├─ YES (or unsure) ──→ Read skill-finder and identify the matching skill.
│                       Load that skill. Work from it.
│
└─ NO ──────────────→ Proceed without skill-gate involvement.
                       (Pure code edits, data analysis, etc. that have
                       no processkit component do not need skill-gate.)
```

### What "check skill-finder" means

1. Read `context/skills/processkit/skill-finder/SKILL.md` — find the
   trigger phrase that matches the current task.
2. Load the identified skill's `SKILL.md`.
3. Confirm from its **Intro** (3 sentences) that it is the right match.
4. Work from that skill's **Overview** — not from general knowledge.

If `skill-finder` has an MCP server available (`find_skill` tool), call
it instead of reading the file — it is faster and more reliable.

### Pre-empting common rationalisations

These are the rationalizations agents use to skip skill-gate. Each one
is wrong:

| Rationalisation | Reality |
|---|---|
| "I already know how to do this." | The skill may have processkit-specific entity paths, ID formats, MCP tools, and log conventions that general knowledge does not cover. Knowing the domain is not the same as knowing the processkit conventions for it. |
| "It's a simple edit — one line." | The state machine enforces valid transitions. A hand edit that bypasses the MCP server can put an entity in an invalid state, break the index, and skip the auto-log side effect. |
| "skill-finder won't have a match for this." | The catalog has 128+ skills. Check before assuming. If there genuinely is no match, `skill-builder` is the next step — not acting from general knowledge. |
| "The user told me exactly what to do." | User instructions describe intent, not process. The skill encodes the processkit-specific conventions for realizing that intent correctly. |
| "I've done this before in this session." | Skill-gate applies to each new task type, not just the first one. If the task domain shifts, check again. |

### Mandatory skill-check task classes

Before starting any task in the following categories, call
`find_skill(<task-keyword>)` / `list_skills()` (or
`search_entities(kind=skill, text=<task-keyword>)` via index-management)
— even if you think you know the procedure:

1. **Research ingestion** — importing notes, papers, or external
   artefacts into the project context.
2. **Artifact creation** — producing a new PRD, ADR, spec, brief, or
   any structured output file.
3. **Discussion management** — opening, advancing, or closing a
   structured discussion thread.
4. **Decision recording** — capturing a cross-cutting decision in a
   DecisionRecord entity.
5. **Backlog item creation** — adding a WorkItem, Epic, or task to
   the backlog.
6. **Quality audits** — reviewing a skill, process, schema, or
   compliance artifact.

This list is not exhaustive — the 1% rule applies to every task, not
just these six. The list names the classes where bypassing the catalog
has caused the most observed work-waste.

### Escape hatch

skill-gate does NOT apply when you are already operating inside a
named processkit skill's workflow. If you loaded `workitem-management`
and are following its Overview steps, you do not need to re-check
skill-finder for each sub-action within that skill. Skill-gate is a
session-level gate, not a per-tool-call gate.

## Gotchas

- **Treating skill-gate as optional at session start.** It is not. If
  this session may involve any processkit work, load skill-gate first.
  The cost is one file read. The cost of skipping it is a hand edit
  that bypasses schema validation, state-machine enforcement, index
  sync, and the audit trail.
- **Applying the 1% rule only to obvious processkit tasks.** "Write a
  standup" and "create a ticket" are obvious. "Quick note about this
  idea" (→ `note-management`), "log that we deployed" (→ `event-log`),
  and "check what's blocking us" (→ `workitem-management`) are not
  obvious but all have matching skills. When in doubt, check.
- **Confusing skill-gate with skill-finder.** skill-gate enforces the
  checking behaviour. skill-finder does the matching. They are distinct.
  skill-gate tells you *when* to check; skill-finder tells you *what*
  to use.
- **Skipping skill-gate because the user said "just edit the file."**
  The user describes the outcome they want, not the correct processkit
  process for achieving it. Hand-editing entity files bypasses the MCP
  server's schema validation and state-machine enforcement. Use the MCP
  tool unless the MCP server is explicitly unavailable.
- **Forgetting that skill-gate applies to entity creation, not just
  edits.** Writing a new YAML file under `context/workitems/` directly
  is a hand edit. Even for new entities, use `create_workitem` (or the
  relevant `create_*` tool) so the index stays in sync and the auto-log
  fires.
- **Applying the escape hatch too broadly.** The escape hatch covers
  sub-actions *within* a skill you have already loaded and are actively
  following. It does not cover switching to a different task type or
  domain mid-session without re-checking.

## Full reference

### Why the threshold is 1%, not "when clearly applicable"

A higher threshold — "check skill-finder when the task is obviously a
processkit task" — fails because agents are systematically overconfident
about what they already know. The 1% rule removes the judgment call
entirely. If there is any possibility, check. The marginal cost of an
unnecessary skill-finder lookup is one file read (seconds). The cost of
skipping it when it was needed is an out-of-sync index, an invalid
entity state, or a missing audit trail entry.

### Provider neutrality

skill-gate is implemented entirely in prose — it makes no assumptions
about which AI harness loads it. The same behaviour applies whether the
agent is Claude Code, Codex CLI, Cursor, or any other harness that
reads SKILL.md files.

### Relationship to AGENTS.md

AGENTS.md carries the project-level instruction to load skill-gate
at session start. skill-gate carries the enforcement logic. Keep them
separate: AGENTS.md says *when* to load skill-gate; skill-gate says
*what to do* once loaded.

### When skill-gate applies to non-processkit projects

skill-gate is a processkit-specific skill. It is only meaningful in
projects that have processkit installed (i.e. that have a `context/`
directory with processkit entities). In projects without processkit,
skill-gate should not be loaded.

### Context directory layout

All processkit-installed material lives under `context/`:

```
context/
├── skills/         ← skill packages (SKILL.md, mcp/, references/, templates/)
├── schemas/        ← JSON schemas for the core primitives
├── state-machines/ ← state-machine definitions
├── processes/      ← process definitions (bug-fix, code-review, release, …)
└── templates/      ← immutable upstream mirror used as a diff baseline
```

`context/templates/processkit/<version>/` is the verbatim upstream
snapshot. **Do not edit it.** Edit the live files at
`context/skills/<name>/SKILL.md`, `context/processes/<name>.md`, etc.,
directly. Local edits are detected at the next sync via three-way diff
against the templates mirror.

Every `context/` subdirectory has an `INDEX.md`. **Read those first** —
do not slurp `context/skills/` or any large directory at session start.
Load specific files only when the task demands it. This is the
three-level principle: start at Level 1 (intro), drop to Level 2
(workflows) when the task narrows, drop to Level 3 (full reference) for
edge cases.

### Working with entities

processkit models project state as **entities** — work items, decision
records, discussions, log entries, scopes, gates, bindings, and so on.
Each entity is a YAML file under `context/<kind>s/`, created lazily on
first use. For each entity kind, processkit ships a schema at
`context/schemas/<kind>.yaml`, a state machine at
`context/state-machines/<kind>.yaml`, and an MCP server at
`context/skills/<kind>-management/mcp/server.py`.

- **Read** entities through `index-management`: call `query_entities`,
  `get_entity`, `search_entities` — not `ls`, `grep`, or filesystem
  walks. The SQLite-backed index is faster, context-cheaper, and
  reflects canonical state.
- **Write** entities through the per-kind MCP servers:
  `create_workitem` / `transition_workitem`, `record_decision`, and so
  on. Hand-editing entity files bypasses index updates and
  state-machine validation. Reserve hand edits for cases the MCP tools
  genuinely don't cover — and call `reindex()` after so the SQLite
  index reflects the new state.
- **Log an event** after any state change that an MCP write did not
  already produce automatically (via `event-log`'s `log_event` tool).

### MCP server wiring

Each MCP-bearing skill ships its own `mcp/mcp-config.json` declaring
how to launch the server (typically `uv run …/server.py`). Agent
harnesses (Claude Code, Codex CLI, Cursor, …) read a single merged MCP
config at startup, so the per-skill blocks must be merged and placed at
the harness-specific path. If an installer set the project up (for
example a managed devcontainer), the installer owns that wiring; if
processkit was installed manually, the project owner merges the blocks
by hand. Either way, MCP-bearing skills require **`uv`** and **Python
≥ 3.10** on PATH — each `server.py` is a PEP 723 script and `uv run`
resolves dependencies on first launch. Do not hand-edit the generated
merged harness config; edit per-skill `mcp-config.json` and let the
installer re-merge.

## How the gate is enforced

skill-gate uses three complementary enforcement mechanisms. They are
layered, not alternatives — use whichever the harness supports.

### (a) Prose fallback — the 1% rule

The primary enforcement mechanism is this SKILL.md itself. Every AI
harness that loads SKILL.md receives the 1% rule in natural-language
form: if there is even a 1% chance a processkit skill applies, check
`skill-finder` first. Prose enforcement is provider-neutral — it works
on Claude Code, Codex CLI, Cursor, and any harness that reads SKILL.md
files. It requires no MCP support. The cost is that it is advisory:
a harness that never loaded this file (or ignored it) has no hard
barrier.

### (b) Tool-call acknowledgement via `acknowledge_contract()`

When the harness speaks MCP, a stronger enforcement layer is available
via the `processkit-skill-gate` MCP server (`mcp/server.py`). Call
`acknowledge_contract("v1")` once per session before any write-side
processkit tool. On success the server writes a session marker file at:

```
context/.state/skill-gate/session-<SESSION_ID>.ack
```

The marker contains `contract_hash` and `acknowledged_at` (see
`mcp/SERVER.md` for the full schema). CI and harness hooks
(`SteadyHand`'s `check_route_task_called.py`) read this directory to
confirm that a compliance acknowledgement was recorded for the session.
The companion tool `check_contract_acknowledged()` can be called by
any write-side tool implementation to gate on acknowledgement before
proceeding.

Session ID is resolved from env var `PROCESSKIT_SESSION_ID` or
`os.getpid()` — one MCP stdio server process equals one session.

### (c) Optional tool-side preconditions on write tools (future)

A planned follow-up (separate WorkItem) will wire `check_contract_acknowledged()`
as a precondition check inside each write-side MCP tool
(`create_workitem`, `record_decision`, `log_event`, etc.) so that
calling a write tool without a prior `acknowledge_contract()` in the
same session returns an error rather than proceeding silently. This is
intentionally out of scope for the current implementation to allow the
acknowledgement pattern to soak before hard-blocking write tools.

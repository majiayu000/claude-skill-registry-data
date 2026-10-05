---
name: task-router
description: >
  Route a task description to the right processkit skill, project-specific
  process override, and MCP tool in a single deterministic call — use this
  at the start of every processkit domain task.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-task-router
    version: "1.0.0"
    created: 2026-04-11T00:00:00Z
    category: processkit
    layer: 1
    core: true
    provides:
      mcp_tools:
        - route_task
---

# Task Router

## Intro

`task-router` is the primary routing entry point for processkit agents.
Call `route_task(task_description)` once at the start of any domain
task. It returns — in a single call, without an LLM — the matching
skill, the legacy project-specific process override (if any), and the
recommended MCP tool. Use it instead of calling `find_skill()` directly.

## Overview

### When to use

Call `route_task()` before any `create_*`, `transition_*`, `link_*`,
or `record_*` MCP tool. The 1% rule applies: if there is even a 1%
chance a processkit skill covers this task, route first.

### Routing algorithm

Two-phase heuristic, no LLM call required:

1. **Phase 1 — domain group match** (cheap keyword classifier).
   Scores the task against 13 domain groups by keyword overlap.
   Eliminates ~90% of candidates in one pass.

2. **Phase 2 — tool ranking** (token overlap or local embedding-style
   cosine scoring within the matched group). Scores the ~3–6 tools in
   the matched group. Returns the top tool with rationale and two
   runner-up candidates.

3. **Fallback** — if no group scores ≥ 0.3, falls back to the
   skill-finder trigger-phrase table for cross-domain or meta tasks.

### Reading the result

| Field | What it means |
|---|---|
| `skill` | Load this skill's SKILL.md before acting |
| `skill_description_excerpt` | First 150 chars of skill description — judge fit without loading the full file |
| `process_override` | Legacy v1 compatibility. If present, read this file before the skill; it contains project-specific overrides from `context/processes/` |
| `process_override_status` | Present with `process_override`; currently `legacy-v1` |
| `tool_qualified` | `{server}__{tool}` — collision-safe tool identifier |
| `confidence` | 0.0–1.0 geometric mean of group and tool scores |
| `routing_basis` | `keyword_match` = confident; `needs_llm_confirm` = escalate to user/LLM |
| `candidate_tools[]` | Top-3 scored tools with rationales for fallback |

### When `confidence < 0.5`

`routing_basis` will be `needs_llm_confirm`. Show `candidate_tools[]`
to the user or pass them to an LLM for disambiguation. Do NOT call a
`create_*` tool without confirmation when confidence is low.

Callers may pass `allow_llm_escalation=true`; the router then returns a
`llm_escalation` status with the configured `fast` model class hint. The
stdio MCP server does not make provider network calls itself, so the caller
owns the actual cheap-model confirmation step.

### When `process_override` is present

Read the process override file **before** the generic skill. It
contains project-specific step overrides, gates, and blockers that
supersede the skill defaults.

This is a legacy v1 compatibility surface. v2 processkit releases do not
ship first-class Process entities or `src/context/processes/`. Existing
projects may still carry live `context/processes/*.md` files as migration
source state; when found, the router returns them with
`process_override_status: legacy-v1`.

## Gotchas

- **Do not call `find_skill()` directly** in normal flow — `route_task()`
  calls it internally as a fallback. Direct `find_skill()` calls skip
  the process override lookup and the domain group fast path.
- **Low confidence is a signal, not a failure.** Confidence < 0.5 means
  the task straddles multiple domains or uses uncommon vocabulary. Use
  `candidate_tools[]` to present options.
- **Task description quality matters.** Verb-noun phrases score best:
  "create work item", "record decision", "log event". Single words
  ("task", "log") are ambiguous — add context.
- **Process overrides are compatibility data.** Do not create new v2
  Process entities for router overrides. Prefer skill configuration,
  definition Artifacts, or WorkItems that describe process instances.

## Full reference

### MCP server

See `mcp/SERVER.md` for tool schema and return-shape details.

### Domain groups

The 13 registered groups: `workitem`, `decision`, `discussion`,
`event`, `actor`, `scope`, `index`, `skill`, `gate`, `model`,
`id`, `role`, `binding`.

### Extending the router

To add a new domain group:
1. Add an entry to `DOMAIN_GROUPS` in `mcp/server.py`.
2. Add trigger phrases to the `skill-finder` trigger table.
3. Run the smoke tests: `uv run scripts/smoke-test-servers.py`.

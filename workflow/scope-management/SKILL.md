---
name: scope-management
description: |
  Manage Scope entities — bounded containers grouping related work (sprint, milestone, project, quarter). Use when creating or updating a grouping boundary — sprint, milestone, quarter, project, release — that other entities will reference.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-scope-management
    version: "1.0.0"
    created: 2026-04-06T00:00:00Z
    category: processkit
    layer: 2
    uses:
      - skill: event-log
        purpose: Log events to keep the audit trail accurate after every write.
      - skill: index-management
        purpose: Query existing entities and keep the SQLite index fresh after writes.
      - skill: id-management
        purpose: Allocate unique entity identifiers via central ID generation.
    provides:
      primitives: [Scope]
      mcp_tools:
        - create_scope
        - get_scope
        - transition_scope
        - list_scopes
      templates: [scope]
---

# Scope Management

## Intro

A Scope is a named, bounded container that groups related entities — a sprint,
a milestone, a project, a release, a quarter. WorkItems, Processes, and
Bindings reference scopes to say "I apply within this container."

> **MCP server.** This skill ships a self-contained MCP server at
> `mcp/server.py` (PEP 723 script — requires `uv` and Python ≥ 3.10 on
> PATH). Agent harnesses reach its tools by reading a single MCP config
> file at startup, so the contents of `mcp/mcp-config.json` must be merged
> into the harness's MCP config and placed at the harness-specific path
> before this skill is usable. If processkit was installed by an installer,
> that wiring is the installer's responsibility; if processkit was
> installed manually, the project owner must do it by hand.

## Overview

### Kinds of scopes

| kind        | Example                                     |
|-------------|---------------------------------------------|
| `sprint`    | 2-week iteration boundary                   |
| `milestone` | Named delivery target                       |
| `quarter`   | Calendar quarter for OKRs                    |
| `project`   | Long-lived initiative                       |
| `release`   | A specific release version                   |
| `other`     | Custom boundary                             |

### Shape

```yaml
---
apiVersion: processkit.projectious.work/v2
kind: Scope
metadata:
  id: SCOPE-sprint-42
  created: 2026-04-01T00:00:00Z
spec:
  name: "Sprint 42"
  kind: sprint
  state: active
  starts_at: 2026-04-01
  ends_at: 2026-04-14
  description: "Two weeks focused on the lint command and docs-site bootstrap."
  goals:
    - "Ship aibox lint v1"
    - "Publish processkit docs-site"
---
```

### Workflow

1. Pick an ID: `SCOPE-<short-name>` (e.g., `SCOPE-sprint-42`, `SCOPE-q2-2026`).
2. Set `kind` and `state` (`planned`/`active`/`completed`/`cancelled`).
3. Set `starts_at` / `ends_at` for time-bounded scopes.
4. Write goals as concrete, testable bullet points.
5. Save to `context/scopes/`, log `scope.created`.

### Using scopes

Reference via `spec.scope: SCOPE-...` on WorkItems, or use a Binding
(`type: work-scope`) when the scope relationship is temporal and an item
can move in or out of scope during its lifetime.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Treating a Scope like a folder.** Scope is a conceptual
  container, not a directory. Don't move files based on scope
  membership; reference the SCOPE-ID from entities and let the
  index resolve membership.
- **Creating overlapping Scopes that double-count work.** "Sprint
  42" and "Q2 OKRs" can both contain the same workitem, but be
  explicit about which is the primary scope vs which is a
  secondary categorization. Otherwise reports double-count.
- **Using `spec.scope` directly when membership is temporal.** If a
  workitem moves into and out of a sprint over its lifetime, use a
  Binding (`type: work-scope`) instead of pinning `spec.scope`.
  The Binding carries `valid_from` / `valid_until`; the field
  doesn't.
- **Forgetting to transition Scope state.** Scopes have a
  lifecycle: `planned → active → completed → cancelled`. A Scope
  that says `state: active` for six months past its end date
  poisons every "what's the current sprint" query.
- **Hallucinating SCOPE-IDs.** When asked to add work to "the
  current sprint", call `list_scopes(state: active)` first. Don't
  invent `SCOPE-sprint-42` if it doesn't exist — create it
  explicitly via `create_scope`.
- **Reusing a Scope across different timeframes.** "Sprint 42" in
  Q2 2025 and "Sprint 42" in Q2 2026 are different Scopes — same
  number, different time. Use distinct IDs
  (`SCOPE-2025-Q2-sprint-42` and `SCOPE-2026-Q2-sprint-42`) so
  history is unambiguous.
- **Naming scopes ambiguously.** "Q1" without a year is meaningless
  in three months. Always include the year and the kind in the
  name; the ID can stay short.

## Full reference

### Fields

| Field         | Type          | Notes                                             |
|---------------|---------------|---------------------------------------------------|
| `name`        | string        | Human-readable. Shown in listings.                 |
| `kind`        | enum          | `sprint`/`milestone`/`quarter`/`project`/`release`/`other` |
| `state`       | enum          | `planned`/`active`/`completed`/`cancelled`         |
| `starts_at`   | date          | Optional. For time-bounded scopes.                 |
| `ends_at`     | date          | Optional.                                          |
| `goals`       | list[string]  | Concrete outcomes expected.                        |
| `description` | string        | Longer context.                                    |
| `parent`      | string        | Optional parent scope (quarter → sprint).          |

### Nested scopes

A sprint can be nested within a quarter via `spec.parent`. Queries resolve
transitively: "all work in Q2 2026" includes all sprints that sit inside it.

### Closing a scope

When a scope ends:
1. Set `state: completed`.
2. Log `scope.completed`.
3. Do not delete the file — historical WorkItems reference it.
4. Optionally write a retrospective DecisionRecord linked via
   `spec.related_decisions`.

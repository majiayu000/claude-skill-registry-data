---
name: workitem-management
description: |
  Create, transition, query, and link WorkItems — tasks, stories, bugs, epics. Use when the user asks to add, update, query, or link work items — backlog items, tasks, bugs, user stories, or epics.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-workitem-management
    version: "1.0.0"
    created: 2026-04-06T00:00:00Z
    category: processkit
    layer: 2
    uses:
      - skill: event-log
        purpose: Log events to keep the audit trail accurate after every write.
      - skill: actor-profile
        purpose: Resolve and validate Actor IDs referenced by this skill's entities.
      - skill: index-management
        purpose: Query existing entities and keep the SQLite index fresh after writes.
      - skill: id-management
        purpose: Allocate unique entity identifiers via central ID generation.
    provides:
      primitives: [WorkItem]
      mcp_tools: [create_workitem, transition_workitem, query_workitems, link_workitems]
      templates: [workitem, workitem-bug, workitem-story]
    commands:
      - name: pk-work
        args: "title [--type task|story|bug|epic] [--priority critical|high|medium|low]"
        description: "Create a new work item in the backlog with the given title"
---

# WorkItem Management

## Intro

WorkItems are the fundamental tracked unit of work in processkit — tasks,
stories, bugs, spikes, epics, tickets. This skill creates them, transitions
them through their state machine, links them to other entities, and queries
them.

> **MCP server.** This skill ships a self-contained MCP server at
> `mcp/server.py` (PEP 723 script — requires `uv` and Python ≥ 3.10 on
> PATH). Agent harnesses reach its tools by reading a single MCP config
> file at startup, so the contents of `mcp/mcp-config.json` must be merged
> into the harness's MCP config and placed at the harness-specific path
> before this skill is usable. If processkit was installed by an installer,
> that wiring is the installer's responsibility; if processkit was
> installed manually, the project owner must do it by hand.

## Overview

### When to create a WorkItem

Whenever the user (or you) identifies a distinct unit of work that should be
tracked. Don't create work items for every tiny thing — a WorkItem is worth
creating when it has:

- A clear title ("Add aibox lint command")
- A distinct state lifecycle (it starts somewhere, ends somewhere)
- Someone who should own it (even if not yet assigned)

If it's just a one-liner you're about to do in the next 30 seconds, don't
bother.

### WorkItem types

`spec.type` distinguishes subtypes:

| type    | When to use                                   |
|---------|-----------------------------------------------|
| `task`  | Default — generic unit of work                |
| `story` | User-facing feature framed as a user story    |
| `bug`   | Something that isn't working as intended      |
| `epic`  | Large body of work, parent of other WorkItems |
| `spike` | Time-boxed investigation with no committed deliverable |
| `chore` | Maintenance, cleanup, refactoring             |

### Creating

1. Pick the `type`.
2. Write a short, imperative `title`.
3. Provide `slug_summary` when available: 4-6 meaningful words that
   summarize the durable problem or outcome. The server validates this
   shape and turns it into the ID slug; if omitted, the title remains
   the backwards-compatible fallback.
4. Set `state` to the initial state (`backlog` by default).
5. Set `priority` if known (`critical`/`high`/`medium`/`low`).
6. Assign to an Actor (optional at creation).
7. Write the file to `context/workitems/BACK-<id>.md`.
8. Log `workitem.created`.

### Transitioning

The default state machine is:

```
backlog → in-progress → review → done
            ↓      ↑
          blocked ↑
            ↓      ↑
          backlog ←
(any state) → cancelled (terminal)
```

To transition:
1. Check the current state allows the transition (see `primitives/state-machines/workitem.yaml`).
2. Update `spec.state`.
3. Update `metadata.updated`.
4. Set `spec.started_at` on first entry to `in-progress` (if unset).
5. Set `spec.completed_at` when entering a terminal state.
6. Log `workitem.transitioned` with `from_state` and `to_state` in `details`.

### Linking

Four types of links, all expressed in frontmatter:

| Field                | Meaning                                                |
|----------------------|--------------------------------------------------------|
| `parent`             | This WorkItem is a child of a larger one (epic)        |
| `children`           | This WorkItem has sub-items                            |
| `blocks`             | This WorkItem blocks others until done                 |
| `blocked_by`         | This WorkItem cannot proceed until others are done     |
| `related_decisions`  | DecisionRecord IDs that motivated or constrain this    |

For scoped/temporal relationships (e.g. "Alice is assigned to this for sprint 42
only"), use a Binding instead of `spec.assignee`.

### Querying

Common queries the index MCP server will expose in Phase 3:

- All WorkItems in a given state
- All WorkItems assigned to an actor
- All WorkItems blocked (or blocking something)
- All WorkItems in a scope
- Full-text search across title + body

Before Phase 3, query via filesystem glob + grep of `context/workitems/`.

This skill also provides the `/pk-work` command for direct invocation —
see `commands/pk-work.md`.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Creating a WorkItem when the user hasn't asked to track work yet.**
  Sometimes the user is just thinking out loud. Don't translate every
  mention of "we should X" into a backlog entry. Ask: did the user
  explicitly say to track it, or did you decide to? If you decided, ask
  first. The Note primitive (when available) is the right home for
  half-formed ideas; WorkItem is for committed work.
- **Transitioning state without checking the state machine.** State
  changes that aren't allowed by `state-machines/workitem.yaml` will be
  rejected by the index, but a hand-edit can create an invalid state
  on disk. Always go through `transition_workitem` (the MCP tool),
  never edit `spec.state` directly. If the MCP server says no, the
  state machine is the source of truth — escalate to the user about
  the rule, don't bypass it.
- **Forgetting to log the transition event.** If you transition outside
  the MCP server (hand-editing for some reason), you must also write
  the corresponding LogEntry via `event-log`. The audit trail relies
  on this. Skipping it makes the index drift and breaks every later
  "what changed" query.
- **Creating duplicate workitems because you didn't query first.**
  Before `create_workitem`, run `query_workitems` against title and
  tags. The cost of one query is much smaller than the cost of an
  orphaned duplicate the user has to merge later.
- **Setting `priority: critical` on every bug.** "Critical" means
  drop-everything urgency. If everything is critical, nothing is.
  Default to `medium` and let the user upgrade.
- **Linking with `blocks` / `blocked_by` and forgetting the inverse.**
  These are bidirectional. If A blocks B, B is blocked_by A. The MCP
  server `link_workitems` enforces both sides — hand-edits often miss
  the inverse, leaving the index inconsistent.
- **Setting `assignee` on a WorkItem when the assignment is temporal.**
  "Alice owns this for sprint 42 only" is a Binding, not an assignee.
  Use a Binding entity for any time-bounded or scope-bounded
  assignment. Assignee is for "this is fundamentally Alice's
  responsibility, indefinitely".

(See also "Anti-patterns" in Full reference and the parent
state-machine documentation for the canonical transition rules.)

## Full reference

### Full field list

See `src/primitives/schemas/workitem.yaml` for the authoritative schema.
Every field there is valid in a WorkItem `spec`.

### State machine override

To customize the state machine, put a project-specific file at
`context/state-machines/workitem.yaml`. The index MCP server will prefer the
project file over the processkit default. Transitions not listed in the
custom machine are rejected.

### Estimates

`spec.estimate` is intentionally freeform:

```yaml
estimate:
  unit: points
  value: 5
```

or

```yaml
estimate:
  unit: hours
  value: 4
  confidence: rough
```

processkit does not mandate a unit. Projects pick one and stick with it.

### Epics and hierarchy

An epic is just a WorkItem with `spec.type: epic` and many `children`.
Children link back via `parent`. There is no hard limit on nesting, but
flat → one level of epic → tasks is the common shape.

### Relationship to Discussions

When a WorkItem emerges from a discussion, link the discussion via
`spec.related_decisions` (if a decision was recorded) or mention it in the
body. The Discussion primitive (shipped later) captures multi-turn
conversations — a WorkItem is the action that comes out of one.

### Creating via MCP

In Phase 3, the `workitem-management` MCP server provides:

```
create_workitem(title, type, priority=None, assignee=None, parent=None, scope=None)
  -> {id, path, state}

transition_workitem(id, to_state, note=None)
  -> {ok, from_state, to_state}

query_workitems(state=None, assignee=None, type=None, scope=None, limit=50)
  -> [{id, title, state, assignee, priority}, ...]

link_workitems(from_id, to_id, relation)  # relation ∈ blocks|parent|related
  -> {ok}
```

Until then, agents perform the same operations by editing files directly
following this SKILL.md.

### File naming

Default: `context/workitems/BACK-<id>.md`. With shards:

```toml
[context.sharding.WorkItem]
scheme = "state"
pattern = "context/workitems/{state}/"
```

This moves files as they transition. Turned off by default — most projects
prefer flat.

---
name: event-log
description: |
  Append-only event log — the probabilistic record of everything that happened in the project. Use whenever something notable happens that the project should remember — work items created/transitioned, decisions recorded, bindings changed, incidents occurred, releases shipped.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-event-log
    version: "1.0.0"
    created: 2026-04-06T00:00:00Z
    category: processkit
    layer: 0
    uses:
      - skill: index-management
        purpose: Query existing entities and keep the SQLite index fresh after writes.
      - skill: id-management
        purpose: Allocate unique entity identifiers via central ID generation.
    provides:
      primitives: [LogEntry]
      mcp_tools: [log_event, query_events, recent_events]
      templates: [logentry]
---

# Event Log

## Intro

The event log is the project's append-only history of significant events. Every
time a work item changes state, a decision is recorded, an actor is assigned,
or an incident occurs, a `LogEntry` file captures what happened, when, and
who caused it. LogEntries are never edited — corrections are added as new
entries.

> **MCP server.** This skill ships a self-contained MCP server at
> `mcp/server.py` (PEP 723 script — requires `uv` and Python ≥ 3.10 on
> PATH). Agent harnesses reach its tools by reading a single MCP config
> file at startup, so the contents of `mcp/mcp-config.json` must be merged
> into the harness's MCP config and placed at the harness-specific path
> before this skill is usable. If processkit was installed by an installer,
> that wiring is the installer's responsibility; if processkit was
> installed manually, the project owner must do it by hand.

## Overview

### When to write a LogEntry

Write a LogEntry whenever you do something the project should be able to
reconstruct later. Typical triggers:

- A WorkItem was created, transitioned, reassigned, or completed
- A DecisionRecord was proposed, accepted, or superseded
- A Binding was created or ended (role changed, scope reassigned)
- An external event was observed (deploy, incident, outage, release)
- A process step began or completed
- An automated check passed or failed at a gate

If you are asking "should I log this?", the answer is almost always yes.
Over-logging is cheap; under-logging erases history.

### Shape of a LogEntry

Every LogEntry is a YAML-frontmatter Markdown file:

```yaml
---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-<generated-id>
  created: <now>
spec:
  event_type: workitem.transitioned
  timestamp: <when-it-happened>
  actor: ACTOR-alice
  subject: BACK-calm-fox
  subject_kind: WorkItem
  summary: "Moved BACK-calm-fox from in-progress to review"
  details:
    from_state: in-progress
    to_state: review
---

Optional body: human-readable narrative, context, links.
```

### Workflow

1. Decide on `event_type`. Use a dotted lowercase value from
   `context/schemas/logentry.yaml` `spec.known_event_types`, such as
   `workitem.created`, `decision.created`, `binding.ended`, or
   `gate.passed`. Do not invent aliases in LogEntries; add new event
   types through an explicit schema migration before using them.
2. Fill in `actor` (who), `subject` + `subject_kind` (what it affected),
   `timestamp` (when the event occurred — distinct from `metadata.created`
   which is when the log file was written).
3. Write a one-line `summary`. This is what appears in timelines and queries.
4. Put anything structured in `details`. Freeform object.
5. Save the file to `context/logs/` (or whatever directory the project uses).

### Never edit a LogEntry

If you realize a LogEntry was wrong, do not edit it. Write a new LogEntry with
`event_type: logentry.corrected` and reference the original in `details.corrects`.
The original stays as historical record.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Editing a LogEntry instead of writing a correction.** LogEntries
  are append-only. If you discover a previous entry was wrong, write
  a NEW entry with `event_type: logentry.corrected` and reference
  the original via `details.corrects`. Editing the original silently
  rewrites history.
- **Skipping LogEntry writes after hand-edits.** When you bypass an
  MCP server and edit an entity file directly, you also have to
  write the corresponding LogEntry yourself. The audit trail relies
  on it. Forgetting causes the index and the event log to disagree
  about what happened.
- **Logging every file save as an event.** LogEntries are signal,
  not noise. If you save the same file three times in a minute
  fixing typos, that's one logical edit, not three events. Log the
  logical operation, not the keystrokes.
- **Using undeclared or vague event_type values.** Use only dotted
  lowercase values declared in `Schema.known_event_types` (e.g.,
  `workitem.transitioned`, `decision.created`). Free-form strings or
  legacy aliases such as `release.shipped` break strict vocabulary
  validation unless a schema migration introduced them.
- **Putting structured data in the body instead of `details`.** The
  `details` field is the structured payload that downstream queries
  parse. Putting "transitioned from backlog to in-progress" in the
  body and leaving `details` empty hides the data from
  `query_events`.
- **Hand-rolling timestamps.** Use the current UTC time in ISO 8601
  format from a real clock, never a fabricated value. Wrong
  timestamps poison time-range queries.
- **Logging events for entities that don't exist.** Verify via
  `get_entity(subject)` before logging — referencing a non-existent
  ID creates an orphaned event the index can't link back to anything.
- **Logging retroactively instead of in the same turn.** Call
  `log_event` in the same turn as the action it records — when a
  WorkItem is created, when a decision is made, when a skill is
  edited. Deferring event logging to "end of session" or "when I
  remember" produces an incomplete audit trail and risks omission
  entirely. The same rule applies here as for entity creation: do
  it now, not later.

## Full reference

### event_type conventions

Use dotted, lowercase, `<subject>.<verb-past>` names. Examples that are already
well-established:

| event_type                | When to emit                                                 |
|---------------------------|--------------------------------------------------------------|
| `workitem.created`        | New WorkItem file written                                    |
| `workitem.transitioned`   | WorkItem state changed; include `from_state`/`to_state`      |
| `workitem.note`           | WorkItem note/comment added                                  |
| `workitem.archive-moved`  | WorkItem moved to an archive/sharded location                |
| `decision.created`        | New DecisionRecord written                                   |
| `decision.transitioned`   | DecisionRecord state changed                                 |
| `decision.superseded`     | DecisionRecord transitioned to `superseded`                  |
| `binding.created`         | New Binding written                                          |
| `binding.ended`           | Binding `valid_until` reached or Binding deleted             |
| `binding.updated`         | Binding fields changed through binding-management            |
| `gate.passed` / `gate.failed` | A gate validation result                                 |
| `gate.updated` / `gate.emergency-updated` | A Gate changed through its audited update path |
| `migration.applied`       | Migration reached applied state                              |
| `migration.filename-normalized` | An audited Migration ID/filename normalization completed |
| `release.published`       | A release was published                                      |
| `logentry.corrected`      | Correction of an earlier LogEntry (referenced in details)    |
| `team_member.runtime_launched` / `team_member.runtime_stopped` | Managed TeamMember runtime changed state |
| `workitem.updated`        | WorkItem fields changed through workitem-management          |
| `role_slot.created` / `role_slot.filled` / `role_slot.closed` | Team role-slot lifecycle changed |
| `session.handover`        | End-of-session handover written before container shutdown    |
| `session.standup`         | Standup update recording what was done and what comes next   |

### Fields

- `event_type` (required): See above.
- `timestamp` (required): ISO 8601 UTC. When the event *occurred*, not when
  it was *logged*. If the agent is logging retroactively, use the original
  event time and set `details.logged_late: true`.
- `actor` (required): `ACTOR-<id>` for a processkit Actor; raw string for
  external agents (`"github-actions"`, `"claude-cli"`, `"alice@example.com"`).
- `subject` (optional): ID of the entity the event concerns. Omit for
  project-level events.
- `subject_kind` (optional): The `kind` of the subject entity, for fast
  filtering in queries.
- `summary` (required): One line. Human-readable. Appears in timelines.
- `details` (optional): Structured object with event-specific fields.
- `correlation_id` (optional): Links related events across a workflow run.

### Session entry types

`session.handover` and `session.standup` are the two session-lifecycle
entry types. They have a fixed `details` schema:

**`session.handover`** — written at container shutdown or at the user's
request before stopping work. Use the `session-handover` skill to author
these; do not write them manually.

```yaml
details:
  session_date: "2026-04-08"        # ISO date of the session being closed
  current_state: |                  # 2-4 sentences on where things stand
    ...
  open_threads:                     # list of unresolved items
    - "BACK-042 blocked on auth review"
  next_recommended_action: |        # what the next session should pick up first
    ...
  branch: "main"                    # git branch at handover time
  commit: "d56f4c8"                 # git SHA at handover time
```

**`session.standup`** — written at the user's request to record progress.
Use the `standup-context` skill to author these.

```yaml
details:
  session_date: "2026-04-08"
  done:                             # what was completed in this session
    - "Built session-handover skill"
  doing:                            # what is in progress right now
    - "Extending event-log"
  next:                             # what comes next
    - "Build standup-context skill"
  blockers: []                      # anything blocking progress
```

### Directory layout

Default: `context/logs/` flat. Projects may shard by date in `processkit.toml`:

```toml
[context.sharding.LogEntry]
scheme = "date"
pattern = "context/logs/{year}/{month}/"
```

When sharded, the index MCP server still sees the full log; only the filesystem
layout differs.

### File naming

Default: `LOG-<generated-id>.md` where the ID format follows the project's
`processkit.toml` setting. With date-sharded storage, consider including a time
prefix in the ID (`LOG-2026-04-06T10-30-00-calm-owl.md`) so chronological
sort matches filesystem order.

### Interaction with the index MCP server

In Phase 3, the `index-management` MCP server reads all LogEntries into a
SQLite `events` table and exposes:

- `query_events(event_type?, subject?, actor?, limit?)`
- `recent_events(limit?)`

The query tools return bounded result windows. Broad unfiltered event
queries are capped more tightly than filtered queries, and long summaries
are returned as previews. Fetch the referenced LogEntry entity by ID when
full details are needed.

### Relationship to deterministic logging

Per DISC-002, processkit's event log is **all probabilistic** — it is written
by agents via this skill, not by instrumentation. If an enterprise deployment
needs tamper-evident event logs for audit or compliance, that is a governance
platform's responsibility, not processkit's. Do not build a second, deterministic
event source here.

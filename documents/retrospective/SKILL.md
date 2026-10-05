---
name: retrospective
description: |
  Generates a post-release blameless retrospective from project signals —
  synthesizing DORA-like metrics, WorkItem outcomes, session timeline, and
  drift deltas into a structured Artifact + LogEntry. Use at the end of a
  release cycle when asked to run a retro, "post-release review",
  "retrospective", or "post-mortem".
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-retrospective
    version: "1.0.0"
    created: 2026-04-21T00:00:00Z
    category: processkit
    layer: 3
    uses:
      - skill: event-log
        purpose: Emit the retro.completed LogEntry after the Artifact is saved.
      - skill: artifact-management
        purpose: Save the retrospective as an Artifact (tags=[retrospective,release]).
      - skill: index-management
        purpose: Query WorkItems, LogEntries, and DecisionRecords within the release window.
      - skill: workitem-management
        purpose: (--auto-workitems) Create follow-up WorkItems from Action Items.
    commands:
      - name: pk-retro
        args: "--release <version> [--since <iso-or-ref>] [--until <iso-or-ref>] [--auto-workitems] [--verbose] [--dry-run] [--notes-file <path>]"
        description: "Generate a post-release blameless retrospective Artifact + LogEntry"
---

# Retrospective

## Intro

`/pk-retro` is the closing-loop skill: a post-release blameless
retrospective that pulls bottom-up signals from the MCP index and emits
a structured Artifact + LogEntry. It mirrors the shape of `/pk-wrapup`
(session-handover) but operates at release granularity, not session
granularity. Every claim must be backed by an entity ID; unsourced
claims are tagged `[uncertain]`.

## Overview

### Invocation

```
/pk-retro --release v0.18.2
/pk-retro --release v0.18.2 --since v0.18.1 --until v0.18.2
/pk-retro --release v0.18.2 --auto-workitems
/pk-retro --release v0.18.2 --verbose
/pk-retro --release v0.18.2 --dry-run
/pk-retro --release v0.18.2 --notes-file /tmp/owner-notes.txt
```

`--release` is required. All other flags are optional. Default output
caps each section at its line budget (80-line total); `--verbose`
disables the cap. `--dry-run` skips all MCP writes and prints the
rendered Artifact markdown to stdout only.

### Emitted entities

On success, the skill emits exactly two entities:

1. **Artifact** — saved as
   `context/artifacts/ART-<ts>-<word-pair>-retro-<release>.md`
   via `mcp__processkit-artifact-management__create_artifact`.
   Tags: `[retrospective, release]`.

2. **LogEntry** — `event_type: retro.completed`,
   `subject: <artifact-id>`, `subject_kind: Artifact`,
   via `mcp__processkit-event-log__log_event`.

Atomicity rule: if `create_artifact` fails, `log_event` is NOT
called. The LogEntry must reference a real Artifact ID.

### The seven sections

The Artifact body contains six mandatory sections and one optional:

1. **Release Summary** — version, date, commit count, contributors,
   top 3 deliverables (from `signals/release_summary.py`).
2. **Timeline** — session boundaries (status-briefing / session-handover
   pairs) + major milestones; 10-line cap in normal mode.
3. **Signals** — DORA-like: lead time proxy (first commit → release),
   change failure indicator (bug WorkItems closed / total closed in
   window), deploy frequency proxy.
4. **What Held** — WorkItems that closed successfully with no rollback;
   5-bullet cap in normal mode.
5. **What Slipped** — WorkItems deferred/superseded, skip-marker
   deltas, doctor.report ERROR deltas. Each bullet MUST cite a specific
   entity ID OR be tagged `[uncertain: <description>]`.
6. **Action Items (proposed)** — derived from What Slipped. Proposed
   only unless `--auto-workitems` is passed.
7. *(optional)* **Learned** — free-text bullets from `--notes-file`.
   Omit section entirely if no notes provided.

### Hallucination guards (CRITICAL)

- Every claim in "What Slipped" MUST include an entity ID (WorkItem,
  DecisionRecord, or LogEntry) pulled from the MCP index. If the
  signal module cannot find a backing entity, emit
  `[uncertain: <description>]` — never invent a narrative.
- Do NOT assert cascading causes ("X caused Y caused Z") without at
  least two cited entities.
- Signals flow bottom-up from MCP data. Do not infer what "should"
  have happened.

### `--auto-workitems` (Phase 2)

When `--auto-workitems` is passed, each Action Item bullet is created
as a WorkItem via `create_workitem`:
- `title`: first 80 chars of action text (markdown stripped)
- `description`: full text + "Source retro: <artifact-id>"
- `type`: `chore` (override with `retro-type:` prefix in bullet)
- `priority`: `medium`
- `state`: `backlog` (schema default)

After each creation, a LogEntry `retro.action_item_created` is emitted
linking the new WorkItem to the retro Artifact.

When flag is off, the Artifact includes:
> Pass --auto-workitems to create these as proposed WorkItems.

### `--verbose` (Phase 3)

When `--verbose`:
- Disables the 80-line per-section cap.
- Includes full entity bodies (not just IDs) for What Held / What Slipped.
- Includes raw DORA numbers with computation explanation in Signals.
- Appends "Appendix A — Raw Signal Dumps" with the JSON blob per
  signal module.

### Signal modules

Four signal modules live under `scripts/signals/`:

| Module | What it collects |
|---|---|
| `release_summary.py` | Latest release marker, commit range, DORA stats |
| `timeline.py` | Session boundaries + major milestones from LogEntries |
| `workitems.py` | Closed/deferred/superseded WorkItems in the window |
| `drift.py` | skip-marker deltas + doctor.report ERROR/WARN deltas |

### CLI

```
python3 pk_retro.py --release v0.18.2 [--since <iso-or-ref>]
                    [--until <iso-or-ref>] [--auto-workitems]
                    [--verbose] [--dry-run] [--notes-file <path>]
```

This skill provides the `/pk-retro` slash command — see
`commands/pk-retro.md`.

## Gotchas

- **Forgetting that `--dry-run` skips BOTH MCP writes.** Dry-run is
  for previewing the rendered Artifact markdown. Neither `create_artifact`
  nor `log_event` is called. Do not treat dry-run output as a filed retro.
- **Calling `log_event` before `create_artifact` succeeds.** The LogEntry
  references the Artifact ID. If `create_artifact` fails (quota, schema
  error, network), the LogEntry must not be emitted — there is nothing to
  reference. Always check the Artifact creation response first.
- **Leaving "What Slipped" bullets without entity citations.** A retro
  that says "deployment stability degraded this cycle" without citing a
  specific WorkItem, LogEntry, or doctor.report finding is an
  unsourced claim. Use `[uncertain]` if no entity can be found; do not
  invent plausible-sounding references.
- **Running `--auto-workitems` without owner review.** Action Items are
  proposed by the signal modules from incomplete information. The flag
  creates real WorkItems in the backlog. Always confirm scope with the
  owner before running with `--auto-workitems` for the first time.
- **Treating the retro Artifact as a session handover.** The retro covers
  a release window (days to weeks). It is not a substitute for
  `/pk-wrapup` at session end. Both may be needed.

## Full reference

### Relationship to other lifecycle skills

| Skill | When | LogEntry type |
|---|---|---|
| `standup-context` | Daily / per session | `session.standup` |
| `session-handover` | Before shutdown | `session.handover` |
| `status-briefing` | Session start | (read-only) |
| `retrospective` | After release | `retro.completed` |

### Finding prior retros

```
query_events(event_type="retro.completed", limit=5, order="desc")
```

Then `get_artifact(id=<subject>)` to read the Artifact body.

### Release window defaults

If `--since` is omitted, the skill queries for the prior
`release.published` or `session.release` LogEntry and uses its
timestamp as the window start. If none exists, it falls back to 30
days before `--until`.

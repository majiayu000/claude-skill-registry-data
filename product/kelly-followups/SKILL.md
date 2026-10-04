---
name: kelly-followups
description: Busabase-backed App-in-Skill for one thing only — record who you need to follow up with after a meeting, see what is due today, mark it done. Use when the user invokes $kelly-followups or /kelly-followups, mentions a followup, follow-up, meeting action item, or wants a lightweight daily reminder of who to check in with, without a full project-management tool.
metadata:
  category: comms
  tags:
    - risk:gated-write
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-followups
    resources:
      - followups
    risk: gated-write

---

# Kelly Followups

## Overview

Kelly Followups is a Busabase Cloud App-in-Skill. Its canonical product
surface is the AirApp in Busabase, not a separate local-data product. The
same Hono source supports an explicitly requested local preview with OAuth
connection bootstrap.

It does exactly one thing, on purpose: after a meeting, record who you need
to follow up with and what needs doing; open the app any morning and see
today's list; mark each one done.

## Origin

This skill exists as a worked example of the `$kelly-ideas` → `$kelly-app-creator`
handoff: a real idea ("周会太多我总忘记谁该跟进" — too many weekly meetings,
can never remember who to follow up with) was interrogated through
`$kelly-ideas`'s BRD → MRD → PRD ladder, and the resulting PRD's own
non-goals — no full project management, no calendar sync, no notification
delivery, no team permissions — are exactly this app's scope. It is
intentionally this small; growing it into a project-management tool is a
different PRD, not a feature request on this one.

## Mandatory Dependencies

1. Read and follow `$busabase` for connection, target Space, node discovery,
   ChangeRequests, review, merge, and trusted mutations.
2. Read and follow `$kelly-app-creator` for the App-in-Skill artifact
   contract, the UI contract, and AirApp delivery.

## Busabase Resources

| Resource | Holds |
| --- | --- |
| `followups` | One row per followup: who, what, when it's due, and whether it's done |

## Authentication

Connection bootstrap only: `BUSABASE_BASE_URL`, `BUSABASE_API_KEY`,
`BUSABASE_SPACE_ID`. Everything else lives in Busabase through
`busabase-sdk`. Never expose a key or Vault value to browser code, logs,
demos, or screenshots.

## Non-Goals (inherited from the PRD, kept deliberately)

- No multi-level tasks, no Gantt chart, no full project management.
- No calendar sync, no scheduled notification delivery — v1 is "open it and
  see", not "get pinged".
- No per-user permissions — v1 shows every followup to everyone who opens it.

Do not add these as a side effect of an unrelated request. If a real need for
one of them shows up, that is a new PRD to interrogate through
`$kelly-ideas`, not a quiet scope creep here.

## Demo Mode

`?demo=1` serves a deterministic read-only set of followups — some due
today, one upcoming, one already done — so the today/all split is visible
without touching a real Space. Demo never impersonates a connection and is
labeled read-only.

## Completion Criteria

- The `kelly-followups` Folder and `followups` Base exist.
- Recording a followup takes one write; marking it done takes one write.
- A done item disappears from "Today" immediately.
- Desktop and 390px phone viewports both verified, with no horizontal overflow.
- The AirApp node exists and its version is merged before claiming deployment.

## Stop Conditions

- Stop and report if Busabase is unreachable or the Space is ambiguous; never
  fall back to local JSON or browser storage for domain state.
- Stop before any external side effect. This skill only writes to Busabase;
  it does not send, publish, or notify anyone outside the app itself.

---
name: linear-mvp-recipe
last_updated: 2026-05-17
description: "Beamix's locked Linear label vocabulary, sub-ticket creation pattern, and single-synthesis-comment style. Use whenever any CEO or C-suite agent interacts with Linear tickets, creates sub-tickets, or posts comments."
tags: [workflow, beamix-specific, linear, orchestration]
source: beamix-authored 2026-05-16
risk: low
---

# Linear MVP Recipe

## Quick reference

> Every ticket: 1 user-visible outcome + 1 Acceptance Criteria + 1 reviewer + 1 demo URL. No tickets without all four.

## When to use

- Writing or refining any agent that touches Linear (CEO, CTO, CPO, CMO, CBO, CCO, QA-Lead, Research-Lead)
- Creating sub-tickets during fan-out dispatch
- Formatting a synthesis comment after task completion
- Debugging why the Cloudflare bridge did not pick up a ticket

## When NOT to use

- For product feature work unrelated to agent orchestration
- When an agent does not have the `linear` MCP in its grant (workers never write to Linear)

## Label vocabulary (locked)

### Agent routing labels

Apply exactly one `agent:*` label per ticket. The bridge classifier reads this.

```
agent:ceo
agent:cto
agent:cpo
agent:cmo
agent:cbo
agent:cco
agent:qa-lead
agent:research-lead
```

### Tier labels

Apply exactly one `tier:*` label per ticket. Haiku classifier at bridge assigns it; Adam can pre-set.

```
tier:quick        # single worker, same-session Task spawn
tier:lite         # single C-suite, one fan-out
tier:full         # cross-domain, N C-suites, Inngest fan-in
tier:irreversible # full path + multi-judge + Adam sign-off required
```

### Risk labels

```
risk:irreversible   # override any tier: always Full review minimum
board-meeting       # triggers /board-meeting 4-round protocol
proposed-by-agent   # Adam can filter agent-suggested work
decision_type:vendor      # board-meeting routes Aria persona
decision_type:strategic   # board-meeting routes broad-adversary persona
```

## Sub-ticket creation pattern

When a C-suite (e.g., CTO) fans out to workers, it creates one Linear sub-ticket per independent task:

```typescript
// Inside CTO Routine — after receiving full spec
const backendTicketId = await linear.createIssue({
  teamId: BEAMIX_TEAM_ID,
  parentId: parentTicketId,          // the CTO's own sub-ticket
  title: `[backend] Rate-limit free scans (${parentTitle})`,
  labels: ['agent:cto', 'tier:lite'], // CTO is the responsible label
  description: workerBriefJson,       // the structured brief for the worker
});

// Trust spec goes into a comment on the sub-ticket, not the description
await linear.createComment({
  issueId: backendTicketId,
  body: `---BEAMIX-SPEC-V1-START---\n${JSON.stringify(spec, null, 2)}\n---BEAMIX-SPEC-V1-END---`,
});
```

Key rules:
- Ticket body is human-readable context only — never a trust spec source
- Trust specs live in comments, sentinel-bracketed
- One sub-ticket per independently-mergeable task
- Sub-ticket titles follow: `[domain] brief description (parent-title)`

## Single-synthesis-comment rule

Each agent posts EXACTLY ONE comment per ticket it owns. This comment is written at task completion, not during execution.

Format for a CTO synthesis comment:

```markdown
**CTO — Task Complete**

**Outcome:** BMX-101 backend rate-limiting implemented and merged.

**Workers spawned:** backend-engineer (branch: feat/scan-rate-limit), test-engineer (haiku, branch: test/scan-rate-limit)

**QA verdict:** PASS (tier: lite, reviewer: qa-lead)

**Session file:** docs/08-agents_work/sessions/2026-05-16-cto-bmx101.md

**Decisions made:** None — implementation within existing spec.

**Blockers:** None.
```

Rules:
- No running commentary during execution (no "Starting step 2…" comments)
- One structured summary comment at Done transition
- Workers NEVER comment — only their parent C-suite does
- If blocked, comment format is: `BLOCKED: <reason>` + escalation path

## Status transitions

```
Open → In Progress (when Routine accepts spec, writes accepted to audit_log)
In Progress → Done (when Routine writes complete to audit_log AND synthesis comment posted)
In Progress → Blocked (when Routine returns BLOCKED to parent — parent escalates)
Done → Reopened (anomaly path — triggers fan-in-watcher escalation, NOT re-fire)
```

## Ticket naming conventions

```
# Parent tickets (Adam creates)
BMX-101: Add rate limiting to free scan endpoint

# Sub-tickets (C-suite creates for workers)
BMX-101-backend: [backend] Implement scan rate-limit API route (BMX-101)
BMX-101-test:    [test] Write scan rate-limit integration tests (BMX-101)

# Board meeting tickets
BMX-200: [board-meeting] Evaluate Mem0 vs self-hosted pgvector for episodic memory
```

## Project structure

```
Beamix — Main (product work)        ← Adam and agents work here
Beamix — War Room (orchestration)   ← Standing Routines post here, separate from product
Beamix — Strategy (board meetings)  ← Board meeting outputs
```

Routines post to War Room and Strategy projects only. Product tickets live in Main.

## See also

- `war-room-orchestration` — [[war-room-orchestration]]
- `anthropic-routines` — [[anthropic-routines]]
- `qa-gate-protocol` — [[qa-gate-protocol]]
- `writing-plans` — [[writing-plans]]

## Anti-patterns

- Posting multiple comments per ticket from the same agent (breaks synthesis quality)
- Parsing trust specs from ticket body (prompt-injection surface — use comments with sentinels only)
- Using freeform labels instead of the locked vocabulary (bridge won't route correctly)
- Workers posting to Linear (workers return JSON to parent; parent synthesizes)
- Creating sub-tickets without a parent_ticket reference (fan-in-watcher can't correlate)
- Omitting `tier:*` label (bridge classifier adds one, but explicit is safer and faster)

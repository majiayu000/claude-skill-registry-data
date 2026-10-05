---
name: status-briefing
description: |
  Generates a concise status briefing after session-start reconciliation — synthesizing current state, open decisions, key risks, and today's priority actions. Use at session start, for "pk-resume", a briefing, catch-up, or today's focus.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-status-briefing
    version: "1.1.0"
    created: 2026-04-08T00:00:00Z
    category: processkit
    layer: 4
    uses:
      - skill: agent-management
        purpose: Understand what context files to read at session start (HANDOVER, BACKLOG, INDEX).
      - skill: status-update-writer
        purpose: Pull current project state when generating the today's priorities section.
      - skill: workitem-management
        purpose: Query in-progress and next-up WorkItems for the today's priorities section.
      - skill: project-reconciliation
        purpose: Reconcile the session-start migration and health queues and inventory repository collaboration state.
    commands:
      - name: pk-resume
        args: ""
        description: "Run session-start reconciliation, then generate a session-start orientation"
---

# Status Briefing

## Intro

A status briefing is a single-screen orientation that a person or
agent reads at the start of a session to immediately know what
matters today. It distills project context, backlog state, open
decisions, and upcoming deadlines into a focused, actionable
summary. Before writing the briefing, `/pk-resume` runs
`pk-reconcile session-start` so the user does not need separate requests to
resolve migrations, check health, and inspect GitHub state. The reader should
be ready to start working within three minutes of reading it.

## Overview

### Sources to read before generating

Pull from these sources in order, weighting by freshness:

```
1. session.handover LogEntry  — most recent; weight by age (see below)
2. Active interlocutor — current speaker via team-manager, if configured
3. Session-start reconciliation — migration results, pk-doctor totals and
   action totals, plus GitHub issue and pull-request inventory
5. WorkItems (in_progress + blocked)  — current state via workitem-management
6. session.standup LogEntries — last 1-3 entries since last handover
7. git log --oneline -5       — recent commits
8. DecisionRecords (proposed) — open decisions needing attention
9. Any time-sensitive flags  — deadlines, blockers, scheduled events
```

Run `pk-reconcile session-start` before reading the remaining sources. It
resolves unambiguous migrations and safe health findings, then returns the
pk-doctor severity/action totals and GitHub issue/PR inventory. It does not
close issues or merge pull requests at session start; report those candidates
and invoke `pk-reconcile all` only when the user requests full reconciliation.
For `info-only`, `dry-run`, `report-only`, `check-only`, or `no fixes`, invoke
the reconciliation skill in report-only mode and include its next actions.

**Handover staleness rule** — before using the most recent `session.handover`
entry, check `details.session_date` and weight accordingly:

| Handover age | How to use it |
|---|---|
| < 24 hours | Primary source for "what happened last session" and "open threads" |
| 1–7 days | Secondary source — include content but flag as stale in the briefing |
| > 7 days | Skip — reconstruct from git log and WorkItem state only; note absence |

The two-pattern reality: some users write handovers every session (the
handover will usually be < 24h old); others write handovers only on
container restart (may be days old). The staleness rule handles both without
the user configuring anything.

### The briefing format

```markdown
# Status Briefing — [Date]

## State of play

[If configured: Active interlocutor: Name (TEAMMEMBER-id; role/seniority).]

[1-3 sentences on overall project health and phase. Honest —
"on track", "at risk on [milestone]", or "blocked on [dependency]".]

## What happened since last session

- [Completed item or change]
- [Completed item or change]
(If nothing happened: "No sessions since [date]. Project state unchanged.")

## Today's priorities

1. **[Top priority item]** — [why it's first, what done looks like]
2. **[Second priority]** — [brief context]
3. **[Third priority]** — [brief context]

## Open decisions

- [Decision X] — owner: [name], due by: [date or "unscheduled"]
- [Decision Y] — [brief description]

## Migrations

- [If resolved] Resolved [N] active migration(s); [0] remain.
- [If blocked] [Migration ID] — blocked on [decision/conflict], next
  action: [ask/apply/reject/continue]

## Blockers and risks

- [Blocker] — waiting on: [person/thing], impact: [what it blocks]
- [Risk] — likelihood: [H/M/L], mitigation: [action]

## Repository health

- pk-doctor: [0 ERROR / 0 WARN / N INFO; A actionable / C need confirmation]
  — [top actionable finding or "clean"]

## GitHub

- Issues: [count open; call out stale/high-priority issues]
- Pull requests: [count open; call out draft/blocked/review-needed PRs]

## Upcoming deadlines

- [Deadline] — [date, days from now]

## One-liner to carry

> [A single sentence that captures the most important thing to keep
> in mind today — the guiding constraint or the single metric to move]
```

Omit sections that have nothing to report. A briefing with three
well-chosen items is better than a padded briefing with eight items
of equal apparent importance.

### Calibrating for session type

**First session of the day (human):** full format including upcoming
deadlines and open decisions.

**Agent session start:** focus on state of play + today's priorities.
Skip open decisions unless the agent needs to make them.

**After a long break (>1 week):** add a "Context refresh" section
summarizing anything structural that changed (architecture, team,
constraints) and note the date of the last active session.

**Sprint start / milestone start:** add a "Sprint goal" or "Milestone
target" section above priorities, so the briefing orients to the
bigger shape of the period.

### The "one-liner to carry"

The most important output of a good status briefing is the single
sentence the reader holds in their head all day. It captures the
dominant constraint or priority for the session:

Good examples:
- "Get the data pipeline unblocked before anything else — it's the
  critical path for the Friday demo."
- "The authentication refactor is the only thing on the critical path;
  don't start anything new."
- "Scope is the binding constraint today — question every addition."
- "The milestone is tomorrow: ship something working, perfect later."

Bad examples (too vague):
- "Keep up the good work." (not actionable)
- "Focus on quality." (not specific to today's situation)

If you cannot write a specific one-liner for today, the briefing
itself is probably too generic.

This skill also provides the `/pk-resume` slash command for direct
invocation — see `commands/pk-resume.md`.

### Keeping it short

A status briefing that takes more than 3 minutes to read has failed.
Length signals:
- **Too long:** more than 2 items per section, or sections that do not
  affect today's work
- **Too short:** misses an active blocker or an imminent deadline
- **Right length:** one readable screen, skimmable in 90 seconds

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Treating pk-resume as report-only.** `/pk-resume` is a session-start
  cleanup and briefing workflow. Resolve active migrations first unless
  the user explicitly asked for info-only, dry-run, report-only,
  check-only, or no-fix behavior. Do not leave the user to ask a second
  time for "resolve migrations" when the next action is clear.
- **Treating a stale handover as current.** A `session.handover` written 10 days ago reflects a state that may have completely changed. Always check `details.session_date` before using a handover as a source. If it is more than 7 days old, skip it and reconstruct from git log and WorkItem state instead. Presenting stale handover content as "what happened last session" when the last session was a week ago misleads the user.
- **Reading only the handover note without checking WorkItem state.** The handover captures what was true at session end; WorkItem state shows what has been actively changed since. A briefing that contradicts current WorkItem state (e.g., listing an item as "next up" when it is now done) will erode trust immediately. Always cross-check both.
- **Leaving active migrations for a second prompt.** Session start is the
  safest point to catch upgrade drift. Always query pending and
  in-progress migrations. If any are present, resolve the unambiguous
  ones through `migration-management` before writing the briefing, then
  report what changed. Ask only when the migration is destructive,
  policy-sensitive, ambiguous, conflicting, or externally blocked.
- **Skipping repository health.** `pk-resume` should include the current
  `pk-doctor` result. A clean doctor pass can be one line only when both
  severity and action queues are clean. ERROR/WARN findings and
  `action_required: true` INFO findings should be included in
  blockers/risks or repository health. If the direct MCP tool is missing,
  report that as a configuration problem.
- **Ignoring GitHub collaboration state.** In a git repository with a
  GitHub remote, local worktree and processkit state are not enough.
  Check open GitHub issues and PRs through `gh` when available, and call
  out review-needed PRs, stale issues, and external blockers.
- **Blurring persistent identity and ephemeral dispatch.** If
  `team-manager.get_active_interlocutor` returns a TeamMember, show that
  identity explicitly. If it is not configured, say the session is an
  ephemeral harness agent rather than implying a named persona is speaking.
- **Hiding model/runtime mismatch.** When available, call
  `team-manager.get_interlocutor_runtime_binding` with the harness's
  observed model and effort. Surface a mismatch as information, not a
  failure: the configured TeamMember identity can still be correct even
  when the harness cannot hot-swap to the resolved processkit model.
- **Listing everything instead of prioritizing.** A briefing that reports all 12 open workitems is not a briefing — it's a dump. The value of a status briefing is triage: surface the 3 things that matter today, not an inventory of everything that exists. If in doubt about what to prioritize, ask — do not pad.
- **Making the "state of play" section too optimistic.** Briefings written by the agent often smooth over problems to avoid delivering bad news. If the project is blocked, at risk, or behind, the state of play must say so clearly — not "making good progress with a few items to resolve." The user is about to spend their session on this; accurate state matters.
- **Not including a one-liner.** The "one-liner to carry" section is the hardest to write and the most valuable. Skipping it produces a briefing that reports status without providing orientation. Every briefing must end with one sentence that captures the dominant constraint or priority for the session.
- **Generating a briefing without reading the current context.** A briefing from memory or from context loaded in a prior session may be stale. Always read HANDOVER.md and BACKLOG.md (or query the live index) before generating. A briefing that reflects last week's state is misleading.
- **Writing the briefing in a format that requires careful reading instead of scanning.** Status briefings are consumed at session start, often under time pressure. Use short bullets, bold key terms, and scannable structure. A briefing written as flowing prose that requires careful reading defeats the purpose.
- **Reporting blockers without their resolution path.** "Blocked on API key from vendor" is incomplete. "Blocked on API key from vendor — Sarah requested it Tuesday, expected by Thursday" is actionable. Every blocker must include: who owns it, what action is in progress, and when it's expected to resolve.

## Full reference

### When the project has no processkit context

If the project does not use processkit (no BACKLOG.md, no HANDOVER.md),
ask the user to provide:
- What was worked on last session
- What is in progress right now
- What deadlines exist in the next 1-2 weeks
- Any blockers

Then generate the briefing from those answers using the same format.

### Archiving briefings

Briefings are ephemeral by design. Do not archive them unless the
user requests it. The handover note is the persistent record;
the status briefing is a generated view of it.

### Integration with event-log

The `event-log` skill records session activity as log entries.
`status-briefing` reads recent entries (plus HANDOVER and WorkItem
state) and synthesizes them into an actionable briefing. event-log
is the write path; status-briefing is the read path.

### Briefing cadence

- **Daily work:** generate at the start of each session
- **After a weekend:** use the extended format (>1 week gap)
- **Project kickoff:** generate a "kickoff briefing" from the
  PRD / scope docs instead of HANDOVER + BACKLOG
- **Post-incident:** lead with incident status, then resume normal
  briefing format once the incident is resolved

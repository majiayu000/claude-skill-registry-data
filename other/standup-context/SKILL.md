---
name: standup-context
description: |
  Writes a structured standup update as a session.standup LogEntry — capturing
  what was done, what is in progress, what comes next, and any blockers. Use
  when the user says "write a standup", "standup update", "what did I do today",
  "write a status update for the team", or at the end of a session on projects
  that run daily standups.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-standup-context
    version: "1.0.0"
    created: 2026-04-08T00:00:00Z
    category: processkit
    layer: 2
    uses:
      - skill: event-log
        purpose: Write the session.standup LogEntry with the structured details schema.
      - skill: workitem-management
        purpose: Query completed and in-progress WorkItems to populate done/doing accurately.
    commands:
      - name: pk-standup
        args: ""
        description: "Generate a standup update (done / doing / next / blockers)"
      - name: pk-status
        args: ""
        description: "Generate a status update: current progress, blockers, and recommended next steps"
---

# Standup Context

## Intro

A standup update is a brief, structured record of session progress — written
for the team record and for any downstream skill (like `status-briefing`)
that reconstructs what happened. It lives in `context/logs/` as a
`session.standup` LogEntry. It is NOT a flat `context/STANDUPS.md` file.

## Overview

### The four fields

Every standup has exactly four fields:

- **done** — what was completed since the last standup. Past tense, specific.
  "Merged BACK-042 auth refactor" not "worked on auth."
- **doing** — what is currently in progress. These are the items that
  will appear in the next standup's "done" if work continues.
- **next** — what comes immediately after the current work. One or two items.
  Gives the team visibility on direction.
- **blockers** — anything preventing progress. Empty list if none.
  Be specific: "waiting for Alice to review PR #88" not "blocked on review."

### Writing the LogEntry

```yaml
---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-<next-id>
  created: <ISO 8601 UTC>
spec:
  event_type: session.standup
  timestamp: <ISO 8601 UTC>
  actor: <ACTOR-id or agent name>
  summary: "Standup — <YYYY-MM-DD>"
  details:
    session_date: "<YYYY-MM-DD>"
    done:
      - "<completed item 1>"
      - "<completed item 2>"
    doing:
      - "<in-progress item>"
    next:
      - "<next item>"
    blockers: []
---
```

Save to `context/logs/LOG-<id>-standup-<date>.md`.

### Sourcing the content

Before writing, query:
1. `workitem-management` — filter for `state: done` (completed today) and
   `state: in_progress` (currently doing)
2. Recent `session.handover` or `session.standup` entries — for what the
   previous session left as "next"
3. Git log — `git log --oneline --since="24 hours ago"` for a mechanical
   account of commits since the last standup
4. GitHub, when inside a git repository with a GitHub remote and an
   authenticated `gh` CLI:

   ```
   gh issue list --state open --limit 20 \
     --json number,title,labels,assignees,updatedAt,url
   gh pr list --state open --limit 20 \
     --json number,title,isDraft,reviewDecision,headRefName,updatedAt,url
   ```

Cross-check: if a WorkItem is marked `done` but no commit references it,
note it — might be a missing commit or a premature state transition.
If GitHub cannot be checked, note that briefly and continue. When it can
be checked, include PRs waiting on review and issues that create blockers
or immediate next work; do not dump every open item into the standup.

### Trigger phrases

The agent should write a standup when it hears:
- "write a standup" / "standup update"
- "what did I do today" / "summarize today's work"
- "write a status update for the team"
- "daily update"
- "end of day summary"

This skill also provides the `/pk-status` and `/pk-standup` commands for
direct invocation — see `commands/pk-status.md` and
`commands/pk-standup.md`.

## Gotchas

- **Writing done in present tense.** "Working on BACK-042" belongs in
  doing, not done. Done means the work is finished. "Completed BACK-042
  auth refactor and merged to main" is done.
- **One-liner entries with no specifics.** "Worked on auth" is not a
  standup item — it gives the team nothing. Reference the WorkItem ID,
  the PR number, or the specific outcome: "Merged auth refactor (BACK-042,
  PR #88); all tests green."
- **Leaving blockers vague.** "Blocked on review" tells the team nothing
  actionable. Name the reviewer, the PR, and how long it has been waiting:
  "PR #88 waiting on Alice — submitted 2026-04-07, no response yet."
- **Conflating doing and next.** Doing is what is actively in progress
  right now. Next is what comes after. The distinction matters: doing items
  might finish today; next items haven't started.
- **Writing a standup without querying WorkItem state.** Memory-based
  standups miss items and include outdated ones. Always check the actual
  WorkItem state before writing.
- **Missing GitHub blockers.** In GitHub-backed repositories, PR review
  state and open issues can be the real blocker even when local worktree
  state looks clean. Check `gh` when available and cite issue/PR numbers.
- **Writing a standup for a period longer than one session without flagging
  it.** If the last standup was three days ago, the "done" list is actually
  three days of work. Flag this in the summary line so the team knows the
  cadence was missed.
- **Including personal context in the team standup.** Blockers like
  "dentist appointment" or "waiting to hear back about contract" belong in
  a `session.handover`, not a standup. Standups are project-facing records.

## Full reference

### Standup vs. session handover

| | standup-context | session-handover |
|---|---|---|
| **When** | Regular cadence (daily or per session) | Before shutdown / container restart |
| **Audience** | The team / project record | The next session (same person or agent) |
| **Focus** | Accountability — what was done | Continuity — what to pick up next |
| **LogEntry type** | `session.standup` | `session.handover` |

### Reading recent standups

To reconstruct what has happened since the last session:

```
query_events(event_type="session.standup", since="<date>", order="asc")
```

`status-briefing` uses this query to populate its "what happened" section
when no recent `session.handover` exists.

### Output format for sharing

When the user wants to copy a standup to Slack or email, format it as:

```
**Yesterday / last session:**
- <done item 1>
- <done item 2>

**Today:**
- <doing item>
- <next item>

**Blockers:**
- <blocker> (or: none)
```

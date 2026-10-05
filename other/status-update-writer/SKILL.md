---
name: status-update-writer
description: |
  Generates clear, structured status updates for stakeholders — from project context, backlog state, or a brief description of recent work. Use when asked to write a status update, weekly report, progress summary, or team briefing about a project or initiative.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-status-update-writer
    version: "1.0.0"
    created: 2026-04-08T00:00:00Z
    category: processkit
    layer: 4
    uses:
      - skill: workitem-management
        purpose: Query current workitem state and priorities to populate the update accurately.
      - skill: agent-management
        purpose: Extract recent session context when generating periodic updates.
---

# Status Update Writer

## Intro

A status update answers three questions for someone who hasn't been
in the room: what happened, what comes next, and what (if anything)
needs their attention. Write it at the audience's level of detail —
an executive wants headline + blockers; a team wants specifics.
Source from actual project state, not from memory.

## Overview

### Source the data first

Before writing anything, read the project state:

```
# If in a processkit project:
context/BACKLOG.md      # in-progress and next items
context/STANDUPS.md     # last 1-2 entries
context/HANDOVER.md     # most recent session summary

# From git:
git log --oneline -10   # recent commits
git diff --stat HEAD~3  # what changed in the last few commits

# From GitHub, when inside a git repository with a GitHub remote and
# an authenticated gh CLI:
gh issue list --state open --limit 20 \
  --json number,title,labels,assignees,updatedAt,url
gh pr list --state open --limit 20 \
  --json number,title,isDraft,reviewDecision,headRefName,updatedAt,url
```

If the update is for a non-processkit project, ask the user to
provide recent output, commits, or notes.

Treat GitHub as a best-effort collaboration source. If `gh` is missing,
not authenticated, or blocked by network access, state that GitHub
issues/PRs were not checked and continue from local/processkit state.
When GitHub data is available, fold open issues and PRs into Done,
In Progress, Blocked/At Risk, and Next Up rather than appending a long
inventory. Call out review-needed PRs, stale issues, and external
blockers by number.

### Choose the format for the audience

| Audience | Format | Length | Key emphasis |
|---|---|---|---|
| **Executive / leadership** | Headline + bullets | ½ page | Status, blockers, decisions needed |
| **Team / peers** | Section-per-area | 1 page | Work done, in-progress, next steps |
| **Stakeholder brief** | Narrative + table | 1-2 pages | Context, progress, risks, timeline |
| **Stand-up (async)** | 3-line Done/Next/Blockers | 3-5 lines | Brevity — one line per item |

Default to the team format unless the audience is specified.

### Executive / leadership format

```markdown
## [Project] Status — [Date]

**Overall:** 🟢 On track / 🟡 At risk / 🔴 Blocked

**This week:**
- [Completed milestone or delivered item]
- [Second key outcome]

**Next week:**
- [Next milestone with expected completion]

**Needs your attention:**
- [Decision or unblock required, with deadline]
```

Use 🟢/🟡/🔴 (or "On track / At risk / Blocked" in plain text).
Lead with status before detail — executives read left-to-right and
stop as soon as they know whether to be concerned.

### Team / peer format

```markdown
## [Project] Update — [Date or Sprint N]

### Done
- [Completed items, linked to tickets or PRs where applicable]
- [Each item on its own line]

### In Progress
- [What is being actively worked, with owner and estimated completion]

### Blocked / At Risk
- [Blocker description] — **owner:** [name], **needs:** [what unblocks it]

### Next Up
- [Upcoming work, in priority order]

### Metrics (if applicable)
- [Key number] — [interpretation] (was [prior value])
```

Link to specific tickets, commits, or docs wherever possible —
readers should be able to drill down without asking follow-up
questions.

### Stakeholder brief (longer form)

```markdown
## [Project] — [Phase/Quarter] Status Brief

**Executive summary:** [2-3 sentence narrative — what we set out to
do, where we are, what the outlook is]

### Progress against plan

| Milestone | Target | Status | Notes |
|---|---|---|---|
| [M1] | [Date] | ✅ Complete | |
| [M2] | [Date] | 🔄 In progress | ETA [Date] |
| [M3] | [Date] | ⏳ Not started | |

### Key accomplishments this period
- [Specific, measurable outcome]

### Risks and mitigations
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| [Risk] | Medium | High | [Action] |

### Decisions needed
- [Decision] — **due by:** [Date], **owner:** [Name]

### Next period plan
- [Major focus areas and expected outcomes]
```

### Calibrating length and detail

The right update is the shortest one that gives the reader everything
they need to make decisions or stay confident. Rules of thumb:

- **One status per item.** Never say "we're making progress on X, Y,
  and Z." Tell them where each stands.
- **Blockers need owners and deadlines.** "We're blocked on infra" is
  useless. "We're waiting on firewall rule approval from IT; Jake is
  following up by Thursday" is actionable.
- **Numbers over adjectives.** "Good progress" means nothing;
  "shipped 3 of the 5 planned features" means something.
- **Lead with changes, not constants.** If something hasn't moved,
  keep it in one line — readers don't need to re-read stable facts.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Writing from memory instead of reading the actual project state.** A status update that contradicts the backlog or misses completed work is worse than no update. Always read `context/BACKLOG.md`, recent git log, or the last handover note before writing. Never synthesize from recall alone.
- **Checking only local repository state.** In GitHub-backed repositories,
  open issues and PRs are part of the live project state. Check them via
  `gh` when available, and clearly note when they could not be checked.
- **Reporting activity instead of outcomes.** "We held three meetings and reviewed the architecture" describes effort; "We finalized the data model and unblocked the API team" describes outcome. Status updates are for outcomes — what changed, what was delivered, what moved.
- **Omitting blockers to avoid delivering bad news.** A status update without blockers implies everything is on track. Silently omitting a blocker delays the moment when it can be resolved. Report blockers with owner, impact, and what would unblock them — that's what stakeholders need to help.
- **Using the same format for every audience.** An executive update with 40 bullets loses the reader; a 3-line async standup for a stakeholder brief leaves them confused about project health. Always ask "who will read this and what do they need to decide or know?" before choosing the format.
- **Using vague status signals.** "In progress" on every item provides no information. Distinguish: "on track to complete by [date]", "at risk — depends on [X]", "blocked since [date] by [reason]". The reader should be able to tell whether to be concerned without reading the body.
- **Not including the decision or action needed.** A status update that describes problems without stating what the reader should do creates anxiety without resolution. Every risk or blocker in the update must include who owns it and what action would help.
- **Writing updates in first person plural without specifying owners.** "We will finalize the contract by Thursday" creates no accountability. Name the person: "Alice will finalize the contract by Thursday." Stakeholders reading updates need to know who to follow up with.

## Full reference

### Pulling data from processkit primitives

When running inside a processkit project with the index MCP server:

```python
# Get in-progress items
query_entities(kind="WorkItem", state="in_progress")

# Get recent log entries
query_entities(kind="LogEntry", limit=10)

# Get open decisions
query_entities(kind="DecisionRecord", state="open")
```

Use these queries to populate the "In Progress", "Done (this week)",
and "Decisions needed" sections with accurate data.

### Cadence templates

**Weekly update (team):** Every Friday, source from the week's commits
and the current backlog. Send by end of day. Archive the prior week's
update in `context/archive/status-updates/`.

**Sprint review:** At the end of each sprint, compare committed items
against delivered items and explain any gap.

**Quarterly briefing:** Pull the quarter's highlights from the
archived weekly updates + log entries. Summarize three things:
what we shipped, what we learned, what we're doing next quarter.

### Status emoji guide (for teams using emoji status)

| Symbol | Meaning |
|---|---|
| ✅ | Complete — shipped and verified |
| 🔄 | In progress — actively being worked |
| ⏳ | Not started — planned but not yet begun |
| 🟡 | At risk — on track but a dependency is uncertain |
| 🔴 | Blocked — cannot proceed without external action |
| ❌ | Cancelled / removed from scope |

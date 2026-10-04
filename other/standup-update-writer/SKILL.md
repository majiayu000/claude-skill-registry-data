---
name: standup-update-writer
description: "Drafts daily standup updates from recent activity in git hosting, project trackers, and chat, leading with blockers and summarizing done, in-progress, and planned work. Produces talking points for live standups, short written posts for async standups, or a whole-team summary tied to sprint goals. Use when the user asks for their standup update, wants to know what to say at standup, needs an async Slack or Teams post, or wants a team standup roll-up."
---

# Standup Update Writer

You turn the user's recent activity into a standup update they can deliver or post. It works for live standups, where they need talking points, and for async ones, where they need a written post. Keep it short, put blockers first, and back every line with data or with what the user told you.

## What to pull from

Use the connected tools and sources that are available:

- **Git hosting** (GitHub, GitLab, Bitbucket): commits since the previous standup, open and merged PRs
- **Project tracker** (Jira, Linear, Asana, Shortcut): tasks in progress, done, and blocked
- **Chat** (Slack, Teams): threads that mention blockers or decisions
- **Uploaded documents or connected knowledge sources**: sprint goals, the team's preferred standup format

*If nothing is connected, have the user supply the context themselves.*

## Steps

### 1. Collect recent activity

Unless told otherwise, the reporting period runs from the previous business day. Pull what you can from connected tools, and ask the user for anything a missing tool would have provided. Look for:

- **Completed** — in the tracker, items marked done or closed; in git, merged PRs. Signals: tickets closed out, PRs merged, features released.
- **In progress** — in the tracker, items marked in progress; in git, open PRs and recent commits. Signals: tickets under way, PRs in review, active branches.
- **Blocked** — in the tracker, items marked blocked or on hold; plus the user's own input. Signals: tickets flagged blocked, PRs that have been waiting for review for more than 24h, a dependency on another team.
- **Upcoming** — in the tracker, to-do or next items, and the sprint board. Signals: the next priorities once current tasks finish.

### 2. Sort and trim

Fit what you collected into the standup structure, following five rules:

1. **Blockers go first.** They are the one standup item that needs others to act, so surface them before anything else.
2. **Summarize rather than list.** "Auth refactor: merged 3 PRs, 1 still in review" beats reciting every PR title.
3. **Tie work to goals.** If sprint goals are available, show which goal each completed or in-progress item moves forward.
4. **Raise risks.** When in-progress work may miss a deadline, put it under blockers or add a separate risk note.
5. **Drop the noise.** Trivial commits (typo fixes, formatting), PRs opened by bots, and administrative tasks don't belong in a standup unless they took real effort.

### 3. Pick the format

Choose whichever of the three formats below fits the situation.

## Formats

### For one person

```
## [Your name] · daily update · [Date]

### Blocked on
- [What's blocked — who or what is needed to clear it — blocked for how long]
[or: No blockers]

### Yesterday (done)
- [Work item — result or progress — linked ticket/PR if relevant]

### Planned for today
- [Work item — concrete goal for today — linked ticket if relevant]

### Risks and heads-ups
- [Anything the team should be aware of — a deadline coming up, a scope change, a dependency]
[or: leave this section out if there's nothing]
```

### For the whole team

Use this when rolling up the team's standup:

```
## [Team name] standup roll-up · [Date]

### Blocked — needs action from someone
- [Person]: [blocker] — needs [action/person]

### Progress on Sprint Goals
- Goal 1: [goal] — [on track / at risk / blocked] — [short status]
- Goal 2: [goal] — [on track / at risk / blocked] — [short status]

### Notable wins
- [Notable completions, deployments, or milestones]

### Today's focus by person
- [Person]: [main focus today]

### Risks to the sprint
- [Risks to sprint commitments or upcoming deadlines]
```

### For async posts (Slack/Teams)

```
**[Name] — [Date]**
✅ Done: [completed items, brief]
🔄 Doing: [in-progress items, brief]
🚫 Blocked: [blockers with needed action]
```

An async update should run 3–5 lines at most. For anything that needs more room, point to the ticket or PR rather than lengthening the post.

## Before you hand it over

Check the draft against this list:

- [ ] Each blocker is specific and says what it would take to unblock it
- [ ] Completed items state outcomes, not effort ("shipped the auth fix", not "worked on code")
- [ ] Planned items are specific enough for the team to see what the user intends to finish
- [ ] Nothing has appeared in more than 2 standups — an item that keeps recurring needs a separate conversation (escalation or re-scoping)
- [ ] The update can be spoken in under 90 seconds (live) or read in under 30 seconds (async)

## Ground rules

- **Don't invent activity.** If there's no data, say: "No activity data available — provide your update or connect [tool name]."
- **Don't guess a ticket's status.** If the project tracker can't tell you, ask the user instead of assuming.
- **Don't make up blockers or risks.** Report only what the data or the user confirms is blocked or at risk.
- **Label the source of every item:** `[From project tracker]`, `[From git]`, or `[From user input]`.

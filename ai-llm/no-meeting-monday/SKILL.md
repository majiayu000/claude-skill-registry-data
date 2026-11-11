---
name: no-meeting-monday
description: "Replaces the weekly team status meeting: collects what each person got done from team chat and the project board, surfaces blockers and stalled tasks, keeps one decision log, pulls action items and owners from call notes, and drafts a one-page Monday brief. Use when a manager wants a weekly update without a meeting, asks what got done, what is stuck or what was decided, or says \"monday brief\", \"status update\" or \"no meeting monday\". Drafts only; never posts or changes tasks."
---

# No Meeting Monday

Five agents that read what your team already wrote down (chat, project board, call notes) and draft a one-page Monday brief: done, stuck, decided, open actions, and at most three things that still need a real conversation.

For teams of roughly 3 to 30. Not for performance reviews or anything about one person's conduct.

## What you need

| Source | Connector (Claude.ai or Claude Code, if your plan and admin allow) | Fallback |
|---|---|---|
| Team chat | Slack | Channel export, or pasted messages with author and date |
| Project board | Asana, Linear, Notion, Jira/Atlassian | CSV export: title, owner, status, last updated, due date, completed date |
| Call notes (optional) | Your note taker's connector (e.g. Fathom, Granola), or Google Drive docs | Pasted transcript or summary |

If a connector is missing, ask for the export or paste, name the columns needed, and carry on. The brief's "Sources and gaps" line says what ran on pasted data.

## Setup (`start`, or when PROFILE is empty)

Ask in two rounds, accept "skip", then show PROFILE and TEAM back.

Round 1
1. Who is on the team, their role, and what each person owns?
2. Which channels hold real work updates? Which must never be read?
3. Which project board, and connector or export?
4. Where do call notes end up, if anywhere?

Round 2
5. Days without movement before a task is "stuck"? Default: 5 working days.
6. What counts as a decision here? Default signals: "we will", "decided", "agreed", "going with", "approved", or a clear yes from the area owner.
7. Who reads the brief and where is it shared?
8. Weekly run? (see Scheduling)

## Commands and routing

| Command | Runs |
|---|---|
| `monday brief` | 1, 2, 3, 4 over the period since the last brief (default 7 days), then 5 |
| `updates [person]` | 1 |
| `blockers` | 2 |
| `decisions` | 3 |
| `call notes` | 4 |

Before acting as an agent, read its file in `agents/`. In Claude Code you can copy them to `.claude/agents/` to run as real subagents.

- `agents/01-update-collector.md`: done and in progress, per person
- `agents/02-blocker-finder.md`: waiting, stalled, overdue, unanswered, ranked
- `agents/03-decision-log.md`: CLEAR / UNCLEAR / REVERSED decisions with source
- `agents/04-call-notes-reader.md`: action items, owners, due dates from calls
- `agents/05-monday-brief.md`: the one-page draft

## Safety rules (every agent)

- Never post, send, react, reply, create, close, reassign or edit anything. The brief and any nudges are drafts with IDs (B1, N1...). The manager shares them.
- Only what is written. No visible update = "no update found", never a guess.
- Every line cites its source: channel and date, task name, or call and timestamp.
- Read only channels and boards listed in PROFILE. No private messages unless the manager pastes them.
- Report work, not people. No judgments about effort.
- NEEDS YOU, never the brief: conflicts between people, pay, health, hiring or firing, anything marked confidential. One-line reason each, manager only.

## Shared files

Claude Code: files in `team/`. Claude.ai: print updated tables at the end so the manager can save them to Project knowledge.

- `PROFILE`: setup answers
- `TEAM`: name | role | owns
- `DECISIONS`: date | decision | decided by | affects | status | source
- `ACTIONS`: id | task | owner | due | source | status
- `BRIEFS`: past briefs, so the next one shows what changed

## Scheduling (optional)

Nothing runs on its own. In Claude Code, `/schedule` a weekly routine with the prompt `monday brief` (connectors must be available to it); the Claude desktop app's scheduled tasks work where your plan has them. It still only writes a draft.

## End of every run

1. One line per agent that ran.
2. The brief draft with its ID.
3. Other drafts awaiting approval (nudges, recap questions).
4. NEEDS YOU items.
5. Sources missing or not connected.
6. "Nothing has been posted or changed."

Example (fake data):

```
Ran: Updates (#eng, #design, board export 12 Oct), Blockers (4), Decisions (3), Call notes (2 calls), Brief.
Draft B7: Week of 12 Oct (one page, below).
Drafts waiting: N1 nudge to Sam re: API keys (blocking 3 tasks).
NEEDS YOU: 1 item (hiring discussion in #leads, not in brief).
Missing: no call notes for Thursday planning call.
Nothing has been posted or changed.
```

---
name: pickup
description: "Use for \"catch me up\", \"where did I leave off\", \"what's the state of X\", or before resuming work on something that's been sitting. Rebuilds the current state from live git, open PRs, the tracker, and the shared record, checks it against reality, and hands back a short brief with the next move."
disable-model-invocation: true
---

# Pickup

Before resuming work, rebuild where things stand and hand back a tight brief. Where it is, what's open, what's been tried, what to do next.

Stay on topic. Read only what the in-scope threads need. The heavy reading goes to subagents; the main thread keeps their findings and the final brief.

## Where the state lives

- **Live state.** Git branches, worktrees, uncommitted changes, open PRs and their checks. This is the truth. Everything else is history.
- **The tracker.** The task, its status, what's attached, who owns it. `tracker` says which backend the repo uses and how to read it.
- **The shared record.** What happened around the same code under other names. Bugs users keep reporting, fixes that shipped and got reverted, errors still firing. That's what `why` searches. A feature with a long bug tail keeps most of its story there.
- **Your own history.** If your harness keeps session transcripts and gives you access, they hold what you did and decided. Use them when they're there. Don't depend on them.

## Steps

1. **Classify.** One specific prior session to resume with a full state capsule already in hand: skip the mining and go. Turning habits into a skill is `reflect`, not this. Pickup loads working context before you act.
2. **Lock the scope.** The window, default the last seven days. The topic, if named. The repo, default the one you're in. State it back. Never quietly narrow "all" to "recent".
3. **Check live state first.** `git status`, `git branch -a`, `git worktree list`, `git log` on the relevant branches, `gh pr list` and `gh pr view` for open PRs, CI status. The worktree registry if the project uses one. A minute of work that anchors everything else.
4. **Read the tracker.** The task, its history, attachments, comments. What was turned in, what got sent back.
5. **Sweep the shared record when the topic names a thing.** A feature, file, subsystem, or bug. Hand it to `why`'s investigators with the question changed from "why was this built this way" to "what's the current state, what's been tried and didn't hold, what are users still reporting". One investigator per source, empty results are findings, unavailable sources named. Skip only for pure activity recall with no named target.
6. **Mine your own history if it's available.** Fan out subagents over the sessions in scope. Each returns the same shape per session: topic, goal, decisions, open threads, corrections, artifacts. Raw transcripts stay in the subagents.
7. **Verify against live state.** A transcript or a stale ticket is history. Every PR, branch, and ticket that surfaced gets checked with git and gh before it goes in the brief.
8. **Write the brief.**

## The brief

- **Capsule.** At most five bullets. What this work is and where it stands.
- **Threads.** One line each with exactly one status tag. `[merged #N]`, `[open PR #N]`, `[in flight <branch>]`, `[verified, uncommitted]`, `[reverted #N]`, `[planned, not started]`. An untagged thread isn't done being described.
- **Problems.** At most five, the recurring ones. What users keep reporting, what shipped and got reverted, so the next attempt starts where the last one failed.
- **Next move.** One concrete action.

Adjacent work stays out unless it blocks this. When the brief outgrows a screen, cut detail before you cut threads. Cite live findings by PR or branch, tracker findings by id, shared-record findings by source. Strip anything private before it goes anywhere public.

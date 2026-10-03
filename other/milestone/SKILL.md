---
description: Record a change that reshaped the repository — what moved, why it was worth doing, and which areas it touched. Use after a migration, a rewrite, or a decision that changed how part of the system works.
disable-model-invocation: true
---

# Record a milestone

A git log says what changed. It rarely says **why the change was worth making**, and never says
which areas moved together. Six months later that is what somebody needs — usually while deciding
whether they are allowed to undo it.

## When to write one

For a change big enough that a newcomer would ask "why is this part like that?"

- a migration — a database, an auth model, a framework
- a rewrite of a module, or a service split in two
- a design reversal: something was done one way, then deliberately undone

Roughly a handful a year on an active repository. If you are writing one a week, they are commits,
not milestones, and the file stops being readable.

## When not to

- **A task, or something in progress.** That is `STATE.md`, or a session record.
- **A single decision with no structural change.** That is `/chamnan:remember` →
  `.chamnan/memory/decisions/`.
- **A repeated procedure.** That is `/chamnan:capture`.
- **Anything with a status, an owner, or a due date.** This is not project management, and adding
  those fields would quietly turn it into a worse version of a tool you already have.

## Where it goes

```
.chamnan/milestones.md
```

One file, and entries are **appended at the end**. Newest last is deliberate: appending keeps every
diff to added lines, where prepending would rewrite the context of the whole file each time.

## The format

```markdown
## 2026-08-20 — Authentication migration

**Why:** sessions dropped under load; the old design held state per node.
**Affected:** auth module, API layer
**Decisions:** short-lived tokens; the old endpoint stays for one release
```

Four parts, and the middle two carry the value:

| | |
|---|---|
| Date and title | ISO date, then a short name for the change |
| **Why** | The problem that made it worth doing. Not "we migrated auth" — *what was going wrong*. |
| **Affected** | Which areas moved together. This is what nobody can reconstruct later. |
| **Decisions** | Choices made along the way, especially anything ruled out. |

Leave out a field rather than filling it with a dash.

Write the *why* as the problem, not the activity. "Migrated to short-lived tokens" is the diff
restated; "sessions dropped under load because the old design held state per node" is the reason,
and it is the half that stops somebody re-treading it.

## What reaches a session

Only the **two most recent titles**, with their dates. The bodies stay in the file, and the agent
reads it when a title looks relevant. So a repository with forty milestones costs the same per
session as one with two.

## What not to put in it

- **No credentials, hostnames or connection strings.** This file is committed. The session-start
  hook redacts what it injects; that does not clean the file on disk.
- No incident write-ups. Name the failure in one clause; a post-mortem belongs in `docs/`.

## Housekeeping

Not pruned by age, on purpose — the oldest entry is usually the one nobody can reconstruct.
Because only titles are injected, length costs nothing per session. Edit an entry if it turns out
to be wrong; a false milestone is worse than a missing one.

Set `"milestones": false` in `.chamnan/config.json` to switch it off.

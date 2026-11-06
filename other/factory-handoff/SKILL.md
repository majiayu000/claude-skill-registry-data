---
name: factory-handoff
description: Hand work from this session to the claude-factory that works this repo. Use when the user says "hand this to the factory" or "let the factory do it". Use also when the user says "queue this" or "file it for the factory". Use also when the user wants to give the rest of a task to the factory's workers. Use also when the user wants to give a branch in progress or a review finding to the factory's workers. Works on any machine where bd syncs this repo's beads, with or without the factory CLI.
---

# factory-handoff

The factory starts a run for each ready, unassigned, top-level bead with the label `factory` in a rig repo.
So a handoff is a good bead plus that label. The full rules are in claude-factory `docs/beads.md`, section "Hand work to the factory".

## 1. Find how this machine reaches the factory

```bash
bd where                      # this repo has beads; stop here if it has none (see the beads-remote plugin)
bd dolt remote list           # a remote: the factory sees the bead after a sync
factory home 2>/dev/null      # a local factory: its CLI can queue and start at once
```

- If `factory home` prints a path, use the factory CLI in step 3.
- If not, use only bd. Then step 4 must push, because the manager runs on another machine.
- If the repo has no bd and no Dolt remote, the factory cannot see a bead. Tell the user, and stop.

## 2. Write the bead

A worker starts with no memory of this session. The bead is all that it gets. Put in it:

- **Title**: the change, as a short command ("Add retry to the upload client").
- **Description**: why the work is needed, what to change, and the files or symbols to start from.
- **Acceptance**: how a verifier proves that it is done (a test, a command, an output).
- **Notes**: the state of this session that a worker cannot see. Give the branch and its last commit if work is in progress. Say what you tried and what failed. Give decisions that the user made, in their words.

Do not put a secret, a token or a private host name in a bead. Beads sync to other machines.

```bash
bd create --title "..." --type task|bug|feature --priority 2 \
  --description "..." --acceptance "..." --notes "..."
```

To hand off an existing bead, add what is missing with `bd update <id> --description/--acceptance/--append-notes`.

**Work in progress on a branch**: commit it and push the branch. Then name the branch in the notes and tell the worker to build on it. Do not leave work only in this checkout.

**Owner decisions**: if the user decided something that a worker must not change, write it in the notes as "Owner decision (date): ...". A worker reads the notes before it plans.

## 3. Queue it

Confirm the bead id, the priority and the start station with the user before you queue. A queued bead starts a run that uses workers and can open a pull request.

```bash
factory queue <rig|repo> <id>            # local factory: label it, clear an old reject
factory queue <rig|repo> <id> plan       # start at a station (default: the factory's first)
bd update <id> --add-label factory       # bd only
bd update <id> --add-label factory --add-label station:plan
```

- Use `station:implement` only when the bead already has a plan in its notes.
- Do not set an assignee. A bead with an assignee does not start.
- Do not queue a child of an epic. Dispatch starts only top-level beads.

## 4. Make the factory see it

- **Local factory**: dispatch looks every 30 s. Nothing more to do.
- **bd only**: run `bd dolt push`. The factory pulls every 5 minutes.
- **Now, not at the next dispatch** (local factory, and only if the user asks): `factory start <factory> <rig> <id>`.

## 5. Tell the user

Give the bead id, its priority, the station, and when it starts (next dispatch, or after the next sync). Use the `factory-status` skill to follow it.

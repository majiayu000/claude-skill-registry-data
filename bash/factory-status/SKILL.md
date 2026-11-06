---
name: factory-status
description: Show what the claude-factory is doing in this repo and what waits on the user. Use when the user asks "what is the factory doing" or "status of my handoff". Use also when the user asks "what does the factory need from me" or "which PRs are next to merge". Use also to follow a bead after factory-handoff. Works with bd alone or with a local factory CLI.
---

# factory-status

Read only. This skill changes nothing.

## With a local factory (`factory home` prints a path)

```bash
factory status                 # each run: station, try, pane, last report
factory status <run>           # one run's full log
factory waiting                # what waits on the user, by rig, and how to answer each
factory ship <rig|repo>        # the ship queue: the next PR to merge, then the others
factory digest                 # per rig: beads by state, the owner queue, PRs to merge in order
```

Show only the rows for this repo's rig, unless the user asks for all.

## With bd only

Run `bd dolt pull` first to make the data current.

```bash
bd list --label factory --status open          # queued, not started
bd list --status in_progress --json | jq -r '.[] | select(.assignee // "" | startswith("factory/")) | "\(.id) \(.assignee) \(.title)"'
bd show <id>                                    # each station's report is a comment on the bead
bd list --label human --status open             # questions for the user
bd list --label rejected --status open          # beads a station sent back, with reject_reason
gh api 'repos/{owner}/{repo}/pulls?state=open&per_page=100' --jq '.[] | select(.head.ref | startswith("factory/")) | "\(.number) \(.head.ref) \(.title)"'
```

## Report

Keep it short:

1. Runs in this repo: bead, station, how long, the last report in one line.
2. What waits on the user: gates, `human` beads, PRs to merge, each with the command that answers it.
3. Beads rejected or deferred since the last check, with the reason.

## What waits on the user

Only the user answers these. Give the command, and run it only when the user tells you the answer:

```bash
factory decide <run> <outcome> [note]                 # a gate: approve, reject and so on
factory decisions answer <rig> <bead> <answer>        # an owner decision
bd human respond <id> -r "<answer>"                   # a human bead, bd only
```

---
name: no-shared-writes
description: "Use when two or more agents, processes, or threads might write to the same file, branch, key, worktree, port, or state object. Give each one its own target first. Add a lock only when one shared writer is a real requirement, and make the lock structural, not a convention."
disable-model-invocation: true
kind: principle
---

# No shared writes

When two things might write to the same place, first ask whether they need to. Usually they don't. Give each one its own file, key, branch, or directory and merge where someone reads the result. Add a lock only when a single shared target is a real requirement, and enforce it by structure, not by asking everyone to take turns.

Races on shared state are intermittent, hard to reproduce, and expensive. Telling agents or threads to "coordinate" doesn't work. Instructions aren't concurrency control.

## How

1. **Find the shared writes.** Files more than one thing reads and writes. Branches more than one thing pushes to. A worktree two agents might both check out. A port two dev servers might both bind. An API one side defines and the other consumes.
2. **Default: split the target.** Ask whether the writers need one canonical object or are each publishing their own facts. Almost always the second. Give each writer its own file, key, branch, or state directory, and combine only when reading or reporting. Two workers writing their own field into one `state.json` is still a shared write. `indexer-state.json` and `metrics-state.json` is not.
3. **Only if one shared target is a real requirement, serialize it structurally.** A lock file, sequential phases, a single-writer process, or compare-and-swap. Treat "we need a lock" as something to question, not the first answer.

## For agents specifically

One task, one branch, one worktree. Before creating or touching a worktree, check who owns it. Ports and hosted environments count too. Two agents on the same branch or port is the same bug as two threads on the same variable, just slower to show up.

The worktree-lock skill is this rule applied to workspaces. It tracks ownership so an agent can claim, check, release, or hand off a worktree without colliding with another one.

## The test

For every place something gets written, can you name exactly one writer? If not, split it or lock it. If a comment or an instruction is what keeps writers apart, you have neither.

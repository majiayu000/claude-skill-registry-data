---
name: worktree
description: Create or inspect runtime-adaptive isolated Git workspaces with explicit ownership and delivery routing
when_to_use: "create worktree, isolated branch, parallel session, managed worktree, list or clean worktrees"
argument-hint: '"task prompt" | list | preserve | integrate | clean <delivery-id>'
user_invocable: true
---

# Worktree

Create or manage isolated agent workspaces without assuming every runtime uses
a sibling directory plus immediate branch. Worktree ownership is recorded in
the shared `$delivery` state; independently reviewable work integrates through
the target repository's PR/queue policy, not an arbitrary local merge.

---
name: mav-block-propagation
description: Idempotent, resumable propagation of a `blocked-by:#N` block from an ejected story to every transitive downstream story in the epic DAG. Triggered when agent-code-reviewer ejects a PR for human handling.
user-invocable: false
disable-model-invocation: true
---

# Block Propagation

When an agent-code-reviewer ejects a PR for human handling, every
downstream story that depended on it is transitively broken. Without
propagation, downstream stories keep branching off and stacking on top of
a broken base, producing PRs that cannot merge or merge into a broken
tree. The `blocked-by:#N` label is the mechanism that stops every
instance from trying.

## Running a propagation

The entire marker-write-walk-clear protocol is one idempotent, resumable
CLI command:

```bash
uv run maverick bprop run <repo> <epic> --ejected <story>
```

It writes the `maverick-bprop` marker on the epic, walks the DAG's
transitive descendants of the ejected story, applies `blocked-by:#<story>`
and posts a block comment on each (skipping any already labelled),
mirrors each story to `blocked` in the epic state, and deletes the marker
when the walk completes. Re-running after a crash resumes exactly where
the walk stopped — never perform the walk by hand.

If cold-start hydration finds a `maverick-bprop` marker on the epic, a
prior instance died mid-walk: re-run the command above with the marker's
`ejected` story **before any other epic work**. A partially-applied block
set invites downstream PRs to merge against a broken base.

## Cancelling in-flight subagents

A block is useless if a subagent is already deep into a now-blocked
story. After the walk:

1. Check `.maverick/worktrees/` for any worktree whose branch refers to a
   now-blocked story.
2. For each: stop the subagent, release its claim (see
   `mav-multi-instance-coordination`), **do not push** its work.
3. Destroy the worktree. Do not attempt to salvage in-progress work — the
   base is broken; the work cannot be preserved usefully.

## Block-on-entry checks

Three places must re-check block state at entry:

| Location | Check | Behaviour on block |
| --- | --- | --- |
| Cold-start target resolution | Target has `blocked-by:#N`? | Abort cleanly — report to user |
| Wave selection | Story has `blocked-by:#N`? | Exclude from wave |
| Per-story re-verify (just before coding) | Story gained `blocked-by:#N` since wave start? | Abort story; release claim |

The per-story re-verify catches the race where a block lands *after* a
wave started but *before* every subagent picked up its story.

## Unblock semantics

Maverick never auto-unblocks — the ejection was explicitly delegated to a
human, so unblocking is a human decision (remove the `blocked-by:#N`
label). Wave selection re-reads labels each pass, so a removed label lets
the story run on the next wave.

## Rules

- **Never silently ignore a block.** If your target carries
  `blocked-by:#N`, abort and report — don't modify, push, or claim.
- **Never remove a `blocked-by:#N` label from inside the workflow.**
  Maverick only applies and reads.
- **Always re-check at entry.** Another instance may have applied or
  removed a label since your run started.

<!-- maverick-plugin-version: 4.0.2-dev -->

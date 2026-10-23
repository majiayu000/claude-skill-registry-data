---
name: stacked-prs
description: Work native GitHub stacks bottom-up and prefer merging the whole stack in one command; drain the ready lower layers first only when the upper layers will clearly take longer.
---

# Stacked pull requests

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/stacked-prs/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Use when a change is a chain of native GitHub stacked pull requests. Read local `AGENTS.md` and
`AGENTS.md` first. They own whether this repository stacks, which tool creates, rebases, and merges
a stack, and who may authorize a merge.

- [gh-stack mechanics](references/gh-stack.md): commands, import, submit and verify, the forge as
  the only truth.
- [Drain and keep track](references/drain.md): ownership, shepherding, ready-prefix merge checks,
  and reconciling the ledger.

## Shape

- Each pull request except the bottom one targets the pull request below it. The bottom pull
  request targets the default branch.
- GitHub merges the selected pull request and every unmerged pull request below it, bottom-up, as
  one operation. That merge is available only when everything below already meets this repository's
  merge requirements. An isolated middle layer cannot merge.
- Auto-merge is unsupported. A non-stack merge is not a substitute.
- When a mid-stack pull request's base is an unmerged branch, confirm the merge path understands
  stacks before merging.
- Re-read the forge's layers, order, and bases immediately before a rebase, merge, or status
  report. Local stack metadata is stale after a rebase, relink, or manual recovery.
- The bottom layer's base must be the default branch. Otherwise merge that base or re-root the
  stack onto the default branch before draining.

## Work bottom-up

- Work bottom-up. Write layers in stack order, and never start a layer before the one below it is
  in decent shape.
- A lower layer is in decent shape when it is committed, its local checks have passed, its pull
  request is open with an updated body, and shepherding has started. Decent shape does not mean
  green CI, ready for review, or merged.
- Start the next dependent layer once the lower layer is in decent shape. Do not wait for merge,
  a ready-delay, or green CI.
- On each shepherd result, act on the lowest owned layer that is not ready before any higher
  layer. Put each fix on the lowest layer that owns it. A bottom layer that reaches ready early
  waits for the rest of the stack unless the layers above will clearly take longer; keep readying
  them.
- Before a command that adds layers to a stack, such as `gh stack add` or `gh stack link`, add the
  forge's open-layer count, plus every locally tracked layer not yet submitted, to every layer the
  command would add. `gh stack add` creates only a local branch, so repeated adds before a submit
  are invisible to the forge count. Above the layer cap (default 10),
  open independent work as its own pull request on the default branch and hold dependent work
  until the bottom layers merge.
- A ready, mergeable, or queued lower layer blocks only an operation that would rewrite that
  layer. Keep readying every other owned layer.

## Merge the whole stack

- Prefer merging the whole stack at once: when every layer is ready and inside the human's
  approval, merge it with one command whose target is the top layer. Never merge one layer at a
  time, and never merge only the lower layers when every layer is ready.
- Ready every layer in parallel so the stack reaches ready together. A ready lower layer waits
  while the layers above are close behind (a poll or a ready-delay away).
- Drain bottom-up only when the layers above will clearly take longer: a requested change or
  `TRIAGE` still open, a pending human review, a blocker, or CI far longer than the wait so far.
  Then merge the ready lower layers in one command whose target is the highest ready layer, state
  why in the report, and merge the rest together when it is ready.
- Re-read every layer's readiness immediately before merging. If the whole stack is ready and
  approved, the target is the top layer; never retarget past the approval.
- Nothing in the stack merges on its own. Run the merge checks in
  [Drain and keep track](references/drain.md#merge-the-whole-stack) before each merge.
- After a bottom-up drain, GitHub retargets the next unmerged layer onto the default branch. That
  layer is the new bottom.
- On a stall, or when a layer closes without merging, stop if the bottom layers are otherwise
  ready. Report every layer and ask before draining them.
- A stall blocks only layers that depend on it. Ready the others. Pause the whole drain only when
  nothing further can be readied without the blocked layer.

## Ownership and workers

- Act only on layers assigned to you. Report the other layers; do not change them.
- One worker per native stack implements that stack and runs its shepherd poll. The parent does
  not poll. It reconciles stacks, starts a worker, and carries merge questions to the human.
- Start shepherding when the first owned pull request exists.
- Independent stacks run at the same time, one worker each. Dependent unmerged work is another
  layer of the same stack, not a second stack whose base is an unmerged head.
- At most one poll process per stack. The parent does not run a second poll for the same stack.
- This skill does not grant a merge. Merge authorization stays with the consumer.

Consumer wrapper owns: default branch, stacking tool and commands, merge-selector syntax, layer cap,
pull request description tool, ownership stamp format, and merge authorization.

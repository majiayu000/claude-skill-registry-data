---
name: finishing-a-development-branch
description: Use when work on a branch is believed complete and ready to merge, or when closing out a branch after its work landed.
---

# Finishing a Development Branch

Believing a branch is done is not the same as it being mergeable, and merging is not the same as
the branch being finished.

## Guardrails

- Run the actual verification the branch's work requires — tests, build, the plan's Definition of
  Done — before calling it ready. See the `verification-before-completion` skill.
- Confirm the diff matches what is being claimed: no debug code, no unrelated changes, no file left
  half-migrated. Scan the whole diff, not only the files you remember touching.
- Classify the integration boundary before asking. Merging an orchestrator-created temporary branch
  or `.worktree` back into the task's owning branch is Delegated after verification. A merge or push
  to a shared branch requires human approval only when the project's authority contract marks that
  transition Escalation or Reserved.
- After the merge lands, verify it actually contains the work — the merge commit exists, it is on
  the target branch, and it is not a fast-forward that silently skipped a commit.
- Close out what the branch was for: delete the branch once merged (unless the project's convention
  keeps it), close the tracking issue or plan, and record anything closeout should capture — an
  architectural decision, a follow-up, a lesson — while the context for it still exists. A branch
  left dangling after merge, or a plan left open after its build landed, is unfinished bookkeeping
  that costs someone else the archaeology later.

## What this is not

Not a requirement to squash history or follow one specific Git workflow — the project's own
branching convention decides that. This is about the branch's actual state matching what everyone
believes about it before it disappears.

## Integration contract

When used by `plan-driven-build`, receive the final verification result, changed-path summary, open
findings, branch state, authority contract, and release requirement. Perform Delegated internal
integration and cleanup directly, including verified worktree-to-owning-branch merges. Return evidence
for any remaining external transition. Stop only when that transition is Escalation or Reserved;
do not manufacture a human gate for reversible repository plumbing.

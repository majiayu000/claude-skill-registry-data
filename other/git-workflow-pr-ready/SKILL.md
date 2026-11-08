---
name: git-workflow-pr-ready
kind: pattern
rule: git-workflow
description: Pattern of rule git-workflow. Load when PRs are already open — leaving draft, handling a red run, bringing a chain to readiness, the order "finish what was handed over first, then take new work". Opening one PR — pattern git-workflow-pr; the chain order — git-workflow-stack.
---
<!-- rt-kit v0.34.0 · patterns/git-workflow-pr-ready.md · f8431e77e19b · правится надстройкой, не здесь -->

# Bringing a PR to readiness

Pattern of the rule `git-workflow`. What must be true — the law
`docs/constitution/delivery.md`. Opening a PR — pattern `git-workflow-pr`, the chain order —
`git-workflow-stack`, resolving one conflict — `git-workflow-merge`.

## When to use

- A PR is open as a draft, and its run has ended.
- Several PRs are open at once, and it must be decided what comes first — finishing them or
  taking the next task.
- The PR's run is red, while the edit in the branch is green on its own.

## A draft is the state of the work, not its look

A draft says one thing: the work cannot be merged. The host locks its merge button, and the
owner opening the list sees not "done" but "being done". A PR with a green run and a draft not
lifted is done work that looks unfinished, and only the one who handed it over can fix that.

Hence the order: **the draft is lifted in the same turn in which the green run was read.** Not
the next one, not after a neighbouring task.

```bash
gh pr ready <номер>
```

Lifting the draft is the last step of handing the work over, not a separate matter. Until it is
done, the work is not handed over, however many commits lie in the branch.

**A merge the executor was told to make goes after the run on the tip is read by a command.** The
merge command is refused by the delivery guard on a red or unfinished run; a click on the host's
button no guard sees, so before it the run is read the same way. An epic went into main over a red
image build, and the rollout fell after it.

```bash
gh run list --commit "$(gh pr view <номер> --json headRefOid --jq .headRefOid)"
```

## Finish the handed-over first, then take new work

An open PR is work in flight: its run ages, its branch lags behind main, its body describes the
tree on the day it was written. All of this is cheap to fix today and expensive three tasks later.

So the queue is this:

1. The runs of the open PRs are read, drafts with green ones are lifted.
2. The red ones are analysed and fixed.
3. Only then is the next task taken.

Taking a new task while leaving a dozen PRs behind as drafts means reporting work the owner does
not have: they see a list of "being done", not a list of "done".

## The state is read at once

What it is read with and how each field is read — pattern `git-workflow-freshness`; here only
what is done with what was read. An empty run is handled on a par with a red one: a chain PR's
base is not the main branch, and the base filter does not let such an event through to the
pipeline.

## A red run is analysed by step, not by PR

```bash
gh pr checks <номер>
```

The answer names the failed run and a link to it. Then the host is asked the name of the failed
step — `gh api` on that run, selecting `select(.conclusion=="failure")` over its steps.

The step name is the diagnosis. The fix goes into the chain branch where the cause arose, not
the one where the run went red: in a chain everything above the cause goes red.

## The cause is fixed in the lowest branch, then a wave upward

A cause shared by the whole chain is fixed once, in the lowest branch. It travels up by merging,
not by rebasing: a rebase rewrites the history of branches already handed over, and the host
closes the upper PRs as merged, though main has none of their edits.

The wave goes bottom-up, one branch at a time, and each step is three separate calls: switching
to the next chain branch, merging the previous one into it, pushing. They are not written as one
line: the delivery guard refuses such a command, and rightly — the check set runs on the tree
that lies there when the command is reviewed, that is, on the previous branch.

A branch skipped in the middle leaves its PR red and breaks the merge order, so the wave passes
the whole chain.

## Common misses

- The draft is not lifted because "the run is still going". The run ended an hour ago; its state
  is read, not the memory of it going.
- The next task is taken, and a dozen PRs stayed drafts. For the owner nothing is done.
- The red is fixed in the branch where it went red. In a chain that is the upper one, and the
  cause is in the lower; a fix from above leaves everything under it red.
- The cause is sent across branches by rebasing. The handed-over branches are rewritten, the PRs
  closed as merged, main has no edits.
- An empty run taken for a green one. The event never reached the pipeline, and the PR is not
  checked at all.

---
name: get-it-done
description: "Pursue an agreed goal to a working outcome without waiting: decompose it, re-prioritise as evidence arrives, branch, gate, get an independent review (a different model or a fresh reviewer subagent — the writer never approves), merge, prune, and bank the operator's decisions in STATUS.md instead of blocking on them. Trigger on \"get it done\", \"don't wait for me\", \"proceed autonomously\", or when an epic or roadmap objective is handed over. Not a close-out: this work set is expected to grow."
---

# Get it done

**The planning, the talking, the debating are over. The plan is agreed —
execute it.** Do not re-open scope, do not re-surface options already ruled on,
do not ask for reassurance. The only reason to interrupt is a decision from the
short "Theirs, always" list below; everything else is action.

The operator has left. **Finish the phase.** Do not stall on anything you can
decide, evidence, or work around — and do not silently decide anything that is
genuinely theirs.

The whole skill is one judgement: **what is mine to call, and what is theirs?**
Get that wrong in the timid direction and the work sits idle for hours. Get it
wrong in the reckless direction and you spend their money, their credibility, or
their consent on a call they never made.

## The boundary — this pursues a goal, it does not close a queue

The unit here is a **goal**: an epic, a roadmap objective, a phase, a thing that
must end up *working*. The work set is derived from that goal and **is expected
to grow** — you decompose, you discover, you re-prioritise as evidence arrives,
and you update the delivery tracker as you go rather than at the end. Done means
the goal is functional, not that a list is empty.

A close-out is the opposite shape: its work set is **frozen** at invocation and never
grows, and it ends in a release advisory. If the operator asked you to close out what is in
flight, do that job, not this one. Running this skill against a closing set is how a
close-out quietly turns into a new sprint.

## The contract

1. **Do not wait.** No "shall I proceed?", no "let me know". If you can act, act.
2. **Bank, don't block.** A decision that is genuinely theirs goes into
   `STATUS.md` with a recommendation — not into a message that stops the work.
3. **Land it.** A phase is not done because the code is written. It is done when
   it is merged to `main`, the branch and worktree are pruned, and the tracked
   documents match reality.
4. **Never fabricate authority.** Blanket "go" covers ordinary work. It does not
   convert into permission for the four things below.

## Theirs, always — bank these, never assume them

Even under an explicit "don't wait for me":

- **Money.** Raising a spending limit, a plan, a paid tier, a metered vendor.
- **Consent, credentials, retention, permissions.** Anything a user agreed to,
  anything that reads or keeps their data, anything holding a secret.
- **One-way doors.** Tags, releases, published artefacts, external submissions,
  force-pushes, deleting a ref whose commits are not reachable from the trunk.
- **Self-approval of a governance record.** An ADR is never accepted by the
  agent that wrote it. Draft it, evidence it, and flag it.

Everything else — ordinary code, tests, docs, refactors, issue filing, branch
hygiene — is yours. Do it.

## When a dependency is missing, route around it and say so

A blocked gate is not a reason to stop; it is a reason to substitute and record
the substitution.

| Unavailable | Substitute | Record |
|---|---|---|
| Hosted CI (quota, outage, no runner) | Run the local equivalent of **each** required check | Name each check and its local equivalent, with exit codes |
| Hosted code review (quota) | An independent reviewer: a different model or a fresh reviewer subagent | Which reviewer, what verdict, what it found |
| The first reviewer unavailable | An alternative only within the project's authorised review policy; otherwise stop the affected gate | Availability, authority and unresolved evidence |
| A required check that *cannot execute* | Merge on the local evidence if the repo permits it | **Say "past checks that could not run", never "past checks"** |

The distinction in that last row is the whole point. A check that failed and a
check that could not start are different facts, and conflating them is how an
unreviewed merge gets laundered into a reviewed one.

**Never route around a guard that exists to stop you.** A denied push, a
protected branch, a consent gate — those are the operator's intent expressed in
config. Routing around them is permission laundering, not resourcefulness.

## The loop

For each unit of work:

1. **Branch.** Never commit to the trunk.
2. **Build**, with the project's own gates run as you go — not saved for the end.
3. **Prove it bites.** Break the source deliberately and confirm the test fails.
   A green suite you have not seen go red is a hypothesis.
4. **Review independently.** A fresh reviewer context running `pr-reviewer`, with optional
   provider diversity under local policy; `adversarial-gate` for design. Follow the
   [Council contract](../pr-reviewer/references/independent-council.md) for bounded loops.
   **The writer never approves the work.** If the candidate changes after review, the review
   is void — re-run it.
5. **Merge** with a merge commit. Never squash, never rebase onto the trunk.
6. **Prune** the branch and worktree — but only once `git cherry` confirms the
   commits are reachable from the trunk. Where integration reworked a patch into
   a new SHA, deleting the ref loses history. Keep it and say why.
7. **Reconcile.** STATUS, CHANGELOG, ROADMAP, ADRs, issues. Findings that live
   only in a chat message evaporate; file them.

## Parallelism

Use worktrees and subagents where the work is genuinely disjoint. **Two agents
editing the same file is not parallelism, it is a merge conflict with extra
steps** — and most "parallel" refactors of one subsystem collide. Say so rather
than parallelising for appearances.

## The handover

`STATUS.md` is what they read when they return, so write it for someone who was
not in the room. It carries:

- **What landed**, with evidence — a SHA, an exit code, an issue number.
- **The decisions waiting on them**, each with: a recommendation (a verb and an
  object, never "consider the options"), what it unblocks, **what it costs if
  they call it wrong**, and whether it is reversible — `cheap`, `costly`, or
  `one-way`. Sort so the compounding ones are first.
- **What you did not do, and why.** Especially anything you declined as theirs.
- **What is still open**, including defects you found and chose not to fix.

## Reporting back

Lead with the outcome, not the narrative. State what merged, what the evidence
was, what you routed around, and what is waiting on them. Report failures
plainly — a phase that half-landed is reported as half-landed.

Never claim a gate passed that you did not run, and never inherit a figure from
an earlier session: **re-derive it, or label it unverified.**

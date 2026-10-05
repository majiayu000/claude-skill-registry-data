---
name: plan-verifying-execution
description: >-
  Guides judging whether completed execution actually did what the plan said, by checking claims against the repository
  rather than against the checklist.
when_to_use: >-
  Use when auditing finished plan execution before archival.
---

# Verifying Plan Execution

The temporal sibling of validating a draft. The same domains, asked after the fact, against the repository instead of
against the text.

## Verify Against the Repository, Not the Checklist

A ticked box is a claim. The entire value of this audit is testing claims against what the repository now contains.

Does the file exist at the path the item named? Does the command still pass when re-run? Does the evidence establish the
criterion it is filed under, or merely sit next to it?

An audit that reads only `delivery.md` establishes that the plan is internally consistent — which was never in doubt,
and which a plan can be while describing work that did not happen.

## The Two Silent Failures

**Scope drift.** Work added quietly because it seemed necessary, or dropped quietly because it turned out not to be.
Both are invisible in a checklist where every box is ticked. Compare what was delivered against what `prd.md` said, not
against what `delivery.md` recorded.

**Evidence that does not establish its claim.** A passing test filed under a criterion it does not exercise. A
screenshot filed as proof of a behaviour it does not show. These pass a glance and fail on reading.

## Gates Must Have Actually Run

A declared gate that never ran is not a passing gate. Check for the evidence record — command, commit, timestamp, result
— rather than for the absence of complaints.

A gate that returned findings and was then repaired is fine, and is a different thing from a gate nobody invoked.

## Cleanup Is Proven, Not Assumed

Re-list the paths the plan said would be removed. "Cleanup ran" is a claim of the same kind as a ticked box.

## Knowledge Capture Is Part of Execution

Every learning must reach a durable owner or be discarded with a reason. An unrouted `learnings.md` blocks archival —
this is the step most often waived, and the one whose omission costs the most later, because the discovery is lost at
exactly the moment it was cheapest to keep.

## Blocking Is the Default

Report what is unresolved plainly rather than passing with a caveat. A caveat in a verdict is read as a pass by everyone
who skims it.

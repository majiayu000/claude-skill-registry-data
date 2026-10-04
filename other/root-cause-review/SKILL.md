---
name: root-cause-review
category: quality
description: Use when a task in code_review was sent back before (an earlier need_revision comment exists) - verify every prior point was fixed at its root
---
# Root-Cause Review

## Overview

When a task returns to code_review after a need_revision cycle, the question is not "did something change" but "was the ROOT CAUSE addressed". Symptom patches come back as bugs; catching them here is cheaper than in QA or production.

## The Process

0. **Find the prior feedback first.** A re-submission enters code_review from `in_progress`, so the earlier need_revision comment is NOT injected into this run automatically — `list_task_comments` on this task is how you find it (also check `get_task_pull_request` for human reviewer comments on the PR itself).
1. **Re-read the prior feedback**: your previous need_revision comment, the QA failure report, or the pipeline failure — list every numbered point.
2. **Map each point to the new diff**: for every point, find the exact change that addresses it. A point with no matching change means the revision is incomplete → back to need_revision citing the unaddressed point.
3. **Judge root cause vs symptom** for each fix:
   - Symptom patch: special-casing the failing input, catching-and-ignoring the error, widening a timeout, deleting the failing assertion.
   - Root-cause fix: the change explains WHY the failure happened and removes that mechanism at its source.
4. **Check the guard test**: a test now exists that reproduces the original failure and passes with the fix. No guard test → Important finding.
5. **Watch for regressions**: revision diffs are written under pressure — re-check the surrounding code paths the fix touches.

## Worked Example (symptom vs root cause)

Prior finding: "export returns empty CSV on DB error (swallowed error)."

- **Resubmission A (symptom patch):** the diff wraps the export call in the handler with `if len(csv)==0 { return 500 }`. Rejected → back to need_revision: *"Point 1: the swallowed error at service.go:24 is still there; you inferred failure from an empty result instead of propagating the error. An empty project also returns empty CSV, so this now 500s a valid empty project. Fix the source."*
- **Resubmission B (root cause):** `ListByProject`'s error is propagated and mapped to 500; a test injects a repo error and asserts 500; the empty-project test still asserts 200 + header-only CSV. Approved → ready_for_qa.

The tell was step 2: B's fix touched service.go:24 (where the mechanism lives); A's didn't.

## Verdict

- Every prior point addressed at the root, guard tests present, pipeline green → ready_for_qa.
- Any symptom patch, unaddressed point, or missing guard test → need_revision, quoting the specific gap ("Point 3 from the previous review: ... — the new diff only catches the exception; the invalid state is still produced upstream in ...").

## Red Flags

- The diff deletes or weakens a failing test instead of fixing the behavior.
- A fix touches none of the files where the failure mechanism lives.
- The fix's commit message or the revision's diff says "fixed" without showing what caused the failure — you never see the developer's closing message, so judge the code and the guard test, not a claim.
- Third revision cycle on the same task — question the design: comment on whether the approach itself is wrong and consider recommending a re-analysis instead of a fourth patch. The system backs this up: three moves into need_revision without a human touch parks the task automatically, so this is also where a real disagreement belongs, not a further round-trip.

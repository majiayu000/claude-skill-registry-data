---
name: review-revision-candidates
description: >-
  Build vN+1 of a rejected patch, draft or page edit from the reviewer's numbered corrections. When
  resubmitting without touching the working tree, keep the rejected version immutable and deliver
  revised files, a new patch and exact anchors. Not for hoa-skill-review.
metadata:
  revision: "5"
  areas: "work-management"
  targets: "runtime-agnostic"
  summary: "run a rejected candidate's revision round: the numbered list is the whole change set"
  summary_zh: "被驳回候选的返修轮：编号清单就是全部变更集，交的是字节不是辩解"
  kind: "entry"
---


# Revise a rejected candidate

Produce a new candidate and a checkable patch. Keep the rejected version and the working tree
unchanged; the latest approved review list is the entire write scope.

1. **Pin the round.** Reread the current review, request, evidence and ledger. Record the target
   base commit and scoped working-tree state; distinguish pre-existing edits from your work.
   If a newer base or a conflicting instruction changes the round, resolve it before editing.
2. **Build in scratch.** From pristine base copies, reproduce the accepted parts of the rejected
   candidate and apply only the current numbered fixes. Restore excluded hunks to the base.
   Verify each replacement anchor matches exactly once before writing any output. Write the
   revised files and a new `vN+1` patch with stable repo-relative `a/` and `b/` paths.
3. **Check both comparisons.** Compare rejected and revised bytes to verify every fix and find
   off-list changes; compare base and revised bytes to verify the complete patch, including
   removed hunks, valid frontmatter where applicable, and absence of rejected conclusions in
   paraphrase. Run `git apply --numstat` and `git apply --check` against the pinned base from
   its root; validate the current target separately or report drift. Apply-check proves structure
   only. Recheck that the rejected bytes and working-tree state did not change.
4. **Hand back the candidate.** Give the revised files, patch, base SHA, numstat and apply-check
   result, plus one stable patch anchor or new fragment per numbered fix. Name unresolved items
   and any decision still needed. State explicitly that nothing was applied to the working tree.

For evidence wording or a Git patch recipe, see
[review checks](references/review-checks-2026-11-21.md).

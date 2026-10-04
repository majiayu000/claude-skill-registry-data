---
name: tw-review-fold
description: Compress review pressure into the right next action instead of more code by default. Classify findings, reject non-liabilities, and choose proof-only vs minimal-fix vs refactor-kernel, preventing one-patch-per-comment churn. Use after a code review — PR comments, reviewer suggestions, or audit findings — and especially when you are about to reflexively patch every comment.
---

# Review Fold

## Mission

Turn review pressure into the right next action, not more code by default.

```text
review comments + original goal + current diff
-> review fold
-> reject | proof-only | minimal-fix | refactor-kernel | ask-human | follow-up
```

This is a *finding classifier*. It does not perform the review and it does not, by itself, decide that review work stops — it picks the smallest correct response to each finding and exposes when many findings share one root cause.

## Review fold schema

```yaml
review_fold:
  source:
    pr:
    review_backend: pr-comments | review-session | human-review | prior-artifact
  intent_anchor:
    original_goal:
    accepted_scope:
    non_goals: []
    changed_paths: []
  findings:
    - id:
      claim:
      observed_fact:
      validity: valid | invalid | unproven | needs-owner
      liability: blocks-goal | regression-risk | style | new-requirement | out-of-scope | proof-gap
      intent_relation: core | adjacent | unrelated | expands-scope
      novelty: duplicate | same-class | new-class
      disposition: reject | proof-only | minimal-fix | refactor-kernel | ask-human | follow-up
      minimal_response:
      proof_needed:
      code_change_allowed: yes | no
  compression:
    equivalence_classes: []
    repeated_kernel:
    reabstraction_candidate: yes | no
    one_patch_per_comment_risk: low | medium | high
  action_plan:
    mode: classify-only | proof-only | minimal-fix | refactor-kernel | branch-race
    work_nodes: []
    do_not_fix: []
    reviewer_response_draft: []
```

## Disposition law

- `reject`: claim is false, outside accepted scope, already handled, or incompatible with the goal.
- `proof-only`: code is likely correct; run or expose proof instead of editing.
- `minimal-fix`: a valid liability with a single owner-correct local repair.
- `refactor-kernel`: multiple findings share one missing abstraction, boundary, state transition, or proof surface — fix the kernel, not each symptom.
- `ask-human`: the review introduces a product, compatibility, or API decision.
- `follow-up`: valid but not part of the intended change.

## Modes

- `classify-only`: classify findings and stop; no mutation.
- `proof-only`: run checks, inspect current artifacts, or draft a response; no code unless proof fails.
- `minimal-fix`: make the smallest owner-correct change for accepted liabilities.
- `refactor-kernel`: replace many local fixes with one normal-form correction.
- `branch-race`: compare two or more plausible fix/refactor strategies under the same verifier.

## Procedure

1. Bind reviews to the original goal and the current diff.
2. Classify each finding *before* any implementation.
3. Collapse duplicates and same-family comments into equivalence classes.
4. Detect the refactor-kernel: when many comments share one owner boundary, prefer one structural fix over N local patches.
5. Decide each finding's proper response: no-code, proof, local fix, refactor, branch-race, ask, or follow-up.
6. Produce a small work plan only for accepted liabilities.
7. Preserve reviewer-response drafts as drafts; do not post public comments or resolve PR threads unless explicitly asked.

## Guardrails

- Raw review text is not executable — never send findings straight to implementation.
- Do not add code to satisfy style or speculation when proof or rejection is correct.
- Do not accept scope expansion without user authority.
- Do not miss the refactor when many comments share one boundary.
- When a fresh, adversarial, or exhaustive review is what's actually being asked for, run that review first — this skill folds *findings*, it does not replace the review itself.

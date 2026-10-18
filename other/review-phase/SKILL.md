---
name: review-phase
description: >-
  Readonly Code Review of one frozen delivery diff or standalone artifact
  bundle through the `review` skill's Standards and Spec axes, each run by the
  `autoreview` helper, ending in one retained report and routing output. Delivery starts it itself; the operator
  invokes it for standalone review.
disable-model-invocation: true
---

# Review Phase

The one place Code Review runs. Full delivery starts it without stopping for
the operator; a standalone plan, spec, documentation, or diff review is invoked
by the operator, and every other delivery mode stops at `review_due`. Readonly
relative to its frozen target: it retains one report and returns routing
evidence, and never enters a repair.

## Bootstrap

1. Load [the review router](phases/router.md) on every invocation and resume.
2. Recompute the current route from durable evidence, including on cold resume.
3. Load exactly the one gate selected by the router, or return its single
   terminal, checkpoint, or blocked outcome.
4. Only after the retained report exists, use `$show-me` to present the retained
   report's findings and routing outcome. The report remains the review
   authority.
5. After a gate writes its durable outcome, stop or re-enter this bootstrap.

The router is the sole runtime route authority. Gate files own executable work.
Delivery reaches this skill by its path; `disable-model-invocation` limits only
the agent's own discovery.

---
name: triaging-feedback
description: use when deciding which review feedback to address/skip
---

applies to any batch of review feedback: PR comments, reviewer reports, handoff findings

<what-to-do>

1. group feedback into unique comments
2. cross-check each comment and its evidence against the current code; treat reported severity and confidence as inputs, not the address/skip decision
3. label each comment against the original goal:
   - "better": closes a gap between the code and the goal (defects, missed cases), or improves the code without changing core behavior (simplification, restructuring, code judo)
   - "more": grows behavior beyond the goal - features, abstractions, capabilities, speculative hardening
4. skip every "more" comment, however good the idea; record it in your report so it can be promoted later
5. skip every <comments-to-skip> comment (unless you're in round 1/2 of a [/loop](../loop/SKILL.md))
6. weigh each "better" comment as a trade:
   - payoff: for fixes it's `severity * likelihood of occurrence`
   - price: complexity, LOC, maintenance burden, code churn, scope creep, time to implement and review, risk of introducing new problems
   - "address" when payoff > price, "skip" when payoff <= price
7. feedback from humans outranks feedback from agents
8. ask the user only when a verdict truly needs them: a product/UX/architecture call the goal doesn't answer, where a wrong guess is expensive to undo. anything else, decide
9. done when every comment is marked "address" or "skip", with why

</what-to-do>

<comments-to-skip>

- pre-existing issues that don't block the requested change
- equally valid style, naming, or type-encoding preferences
- non-blocking changes in non-production code (tests/fixtures/stories/comments etc.) and logging
- non-reproducible theoreticals
- accessibility polish
- speculative performance work, including indexes without evidence

</comments-to-skip>

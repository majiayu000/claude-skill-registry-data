---
name: plan-mode-counsel
description: Counsel someone making a consequential choice with competing priorities. Use when the user asks what they should do, seeks a recommendation, or needs help weighing tradeoffs under uncertainty.
license: MIT
---

# Counsel

Help the user decide in light of their priorities, without treating advice as permission to act.

1. Identify the choice, the user's stated priorities and constraints, the available options, and the cost of waiting. If a missing priority could reverse the answer, ask for it; otherwise make your assumption explicit.
2. Compare the options on the few factors that matter to this decision. Separate verified facts from estimates and preferences. Check time-sensitive or high-stakes facts before relying on them.
3. Recommend a course of action and explain why it fits those priorities. State the strongest reason to choose differently and the condition under which you would change your advice.
4. Offer a small, reversible next step when one exists. Identify any decision that still belongs to the user.

Finish with a clear recommendation, its rationale, and its material uncertainty. Do not execute the decision unless the user has authorized that action.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.

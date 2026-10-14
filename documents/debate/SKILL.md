---
name: plan-mode-debate
description: Debate a concrete proposal or contested decision from opposing positions. Use when the user wants a rigorous case for and against an idea, an adversarial review, or the strongest counterargument.
license: MIT
---

# Debate

Make disagreement useful by testing the strongest version of each position.

1. State the proposition being debated and the decision it affects. If the prompt is broad, narrow it to a claim that can be evaluated without changing the user's intent.
2. Build the strongest affirmative and negative cases. Give each side its main evidence or reasoning, assumptions, and likely failure condition. Distinguish a factual dispute from a difference in priorities.
3. Make each side answer the other's hardest point. Do not fabricate evidence or claim a consensus that has not been established; identify facts that need checking.
4. Synthesize the disagreement: what both sides accept, what remains decisive, and what observation or test would change the conclusion. Give a verdict only if the user asked for one or supplied a decision rule.

The debate is complete when neither side depends on a straw man and the remaining uncertainty is explicit. Keep the result tied to the proposition rather than expanding into unrelated alternatives.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.

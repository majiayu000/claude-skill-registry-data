---
name: plan-mode-calibrate
description: State how much you actually know before acting. Use when a claim's certainty is uncertain and the decision depends on getting it right.
license: MIT
---

# Calibrate

The most dangerous state is being confidently wrong. Rate your own certainty and act on the rating, not on the confidence.

1. State the claim and the evidence for it: read directly, inferred from a pattern, reported by a tool, or assumed. Label each piece of evidence with its source.
2. Rate the claim as known, likely, uncertain, or unknown, and say what would move it up or down. A claim with no path to being wrong is not a claim.
3. If the rating is below what the decision requires, say so and name the specific observation that would raise it. Do not proceed on a guess because the cost of checking seems high.
4. Record the rating and the path to raise it, so the next person knows what to verify.

Calibrating is read-only and does not authorize proceeding. If the decision cannot wait for the required certainty, say so explicitly and state the risk.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.

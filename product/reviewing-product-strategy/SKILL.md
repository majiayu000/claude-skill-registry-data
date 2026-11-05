---
name: reviewing-product-strategy
description: CEO/founder-mode plan review. Rethink the problem, find the 10-star product, challenge premises.
phase: 6 (Brainstorm)
role: Lead
---

# Reviewing Product Strategy (CEO Review)

**Role Constraints:** Lead (Write/Bash access allowed).
**File Access:** Do NOT use literal placeholders for file paths. Use the `glob` tool to search for the active feature directory under `.jonggrang/.output/features/`.

## Objective
Rethink the problem, find the 10-star product, challenge premises, and expand scope when it creates a better product. Think like a CEO/Founder.

## Execution Steps

1. **Locate Feature Context:** Use the `glob` tool to find the active feature directory under `.jonggrang/.output/features/` and `read` the `pitch.md` or `plan.md`.
2. **Analyze & Interrogate:**
   - Expose the demand reality: Is this truly solving a hard problem?
   - Challenge the status quo: Why hasn't this been solved this way before?
   - Desperate specificity: Who exactly is desperate for this?
3. **Four Modes of Evaluation:** Decide on the approach and present the recommendation to the user:
   - **SCOPE EXPANSION (dream big):** The current plan is too timid. What is the 10-star version?
   - **SELECTIVE EXPANSION (hold scope + cherry-pick):** Mostly good, but add 1-2 high-impact elements.
   - **HOLD SCOPE (maximum rigor):** The scope is right, ensure execution is flawless.
   - **SCOPE REDUCTION (strip to essentials):** The plan is bloated. Cut it down to the MVP.
4. **Draft the Review:** Use the `write` tool to save the strategic review findings into `strategy-review.md` in the active feature directory. Include the chosen evaluation mode, challenged premises, and final scope recommendations.

## Completion Signal
When the strategy review is complete and the file is written, output exactly:

STRATEGY_REVIEW_COMPLETE

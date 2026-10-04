---
name: culinary-reasoning
description: Diagnose culinary mechanisms and choose interventions. Use for troubleshooting, sensory analysis, technique tradeoffs, failure recovery, and explaining why a cooking action works.
license: MIT
---

# Culinary Reasoning

## Core Workflow

1. Restate the observed culinary problem in state terms.
2. Identify likely mechanisms such as heat transfer, evaporation, emulsification, starch gelatinization, protein denaturation, browning, seasoning balance, or hydration.
3. Distinguish reversible problems from irreversible ones.
4. Select the lowest-risk intervention that targets the mechanism.
5. Predict side effects such as dilution, toughness, graininess, sweetness, salt concentration, over-reduction, or texture loss.
6. Give verification cues so the user can tell whether the intervention worked.

## Troubleshooting Pattern

Use this sequence for failed or drifting dishes:

```text
observed state -> likely causes -> mechanism -> intervention -> side effects -> verification cue
```

Include the target state before selecting an intervention, even if the final answer does not use formal headings. Avoid generic fixes when mechanism matters. For example, thin gravy might require reduction, more gelatinized starch, more roux, better emulsion, or simply time.

Do not stack multiple strong adjustments at once unless the user is intentionally reformulating the dish. Prefer a staged first move, then explain how to verify and what to change next if the cue is not met.

## Output Contract

- Observed state
- Target state
- Likely causes ranked by fit
- Recommended intervention
- Staged adjustment path when more than one fix is plausible
- Side effects and risks
- Verification cues
- When to stop or discard if recovery is not reasonable

## References

- Read `references/culinary-reasoning-checklist.md` when diagnosing a dish or explaining a culinary mechanism.

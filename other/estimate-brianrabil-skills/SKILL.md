---
name: plan-mode-estimate
description: Size the work and name the unknowns. Use when a plan needs a size, a date, or a confidence level before resources are committed.
license: MIT
---

# Estimate

An estimate that hides its unknowns is a guess with extra steps. Size the work and separate what is known from what is not.

1. Break the work into the smallest pieces that can be sized independently. A piece that cannot be sized is a piece that is not understood.
2. For each piece, give a size and the basis for it: comparable past work, a known quantity, or a named unknown. Distinguish a measured estimate from a guess.
3. Sum the pieces and state the total with its confidence. A range with a reason is more useful than a false point.
4. Name the unknowns that would most change the estimate, and the cheapest way to resolve each. An estimate without its unknowns is not an estimate.

An estimate is a planning input, not a commitment. It does not authorize starting work or promising a date.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.

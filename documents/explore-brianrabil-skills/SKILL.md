---
name: plan-mode-explore
description: Explore possible approaches before choosing one. Use when the user wants paths, feasibility, tradeoffs, or a quick map of unfamiliar terrain.
license: MIT
---

# Explore

Map the viable paths far enough to reveal the decision, then stop.

1. State the decision and known constraints. Inspect relevant local interfaces, documentation, and examples; verify current external facts that affect feasibility.
2. Identify distinct approaches, including the simplest viable one. Check each decisive dependency or limitation. Drop options that fail a stated constraint.
3. Compare remaining approaches on the tradeoffs the user will actually feel: setup, capability, ongoing work, reversibility, and fit with existing tools. Mark evidence, inference, and unknowns separately.
4. Give a compact option map and recommend the next probe or choice. The exploration is complete when the user can choose a path or knows exactly which fact must be checked next.

Stay read-only unless the user separately asks for a prototype or implementation. Use `plan-mode-research` when the main need is a sourced answer to one question; use `plan-mode-deep-research` when the decision requires broad, conflicting evidence.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.

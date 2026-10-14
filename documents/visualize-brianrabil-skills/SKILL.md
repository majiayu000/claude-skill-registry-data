---
name: plan-mode-visualize
description: Visualize relationships, sequences, comparisons, or quantities to make an idea easier to understand. Use when the user asks for a diagram or when a visual would clarify a complex explanation or decision.
license: MIT
---

# Visualize

Choose a visual form that exposes the structure of the question.

1. Identify what the visual must show: relationships, order, branching choices, comparisons, or measured values. Confirm the labels and numbers against the supplied material or a verified source; mark unknowns rather than filling them in.
2. Choose the smallest fitting form: a diagram for relationships, timeline for sequence, decision tree for branches, table for comparisons, or chart for quantities. Use an inline Mermaid diagram when it fits a compact technical structure.
3. Label the parts so the visual stands alone. Keep scale and direction honest; do not imply precision or causation that the evidence does not support.
4. Follow the visual with one sentence stating the main pattern and any consequential limitation. If the user needs a shareable or publication-ready figure, create an appropriate standalone artifact.

Finish when the visual accurately maps every essential element and makes the requested relationship easier to see than prose alone.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.

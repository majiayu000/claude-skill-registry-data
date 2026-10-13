---
name: abd-design
description: "ABD Design agent: produces architecture diagrams, component breakdowns, data flow, and design decisions from the current plan."
effort: high
allowed-tools: Read, Write, Glob, Grep
---

# ABD — Design

Adopt the **Design** role in the Agent-Based Development workflow.

Read the shared references before acting: [envelope and artifact rules](../../shared/envelope.md), [Git rules](../../shared/git-rules.md), [MVP gate](../../shared/mvp-gate.md).

**If `handoffs/` does not exist**, stop and tell the user to run the Planning skill (`abd-plan`) first — see [project-start.md](../../shared/project-start.md).

**Instructions:**

1. Use Read to read the current plan from `handoffs/plans/`.
2. Produce architecture diagrams (as Mermaid or text), component breakdowns, data flow, and design decisions.
3. Use Write to create a design artifact in `handoffs/designs/` following the envelope schema.

Follow the output format in [envelope.md](../../shared/envelope.md) when reporting.

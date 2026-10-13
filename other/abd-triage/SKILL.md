---
name: abd-triage
description: "ABD Planning Triage agent: reviews open critical/severe/moderate findings and creates rework assignments or marks them resolved."
allowed-tools: Read, Write, Glob, Grep
---

# ABD — Planning Triage

Adopt the **Planning Triage** role in the Agent-Based Development workflow.

Read the shared references before acting: [envelope and artifact rules](../../shared/envelope.md), [Git rules](../../shared/git-rules.md), [MVP gate](../../shared/mvp-gate.md).

**If `handoffs/` does not exist**, stop and tell the user to run the Planning skill (`abd-plan`) first — see [project-start.md](../../shared/project-start.md).

**Instructions:**

1. Use Glob and Read to find all open findings in `handoffs/reviews/` with severity critical, severe, or moderate.
2. Create rework assignments or mark resolved.
3. Use Write to update `handoffs/plans/` following the envelope schema.

Follow the output format in [envelope.md](../../shared/envelope.md) when reporting.

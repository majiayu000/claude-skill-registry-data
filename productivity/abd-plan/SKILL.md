---
name: abd-plan
description: "ABD Planning agent: bootstraps projects, assigns tasks to agents, and updates plan artifacts. Run /abd-triage to triage review findings."
effort: high
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# ABD — Planning

Adopt the **Planning** role in the Agent-Based Development workflow.

Read the shared references before acting: [envelope and artifact rules](../../shared/envelope.md), [Git rules](../../shared/git-rules.md), [MVP gate](../../shared/mvp-gate.md).

**If `handoffs/` does not exist** in the current working directory, this is project start: follow [project-start.md](../../shared/project-start.md).

**If `handoffs/` exists:**

1. Use Glob to read `handoffs/reviews/` for open findings. Triage critical/severe/moderate findings.
2. Use Write to create or update plan artifacts in `handoffs/plans/` following the envelope schema.
3. Update `docs/ToDo.md`.

Follow the output format in [envelope.md](../../shared/envelope.md) when reporting.

---
name: abd-review
description: "ABD Tech Review agent: reviews code quality, architecture, naming, and error handling; writes severity-graded review artifacts."
allowed-tools: Read, Write, Glob, Grep
---

# ABD — Tech Review

Adopt the **Tech Review** role in the Agent-Based Development workflow.

Read the shared references before acting: [envelope and artifact rules](../../shared/envelope.md), [Git rules](../../shared/git-rules.md), [MVP gate](../../shared/mvp-gate.md).

**If `handoffs/` does not exist**, stop and tell the user to run the Planning skill (`abd-plan`) first — see [project-start.md](../../shared/project-start.md).

**Instructions:**

1. Use Glob and Read to read code and `handoffs/dev/` artifacts.
2. Review code quality, architecture, naming conventions, error handling, placeholder-free code, schema validation usage.
3. Use Write to create a review artifact in `handoffs/reviews/` with severity-graded findings (`critical | severe | moderate | low | info`) following the envelope schema.

Follow the output format in [envelope.md](../../shared/envelope.md) when reporting.

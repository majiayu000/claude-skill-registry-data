---
name: abd-docs
description: "ABD Documentation agent: updates README, ToDo, assumptions, and changelogs from all handoff artifacts and the codebase."
allowed-tools: Read, Write, Edit, Glob, Grep
---

# ABD — Documentation

Adopt the **Documentation** role in the Agent-Based Development workflow.

Read the shared references before acting: [envelope and artifact rules](../../shared/envelope.md), [Git rules](../../shared/git-rules.md), [MVP gate](../../shared/mvp-gate.md).

**If `handoffs/` does not exist**, stop and tell the user to run the Planning skill (`abd-plan`) first — see [project-start.md](../../shared/project-start.md).

**Instructions:**

1. Use Glob and Read to read all handoffs and the codebase.
2. Use Edit and Write to update `README.md`, `docs/ToDo.md`, `docs/assumptions.md`.
3. On release, use Write to create `docs/CHANGELOG.md` or `docs/changelogs/<version>.md`.

Follow the output format in [envelope.md](../../shared/envelope.md) when reporting.

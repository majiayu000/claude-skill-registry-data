---
name: planning
description: Plan a repository change and save the decision outside Git.
---

# Planning

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/planning/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Use when a task needs a plan. Scale detail to uncertainty and impact; no fixed headings, tables,
diagram, independent reviewer, or separate issue are required by this skill.

1. State the desired outcome and compare no change, reuse, and alternative approaches. Choose the
   smallest durable option; ask before treating an unresolved product choice as settled.
2. Read applicable instructions, documentation, current code, tests, and recent changes from a
   fresh base. Record which evidence supports each proposed path.
3. Map affected owners, contracts, operational boundaries, and tests. Use independent review or
   exploration when the change is cross-cutting or uncertain and local policy calls for it.
4. Record the chosen approach, steps, validation, and unresolved decisions. Mark which steps run
   concurrently and name the dependency that serializes each remaining step. Add rollout details
   only when an established deployment contract requires them.
5. Save the plan once outside Git: an existing issue, a PR description, or a durable native plan
   file outside the repository. Do not commit task plans or count temporary scratch files as saved
   plans. If no durable record is available, use an issue through the local issue workflow. Link
   the record from the handoff instead of duplicating it. When creating a plan issue from a source issue
   that already has a milestone or project, apply that same existing milestone or project through
   [github-issue](../github-issue/SKILL.md).

For cross-cutting changes, read [impact discovery](references/impact-discovery.md) before selecting
tests or concluding that a surface has no dependents.

Consumer wrapper owns: durable plan storage, repository, taxonomy, discovery tools, and approval.

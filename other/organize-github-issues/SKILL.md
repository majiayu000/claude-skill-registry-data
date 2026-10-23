---
name: organize-github-issues
description: Apply existing issue and PR taxonomy within the requested scope.
---

# Organize GitHub issues

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/organize-github-issues/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Use for issue hygiene, priority normalization, milestone assignment, and project membership. Read
local `AGENTS.md`, and live taxonomy guidance before acting.

1. Confirm repository identity. Fetch live labels, milestone descriptions, open project
   descriptions, and the in-scope issue or pull-request evidence. Before a mutation, apply the
   operation-specific gate from [github-issue](../github-issue/SKILL.md). Pull-request metadata
   does not require issues to be enabled.
2. Classify from the permitted metadata and discussion. Do not guess from the implementation. Keep
   automation, ownership, and provenance labels unless local policy explicitly allows a change.
3. Apply only existing labels, milestones, and projects without requesting separate label approval.
   Follow [github-issue](../github-issue/SKILL.md) for single-project membership, auto-added
   sub-issues, and a status that closes the issue. Do not create taxonomy, close work, rewrite
   bodies, or change titles unless the caller separately authorizes that scope.
4. In review mode, report the exact proposed metadata changes and do not mutate. In apply mode,
   make only necessary, idempotent updates.
5. Refetch every touched item. Verify the requested metadata, including project membership, and
   confirm protected metadata stayed intact. After a project add, report any additional item the
   project's automation pulled in, such as a parent issue's sub-issues. Report changed, unchanged,
   and ambiguous items separately.

Consumer wrapper owns: priorities, labels, milestones, projects, clarification policy, default
scope, and permissions.

---
name: agnos-meta-docs-sync
description: "AGNOS maintainer skill. Updates CHANGELOG.md, AGENTS.md, CLAUDE.md and the user's guide AGNOS-GETTING-STARTED.md, agnos-init's template, from what changed in the repository since each of them was last changed. USE FOR: before a release, or after a series of tasks, when the entry-point documents may have drifted. Edits the four files only and never commits: the maintainer reviews and commits."
argument-hint: "(no arguments)"
---

<!-- FTR-DOC-001; RQ-DOC-003 -->
# AGNOS Documentation Sync (Claude Code entry point)

This is a thin pointer, kept in sync with the canonical procedure so the process has a single source of truth. Read and
follow the full procedure (the report script, the rules for each of the four documents) at:

`.github/skills/agnos-meta-docs-sync/SKILL.md`

The sub-agent `agnos-meta-docs-sync` (defined in `.github/agents/agnos-meta-docs-sync.agent.md`, Haiku model) runs it for you.

Do not duplicate that procedure here; if it and this file ever disagree, the `.github` version is authoritative.

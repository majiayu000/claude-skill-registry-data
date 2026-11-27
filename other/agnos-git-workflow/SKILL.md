---
name: agnos-git-workflow
description: "AGNOS process GIT workflow skill. Handles all git operations mandated by the AGNOS process: 'start-session' creates and checks out a feature branch; 'commit-task' stages and commits changes with the correct AGNOS message format. USE FOR: START SESSION branch creation and DoD commit step. Validates all artifact IDs before executing any git command."
argument-hint: "start-session <TRI> | commit-task <TASK-ID> [<ADR-ID>] <description>"
---

# AGNOS Git Workflow (Claude Code entry point)

This is a thin pointer, kept in sync with the canonical procedure so the AGNOS process has a
single source of truth. Read and follow the full procedure — sub-commands
`start-session <TRI>` and `commit-task <TASK-ID> [<ADR-ID>] <description>`, ID validation, and
platform-aware script dispatch — at:

`.github/skills/agnos-git-workflow/SKILL.md`

Do not duplicate that procedure here; if it and this file ever disagree, the `.github` version is
authoritative.

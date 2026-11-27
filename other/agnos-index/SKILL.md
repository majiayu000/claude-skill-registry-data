---
name: agnos-index
description: "AGNOS process index skill. Regenerates agnos-process/process.idx.md, the machine-oriented index (ID, line range, status, title) of every FTR/RQ/ADR/DEC/PLAN/TASK definition in agnos-process/. USE FOR: START SESSION step 4 (before scanning agnos-process/) and commit-task (before staging). The index SHALL NEVER be edited by hand."
argument-hint: "(no arguments)"
---

<!-- RQ-IDX-010 / ADR-IDX-001 -->
# AGNOS Index (Claude Code entry point)

This is a thin pointer, kept in sync with the canonical procedure so the AGNOS process has a
single source of truth. Read and follow the full procedure (platform-aware script dispatch, exit
codes, index reading rules) at:

`.github/skills/agnos-index/SKILL.md`

Do not duplicate that procedure here; if it and this file ever disagree, the `.github` version is
authoritative.

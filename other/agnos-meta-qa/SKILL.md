---
name: agnos-meta-qa
description: "AGNOS maintainer skill. Writes a code quality report on this repository's Python and JavaScript, as JSON for an AI or a tool to correct from, using pinned ruff, complexipy and ESLint with SonarJS rules. USE FOR: an explicit request from a human or an instruction, typically before a commit or a push, to avoid corrections in the pull request. It runs on an explicit request only, never blocks anything and never changes the code."
argument-hint: "setup | check [--all] [<path>...] [--out <file>]"
---

<!-- FTR-QLT-001; RQ-QLT-008 -->
# AGNOS Code Quality Report (Claude Code entry point)

This is a thin pointer, kept in sync with the canonical procedure so the process has a single source of truth. Read and
follow the full procedure (the sub-commands, the report's schema, the exceptions) at:

`.github/skills/agnos-meta-qa/SKILL.md`

Do not duplicate that procedure here; if it and this file ever disagree, the `.github` version is authoritative.

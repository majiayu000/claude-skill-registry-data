---
name: agnos-init
description: "AGNOS process initialisation skill. Adds AGNOS to a project by completing its CLAUDE.md and AGENTS.md with one delimited block and creating its agnos-process/ folders, without touching what the developer wrote. USE FOR: adding AGNOS to a new or existing repository, updating the block after AGNOS changes, or whenever agnos-index reports that agnos-process/ is missing."
argument-hint: "<project folder>"
---

<!-- RQ-INI-009 / ADR-INI-001 -->
# AGNOS Init (Claude Code entry point)

This is a thin pointer, kept in sync with the canonical procedure so the AGNOS process has a
single source of truth. Read and follow the full procedure at:

`.github/skills/agnos-init/SKILL.md`

Do not duplicate that procedure here; if it and this file ever disagree, the `.github` version is
authoritative.

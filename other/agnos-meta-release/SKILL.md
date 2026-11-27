---
name: agnos-meta-release
description: "AGNOS maintainer skill. Rehearses a release of this repository in a folder: selects the delivered layers of a commit, writes them as a marketplace holding the plugin agnos, removes the IDs of AGNOS's own development, checks none is left, and proves on the demo that the output behaves as the repository does. USE FOR: checking what a release would hold before deciding to publish. It publishes nothing: no commit on main, no tag, no push."
argument-hint: "--dry-run --output <folder> [--demo <folder>] [--repo <folder>]"
---

<!-- FTR-MTA-002; RQ-MTA-013 -->
# AGNOS Release Rehearsal (Claude Code entry point)

This is a thin pointer, kept in sync with the canonical procedure so the process has a single source of truth. Read and
follow the full procedure (the command, the checks, the report) at:

`.github/skills/agnos-meta-release/SKILL.md`

Do not duplicate that procedure here; if it and this file ever disagree, the `.github` version is authoritative.

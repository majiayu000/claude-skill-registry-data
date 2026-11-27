---
name: agnos-meta-demo
description: "AGNOS maintainer skill. Builds, rebuilds and verifies agnos-lightweight-process.demo, the simulated two-month demonstration project that shows the AGNOS process applied by a team and serves as the reference to demonstrate and test AGNOS. USE FOR: refreshing the demo after AGNOS evolves, checking it against its requirements, extending its scenario."
argument-hint: "build [--verify] | verify"
---

<!-- RQ-DMO-020 / ADR-DMO-001 (DEC-DMO-006) -->
# AGNOS Demo (Claude Code entry point)

This is a thin pointer, kept in sync with the canonical procedure so the AGNOS process has a single
source of truth. Read and follow the full procedure (sub-commands `build` and `verify`, layout, evolution
steps) at:

`.github/skills/agnos-meta-demo/SKILL.md`

Do not duplicate that procedure here; if it and this file ever disagree, the `.github` version is
authoritative.

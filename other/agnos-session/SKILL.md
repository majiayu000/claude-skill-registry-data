---
name: agnos-session
description: "AGNOS process session-state skill. A script writes agnos-process/_sessionstate/session.yaml (trigram, tests, platform), prints it, and appends the session's friction-metrics row to METRICS_LOG.md, so that the agent never writes these files itself. USE FOR: START SESSION step 3 ('init'), reloading the session variables before a Tier M or L task ('show'), END SESSION step 2 ('close')."
argument-hint: "init --tri <TRI> --tests <true|false> | show | close <questions> <recoveries> <re-tiered> <verification>"
---

<!-- RQ-INI-018 / ADR-INI-002 -->
# AGNOS Session (Claude Code entry point)

This is a thin pointer, kept in sync with the canonical procedure so the AGNOS process has a
single source of truth. Read and follow the full procedure at:

`.github/skills/agnos-session/SKILL.md`

Do not duplicate that procedure here; if it and this file ever disagree, the `.github` version is
authoritative.

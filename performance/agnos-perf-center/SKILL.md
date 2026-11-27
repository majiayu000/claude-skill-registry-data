---
name: agnos-perf-center
description: "AGNOS performance center: monitors how the process runs on a project (not code speed). From agnos-graph's state graph, built if absent, writes an HTML page and its data: coverage, quality score, findings. USE FOR: checking MANDATORY TRACEABILITY at session end or before a release; what cites a requirement; with --call-graph, its functions; with --history, who changed what and what was delivered."
argument-hint: "--process <dir> [--sources <dir>...] [--graph <file>] [--rebuild] [--out <file>] [--ext <.x>...] [--exclude <pattern>...] [--title <t>] [--generated-at <t>] [--call-graph] [--history [--history-since <date|duration>] [--history-depth <n>]]"
---

# AGNOS Performance Center (Claude Code entry point)

<!-- RQ-TRC-017, DEC-TRC-008 -->

This is a thin pointer, kept in sync with the canonical procedure so the process has a single source of truth. Read and
follow the procedure (command, parameters, exit codes, where to find the rest) at:

`.github/skills/agnos-perf-center/SKILL.md`

Do not duplicate that procedure here; if it and this file ever disagree, the `.github` version is authoritative.

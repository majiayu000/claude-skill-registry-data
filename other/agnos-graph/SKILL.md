---
name: agnos-graph
description: "AGNOS project state graph: from the process index and the source folders, writes one dated JSON file of the project's state at a commit: the artifacts, their links with proofs, the IDs the sources cite, task tiers; on request the call graph and the history. Holds no score. USE FOR: giving a tool or agent the project's state; rebuilding the graph agnos-perf-center reads."
argument-hint: "--process <dir> --sources <dir> [--sources <dir>...] [--out <file>] [--ext <.x>...] [--exclude <pattern>...] [--generated-at <t>] [--call-graph] [--history [--history-since <date|duration>] [--history-depth <n>]]"
---

# AGNOS Graph (Claude Code entry point)

<!-- RQ-TRC-133, DEC-TRC-077 -->

This is a thin pointer, kept in sync with the canonical procedure so the process has a single source of truth. Read and
follow the procedure (command, parameters, exit codes, where to find the rest) at:

`.github/skills/agnos-graph/SKILL.md`

Do not duplicate that procedure here; if it and this file ever disagree, the `.github` version is authoritative.

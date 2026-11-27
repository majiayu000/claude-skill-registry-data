---
name: agnos-meta-release-prep
description: "AGNOS maintainer skill. Prepares a release of this repository before agnos-meta-release: checks the working tree and the index, syncs the documents with agnos-meta-docs-sync, shows the diff, the changelog's unreleased entries and a proposed SemVer 2.0.0 version, records the version the maintainer approves and commits it, then states the steps left. USE FOR: before rehearsing a release to publish. It publishes nothing: no merge, no tag, no push."
argument-hint: "(no arguments)"
---

<!-- FTR-PLG-005; RQ-PLG-030 / ADR-PLG-005 (DEC-PLG-022) -->
# AGNOS Release Preparation (Claude Code entry point)

This is a thin pointer, kept in sync with the canonical procedure so the process has a single source of truth. Read and
follow the full procedure (the script's three commands, the docs-sync sub-agent, the approval, the commit, the next steps) at:

`.github/skills/agnos-meta-release-prep/SKILL.md`

Do not duplicate that procedure here; if it and this file ever disagree, the `.github` version is authoritative.

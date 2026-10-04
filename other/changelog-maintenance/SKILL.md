---
name: changelog-maintenance
description: Maintain changelogs for software, skillsets, libraries, and documentation projects. Use when Codex is asked to update CHANGELOG.md, normalize entries, add unreleased changes, prepare a version section, or keep release history consistent.
license: MIT
---

# Changelog Maintenance

## Core Workflow

1. Identify the changelog format, current version, target version, and source of
   changes.
2. Preserve existing structure and style unless the user asks for a migration.
3. Add concise entries under stable categories such as Added, Changed, Fixed,
   Deprecated, Removed, Security, and Docs.
4. Move completed Unreleased entries into a version section when preparing a
   release.
5. Keep issue, PR, and commit references only when they are useful and accurate.
6. Note breaking changes and migration requirements prominently.

## Safety Rules

- Do not invent change history, issue numbers, contributors, dates, or fixes.
- Do not rewrite historical entries unless asked.
- Do not hide breaking changes or security-relevant notes.

## Deliverable Shape

For changelog work, provide:

- Changelog section changed
- Entries added or moved
- Version/date assumptions
- Breaking or migration notes
- Source changes used
- Validation or review notes

## References

- Read `references/changelog-maintenance-checklist.md` when updating or
  reviewing changelogs.

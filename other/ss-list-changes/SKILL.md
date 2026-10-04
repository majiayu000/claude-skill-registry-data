---
name: ss-list-changes
description: Lists active OpenSpec changes and recent archived entries in the current repository. Use this skill to get a quick inventory of in-flight delta specs and what has already been merged, without manually browsing the openspec/ directory.
---

# List OpenSpec Changes

Give a compact inventory of what is currently in flight and what was recently archived
under `openspec/changes/`. This skill is read-only: it never edits files.

## Inputs

Optional: how many archived entries to show (default 10).

## Process

1. Check that `openspec/changes/` exists. If it does not, report that this repository has
   no OpenSpec baseline yet and suggest running the `ss-write-spec` or `ss-reverse-spec`
   skill to create one.
2. **Active changes** — for every directory directly under `openspec/changes/` (excluding
   `archive/`):
   - note whether it contains a `proposal.md` and delta spec files
   - list the capabilities its delta specs touch, cross-referenced against
     `openspec/specs/*/spec.md`
3. **Archived changes** — list the most recent entries under `openspec/changes/archive/`,
   newest first, capped at the requested count (default 10). For each, show the archive
   date, change id, and touched capabilities.

## Output

Present the result as a compact table:

| Status | Change | Capabilities | Files |
|--------|--------|--------------|-------|
| active / archived | change-id | cap-a, cap-b | proposal.md, specs/... |

Do not edit any files.

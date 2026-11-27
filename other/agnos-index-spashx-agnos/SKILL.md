---
name: agnos-index
description: "AGNOS process index skill. Regenerates agnos-process/process.idx.md, the machine-oriented index (ID, line range, status, title) of every FTR/RQ/ADR/DEC/PLAN/TASK definition in agnos-process/. USE FOR: START SESSION step 4 (before scanning agnos-process/) and commit-task (before staging). The index SHALL NEVER be edited by hand."
argument-hint: "(no arguments)"
---

<!-- RQ-IDX-010, RQ-IDX-011, RQ-IDX-013, RQ-IDX-018 / ADR-IDX-001 (DEC-IDX-001, DEC-IDX-003, DEC-IDX-004) -->
# AGNOS Index

`<skill-folder>` is the folder holding this file. <!-- RQ-PLG-005 -->

## Procedure

1. From the project's root, run the script matching `session.platform` (read
   `agnos-process/_sessionstate/session.yaml` first if not already in context):

   | `session.platform` | Command |
   |---|---|
   | `windows` | `powershell -NoProfile -File <skill-folder>/scripts/build-index.ps1` |
   | `linux` / `macos` | `bash <skill-folder>/scripts/build-index.sh` |

2. Check the exit code:
   - `0`: done. The single output line gives the entry and document counts, then the
     time the run took (`agnos-index: <n> entries, <n> documents, <index> <updated|unchanged> in <s.mmm> s`);
     the duration is never written into the index <!-- RQ-IDX-018 -->.
   - `2`: duplicate IDs, listed on the error stream. The index is written; report the duplicates
     to the user (MANDATORY UNIQUE IDENTIFIERS).
   - `1`: error, nothing written. Apply the Error Recovery Protocol.

## Reading the index

- `@<path>` opens a document; each following row is `ID|first-last|status|title`.
- `#next` gives the next free ID of each `<TYPE>-<TRI>` prefix.
- Read an artifact by its line range only; open a whole document only when needed.
- After editing a document in-session, its line numbers after the edit shift: locate an ID by
  searching its heading in that document, or re-run this skill.

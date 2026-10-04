---
name: task-hygiene
type: Skill
title: "task-hygiene — cleanup and triage of the repo task system"
description: "Cleanup and triage of the task ledgers FOUND_DEFECTS.md, CURRENT_ERRORS.md, .matrx/AGENT_TASKS.md, .matrx/ARMAN_TASKS.md. Use when invoked as /task-hygiene <step>, cleaning up tasks, defects, or errors, triaging an error dump, promoting defects, or bootstrapping these files."
tags: [tasks, defects, errors, triage, hygiene, ledgers]
timestamp: 2026-09-10T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/task-hygiene/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# Task Hygiene

Maintenance of the four-file task system in every repo. Run the full sequence or exactly one
step; steps are independent, never assume an earlier one ran.

## Invocation

`/task-hygiene` (all steps, 0–7) or `/task-hygiene <n|name>` (that step, after step 0).

| # | Name | One-liner |
|---|------|-----------|
| 0 | `bootstrap` | Verify/create the four files; always runs first |
| 1 | `cleanup` | Move clearly-done items to condensed completed entries |
| 2 | `dedupe` | Merge duplicates, same-root-cause pairs, defect↔task overlaps |
| 3 | `promote` | Propose ≤3 defect→task promotions to Arman at a time |
| 4 | `analyze` | Full code analysis of named items; stamp the entries |
| 5 | `enrich` | Add concise pointers that make tasks easier to execute later |
| 6 | `docs` | Fix documentation the above revealed as stale |
| 7 | `excavate` | Hunt buried work items in docs; file the orphans |

## The four files

Adapt to where a repo keeps them; never force moves.

| File | Role |
|------|------|
| `FOUND_DEFECTS.md` (root) | **Holding area.** Unapproved discoveries with evidence. NOT a worklist. |
| `CURRENT_ERRORS.md` (root) | **Error-dump inbox.** Arman pastes raw logs; every line gets a home. **Not in aidream** — run [aidream-error-systems.md](aidream-error-systems.md) there instead. |
| `.matrx/AGENT_TASKS.md` | **The only approved worklist.** |
| `.matrx/ARMAN_TASKS.md` | Steps only Arman can perform. A decision is not a row here: it goes through [ask-arman](/skills/ask-arman/SKILL.md). |

Never read, write, or list any `.arman/` directory. Never edit docs under any `official/`
directory — file the correction instead. The repo's own CLAUDE.md wins on conflict.

## Conventions

- **Dates:** absolute `YYYY-MM-DD` on every entry.
- **Defect IDs:** the ledger's real scheme, claimed from the maximum —
  [defect ownership § Entry IDs](/policies/reality-is-the-referee.md). Only open entries carry an ID,
  and every open entry sits under `## OPEN`.
- **Admission test for a friction entry:** reproducible on a fresh checkout AND fixable in the
  repo. Never file your own sandbox or permission errors, shell mistakes, transient flakes,
  local corrupted state, third-party limits with no workaround, or secrets.
- **Priority:** `P0` breaks users/data now · `P1` this week · `P2` can wait · `P3` polish.
- **Defect statuses:** `open` / `needs-hw-verification` / `blocked-external` / `rejected`.
- **Analysis stamp**, exactly one per entry: `Unverified — from docs/logs only` (the default) or
  `Analyzed <date> — verified in code: <finding>`. A task from an unanalyzed defect says "code
  analysis pending".

## Lifecycle

- **Fixed while in holding:** delete the defect entry at once and add
  `- [x] <what> — fixes {ID} (<date>, commit)` to AGENT_TASKS Completed.
- **Completed items** condense to one line; detail lives in git. Compress anything done more
  than ~2 weeks ago.
- **Rejected registry** at the bottom of FOUND_DEFECTS:
  `- {ID} — <reason> — <date> — delete when: <condition>`. Check it before re-filing; step 1
  deletes lines whose condition has happened.
- **Cross-repo routing:** a defect belonging to another local repo is filed in that repo's own
  files, noting who found it. Repo absent → file locally as `blocked-external`.
- **Headless runs:** step 3 needs Arman live. Otherwise write the prepared batch into
  `## Pending Arman review` in FOUND_DEFECTS. Never stall, never self-approve.

## Step 0 — Bootstrap

Check the four files exist; create any missing one from [templates.md](templates.md) (never
`CURRENT_ERRORS.md` in aidream). No Task Tracking section in the repo CLAUDE.md → add a brief one.
Equivalent files under other names → use them, update headers, don't relocate.

## Step 1 — Cleanup

Mechanical only. AGENT_TASKS and ARMAN_TASKS done items → one line in Completed/Done.
FOUND_DEFECTS `fixed` entries → fixed-while-in-holding (never record twice). Prune the
Rejected registry.

## Step 2 — Combine

Merge same-problem pairs, one-root-cause symptom groups, and any defect that already exists as
an open task (fold its evidence into the task, delete the defect). CURRENT_ERRORS signatures
duplicating an entry → link by ID. Union evidence, never drop it.

## Step 3 — Promote

Before promoting, record two checks on the entry: **already built?** (search by domain
concept; found → delete with a pointer to the code) and **still real?** (reproduce it;
not reproducible → `needs-hw-verification` or delete with evidence). Present at most 3 to
Arman, each: title · priority · one-paragraph why · defect ID replaced · analysis stamp.
Approved → move to AGENT_TASKS; rejected → a Rejected line. Then the next ≤3.

## Step 4 — Analyze

Read the code; confirm or refute; root cause, blast radius, fix sketch. Update the entry in
place with the stamp and file:line evidence. A wrong claim is corrected or deleted.

## Step 5 — Enrich

Add only what makes execution cheap: exact paths, the pinning test, the related FEATURE.md,
gotchas from sibling tasks. An entry that already suffices gets nothing.

## Step 6 — Docs

Grep for claims touched by recently completed work, verify in code, then fix per the
[docs](/skills/docs/SKILL.md) skill.

## Step 7 — Excavate buried work

1. **Candidates (grep):** filenames `TASK-*`, `*PLAN*`, `*ROADMAP*`, `*HANDOFF*`, `NEXT_*`,
   `KNOWN_*`, `*_INITIATIVE*` in the root and `docs/` (skip `official/`, `.arman/`); content
   `not yet built|not yet wired|planned|follow-up|TODO|deferred`.
2. **Orphan filter (grep):** a candidate whose basename appears in any tracked surface
   (the four files, root CLAUDE.md, `docs/handoffs/`, nearby FEATURE.md) is dropped. Cap ~10,
   oldest first.
3. **Judgment:** one small read-only agent reads each orphan's first ~60 lines: undone work?
   one-line summary? superseded (evidence)?
4. **File:** live work → one FOUND_DEFECTS entry marked "BURIED WORK RESCUED" with the path;
   dead docs → step 6. Never drop a candidate silently.

A repeat run skips anything already filed.

## CURRENT_ERRORS lifecycle (not aidream)

Dumps are batch snapshots: Arman often cannot re-test for hours.

1. Raw exports land at the bottom of **Inbox**.
2. Fingerprint each error (ignore timestamps and frame noise), dedupe against **Unique errors**,
   and give every new signature a home: fix now if quick (tell Arman at once), FOUND_DEFECTS,
   an agent task (step 3), or ARMAN_TASKS.
3. Clear the Inbox after triage.
4. Resolved rows stay until a shipped build confirms (~2 weeks), then go. A returning error gets
   a new row citing the old ID. The file only shrinks.

In aidream, tool-call failures are mostly harness defects (faulty tools, poor instructions) —
codebase improvements, not agent mistakes.

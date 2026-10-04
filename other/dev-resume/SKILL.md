---
name: dev-resume
description: Use only on explicit request to resume or take over work when the next task is undecided. Use mak:dev-kickoff for a decided task, mak:reverse-engineering when project docs are absent, and mak:doc-audit for document-consistency audits.
---

# mak:dev-resume — Work Re-Entry Point

Derives, from what project documents already show, (a) how far work has progressed, (b) problems in that state, (c) one concrete next step — each backed by evidence. Owns the **inbound** side of session handoff: finding out what to do, not doing it.

Report and all user-facing output in the user's conversation language (or the project's documented language policy).

## Write boundary

This skill diagnoses, reports, and routes only — fixes go through the normal flow. Allowed: Read / Grep / Glob, read-only git commands, and reproducing only the verification commands the documents actually claim (§Procedure step 3). Forbidden: creating/modifying/deleting any file and any code change; found defects go on the next-step candidate list.

## When to Use

Resuming in-progress work, or picking up a handed-off session, when the next concrete task itself is undecided.

Route elsewhere:

| Situation | Go to |
| :--- | :--- |
| No project documents at all | `mak:reverse-engineering` |
| Document drift dominates over "what's next" | `mak:doc-audit` |
| The roadmap/phase structure itself is stale | `mak:roadmap-planning` |
| The task is already decided | `mak:dev-kickoff` |

## Scope Rule

Fixed entry points only — inherits `mak:doc-audit` §Scope Rule; never a full codebase scan.

Entry points: the roadmap's SSOT status (located per the `mak:roadmap-planning` save-path priority), design docs (located per the `mak:design-doc-template` save-path rule) — their meta `Status` values and §5.0 `Step → verify` status column, recent commits, uncommitted changes — plus the paths/symbols those documents cite.

## Procedure

1. **Confirm current position** — read the entry points above. The design doc's §5.0 status column is the stated progress: read it first and treat it as a claim, not as truth. Infer position from commits and code only where that column is missing, or where step 3 shows it contradicts the observed state
2. **Collect entry points** — trace cited paths/symbols per §Scope Rule
3. **Verify claims** — reproduce only commands that verify a claim the documents actually make (stated test counts, "clean" lint/build, etc.); read only cited code. No claim → no command
4. **Report diagnosis** — see §Report
5. **Present next steps** — 2–3 candidates, ask the user to choose. If a document already designates a next item, it must be one of the candidates

## Report

Reuse `mak:review-report` grades — 🔴 Critical / 🟡 Warning / 🟢 Pass / 📝 Note — no new grades. Every finding pairs a document's claim with the observed fact. Distinguish "no issue found" from "could not verify".

| Grade | Item | Location | Evidence (claim vs. observed) |
| :--- | :--- | :--- | :--- |

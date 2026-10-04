---
name: doc-audit
description: Use after a slice/phase completes, at a phase transition, or before handing off unfinished work.
---

# Document Audit Guide

Audits **document-to-document consistency** and **whether the code paths/symbols the documents cite still exist**. Other mak stages only diff code against one design doc — nothing checks whether the rest of the documents are still valid.

Report only, in the user's language — **never edit documents**. Fixes go through `mak:doc-editor` or the main thread.

**Delegation** — if the `mak:auditor` agent is in the available agent list, the audit itself may be delegated to it. It loads this skill as a companion, so the assignment does not need to re-transmit §Checklist, §Report, §Scope Rule, or §Non-goals below — it still must carry which §When to Use trigger this audit is running under, the entry points, the derived audit surface, the output language, and the project path. It reports only too; fixes stay with the main thread either way.

---

## When to Use

- Right after a slice/phase completes
- At a phase transition
- Before handing off an unfinished session

**Do not run on every commit** — this targets accumulated drift across documents, not a single change.

Route elsewhere: implementation vs. one design doc → `mak:review-report`; build/lint/tests → `mak:verify-checklist`; whether documented *behavior* matches code → `mak:analyzer`; choosing the next task → `mak:dev-resume`.

## Audit Surface

Audit only what exists; silently skip what doesn't.

| Surface | Where |
| :--- | :--- |
| Design docs (master + sub-docs) | per the `mak:design-doc-template` save-path rule |
| Roadmap | per the `mak:roadmap-planning` save-path priority |
| Permanent doc set | `docs/` |

If `docs/00.INDEX.md` / `docs/CLAUDE.md` exist, they are the SSOT for that set's structure and per-topic ownership — audit against them. If absent, treat `docs/*.md` as plain documents and never invent structure.

## Scope Rule

Fixed entry points — never scan everything, unless the user explicitly requests a full scan.

Resolve cited paths against the project they belong to — a document may legitimately cite a *target* project's file (`docs/CLAUDE.md`, `.claude/CLAUDE.md`) that does not exist in this repository. Treat those as out of scope, not as dangling.

1. Collect entry points — slice IDs / documents / source files or symbols changed or completed this cycle
2. Trace backward — grep each entry point across the audit surface
3. Audit only entry-point documents + grep hits — read nothing else

## Checklist

1. **Back-reference tracking** — grep changed slice IDs/symbols; do referencing documents match the post-change content?
2. **Dangling references** — references to nonexistent symbols, sections, documents, or code paths/identifiers
3. **Mismarked completion** — marked done while residual tasks remain. Includes the design doc's own progress record: a meta `Status: done` over §5.0 rows still sitting at `⬜ todo` / `▶ in progress`, or a roadmap item marked complete while its design doc's §5.0 disagrees. Compare the documents against each other only — whether a `✅ done` row matches the actual code is §Non-goals
4. **Cross-document contradiction** — phase placement/status differs between documents
5. **SSOT inversion** — a derived document contradicts its SSOT (sub-doc vs. master, `docs/` per-topic SSOT)

### Handoff Check

Only at session handoff. Single question: can the next session identify one concrete task to start from the documents alone (yes/no + evidence)? The receiving side of that handoff is `mak:dev-resume`.

### Non-goals

Whether documented behavior/flow matches the code is out of scope — that needs code reading, not comparison (`mak:analyzer`'s job). If a drift signal appears (symbol exists but signature/arity differs from the doc, or cited code changed substantially after the doc's last update), do not judge it here — record it as a 📝 Note recommending `mak:analyzer` re-analysis.

## Report

Reuse `mak:review-report`'s grades: 🔴 Critical / 🟡 Warning / 🟢 Pass / 📝 Note — no new grades. Every finding needs evidence (a grep hit, or two contradicting locations). State the entry points used and the derived audit surface at the top. Distinguish "no issues found" from "could not verify".

| Grade | Item | Location | Evidence | Suggested fix |
| :--- | :--- | :--- | :--- | :--- |

If clean: `✅ No cross-document inconsistencies found`

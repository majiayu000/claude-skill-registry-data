---
name: research-stream-consolidation
description: >-
  Merge overlapping research runs into one project without losing provenance. When two studies cover
  the same topic and their files must move, relocate whole run directories, deduplicate identical
  artifacts and repair manifests, receipts and links bound to old paths. Not for
  contract-bound-deliverables.
metadata:
  revision: "4"
  areas: "work-management"
  targets: "runtime-agnostic"
  summary: "merge overlapping research streams into one project and repair the records that bound the old paths"
  summary_zh: "把重复的研究流并成一个项目，并修好绑定旧路径的记录"
  kind: "entry"
---

# Research stream consolidation

Use when two or more independent research runs cover the same topic (typically the same owner
commissioned them from different agents or models) and they must become one project: merge A
into B, delete A, dedup B, then review the union and evolve the deliverable. This is a
relocation + reconciliation problem, not a copy-paste: research repos bind artifact paths in
manifests, receipts, study-control records and navigation docs.

If the evolved deliverable has a length/format contract, assemble and QA it with the discipline
of `contract-bound-deliverables`; this skill covers the merge and reconciliation around it.

## Procedure

1. **Inventory before moving anything.** List both trees (`find`, `du`), read the target
   project's README/plan for its rules (what may be deleted, what must be kept), and grep the
   whole repo for the source path — study-control records, manifests, READMEs and wiki pages
   bind it. Every hit is a record to update or annotate afterwards.

2. **Relocate the stream as one unit.** `git mv <source-dir> <target-project>/<stream-name>/`
   preserves internal structure, relative paths and receipts; scattering files into the target
   destroys them. Run `git mv` and any `git rm` as separate commands: a compound
   `git mv … && git rm …` exits 1 because rename-staged files need `-f` for removal — check
   `git status`, then re-run the removal alone.

3. **Dedup by content identity — once.** Hash the candidate duplicates in a single pass
   (`sha256sum`), keep one representative, `git rm -f` the rest. One identity pass decides;
   re-hashing to "confirm" the same files later is stalling. Respect the project's keep rules:
   files a plan says to retain (e.g. empty result/error outputs as run evidence) are not dedup
   targets even when byte-identical.

4. **Record the relocation on both sides.** Artifact side: what moved, what was deleted, how to
   recover from git history. Study/control side: a note where the old path was bound, so
   path-bound records stay traceable. Then update navigation docs (README/MATERIALS) and
   re-resolve their links mechanically (parse every link, not just spot-check). Then re-run the
   study's validator and repair path/hash binding drift (repair the path and hash bindings in the study's control records) — a
   relocation note documents the move; it does not fix the bound records.

5. **Re-read moved files before editing them.** After a path move the edit tool requires a
   fresh read at the new path; overwriting from pre-move context fails.

6. **Reconciliation review.** Compare the two streams' item sets — they often barely overlap,
   and that is the merge value. Build a conflict table for claims that differ (same program,
   different status wording) and write the disposition: which stream's wording wins, and why.
   Figures the streams independently rejected stay rejected — independent convergence on a drop
   is corroboration, not a gap to fill.

7. **Evolve the deliverable from the union.** Preserve each claim's original evidence level —
   appearing in two streams does not promote it (a summary-level item does not become
   claim-level by duplication). Put the provenance map (new reference id → source stream/claim),
   conflict dispositions and a not-included log in a sidecar memo, not in the deliverable.
   Re-run the deliverable's own QA script against the union corpus.

## Pitfalls

- Re-verifying after every step (re-hashing, re-checking). Establish integrity once, where it
  decides something (provenance, duplicate detection), then advance — the owner calls repeated
  hash loops out as stalling.
- Resurrecting a figure both streams deliberately dropped.
- Moving files without the study/control-side note — and stopping there: manifests and closeout
  records still point at the old path, and the study validator fails on the broken bindings;
  repair the chain (repair the path and hash bindings in the study's control records), do not just annotate.
- Editing a moved file from a stale (pre-move) read.
- Treating byte-identical files as mergeable content: keep one, delete the rest, and say so in
  the relocation record.

## Supporting files

- `references/reconciliation-formats.md` — conflict-disposition table, provenance map and
  not-included log formats for the sidecar memo.

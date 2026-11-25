---
name: review-consolidate
description: >
  Run repository/lens reviews in separate processes, then consolidate validated,
  scope-aware full reports. Focused verifications and legacy reports remain history
  and cannot replace full-review status.
argument-hint: "<repo> [<repo>...] --out <file.md> [--lenses a,b,c] [--no-run] [--all]"
---

# review-consolidate

Read `docs/report-contract.md` from the extension directory. Consolidation arranges
existing evidence; it does not review source, invent findings, or reclassify severity.
No subagents. Parallelism is the existing matrix launcher.

## 0 — Arguments

Require at least one repo and `--out`; never default either. Resolve paths to
absolute and permit a directory prefix only when exactly one repo matches.
`--lenses` limits the matrix, `--no-run` reads existing artifacts, and `--all`
includes historical full snapshots in an appendix, **not** a union of old and
current defect counts. Stop with usage when arguments are missing/ambiguous.

Use a UTC stamp and a sibling `<out-directory>/review-matrix-<stamp>.logs` directory.

## 1 — Run once, unless --no-run

```bash
<extension>/bin/run-matrix.sh --log-dir <logdir> [--lenses a,b,c] <repos...>
```

One process per repo/lens, all launched before waiting. Use a generous timeout;
never restart the launcher, spawn subagents, or silently retry failed pairings.
Read `manifest.tsv`: repo, lens, exit, seconds, report, log. The launcher validates
v2 sidecars before accepting a REPORT path; missing/invalid reports are failures.

A failed pairing stays FAILED for this run. Do **not** substitute an older success
and make current coverage appear complete. Historical artifacts may be linked
separately, explicitly dated.

## 2 — Collect by identity, revision, and scope

For successful manifest pairings, use exactly their reported paths and sidecars.
Validate structural/history consistency; do not infer a newer report from mtimes.
For `--no-run` use:

```bash
node <extension>/bin/report-tools.mjs select <absolute-repo> [--all]
```

The selector groups by target/PR, mode, and explicit lens set, then orders parsed
UTC timestamps. It selects only **full v2** reports. Its `ignored` list includes
legacy/focused artifacts and reasons: preserve that list in the output. Do not
let a recent `verification`, a focused `multi`, or a legacy zero-count report
replace a full review. These artifacts remain visible as history without a new
whole-repository/PR approval.

The latest full report already contains its cumulative ledger. A later focused
verification may settle its named issue, but does not silently recalculate that
full report's verdict: list the verification separately, and require a reconciled
full report before presenting a new approval. Do not resurrect old issues by
unioning every historical snapshot's findings.

If parsing/validation fails, record the exact artifact and error as UNPARSEABLE /
INVALID. If there is no full v2 report, record NO VALID FULL REPORT, even if legacy
history exists. Do not claim an empty repository is healthy.

Report: repos, pairings run, full sidecars selected, active confirmed findings,
verification questions, historical/focused artifacts, and failed pairings.

## 3 — Arrange the evidence

1. Keep target, head SHA, mode, scope, and lens identity on every row. Reports of
   different revisions are not equivalent current checks. Flag mixed-head runs;
   never present them as one current-revision certification.
2. Within the same repo/target/head, merge repeated stable IDs/explicit aliases,
   preserving evidence and lenses. If two reports conflict about disposition,
   retain both observations and mark reconciliation required; do not adjudicate.
3. Active means `status: open`, or `not_rechecked` with `prior_status: open`.
   Count VALID separately from AMBIGUOUS. Fixed, disproved, and deferred records
   belong in a disposition section, not the active-defect totals.
4. Never merge findings across repositories. Shared defect classes may receive
   CROSS-REPO labels, but each owner retains its own finding and evidence.
5. Preserve judged severity. Multiple labels/lenses are not independent evidence.

## 4 — Write --out

Create its parent; write only the requested output, not inside reviewed repos
unless that is the explicit output path. Do not modify their source or reports.

Structure:

- Summary: repo/target/revision/scope, confirmed P0–P3, uncertain P0–P3, verdict.
- Coverage: each requested pairing, report date/head, validation status and log.
- Active confirmed findings: severity, then repo, with failure/evidence/fix.
- Verification questions: uncertainty and the exact check needed.
- Finding dispositions: verified fixes, disproofs, deferrals, and unrechecked issues.
- Cross-repository themes, if supported.
- History: focused/legacy reports and optional `--all` snapshots, clearly non-current.
- Not consolidated: failed/missing/invalid reports, conflicting dispositions,
  mixed revisions, and incomplete coverage. Never hide these behind zero counts.

A failed or incomplete pairing prevents an overall healthy/SHIP summary. Do not
rescue an INCOMPLETE report by combining unrelated partial outputs. Read-only
artifact collection is the only work here; no source review or application runs.

## 5 — Summary

Return counts with scope/revision qualifications, pairings run/failed, top five
confirmed findings, outstanding verification questions, and output path.
Last line: `CONSOLIDATED: <absolute-output-path>`.

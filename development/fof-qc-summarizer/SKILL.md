---
name: fof-qc-summarizer
description: Aggregate-only summarizer for K18 QC artifacts; produces summary outputs and appends manifest rows when format is confirmed.
metadata:
  short-description: Aggregate-only QC summarizer for K18 outputs.
---

## How to use

Run from the Fear-of-Falling subproject root or repo root.

Example:

```bash
Rscript .codex/skills/fof-qc-summarizer/scripts/qc_summarize.R
```

Optional overrides:

```bash
Rscript .codex/skills/fof-qc-summarizer/scripts/qc_summarize.R --qc-dir PATH --out-dir PATH --script-label K18_QC_SUMMARY
```

## Inputs

- QC outputs under `Fear-of-Falling/R-scripts/K18/outputs/K18_QC/qc/`.
- Manifest helpers discovered by scanning for `init.R` with `append_manifest()` and `manifest_row()`.
- Policy sources: `Fear-of-Falling/CLAUDE.md`, `Fear-of-Falling/QC_CHECKLIST.md`.

## Outputs

- `Fear-of-Falling/R-scripts/K18/outputs/K18_QC/qc_summary/qc_summary.csv`
- `Fear-of-Falling/R-scripts/K18/outputs/K18_QC/qc_summary/qc_summary.txt`
- One manifest row per new artifact (if manifest format is confirmed).

## Failure modes

- Fear-of-Falling project root not found.
- QC outputs directory missing.
- Manifest helpers missing.
- Manifest header mismatch (fail closed).
- No eligible aggregate QC artifacts to summarize.

## Safety/guardrails

- FAIL CLOSED: if manifest helpers or format are not verifiable, the script exits 1.
- Privacy: skips any file with `ids`, `row_level`, or `participant` in the name or
  an `id`-like column; never writes participant-level rows.
- No external APIs or network calls.
- Does not modify raw data or QC inputs.

Sources: `Fear-of-Falling/CLAUDE.md`, `Fear-of-Falling/QC_CHECKLIST.md`.

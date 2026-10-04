---
name: researchforge-paper
description: Build the research package — BibTeX citations, related work, evidence matrix, paper outline, reproducibility bundle, and experiment data. Use when the user wants publication materials or a research write-up bundle.
---

# Build the research package

```bash
researchforge paper package --json
```

Requires stored papers (run the researchforge-papers skill first). Output
goes to `.researchforge/research-output/` by default; `--output DIR` writes
elsewhere (only with the user's say-so — it creates a directory in their
tree).

The bundle (all generated from recorded data only):

- `citations.bib`, `related_work.md`, `evidence_matrix.csv` — from stored
  papers and the landscape's evidence claims;
- `hypotheses.md`, `paper_outline.md` — the outline marks every section that
  has no recorded data as *to be completed by the author*; leave those
  honest, do not fill them with invented content;
- `methodology.md`, `limitations.md`, `reproducibility.md` — frozen
  contract, environment fingerprint, exact command sequence, patch hashes;
- `experiments/` — `results.csv`, `run_manifest.json`, and
  `rejected_experiments.md` (negative results are part of the record);
- `figures/README.md` — figures are not auto-generated; say so if asked.

When presenting the package, describe what each file contains using the
`--json` file list, and remind the user the outline is a starting point for
*their* paper: the recorded evidence supports it, but the prose and any
novelty claims are theirs to make.

## Rules

- The Python engine is the boundary: never work around a validation error, a
  protected path, or an approval gate — fix the artifact or ask the user.
- Approvals belong to the user: never pass `--yes` or type a confirmation
  unless the user explicitly approved that step in this conversation.
- Ground every summary in stored data: quote only numbers returned by
  `--json` output or files under `.researchforge/` — never invent metrics.

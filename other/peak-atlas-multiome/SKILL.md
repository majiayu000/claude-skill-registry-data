---
name: peak-atlas-multiome
description: "Consensus scATAC peak atlas from true 10x Multiome (paired RNA+ATAC, same cells): peaks per RNA/ATAC/WNN/cell-type grouping, pseudo-replicate reproducibility, four-way vote, then Primary+Rescue quantify-and-prune protecting rare populations. Use when RNA+ATAC are paired. For unpaired data use peak-atlas-unpaired; builds on peak-atlas-framework."
license: MIT
---

# Peak Atlas from True 10x Multiome (paired RNA + ATAC)

## Prerequisites

`peak-atlas-framework` is the required companion skill and holds the shared spine. This child only
specializes which groupings feed the paired-multiome regime; everything generic links up. Jump
directly to:

- `peak-atlas-framework/references/macs3-scatac-params.md` — the MACS3 flags, the 501bp rationale, chromosome/blacklist/N filters
- `peak-atlas-framework/references/iterative-overlap-merge.md` — the summit-faithful merge algorithm
- `peak-atlas-framework/references/support-voting.md` — `n_strategies`, the compute-before-merge rule, the score boost
- `peak-atlas-framework/references/rare-celltype-protection.md` — the adaptive per-cluster threshold, stratified sampling, rescue
- `peak-atlas-framework/references/validation-battery.md` — FRiP / TSS / marker / embedding / chromVAR gates
- `peak-atlas-framework/scripts/` — `iterative_overlap.R`, `support_voting.R`, `normalize_width.R`, `blacklist.R`, `frip.R` (source these; do not re-define)

The pipeline is **CALL → MERGE → FILTER → TIER → VALIDATE**. Read the methodology once in the framework. Below is only what is multiome-specific.

---

## What "paired" buys you

In true 10x Multiome the RNA and ATAC come from the SAME nucleus, so a cell's transcriptional identity and its chromatin both label the same barcode. That lets you discover peaks separately inside each transcriptionally- AND epigenetically-defined population, and treat agreement across modalities as a confidence signal. Unpaired data cannot do this — there RNA identity is *transferred* onto separate ATAC cells, which is why it gets its own child (`peak-atlas-unpaired`).

---

## The four strategies (the multiome-specific CALL groupings)

Peaks are called per cell-group, four times, under four independent groupings of the same cells. Why four: a rare population's accessible regions are easily drowned out when peaks are called on the whole dataset, so each grouping is peak-called separately; and because the four groupings span modalities (RNA, ATAC, joint, expert), agreement across them is the cross-strategy confidence (`n_strategies`).

| Strategy | Grouping column | How it is derived |
|---|---|---|
| RNA | `RNA_clusters` | `FindClusters` on the `RNA_snn` graph (built from `pca` dims `1:30`), `resolution = 0.5` |
| ATAC | `ATAC_clusters` | `FindClusters` on the `ATAC_snn` graph (built from `lsi` dims `2:30`), `resolution = 0.5` |
| WNN | `WNN_clusters` | weighted-nearest-neighbor `wsnn` clustering — needs paired data; reuse an existing `wsnn_res*` column or compute via `FindMultiModalNeighbors` then `FindClusters(graph.name="wsnn")` |
| CellType | expert annotation | the curated `refined_cell_type` (or equivalent) column |

ATAC LSI uses dims `2:30` (not `1:30`) because LSI component 1 typically tracks sequencing depth, not biology — see the `DepthCor` check in re-embedding below. Each strategy is peak-called and merged independently into one GRanges, giving four merged sets that vote.

Deep dive: `references/multiome-strategies.md`.

---

## Per-group calling with pseudo-replicates

Every group is called by `call_peaks_with_pseudoreps` (in `scripts/call_peaks_multistrategy.R`). The order of operations and the guardrails:

1. **Skip small groups.** Need `MIN_CELLS_PER_GROUP * 2 = 100` cells (two pseudo-reps of `MIN_CELLS_PER_GROUP = 50`). A group below this is skipped — too few cells to call reproducibly.
2. **Downsample large groups** to `MAX_CELLS_PER_GROUP = 1000` for speed (peak discovery saturates well before this).
3. **Split 50/50 into two pseudo-replicates** (`split_pseudoreplicates`, random `floor(n/2)` vs the rest).
4. **Fragment floor.** Build a BEDPE pseudobulk per rep; if either rep has `< MIN_FRAGS_PER_PSEUDOREP = 5000` fragments, skip the group.
5. **Call MACS3 independently on each rep** with the scATAC params (`--nomodel --shift -100 --extsize 200 --call-summits --keep-dup all -q 0.01`, `-g mm` / `-f BEDPE`). See `peak-atlas-framework/references/macs3-scatac-params.md`.
6. **Normalize to 501bp** on the summit (`normalize_to_501bp`, framework script).
7. **PRIMARY NOISE FILTER — pseudo-rep reproducibility.** Keep only rep1 peaks that overlap a rep2 peak (`filter_by_pseudoreps`, `min_overlap = 1` bp). Typically retains ~78-86% of rep1 peaks. This — not the MACS q-value — is the real noise filter.

The framework's `-q 0.01` is intentionally permissive precisely because reproducibility, not q-value, gates noise. MACS3 details and the 501bp rationale are in the framework reference, not here.

---

## Cross-strategy reconciliation (MERGE + TIER)

Source the framework scripts (`iterative_overlap.R`, `support_voting.R`) and follow the canonical order. The one rule that matters: **compute `n_strategies` BEFORE the final merge**, or the final merge "bridges" every survivor onto all four strategies and the signal is destroyed.

1. **Merge WITHIN each strategy:** `convergeClusterGRanges(strat_peaks, by = "score")` → one merged GRanges per strategy.
2. **Combine** the four merged sets: `combined <- do.call(c, unname(strategy_merged))`.
3. **Compute support BEFORE the merge:** `calculate_strategy_support(combined, strategy_merged)` sets `n_strategies` (1..4) and a `strategies` label.
4. **Boost the rank key:** `adjusted_score = score * (1 + 0.5*(n_strategies - 1))` (`add_adjusted_score`).
5. **Final merge:** `convergeClusterGRanges(combined, by = "adjusted_score")` — multi-strategy consensus peaks now win ties against single-strategy peaks.

Quality filters (standard-chromosome, chromosome-boundary, blacklist) are applied to the combined set per the framework reference. `scripts/call_peaks_multistrategy.R` wires the whole CALL→MERGE→TIER sequence end to end.

---

## Quantify-then-prune (the FILTER stage)

Do not chase a target peak count; chase FRiP and marker coverage and protect rare types (framework first principle). The candidate atlas (~2.3M peaks here) is pruned against ACTUAL cell-by-peak counts in six phases:

| Phase | What | Detail |
|---|---|---|
| 1 | Metadata pre-filter | keep if `n_strategies >= 2` OR singleton with `score > quantile(score, 0.85)` — cheap, no quantification |
| 2 | Stratified cell sampling | `max(~100, 0.10 * n_type)` cells per type so rare types are not sampled away |
| 3 | Subsampled quantification | `Signac::FeatureMatrix` on the sampled cells x pre-filtered peaks |
| 4 | Primary+Rescue prune | the adaptive per-cell-type filter (below) on the subsampled counts |
| 5 | Full quantification | `FeatureMatrix` over ALL cells x surviving peaks, then a new `ChromatinAssay` |
| 6 | Validation | FRiP retention, rare-marker promoter retention, embedding, chromVAR |

Phases 1-2 are framework methodology — see `peak-atlas-framework/references/rare-celltype-protection.md`. Phase 4 is the part worth detailing here.

### Primary+Rescue — the hybrid adaptive filter

`scripts/apply_primary_rescue_filter.R` (reproduced faithfully from `peak_utils.R::apply_primary_rescue_filter`). A peak survives if it passes EITHER arm:

- **PRIMARY** — per cell-type adaptive threshold `clamp(0.02 * n, 15, 200)` = `max(15, min(0.02*n, 200))`. Count, per cluster, how many of that cluster's cells have the peak accessible; keep the peak if it clears the threshold in ANY ONE cluster. A rare type (HSC, n=147 gives 15 cells = 10.2%) faces a low absolute bar; an abundant type (Neutrophil, n=4500 gives 90 cells = 2.0%) faces a higher relative bar. This is the rare-cell-type protection in action.
- **RESCUE** — keep peaks with `n_strategies == 4` AND global presence `>= 10` cells. This re-adds replicated rare biology that sits right at the per-cluster boundary but is corroborated by every independent grouping.

`final_keep = primary_keep | rescue_keep`. On the source bone-marrow multiome this produced **~544k peaks**, versus **~1.15M** for the simpler global-sparsity path (`peak_presence > 3` in the subsample) — the adaptive filter is meaningfully tighter while protecting rare biology. Full math and rationale: `references/primary-rescue-filter.md`.

---

## Requantify and re-embed (after FILTER)

Build the new assay from the surviving peaks and recompute the chromatin embedding:

1. `FeatureMatrix` over all cells, then `CreateChromatinAssay(counts, fragments, ranges = peaks, annotation = ...)`.
2. `FindTopFeatures(min.cutoff = 5)`, then `RunTFIDF`, then `RunSVD`.
3. **DepthCor check.** If `abs(cor)` of LSI component 1 with depth `> 0.9`, use `lsi_dims = 2:30`; else `1:30`. LSI component 1 is usually a depth artifact, so this guards against embedding on noise.
4. `RunUMAP(reduction = "lsi", dims = lsi_dims)` for an ATAC-only embedding.
5. **Refresh WNN:** `FindMultiModalNeighbors(reduction.list = list("pca","lsi"), dims.list = list(1:30, lsi_dims))`, then `RunUMAP(nn.name = "weighted.nn")`.

Validate per the framework battery: rare-marker promoter-peak retention `>= 0.95` (`checks/check_marker_retention.R`), chromVAR TF activity tracking expected lineage TFs (route to `chromvar-motif-accessibility`), and an embedding comparison across candidate peak sets (the atlas that best resolves known populations wins, even with fewer peaks).

---

## Verification checklist

- [ ] Support distribution is NOT almost-all `n_strategies == 4` (if it is, you computed support after the merge — see pitfalls).
- [ ] Every peak is exactly 501bp and the set is non-overlapping: `Rscript peak-atlas-framework/checks/check_peak_atlas.R atlas.rds`.
- [ ] FRiP retention `>= 0.90`: `Rscript peak-atlas-framework/checks/check_frip_retention.R orig_frip.rds filt_frip.rds`.
- [ ] Rare-marker promoter retention `>= 0.95`: `Rscript checks/check_marker_retention.R orig.rds filt.rds`.
- [ ] DepthCor handled: LSI dims are `2:30` whenever component 1 correlates with depth.

---

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Support distribution is almost entirely `n_strategies == 4` | `calculate_strategy_support` was run AFTER the final merge — overlapping winners bridge all four strategies onto every survivor | Compute support on the per-strategy merged sets BEFORE the final `convergeClusterGRanges` (steps 1-3 above) |
| `WNN_clusters` missing / WNN strategy skipped | WNN clustering needs a `wsnn` graph that only exists for paired data | Reuse an existing `wsnn_res*` column, or run `FindMultiModalNeighbors` then `FindClusters(graph.name = "wsnn")`; never substitute RNA or ATAC clusters for it |
| A rare cell type loses its marker peaks after filtering | A single global sparsity threshold prunes anything rare | Use Primary+Rescue (`apply_primary_rescue_filter`): adaptive per-cluster bar `max(15, min(0.02*n, 200))` plus the 4-strategy rescue |
| All four strategies return identical peaks | The grouping column was not set (`group.by`), so every "group" is the whole dataset | Build and set `RNA_clusters` / `ATAC_clusters` / `WNN_clusters` / cell-type explicitly before calling |
| ATAC UMAP separates by sequencing depth, not biology | Embedded on LSI component 1, which tracks depth | Honor the DepthCor check — drop component 1 (`lsi_dims = 2:30`) when `abs(cor) > 0.9` |
| Pseudo-rep filter keeps near-100% of peaks | Pseudo-reps overlap because cells were not actually split, or `min_overlap` was set too loose | Confirm `split_pseudoreplicates` produced two disjoint cell sets and MACS3 ran independently per rep; ~78-86% retention is expected |

---

## Resources

- Signac (multiome / ChromatinAssay): https://stuartlab.org/signac/
- WNN (Hao et al., Cell 2021): https://doi.org/10.1016/j.cell.2021.04.048
- ArchR / iterative-overlap (Granja et al., Nat Genet 2021): https://www.nature.com/articles/s41588-021-00790-6
- Corces & Granja et al., Science 2018: https://www.science.org/doi/10.1126/science.aav1898
- MACS3: https://macs3-project.github.io/MACS/


---

## When not to use

- Do not use for unpaired RNA+ATAC (separate cell pools). Use peak-atlas-unpaired instead.
- Do not use to learn the shared merge/voting/validation methodology. That lives in peak-atlas-framework.

---

## See also

- `peak-atlas-framework` — Foundation; this child links up to the shared CALL/MERGE/FILTER/TIER/VALIDATE methodology
- `peak-atlas-unpaired` — Sibling (other data regime); unpaired RNA+ATAC (separate pools, transferred identity)
- `signac-chromatin-analysis` — Upstream / downstream; peak quantification, coverage, `CallPeaks`, ChromatinAssay mechanics
- `iterative-peak-merging` — Embedded merge primitive; the bare within-study merge primitive from MACS summit BEDs
- `chromvar-motif-accessibility` — Downstream validation; TF-motif activity validation of the finished atlas

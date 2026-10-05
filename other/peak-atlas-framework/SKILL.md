---
name: peak-atlas-framework
description: "scATAC/multiome consensus peak-set methodology — multi-strategy calling, support voting, iterative-overlap merge, quantify-then-prune, tier, validate — with rare-cell-type protection as a first principle. Use when deciding how to build or evaluate a fixed-width peak set, or choosing strategies, thresholds, and filtration tradeoffs."
license: MIT
---

# Peak Atlas Framework and Router

A peak atlas is the coordinate system every downstream scATAC analysis (counting, chromVAR, peak-to-gene, GRN) inherits. Get it wrong — lose a rare cell type's peaks, or smear summits into midpoints — and no later step can recover the signal. The guiding principle here: **chase FRiP and marker coverage, not a target peak count**, and protect rare cell types by design rather than by luck.

This skill is the **router and shared spine** for the peak-atlas-* family. The two children (`peak-atlas-multiome`, `peak-atlas-unpaired`) elaborate data-regime specifics and the concrete grouping/tier schemes; they link UP into the references and scripts here rather than restating the methodology. Cite the iterative-overlap origin: Corces & Granja et al., Science 2018; ArchR (Granja et al., Nat Genet 2021).

---

## Routing decision tree

```
Building a consensus peak set from single-cell / single-nucleus ATAC?
│
├─ Paired 10x Multiome (RNA + ATAC in the SAME cells)
│     → peak-atlas-multiome   (cross-modal voting across RNA/ATAC/WNN/CellType groupings)
│
├─ Unpaired (separate scRNA and scATAC pools; ATAC identity TRANSFERRED from RNA)
│     → peak-atlas-unpaired   (label-transfer first, then group ATAC by transferred identity)
│
└─ ATAC-only (no RNA at all)
      → DEGRADE GRACEFULLY: use ATAC clusters only, drop cross-modal voting,
        lean on an external consensus atlas where one exists. Stay in this
        framework for the merge/filter/validate spine; skip the RNA strategies.
```

The pipeline is the methodology: **CALL → MERGE → FILTER → TIER → VALIDATE.** Read it once here; the children only specialize WHICH groupings feed each stage.

---

## Stage CALL — pseudobulk peaks per cell-group

Generate a pseudobulk per cell-group, call peaks with scATAC-tuned MACS3, and normalize every peak to a **501bp summit-centered fixed width**. The calling *mechanics* (fragment handling, pseudobulk, MACS3 vs Signac wrappers) live in `snapatac2-atac-preprocessing` / `signac-chromatin-analysis`; the children define WHICH groupings (RNA clusters, ATAC clusters, WNN, cell type) produce the pseudobulks.

The canonical scATAC MACS3 call and the rationale for every flag — `--nomodel --shift -100 --extsize 200` (center on the Tn5 cut site), `--call-summits` (summit for 501bp normalization), `--keep-dup all` (real single-cell signal), `-q 0.01` — are in `references/macs3-scatac-params.md`, alongside the 501bp rationale, standard-chromosome filtering, blacklist removal, the N-content filter, and the Signac `CallPeaks` wrapper variant for unpaired pseudobulk.

Width normalization is `scripts/normalize_width.R` (`normalize_to_501bp`, summit ± `extend`, default `extend=250` → 501bp).

---

## Stage MERGE — iterative-overlap consensus

Resolve overlapping peaks with **iterative-overlap** selection (Corces & Granja 2018 / ArchR): rank peaks by score, keep the best per overlap cluster, remove it and everything it overlaps, repeat until the set is non-overlapping. The result is **summit-faithful** — it keeps the highest-signal *actual* peak per cluster, never an artificial midpoint — and here it is **support-weighted** (the rank key is the support-boosted `adjusted_score`).

Relationship to the sibling primitive: `iterative-peak-merging` is the standalone tool that merges MACS `_summits.bed` files from a within-study design. Here the same algorithm is **embedded** in the consensus pipeline and made **support-aware**. Do not reimplement it in a child — link to `scripts/iterative_overlap.R` (`clusterGRanges`, `convergeClusterGRanges`) and read `references/iterative-overlap-merge.md`. The `createIterativeOverlapPeakSet` SPM/rule variant (defaults `extend=250`, `spm=5`, `rule="2"` meaning `(n+1)/2`) is documented there as an optional reproducibility path.

---

## Stage FILTER — quantify, then prune

State the first principle plainly: **chase FRiP and marker coverage, not a target peak count, and protect rare cell types.** Quantify the candidate atlas against the actual cell-by-peak counts, then prune sparse peaks using an *adaptive per-cluster* threshold so a rare cell type clears a low absolute bar while an abundant type clears a higher relative bar. A peak survives if it clears the bar in ANY one cluster. See `references/rare-celltype-protection.md` for the formula, stratified sampling, the rescue mechanism, and the metadata pre-filter; the helper is `scripts/support_voting.R` plus the filtration config in `assets/peak_filtration_config.yaml`.

---

## Stage TIER — confidence from cross-strategy support

Each peak carries `n_strategies`: how many independent groupings (RNA, ATAC, WNN, cell type) discovered it. This is the cross-strategy confidence signal — peaks found by several independent strategies are more likely to be real. Support boosts the merge rank via `adjusted_score = score * (1 + 0.5*(n_strategies-1))` and gates the pre-filter and rescue. The one rule that matters: **compute support BEFORE the final merge** (after-the-fact computation bridges everything to look fully supported). See `references/support-voting.md`. The children give the concrete tier and filter schemes that key off `n_strategies`.

---

## Stage VALIDATE — does the atlas preserve biology?

A peak set is only as good as the signal it retains. Validate on four axes: **FRiP retention** (≥0.90 of the original per-cell median), **marker / biology recovery** (rare-marker promoter-peak retention ≥0.95), **embedding quality** (recompute LSI/UMAP/WNN per candidate and compare structure), and **external correlation** (chromVAR TF activity, per-lineage promoter accessibility). TSS enrichment is a sanity FLOOR, not a discriminator. Full battery in `references/validation-battery.md`; runnable gates in `checks/check_peak_atlas.R` and `checks/check_frip_retention.R`.

---

## Shared scripts (load on demand)

| Need | Script | Provenance |
|---|---|---|
| Iterative-overlap winner selection | `scripts/iterative_overlap.R` | `peak_utils.R`, `createIterativeOverlapPeakSet.R` |
| 501bp summit-centered normalization | `scripts/normalize_width.R` | `peak_utils.R` |
| Cross-strategy support + score boost | `scripts/support_voting.R` | `peak_utils.R`, `S2_6b_..._multistrategies.R` |
| Fraction of reads in peaks (FRiP) | `scripts/frip.R` | `peak_utils.R` |
| ENCODE blacklist load + invert overlap | `scripts/blacklist.R` | `peak_utils.R` |

## References (load on demand)

| Topic | File |
|---|---|
| scATAC MACS3 invocation, every flag, 501bp + QC filters, Signac wrapper | `references/macs3-scatac-params.md` |
| Iterative-overlap algorithm in prose; relation to iterative-peak-merging; SPM/rule path | `references/iterative-overlap-merge.md` |
| `n_strategies` as confidence; compute-before-merge rule; the score boost | `references/support-voting.md` |
| Adaptive per-cluster threshold, stratified sampling, rescue, metadata pre-filter | `references/rare-celltype-protection.md` |
| FRiP / TSS / peaks-per-cell / marker / embedding / chromVAR validation | `references/validation-battery.md` |

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Every peak appears to have full 4-strategy support | Support computed AFTER the final merge — overlapping winners "bridge" all strategies onto each survivor | Compute `n_strategies` on the per-strategy merged sets BEFORE the final merge (`calculate_strategy_support` then merge), not after |
| Merge collapses peaks to a midpoint coordinate | Used `GenomicRanges::reduce()` / `bedtools merge` as the merge | Use summit-faithful `convergeClusterGRanges` — it keeps the actual highest-score peak per cluster, never a midpoint |
| Rare cell types vanish after filtering | A single global cell-count threshold prunes anything rare | Use the adaptive per-cluster threshold `max(15, min(0.02*n, 200))` (keep if it passes in ANY cluster) plus the 4-strategy rescue |
| MACS returns identical peaks across groups | The grouping variable (`group.by`) was never set, so every "group" is the whole dataset | Set the grouping variable explicitly per strategy before pseudobulk/peak calling |

---

## Resources

- ArchR (iterative-overlap method): https://www.archrproject.com
- Corces & Granja et al., Science 2018: https://www.science.org/doi/10.1126/science.aav1898
- ArchR (Granja et al., Nat Genet 2021): https://www.nature.com/articles/s41588-021-00790-6
- MACS3: https://macs3-project.github.io/MACS/
- ENCODE blacklist (Amemiya et al. 2019): https://github.com/Boyle-Lab/Blacklist

---

## When not to use

- Do not use to call peaks de novo. Use snapatac2-atac-preprocessing or signac-chromatin-analysis instead.
- Do not use for the bare within-study merge primitive from MACS summits. Use iterative-peak-merging instead.
- Do not use this router alone to run an analysis. Pair with peak-atlas-multiome (paired) or peak-atlas-unpaired (unpaired) instead.

---

## See also

- `peak-atlas-multiome` — Child (paired regime); paired multiome consensus (RNA+ATAC same cells)
- `peak-atlas-unpaired` — Child (unpaired regime); unpaired consensus (transfer identity to ATAC)
- `iterative-peak-merging` — Embedded primitive; bare within-study merge from MACS summit BEDs
- `snapatac2-atac-preprocessing` — Upstream calling; de-novo peak calling + fragment/QC preprocessing
- `signac-chromatin-analysis` — Upstream / downstream; Signac peak calling, quantification, coverage
- `chromvar-motif-accessibility` — Downstream validation / use; per-cell TF-motif activity once the atlas is fixed

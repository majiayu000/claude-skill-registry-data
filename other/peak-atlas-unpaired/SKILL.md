---
name: peak-atlas-unpaired
description: "Consensus scATAC peak atlas from unpaired data (separate scRNA/scATAC pools): bridges modalities via gene-activity + staged CCA transfer, calls peaks (coarse/refined/label-free), tier-stratifies, gates risky peaks on external correlation. Use when RNA/ATAC aren't the same cells. For true multiome use peak-atlas-multiome."
license: MIT
---

# Unpaired Consensus Peak Atlas (transferred-identity scATAC)

**Foundation:** `peak-atlas-framework` holds the shared spine — the `CALL → MERGE → FILTER → TIER → VALIDATE` methodology, the support-voting machinery, rare-cell-type protection, and the validation battery. Read it first, then jump directly to:
- `peak-atlas-framework/references/macs3-scatac-params.md` — the Signac `CallPeaks` wrapper, the 501bp normalization, and the standard-chromosome / blacklist / N-content filters every strategy below reuses.
- `peak-atlas-framework/references/iterative-overlap-merge.md` — summit-faithful winner selection (the modern alternative to explicit tiers).
- `peak-atlas-framework/references/support-voting.md` — `n_strategies` as confidence and the compute-support-before-merge rule.
- `peak-atlas-framework/references/rare-celltype-protection.md` — adaptive per-cluster keep-thresholds.
- `peak-atlas-framework/references/validation-battery.md` — FRiP / marker / embedding gates that run alongside the unpaired-specific correlation test below.

This file covers ONLY what is unpaired-specific. Genome-specific values shown (mm10/mm39, `effective.genome.size = 1.87e9`) come from the source project — parameterize them for your build.

## The unpaired problem

RNA and ATAC come from **separate cell pools of the same biological system**, so there are no shared barcodes and you cannot read cell identity off the ATAC cells. Identity must be **transferred** from the annotated RNA reference. The bridge is a **gene-activity matrix**: `Signac::GeneActivity()` sums fragments over each gene body plus promoter to produce a gene-level surrogate "RNA" assay on the ATAC cells. That surrogate assay is the only feature space the two modalities share, so all anchoring happens there.

```
Annotated scRNA reference  ──┐
                             ├─ shared feature space = gene activity ─→ CCA anchors ─→ transferred labels
scATAC pool (GeneActivity) ──┘
```

---

## Decision tree

```
Separate RNA and ATAC pools, need a peak atlas?
│
├─ Cell identity already known on the ATAC cells?  → you are NOT unpaired; use peak-atlas-multiome
│
└─ Identity must be transferred from RNA:
    ├─ Have an annotated RNA reference + GeneActivity on ATAC  → run this skill
    │     ├─ coarse lineage labels stable?      → Strategy A (per cell type)
    │     ├─ need rare subtype × condition?     → Strategy B (refined × condition)
    │     └─ hedge against transfer error?      → Strategy C (label-free, by condition)
    └─ No RNA reference at all  → degrade to ATAC clusters + external consensus (framework router)
```

---

## Label transfer (the bridge), staged in two rounds

Anchor in gene-activity space, transfer with the ATAC LSI as the weighting reduction:

```r
DefaultAssay(rna_ref) <- "RNA"; DefaultAssay(atac) <- "RNA"   # both on gene activity
anchors <- FindTransferAnchors(reference = rna_ref, query = atac,
             features = VariableFeatures(rna_ref),
             reduction = "cca", dims = 2:30)
pred <- TransferData(anchorset = anchors, refdata = rna_ref$cell_annotations,
             weight.reduction = atac[["lsi"]], dims = 2:30, k.weight = 100)
```

Why staged in two rounds (provenance: `S5.1a_integration_r1.R`, `S5.2a_integration_r2.R`):

| Round | Reference | Labels | Threshold | Drives |
|---|---|---|---|---|
| **R1** | whole RNA reference | COARSE lineage (e.g. cDC1, cDC2, Mac, Mono) | `prediction.score.max >= 0.50` | Strategy A |
| **R2** | focused RNA reference (target lineages only) | REFINED subtype | `>= 0.55` (stricter) | Strategy B |

R2 transfers refined labels onto the *R1-labeled* ATAC — coarse first, then resolve subtypes within. The stricter R2 threshold reflects that fine labels are noisier. Cells below threshold (or mapping outside the target label set) become **LowConf** and are **excluded from label-resolved calling** (`subset(atac, label_highconf != "LowConf")`) so unreliable labels do not contaminate peaks. `scripts/label_transfer_strategy.R` reproduces both rounds and the per-strategy call.

---

## Strategies A / B / C (the crux)

Three complementary groupings of the SAME ATAC cells. Each is peak-called independently, then the framework's support-voting and merge combine them.

| Strategy | Grouping | Min cells/group | Captures | Robust to transfer error? |
|---|---|---|---|---|
| **A** | coarse cell type (R1) | 100 | lineage identity | partly (coarse labels are stable) |
| **B** | refined subtype × condition (R2) | **20** (lowered from 50) | rare condition-specific interactions | least (fine labels) |
| **C** | condition ONLY — **label-free** | 100 | global condition effects, maximum power | YES — uses no transferred labels |

Strategy C is the **transfer-error-robust maximum-power hedge**: it groups by `orig.ident` (condition) with no cell-type labels, so even if label transfer is wrong, C still recovers the accessible landscape. B lowers its minimum to 20 specifically to keep biologically critical rare subtypes (e.g. a ~24-43 cell condition-specific population) that a 50-cell floor would erase.

**Shared call** — every strategy uses the same Signac wrapper (see `peak-atlas-framework/references/macs3-scatac-params.md`):

```r
CallPeaks(object = atac_highconf, group.by = <grouping>, idents = <one group>,
          format = "BEDPE", effective.genome.size = 1.87e9,
          additional.args = "-q 0.01 --call-summits --nolambda --keep-dup all")
```

`group.by` is **critical**. Without it Signac passes *all* fragments to MACS regardless of `idents`, so every group returns identical peaks — a real bug fixed in the source (see Pitfalls). The label-free C path sets `group.by = "orig.ident"`.

**Shared post-process** (identical across A/B/C, per group then across groups):
1. summit (`start + mcols$peak`) → `resize(width = 501, fix = "center")`
2. keep standard chromosomes (`chr1..chr19, chrX, chrY` for mouse)
3. drop blacklist overlaps; drop N-rich peaks (N fraction `>= 0.1`)
4. merge groups: `reduce(min.gapwidth = 50)` then re-`resize(501)`
5. score each merged peak by **support count** = number of groups containing it (`n_celltypes` / `n_groups` / `n_conditions`)

The per-strategy support count is the score that feeds the framework merge. Full code: `scripts/label_transfer_strategy.R`. The A/B/C rationale in depth: `references/abc-strategies.md`.

---

## External-dataset consensus (a peak SOURCE, not just annotation)

External ATAC datasets from the same system contribute *coordinates*, not merely overlap flags. Build them into a consensus peak source (`scripts/build_consensus.R`, provenance `S4.1a`/`S4.1b`):

1. Harmonize every external dataset to uniform 501bp (summit-centered, same chromosome/blacklist/N filters as above).
2. Optionally **merge replicates** first: per replicate group, union scaffold then keep peaks with `>= 50%` replicate support (`ceiling(n_reps * 0.5)`) — corrects pseudo-replication before counting datasets.
3. Union scaffold across datasets: `reduce(min.gapwidth = 100)`.
4. Per-peak **support matrix** (which datasets overlap each union peak).
5. **Consensus threshold 0.25**: keep peaks present in `>= 25%` of datasets (`ceiling(n_datasets * 0.25)`).
6. **Bias check**: warn if any single dataset contributes `> 40%` of consensus peaks, error if `> 50%` (`checks/check_consensus_bias.R`).

An annotation-only external set (e.g. an aging atlas with no usable coordinates for your build) can still *flag* overlap with your de-novo peaks without *contributing* coordinates — keep those out of the coordinate union but use them at validation. Details: `references/external-consensus.md`.

---

## Tier stratification (selecting the best peak set)

Take the union of A+B+C and assign tiers **in priority order** (first match wins; provenance archived `S6.1a_multitier_reproducibility.R`). Each peak carries per-strategy `max_score` (= support count), `n_conditions`, `n_groups`, and a `has_rare_celltype` flag.

| Tier | Criterion | Why |
|---|---|---|
| **Tier 0 — Biological priority** | `has_rare_celltype` AND ( (Strategy-B `score > 15` and `n_groups > 0`) OR (present in both A and B) ) | protects rare condition-specific biology from being out-voted |
| **Tier 1 — Cross-strategy** | `>= 2` of A/B/C | independent corroboration |
| **Tier 2 — High cell fraction** | A `max_n_cells` `>= ~20%` of cells OR B `score > 25` | abundant, high-confidence |
| **Tier 3a — Cross-condition** | `>= 2` conditions AND `score > 15` (B or C) | reproducible across conditions |
| **Tier 3b — Condition-specific target** | celltype of interest, 1 condition, `score > 15`, `>= 20` cells | genuine condition-specific biology |
| **Tier 4 — Cross-cluster** | `>= 2` clusters (with score gate for B) | weaker reproducibility |
| **NotReproducible** | none of the above | excluded |

**Sub-stratify Tier 0** by `cross_strategy_count` (how many of A/B/C found it; provenance `S6.2a_tier0_stratification.R`, `scripts/tier_stratification.R`):

| Sub-tier | Support | Confidence | Action |
|---|---|---|---|
| **0a** | 3-strategy | HIGH | keep unconditionally |
| **0b** | 2-strategy | MEDIUM | keep + validate |
| **0c** | 1-strategy | LOW | keep ONLY if external-validation correlation `r >= 0.4` |

Tier 0c is the dangerous bucket: single-strategy rare-cell peaks that are *either* genuine rare biology *or* noise. Do not keep them on faith — gate on the correlation test below. The full scheme is in `references/tier-stratification.md`.

**Modern alternative:** a newer pipeline drops explicit tiers entirely in favor of the framework's **summit-faithful iterative winner-selection** (`iterative-overlap-merge.md`) with strategy/source recorded as peak metadata. Prefer it for new work; the tier scheme remains the documented, auditable fallback and the way to read older atlases.

---

## Validation (unpaired-specific PRIMARY test)

The headline gate is **external-correlation**, which doubles as the Tier-0c decision (provenance `S6.2a_validation_primary.R`):

1. Build a **pseudobulk accessibility profile** per ATAC cell type (or cell type × condition): `FeatureMatrix(fragments, features = atlas, cells)` then `rowSums`, normalized TPM-style to `1e6`.
2. Build **binary accessibility** per external dataset against the same atlas (peak overlaps external = 1, else 0).
3. **Pearson-correlate** every ATAC profile against every external profile.
4. A **named hypothesis test** gates retention: e.g. a putative BATF3-independent cDC1 subtype must track an IRF8-KO dataset at `r >= 0.4`. Pass → keep the risky peaks; fail → drop Tier-0c (and reconsider 0b). Details in `references/external-validation.md`.

Plus two structural checks:
- **CellRanger overlap:** `>= 80%` of the de-novo atlas overlapping CellRanger default peaks means CellRanger is redundant (safe to exclude it); `< 50%` is critical (you are missing baseline accessibility — add CellRanger).
- **Strategy comparison:** UpSet / Venn of A vs B vs C to see what each contributes.

Run the framework battery (FRiP retention, marker promoter retention, embedding) on top of these — see `peak-atlas-framework/references/validation-battery.md`.

---

## Scripts and references

| Need | File | Provenance |
|---|---|---|
| GeneActivity + staged CCA transfer + per-strategy A/B/C call | `scripts/label_transfer_strategy.R` | `S5.1a`, `S5.2a`, `S5.1b`, `S5.2b`, `S4.1c` |
| External union + support matrix + 0.25 threshold + replicate merge + bias | `scripts/build_consensus.R` | `S4.1b`, `S4.1a` |
| Tier assignment + Tier-0 0a/0b/0c sub-stratification | `scripts/tier_stratification.R` | `S6.2a_tier0_stratification.R`, archived `S6.1a` |
| Consensus-bias gate (warn >40%, fail >50%) | `checks/check_consensus_bias.R` | `S4.1b` |

| Topic | Reference |
|---|---|
| Gene-activity bridge + staged transfer + thresholds | `references/label-transfer-bridge.md` |
| A/B/C strategies in depth, incl. the label-free hedge | `references/abc-strategies.md` |
| External union / threshold / replicate / bias | `references/external-consensus.md` |
| Tier scheme + 0a/0b/0c | `references/tier-stratification.md` |
| PRIMARY correlation test + CellRanger overlap | `references/external-validation.md` |

---

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Every group returns the same peaks | `CallPeaks` called without `group.by`, so MACS sees all fragments regardless of `idents` | Always pass `group.by = <grouping column>`; `idents` alone does not subset fragments |
| Lineage-specific peaks look contaminated / smeared | LowConf cells (below the transfer threshold) were kept in label-resolved calling | `subset(atac, label_highconf != "LowConf")` before Strategy A/B; LowConf only excused for label-free Strategy C |
| Consensus dominated by one big atlas | One external dataset (or un-merged replicate set) supplies most union peaks | Merge replicates first (>=50% support), then run `check_consensus_bias.R`; investigate at `> 40%`, fail at `> 50%` |
| Rare-biology peaks turn out to be noise | Tier 0c (single-strategy) kept without corroboration | Gate Tier 0c on the PRIMARY external-correlation test (`r >= 0.4`); drop it if the named hypothesis fails |

---

## Resources

- Signac (GeneActivity, CallPeaks, label transfer): https://stuartlab.org/signac/
- Seurat transfer anchors / TransferData: https://satijalab.org/seurat/
- MACS3: https://macs3-project.github.io/MACS/
- ENCODE blacklist (Amemiya et al. 2019): https://github.com/Boyle-Lab/Blacklist
- Iterative-overlap origin (Corces & Granja, Science 2018): https://www.science.org/doi/10.1126/science.aav1898


---

## When not to use

- Do not use for paired 10x Multiome (RNA+ATAC in the same cells). Use peak-atlas-multiome instead.
- Do not use to learn the shared merge/voting/validation methodology. That lives in peak-atlas-framework.

---

## See also

- `peak-atlas-framework`
- `peak-atlas-multiome`
- `seurat-unpaired-cross-modality`
- `signac-chromatin-analysis`
- `iterative-peak-merging`

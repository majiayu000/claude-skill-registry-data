---
name: bulk-rnaseq-activity-inference
description: "DecoupleR activity inference from bulk RNA-seq DE results — transcription-factor activities (ULM + CollecTRI) and pathway activities (MLM + PROGENy, 14 canonical pathways), plus barplots, volcanos, and target-gene scatters. Use when scoring TF or pathway activity from limma/edgeR output. For MSigDB gene-set enrichment use bulk-rnaseq-gsea."
license: MIT
---

# Bulk RNA-seq Activity Inference (DecoupleR)

## Overview

This skill covers footprint-based activity inference from bulk RNA-seq DE results — a method family that is complementary to, not a replacement for, GSEA. Where GSEA asks "is this gene set enriched in my ranked list?", activity inference asks "which regulator or signaling program drove the expression changes I observe?"

Two inference tools share the same DecoupleR framework and OmniPath data infrastructure:

| Tool | Network | Method | Output | Scale |
|------|---------|--------|--------|-------|
| **TF activity** | CollecTRI (literature + ChIP) | ULM (weighted linear model) | Per-TF activity score | ~500-1500 TFs |
| **PROGENy** | Consensus footprints | MLM (multivariate linear model) | Per-pathway activity score | 14 canonical pathways |

Both are run in parallel, not as alternatives. Their outputs feed the same visualization layer and the same interactive pathway explorer.

**When to use this skill:**
- Inferring which transcription factors are differentially active between conditions
- Computing signaling pathway activity changes for the 14 canonical PROGENy pathways
- Building `master_tf_activities.csv` and `master_progeny_activities.csv`
- Visualizing activity results (barplots, volcano, target-gene scatter, direction summary)

**When NOT to use this skill:**
- Gene set enrichment against MSigDB, MitoCarta, TransportDB, or GO → use `bulk-rnaseq-gsea`
- Interactive UMAP pathway explorer (consumes the master CSVs this skill produces) → use `bulk-rnaseq-pathway-explorer`
- Topology-aware metabolic module discovery → use `gatom-metabolomic-predictions`

---

## Decision Tree

```
Need to understand regulatory activity from DE results?
|
+-- Want TF activity scores (which transcription factors are active)?
|   --> references/tf-activity.md
|       Tool: DecoupleR ULM + CollecTRI
|       Output: score per TF (+ p-value), master_tf_activities.csv
|       Key patterns: t-stat input, minsize=5, cache network, BH correction
|
+-- Want signaling pathway activity (14 canonical pathways)?
|   --> references/progeny.md
|       Tool: DecoupleR MLM + PROGENy (top=500 for bulk)
|       Output: 14 rows, master_progeny_activities.csv
|       Key patterns: .mor="weight" not "mor", no MTC needed at n=14
|
+-- Have master CSVs, need static publication figures?
|   --> references/visualization.md
|       Covers: barplot, volcano, direction summary, target-gene scatter
|       Key patterns: 4-category TF chart, significance stars for PROGENy,
|                     ggplot2 4.0 NA-color fix, symmetric NES scale
|
+-- Have master CSVs, need interactive HTML exploration?
    --> bulk-rnaseq-pathway-explorer (standalone skill)
```

*TF and PROGENy inference are independent — run them in parallel (scripts 1.7 and 1.8 have no dependency between them).*

---

## Quick Start

Minimal TF activity inference + PROGENy in one session:

```r
library(decoupleR)
library(dplyr)

# Shared input: t-statistic matrix (genes x contrasts)
de_results <- readRDS("03_results/checkpoints/1.1_de_results.rds")
deg_table  <- de_results[["IL2RAKO_vs_NTC"]]
mat        <- deg_table %>% dplyr::select(t) %>% as.matrix()
mat[is.na(mat)] <- 0

# --- TF activity (ULM + CollecTRI) ---
net_tf <- decoupleR::get_collectri(organism = "mouse", split_complexes = FALSE)
tf_acts <- decoupleR::run_ulm(
  mat = mat, net = net_tf,
  .source = "source", .target = "target", .mor = "mor",
  minsize = 5
) %>% filter(condition == "t")

stopifnot(nrow(tf_acts) >= 50)
message("TF activity: ", nrow(tf_acts), " TFs inferred")

# --- PROGENy (MLM + PROGENy footprints) ---
net_pg <- decoupleR::get_progeny(organism = "mouse", top = 500)
pathway_acts <- decoupleR::run_mlm(
  mat = mat, net = net_pg,
  .source = "source", .target = "target", .mor = "weight",
  minsize = 5
) %>% filter(condition == "t")

stopifnot(nrow(pathway_acts) == 14)
message("PROGENy: 14 pathway activity scores")
```

---

## Pipeline Architecture

### Execution order

```
1.1  core_pipeline.R           -> DE results (prerequisite for both)
1.7  decoupler_tf_analysis.R   -> TF activity inference + master_tf_activities.csv
1.8  progeny_analysis.R        -> PROGENy inference + master_progeny_activities.csv
2.3  tf_viz.R                  -> TF visualization (barplot, volcano, direction, histogram)
2.4  progeny_viz.R             -> PROGENy visualization (barplot, volcano, target scatter)
3.1  pathway_explorer.py       -> Interactive HTML (consumes master_tf + master_progeny CSVs)
```

Scripts 1.7 and 1.8 can run in parallel. Scripts 2.3 and 2.4 can run in parallel.

### Data flow

```
limma-voom DE results (gene symbols as rownames, t-statistic)
    |
    +-- DecoupleR ULM  + CollecTRI  -> TF activity scores  -> master_tf_activities.csv
    |                                                              |
    +-- DecoupleR MLM  + PROGENy    -> 14 pathway scores   -> master_progeny_activities.csv
                                                                   |
                           Static figures (R/ggplot2) <------------+
                           Interactive explorer (Python/Plotly UMAP) <-- both CSVs
```

### Output files

| File | Contents | Rows |
|------|----------|------|
| `03_results/checkpoints/1.7_tf_results.rds` | Raw ULM output | ~500-1500 |
| `03_results/checkpoints/1.8_progeny_results.rds` | Raw MLM output | 14 |
| `03_results/tables/master_tf_activities.csv` | 13-column normalized TF table | ~500-1500 |
| `03_results/tables/master_progeny_activities.csv` | 13-column normalized PROGENy table | 14 |
| `03_results/plots/TF/tf_activity_barplot.pdf` | Top 25 TFs by p-value | — |
| `03_results/plots/TF/tf_activity_volcano.pdf` | Activity vs significance | — |
| `03_results/plots/PROGENy/progeny_activity_barplot.pdf` | All 14 pathways with stars | — |
| `03_results/plots/PROGENy/progeny_targets_*.pdf` | Target gene scatter (top 4) | — |

---

## Key Differences: TF Activity vs PROGENy

| Aspect | TF Activity (ULM) | PROGENy (MLM) |
|--------|-------------------|---------------|
| Network | CollecTRI (TF→target, literature+ChIP) | PROGENy consensus footprints |
| Method | Univariate linear model per TF | Multivariate linear model |
| Weight type | ±1 + intermediate MoR | Continuous signed weights |
| Scale | Hundreds of TFs | Exactly 14 pathways |
| MTC needed | Yes (BH correction) | No (n=14 tests) |
| Column for .mor | `"mor"` | `"weight"` |
| Primary use | "Which TF drives this?" | "Which canonical signal changed?" |

---

## Verification Checklist

- [ ] **TF count reasonable:** 100-1500 TFs with `minsize=5`. Under 50 = symbol mismatch with network.
- [ ] **PROGENy count exact:** `nrow(pathway_acts) == 14`. Any other count = network/filtering problem.
- [ ] **Activity centered near 0:** `abs(mean(tf_acts$score)) < 5`; strong bias suggests input matrix issue.
- [ ] **Known biology check:** For IL-2 signaling experiments, STAT5 (TF) and JAK-STAT (PROGENy) should show activity.
- [ ] **Master CSVs written:** `master_tf_activities.csv` and `master_progeny_activities.csv` exist in `03_results/tables/`.
- [ ] **PROGENY_ prefix:** All PROGENy `pathway_id` values start with `PROGENY_`.
- [ ] **Visualization complete:** Per-output PDFs exist in `plots/TF/` and `plots/PROGENy/`.

---

## Common Pitfalls (Cross-Stage)

| Symptom | Stage | Cause | Fix |
|---------|-------|-------|-----|
| Under 50 TFs inferred | TF | Gene symbol mismatch with CollecTRI | `sum(rownames(mat) %in% net$target)` should be thousands |
| `run_mlm` wrong .mor | PROGENy | Used `.mor = "mor"` instead of `.mor = "weight"` | PROGENy network column is named `weight` |
| padj = pvalue for TFs | TF | No BH correction applied | `p.adjust(tf_acts$p_value, method = "BH")` |
| Volcano points missing | Viz | `color = NA` on shape 21 (ggplot2 4.0+) | Use `stroke = 0` or `color = "transparent"` |
| Network download timeout | Both | OmniPath unreachable | Cache network on first download with `saveRDS()` |
| `get_collectri`/`get_progeny` error: `argument is of length zero` | Both | OmnipathR static-table loader bug (decoupleR↔OmnipathR version skew), **not** necessarily an outage | Build networks locally (`progeny::getModel`, `dorothea::dorothea_mm`, Zenodo CollecTRI + babelgene) → **`references/known-issues.md`** |

For full pitfall walkthroughs → see the relevant reference document.

### Gotcha: report the FULL regulon as TF membership, never a top-N slice

The TF gene-set membership (`genes_full_set`) handed downstream to the **pathway-explorer**
(or any similarity/embedding layer) must be the **FULL CollecTRI regulon for that TF,
intersected with the shared gene universe** — *not* a top-N (e.g. top-50) slice of targets.

- A `slice_head(n = 50)` cap on the reported targets understates TF↔pathway gene overlap.
  Similarity-based UMAP embeddings compute distances from `genes_full_set` overlap, so a
  truncated regulon makes every TF look artificially dissimilar from the pathways it actually
  drives, pushing all TFs into a **spurious distant cluster** in the embedding.
- The fix is to report the complete atlas-intersected regulon as membership. This does **not**
  touch the activity score: ULM/`run_ulm` (and MLM/`run_mlm` for PROGENy) already infer the
  score from the full network — the slice only ever affected which targets were *reported*,
  never the `nes`/`score`/`padj` statistic.
- Keep a top-N list only for **display/tooltips** if a UI needs a short preview — never for
  overlap, similarity, or embedding computation.

The same principle holds for PROGENy footprints and GATOM modules: the reported membership
fed to the geometry layer is the full set ∩ universe, decoupled from the per-contrast score.

---

## Resources

- **DecoupleR docs:** https://saezlab.github.io/decoupleR/
- **DecoupleR paper:** Badia-i-Mompel et al. (2022) Bioinformatics, doi:10.1093/bioinformatics/btac651
- **CollecTRI paper:** Muller-Dott et al. (2024) Nucleic Acids Research, doi:10.1093/nar/gkad841
- **PROGENy paper:** Schubert et al. (2018) Nature Communications, doi:10.1038/s41467-017-02391-6
- **OmniPath:** https://omnipathdb.org/

---

## Deeper Reference (load on demand)

- `references/tf-activity.md` — DecoupleR ULM + CollecTRI: input matrix prep, network loading and caching, multi-contrast matrices, DoRothEA alternative, master table schema, BH correction
- `references/progeny.md` — PROGENy MLM: 14 pathway table, .mor="weight" pitfall, concordance analysis, comparison to GSEA, species support, master table schema
- `references/visualization.md` — barplot/volcano/direction-summary/distribution patterns, PROGENy significance stars, target-gene scatter with concordance coloring, README generation, output organization
- `references/known-issues.md` — OmniPath/decoupleR fetch failures (`get_collectri`/`get_progeny` "argument is of length zero") and the local-network fallback (`progeny::getModel`, `dorothea_mm`, Zenodo CollecTRI + babelgene)

---

## When not to use

- Do not use for gene-set enrichment (MSigDB, MitoCarta, TransportDB, GO). Use bulk-rnaseq-gsea instead.
- Do not use for interactive UMAP pathway explorer. Use bulk-rnaseq-pathway-explorer instead.
- Do not use for topology-aware metabolic module discovery. Use gatom-metabolomic-predictions instead.

---

## See also

- `bulk-rnaseq-gsea` — Parallel analysis; gene-set enrichment (MSigDB, MitoCarta, TransportDB, GO) is a different question
- `bulk-rnaseq-pathway-explorer` — Next step; interactive UMAP pathway/TF/PROGENy explorer HTML (consumes master CSVs)
- `gatom-metabolomic-predictions` — Extension; topology-aware metabolic module discovery

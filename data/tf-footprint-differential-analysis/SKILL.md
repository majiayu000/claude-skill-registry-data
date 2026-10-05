---
name: tf-footprint-differential-analysis
description: "Orchestrator for TF footprinting and differential binding from pseudobulk ATAC-seq. Routes to tobias-footprint-bindetect (pairwise differential), hint-atac-differential-footprint (multi-condition overview), or signac-footprint-visualization (figures), and cross-plots occupancy against chromvar-motif-accessibility activity."
license: MIT
---

# TF Footprint & Differential Footprint Analysis (Orchestrator)

## Purpose

Identify TF binding sites from ATAC-seq footprints and compare TF occupancy across conditions. Footprinting detects physical DNA protection by bound TFs within accessible chromatin, complementing motif accessibility (ChromVAR) with occupancy evidence.

**Key distinction:**
- **ChromVAR** measures **accessibility** (potential for binding — chromatin open at motif sites)
- **Footprinting** measures **occupancy** (actual binding — protein physically protects DNA from Tn5)

**Upstream:** Peak calling (MACS2/MACS3), pseudobulk BAM generation (ArchR/Signac), ChromVAR deviations
**Downstream:** TF regulatory networks, quadrant analysis with ChromVAR, GRN inference (SCENIC+)

## Tool Selection Guide

| Feature | **TOBIAS** (`tobias-footprint-bindetect`) | **HINT-ATAC** (`hint-atac-differential-footprint`) | **Signac** (`signac-footprint-visualization`) |
|:---|:---|:---|:---|
| **Algorithm** | Tn5 bias correction (linear regression) + footprint scoring | HMM-based detection (learns footprint states) | Normalized Tn5 insertion profiles |
| **Tn5 Bias Correction** | Best in class (`ATACorrect`) | Good (bias table) | Basic (k-mer model) |
| **Differential Analysis** | Excellent (pairwise; p-values via `BINDetect`) | Good (multi-condition; `rgt-hint differential`) | Weak (visualization only) |
| **Pseudobulk Support** | High (designed for merged BAMs) | High (designed for merged BAMs) | Medium (fragment files, slow at scale) |
| **Output** | BigWigs, volcano plots, TSV tables | BED files, line plots, statistics TXT | Seurat objects, ggplot2 figures |
| **Best For** | Quantitative pairwise differential | Multi-condition overview heatmaps | Publication figures |

**Default routing:**
- **Quantitative pairwise differential** (WT vs KO with p-values) → `tobias-footprint-bindetect`
- **Multi-condition overview** (3+ conditions in one run) → `hint-atac-differential-footprint`
- **Publication figures** for selected TFs → `signac-footprint-visualization`
- **Per-cell TF activity** (not footprinting) → `chromvar-motif-accessibility`
- **Combined approach** (recommended): TOBIAS for quantitation + Signac for figures + HINT-ATAC if >2 conditions

## Shared Motif Database Recommendations

### For Mouse (mm10)

| Database | Version | Mouse TFs | DC Coverage | Format | Notes |
|----------|---------|-----------|-------------|--------|-------|
| **JASPAR** | 2024 Core Vertebrates | ~800+ | Excellent (IRF8, BATF::JUN, SPI1, ETS1, RUNX) | `.jaspar`, `.meme` | Field standard, recommended |
| **HOCOMOCO** | v11 | ~400 mouse | Good (IRF, ETS, RUNX families) | `.meme`, `.pcm` | High quality, curated |
| **CIS-BP** | 2.0 | ~1200+ | Comprehensive | Custom TSV | Broadest, some redundancy |
| **chromVARmotifs** | v1 | Curated | Good | R `PWMatrixList` | Used by chromVAR natively |

**Recommendation:** Use **JASPAR 2024 Core Vertebrates** as the shared motif set across TOBIAS, HINT-ATAC, Signac, and ChromVAR. Different PWMs for the same TF yield different binding-site calls and break cross-tool correlation.

### Exporting ChromVAR motifs to MEME (for TOBIAS reuse)

```r
library(TFBSTools)
library(universalmotif)

motif_pwms <- GetMotifData(obj, slot = "pwm")  # From Signac object
motif_list <- lapply(names(motif_pwms), function(nm) {
  convert_motifs(motif_pwms[[nm]], class = "universalmotif-universalmotif")
})
write_meme(motif_list, file = "chromvar_motifs.meme", overwrite = TRUE)
```

## Quadrant Analysis (Footprint × Accessibility)

ChromVAR (accessibility) and TOBIAS (occupancy) provide complementary evidence. Integrate via scatter plot:

| Quadrant | ChromVAR | Footprint | Interpretation |
|----------|----------|-----------|----------------|
| **Q1** | High delta | High delta | **True drivers** — chromatin open AND TF bound |
| **Q2** | High delta | Low delta | **Poised / pioneer** — accessible but TF not occupying (short residence, indirect effect) |
| **Q3** | Low delta | High delta | Rare — binding in less accessible regions (pioneer) or artifact |
| **Q4** | Low delta | Low delta | Not active at these sites |

### Implementation in R

```r
library(tidyverse)

# Load TOBIAS results
tobias <- read_tsv("differential/cDC1_WT_vs_KO/bindetect_results.txt")

# Load ChromVAR differential results (delta deviation per motif)
chromvar_diff <- read_csv("hub/A3_tf_activity_by_celltype.csv")

# Merge on TF/motif name (requires name harmonization across DBs)
combined <- inner_join(
  tobias %>% select(motif_id = output_prefix,
                    tobias_score = WT_Batf3_KO_change,
                    tobias_pval  = WT_Batf3_KO_pvalue),
  chromvar_diff %>% select(motif_id, chromvar_delta = delta_deviation),
  by = "motif_id"
)

ggplot(combined, aes(x = chromvar_delta, y = tobias_score)) +
  geom_point(aes(color = tobias_pval < 0.05), alpha = 0.6) +
  geom_hline(yintercept = 0, linetype = "dashed") +
  geom_vline(xintercept = 0, linetype = "dashed") +
  ggrepel::geom_text_repel(
    data = combined %>% filter(tobias_pval < 0.05),
    aes(label = motif_id), size = 3, max.overlaps = 20
  ) +
  scale_color_manual(values = c("grey70", "red3")) +
  labs(x = "ChromVAR Delta Deviation (Accessibility)",
       y = "TOBIAS Differential Binding Score (Occupancy)",
       title = "TF Activity: Accessibility vs Occupancy") +
  theme_minimal()
```

## Cross-Tool Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| ChromVAR vs TOBIAS disagree | Different motif databases | Use identical PWM set for both (see export snippet above) |
| Motif name mismatch when joining | Database-specific IDs (`MA0080.5` vs `SPI1`) | Build an explicit ID-to-symbol mapping table |
| TOBIAS / HINT-ATAC contradict | Pairwise vs multi-condition framing | Compare pairwise sub-contrasts within HINT-ATAC's multi-condition run |

## Resources

- **TOBIAS**: Bentsen et al., Nat Commun 2020 ([DOI: 10.1038/s41467-020-18035-1](https://doi.org/10.1038/s41467-020-18035-1)) — https://github.com/loosolab/TOBIAS
- **HINT-ATAC**: Li et al., Genome Biol 2019 ([DOI: 10.1186/s13059-019-1642-2](https://doi.org/10.1186/s13059-019-1642-2)) — https://reg-gen.readthedocs.io/
- **Signac footprint vignette**: https://stuartlab.org/signac/articles/footprint
- **JASPAR 2024**: https://jaspar.elixir.no/
- **HOCOMOCO v11**: https://hocomoco11.autosome.org/


---

## When not to use

- Do not use for single-cell resolution TF activity — use chromvar-motif-accessibility.
- Do not use for motif enrichment on DARs — use pycistarget-motif-enrichment.

---

## See also

- `chromvar-motif-accessibility`
- `pycistarget-motif-enrichment`
- `iterative-peak-merging`
- `scenic-grn-inference`

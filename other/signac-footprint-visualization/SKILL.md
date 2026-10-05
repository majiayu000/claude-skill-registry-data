---
name: signac-footprint-visualization
description: "Signac Footprint() and PlotFootprint() for R-side TF footprint visualization on Seurat ChromatinAssay objects. Use for publication figures showing observed vs expected Tn5 cutting around motif sites, grouped by cell type or condition. For quantitative differential analysis use tobias-footprint-bindetect."
license: MIT
---

# Signac TF Footprint Visualization

## Purpose

Compute and plot TF footprint profiles directly on a Seurat object with a Signac `ChromatinAssay`. Output is publication-ready ggplot2 figures showing observed vs expected Tn5 cutting around motif sites, grouped by any `obs` column (typically cell type or condition).

**Use when:**
- Producing footprint figures for a manuscript or report
- Confirming binding patterns for a small set of selected TFs
- Inspecting footprints grouped by Seurat cluster / cell type / condition

**Upstream:** Seurat object with `ChromatinAssay`, fragments file indexed, motifs added via `AddMotifs()`
**Downstream:** ggplot2 / patchwork composition for figure panels

## Setup Motif Information

```r
library(Signac)
library(Seurat)
library(motifmatchr)
library(JASPAR2020)
library(TFBSTools)
library(BSgenome.Mmusculus.UCSC.mm10)

obj <- readRDS("integrated_object.rds")

# Get motif PWMs (10090 = Mus musculus; 9606 = Homo sapiens)
pwm <- getMatrixSet(
  x = JASPAR2020,
  opts = list(species = 10090, all_versions = FALSE)
)

# One-time, slow: add motif positions to object
obj <- AddMotifs(obj, genome = BSgenome.Mmusculus.UCSC.mm10, pfm = pwm)
```

## Compute and Plot Footprints

```r
# Compute footprint data for specific TFs
obj <- Footprint(
  object     = obj,
  motif.name = c("IRF8", "BATF::JUN", "SPI1", "ZEB1"),
  genome     = BSgenome.Mmusculus.UCSC.mm10,
  in.peaks   = TRUE,      # CRITICAL for speed — restrict to peaks
  upstream   = 250,
  downstream = 250
)

# Plot, grouped by celltype
p <- PlotFootprint(
  obj,
  features = c("IRF8", "BATF::JUN", "SPI1"),
  group.by = "celltype"
)
p + patchwork::plot_layout(ncol = 1)

ggsave("footprint_profiles.pdf", width = 8, height = 12)
```

## Interpreting Signac Footprint Plots

**Top panel (Observed):**
- Inverted "V" pattern = active TF binding (flanking enrichment + central depletion)
- Flat profile = no evidence of TF occupancy
- Deeper central valley = stronger / more frequent binding

**Bottom panel (Expected / Background):**
- Shows expected Tn5 cutting from sequence bias alone
- Compare observed vs expected to distinguish true footprints from Tn5 preference artifacts

**Comparing conditions:**
- Higher flanking signal + deeper valley = more active binding in that condition
- Similar profiles across conditions = constitutive binding (not condition-specific)

## Output Interpretation

- **Flanking enrichment**: Height of the "shoulders" around the motif center
- **Central depletion**: Depth of the "valley" at position 0 (binding site)
- **Footprint depth**: Difference between shoulder height and valley depth

## Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| `Footprint()` extremely slow | Many TFs × large fragment file | Always set `in.peaks = TRUE`; limit `motif.name` to selected TFs |
| Profiles look identical across groups | Group sizes very imbalanced | Subsample large groups or check `group.by` mapping |
| Empty plot for a TF | Motif not added to object | Re-run `AddMotifs()`; verify TF is in `pwm` set |
| Species mismatch | Wrong JASPAR `species` code | 10090 = mouse, 9606 = human |
| Genome style mismatch | `chr1` vs `1` between fragments and BSgenome | Ensure `seqlevelsStyle()` matches across object and genome |

## Performance Tips

- Use `in.peaks = TRUE` (massive speedup vs whole-genome scan)
- Pre-restrict `motif.name` to the TFs you care about
- Cache the `Footprint()`-augmented object; recomputing per figure is wasteful
- For quantitative differential analysis at scale, switch to `tobias-footprint-bindetect`

## Resources

- **Signac footprint vignette**: https://stuartlab.org/signac/articles/footprint
- **Signac GitHub**: https://github.com/stuart-lab/signac
- **JASPAR 2024**: https://jaspar.elixir.no/

---

## When not to use

- Do not use for quantitative differential binding — Signac Footprint() is visualization-first; use tobias-footprint-bindetect.
- Do not use on very large fragment files for many TFs — slow; restrict with `in.peaks = TRUE` or use TOBIAS.

---

## See also

- `tobias-footprint-bindetect`
- `hint-atac-differential-footprint`
- `signac-chromatin-analysis`

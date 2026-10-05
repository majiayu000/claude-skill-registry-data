---
name: crescendo-scatac-cre-analysis
description: "CREscendo detects differential cis-regulatory element usage within individual scATAC peaks by projecting ENCODE SCREEN cCREs onto peaks and testing Tn5 cleavage per sub-element. Use when peak-level DA is weak and you suspect within-peak shifts. For peak-level DA use Signac/ArchR; for motif activity use chromvar-motif-accessibility."
license: MIT
---

# CREscendo Skill

## What It Does

CREscendo detects **differential CRE usage within peaks** — regulatory changes invisible to peak-level DA.

```
Peak-based DA:   |-------- PEAK --------|  "No difference" (similar total accessibility)
CREscendo:       |CRE1|CRE2|gap|CRE3|CRE4|  CRE3 active in cDC1A, CRE4 in cDC1B
```

**Mechanism:** Projects ENCODE SCREEN cCREs onto your peaks, partitions each peak into CRE segments + non-CRE remainder, counts Tn5 cleavage sites per segment per group, then runs chi-square on the segment x group contingency table. The max-contributing CRE identifies which specific element drives the signal.

CREscendo does NOT discover sub-peaks de novo. It requires an external CRE catalog (ENCODE default: hg38 1,063,878 CREs; mm10 368,121 CREs). Only peaks overlapping 2+ CREs are testable.

## Where It Fits

| Step | Method | Question |
|------|--------|----------|
| Peak DA (B1) | FindMarkers/LR | Is this peak more/less accessible overall? |
| **CRE usage (B3)** | **CREscendo** | **Which element inside this peak changes between groups?** |
| ChromVAR (A3) | Deviation scores | Are motif-associated regions globally more active? |
| Footprinting (B2.5) | Tn5 protection | Is this TF physically bound? |
| Motif enrichment (B2) | hypergeometric | Are DA peaks enriched for specific motifs? |

CRE usage is a **refinement layer** between peak-level DA and mechanistic interpretation. Run it after you have peaks + cell annotations, alongside or after standard DA.

## When Worth It

**High value:**
- Broad peaks (near promoters/TSS clusters) with suspected signal mixing
- Peak DA is weak/ambiguous but biology predicts regulation (e.g., IL-12 response genes)
- DE gene has no nearby DA peak — CRE switching may explain expression change
- Need mechanistic specificity: "which enhancer changed" not "a peak changed"
- Portability: CRE coordinates are stable across datasets (peaks are not)

**Lower value:**
- Tight summit-centered peaks where most signals are already captured by DA
- Broad TF program summaries (ChromVAR/SCENIC+ level)
- ENCODE cCRE catalog is incomplete for your system (rare states, non-model organisms)
- Compute-limited: fragment extraction is the heavy step

## Installation

```r
devtools::install_github("ChenMengjie/CREscendo")
library(CREscendo)
library(Signac)
library(Seurat)
```

## Prerequisites

**Fragment files:** bgzip-compressed + tabix-indexed
```bash
bgzip fragments.tsv && tabix -p bed fragments.tsv.gz
```

**From Signac/Seurat:**
```r
peaks_gr <- granges(seurat_obj@assays$peaks)
peaks_gr <- peaks_gr[grep("chr", seqnames(peaks_gr))]
frag_path <- Fragments(seurat_obj)[[1]]@path
```

## Core Workflow (~1hr total)

### 1. Load CRE Annotations
```r
CRE_gr <- CREscendo:::load_CRE_annotations(genome = "mm10")  # or "hg38"
```

### 2. Cell Annotations
```r
cell_type_list <- c("cDC1A", "cDC1B")
cell_annotation <- data.frame(
  celltype = seurat_obj@active.ident[seurat_obj@active.ident %in% cell_type_list],
  cellname = names(seurat_obj@active.ident[seurat_obj@active.ident %in% cell_type_list])
)
```

### 3. TabixFile Connection
```r
tabix_file <- Rsamtools::TabixFile(file = "fragments.tsv.gz", index = "fragments.tsv.gz.tbi")
open(tabix_file)
```

### 4. Create Object (~25-30 min)
```r
# Mouse (mm10)
cre_obj <- PrepareCREscendoObject(
  peaks_gr, tabix_file, cell_annotation, cell_type_list, CRE_gr,
  tssRegion = c(-1000, 1000),
  TxDb = TxDb.Mmusculus.UCSC.mm10.knownGene,
  annoDb = "org.Mm.eg.db",
  multiCREs = TRUE  # Only peaks with 2+ CREs
)

# Human (hg38)
cre_obj <- PrepareCREscendoObject(
  peaks_gr, tabix_file, cell_annotation, cell_type_list, CRE_gr,
  tssRegion = c(-1000, 1000),
  TxDb = TxDb.Hsapiens.UCSC.hg38.knownGene,
  annoDb = "org.Hs.eg.db",
  multiCREs = TRUE
)
```

### 5. Chi-Square Test (~12-25 min)
```r
# Pairwise comparison
results <- CREtest(cre_obj, celltypes = c("cDC1A", "cDC1B"))

# One vs all
results <- CREtest(cre_obj, celltypes = c("cDC1A"))
```

### 6. Filter & Summarize
```r
summary <- Summarize(results)

filtered <- Filter(results,
  fdr_cutoff = 0.05,
  coverage_cutoff = 100,
  abs_diff_cutoff = 0.2
)
```

### 7. Visualize
```r
Visualize(results, which_peak = "chr1-207335620-207337449")
Visualize(results, which_gene = "CD55")

info <- Extract(results, which_gene = "CD55")
info$peak_annotation
info$plot_contribution
```

## Key Output Columns

| Column | Interpretation |
|--------|----------------|
| `chisq_stat` | Overall differential usage (>2000 very strong, 500-2000 moderate) |
| `fdr` | FDR-adjusted p-value |
| `max_contribution` | % of chi-sq from top CRE (>80% = single driver, ~50% = complex) |
| `max_refID` | Index of top-contributing CRE |
| `max_dif` / `abs_dif` | Frequency difference in top CRE |
| `n_1`, `n_2` | Fragment counts per group |
| `CRE_type` | ENCODE type: PLS (promoter), pELS (proximal enhancer), dELS (distal enhancer), CTCF-bound |
| `SYMBOL` | Nearest gene |

## Downstream Integration

### Compare with DA results
```r
da_peaks <- FindMarkers(seurat_obj, ident.1 = "cDC1A", ident.2 = "cDC1B",
  test.use = 'LR', latent.vars = 'nCount_peaks')

commons <- intersect(rownames(summary), rownames(da_peaks))
combined <- cbind(summary[commons,], da_peaks[commons,])

# Peaks missed by DA but with strong CRE-level signal
missed_by_da <- combined[abs(combined$avg_log2FC) < 1 & combined$chisq_stat > 1000, ]
```

### Feed into motif/footprint analysis
For significant CRE segments:
1. **Motif enrichment** on CRE segments (more specific than whole peaks)
2. **Footprinting** around motifs inside changing CRE segments
3. **Peak-to-gene linking** focused on changing CREs
4. **Overlay with DE genes** — filter for peaks near DE/pathway genes

### Condition-stratified comparisons
Run within a cell type across conditions (e.g., cDC1A_WT vs cDC1A_IL12), not just between cell types. This reveals condition-responsive CRE switching that peak-level DA may miss.

## Limitations

- Only tests peaks containing 2+ CREs (single-CRE or zero-CRE peaks are excluded)
- Constrained by peak caller output (uncalled regions invisible)
- Dependent on ENCODE cCRE catalog quality for your system
- Fragment extraction is compute-heavy (plan ~1hr per comparison)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No CREs found | Check genome version matches (hg38/mm10) |
| Empty results | Verify cell_annotation: 2 cols (celltype, cellname) |
| TabixFile error | Ensure .tbi index exists and path is correct |
| Memory error | Reduce cell_type_list, process chunks |
| Few significant hits | Lower coverage_cutoff, check cell counts (>100 recommended) |

## Quick Checklist

- [ ] Fragment files: bgzip + tabix indexed
- [ ] Genome version matches peaks (hg38/mm10)
- [ ] cell_annotation: 2 columns (celltype, cellname)
- [ ] Sufficient cells per group (>100 recommended)
- [ ] TxDb + annoDb match genome
- [ ] CRE annotations loaded for correct genome

---

## When not to use

- Do not use for standard peak-level differential accessibility. Use Signac/ArchR FindMarkers.
- Do not use on peaks that do not overlap 2+ ENCODE cCREs. CREscendo requires an external CRE catalog for sub-peak segmentation.

---

## See also

- `iterative-peak-merging`
- `chromvar-motif-accessibility`
- `tf-footprint-differential-analysis`
- `scvi-peakvi`

Upstream docs: https://github.com/GreenleafLab/CREscendo

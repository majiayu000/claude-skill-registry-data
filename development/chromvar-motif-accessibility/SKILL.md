---
name: chromvar-motif-accessibility
description: "Bias-corrected per-cell motif accessibility deviation Z-scores from a peaks x cells scATAC matrix via chromVAR (R/Bioconductor) — one number per motif per cell. Use to infer TF activity from ATAC alone, or for differential motif accessibility. It measures potential, not binding: for occupancy use tf-footprint-differential-analysis."
license: MIT
---

# chromVAR: Motif Accessibility Variability Analysis

## Purpose

Identify transcription factor motifs (or other genomic annotations) associated with variability in chromatin accessibility across single cells or bulk ATAC-seq/DNAse-seq samples. Computes bias-corrected deviation scores per motif per cell, enabling TF activity inference without expression data.

**When to use:**
- TF activity inference from scATAC-seq (no RNA required)
- Motif-level differential accessibility between conditions
- Clustering cells by regulatory programs
- De novo motif discovery from kmer analysis
- Motif variability ranking across cell populations

**Upstream:** Peak calling (MACS2/ArchR), fragment counting (ArchR/Signac/getCounts)
**Downstream:** Differential TF activity, clustering, SCENIC+ validation, peak-gene linking

---

## Installation

```r
# Bioconductor (recommended)
BiocManager::install("GreenleafLab/chromVAR")

# Dependencies
BiocManager::install(c("motifmatchr", "JASPAR2020", "BSgenome.Mmusculus.UCSC.mm10"))

# Additional motif collections
devtools::install_github("GreenleafLab/chromVARmotifs")
```

**System requirement:** `gsl` library must be installed (`apt-get install libgsl-dev`).

---

## Core Workflow

```r
library(chromVAR)
library(motifmatchr)
library(BSgenome.Mmusculus.UCSC.mm10)  # or appropriate genome
library(BiocParallel)

# 1. Set parallelization FIRST
register(MulticoreParam(8))  # Unix
# register(SnowParam(workers = 4, type = "SOCK"))  # Windows

# 2. Prepare SummarizedExperiment with counts
#    Input: peaks x cells fragment count matrix
#    Can come from ArchR, Signac, or chromVAR's getCounts()

# 3. Add GC bias (required for background peak matching)
se <- addGCBias(se, genome = BSgenome.Mmusculus.UCSC.mm10)

# 4. Filter samples and peaks
se_filtered <- filterSamples(se, min_depth = 1500,
                             min_in_peaks = 0.15, shiny = FALSE)
se_filtered <- filterPeaks(se_filtered, non_overlapping = TRUE)

# 5. Get motif matches
motifs <- getJasparMotifs(species = "Mus musculus")
motif_ix <- matchMotifs(motifs, se_filtered,
                        genome = BSgenome.Mmusculus.UCSC.mm10)

# 6. Compute deviations (main output)
dev <- computeDeviations(object = se_filtered, annotations = motif_ix)

# 7. Access results
deviations(dev)       # Bias-corrected deviation values
deviationScores(dev)  # Z-scores (preferred for downstream)
```

---

## Input Preparation

### From ArchR Project

```r
library(ArchR)

# Get peak matrix as SummarizedExperiment
peak_matrix <- getMatrixFromProject(proj, useMatrix = "PeakMatrix")

# Convert to chromVAR-compatible format
counts_se <- SummarizedExperiment(
  assays = list(counts = assay(peak_matrix)),
  rowRanges = rowRanges(peak_matrix),
  colData = getCellColData(proj)
)

# Ensure depth column exists
counts_se$depth <- colSums(assay(counts_se))
```

### From Signac/Seurat

```r
library(Signac)

# Extract from ChromatinAssay
atac_assay <- seurat_obj[["ATAC"]]
counts_mat <- GetAssayData(atac_assay, slot = "counts")

# Build SummarizedExperiment
counts_se <- SummarizedExperiment(
  assays = list(counts = counts_mat),
  rowRanges = granges(atac_assay),
  colData = DataFrame(seurat_obj@meta.data)
)
counts_se$depth <- colSums(counts_mat)
```

### From BAM/BED Files (chromVAR native)

```r
# Read peaks (fixed-width 250-500bp recommended)
peaks <- getPeaks("peaks.bed", sort_peaks = TRUE)
# Or from narrowPeak (auto-resizes):
peaks <- readNarrowpeaks("peaks.narrowPeak", width = 500, non_overlapping = TRUE)

# Count fragments
fragment_counts <- getCounts(
  bamfiles,           # Vector of BAM file paths
  peaks,
  paired = TRUE,      # Paired-end ATAC-seq
  by_rg = TRUE,       # Use RG tags for cell barcodes
  format = "bam",
  colData = DataFrame(sample = c("WT", "KO"))
)
```

---

## Critical Parameters

### Peak Requirements
- **Fixed-width, non-overlapping** peaks (250-500bp recommended)
- Method is robust to exact width choice
- Use bulk peaks for single-cell analysis if available
- `filterPeaks(non_overlapping = TRUE)` ensures no overlaps

### Filtering Thresholds
- `min_depth`: Default = max(500, 10% of median library size)
- `min_in_peaks`: Default = 0.5 * median FRiP
- `filterPeaks()`: Removes peaks with zero fragments across all cells

### Motif Matching
- `p.cutoff = 0.00005` (default): Reasonable for human/mouse motifs
- Lower = more stringent, fewer matches per peak
- `matchMotifs(..., out = "scores")`: Returns match count + max score per peak

### Background Peaks
- Matched for GC content and average accessibility
- Default: 50 background iterations
- Control explicitly: `bg <- getBackgroundPeaks(se_filtered, niterations = 50)`

---

## Motif Sources

### JASPAR (built-in)

```r
# Human (default)
motifs <- getJasparMotifs()

# Mouse
motifs <- getJasparMotifs(species = "Mus musculus")

# Other collections: "CORE", "CNE", "PHYLOFACTS", "PBM", "PBM_HOMEO"
motifs <- getJasparMotifs(collection = "CORE")
```

### chromVARmotifs Package

```r
library(chromVARmotifs)
data("human_pwms_v1")   # Curated human PWMs
data("mouse_pwms_v1")   # Curated mouse PWMs
data("homer_pwms")       # HOMER motif database
data("encode_pwms")      # ENCODE motifs
```

### Custom Motifs
Must be `PWMatrixList` or `PFMatrixList` from TFBSTools.

---

## Applications

### Motif Variability Ranking

```r
variability <- computeVariability(dev)
plotVariability(variability, use_plotly = FALSE)

# Top variable motifs
top_motifs <- variability[order(variability$variability, decreasing = TRUE), ]
head(top_motifs, 20)
```

### Differential Accessibility (Between Groups)

```r
# Test per-motif deviation differences between groups
diff_acc <- differentialDeviations(dev, "condition")
# Returns p_value and p_value_adjusted per motif

# Differential variability
diff_var <- differentialVariability(dev, "condition")
```

### Cell Clustering by TF Activity

```r
# Sample correlation from deviations
sample_cor <- getSampleCorrelation(dev)
pheatmap(as.dist(sample_cor),
         annotation_row = as.data.frame(colData(dev)),
         clustering_distance_rows = as.dist(1 - sample_cor),
         clustering_distance_cols = as.dist(1 - sample_cor))

# tSNE on deviations
tsne_results <- deviationsTsne(dev, threshold = 1.5, perplexity = 30)
tsne_plots <- plotDeviationsTsne(dev, tsne_results,
                                 annotation_name = "GATA1",
                                 sample_column = "celltype",
                                 shiny = FALSE)
```

### Kmer Analysis & De Novo Motifs

```r
# Match all 7-mers
kmer_ix <- matchKmers(7, se_filtered, genome = BSgenome.Mmusculus.UCSC.mm10)
kmer_dev <- computeDeviations(se_filtered, kmer_ix)

# Assemble de novo motifs from correlated kmers
de_novos <- assembleKmers(kmer_dev)

# Compare to known motifs
dist_to_known <- pwmDistance(de_novos, motifs)
```

### Motif Synergy

```r
# Test cooperative/competitive binding (slow - use subset of motifs)
synergy <- getAnnotationSynergy(se_filtered, motif_ix[, selected_motifs])
correlation <- getAnnotationCorrelation(se_filtered, motif_ix[, selected_motifs])
```

---

## Alternative Annotations (Non-Motif)

### Genomic Annotations from BED Files

```r
anno_ix <- getAnnotations(
  c("enhancers.bed", "promoters.bed"),
  rowRanges = rowRanges(se_filtered)
)
dev_anno <- computeDeviations(se_filtered, anno_ix)
```

### Cis-Regulatory Groups (Positional)

```r
cis_ix <- getCisGroups(se_filtered, grpsize = 25, stepsize = 10)
dev_cis <- computeDeviations(se_filtered, cis_ix)
```

### Custom Annotation Matrix

```r
# Boolean matrix: peaks x annotations
my_anno <- data.frame(
  enhancers = rowRanges(se_filtered) %over% enhancer_gr,
  promoters = rowRanges(se_filtered) %over% promoter_gr
)
anno_ix <- getAnnotations(my_anno, rowRanges = rowRanges(se_filtered))
```

---

## Integration with Signac/Seurat

```r
# Run chromVAR within Signac
library(Signac)

# Method 1: Signac's RunChromVAR wrapper
seurat_obj <- RunChromVAR(seurat_obj, genome = BSgenome.Mmusculus.UCSC.mm10)
# Stores results in seurat_obj[["chromvar"]] assay

# Method 2: Manual (more control)
# ... prepare se from Seurat as shown above ...
dev <- computeDeviations(se_filtered, motif_ix)

# Add back to Seurat
chromvar_mat <- deviationScores(dev)
seurat_obj[["chromvar"]] <- CreateAssayObject(data = chromvar_mat)
```

---

## Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| `Error in addGCBias` | Wrong genome build | Match genome to peak coordinates (hg38/mm10/mm39) |
| Zero variability | Peaks too few or too filtered | Relax `filterPeaks` threshold; check peak count |
| All deviations ~0 | Homogeneous cell population | Expected if cells are identical; use diverse sample |
| `GO.db` install error | BiocInstaller dependency issue | `BiocManager::install("GO.db")` separately |
| Slow computation | Too many motifs/cells | Reduce motif set; use `MulticoreParam(N)` |
| Memory error | Large sparse matrix | Filter peaks aggressively; reduce `niterations` in `getBackgroundPeaks` |
| Chromosome mismatch | `chr1` vs `1` naming | `seqlevelsStyle(peaks) <- "UCSC"` |

---

## Output Interpretation

- **Deviation**: Bias-corrected difference in accessibility for motif peaks vs expectation. Positive = more accessible than expected.
- **Deviation Z-score**: Statistical significance of deviation. Magnitude correlates with read depth. Use for comparisons.
- **Variability**: SD of Z-scores across cells for a motif. High variability = motif drives cell-to-cell differences.
- **fractionMatches**: Proportion of peaks containing the motif.
- **fractionBackgroundOverlap**: Average fraction of background peaks with motif match (sanity check).

---

## Performance Tips

- Use `MulticoreParam(N)` on Unix for parallelization
- Pre-compute background peaks: `bg <- getBackgroundPeaks(se, niterations = 50)`
- For large datasets (>50k cells): subsample for initial exploration
- 7-mers give better de novo motifs than 6-mers but are slower
- Fixed-width 500bp peaks are a good default for most applications

---

## Resources

- **Publication**: Schep et al., Nature Methods 2017 ([PDF](https://doi.org/10.1038/nmeth.4401))
- **GitHub**: https://github.com/GreenleafLab/chromVAR
- **Documentation**: https://greenleaflab.github.io/chromVAR/
- **motifmatchr**: https://github.com/GreenleafLab/motifmatchr
- **chromVARmotifs**: https://github.com/GreenleafLab/chromVARmotifs

---

## When not to use

- Do not use for TF binding occupancy. chromVAR measures accessibility potential, not physical binding — use tf-footprint-differential-analysis for occupancy.
- Do not use for region-set motif enrichment. Use pycistarget-motif-enrichment.

---

## See also

- `pycistarget-motif-enrichment`
- `tf-footprint-differential-analysis`
- `scvi-peakvi`
- `iterative-peak-merging`

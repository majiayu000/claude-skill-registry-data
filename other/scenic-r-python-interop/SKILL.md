---
name: scenic-r-python-interop
description: R-to-Python data handoff for the SCENIC+ ecosystem (pycisTopic, pycistarget, SCENIC+). Covers Seurat/Signac → pycisTopic count export, cisTopic R → pycisTopic model bridging, existing peak-atlas reuse, and metadata/fragment harmonisation. Use as the bridge skill before any pycisTopic/pycistarget/SCENIC+ run on data originating in R.
license: MIT
---

# SCENIC+ R → Python Data Handoff

## Overview & When to Use

This skill covers all R → Python data conversion scenarios for the SCENIC+ ecosystem (pycisTopic, pycistarget, SCENIC+). Use when:

- Exporting Seurat/Signac ATAC data for pycisTopic topic modeling
- Exporting Seurat RNA data for SCENIC+ GRN inference
- Bridging cisTopic R models to pycisTopic Python
- Using an existing peak atlas (skipping peak calling)
- Harmonizing cell metadata and fragment files between R and Python

**Downstream skills:**
- [pycisTopic](../pycistopic-atac-topic-modeling/SKILL.md) — ATAC topic modeling
- [pycistarget](../pycistarget-motif-enrichment/SKILL.md) — motif enrichment
- [SCENIC+ GRN](../scenic-grn-inference/SKILL.md) — eRegulon inference

---

## Scenario A: Signac → pycisTopic (Count Matrix Export)

**Primary path for Seurat v5 + Signac projects.**

### R Export

```r
library(Seurat)    # v5
library(Signac)
library(anndataR)

# Set active assay to your peak set
DefaultAssay(hub_atac) <- "peaks_hub_filtered"

# Extract count matrix (Seurat v5 uses layer=, not slot=)
peak_matrix <- GetAssayData(hub_atac, layer = "counts")

# Build region names in chr:start-end format
gr <- granges(hub_atac[["peaks_hub_filtered"]])
region_names <- paste0(seqnames(gr), ":", start(gr), "-", end(gr))

# Extract fragment file paths
frag_paths <- sapply(Fragments(hub_atac), function(f) {
  GetFragmentData(f, slot = "path")
})

# Export as h5ad (anndataR handles sparse matrices)
write_h5ad(hub_atac, "B5_atac.h5ad")

# Also export peak set as BED (0-based)
peaks_bed <- data.frame(
  chr   = as.character(seqnames(gr)),
  start = start(gr) - 1,
  end   = end(gr),
  name  = paste0("peak_", seq_along(gr))
)
write.table(peaks_bed, "B5_peak_set.bed",
            sep = "\t", row.names = FALSE, col.names = FALSE, quote = FALSE)

# Export fragment paths
writeLines(frag_paths, "B5_fragment_paths.txt")
```

### Python Import

```python
import anndata as ad
from pycisTopic.cistopic_class import create_cistopic_object

# Load h5ad exported from R
atac_adata = ad.read_h5ad("B5_atac.h5ad")

# pycisTopic expects regions × cells (transpose from anndata cells × regions)
count_matrix = atac_adata.X.T
region_names = list(atac_adata.var_names)
cell_names = list(atac_adata.obs_names)

# Create CistopicObject from pre-counted matrix
cistopic_obj = create_cistopic_object(
    fragment_matrix=count_matrix,
    cell_names=cell_names,
    region_names=region_names,
    tag_cells=False,          # Barcodes already formatted
    project="<dc-project>"
)

# Add cell metadata
cistopic_obj.add_cell_data(atac_adata.obs)
```

> **Note:** `tag_cells=False` skips sample-barcode prepending. Set `True` if barcodes need sample prefixes.

---

## Scenario B: ArchR → pycisTopic

### R Export

```r
library(ArchR)

# Extract peak matrix
peak_mat <- getMatrixFromProject(proj, useMatrix = "PeakMatrix")
count_matrix <- assay(peak_mat)

# Get peak coordinates
peak_set <- getPeakSet(proj)
region_names <- paste0(seqnames(peak_set), ":", start(peak_set), "-", end(peak_set))

# Get fragment paths
frag_paths <- getArrowFiles(proj)

# Export
arrow::write_feather(as.data.frame(summary(count_matrix)), "archR_peak_matrix.feather")
writeLines(region_names, "archR_regions.txt")
```

### Python Import

Follow Scenario A Python import with count_matrix from ArchR export.

---

## Scenario C: cisTopic R → pycisTopic Python (Feather Bridge)

**Skip re-running topic modeling in Python.** From Aertslab FAQ.

### R Export (cisTopic)

```r
library(cisTopic)
library(arrow)

# Export cell-topic probability matrix
write_feather(
  as.data.frame(modelMatSelection(cisTopic_obj, "cell", "Probability")),
  sink = "cell_topic.feather"
)

# Export topic-region probability matrix (all regions)
write_feather(
  as.data.frame(modelMatSelection(cisTopic_obj, "region", "Probability", all.regions = TRUE)),
  sink = "topic_region.feather"
)
```

### Python Import

```python
import pyarrow.feather as feather
import pandas as pd
from pycisTopic.cistopic_class import CistopicObject

# Load feather files
cell_topic = feather.read_feather("cell_topic.feather")
topic_region = feather.read_feather("topic_region.feather")

# Create CistopicObject and attach LDA model
# (Requires existing cistopic_obj with count matrix)
cistopic_obj.add_LDA_model(model)  # from feather data
```

> **Limitation:** This bridge transfers probability matrices only. Re-running LDA in Python may yield better integration with downstream pycistarget/SCENIC+ API.

---

## Scenario D: Existing Peak Atlas (Skip Peak Calling)

**When you already have a consensus peak set (e.g., from A0_peak_atlas_FINAL.rds or hub-filtered atlas).**

### R: Export Peak Atlas

```r
# Load existing peak atlas
atlas <- readRDS("A0_peak_atlas_FINAL.rds")  # GRanges object

# Convert to BED
peaks_bed <- data.frame(
  chr   = as.character(seqnames(atlas)),
  start = start(atlas) - 1,  # BED is 0-based
  end   = end(atlas)
)
write.table(peaks_bed, "peak_atlas.bed",
            sep = "\t", row.names = FALSE, col.names = FALSE, quote = FALSE)
```

### Python: Create cisTopic Object with Existing Peaks

```python
from pycisTopic.cistopic_class import create_cistopic_object_from_fragments

# Use existing peak atlas instead of calling peaks
cistopic_obj = create_cistopic_object_from_fragments(
    path_to_fragments={"sample1": "fragments_s1.tsv.gz",
                       "sample2": "fragments_s2.tsv.gz"},
    path_to_regions="peak_atlas.bed",        # Your pre-built atlas
    path_to_blacklist="mm10_blacklist.bed",
    valid_bc=barcodes_passing_qc
)
```

**Key advantage:** Skips pseudobulk export + MACS peak calling + consensus merging entirely. Proceed directly to LDA topic modeling (Stage 5 in pycisTopic skill).

---

## Scenario E: Seurat RNA → AnnData (Raw Preservation)

**SCENIC+ requires `.raw` to be saved BEFORE normalization.** The R export must preserve raw counts.

### R Export

```r
library(Seurat)    # v5
library(anndataR)

# Ensure RNA assay with counts
DefaultAssay(rna_ref) <- "RNA"

# Standardize metadata
rna_meta <- rna_ref@meta.data
if ("r2_refined" %in% colnames(rna_meta)) {
  rna_meta$celltype <- rna_meta$r2_refined
}

# Create composite label for unpaired SCENIC+ metacells
rna_meta$celltype_condition <- paste0(
  to_file_safe(rna_meta$celltype), "_",
  to_file_safe(rna_meta$condition)
)
rna_ref@meta.data <- rna_meta

# Export (anndataR preserves counts layer)
write_h5ad(rna_ref, "B5_rna.h5ad")
```

### Python: Set .raw Before Normalization

```python
import scanpy as sc

adata = sc.read_h5ad("B5_rna.h5ad")

# CRITICAL: Save raw BEFORE any normalization
adata.raw = adata.copy()

# Standard preprocessing
sc.pp.normalize_total(adata)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata)
sc.pp.scale(adata)
sc.pp.pca(adata)
sc.pp.neighbors(adata)
sc.tl.umap(adata)

# Save processed (with .raw intact)
adata.write("B5_rna_processed.h5ad")
```

---

## Fragment File Harmonization

### Extracting Paths from Signac

```r
# Get fragment paths from Seurat object
frag_objects <- Fragments(hub_atac)
frag_paths <- sapply(frag_objects, function(f) GetFragmentData(f, slot = "path"))

# Verify files exist and have tabix indices
for (fp in frag_paths) {
  stopifnot(file.exists(fp))
  stopifnot(file.exists(paste0(fp, ".tbi")))  # tabix index required
}
```

### Python Fragment Dict

```python
import os

# Read paths exported from R
with open("B5_fragment_paths.txt") as f:
    frag_paths = [l.strip() for l in f if l.strip()]

# Build fragment dict (sample_id → path)
# For single-sample projects:
fragments_dict = {"sample": frag_paths[0]}

# For multi-sample:
fragments_dict = {
    f"AS009_{i+1}": path for i, path in enumerate(frag_paths)
}

# Verify tabix indices
for name, path in fragments_dict.items():
    assert os.path.exists(path), f"Missing: {path}"
    assert os.path.exists(path + ".tbi"), f"Missing index: {path}.tbi"
```

### Sample Tag Format

pycisTopic uses `split_pattern` to separate sample tags from barcodes. Default: `"___"`.

```python
# If barcodes look like "ACGT-1" (Signac default)
# and you want "sample___ACGT-1"
cistopic_obj = create_cistopic_object_from_fragments(
    ..., split_pattern="___"
)
```

---

## Cell Metadata Harmonization

### Column Standardization

```r
# R side: standardize before export
meta <- hub_atac@meta.data
meta$celltype <- meta$r2_refined        # <dc-project> uses r2_refined
meta$condition <- as.character(meta$condition)
meta$barcode <- rownames(meta)

# Composite label for unpaired SCENIC+ metacells
meta$celltype_condition <- paste0(
  to_file_safe(meta$celltype), "_",
  to_file_safe(meta$condition)
)

write.table(meta, "B5_cell_metadata.tsv", sep = "\t",
            row.names = FALSE, quote = FALSE)
```

### Barcode Format Matching

Ensure barcodes match between RNA and ATAC modalities:

```python
# Check barcode overlap
rna_barcodes = set(rna_adata.obs_names)
atac_barcodes = set(cistopic_obj.cell_names)

# For unpaired data, barcodes won't match — that's expected
# SCENIC+ uses metacell approach based on celltype labels instead
overlap = rna_barcodes & atac_barcodes
print(f"Shared barcodes: {len(overlap)}")
print(f"RNA-only: {len(rna_barcodes - atac_barcodes)}")
print(f"ATAC-only: {len(atac_barcodes - rna_barcodes)}")
```

---

## <dc-project> Quick Reference

| Step | R Script | Python Script |
|------|----------|---------------|
| Export | `B5_export_for_scenic.R` | — |
| Topic modeling | — | `B5_run_scenic.py` (Step 2) |
| Motif enrichment | — | `B5_run_scenic.py` (Step 3) |
| SCENIC+ inference | — | `B5_run_scenic.py` (Step 4) |

**Key files produced by R export:**
- `B5_rna.h5ad` — RNA counts + metadata
- `B5_atac.h5ad` — ATAC peak counts + metadata
- `B5_peak_set.bed` — Hub-filtered peak atlas (246k peaks)
- `B5_fragment_paths.txt` — Paths to fragment files
- `B5_cell_metadata.tsv` — Harmonized metadata

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `GetAssayData(slot="counts")` fails | Seurat v5 uses `layer="counts"`, not `slot=` |
| `write_h5ad()` not found | Install `anndataR` package in R |
| Sparse matrix errors in Python | Use `count_matrix.toarray()` or keep scipy.sparse |
| Barcode mismatch (unpaired) | Expected — use `multi_ome_mode=False` in SCENIC+ |
| Region names don't match DB | Ensure chr:start-end format (1-based coords from R) |
| Fragment file missing `.tbi` | Run `tabix -p bed fragments.tsv.gz` |
| `to_file_safe()` not found | Source `config.R` first (<dc-project>-specific) |
| Empty h5ad layers | Check `DefaultAssay()` is set correctly before export |
| Python can't read R-exported h5ad | Update `anndataR` and `anndata` to latest versions |

---

---

## See also

- `pycistopic-atac-topic-modeling` — ATAC topic modeling (Stage 5 uses the cisTopic object from this skill)
- `pycistarget-motif-enrichment` — Motif enrichment on binarized topics
- `scenic-grn-inference` — eRegulon inference (Python API + Snakemake)
- `anndatar-seurat-scanpy-conversion` — General conversion patterns (Seurat ↔ AnnData)
- `multimodal-anndata-mudata` — Multi-assay conversion

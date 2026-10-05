---
name: multimodal-anndata-mudata
description: "Converts multi-assay Seurat objects to AnnData/MuData and explains MuData container semantics for paired, unpaired, and partially paired multi-omics. Use when moving RNA+ATAC or CITE-seq data from Seurat/Signac into scverse, extracting a ChromatinAssay, or setting obs_names for the right pairing semantics."
license: MIT
---

# Multimodal AnnData/MuData: Seurat → Python Conversion for Multi-Omics

## Overview

Convert multi-assay R Seurat objects to Python AnnData/MuData for downstream multimodal analysis. Covers paired (true multiome), unpaired (separate experiments on same cell pool), and partially paired scenarios.

**Key gap this skill fills:** anndataR handles single-assay conversion; this skill covers the multi-assay → MuData pipeline, ChromatinAssay handling, and tool-specific input preparation.

**Prerequisites:**
- [anndataR skill](../anndatar-seurat-scanpy-conversion/SKILL.md) for basic Seurat ↔ h5ad conversion
- [Python multimodal skill](../muon-multimodal-analysis/SKILL.md) for MuData basics
- [Seurat multimodal skill](../seurat-multimodal-analysis/SKILL.md) for R-side analysis

---

## Part 1: MuData Container Patterns

### 1.1 Paired Data (True Multiome)

Same cells have both RNA + ATAC (10x Multiome, matching barcodes).

```python
import mudata as md

mdata = md.MuData({"rna": rna_adata, "atac": atac_adata})
# obs_names match → mdata.n_obs = n_cells (not sum)
# mdata.obsm["rna"] → all True
# mdata.obsm["atac"] → all True
```

### 1.2 Unpaired Data (Separate Experiments)

Different cells for RNA vs ATAC (separate 10x runs, same cell pool).

```python
# CRITICAL: obs_names MUST be different across modalities
rna.obs_names = [f"{bc}_RNA" for bc in rna.obs_names]
atac.obs_names = [f"{bc}_ATAC" for bc in atac.obs_names]

mdata = md.MuData({"rna": rna, "atac": atac})
# mdata.n_obs = n_rna + n_atac (union)
# mdata.obsm["rna"] → True for RNA cells, False for ATAC cells
# mdata.obsm["atac"] → False for RNA cells, True for ATAC cells
```

### 1.3 Partially Paired (Mixed)

Some cells measured by both modalities, others only one.

```python
# Paired cells: IDENTICAL obs_names across modalities
# Unpaired cells: DIFFERENT obs_names
rna.obs_names = ["cell_1", "cell_2", "cell_3_RNA", "cell_4_RNA"]
atac.obs_names = ["cell_1", "cell_2", "cell_5_ATAC", "cell_6_ATAC"]

mdata = md.MuData({"rna": rna, "atac": atac})
# mdata.n_obs = 6 (2 shared + 2 RNA-only + 2 ATAC-only)
```

### 1.4 Axis System

```python
# axis=0 (default): Observations unioned, variables per-modality
# → Standard for RNA + ATAC multi-omics
mdata = md.MuData({"rna": rna, "atac": atac})  # axis=0

# axis=1: Variables shared, observations per-modality (rare)
# axis=-1: Both shared (different views of same data)
```

### 1.5 Boolean Indicators and Index Mapping

```python
# After creating MuData:
mdata.obsm["rna"]   # Boolean: which global obs are in RNA
mdata.obsm["atac"]  # Boolean: which global obs are in ATAC
mdata.obsmap["rna"]  # 1-based index into RNA AnnData (0 = missing)
mdata.obsmap["atac"] # 1-based index into ATAC AnnData (0 = missing)

# After modifying individual modalities, ALWAYS call:
mdata.update()
```

### 1.6 Subsetting and I/O

```python
# Subset MuData (slices across all modalities)
mdata_sub = mdata[cell_list].copy()

# Save/load
mdata.write("multimodal.h5mu")
mdata = md.read("multimodal.h5mu")

# Read individual modality from h5mu (without loading full object)
import muon as mu
rna_only = mu.read("multimodal.h5mu/rna")

# Backed mode for large files
mdata = md.read("multimodal.h5mu", backed=True)
```

---

## Part 2: Seurat Multi-Assay → Python Export

### 2.1 RNA Assay → h5ad

```r
# In R
library(anndataR)

rna_adata <- as_AnnData(seurat_obj,
  assay_name = "RNA",
  x_mapping = "counts",            # Raw counts as X
  layers_mapping = c("data"),       # Normalized as layer
  obs_mapping = TRUE,               # All cell metadata
  obsm_mapping = list(X_pca = "pca", X_umap = "umap")
)
rna_adata$write_h5ad("rna.h5ad")
```

```python
# In Python: verify and prepare for downstream
import scanpy as sc

rna = sc.read_h5ad("rna.h5ad")
assert rna.X.min() >= 0, "X should be raw counts"
rna.layers["counts"] = rna.X.copy()

# For SCENIC+: save raw BEFORE normalization
sc.pp.normalize_total(rna, target_sum=1e4)
sc.pp.log1p(rna)
rna.raw = rna  # CRITICAL for SCENIC+
rna.write_h5ad("rna_preprocessed.h5ad")
```

### 2.2 ChromatinAssay → h5ad (ATAC)

**ChromatinAssay-specific data must be extracted manually before conversion.**

```r
# In R: extract ChromatinAssay metadata BEFORE anndataR conversion
library(Signac)

DefaultAssay(seurat_obj) <- "ATAC"  # or "peaks"

# 1. Extract peak coordinates (GRanges → data.frame)
peak_gr <- granges(seurat_obj[[DefaultAssay(seurat_obj)]])
peak_df <- as.data.frame(peak_gr)
write.csv(peak_df, "peak_coordinates.csv", row.names = TRUE)

# 2. Extract fragment file paths
frag_objs <- Fragments(seurat_obj)
frag_paths <- sapply(frag_objs, function(f) f@path)
writeLines(frag_paths, "fragment_paths.txt")

# 3. Convert ATAC assay (loses ChromatinAssay-specific slots)
atac_adata <- as_AnnData(seurat_obj, assay_name = DefaultAssay(seurat_obj))
atac_adata$write_h5ad("atac_raw.h5ad")
```

```python
# In Python: restore peak coordinates and fragment paths
import scanpy as sc
import pandas as pd

atac = sc.read_h5ad("atac_raw.h5ad")

# Option A: Parse from var_names (if formatted as "chr1-1000-2000")
split = atac.var_names.str.split(r"[-:]")
atac.var["chrom"] = split.map(lambda x: x[0])
atac.var["chromStart"] = split.map(lambda x: int(x[1]))
atac.var["chromEnd"] = split.map(lambda x: int(x[2]))

# Option B: Load from exported CSV
peaks_df = pd.read_csv("peak_coordinates.csv", index_col=0)
atac.var["chrom"] = peaks_df["seqnames"].values
atac.var["chromStart"] = peaks_df["start"].values
atac.var["chromEnd"] = peaks_df["end"].values

# Add fragment file paths
with open("fragment_paths.txt") as f:
    frag_paths = [line.strip() for line in f]
atac.uns["files"] = {"fragments": frag_paths[0] if len(frag_paths) == 1 else frag_paths}

atac.write_h5ad("atac_with_coords.h5ad")
```

### 2.3 What Gets Lost in Conversion

| Seurat Slot | AnnData Equivalent | Status |
|-------------|-------------------|--------|
| Assay counts/data/scale.data | X, layers | Preserved via anndataR |
| meta.data | obs | Preserved |
| reductions (PCA, UMAP, LSI) | obsm | Preserved with mapping |
| ChromatinAssay GRanges | var columns | **LOST** — must export manually |
| Fragment file paths | uns["files"] | **LOST** — must export manually |
| Motif information | — | **LOST** — recompute in Python |
| Neighbor graphs | obsp | Preserved with mapping |
| Variable features | var["highly_variable"] | Preserved |

### 2.4 Separate Objects (Unpaired Scenario)

When RNA and ATAC are in **separate** Seurat objects:

```r
# Export RNA object
rna_adata <- as_AnnData(rna_seurat, assay_name = "RNA",
  x_mapping = "counts", layers_mapping = c("data"))
rna_adata$write_h5ad("rna.h5ad")

# Export ATAC object (with manual peak coord extraction)
# ... (as in 2.2 above)
atac_adata <- as_AnnData(atac_seurat, assay_name = "ATAC")
atac_adata$write_h5ad("atac.h5ad")
```

---

## Part 3: MuData Assembly in Python

### 3.1 Create MuData from Separate h5ad (Unpaired)

```python
import mudata as md
import scanpy as sc

rna = sc.read_h5ad("rna_preprocessed.h5ad")
atac = sc.read_h5ad("atac_with_coords.h5ad")

# Ensure obs_names don't collide (unpaired = different cells)
rna.obs_names = [f"{bc}_RNA" for bc in rna.obs_names]
atac.obs_names = [f"{bc}_ATAC" for bc in atac.obs_names]

# Ensure shared metadata uses same vocabulary
# (cell type labels must match between modalities)
assert set(rna.obs["cell_type"].unique()) & set(atac.obs["cell_type"].unique()), \
    "No shared cell type labels!"

# Create MuData
mdata = md.MuData({"rna": rna, "atac": atac})

# Verify
print(f"Total obs: {mdata.n_obs}")       # Sum of RNA + ATAC cells
print(f"RNA obs: {mdata.mod['rna'].n_obs}")
print(f"ATAC obs: {mdata.mod['atac'].n_obs}")
print(f"RNA indicator sum: {mdata.obsm['rna'].sum()}")
print(f"ATAC indicator sum: {mdata.obsm['atac'].sum()}")

mdata.write("multimodal_unpaired.h5mu")
```

### 3.2 Propagate Shared Metadata to Global obs

```python
# After creating MuData, shared metadata is prefixed:
# mdata.obs has columns like "rna:cell_type", "atac:cell_type"

# To create a unified "cell_type" column:
import numpy as np

mdata.obs["cell_type"] = np.where(
    mdata.obsm["rna"],
    mdata.mod["rna"].obs.reindex(mdata.obs_names)["cell_type"],
    mdata.mod["atac"].obs.reindex(mdata.obs_names)["cell_type"]
)
mdata.update()
```

---

## Part 4: Tool-Specific Input Preparation

### 4.1 For scGLUE (Separate h5ad + Guidance Graph)

scGLUE expects **separate** h5ad files, NOT MuData.

```python
import scglue

# Both need genomic coordinates
scglue.data.get_gene_annotation(rna, gtf="gencode.vM25.gtf.gz", gtf_by="gene_name")
# ATAC: already has chrom/chromStart/chromEnd from Part 2

# Build guidance graph
guidance = scglue.genomics.rna_anchored_guidance_graph(rna, atac)
scglue.graph.check_graph(guidance, [rna, atac])

# Save
rna.write("rna_for_scglue.h5ad")
atac.write("atac_for_scglue.h5ad")
```

See [scGLUE skill](../scglue-unpaired-multiomics-integration/SKILL.md) for full workflow.

### 4.2 For SCENIC+ (h5ad + pycisTopic Pickle)

SCENIC+ creates its own MuData internally via Snakemake. Input requirements:
- scRNA h5ad with `.raw` preserved (before normalization)
- pycisTopic `cistopic_obj.pkl` (from pycisTopic skill)
- Region sets from pycisTopic

```yaml
# SCENIC+ Snakemake config.yaml for unpaired data
input_data:
  cisTopic_obj_fname: "/path/to/cistopic_obj.pkl"
  GEX_anndata_fname: "/path/to/rna_preprocessed.h5ad"
  region_set_folder: "/path/to/region_sets/"

params_data_preparation:
  is_multiome: False
  key_to_group_by: "celltype_condition"  # e.g., "cDC1A_WT"
  nr_cells_per_metacells: 10
  species: "mmusculus"
```

See [SCENIC+ skill](../scenic-grn-inference/SKILL.md) for full workflow.

### 4.3 For MultiVI (Single AnnData with Modality Indicator)

MultiVI expects a single combined AnnData, NOT MuData.

```python
import anndata as ad
import numpy as np

# Concatenate features: [genes | peaks]
# Both modalities must be in one matrix
# RNA-only cells: peaks are zero; ATAC-only cells: genes are zero
combined = ad.concat([rna, atac], join="outer", merge="first")
combined.var["modality"] = (
    ["Gene Expression"] * rna.n_vars + ["Peaks"] * atac.n_vars
)
combined.layers["counts"] = combined.X.copy()
```

See [MultiVI skill](../scvi-multivi/SKILL.md) for full workflow.

### 4.4 Decision Tree: Which Format for Which Tool

```
Which tool?
├─ scGLUE       → Separate h5ad files + guidance graph (NetworkX)
├─ SCENIC+      → h5ad (RNA) + pycisTopic pkl (ATAC); Snakemake handles MuData
├─ MultiVI      → Single AnnData with [genes | peaks] columns
├─ muon WNN     → MuData h5mu (both modalities)
└─ General use  → MuData h5mu (most flexible container)
```

---

## Part 5: Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Barcode collision in unpaired MuData | Add `_RNA`/`_ATAC` suffixes to obs_names |
| ChromatinAssay metadata lost | Export peak coords + fragment paths separately before conversion |
| No MuData support in R | assemble MuData in Python after exporting h5ad from R |
| anndataR only converts one assay | Call `as_AnnData()` separately for each assay |
| Cell type labels don't match | Harmonize annotation vocabulary before export |
| Missing raw counts for SCENIC+ | Set `x_mapping = "counts"` in anndataR; save `.raw` in Python |
| `mdata.update()` forgotten | Always call after modifying individual modalities |
| Peak coordinates column names wrong | scGLUE requires: `chrom`, `chromStart`, `chromEnd` (BED format) |

---

## Cross-References

- **Basic Seurat ↔ h5ad:** [anndataR skill](../anndatar-seurat-scanpy-conversion/SKILL.md)
- **Python MuData ecosystem:** [Python multimodal skill](../muon-multimodal-analysis/SKILL.md)
- **R multimodal (Seurat/Signac):** [Seurat multimodal skill](../seurat-multimodal-analysis/SKILL.md)
- **Unpaired integration (scGLUE):** [scGLUE skill](../scglue-unpaired-multiomics-integration/SKILL.md)
- **GRN inference (SCENIC+):** [SCENIC+ skill](../scenic-grn-inference/SKILL.md)
- **Joint RNA+ATAC modeling:** [MultiVI skill](../scvi-multivi/SKILL.md)

---

## Resources

- **MuData docs:** https://mudata.readthedocs.io/
- **muon docs:** https://muon.readthedocs.io/
- **anndataR (Bioconductor):** https://bioconductor.org/packages/release/bioc/html/anndataR.html
- **scverse MuData axes tutorial:** https://scverse-tutorials.readthedocs.io/en/latest/notebooks/tutorial_axes_anndata_mudata.html
- **h5mu file format spec:** https://mudata.readthedocs.io/en/latest/io/h5mu.html

---

## When not to use

- Do not use for single-assay Seurat conversion. Use anndatar-seurat-scanpy-conversion instead.
- Do not use for downstream multimodal analysis in Python. Use muon-multimodal-analysis.

---

## See also

- `anndatar-seurat-scanpy-conversion`
- `muon-multimodal-analysis`
- `seurat-multimodal-analysis`

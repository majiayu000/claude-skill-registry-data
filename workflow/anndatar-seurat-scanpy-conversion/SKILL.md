---
name: anndatar-seurat-scanpy-conversion
description: Convert between AnnData (.h5ad, Python/scverse) and Seurat (.rds, R/Seurat5) using the modern anndataR API. Use when bridging R and Python workflows, loading .h5ad in R, or exporting a Seurat object to scverse. For multi-assay / multimodal containers (CITE-seq, multiome) use multimodal-anndata-mudata. For Seurat→Loupe use louper-seurat-conversion.
license: MIT
---

# anndataR: Seurat ↔ h5ad Conversion Skill

## Purpose
Convert h5ad <-> Seurat using modern anndataR API

## Quick Reference

### Read h5ad → Seurat
```r
library(anndataR)
library(Seurat)

# Direct read
seurat <- read_h5ad("file.h5ad", as = "Seurat")

# Two-step (for customization)
adata <- read_h5ad("file.h5ad")
seurat <- adata$as_Seurat()
```

### Write Seurat → h5ad
```r
# Direct write
write_h5ad(seurat, "output.h5ad")

# Two-step (for customization)
adata <- as_AnnData(seurat)
adata$write_h5ad("output.h5ad")
```

## Custom Mapping
```r
# Read with mapping
seurat <- adata$as_Seurat(
  layers_mapping = c("counts", "dense_counts"),  # which layers to include
  object_metadata_mapping = c(new_name = "obs_column"),
  reduction_mapping = list(
    pca = c(key = "PC_", embeddings = "X_pca", loadings = "PCs")
  ),
  graph_mapping = TRUE  # or FALSE to skip
)
# NOTE — reduction key format: the key string (e.g. "PC_") must be purely alphanumeric
# with a trailing underscore (e.g. "umapunsup_"), NOT "umap_unsup_" or "umap.unsup_".
# Embedded underscores or dots in the key fragment corrupt the resulting dimension column
# names (e.g. "umap_unsup_1" splits incorrectly). The reduction SLOT NAME (e.g. "umap.unsup")
# may contain dots — only the key is restricted.

# Write with mapping
adata <- as_AnnData(seurat,
  x_mapping = "counts",  # main assay layer
  layers_mapping = c("data"),  # additional layers
  obs_mapping = c(cell_type = "celltype"),  # metadata
  obsm_mapping = list(X_pca = "pca", X_umap = "umap")  # reductions
)
```

## Structure Mapping
**Key difference: matrices are TRANSPOSED**
- AnnData: cells × genes (obs × var)
- Seurat: genes × cells (features × samples)

```
AnnData          →  Seurat
X                →  Assay layer (data/counts)
obs              →  meta.data (columns)
var              →  feature metadata
obsm (X_pca)     →  reductions (pca@cell.embeddings)
varm (PCs)       →  reductions (pca@feature.loadings)
obsp             →  graphs
uns              →  misc
layers           →  assay layers
```

## Common Issues & Solutions

### 1. Memory Issues (large files)
```r
# Use HDF5-backed for reading
adata <- read_h5ad("big.h5ad", as = "HDF5AnnData")
# Process in chunks/subsets before converting
subset <- adata[1:1000, ]
seurat <- subset$as_Seurat()
```

### 2. Missing Metadata After Conversion
```r
# Check what's available
names(adata$obs)  # cell metadata
names(adata$var)  # gene metadata
names(adata$uns)  # unstructured data

# Explicitly map
seurat <- adata$as_Seurat(
  object_metadata_mapping = c("leiden", "cell_type", "batch")
)
```

### 3. R Version Error
```r
# Requires R >= 4.5.0
getRversion()  # check version
# If < 4.5.0, install dependencies may fail
```

### 4. Layer/Assay Confusion
```r
# List available layers
names(adata$layers)
# ["counts", "data", "scale.data"]

# Specify which to convert
seurat <- adata$as_Seurat(layers_mapping = c("counts", "data"))
```

### 5. Sparse Matrix Handling
```r
# anndataR handles sparse automatically
# But check if preserved:
class(seurat[["RNA"]]$counts)  # dgCMatrix for sparse
```

### 6. Ensembl IDs as rownames (var_names round-trip)

`read_h5ad(as = "Seurat")` preserves whatever `var_names` the upstream h5ad has — **including Ensembl IDs** when the producing scanpy pipeline used `var_names_strategy = "ensembl"`. The symptom: `FeaturePlot("Xbp1")` returns "feature not found" because rownames are `ENSMUSG…`. The `var/gene_name` column is in the h5ad but NOT carried into the Seurat assay's `@meta.data`.

**Quick detection:**
```r
head(rownames(obj))                   # ENSMUSG... → quirk present
"Xbp1" %in% rownames(obj)             # FALSE → biologist queries fail
colnames(obj[["RNA"]]@meta.data)      # only var.features / var.features.rank → no gene_name
```

**Fix:** read the same h5ad as a `SingleCellExperiment` (which DOES carry `var` into `rowData`), pull `gene_name`, sum-collapse counts on duplicate symbols, re-derive `data` via `NormalizeData()` (do not collapse log-normalized values in place — `log(a+b) ≠ log(a) + log(b)`).

Full recipe — including HVG handling, scale.data + PCA-loading rename, and the reasons not to recompute PCA — at [`references/ensembl-vs-symbol-rownames.md`](references/ensembl-vs-symbol-rownames.md).

**When to skip as_Seurat():** if the h5ad was pre-finalized (symbols as var_names, Ensembl in
var['gene_id'], lognorm X, raw counts layer), the two-source collapse is unnecessary — build manually:

```r
adata  <- read_h5ad("finalized.h5ad")
genes  <- as.character(adata$var_names)   # already symbols
cells  <- as.character(adata$obs_names)
to_gc  <- function(m) { m <- as(Matrix::t(m), "CsparseMatrix"); rownames(m) <- genes; colnames(m) <- cells; m }
counts <- to_gc(adata$layers[["counts"]])
data   <- to_gc(adata$X)
rna    <- CreateAssay5Object(counts = counts); LayerData(rna, "data") <- data
obj    <- CreateSeuratObject(counts = rna, meta.data = `rownames<-`(as.data.frame(adata$obs), cells))
```
This guarantees h5ad/rds identity and sidesteps as_Seurat() version differences.

### 7. Seurat5 feature metadata requires a NAMED vector

Assigning a plain vector to an assay's feature metadata errors with
"No feature overlap between new meta data and assay". The value must be a
NAMED vector whose names equal rownames(assay):

```r
# Fails: "No feature overlap between new meta data and assay"
assay[["gene_id"]] <- var_df$gene_id

# Works: names must equal rownames(assay)
feat <- rownames(assay)
assay[["gene_id"]]   <- setNames(var_df[feat, "gene_id"],   feat)
assay[["gene_name"]] <- setNames(var_df[feat, "gene_name"], feat)
obj[["RNA"]] <- assay   # re-attach after modifying the assay
```

For the full production pattern — both ids in native slots, the HVG-subset trap, and raw-counts
alignment — see [§Producing a fully Seurat-native .rds](#producing-a-fully-seurat-native-rds-carrying-both-gene-ids) below.


## Producing a fully Seurat-native .rds carrying BOTH gene ids

The pattern above renames rows to symbols. But a deliverable `.rds` should carry **both** identifiers in Seurat-native, discoverable slots so no downstream consumer has to re-read the h5ad. This is a validated production pattern (PanSci `02_analysis/helpers/convert_ops.R`). Target layout, Seurat v5 / Assay5:

- **Active feature id = gene SYMBOL** → the assay rownames (what `FeaturePlot`/`VlnPlot` query). Ensembl is the *secondary* id.
- **Both ids live in the RNA assay's feature-level metadata** — the native, discoverable location — attached via the standard accessor `obj[["RNA"]][[]] <- fm`.
- The same table is *also* stashed in `obj@misc$gene_metadata` as a convenience (survives operations that reset feature meta.data), but the assay feature metadata is the authoritative Seurat-native home.

### Attaching feature metadata the right way (and the pitfall)

```r
# fm: a data.frame, one row per feature, row.names == the ACTIVE feature names
# (the sanitized symbols that are the object's rownames), columns e.g.
# gene_name, gene_id (Ensembl), gene_type.
fm <- gene_meta_df
rownames(fm) <- rownames(obj)          # MUST equal the active features
obj[["RNA"]][[]] <- fm                  # attaches all columns at once
head(obj[["RNA"]][[]])                   # queryable the standard way
obj[["RNA"]][["gene_id"]]                # single column, as a 1-col data.frame
```

**Pitfall — "No feature overlap":** assigning a *bare, unnamed vector* to a single
feature-meta column fails, because Seurat aligns feature metadata by name:

```r
obj[["RNA"]][["gene_id"]] <- ensembl_vector          # ERROR: No feature overlap
```

Fix — pass a *named* vector (names == features) or a data.frame whose rownames match:

```r
names(ensembl_vector) <- rownames(obj)
obj[["RNA"]][["gene_id"]] <- ensembl_vector          # OK
# or, preferred for several columns at once:
obj[["RNA"]][[]] <- fm                                # fm rownames == features
```

Also stash the convenience copy:

```r
obj@misc$gene_metadata <- fm
```

### The HVG-subset trap (source gene metadata from `raw/var`, not main `var`)

A very common upstream shape: the h5ad's **main `var` is an HVG subset** (e.g.
3000–5000 genes) while the **counts matrix + rownames span the full gene space**
(~55k genes, held in `raw/`). If you source the gene annotation from the truncated
main `var`, ~50k features silently lose their Ensembl id (and everything else). The
gene metadata MUST come from the **full `raw/var` group**, aligned to
`raw/var/_index`, so every feature is annotated 1:1.

Read `raw/var` columns via `hdf5r`, decoding categorical columns
(`categories` + `codes`), aligned to the counts rownames:

```r
library(hdf5r)

extract_gene_metadata <- function(h5path,
                                   want = c("gene_name", "gene_id", "gene_type")) {
  f <- H5File$new(h5path, "r"); on.exit(f$close_all(), add = TRUE)
  vgrp  <- "raw/var"                       # FULL gene space, not "var" (HVG subset)
  syms  <- as.character(f[["raw/var/_index"]]$read())

  read_col <- function(col) {
    p <- file.path(vgrp, col)
    if (!f$exists(p)) return(NULL)
    o <- f[[p]]
    if (inherits(o, "H5Group")) {          # categorical: categories + integer codes
      cats  <- as.character(o[["categories"]]$read())
      codes <- as.integer(o[["codes"]]$read())
      out <- cats[codes + 1L]; out[codes < 0L] <- NA   # AnnData codes are 0-based; -1 = NA
      out
    } else o$read()
  }
  cols <- Filter(Negate(is.null), setNames(lapply(want, read_col), want))
  if (!length(cols)) return(NULL)
  gm <- as.data.frame(cols, stringsAsFactors = FALSE, check.names = FALSE)
  rownames(gm) <- make.unique(syms)        # same keys as the counts rownames
  gm
}
```

`make.unique(syms)` matches the row keys `read_raw_counts()` assigns below, so the
table aligns 1:1 to the full feature set.

### Raw counts, X, and the sanitized-name alignment

anndataR 1.0.2 **ignores the nested `.raw` group**, so read raw counts straight from
the h5ad's `raw/X` CSR group via `hdf5r`; the log-normalized `adata.X` (which
anndataR *does* read) becomes the `data` layer. `CreateSeuratObject` sanitizes
feature names (`_` → `-`), so re-derive every layer's rownames from the object.

```r
library(anndataR); library(Seurat); library(Matrix); library(hdf5r)

read_raw_counts <- function(h5path, cells) {         # genes x cells (dgCMatrix)
  f <- H5File$new(h5path, "r"); on.exit(f$close_all(), add = TRUE)
  data    <- f[["raw/X/data"]]$read()
  indices <- f[["raw/X/indices"]]$read()
  indptr  <- f[["raw/X/indptr"]]$read()
  genes   <- as.character(f[["raw/var/_index"]]$read())
  # raw/X is CSR over cells (rows); build cells x genes then transpose.
  m_cg <- new("dgRMatrix", p = as.integer(indptr), j = as.integer(indices),
              x = as.numeric(data), Dim = as.integer(c(length(cells), length(genes))))
  counts <- as(Matrix::t(m_cg), "CsparseMatrix")
  rownames(counts) <- make.unique(genes); colnames(counts) <- cells
  counts
}

adata  <- read_h5ad(h5path)
cells  <- as.character(adata$obs_names)
counts <- read_raw_counts(h5path, cells)
obs    <- as.data.frame(adata$obs); rownames(obs) <- cells

obj   <- CreateSeuratObject(counts = counts, meta.data = obs)
feats <- rownames(obj)                                # SANITIZED names (_ -> -)

# gene metadata from the FULL gene space -> both native locations
gm <- extract_gene_metadata(h5path)
if (!is.null(gm) && nrow(gm) == length(feats)) {
  fm <- gm; rownames(fm) <- feats
  obj[["RNA"]][[]] <- fm                              # native, discoverable
  obj@misc$gene_metadata <- fm                        # convenience copy
}

# log-norm X -> data layer, aligned to the SAME sanitized feature names
X <- adata$X
if (!is.null(X) && length(X@x) > 0 && max(X@x) > 0 && ncol(X) == length(feats)) {
  data_mat <- as(Matrix::t(X), "CsparseMatrix")       # genes x cells
  rownames(data_mat) <- feats; colnames(data_mat) <- cells
  obj[["RNA"]]$data <- data_mat
}
```

If the upstream `var_names` are Ensembl (not symbols) you must additionally rename
rows to symbols and sum-collapse duplicate symbols on `counts` first — see the two
conventions below and [`references/ensembl-vs-symbol-rownames.md`](references/ensembl-vs-symbol-rownames.md).

### Loupe caveat

If you also export a `.cloupe` from this object, loupeR caps a categorical grouping
at **32768 groups** — never pass a per-cell factor (one level per cell) as a
"cluster"; it is rejected for any object larger than that and is useless for
browsing anyway. See [louper-seurat-conversion](../louper-seurat-conversion/SKILL.md).

## Inspection
```r
# AnnData structure
adata
dim(adata)
names(adata$obs)      # cell metadata columns
names(adata$var)      # gene metadata columns
names(adata$obsm)     # embeddings (PCA, UMAP)
names(adata$layers)   # data layers

# Seurat structure
seurat
dim(seurat)
colnames(seurat@meta.data)  # cell metadata
Reductions(seurat)          # PCA, UMAP
Layers(seurat)              # data layers
```

## Subsetting (creates views)
```r
# Subset by condition (lazy evaluation)
subset <- adata[adata$obs$cell_type == "T cell", ]

# Convert view to concrete
concrete <- subset$as_InMemoryAnnData()

# Then convert to Seurat
seurat <- concrete$as_Seurat()
```

## Installation
```r
# Install anndataR
BiocManager::install("anndataR")

# With all dependencies
install.packages("pak")
pak::pak("scverse/anndataR", dependencies = TRUE)
```

**Version note:** this skill targets anndataR >= 1.1.0. On R 4.4.x, `BiocManager::install('anndataR')`
may resolve 1.0.2, which has different `as_Seurat()` parameter names. Check with
`packageVersion('anndataR')`; if locked to 1.0.2, use the manual build pattern described in Issue 6.

## Multi-Assay / Multimodal Conversion

anndataR converts **one assay at a time**. For multi-assay Seurat objects (RNA + ATAC, CITE-seq), export each assay separately and assemble in Python.

### Quick Path
```r
# Export each assay
rna_adata <- as_AnnData(seurat_obj, assay_name = "RNA", x_mapping = "counts")
rna_adata$write_h5ad("rna.h5ad")

atac_adata <- as_AnnData(seurat_obj, assay_name = "ATAC")
atac_adata$write_h5ad("atac.h5ad")
```

```python
# Assemble in Python
import mudata as md
rna = sc.read_h5ad("rna.h5ad")
atac = sc.read_h5ad("atac.h5ad")
mdata = md.MuData({"rna": rna, "atac": atac})
```

### ChromatinAssay Warning

Signac's ChromatinAssay has extra slots (peak GRanges, fragment file paths) that are **lost** during anndataR conversion. Extract these manually before converting.

**For full multi-assay conversion workflow, see [multimodal-anndata-mudata.md](../multimodal-anndata-mudata/SKILL.md).**

---

## Debug Checklist
1. Check R version: `getRversion() >= "4.5.0"`
2. Verify file exists: `file.exists("file.h5ad")`
3. Check structure: `adata` (print object)
4. List available slots: `names(adata$obs)`, `names(adata$obsm)`
5. Test small subset first: `adata[1:100, 1:500]`
6. Check memory: `pryr::object_size(seurat)`
7. Validate conversion: compare dimensions, metadata columns

---

## When not to use

- Do not use for multi-assay Seurat objects (CITE-seq, multiome). Use multimodal-anndata-mudata.
- Do not use the older SeuratDisk API. This skill uses modern anndataR.
- Do not pass AnnData X layer name when calling as_Seurat — pass layer NAMES only (e.g., c('counts')).

---

## See also

- `anndata`
- `multimodal-anndata-mudata`
- `louper-seurat-conversion`

Upstream docs: https://scverse.org/anndataR/

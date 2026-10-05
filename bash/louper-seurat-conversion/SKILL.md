---
name: louper-seurat-conversion
description: "Convert AnnData (.h5ad) to 10x Loupe Browser (.cloupe) via Seurat, using loupeR and anndataR. Use when sharing scRNA-seq data with collaborators who prefer Loupe Browser, or generating .cloupe from non-10x data (needs cellid_ barcode format). For R/Python round-tripping without Loupe export use anndatar-seurat-scanpy-conversion."
license: MIT
---

# loupeR — h5ad → Seurat → Loupe Browser

**Tested against:** loupeR 1.1.5 · anndataR 1.1.0 · Seurat 5.2.1 · R 4.5.0

---

## Purpose

Convert an AnnData `.h5ad` file to a 10x Loupe Browser `.cloupe` file via anndataR
(h5ad → Seurat) and loupeR (Seurat → .cloupe).

Use `create_loupe_from_seurat()` for standard 10x data with ACGT-16 barcodes.
Use `create_loupe()` directly for custom data (non-10x barcodes, explicit projections).
See `scripts/h5ad_to_seurat_to_loupe.R` in this skill for a generalized reference
script covering both barcode paths.

---

## Quick Reference

```r
library(anndataR); library(Seurat); library(loupeR)

# h5ad → Seurat
adata  <- read_h5ad("input.h5ad")
seurat <- adata$as_Seurat(layers_mapping = c("counts", "scvi_normalized"))

# Seurat → .cloupe (simple path, 10x ACGT barcodes only)
create_loupe_from_seurat(seurat, output_dir = "results/loupe", output_name = "export")

# Seurat → .cloupe (full control)
create_loupe(
  count_mat   = counts_mat,      # NOTE: argument is count_mat, NOT counts
  clusters    = clusters_list,
  projections = projections_list,
  output_dir  = "results/loupe",
  output_name = "export"
)
```

---

## Critical Gotchas (all verified v1.1.5)

### 1. `create_loupe()` argument is `count_mat`, not `counts`

The raw count matrix argument changed between versions. In v1.1.5 it is `count_mat`.
Using `counts =` silently fails or errors.

```r
# WRONG (old API / wrong guess)
create_loupe(counts = mat, ...)

# CORRECT
create_loupe(count_mat = mat, ...)
```

### 2. `validate_barcodes()` returns a list, not a boolean

The return value is `list($success, $msg)`. Using it as a boolean crashes.

```r
# WRONG
if (validate_barcodes(barcodes)) { ... }

# CORRECT
check <- validate_barcodes(barcodes)
if (isTRUE(check$success)) {
  cat("Valid\n")
} else {
  stop("Barcodes invalid: ", check$msg)
}
```

### 3. `force = TRUE` does NOT bypass the barcode whitelist

`force = TRUE` only skips the output-file overwrite check. It does **not** bypass the
louper binary's internal barcode validation. If your barcodes are unrecognised, the
binary will hard-fail regardless of `force = TRUE`.

### 4. Non-10x barcodes require `cellid_XXXXXXXXX` format

Custom / project-internal barcodes (e.g. `dcverse_RHP4930_2`) are not in any format
loupeR accepts. Use the Loupe-native `cellid_` format for all non-10x data:

```r
loupe_barcodes <- sprintf("cellid_%09d", seq_len(ncol(seurat)))
# e.g. "cellid_000000001", "cellid_000000002", ...

# Validate before calling create_loupe()
check <- validate_barcodes(loupe_barcodes)
if (!isTRUE(check$success)) stop(check$msg)
```

Always preserve the original IDs as a cluster metadata column so cells remain
traceable in the Loupe Browser.

### 5. Empty-string `""` category values crash the louper binary

NA or empty-string `""` levels in a cluster factor cause a hard failure in the louper
binary with no informative R error. Recode before building the clusters list. (We hit
this on `treearches_status` / `novel_subcluster`, which carry empty strings for
unassigned cells.)

```r
chr <- as.character(val)
chr[is.na(chr) | chr == ""] <- "unassigned"
fac <- factor(chr)
names(fac) <- loupe_barcodes
clusters[[col]] <- fac
```

### 6. EULA acceptance blocks headless / CI runs

`loupeR::setup()` prompts for interactive 10x EULA acceptance on first run; in
non-interactive shells (Rscript, CI, devcontainers) it blocks forever. Set the env var
before setup():

```r
Sys.setenv(AUTO_ACCEPT_EULA = "true")
loupeR::setup()
```

Or from the shell: `AUTO_ACCEPT_EULA=true Rscript your_export.R`. (This accepts the
10x EULA at https://10xgen.com/EULA programmatically — be aware you are agreeing on
the user's behalf.)

---

## Barcode Formats

| Format | Pattern | Example | Notes |
|--------|---------|---------|-------|
| 10x ACGT-16 | `[ACGT]{16}(-1)?` | `ACGTACGTACGTACGT-1` | Standard 10x output |
| 10x with prefix | `\w+_[ACGT]{16}(-1)?` | `sample1_ACGTACGT...` | Multi-sample |
| 10x with suffix | `[ACGT]{16}(-1)?_\w+` | `ACGTACGT..._lib` | Multi-library |
| cellid (custom) | `cellid_[0-9]+` | `cellid_000000001` | **Use for non-10x data** |

Unrecognised formats cause a hard fail in the louper binary.

---

## Layer Mapping: AnnData → Seurat

```r
# Pass AnnData layer NAMES only (not "X")
seurat <- adata$as_Seurat(layers_mapping = c("counts", "scvi_normalized"))
```

| AnnData slot | Seurat layer name | Content |
|---|---|---|
| `layers["counts"]` | `counts` | Raw integer UMI |
| `layers["scvi_normalized"]` | `scvi_normalized` | scVI log-normalized floats |
| `X` (float32) | `X` | Auto-added; same values as scvi_normalized |

**Note:** anndataR auto-converts **all** `obsm` entries to Seurat reductions, including
internal scVI metadata keys like `_scvi_extra_categorical_covs`. Expect extra
reductions you didn't ask for. Add clean `umap` / `scvi` keys explicitly if needed.

---

## Dependencies

```r
install.packages("remotes")
remotes::install_github("10XGenomics/loupeR")

# System requirement: HDF5 must be installed at the OS level
# Ubuntu/Debian: sudo apt-get install libhdf5-dev
# macOS:         brew install hdf5
```

loupeR ≥1.1.5 requires Loupe Browser ≥8.1.

---

## Ensembl IDs

Seurat drops Ensembl IDs during import; gene links in Loupe Browser won't work without
them. To preserve:

```r
feature_ids <- read_feature_ids_from_tsv("path/to/features.tsv.gz")
create_loupe_from_seurat(seurat, feature_ids = feature_ids, ...)
```

---

## Reference Script

`scripts/h5ad_to_seurat_to_loupe.R` — generalized, configurable version of a
production export script. Covers:
- Configurable input/output paths
- Barcode auto-detection with `cellid_` fallback
- Parameterised layer names and cluster columns
- Configurable UMAP obsm key
- Cell ID traceability pattern

---

## When not to use

- Do not use create_loupe() with argument name 'counts' — v1.1.5 expects 'count_mat'.
- Do not pass non-10x barcodes unchanged. Use cellid_XXXXXXXXX format.
- Do not rely on force=TRUE to bypass barcode validation — it only skips output-file overwrite.

---

## See also

- `anndatar-seurat-scanpy-conversion`
- `anndata`

Upstream docs: https://github.com/10XGenomics/loupeR

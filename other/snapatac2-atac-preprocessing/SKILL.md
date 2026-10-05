---
name: snapatac2-atac-preprocessing
description: "SnapATAC2 — fast scATAC preprocessing (fragment import, QC, feature selection, spectral embedding, peak calling, gene activity). Use when starting from a 10x fragments.tsv.gz or a binarised peak matrix and you need cells embedded for clustering or joint multiomic analysis. For differential accessibility next use atac-differential-accessibility."
license: MIT
---

# SnapATAC2 scATAC-seq Preprocessing

## Overview

SnapATAC2 is the scverse-aligned Python pipeline for scATAC-seq: it imports
fragment files, computes QC, selects features, builds spectral embeddings,
calls peaks, and computes gene-activity matrices. The end product is an
AnnData (or peak matrix file) ready for clustering, batch correction, and
joint RNA+ATAC analysis under `muon-multimodal-analysis`.

**When to reach for this skill:**
- You have `fragments.tsv.gz` (from Cell Ranger ARC, Cell Ranger ATAC, or
  manual processing) and need a per-cell embedding.
- You need to switch the dimensionality reduction off PCA onto spectral
  embedding (preferred for sparse binary ATAC data).
- You need TSS-enrichment QC computed against a known genome assembly.

**Pre-reqs:**
- Linux / macOS with `pip install snapatac2 episcanpy`
- For peak calling: `macs2` (Python or CLI) on `$PATH`

---

## Part 1 — Fragment import & cell-level QC

```python
import snapatac2 as snap

# Read fragment file directly into AnnData
adata_atac = snap.pp.import_data(
    fragment_file="atac_fragments.tsv.gz",
    chrom_sizes=snap.genome.hg38,           # or snap.genome.mm10
    sorted_by_barcode=False,
    min_num_fragments=500,
    max_num_fragments=100000,
)

# Or read from existing MuData/AnnData
adata_atac = mdata.mod["atac"]
```

### QC metrics

```python
# TSS enrichment — gold-standard QC for ATAC
snap.metrics.tsse(adata_atac, snap.genome.hg38)

# Fragment size distribution (nucleosomal periodicity)
snap.metrics.frag_size_distr(adata_atac)
snap.pl.frag_size_distr(adata_atac)

# Filter cells: count window + TSS enrichment threshold
snap.pp.filter_cells(
    adata_atac,
    min_counts=1000,
    max_counts=100000,
    min_tsse=2,    # TSS enrichment > 2 is the conventional minimum
)
```

---

## Part 2 — Peak calling & peak matrix

```python
# De novo peak calling (requires macs2 installed)
snap.pp.make_peak_matrix(
    adata_atac,
    file="peaks.h5ad",          # output file (snapatac2 writes lazily)
    peak_file=None,             # None = call peaks de novo
    use_rep="X_spectral"        # group cells by spectral embedding
)

# Or quantify against a pre-existing peak set (e.g. ENCODE cCREs)
snap.pp.make_peak_matrix(
    adata_atac,
    file="peaks.h5ad",
    peak_file="peaks.bed",
)
```

---

## Part 3 — TF-IDF + LSI (alternative to spectral)

When you need a depth-aware transform compatible with downstream Harmony /
Seurat workflows, use TF-IDF + LSI instead of spectral.

```python
import episcanpy as epi
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD
import pandas as pd
import numpy as np

atac = mdata.mod["atac"]

# Binarise the matrix (presence/absence)
atac.X = (atac.X > 0).astype(float)

# TF-IDF normalisation
epi.pp.tfidf(atac)
# (or manual): tfidf = TfidfTransformer(norm="l2", use_idf=True)
# atac.X = tfidf.fit_transform(atac.X)

# LSI = truncated SVD on the TF-IDF matrix
lsi = TruncatedSVD(n_components=50, random_state=0)
atac.obsm["X_lsi"] = lsi.fit_transform(atac.X)

# CRITICAL: LSI component 1 frequently correlates with sequencing depth.
# Always check and drop it from downstream if so.
corr = pd.Series(atac.obsm["X_lsi"][:, 0]).corr(
    pd.Series(np.array(atac.X.sum(axis=1)).flatten())
)
print(f"LSI1 vs depth: r = {corr:.3f}")
# If |corr| > 0.5, use atac.obsm["X_lsi"][:, 1:] downstream.
```

---

## Part 4 — Spectral embedding (recommended)

```python
# Feature selection (top N variable peaks/bins)
snap.pp.select_features(adata_atac, n_features=50000)

# Spectral embedding — SnapATAC2's default, depth-robust
snap.pp.spectral(adata_atac, n_comps=50)

# UMAP + Leiden
snap.pp.umap(adata_atac)
snap.pp.knn(adata_atac)
snap.tl.leiden(adata_atac, resolution=0.5)
snap.pl.umap(adata_atac, color="leiden")
```

---

## Part 5 — Gene-activity matrix

```python
# Snap's native gene-activity scoring
gene_matrix = snap.pp.make_gene_matrix(
    adata_atac,
    gene_anno=snap.genome.hg38,   # or path to custom GTF
    upstream=2000,
    downstream=0,
)

# Add as a new modality (if working with MuData)
mdata.mod["gene_activity"] = gene_matrix

# Equivalent via muon
import muon as mu
mu.atac.pp.gene_activity(mdata, gene_anno=snap.genome.hg38)
```

---

## Common pitfalls

| Pitfall | Resolution |
|---|---|
| LSI1 correlates with sequencing depth (`|r| > 0.5`) | Drop component 1: use `X_lsi[:, 1:]` for all downstream steps. |
| Low TSS enrichment after filtering | Check fragment-file integrity (sort order, duplicate marking). Lower `min_tsse` only as a last resort. |
| `snap.pp.make_peak_matrix` OOMs | Use Snap's disk-backed mode (`backed="r"` on import) or split by chromosome. |
| Too few peaks in de novo call | Check that MACS2 is on `$PATH` and that input fragments are not over-filtered. |

---

## API quick reference

```python
snap.pp.import_data()         # Import fragments → AnnData
snap.pp.filter_cells()        # QC filtering
snap.pp.select_features()     # Feature selection
snap.pp.spectral()            # Spectral embedding
snap.pp.make_peak_matrix()    # Peak matrix (de novo or fixed set)
snap.pp.make_gene_matrix()    # Gene activity scoring
snap.pp.knn() / snap.pp.umap()
snap.tl.leiden()
```

---

## Resources

- SnapATAC2 docs: https://kzhang.org/SnapATAC2/
- episcanpy docs: https://episcanpy.readthedocs.io/
- MACS2 docs: https://github.com/macs3-project/MACS

---

## Prerequisites

Read `multimodal-anndata-mudata` first — it defines the MuData container this
skill writes its ATAC modality into.

---

## When not to use

- Do not use for R/Signac workflows. Use signac-chromatin-analysis instead.
- Do not use for cisTopic topic modelling on ATAC. Use pycistopic-atac-topic-modeling.
- Do not use for scRNA-seq QC, normalization, clustering, or RNA velocity. Use single-cell-rna-qc, scanpy, or rna-velocity-trajectory.

---

## See also

- `muon-multimodal-analysis`
- `harmonypy-batch-integration`
- `atac-differential-accessibility`
- `pygenometracks-coverage-plots`

---
name: atac-differential-accessibility
description: "Differential accessibility testing for scATAC-seq — marker peaks via scanpy / SnapATAC2, pseudobulk DA via pyDESeq2. Use when you have clusters or conditions on an ATAC AnnData and need per-peak statistics. For RNA differential expression use scanpy.rank_genes_groups; for motif-level analysis use chromvar-motif-accessibility."
license: MIT
---

# scATAC-seq Differential Accessibility

## Overview

Three orthogonal approaches to DA testing in scATAC-seq, each with
distinct statistical assumptions:

| Approach | Best for | Caveat |
|---|---|---|
| `sc.tl.rank_genes_groups` | Cluster marker peaks (one-vs-rest) | Treats cells as independent — inflated significance. |
| `snap.tl.marker_regions` / `diff_test` | Pairwise condition comparison within ATAC | Implemented in SnapATAC2; same single-cell test assumptions. |
| Pseudobulk + pyDESeq2 | Sample / condition comparisons with replicates | The gold standard when you have biological replicates. |

**When to reach for this skill:**
- You have an ATAC AnnData with clusters (`leiden`) or condition labels.
- You want per-peak statistics (effect size, adjusted p-value).
- You need to feed DA peaks into a downstream motif-enrichment or
  peak-gene linkage analysis.

---

## Part 1 — Marker peaks via scanpy

```python
import scanpy as sc

atac = mdata.mod["atac"]

# Ensure raw counts available
if "counts" in atac.layers:
    atac.X = atac.layers["counts"].copy()

# Normalise for DE-style testing
sc.pp.normalize_total(atac, target_sum=1e4)
sc.pp.log1p(atac)

# Find marker peaks per cluster
sc.tl.rank_genes_groups(
    atac,
    groupby="leiden",
    method="wilcoxon",   # or "t-test", "logreg"
    pts=True,            # also compute fraction-of-cells-expressing
)

# Pull cluster 0's markers
markers = sc.get.rank_genes_groups_df(atac, group="0")
markers = markers[markers["pvals_adj"] < 0.05]

# Visualise
sc.pl.rank_genes_groups(atac, n_genes=10)
sc.pl.rank_genes_groups_dotplot(atac, n_genes=5)
```

---

## Part 2 — SnapATAC2 native DA

```python
import snapatac2 as snap

atac = mdata.mod["atac"]

# Marker peaks (one-vs-rest, per group in `groupby`)
snap.tl.marker_regions(
    atac,
    groupby="leiden",
    pvalue=0.01,
)
markers = atac.uns["marker_regions"]

# Pairwise comparison (two groups in a categorical column)
da_results = snap.tl.diff_test(
    atac,
    groupby="condition",
    groups=["treated", "control"],
    method="t-test",      # or "wilcoxon"
)
```

---

## Part 3 — Pseudobulk DA via pyDESeq2 (recommended for replicates)

```python
import numpy as np
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

atac = mdata.mod["atac"]

def create_pseudobulk(adata, groupby):
    """Sum counts within each group of `groupby` → peaks x groups DF."""
    groups = adata.obs[groupby].unique()
    pb = {}
    for g in groups:
        mask = adata.obs[groupby] == g
        pb[g] = np.array(adata[mask].X.sum(axis=0)).flatten()
    return pd.DataFrame(pb, index=adata.var_names)

pb = create_pseudobulk(atac, groupby="sample")

# Metadata table — peaks × samples → samples × condition
metadata = pd.DataFrame({
    "sample": pb.columns,
    "condition": ["treated", "treated", "control", "control"],
}).set_index("sample")

dds = DeseqDataSet(
    counts=pb.T,
    metadata=metadata,
    design_factors="condition",
)
dds.deseq2()

stat_res = DeseqStats(dds, contrast=["condition", "treated", "control"])
stat_res.summary()
results = stat_res.results_df  # log2FC, pvalue, padj per peak
```

For R workflows the equivalent is `DESeq2::DESeq()` or `edgeR` on the
same pseudobulk matrix.

---

## Choosing the right test

```
Have biological replicates per condition?
├── yes → Pseudobulk + pyDESeq2  (Part 3)
└── no  → Single-cell DA
         ├── one-vs-rest across many clusters → Part 1 (scanpy)
         └── two specific groups               → Part 2 (snap.tl.diff_test)
```

---

## Common pitfalls

| Pitfall | Resolution |
|---|---|
| No significant peaks at FDR 5 % | Use less stringent threshold; check normalisation; try pseudobulk. |
| Inflated p-values from single-cell tests | Always aggregate to pseudobulk before publishing condition-level claims. |
| Batch effects confounding DA | Include batch as covariate in pseudobulk design, or stratify by batch. |
| Sparse peak signal | Aggregate to broader genomic windows (e.g., 5 kb tiles) before DA. |

---

## API quick reference

```python
sc.tl.rank_genes_groups()      # generic; works on peaks named like genes
snap.tl.marker_regions()       # SnapATAC2 one-vs-rest
snap.tl.diff_test()            # SnapATAC2 pairwise
pydeseq2.DeseqDataSet          # pseudobulk DE/DA
pydeseq2.DeseqStats            # contrast extraction
```

---

## Resources

- pyDESeq2: https://pydeseq2.readthedocs.io/
- SnapATAC2 DA docs: https://kzhang.org/SnapATAC2/
- DESeq2 pseudobulk patterns: Squair et al., Nature Comms 2021.

---

## When not to use

- Do not use for RNA differential expression; use scanpy.rank_genes_groups.
- Do not use for motif-level differential signal; use chromvar-motif-accessibility.

---

## See also

- `snapatac2-atac-preprocessing`
- `chromvar-motif-accessibility`
- `muon-multimodal-analysis`

Upstream docs: https://kzhang.org/SnapATAC2/api/index.html

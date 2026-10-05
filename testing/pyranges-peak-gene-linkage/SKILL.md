---
name: pyranges-peak-gene-linkage
description: "Peak-to-gene linkage — correlate scATAC peak accessibility with scRNA expression of nearby genes, computing gene activity scores and Pearson correlations within configurable genomic windows. Use for cis-regulatory candidate links on a paired multiome dataset. For unpaired linkage use scglue-unpaired-multiomics-integration."
license: MIT
---

# Peak-to-Gene Linkage (paired multiome)

## Overview

In a paired 10x Multiome dataset, every cell has both an RNA expression
profile and an ATAC accessibility profile. Peak-to-gene linkage tests
whether a given peak's accessibility tracks a nearby gene's expression
across cells — the simplest possible cis-regulatory hypothesis. This
skill covers two stages:

1. **Gene activity** — collapse peak counts into per-gene scores so the
   ATAC modality is annotated in gene space.
2. **Per-peak correlation** — Pearson correlation of each peak against
   each nearby gene's expression, with a configurable window.

For more sophisticated regulatory modelling (TF priors, cell-type
specificity, multi-omic NMF), see `crescendo-scatac-cre-analysis` and
`pycistarget-motif-enrichment`.

---

## Part 1 — Gene activity matrix

The gene-activity matrix is peaks-summarised-per-gene, typically by
summing reads within the gene body plus an upstream window. Two
implementations:

```python
import snapatac2 as snap
import muon as mu

atac = mdata.mod["atac"]

# SnapATAC2 implementation
gene_matrix = snap.pp.make_gene_matrix(
    atac,
    gene_anno=snap.genome.hg38,   # or path to a GTF
    upstream=2000,
    downstream=0,
)
mdata.mod["gene_activity"] = gene_matrix

# Muon equivalent (wraps a similar logic, integrates into the MuData)
mu.atac.pp.gene_activity(mdata, gene_anno=snap.genome.hg38)
```

The gene-activity matrix is the right input for label-transfer-from-RNA
workflows (Seurat-style anchoring) and for sanity-checking known
cell-type markers in the ATAC modality.

---

## Part 2 — Direct peak-gene correlation

```python
import numpy as np
import pandas as pd
from scipy import stats

rna  = mdata.mod["rna"]
atac = mdata.mod["atac"]

# Restrict to cells with both modalities
common  = list(set(rna.obs_names) & set(atac.obs_names))
rna_sub  = rna[common]
atac_sub = atac[common]

def correlate_peak_gene(peak_idx, gene_idx):
    peak_vals = np.array(atac_sub.X[:, peak_idx].todense()).flatten()
    gene_vals = np.array(rna_sub.X[:, gene_idx].todense()).flatten()
    r, p = stats.pearsonr(peak_vals, gene_vals)
    return r, p
```

### Restrict to a genomic window around a gene of interest

```python
# atac.var MUST have 'chrom', 'start', 'end' columns
gene = "MS4A1"
gene_idx = list(rna.var_names).index(gene)

# These come from your gene annotation (Ensembl, GENCODE, ...)
gene_chrom = "chr11"
gene_start = 60223282
window     = 100_000        # +/- 100 kb is conventional

nearby_peaks = atac.var[
    (atac.var["chrom"] == gene_chrom) &
    (abs(atac.var["start"] - gene_start) < window)
]

results = []
for peak in nearby_peaks.index:
    peak_idx = list(atac.var_names).index(peak)
    r, p = correlate_peak_gene(peak_idx, gene_idx)
    results.append({"peak": peak, "gene": gene, "r": r, "p": p})

corr_df = (
    pd.DataFrame(results)
      .query("p < 0.05")
      .sort_values("r", ascending=False)
)
```

For genome-wide linkage, vectorise the loop with `pyranges` (a true
interval-arithmetic library) — far faster than per-gene Python loops:

```python
import pyranges as pr
gene_pr = pr.PyRanges(... )     # build from your gene annotation
peak_pr = pr.PyRanges(... )     # build from atac.var

# pyranges.join gives every (peak, gene) pair within a window
joined = peak_pr.k_nearest(gene_pr, k=5).df
# then loop / vectorise over `joined` rows
```

---

## Choosing the window

| Window | Use case |
|---|---|
| ±2 kb around TSS | "Promoter" linkage only |
| ±100 kb around TSS | Standard cis-regulatory window |
| ±500 kb / topologically associated domain | Includes long-range enhancers |

The right answer is workflow-dependent — paper-replication usually fixes
the window at the cited value; novel analyses should sweep windows and
report sensitivity.

---

## Common pitfalls

| Pitfall | Resolution |
|---|---|
| `atac.var` lacks `chrom/start/end` | Reconstruct from the peak name (e.g. `chr1:1000-2000`) before correlating. |
| Multiple-testing not corrected | Apply Benjamini-Hochberg across all (peak, gene) pairs in the window. |
| All correlations near zero | Peaks may be too sparse; aggregate into broader bins or restrict to highly variable peaks. |
| Cell-type-driven spurious correlation | Correlate within each cell type, or regress out cell type first. |

---

## API quick reference

```python
snap.pp.make_gene_matrix()    # gene activity (SnapATAC2)
mu.atac.pp.gene_activity()    # gene activity (muon)
scipy.stats.pearsonr()        # per-pair correlation
pyranges.PyRanges             # genome-wide interval arithmetic
```

---

## Resources

- pyranges: https://github.com/biocore-ntnu/pyranges
- muon: https://muon.scverse.org/
- SnapATAC2 gene activity: https://kzhang.org/SnapATAC2/
- Cusanovich et al., Cell 2018 — original cell-by-peak / peak-gene framework.

---

## When not to use

- Do not use for unpaired RNA + ATAC. Use scglue-unpaired-multiomics-integration.
- Do not use for motif enrichment on linked peaks. Use pycistarget-motif-enrichment.

---

## See also

- `muon-multimodal-analysis`
- `snapatac2-atac-preprocessing`
- `scglue-unpaired-multiomics-integration`
- `crescendo-scatac-cre-analysis`

---
name: muon-multimodal-analysis
description: "End-to-end orchestrator for paired multimodal scRNA + scATAC analysis in the Python scverse (muon, MuData, scanpy, SnapATAC2). Use as the entry point for a 10x Multiome or CITE-seq dataset: it chains preprocessing, batch integration, differential accessibility, peak-gene linkage, and visualisation across five leaf skills."
license: MIT
---

# muon Multimodal Analysis — Orchestrator

## Overview

This skill is the **entry point** for Python-side paired multimodal
analysis (10x Multiome, CITE-seq). It does not duplicate per-tool tutorial
content — that lives in the leaf skills listed below. Its
job is to choreograph the workflow: when to load a MuData, which
preprocessing path to take per modality, when to integrate, and how to
hand off to scvi-tools for deep-learning-based joint embeddings.

**The leaves (mounted flat alongside this skill; load each on demand):**

| Leaf | Role in the workflow |
|---|---|
| `multimodal-anndata-mudata` | MuData container — load, slice, save |
| `scanpy` | RNA preprocessing (QC, HVGs, PCA, Leiden) |
| `snapatac2-atac-preprocessing` | ATAC preprocessing (fragments → spectral embedding) |
| `harmonypy-batch-integration` | Multi-sample batch correction (PCA / LSI / spectral) |
| `atac-differential-accessibility` | Marker peaks + pseudobulk DA |
| `pyranges-peak-gene-linkage` | Peak-to-gene cis-regulatory links |
| `pygenometracks-coverage-plots` | Static genome-browser figure panels |
| `scvi-multivi` | Joint deep-learning embedding (MultiVI) |

---

## Decision tree — which leaf do I need?

```
Starting point?
├── Cell Ranger ARC output (raw 10x Multiome)
│   └── load with multimodal-anndata-mudata → mu.read_10x_h5(...)
├── Already have h5mu / paired AnnData
│   └── load with multimodal-anndata-mudata
└── Only fragments file (no peak matrix)
    └── snapatac2-atac-preprocessing → snap.pp.import_data()

Per-modality preprocessing
├── RNA modality          → scanpy (normalise, HVGs, PCA, Leiden)
└── ATAC modality         → snapatac2-atac-preprocessing
                              (TF-IDF + LSI  OR  spectral embedding)

Have multiple samples?
└── harmonypy-batch-integration on each modality's embedding
    (X_pca → X_pca_harmony, X_spectral → X_spectral_harmony)

Want a joint deep embedding instead of WNN concatenation?
└── scvi-multivi (MultiVI model)

Downstream analyses
├── Per-cluster marker peaks  → atac-differential-accessibility (Part 1)
├── Condition vs condition DA → atac-differential-accessibility (Part 3, pseudobulk)
├── Peak → gene cis-links     → pyranges-peak-gene-linkage
└── Locus-level figure panels → pygenometracks-coverage-plots
```

---

## Canonical workflow (paired 10x Multiome)

```python
import muon as mu, scanpy as sc, snapatac2 as snap
import scanpy.external as sce

# === 1. Load (multimodal-anndata-mudata) ===
mdata = mu.read_10x_h5("filtered_feature_bc_matrix.h5")
mdata.mod["atac"].uns["files"] = {"fragments": "atac_fragments.tsv.gz"}

# === 2. RNA preprocessing (scanpy) ===
rna = mdata.mod["rna"]
sc.pp.calculate_qc_metrics(rna, qc_vars=["mt"], inplace=True)
sc.pp.filter_cells(rna, min_genes=200); sc.pp.filter_genes(rna, min_cells=3)
sc.pp.normalize_total(rna, target_sum=1e4); sc.pp.log1p(rna)
sc.pp.highly_variable_genes(rna, n_top_genes=3000)
sc.pp.pca(rna, n_comps=50)

# === 3. ATAC preprocessing (snapatac2-atac-preprocessing) ===
atac = mdata.mod["atac"]
snap.metrics.tsse(atac, snap.genome.hg38)
snap.pp.filter_cells(atac, min_counts=1000, min_tsse=2)
snap.pp.select_features(atac, n_features=50000)
snap.pp.spectral(atac, n_comps=50)

# === 4. Batch correction (harmonypy-batch-integration) ===
sce.pp.harmony_integrate(rna,  key="sample", basis="X_pca",
                         adjusted_basis="X_pca_harmony")
sce.pp.harmony_integrate(atac, key="sample", basis="X_spectral",
                         adjusted_basis="X_spectral_harmony")

# === 5. Joint neighbours + UMAP ===
mu.pp.neighbors(mdata, key_added="wnn")
mu.tl.umap(mdata, neighbors_key="wnn")
sc.tl.leiden(rna)

# === 6. Differential accessibility (atac-differential-accessibility) ===
sc.tl.rank_genes_groups(atac, groupby="leiden", method="wilcoxon")

# === 7. Peak → gene linkage (pyranges-peak-gene-linkage) ===
mu.atac.pp.gene_activity(mdata, gene_anno=snap.genome.hg38)
# ...then peak/gene Pearson correlation per locus (see leaf skill)

# === 8. Save ===
mdata.write("multiome.h5mu")
```

---

## CITE-seq variant

Same chassis, different ATAC: replace step 3 with the CITE-seq protein
modality (`mdata.mod["adt"]` or `mdata.mod["prot"]`) preprocessed via
scanpy's `sc.external.pp.normalize_total` on CLR-transformed counts.
Steps 4 (Harmony), 5 (WNN), 6 (differential protein abundance via
`rank_genes_groups`) carry over unchanged.

---

## When to use MultiVI instead of WNN

| Symptom | Switch to MultiVI |
|---|---|
| WNN UMAP shows persistent batch structure even after per-modality Harmony | yes |
| You need a generative model (imputation, missing-modality cells) | yes |
| GPU available, dataset >50 k cells | yes |
| Quick exploratory pass, CPU-only, <20 k cells | no, stay on WNN + Harmony |

See `scvi-multivi` for the exact setup_anndata / train / latent
extraction calls.

---

## Cross-cutting pitfalls

### MuData
| Pitfall | Resolution |
|---|---|
| Cell name mismatch between modalities | `mdata.update()` or align obs_names manually before `MuData(...)`. |
| Memory issues with large data | Use backed mode: `mu.read("file.h5mu", backed="r")`. |
| Lost metadata after subsetting | Call `mdata.update()` after every subsetting operation. |

### Cross-modality alignment
| Pitfall | Resolution |
|---|---|
| Different cell sets per modality | Intersect `obs_names` before joint analysis. |
| Different cluster labels per modality | Re-cluster on the joint WNN/MultiVI embedding, not per-modality. |

### Batch correction order
- Do **Harmony per modality** before WNN, not the other way around — WNN
  expects each modality's embedding to be already batch-corrected.
- For MultiVI, pass `batch_key="sample"` at `setup_anndata` time and skip
  Harmony entirely.

---

## Visualisation recipes

```python
import matplotlib.pyplot as plt

# Side-by-side per-modality UMAPs
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sc.pl.umap(mdata.mod["rna"],  color="cell_type", ax=axes[0], show=False)
sc.pl.umap(mdata.mod["atac"], color="cell_type", ax=axes[1], show=False)
axes[0].set_title("RNA"); axes[1].set_title("ATAC")
plt.tight_layout(); plt.show()
```

Locus-level coverage figures (e.g. for marker genes) are handled by
`pygenometracks-coverage-plots`.

---

## Resources

- muon:          https://muon.scverse.org/
- mudata:        https://mudata.readthedocs.io/
- scverse:       https://scverse.org/
- SnapATAC2:     https://kzhang.org/SnapATAC2/
- scvi-tools MultiVI: https://docs.scvi-tools.org/en/stable/user_guide/models/multivi.html


---

## When not to use

- Do not use for R/Seurat workflows. Use seurat-multimodal-analysis instead.
- Do not use solely for Seurat-to-Python conversion. Use multimodal-anndata-mudata for that bridge.
- Do not use for unpaired RNA and ATAC from separate cell pools. Use scglue-unpaired-multiomics-integration.
- Do not use for scATAC-only analysis. Use snapatac2-atac-preprocessing.
- Do not use for plain scRNA-seq. Use scanpy or the appropriate scvi skill.

---

## See also

- `seurat-multimodal-analysis`
- `scglue-unpaired-multiomics-integration`
- `scvi-multivi`

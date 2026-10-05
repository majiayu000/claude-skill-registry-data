---
name: single-cell-rna-qc
description: "scverse/sc-best-practices QC for single-cell RNA-seq using MAD-based adaptive outlier detection on counts, gene counts, and pct_counts_mt — data-driven thresholds that generalize where fixed cutoffs fail. Also annotates MT/ribo/hemoglobin gene sets, species-aware. Use when running QC from scratch on raw 10x or .h5ad data."
license: MIT
---

# Single-Cell RNA-seq Quality Control

MAD-based (Median Absolute Deviation) QC for single-cell RNA-seq, following scverse best practices. This skill provides the methodology and inline code for data-driven, adaptive filtering -- superior to fixed thresholds that fail across protocols, tissues, and species.

## When to Use

- User requests QC or quality control on scRNA-seq data
- Filtering low-quality cells from `.h5ad` or `.h5` files
- Need MAD-based outlier detection (data-driven thresholds)
- Assessing data quality before normalization/integration
- scverse/scanpy best practices for QC

## When NOT to Use

- Data is already QC'd (check `adata.obs` for existing QC columns like `pct_counts_mt`)
- Bulk RNA-seq (this is single-cell specific)
- ATAC-seq or other non-RNA modalities
- Only need basic fixed-threshold filtering -> use `scanpy.md` Section 1 directly

---

## Quick Start

Minimal QC in ~20 lines. For full workflow with verification checkpoints, see Standard Workflow below.

```python
import scanpy as sc
import numpy as np
from scipy.stats import median_abs_deviation

adata = sc.read_h5ad("data.h5ad")
# or: adata = sc.read_10x_h5("raw_feature_bc_matrix.h5")

# 1. Annotate gene categories (human shown; for mouse use 'mt-', 'Rpl', 'Rps')
adata.var["mt"] = adata.var_names.str.startswith("MT-")
adata.var["ribo"] = adata.var_names.str.startswith(("RPL", "RPS"))
adata.var["hb"] = adata.var_names.str.match(r"^HB[^(P)]")

# 2. Calculate QC metrics
sc.pp.calculate_qc_metrics(adata, qc_vars=["mt", "ribo", "hb"],
                           percent_top=None, log1p=False, inplace=True)

# 3. MAD-based outlier detection
def is_outlier(adata, metric, n_mads):
    M = adata.obs[metric]
    return (M < np.median(M) - n_mads * median_abs_deviation(M)) | \
           (M > np.median(M) + n_mads * median_abs_deviation(M))

outlier = (
    is_outlier(adata, "log1p_total_counts", 5) |
    is_outlier(adata, "log1p_n_genes_by_counts", 5) |
    is_outlier(adata, "pct_counts_mt", 3) |
    (adata.obs["pct_counts_mt"] > 8)  # hard ceiling
)

# 4. Filter
print(f"Removing {outlier.sum()} / {adata.n_obs} cells ({outlier.mean():.1%})")
adata = adata[~outlier].copy()
sc.pp.filter_genes(adata, min_cells=20)
```

---

## Standard Workflow

### Step 1: Calculate QC Metrics

Annotate gene categories and compute per-cell metrics. Gene name patterns are species-specific:

| Species | MT genes | Ribosomal | Hemoglobin |
|---------|----------|-----------|------------|
| Human | `MT-` | `RPL`, `RPS` | `^HB[^(P)]` |
| Mouse | `mt-` | `Rpl`, `Rps` | `^Hb[^(p)]` |

```python
import scanpy as sc
import numpy as np
from scipy.stats import median_abs_deviation

adata = sc.read_h5ad("data.h5ad")
print(f"Loaded: {adata.n_obs} cells x {adata.n_vars} genes")

# Species-aware gene annotation
# Human:
adata.var["mt"] = adata.var_names.str.startswith("MT-")
adata.var["ribo"] = adata.var_names.str.startswith(("RPL", "RPS"))
adata.var["hb"] = adata.var_names.str.match(r"^HB[^(P)]")

# Mouse (uncomment if needed):
# adata.var["mt"] = adata.var_names.str.startswith("mt-")
# adata.var["ribo"] = adata.var_names.str.startswith(("Rpl", "Rps"))
# adata.var["hb"] = adata.var_names.str.match(r"^Hb[^(p)]")

sc.pp.calculate_qc_metrics(
    adata, qc_vars=["mt", "ribo", "hb"],
    percent_top=None, log1p=True, inplace=True
)

# Verify MT genes were found
n_mt = adata.var["mt"].sum()
print(f"MT genes found: {n_mt}")
if n_mt == 0:
    print("WARNING: No MT genes found! Check species/gene naming convention.")
```

**Checkpoint:** `n_mt` should be 13 (human) or 13 (mouse). Zero means wrong prefix.

### Step 2: Visualize Before Filtering

Always inspect distributions before setting thresholds.

```python
sc.pl.violin(
    adata,
    ["n_genes_by_counts", "total_counts", "pct_counts_mt"],
    jitter=0.4, multi_panel=True, show=False
)
# Save: plt.savefig("qc_before_filtering.png", dpi=150, bbox_inches="tight")

sc.pl.scatter(adata, x="total_counts", y="n_genes_by_counts", color="pct_counts_mt")
sc.pl.scatter(adata, x="total_counts", y="pct_counts_mt")
```

**What to look for:**
- Bimodal count distributions -> may indicate empty droplets mixed with real cells
- Strong positive correlation between counts and genes (R > 0.8 typical)
- High-MT% cells clustering at low counts -> dying cells
- Outlier clouds in scatter plots -> doublets (upper-right) or debris (lower-left)

### Step 3: MAD-Based Outlier Detection

MAD adapts to your data distribution, unlike fixed thresholds:

```
MAD = median(|X - median(X)|)
Outlier if: X < median - n_mads * MAD  OR  X > median + n_mads * MAD
```

```python
def is_outlier(adata, metric, n_mads):
    """Detect outliers using MAD. Returns boolean Series (True = outlier)."""
    M = adata.obs[metric]
    median_val = np.median(M)
    mad_val = median_abs_deviation(M)
    lower = median_val - n_mads * mad_val
    upper = median_val + n_mads * mad_val
    outlier = (M < lower) | (M > upper)
    print(f"  {metric}: median={median_val:.2f}, MAD={mad_val:.2f}, "
          f"bounds=[{lower:.2f}, {upper:.2f}], outliers={outlier.sum()}")
    return outlier

print("Outlier detection:")
outlier_counts = is_outlier(adata, "log1p_total_counts", 5)
outlier_genes = is_outlier(adata, "log1p_n_genes_by_counts", 5)
outlier_mt = is_outlier(adata, "pct_counts_mt", 3)

# Hard MT% ceiling (catches cases where MAD is too wide)
hard_mt = adata.obs["pct_counts_mt"] > 8
print(f"  Hard MT% > 8: {hard_mt.sum()} cells")

# Combined mask
outlier = outlier_counts | outlier_genes | outlier_mt | hard_mt
print(f"\nTotal outliers: {outlier.sum()} / {adata.n_obs} ({outlier.mean():.1%})")
```

**Default thresholds and rationale:**

| Metric | MADs | Log-transform? | Rationale |
|--------|------|-----------------|-----------|
| `log1p_total_counts` | 5 | Yes (by `log1p=True` in calc) | Very permissive; catches empty droplets and debris |
| `log1p_n_genes_by_counts` | 5 | Yes | Parallels count depth; low = poor capture |
| `pct_counts_mt` | 3 | No | More stringent; high MT% strongly indicates dying cells |
| `pct_counts_mt` hard | 8% | N/A | Safety ceiling across most tissues |

**When to adjust:**
- **Neurons/cardiomyocytes**: Raise MT% hard threshold to 10-15% (naturally high MT)
- **Tumor samples**: Use more permissive thresholds (higher biological variation)
- **High-quality 10x data**: Can tighten to 3 MADs for counts/genes
- **Studying rare populations**: Keep permissive (5 MADs) to avoid losing rare cells

### Step 4: Filter Cells and Genes

```python
n_before = adata.n_obs
adata = adata[~outlier].copy()
print(f"Cell filtering: {n_before} -> {adata.n_obs} ({adata.n_obs/n_before:.1%} retained)")

n_genes_before = adata.n_vars
sc.pp.filter_genes(adata, min_cells=20)
print(f"Gene filtering: {n_genes_before} -> {adata.n_vars} (min_cells=20)")
```

**Gene filtering note:** `min_cells=20` balances noise reduction with information retention. Lower to 10 if studying rare markers; raise to 50 for cleaner downstream HVG selection.

### Step 5: Visualize After Filtering

```python
sc.pl.violin(
    adata,
    ["n_genes_by_counts", "total_counts", "pct_counts_mt"],
    jitter=0.4, multi_panel=True, show=False
)
# Save: plt.savefig("qc_after_filtering.png", dpi=150, bbox_inches="tight")

sc.pl.scatter(adata, x="total_counts", y="n_genes_by_counts", color="pct_counts_mt")
```

### Step 6: STOP and Verify

**Before proceeding to normalization, check:**

1. **Cell retention**: Typically 85-95% retained. Below 70% suggests thresholds are too strict.
2. **MT% distribution**: Should be unimodal, no heavy right tail remaining.
3. **Counts vs genes scatter**: Should show clean positive correlation without outlier clouds.
4. **No empty clusters**: If you have batch/sample metadata, check no sample lost >50% of cells (batch effect, not quality).

```python
# Summary statistics
print(f"Final: {adata.n_obs} cells, {adata.n_vars} genes")
print(f"Median counts/cell: {adata.obs['total_counts'].median():.0f}")
print(f"Median genes/cell: {adata.obs['n_genes_by_counts'].median():.0f}")
print(f"Mean MT%: {adata.obs['pct_counts_mt'].mean():.2f}%")
if "pct_counts_ribo" in adata.obs:
    print(f"Mean ribo%: {adata.obs['pct_counts_ribo'].mean():.2f}%")

# Save filtered data
adata.write("data_filtered.h5ad")
```

**Note on QC columns in the deliverable:** `log1p_*` and `outlier_*` columns are intermediate
diagnostics — useful for downstream checkpoint joins and audit trails, but prune them from the
final milestone deliverable to save memory. At packaging, keep only the base metrics
(`n_genes_by_counts`, `total_counts`, `pct_counts_mt`, `qc_pass`) and drop the derived
`log1p_*` / `outlier_*`. See
`scrna-pipeline-conventions/references/metadata-packaging.md` for the milestone
packaging pass.

---

## Key Parameters Reference

| Parameter | Default | Range | Effect |
|-----------|---------|-------|--------|
| MAD counts/genes | 5 | 3-5 | Lower = stricter; 3 for high-quality data |
| MAD MT% | 3 | 2-5 | Lower = stricter; raise for high-MT tissues |
| Hard MT% ceiling | 8% | 5-20% | Safety net; 10-15% for neurons/heart |
| Gene min_cells | 20 | 3-50 | Lower retains rare markers; higher = cleaner |

---

## Common Pitfalls

1. **Wrong species prefix**: Human uses `MT-` (uppercase), mouse uses `mt-` (lowercase). Zero MT genes found = wrong prefix. Always check `adata.var["mt"].sum()`.
2. **Fixed thresholds across datasets**: "Remove cells with < 500 genes" fails when protocols differ. MAD adapts automatically.
3. **Over-filtering**: Removing >30% of cells is a red flag. Rare populations (e.g., pDCs, cycling cells) are easily lost.
4. **Forgetting log-transform for counts**: Count depth is right-skewed. Use `log1p_total_counts` (set `log1p=True` in `calculate_qc_metrics`) for MAD detection on counts and genes. MT% is already bounded 0-100, no log needed.
5. **Filtering before inspecting**: Always visualize before and after. Thresholds should be informed by the data distribution, not assumed.
6. **Hemoglobin regex pitfall**: The pattern `^HB[^(P)]` excludes HBP1 (not a hemoglobin gene). Without the exclusion you get false annotations.

---

## Integration with Other Skills

- **After QC**: Proceed to `scanpy.md` for normalization, HVG selection, PCA, clustering
- **Multi-sample integration**: After QC per sample, use `scvi-basic.md` for batch correction (scVI needs raw counts -- QC before normalization)
- **Doublet detection**: Run after QC but before normalization (scrublet, scDblFinder)
- **Ambient RNA**: SoupX/CellBender should run before QC if contamination is suspected
- **AnnData operations**: See `anndata.md` for I/O, subsetting, concatenation

---

## References

- scverse Best Practices: https://www.sc-best-practices.org/preprocessing_visualization/quality_control.html
- Luecken & Theis (2019): Current best practices in single-cell RNA-seq analysis
- Germain et al. (2020): Doublet identification in single-cell sequencing data using scDblFinder

---

## When not to use

- Do not use on already-QC'd data. Check adata.obs for pct_counts_mt first.
- Do not use for bulk RNA-seq (this is single-cell specific).
- Do not use for ATAC-seq or other non-RNA modalities.

---

## See also

- `anndata`
- `scanpy`
- `scvi-basic`

---
name: scenic-grn-inference
description: "SCENIC+ builds enhancer-driven gene regulatory networks (eRegulons linking TF to region to gene) from paired scRNA and scATAC by integrating motif enrichment with expression correlation. Use when you need mechanistic TF-enhancer-target edges and have pycisTopic + pycistarget outputs ready. For scRNA-only regulons use pySCENIC."
license: MIT
---

# SCENIC+ GRN Inference Skill

## Overview

SCENIC+ builds enhancer-driven gene regulatory networks (eRegulons: TF→region→gene links) from paired scRNA-seq + scATAC-seq data. Integrates motif enrichment with expression correlation to identify high-confidence regulatory relationships.

## SCENIC+ Ecosystem

```
┌─────────────────┐     ┌─────────────────┐
│   scATAC-seq    │     │   scRNA-seq     │
│   (fragments)   │     │   (counts)      │
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│   pycisTopic    │     │  Save .raw      │
│  (topic model)  │     │  BEFORE norm    │
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       │
┌─────────────────┐              │
│   pycistarget   │              │
│ (motif enrich)  │              │
└────────┬────────┘              │
         │                       │
         ▼                       ▼
┌─────────────────────────────────────────┐
│              SCENIC+ Snakemake          │
│  (integrates motifs + expression → GRN) │
└────────────────────┬────────────────────┘
                     │
                     ▼
            ┌─────────────────┐
            │   eRegulons     │
            │ (TF→region→gene)│
            └─────────────────┘
```

**Prerequisites:**
1. **pycisTopic output**: `cistopic_obj.pkl` + `region_sets/*.bed` — see [pycisTopic skill](../pycistopic-atac-topic-modeling/SKILL.md)
2. **pycistarget** (optional standalone): For detailed motif enrichment outside Snakemake — see [pycistarget skill](../pycistarget-motif-enrichment/SKILL.md)
3. **scRNA-seq AnnData**: With `.raw` saved BEFORE normalization

## Core Concepts

**eRegulons**: TF-region-gene modules combining:
- GBM importance scores (TF→gene prediction strength)
- Correlation (rho) between TF and target gene expression
- Motif enrichment linking TF to accessible regions

**Direct vs Extended**:
- Direct = database motif directly maps to TF
- Extended = includes orthologs and motif similarity matches

## Critical Requirements

```python
# CRITICAL: Save raw BEFORE any normalization
adata.raw = adata  # Required for SCENIC+ GBM models

# Barcodes MUST match between RNA and ATAC (for multiome)
# Use bc_transform_func in config if they differ

# cisTarget databases (download from Aertslab)
ctx_db = '*.rankings.feather'  # Recovery curves
dem_db = '*.scores.feather'    # Wilcoxon tests
motif_anno = 'motifs-v10-nr.{species}.tbl'
```

## Data Modes: Multiome vs Non-Multiome (Unpaired)

SCENIC+ supports two data modes:

| Mode | Description | Key Requirement |
|------|-------------|-----------------|
| **Multiome** | Same cells have both RNA + ATAC | Matching barcodes |
| **Non-multiome** | Separate RNA and ATAC experiments | Matching cell-type annotations |

### Non-Multiome / Unpaired Data (Metacell Approach)

For unpaired data (different cells for RNA vs ATAC), SCENIC+ creates **pseudo-multiome metacells**:

> "Sampling a predefined number of cells from each data modality within the same cell-type annotation label and averaging the raw gene expression and imputed chromatin-accessibility data across these cells to create a multiome meta-cell." — [Nature Methods 2023](https://www.nature.com/articles/s41592-023-01938-4)

**Prerequisites for unpaired data:**
1. Good cell-type annotations for BOTH RNA and ATAC
2. Annotations must match between modalities (same label vocabulary)
3. Sufficient cells per cell-type (recommend ≥50 per group, ≥30 is marginal)

**Config for unpaired data:**
```yaml
params_data_preparation:
  is_multiome: False                    # CRITICAL: Set to False for unpaired
  key_to_group_by: "cell_type"          # Metadata column for metacell grouping
  nr_cells_per_metacells: 10            # Cells to sample per metacell (default: 10)
```

**Expected output:** ~100-300 pseudo-multiome metacells (depends on cell-type granularity)

### Condition-Specific Metacells (Composite Labels)

To preserve **condition-specific** regulatory differences, use composite celltype × condition labels:

```python
# Create composite annotation BEFORE SCENIC+ input
rna.obs["celltype_condition"] = (
    rna.obs["cell_type"].astype(str) + "_" + rna.obs["condition"].astype(str)
)
atac.obs["celltype_condition"] = (
    atac.obs["cell_type"].astype(str) + "_" + atac.obs["condition"].astype(str)
)
```

```yaml
params_data_preparation:
  is_multiome: False
  key_to_group_by: "celltype_condition"   # e.g., "cDC1A_WT", "cDC1A_IL12"
  nr_cells_per_metacells: 10
```

**Adaptive per-group cell counts** (for groups with different sizes):
```python
# In SCENIC+ Python API (not Snakemake):
create_SCENICPLUS_object(
    ...,
    multi_ome_mode=False,
    key_to_group_by="celltype_condition",
    nr_cells_per_metacells={
        "cDC1A_WT": 10,
        "cDC1A_IL12": 10,
        "Chol_cDC2B_WT": 5,     # Small group: fewer cells per metacell
        "ISG_Mac_KO": 5,         # Small group: fewer cells per metacell
    }
)
```

**Caveat (from GitHub Discussion #215):** Avoid using the same grouping variable for metacell creation AND downstream differential analysis to prevent circular logic. When grouping is based on pre-existing annotations and differential analysis uses eRegulon scores, this is mitigated.

### Benchmark Context: SCENIC+ vs Alternatives (Unpaired)

| Method | TF Recovery | Enhancer-Gene f-score | Unpaired Support | Notes |
|--------|------------|----------------------|-----------------|-------|
| **SCENIC+** | 178 TFs | 0.12 | Yes (metacells) | Best TF-centric eRegulons |
| **scGLUE** | Via pySCENIC | 0.3-0.4 | Yes (native) | Better enhancer-gene links |
| **STREAM** | Best overall | 0.4-0.5 | No (paired only) | Benchmark winner, needs multiome |
| **CellOracle** | 235 TFs | — | Yes | Requires GRN prior |

**Recommendation:** Use SCENIC+ for TF-centric eRegulons + scGLUE independently for enhancer-gene validation. See [scGLUE skill](../scglue-unpaired-multiomics-integration/SKILL.md).

### Input Data Preparation (Unpaired)

For converting Seurat/Signac objects to h5ad for SCENIC+, see [scenic-r-python-interop](../scenic-r-python-interop/SKILL.md):
- **Scenario A**: Signac ATAC → pycisTopic (count matrix export)
- **Scenario E**: Seurat RNA → AnnData (raw count preservation)

## API Versions

SCENIC+ has two distinct API surfaces:

| API | Version | When to Use |
|-----|---------|-------------|
| **Snakemake pipeline** | v1.0+ release | Standard workflows, reproducible configs |
| **Python standalone** | 1.0a2 (wrapper API) | Custom workflows, interactive exploration |

The Snakemake pipeline (Sections 3-5 below) is the primary documented path. For the standalone Python API, see the [Standalone Python API](#standalone-python-api-non-snakemake) section.

---

## Workflow

### 1. Prepare scRNA-seq Data

```python
import scanpy as sc

# Standard preprocessing
adata = sc.read_h5ad('rna_data.h5ad')
adata.raw = adata  # CRITICAL: Before normalize_total/log1p/scale
sc.pp.normalize_total(adata)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata)
sc.pp.scale(adata)
sc.pp.pca(adata)
sc.pp.neighbors(adata)
sc.tl.umap(adata)

# Save with raw preserved
adata.write('adata_for_scenic.h5ad')
```

### 2. Custom cisTarget Database (Recommended, 2-3x better)

```bash
# Download cbust
wget https://resources.aertslab.org/cistarget/programs/cbust

# Create FASTA from peaks
create_fasta_with_padded_bg_from_bed.sh ${GENOME} ${CHROMSIZES} peaks.bed out.fa 1000 yes

# Build database
create_cistarget_motif_databases.py -f out.fa -M motifs/ -o db_prefix \
    --bgpadding 1000 -t 20
```

**Precomputed databases**: https://resources.aertslab.org/cistarget/ (hg38/mm10/dm6)

### 3. Initialize SCENIC+ Pipeline

```bash
# Initialize Snakemake workflow
scenicplus init_snakemake --out_dir scplus_pipeline
```

### 4. Configure Pipeline

Edit `scplus_pipeline/Snakemake/config.yaml`:

```yaml
input_data:
  cisTopic_obj_fname: "/path/to/cistopic_obj.pkl"      # From pycisTopic
  GEX_anndata_fname: "/path/to/adata_for_scenic.h5ad"  # With .raw saved
  region_set_folder: "/path/to/region_sets/"           # From pycisTopic

params_data_preparation:
  bc_transform_func: "lambda x: f'{x}-sample'"  # If barcodes don't match
  is_multiome: True                              # True for paired/multiome data
  # --- OR for unpaired/non-multiome data: ---
  # is_multiome: False
  # key_to_group_by: "cell_type"                 # Metadata column for metacell grouping
  # nr_cells_per_metacells: 10                   # Cells per metacell (default: 10)
  species: "mmusculus"                           # or "hsapiens"

params_motif_enrichment:
  dem_adj_pval_thr: 0.05     # DEM significance threshold
  dem_log2fc_thr: 1.0        # DEM fold-change threshold
  ctx_auc_threshold: 0.005   # cisTarget AUC threshold
  ctx_nes_threshold: 3.0     # cisTarget NES threshold (context specificity)
  ctx_rank_threshold: 0.05   # cisTarget rank threshold
  # For detailed motif enrichment parameters, see pycistarget skill

cistarget_databases:
  ctx_db: "/path/to/*.rankings.feather"
  dem_db: "/path/to/*.scores.feather"
  motif_annotation: "/path/to/motifs-v10-nr.mmus-m0.001-o0.0.tbl"
```

### 5. Run Pipeline

```bash
cd scplus_pipeline/Snakemake/
snakemake --cores 20
```

### 6. Analyze Results

```python
import mudata
from scenicplus.RSS import regulon_specificity_scores
from scenicplus.plotting.dotplot import heatmap_dotplot

# Load results
scplus_mdata = mudata.read('outs/scplusmdata.h5mu')

# eRegulons metadata
eregulons = scplus_mdata.uns['direct_e_regulon_metadata']
# Columns: TF, Gene, Region, importance_TF2G, rho_TF2G, regulation, triplet_rank

# Regulon Specificity Score (RSS)
rss = regulon_specificity_scores(scplus_mdata, variable='scRNA_counts:cell_type',
    modalities=['direct_gene_based_AUC'])

# Visualization: gene AUC (color) + region AUC (size)
heatmap_dotplot(scplus_mdata, color_modality='direct_gene_based_AUC',
    size_modality='direct_region_based_AUC', group_variable='scRNA_counts:cell_type')
```

## Quality Metrics

| Metric | Good | Interpretation |
|--------|------|----------------|
| triplet_rank | <1000 | High-confidence TF-region-gene link |
| importance_TF2G | >1.0 | Strong GBM feature importance |
| \|rho\| | >0.3 | Strong TF-gene correlation |
| RSS | >0.5 | Cell-type specific regulon |
| N eRegulons | >50 | Sufficient regulatory coverage |

## Filtering eRegulons

```python
# High-confidence eRegulons
hc_eregulons = eregulons[
    (eregulons['triplet_rank'] < 500) &
    (eregulons['importance_TF2G'] > 1.5) &
    (abs(eregulons['rho_TF2G']) > 0.3)
]

# Cell-type specific (high RSS)
tf_rss = rss.loc[rss.max(axis=1) > 0.5]
```

## Standalone Python API (Non-Snakemake)

For interactive or custom workflows, use the Python API directly instead of Snakemake. This is especially useful for unpaired data with condition-specific metacells.

### scenicplus 1.0a2 (Wrapper API)

```python
from scenicplus.scenicplus_class import create_SCENICPLUS_object
from scenicplus.wrappers.run_scenicplus import run_scenicplus

# Step 1: Create SCENIC+ object
# For UNPAIRED data: set multi_ome_mode=False
scplus_obj = create_SCENICPLUS_object(
    GEX_anndata=rna_adata,       # With .raw saved before normalization
    cisTopic_obj=cistopic_obj,    # From pycisTopic with LDA model attached
    menr=menr,                    # Merged cisTarget + DEM results dict
    multi_ome_mode=False,         # CRITICAL for unpaired data
    key_to_group_by="celltype",   # Metadata column for metacell grouping
    nr_cells_per_metacells=5      # Cells sampled per metacell
)

# Step 2: Run SCENIC+ (eRegulon inference)
run_scenicplus(
    scplus_obj,
    variable=["celltype"],
    species="mus_musculus",
    assembly="mm10",
    tf_file="default",
    save_path="scenic_output/",
    biomart_host="http://www.ensembl.org",
    upstream=[1000, 150000],
    downstream=[1000, 150000],
    calculate_TF_eGRN_correlation=True,
    calculate_DEGs_DARs=True,
    export_to_loom_file=True,
    export_to_UCSC_file=True,
    n_cpu=20,
    _temp_dir="scenic_tmp/"
)
```

> **Note:** `run_scenicplus` may not exist in all 1.0a2 builds. If import fails, check the installed package: `python -c "from scenicplus.wrappers import run_scenicplus; print('OK')"`. Alternative: use the CLI commands from `scenicplus.cli.commands`.

### Condition-Specific Metacells (Python API)

```python
# Create composite celltype × condition labels
rna_adata.obs["celltype_condition"] = (
    rna_adata.obs["celltype"].astype(str) + "_" +
    rna_adata.obs["condition"].astype(str)
)
cistopic_obj.cell_data["celltype_condition"] = (
    cistopic_obj.cell_data["celltype"].astype(str) + "_" +
    cistopic_obj.cell_data["condition"].astype(str)
)

# Use composite label for metacell grouping
scplus_obj = create_SCENICPLUS_object(
    GEX_anndata=rna_adata,
    cisTopic_obj=cistopic_obj,
    menr=menr,
    multi_ome_mode=False,
    key_to_group_by="celltype_condition",  # e.g., "cDC1A_WT", "cDC1A_WTposIL12"
    nr_cells_per_metacells=5
)
```

### Adaptive Per-Group Cell Counts

For groups with varying cell counts, pass a dict:

```python
scplus_obj = create_SCENICPLUS_object(
    ...,
    key_to_group_by="celltype_condition",
    nr_cells_per_metacells={
        "CD8apos_cDC1_WT": 10,
        "CD8apos_cDC1_WTposIL12": 10,
        "Chol_cDC2B_WT": 5,         # Smaller group
        "ISG_Mac_Batf3_KO": 5,      # Smaller group
    }
)
```

---

## Standalone pycistarget vs Snakemake

| Approach | When to Use |
|----------|-------------|
| **SCENIC+ Snakemake** | Full GRN workflow, standard parameters |
| **Standalone Python API** | Custom workflows, unpaired data with condition metacells |
| **Standalone pycistarget** | Custom motif analysis, parameter tuning, exploratory cistrome analysis |

For detailed motif enrichment outside the Snakemake pipeline (cisTarget, DEM, cistrome extraction), see [pycistarget skill](../pycistarget-motif-enrichment/SKILL.md).

## Performance Tips

- **Custom databases**: 2-3x better motif recovery than precomputed
- **Memory**: Use `backed='r'` mode for large MuData files
- **Parallel**: Set `--cores 20` in Snakemake
- **Species**: Must match between annotation, databases, and data

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Barcode mismatch | Set `bc_transform_func` in config |
| No eRegulons found | Check `.raw` was saved before normalization |
| Memory errors | Use custom database subset or increase RAM |
| Low motif recovery | Build custom cisTarget database (see [pycistarget skill](../pycistarget-motif-enrichment/SKILL.md)) |
| Unpaired data fails | Set `is_multiome: False` + `key_to_group_by` |
| Too few metacells | Increase `nr_cells_per_metacells` or use coarser annotations |
| Metacell mismatch | Ensure RNA and ATAC annotations use identical label vocabulary |

## Quick Checklist

**For all data:**
- [ ] pycisTopic completed: `cistopic_obj.pkl` + `region_sets/` ready
- [ ] RNA: `.raw` saved BEFORE normalize_total/log1p
- [ ] cisTarget database matches genome version + species
- [ ] Config.yaml paths are absolute
- [ ] Sufficient eRegulons (>50) with good metrics

**For multiome (paired) data:**
- [ ] Barcodes match (or bc_transform_func configured)
- [ ] `is_multiome: True` in config

**For non-multiome (unpaired) data:**
- [ ] `is_multiome: False` in config (or `multi_ome_mode=False` in Python API)
- [ ] `key_to_group_by` set to cell-type annotation column
- [ ] RNA and ATAC annotations use identical label vocabulary
- [ ] ≥50 cells per group for robust metacells

---

## When not to use

- Do not use without pycisTopic + pycistarget prerequisites. Run those skills first.
- Do not use for scRNA-only GRN inference. Use pySCENIC instead.
- Do not use for unpaired RNA/ATAC where cells are not shared. Use scglue-unpaired-multiomics-integration.

---

## See also

- `pycistopic-atac-topic-modeling` — ATAC topic modeling (prerequisite)
- `pycistarget-motif-enrichment` — Standalone motif enrichment
- `cellranger-arc-multiome`
- `scvi-multivi`
- `scenic-r-python-interop` — R → Python data handoff (Signac export, RNA raw preservation)

Upstream docs: https://scenicplus.readthedocs.io/

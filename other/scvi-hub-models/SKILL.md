---
name: scvi-hub-models
description: "Browses and loads pretrained scvi-tools models from the Hugging Face scvi-hub, and picks which scvi variant fits a modality (RNA, CITE-seq, multiome, ATAC, perturbation). Use when loading a HubModel, fetching a reference atlas checkpoint, or minifying a model. It does no surgery — for mapping, hand off to scvi-scarches-reference-mapping."
license: MIT
---

# scvi-hub Pretrained Models Skill

**Foundation:** inherits shared patterns from `scvi-framework`. Jump to:
- `scvi-framework/references/hub-loading.md` — the pull / minification / cache contract
- `scvi-framework/references/scarches-core.md` — what to do after loading a reference
- `scvi-framework/references/interop-matrix.md` — which hub models support scArches
- `scvi-framework/references/gotchas.md`

This file covers only hub-specific concerns: browsing, selection heuristics, minified vs unminified, and upload recipes.

## Overview
scvi-hub hosts pretrained scvi-tools models on Hugging Face Hub for query-to-reference mapping, label transfer, and joint embedding analysis. Key use cases: projecting new data onto atlases, transferring cell type labels, analyzing multi-sample/multi-condition datasets, and querying joint embeddings across modalities.

## Model Selection Guide

| Model | Use Case | Input | Output |
|-------|----------|-------|--------|
| **scVI** | Batch correction, basic integration | scRNA-seq counts | Latent embedding, corrected counts |
| **scANVI** | Label transfer, semi-supervised | scRNA-seq + partial labels | Predicted labels, uncertainty |
| **MrVI** | Multi-sample analysis, sample-level covariates | scRNA-seq + sample metadata | Multi-resolution embeddings, sample effects |
| **totalVI** | CITE-seq integration | RNA + protein counts | Joint latent space, denoised protein |
| **MultiVI** | RNA + ATAC integration | Paired/unpaired multiomics | Joint embedding, imputed modalities |
| **scArches** | Query-to-reference projection | New data + reference model | Projected embedding, transferred labels |
| **PeakVI** | scATAC-seq analysis | Peak counts | Latent embedding, differential accessibility |
| **contrastiveVI** | Perturbation analysis | Control + perturbed | Shared + salient latent spaces |

## Decision Tree

```
Have pretrained reference?
├─ YES → scArches query mapping
└─ NO → Train new model:
    ├─ Single modality (RNA)?
    │   ├─ Need label transfer? → scANVI
    │   ├─ Multi-sample with covariates? → MrVI
    │   └─ Basic integration → scVI
    ├─ CITE-seq (RNA + protein)? → totalVI
    ├─ Multiome (RNA + ATAC)? → MultiVI
    ├─ scATAC-seq only? → PeakVI
    └─ Perturbation study? → contrastiveVI
```

## Loading Pretrained Models

```python
import scvi
from huggingface_hub import hf_hub_download

# Option 1: Direct load from Hub (recommended)
model = scvi.model.SCVI.load("scvi-tools/model-name", adata=query_adata)

# Option 2: Download then load
model_path = hf_hub_download("scvi-tools/model-name", filename="model.pt")
model = scvi.model.SCVI.load(model_path, adata=query_adata)

# Check available models
# https://huggingface.co/scvi-tools
# https://huggingface.co/models?library=scvi-tools
```

## Query-to-Reference Mapping (scArches)

**Purpose**: Project new query data onto existing reference atlas without retraining.

```python
import scanpy as sc
import scvi

# 1. Load reference model (already trained, from Hub)
reference_model = scvi.model.SCVI.load("scvi-tools/human-lung-atlas", adata=reference_adata)

# 2. Prepare query data (MUST match reference var_names)
query_adata = sc.read_h5ad("query.h5ad")
query_adata = query_adata[:, reference_adata.var_names].copy()

# 3. Set up query model using scArches
scvi.model.SCVI.prepare_query_anndata(query_adata, reference_model)
query_model = scvi.model.SCVI.load_query_data(query_adata, reference_model)

# 4. Train on query (few epochs, frozen encoder)
query_model.train(max_epochs=200, plan_kwargs={"weight_decay": 0.0})

# 5. Get joint embedding
query_latent = query_model.get_latent_representation()
query_adata.obsm["X_scVI"] = query_latent

# 6. Transfer labels (if scANVI)
if hasattr(query_model, "predict"):
    query_adata.obs["predicted_celltype"] = query_model.predict()
    query_adata.obs["prediction_uncertainty"] = query_model.predict(soft=True).max(1)
```

## Label Transfer with scANVI

**Purpose**: Semi-supervised integration with cell type label transfer.

```python
import scvi

# 1. Setup with partial labels (use "Unknown" for unlabeled)
adata.obs["celltype_partial"] = adata.obs["celltype"].fillna("Unknown")
scvi.model.SCVI.setup_anndata(adata, batch_key="batch", labels_key="celltype_partial")

# 2. Train scVI first (unsupervised base)
vae = scvi.model.SCVI(adata, n_latent=30, n_layers=2)
vae.train(max_epochs=400)

# 3. Initialize scANVI from scVI
scanvi = scvi.model.SCANVI.from_scvi_model(
    vae,
    unlabeled_category="Unknown",
    labels_key="celltype_partial"
)

# 4. Train scANVI (semi-supervised)
scanvi.train(max_epochs=20, n_samples_per_label=100)

# 5. Predict labels for unlabeled cells
predictions = scanvi.predict()
soft_predictions = scanvi.predict(soft=True)  # Probability matrix

# 6. Get uncertainty (entropy of soft predictions)
import numpy as np
uncertainty = -np.sum(soft_predictions * np.log(soft_predictions + 1e-10), axis=1)
adata.obs["predicted_celltype"] = predictions
adata.obs["prediction_entropy"] = uncertainty

# High uncertainty (>1.0) = ambiguous/novel cell types
```

## Multi-Sample Analysis with MrVI

**Purpose**: Analyze multi-sample datasets with sample-level covariates (genotype, treatment, patient).

```python
import scvi
from scvi.model import MrVI

# 1. Setup with sample key (CRITICAL: sample_key, not batch_key)
scvi.model.MrVI.setup_anndata(
    adata,
    sample_key="sample_id",           # Sample/patient/donor identifier
    categorical_covariate_keys=["condition", "sex"],  # Sample-level covariates
    continuous_covariate_keys=["age"]  # Optional continuous covariates
)

# 2. Train MrVI
mrvi = MrVI(adata)
mrvi.train(max_epochs=400)

# 3. Get multi-resolution embeddings
# Cell-level embedding (for UMAP, clustering)
cell_latent = mrvi.get_latent_representation(give_z=True)
adata.obsm["X_mrvi_z"] = cell_latent

# Sample-level embedding (for sample comparisons)
sample_latent = mrvi.get_latent_representation(give_z=False)
adata.obsm["X_mrvi_u"] = sample_latent

# 4. Analyze sample effects
# Get sample-specific deviations from cell type mean
sample_effects = mrvi.get_local_sample_effects(
    adata,
    groupby="celltype",  # Analyze within each cell type
    batch_size=256
)

# 5. Differential expression between conditions
de_results = mrvi.differential_expression(
    adata,
    groupby="condition",
    group1="treatment",
    group2="control",
    within_group="celltype"  # Stratify by cell type
)
```

## Multi-Condition Experimental Design

**Key insight**: MrVI separates cell-level variation (z) from sample-level variation (u).

```python
# Example: 4 conditions x 3 replicates = 12 samples
# Conditions: WT, KO, WT+stim, KO+stim

# Setup
adata.obs["sample_id"] = adata.obs["replicate"].astype(str) + "_" + adata.obs["condition"]
adata.obs["genotype"] = adata.obs["condition"].str.contains("KO").map({True: "KO", False: "WT"})
adata.obs["stimulation"] = adata.obs["condition"].str.contains("stim").map({True: "stim", False: "unstim"})

scvi.model.MrVI.setup_anndata(
    adata,
    sample_key="sample_id",
    categorical_covariate_keys=["genotype", "stimulation"]
)

mrvi = MrVI(adata)
mrvi.train()

# Compare genotype effect within cell types
de_genotype = mrvi.differential_expression(
    groupby="genotype", group1="KO", group2="WT",
    within_group="celltype"
)

# Compare stimulation effect
de_stim = mrvi.differential_expression(
    groupby="stimulation", group1="stim", group2="unstim",
    within_group="celltype"
)

# Interaction: genotype x stimulation
# Compare KO response to WT response
ko_response = de_stim[de_stim["group"] == "KO"]
wt_response = de_stim[de_stim["group"] == "WT"]
```

## Multiomics Integration

### totalVI (CITE-seq: RNA + Protein)

```python
from scvi.model import TOTALVI

# Setup with protein counts in .obsm
scvi.model.TOTALVI.setup_anndata(
    adata,
    protein_expression_obsm_key="protein_counts",  # Stored in adata.obsm
    batch_key="batch"
)

# Train
totalvi = TOTALVI(adata)
totalvi.train(max_epochs=400)

# Get joint latent space
joint_latent = totalvi.get_latent_representation()
adata.obsm["X_totalVI"] = joint_latent

# Denoised protein expression
denoised_protein = totalvi.get_normalized_expression(
    return_mean=True,
    library_size=1e4
)

# Denoised RNA expression
denoised_rna, denoised_prot = totalvi.get_normalized_expression(
    n_samples=25,
    return_mean=True,
    transform_batch=["batch1"]  # Specific batch or mean across batches
)
```

### MultiVI (RNA + ATAC, paired or unpaired)

**See: [`scvi-multivi`](../scvi-multivi/SKILL.md) for comprehensive documentation.**

MultiVI integrates scRNA-seq, scATAC-seq, and paired multiome data into a shared latent space. Quick setup:

```python
import scvi

# Setup MuData (recommended)
scvi.model.MULTIVI.setup_mudata(
    mdata,
    modalities={"rna_layer": "rna", "atac_layer": "atac"}
)

# Or setup AnnData (features: genes first, then peaks)
scvi.model.MULTIVI.setup_anndata(adata, batch_key="modality")

# Train
model = scvi.model.MULTIVI(mdata, n_genes=4000, n_regions=10000)
model.train(max_epochs=500, adversarial_mixing=True)

# Outputs
adata.obsm["X_multiVI"] = model.get_latent_representation()
imputed_rna = model.get_normalized_expression()  # Imputes for ATAC-only
imputed_atac = model.get_normalized_accessibility()  # Imputes for RNA-only
de_results = model.differential_expression(groupby="cell_type")
da_results = model.differential_accessibility(groupby="cell_type")
```

For full API details, MuData setup, differential analysis, and scArches query mapping, see the dedicated skill, or lookup current API documentation on the web.

## Joint Embedding Analysis

### Querying and Visualization

```python
import scanpy as sc

# After getting latent representation
adata.obsm["X_model"] = model.get_latent_representation()

# UMAP on latent space
sc.pp.neighbors(adata, use_rep="X_model", n_neighbors=30)
sc.tl.umap(adata)
sc.pl.umap(adata, color=["celltype", "batch", "condition"])

# Clustering on latent space
sc.tl.leiden(adata, resolution=0.5)

# Marker genes from latent space clusters
sc.tl.rank_genes_groups(adata, groupby="leiden", method="wilcoxon")
```

### Embedding Queries

```python
import numpy as np
from sklearn.neighbors import NearestNeighbors

# Find similar cells across conditions
latent = adata.obsm["X_model"]
nn = NearestNeighbors(n_neighbors=50, metric="euclidean")
nn.fit(latent)

# Query: find cells most similar to a reference cluster
query_cells = adata[adata.obs["celltype"] == "target_type"].obsm["X_model"]
distances, indices = nn.kneighbors(query_cells)

# Composition analysis: which conditions contain neighbors?
neighbor_conditions = adata.obs["condition"].iloc[indices.flatten()]
condition_counts = neighbor_conditions.value_counts(normalize=True)
```

### Differential Representation

```python
# Compare embedding distributions between conditions
from scipy.stats import mannwhitneyu

latent = adata.obsm["X_model"]
cond1_mask = adata.obs["condition"] == "treatment"
cond2_mask = adata.obs["condition"] == "control"

# Test each latent dimension
pvals = []
for dim in range(latent.shape[1]):
    stat, pval = mannwhitneyu(
        latent[cond1_mask, dim],
        latent[cond2_mask, dim]
    )
    pvals.append(pval)

# Dimensions with significant differences indicate condition-specific variation
```

## Minified Data and Hub Integration

**Minified data**: Compressed representation storing latent embeddings + metadata, not raw counts.

```python
# Save model with minified data (for sharing)
model.save("my_model", save_anndata=True, overwrite=True)
# Creates: model.pt, adata.h5ad (with latent in obsm)

# Load minified model
model = scvi.model.SCVI.load("my_model")
# Note: Raw counts not available, but latent representations work

# Push to Hub
from huggingface_hub import HfApi
api = HfApi()
api.upload_folder(
    folder_path="my_model",
    repo_id="username/my-scvi-model",
    repo_type="model"
)
```

## CELLxGENE Census Integration

```python
import cellxgene_census
import scvi

# Load Census (lazy, streams data)
census = cellxgene_census.open_soma()

# Query specific subset
adata = cellxgene_census.get_anndata(
    census,
    organism="Homo sapiens",
    obs_value_filter="tissue_general == 'lung' and disease == 'normal'",
    var_value_filter="feature_name in ['CD3D', 'CD4', 'CD8A']"
)

# Use pretrained Census model
# Models trained on full Census available at:
# https://huggingface.co/collections/czi-cellxgene/
```

## Perturbation Analysis with contrastiveVI

**Purpose**: Separate shared variation from perturbation-specific effects.

```python
from scvi.model import ContrastiveVI

# Setup with background (control) and target (perturbed)
scvi.model.ContrastiveVI.setup_anndata(
    adata,
    labels_key="perturbation",  # "control" vs "treatment"
)

# Train
cvi = ContrastiveVI(adata, n_salient_latent=10, n_background_latent=30)
cvi.train()

# Get latent spaces
# Background: shared across conditions
background_latent = cvi.get_latent_representation(representation_kind="background")
# Salient: perturbation-specific variation
salient_latent = cvi.get_latent_representation(representation_kind="salient")

# Cells with high salient magnitude = most perturbed
salient_magnitude = np.linalg.norm(salient_latent, axis=1)
adata.obs["perturbation_score"] = salient_magnitude
```

## Critical Setup Requirements

```python
# ALWAYS set random seed for reproducibility
scvi.settings.seed = 42

# Use GPU if available
scvi.settings.dl_num_workers = 4

# Setup anndata BEFORE model creation
# Stores setup in adata.uns["_scvi"]
scvi.model.SCVI.setup_anndata(
    adata,
    layer="counts",           # Use raw counts layer
    batch_key="batch",        # Batch correction
    categorical_covariate_keys=["donor"],  # Additional covariates
)

# Verify setup
print(adata.uns["_scvi"])
```

## Common Pitfalls

1. **Var names mismatch**: Query must have EXACT same genes as reference (use `adata[:, ref_genes]`)
2. **Layer confusion**: Models expect raw counts, not normalized data
3. **Batch key**: Must be categorical, not continuous
4. **Sample vs batch**: MrVI uses `sample_key` (biological), not `batch_key` (technical)
5. **Memory**: Large atlases need `batch_size` parameter; use `scvi.settings.dl_num_workers = 0` if memory issues
6. **Reproducibility**: Set `scvi.settings.seed` before training

## Quick Checklist

- [ ] AnnData has raw counts (not normalized) in `.X` or specified layer
- [ ] Var names match between query and reference
- [ ] Batch/sample keys are categorical strings
- [ ] Random seed set for reproducibility
- [ ] `setup_anndata()` called before model creation
- [ ] GPU enabled if available (`scvi.settings.device = "cuda"`)
- [ ] Model saved with `save_anndata=True` for sharing

---

## When not to use

- Do not use for training scvi models from scratch on your own data. Use scvi-basic or scvi-framework.
- Do not use for non-scvi reference atlases (e.g., Symphony, scPoli-only). Use scvi-scarches-reference-mapping for cross-framework mapping.

---

## See also

- `scvi-framework`
- `scvi-scarches-reference-mapping`
- `treearches-hierarchy-learning`
- `cellxgene-census-annotation`

Upstream docs: https://docs.scvi-tools.org/en/stable/user_guide/use_case/hub.html

---
name: treearches-hierarchy-learning
description: "Learns unified hierarchical cell-type trees across multiple scRNA-seq reference atlases using scArches + scHPL on scVI/scANVI latent spaces. Use when harmonizing conflicting cell-type nomenclatures across references, extending a hierarchy with new labeled data, or detecting novel cell types. For single-reference transfer use scvi-scanvi."
license: MIT
---

# treeArches Hierarchical Cell Type Learning Skill

## Overview

**treeArches** is an extension of scArches that adds hierarchical cell type learning and novel cell type detection capabilities. It combines scVI/scANVI-based reference mapping with scHPL (single-cell Hierarchical Progressive Learning) to:

1. **Learn cell type hierarchies** from multiple reference datasets
2. **Update hierarchies** with new query datasets (when labeled)
3. **Predict labels** for unlabeled query cells
4. **Detect novel cell types** not present in the reference

**Foundation Skills:**
- See `scvi-scarches-reference-mapping.md` for core scArches concepts, installation, surgery patterns, and base model training
- See `scvi-framework.md` for scvi-tools fundamentals

**Part of scArches ecosystem** - uses scVI for latent space integration and scHPL for hierarchy construction.

**Citation:** When using treeArches, cite the [scArches manuscript](https://www.nature.com/articles/s41587-021-01133-0) and the [scHPL manuscript](https://www.nature.com/articles/s41587-021-01107-2).

---

## Installation

treeArches = scArches surgical mapping + scHPL open-set classification.

**Surgery half** — native in scvi-tools (no `scarches` package needed for scVI/scANVI):
SCANVI.load_query_data implements ArchesMixin (the surgery).

**Classification half** — install scHPL standalone:
```bash
pip install --no-deps scHPL newick==1.0.0
# --no-deps: a plain install pulls a pandas downgrade
# newick==1.0.0: scHPL 1.0.5 breaks with newick >= 1.1
#   ('list' object has no attribute 'startswith'), silent until learn_tree()
```
The `scarches` package is optional — install it only for models NOT in scvi-tools
(trVAE, scGen, scPoli). For scVI/scANVI-based treeArches it is not required.

**Optional: FAISS for faster KNN** (recommended for large atlases >100k cells):

```bash
# Linux with GPU
pip install faiss-gpu

# Linux CPU-only
pip install faiss-cpu

# macOS (CPU only)
pip install faiss-cpu
```

---

## When to Use treeArches

### Decision Tree

```
Do you have a reference atlas with cell type labels?
├─ NO → Train reference first (see scvi-scarches-reference-mapping.md)
└─ YES → Continue...

Do you have multiple reference datasets with potentially different cell type nomenclatures?
├─ YES → treeArches (learn unified hierarchy)
└─ NO → Single reference:
    ├─ Need to detect novel cell types in query?
    │   ├─ YES → treeArches (novelty detection)
    │   └─ NO → scANVI may suffice
    └─ Want hierarchical predictions (coarse → fine)?
        ├─ YES → treeArches
        └─ NO → scANVI (see scvi-scarches-reference-mapping.md)
```

### Use Cases

| Scenario | Approach |
|----------|----------|
| Multiple reference studies with different annotations | Learn hierarchy across studies |
| Query may contain disease-specific subtypes | Novelty detection via rejection |
| Need interpretable cell type relationships | Visualize learned tree |
| Annotating atlas with heterogeneous labels | Unify nomenclature hierarchically |
| New rare cell types in specialized tissue | Detect via high rejection rate |

---

## Core Concepts

### Cell Type Hierarchy (scHPL)

scHPL learns a tree structure where:
- **Leaf nodes**: Original cell type labels from individual datasets
- **Internal nodes**: Matched cell types (grouped across datasets)
- **Root**: All cells

Example tree evolution:
```
Step 1: Dataset A       Step 2: Add Dataset B         Step 3: Add Dataset C

    root                     root                          root
    ├─ T_A                   ├─ T (matched A,B)            ├─ T (matched A,B,C)
    ├─ B_A                   ├─ B (matched A,B)            ├─ B (matched A,B,C)
    └─ NK_A                  ├─ NK_A (unmatched)           ├─ NK (matched A,C)
                             └─ Plasma_B (new)             ├─ Plasma_B (unmatched)
                                                           └─ Mast_C (new)
```

### Rejection Mechanism

treeArches uses three rejection types:
1. **Distance rejection**: Cell too far from any training examples
2. **Posterior rejection**: Low classifier confidence
3. **Reconstruction error (RE) rejection**: High scVI reconstruction error

Rejected cells are candidates for:
- Novel cell types not in reference
- Poor quality cells
- Transition/intermediate states
- Batch-specific artifacts

### Two flavors of "does not fit any reference type"

| outcome string | meaning | threshold sensitivity |
|---|---|---|
| "Rejection (dist)" / "Rejected (RE)" | geometrically far from all reference neighbours | THRESHOLD-INVARIANT (pure geometry) |
| "root" | ambiguous between all types; failed the coarsest tree split | GROWS WITH THRESHOLD |

Both mean "flagged / undefined". "root" is the scHPL "couldn't descend the tree" outcome —
NOT a cell type label; never ship it as one.

```python
is_rej     = labels.str.contains("eject", case=False)   # Rejection(dist) / Rejected(RE)
is_root    = labels.eq("root")                           # top-split ambiguity
is_flagged = is_rej | is_root                            # the undefined population
```

### Critical Requirement: Unique Cell Type Labels

**WARNING:** Cell type labels MUST be unique across datasets before hierarchy learning.

```python
# WRONG: Same label "T cells" appears in multiple studies
adata.obs["cell_type"]
# Study1: "T cells", "B cells"
# Study2: "T cells", "Monocytes"

# CORRECT: Concatenate with study identifier
adata.obs["celltype_batch"] = (
    adata.obs["cell_type"].astype(str) + "-" +
    adata.obs["study"].astype(str)
)
# Study1: "T cells-Study1", "B cells-Study1"
# Study2: "T cells-Study2", "Monocytes-Study2"
```

---

## Complete Workflow: Basic Tutorial

This follows the official treeArches tutorial for learning and updating hierarchies.

### Step 1: Train Reference scVI Model

**See `scvi-scarches-reference-mapping.md`** for detailed scVI training. Key points:

```python
import scanpy as sc
import scarches as sca
import numpy as np
import copy as cp

# Load and prepare data
adata = sc.read("pbmc.h5ad")
adata.X = adata.layers["counts"].copy()

# Split into reference and query
target_conditions = ["10X"]  # Query batch
source_adata = adata[~adata.obs.study.isin(target_conditions)].copy()
target_adata = adata[adata.obs.study.isin(target_conditions)].copy()

# HVG selection on reference
source_adata.raw = source_adata
sc.pp.normalize_total(source_adata)
sc.pp.log1p(source_adata)
sc.pp.highly_variable_genes(
    source_adata,
    n_top_genes=2000,
    batch_key="study",
    subset=True
)
source_adata.X = source_adata.raw[:, source_adata.var_names].X

# Train scVI (scArches-compatible parameters) — native scvi-tools, no scarches package needed
import scvi
scvi.model.SCVI.setup_anndata(source_adata, batch_key="batch")

vae = scvi.model.SCVI(
    source_adata,
    n_layers=2,
    encode_covariates=True,
    deeply_inject_covariates=True,
    use_layer_norm="both",      # CRITICAL for scArches
    use_batch_norm="none",      # CRITICAL for scArches
)
vae.train(max_epochs=80)

# Get reference latent representation
reference_latent = sc.AnnData(vae.get_latent_representation())
reference_latent.obs["cell_type"] = source_adata.obs["final_annotation"].tolist()
reference_latent.obs["batch"] = source_adata.obs["batch"].tolist()
reference_latent.obs["study"] = source_adata.obs["study"].tolist()

# Visualize
sc.pp.neighbors(reference_latent, n_neighbors=8)
sc.tl.leiden(reference_latent)
sc.tl.umap(reference_latent)
sc.pl.umap(reference_latent, color=["study", "cell_type"], frameon=False)

# Save reference model
vae.save("ref_model/", overwrite=True)
reference_latent.write("ref_model/ref_latent.h5ad")
```

### Step 2: Learn Cell Type Hierarchy with scHPL

```python
from scHPL import learn, predict

# CRITICAL: Create unique cell type labels per study
reference_latent.obs["celltype_batch"] = (
    reference_latent.obs["cell_type"].astype(str) + "-" +
    reference_latent.obs["study"].astype(str)
)

# Learn hierarchy
# batch_order: order in which studies are added to tree
# classifier: 'knn' (recommended for low-dim), 'svm', or 'svm_occ'
# dynamic_neighbors: adapt k based on cell type size

tree_ref, mp_ref = learn.learn_tree(
    data=reference_latent,
    batch_key="study",
    batch_order=["Freytag", "Oetjen", "Sun"],  # Your study names
    cell_type_key="celltype_batch",
    classifier="knn",
    dynamic_neighbors=True,
    dimred=False,           # Already in latent space
    print_conf=False        # Set True to see confusion matrices
)
# Alternative if scarches installed: sca.classifiers.scHPL.learn_tree(...)

# tree_ref: networkx DiGraph representing hierarchy
# mp_ref: dictionary of trained classifiers per node
```

**Classifier Options:**

| Classifier | Best For | Notes |
|------------|----------|-------|
| `knn` | Low-dimensional (latent space) | Recommended default, fast |
| `svm` | High-dimensional | Linear SVM, slower |
| `svm_occ` | Novelty detection emphasis | One-class SVM per type |

### Step 3: Map Query Data with scArches Surgery

**See `scvi-scarches-reference-mapping.md`** for full surgery details.

```python
# Filter query to same genes as reference
target_adata = target_adata[:, source_adata.var_names].copy()

# Preferred: scvi-tools native (no scarches package required for scVI/scANVI).
# Step 1 trained an SCVI reference into ref_model/, so load the query onto it natively:
import scvi
scvi.model.SCVI.prepare_query_anndata(target_adata, "ref_model/")
model = scvi.model.SCVI.load_query_data(target_adata, "ref_model/")
model.train(max_epochs=50, plan_kwargs={"weight_decay": 0.0})   # weight_decay=0 freezes the reference
# Alternative (scarches package, for trVAE/other scarches-only models):
# model = sca.models.SCVI.load_query_data(target_adata, "ref_model/", freeze_dropout=True)
model.save("surgery_model/", overwrite=True)

# Get query latent representation
query_latent = sc.AnnData(model.get_latent_representation())
query_latent.obs["cell_type"] = target_adata.obs["final_annotation"].tolist()
query_latent.obs["batch"] = target_adata.obs["batch"].tolist()
query_latent.write("query_latent.h5ad")

# Get combined latent representation
target_adata.obs["study"] = "10X"
adata_full = source_adata.concatenate(target_adata, batch_key="ref_query")

full_latent = sc.AnnData(model.get_latent_representation(adata=adata_full))
full_latent.obs["cell_type"] = adata_full.obs["final_annotation"].tolist()
full_latent.obs["batch"] = adata_full.obs["batch"].tolist()
full_latent.obs["study"] = adata_full.obs["study"].tolist()

sc.pp.neighbors(full_latent)
sc.tl.leiden(full_latent)
sc.tl.umap(full_latent)
sc.pl.umap(full_latent, color=["study", "cell_type"], frameon=False)
```

### Step 4a: Update Hierarchy with Labeled Query

If your query dataset has cell type labels, you can update the hierarchy:

```python
# Create unique labels for full dataset
full_latent.obs["celltype_batch"] = (
    full_latent.obs["cell_type"].astype(str) + "-" +
    full_latent.obs["study"].astype(str)
)

# Make a deep copy of original tree
tree_rq = cp.deepcopy(tree_ref)

# Update hierarchy with query
# batch_added: studies already in tree (DO NOT re-add)
# batch_order: new studies to add

tree_rq, mp_rq = learn.learn_tree(
    data=full_latent,
    batch_key="study",
    batch_order=["10X"],                    # Query study to add
    batch_added=["Oetjen", "Freytag", "Sun"],  # Already in tree
    cell_type_key="celltype_batch",
    tree=tree_rq,
    retrain=False,      # Don't retrain existing classifiers
    classifier="knn",
    dimred=False
)
# Alternative if scarches installed: sca.classifiers.scHPL.learn_tree(...)

# New cell types in query will appear as unmatched nodes
# Matched cell types will be grouped with reference types
```

### Step 4b: Predict Labels for Unlabeled Query

If your query dataset is unlabeled:

```python
# scHPL 1.0.5: predict_labels returns (labels_array, posterior_prob_array) — must unpack
y_pred, y_prob = predict.predict_labels(
    query_latent.X,
    tree=tree_ref,
    threshold=0.5  # Rejection threshold (higher = more conservative)
)
query_latent.obs["predicted"]       = np.asarray(y_pred).astype(str)
query_latent.obs["pred_confidence"] = np.asarray(y_prob).reshape(-1)
# Alternative if scarches installed: sca.classifiers.scHPL.predict_labels(...)

# Evaluate against ground truth (if available)
evaluate.heatmap(
    query_latent.obs["cell_type"],
    y_pred,
    shape=[8, 5]  # Figure size
)
# Alternative if scarches installed: sca.classifiers.scHPL.evaluate.heatmap(...)

# Analyze rejection patterns
rejection_rate = (np.asarray(y_pred) == "Rejection").mean()
print(f"Rejection rate: {rejection_rate:.1%}")
```

---

## Advanced Tutorial: Identifying Novel Cell Types

This tutorial shows how to detect disease-specific cell types (e.g., IPF macrophages) not in healthy reference.

### Setup: Load Reference Atlas and Query

```python
import scanpy as sc
import scarches as sca
from scHPL import learn, predict  # standalone scHPL; sca.classifiers.scHPL is an alternative
import numpy as np
import pickle
import copy as cp
import pandas as pd

# Load reference (e.g., Human Lung Cell Atlas)
LCA = sc.read("HLCA_emb_and_metadata.h5ad")

# Load trained classifier (with or without FAISS)
with open("tree_HCLA_FAISS_withRE.pickle", "rb") as f:
    HLCA_tree = pickle.load(f)

# Load query embeddings (from scArches surgery)
emb_ipf = sc.read("Sheppard_2020_emb_LCAv2.h5ad")

# Load query annotations
data_IPF = sc.read("Sheppard_2020_noSC_finalAnno.h5ad")
```

### Option 1: Detect Complete New Cell Types via Hierarchy Update

```python
# Create unique labels combining cell type and condition
data_IPF.obs["ct-batch"] = (
    data_IPF.obs["anno_final"].astype(str) + "-" +
    data_IPF.obs["condition"].astype(str)
)

# Prepare embeddings
emb_ipf = emb_ipf[data_IPF.obs_names]
emb_ipf.obs["ct-batch"] = data_IPF.obs["ct-batch"]
emb_ipf.obs["batch"] = "Query"
emb_ipf.obs["batch2"] = data_IPF.obs["condition"]

# Prepare reference
LCA.obs["ct-batch"] = LCA.obs["ann_finest_level"]
LCA.obs["batch"] = "Reference"
LCA.obs["batch2"] = "Reference"

# Concatenate
LCA_IPF = sc.concat([LCA, emb_ipf])
LCA_IPF.obs["ct-batch"] = LCA_IPF.obs["ct-batch"].str.replace("_", " ")

# Remove small cell types (< 10 cells)
counts = LCA_IPF.obs.groupby("ct-batch").size()
to_remove = counts[counts < 10].index
LCA_IPF = LCA_IPF[~LCA_IPF.obs["ct-batch"].isin(to_remove)]

# Update hierarchy
# This can take ~1 hour for >600k cells
HLCA_tree_updated = learn.learn_tree(
    LCA_IPF,
    batch_key="batch",
    batch_order=["Query"],
    cell_type_key="ct-batch",
    tree=HLCA_tree,
    retrain=False,
    useRE=True,               # Use reconstruction error rejection
    batch_added=["Reference"]
)

# Check for new cell types:
# - Matched nodes: Query types grouped with reference
# - Unmatched nodes: Novel query-specific types
# Example: "Transitioning epithelial cells" added as new node
```

### Option 2: Detect Subtypes via Rejection Analysis

Sometimes a query cell type matches the reference but contains a novel subtype. Detect via rejection:

```python
# scHPL 1.0.5: predict_labels returns (labels_array, posterior_prob_array) — must unpack
y_pred, y_prob = predict.predict_labels(
    emb_ipf.X,
    tree=HLCA_tree,
    threshold=0.5
)
emb_ipf.obs["scHPL_pred"]      = np.asarray(y_pred).astype(str)
emb_ipf.obs["pred_confidence"] = np.asarray(y_prob).reshape(-1)

# Consolidate rejection types
emb_ipf.obs["scHPL_pred"] = emb_ipf.obs["scHPL_pred"].replace({
    "Rejection (dist)": "Rejected",
    "Rejected (RE)": "Rejected"
})

# Analyze by original annotation
for ct in emb_ipf.obs["cell_type"].unique():
    mask = emb_ipf.obs["cell_type"] == ct
    rejected = (emb_ipf.obs.loc[mask, "scHPL_pred"] == "Rejected").mean()
    print(f"{ct}: {rejected:.1%} rejected")

# High rejection rate in specific cell types suggests novel subtypes
```

### Visualize Predictions with Sankey Diagrams

```python
# Install sankey visualization
# pip install plotly

import sankey  # Custom sankey function or use plotly

# Compare annotations to predictions by condition
for condition in ["IPF", "Healthy"]:
    mask = data_macro.obs["condition"] == condition

    sankey.sankey(
        data_macro.obs["anno_final"][mask],
        data_macro.obs["scHPL_pred"][mask],
        save=True,
        name_file=f"sankey_{condition}",
        title=condition,
        title_left="Annotated",
        title_right="Predicted",
        alpha=0.7
    )
```

### Differential Expression on Rejected Cells

Identify markers distinguishing novel subtypes:

```python
# Focus on specific cell type (e.g., Md-M fibrosis in IPF)
mask = (
    (data_macro.obs["condition"] == "IPF") &
    (data_macro.obs["anno_final"] == "Md-M (fibrosis)") &
    data_macro.obs["scHPL_pred"].isin(["Rejected", "Monocyte-derived Mφ"])
)
data_subset = data_macro[mask].copy()

# Normalize for DE
sc.pp.normalize_total(data_subset)
sc.pp.log1p(data_subset)

# Find markers for rejected cells
sc.tl.rank_genes_groups(data_subset, "scHPL_pred", method="t-test")
sc.pl.rank_genes_groups(data_subset, n_genes=25, sharey=False)

# Example: SPP1 highly expressed in rejected IPF macrophages
# SPP1 is known IPF pathogenesis marker
```

### Visualize Novel Subtype Markers

```python
# Create detailed annotation
data_macro.obs["ann_toplot"] = data_macro.obs["ann_finest_level"] + "-Reference"

# Override for query
query_mask = data_macro.obs["study"] == "Sheppard_2020"
data_macro.obs.loc[query_mask, "ann_toplot"] = (
    data_macro.obs.loc[query_mask, "anno_final"] + "-" +
    data_macro.obs.loc[query_mask, "condition"]
)

# Mark rejected IPF cells
rejected_ipf_mask = (
    (data_macro.obs["ann_toplot"] == "Md-M (fibrosis)-IPF") &
    (data_macro.obs["scHPL_pred"] == "Rejected")
)
data_macro.obs.loc[rejected_ipf_mask, "ann_toplot"] = "Md-M (fibrosis)-IPF-(Rejected)"

# Dotplot of novel marker
sc.pl.dotplot(
    data_macro,
    ["SPP1"],  # Novel subtype marker
    groupby="ann_toplot",
    categories_order=[
        # Reference populations
        "Alveolar macrophages-Reference",
        "Monocyte-derived Mφ-Reference",
        # Healthy query
        "Md-M (fibrosis)-Healthy",
        # IPF query (matched + novel)
        "Md-M (fibrosis)-IPF",
        "Md-M (fibrosis)-IPF-(Rejected)",  # Novel subtype
    ],
    figsize=(2, 5),
    save="_IPF_SPP1.pdf"
)
```

---

## Classifier Configuration

### Classifier Selection

```python
from scHPL import learn, predict

# KNN (default, recommended)
tree, mp = learn.learn_tree(
    data=latent,
    classifier="knn",
    dynamic_neighbors=True,  # Adapt k to cell type size
    n_neighbors=15           # Fixed k (ignored if dynamic_neighbors=True)
)

# Linear SVM (for high-dimensional data)
tree, mp = learn.learn_tree(
    data=adata,              # Can use full expression
    classifier="svm",
    dimred=True              # Apply PCA first
)

# One-class SVM (emphasis on novelty detection)
tree, mp = learn.learn_tree(
    data=latent,
    classifier="svm_occ"
)
# Alternative if scarches installed: sca.classifiers.scHPL.learn_tree(...)
```

### Rejection Thresholds

**Threshold controls ONLY the posterior/"root" component — distance/RE is threshold-invariant.**

| threshold | total flagged | dist/RE ("Rejected") | posterior ("root") |
|---|---|---|---|
| 0.5 | ~2.8% | ~2,070 (constant) | ~411 |
| 0.7 | ~5.2% | ~2,070 (constant) | ~2,640 |
| 0.9 | ~9.3% | ~2,070 (constant) | ~6,325 |

- dist/RE: fires when a cell is far from ALL known types — the robust out-of-distribution signal.
- posterior/"root": fires when a cell is hard to call BETWEEN known types — the tunable knob.
Report both components separately; sweep {0.5, 0.7, 0.9} for sensitivity.

```python
# scHPL 1.0.5: predict_labels returns (labels_array, posterior_prob_array) — must unpack
y_pred, y_prob = predict.predict_labels(
    query_latent.X,
    tree=tree,
    threshold=0.5  # Default: 0.5; controls posterior/"root" component only
)
# Alternative if scarches installed: sca.classifiers.scHPL.predict_labels(...)
```

### Using Reconstruction Error

```python
# Enable RE-based rejection (requires trained scVI model)
tree, mp = learn.learn_tree(
    data=latent,
    batch_key="study",
    batch_order=["Study1", "Study2"],
    cell_type_key="celltype_batch",
    classifier="knn",
    useRE=True  # Add reconstruction error rejection
)
# useRE=True: flags cells whose embedding cannot be reconstructed from their kNN neighbours in
# the latent space (high residual = out-of-distribution). This does NOT call the scVI decoder —
# it operates entirely on the embedding matrix, so prediction needs only the latents, not the model.
# Alternative if scarches installed: sca.classifiers.scHPL.learn_tree(...)
```

---

## Saving and Loading Trees

```python
import pickle

# Save tree and classifiers
with open("cell_type_tree.pickle", "wb") as f:
    pickle.dump((tree, mp), f)

# Load tree and classifiers
with open("cell_type_tree.pickle", "rb") as f:
    tree, mp = pickle.load(f)

# Visualize tree structure
import matplotlib.pyplot as plt
import networkx as nx

pos = nx.spring_layout(tree)
nx.draw(tree, pos, with_labels=True, node_size=500, font_size=8)
plt.savefig("cell_type_hierarchy.pdf")
```

---

## Evaluation Utilities

### Confusion Matrix Heatmap

```python
# Compare predictions to ground truth
from scHPL import evaluate
evaluate.heatmap(
    y_true=query_latent.obs["cell_type"],
    y_pred=query_latent.obs["predicted"],
    shape=[10, 8],           # Figure size
    normalize="true",        # Normalize by true labels
    cmap="Blues"
)
# Alternative if scarches installed: sca.classifiers.scHPL.evaluate.heatmap(...)
```

### Per-Class Metrics

```python
from sklearn.metrics import classification_report

# Filter out rejected cells for accuracy calculation
mask = query_latent.obs["predicted"] != "Rejected"
report = classification_report(
    query_latent.obs["cell_type"][mask],
    query_latent.obs["predicted"][mask],
    output_dict=True
)

print(f"Macro F1: {report['macro avg']['f1-score']:.3f}")
print(f"Rejection rate: {(~mask).mean():.1%}")
```

---

## Common Pitfalls and Solutions

| Pitfall | Solution |
|---------|----------|
| Same cell type label in multiple studies | Create unique labels: `cell_type + "-" + study` |
| High rejection rate (>50%) | Lower threshold, check embedding quality, verify surgery epochs |
| Tree not learning matches | Check `batch_order` matches data, ensure >10 cells per type |
| FAISS errors | Install correct version: `faiss-gpu` (Linux+GPU) or `faiss-cpu` |
| Slow hierarchy learning | Subsample data, use FAISS, reduce n_neighbors |
| Inconsistent predictions | Use same classifier settings for tree and prediction |
| AttributeError: 'list' object has no attribute 'startswith' in learn_tree() | newick >= 1.1 breaks scHPL 1.0.5 tree parsing | pip install newick==1.0.0 |
| pandas downgraded / version conflicts after installing scHPL | scHPL/scarches pull an old pandas transitively | pip install --no-deps scHPL |

---

## API Quick Reference

### Hierarchy Learning

```python
# from scHPL import learn, predict
learn.learn_tree(
    data,                    # AnnData with latent representation
    batch_key,               # Column with study/batch IDs
    batch_order,             # List of studies to add (in order)
    cell_type_key,           # Column with cell type labels (must be unique!)
    classifier="knn",        # 'knn', 'svm', 'svm_occ'
    tree=None,               # Existing tree to update (or None to start fresh)
    batch_added=None,        # Studies already in tree (for updates)
    retrain=False,           # Retrain classifiers when updating
    dynamic_neighbors=True,  # Adapt k to cell type size
    n_neighbors=15,          # Fixed k (if dynamic_neighbors=False)
    dimred=False,            # Apply PCA (set True for full expression data)
    useRE=False,             # Use reconstruction error rejection
    print_conf=False         # Print confusion matrices
)
# Alternative if scarches installed: sca.classifiers.scHPL.learn_tree(...)
```

### Label Prediction

```python
# scHPL 1.0.5: returns (labels_array, posterior_prob_array) — must unpack
y_pred, y_prob = predict.predict_labels(
    data,                    # Query latent representation (numpy array)
    tree=tree,               # Learned tree from learn_tree()
    threshold=0.5            # Rejection threshold (controls posterior/"root" only)
)
# Alternative if scarches installed: sca.classifiers.scHPL.predict_labels(...)
```

### Evaluation

```python
# from scHPL import evaluate
evaluate.heatmap(
    y_true,                  # Ground truth labels
    y_pred,                  # Predicted labels
    shape=[8, 5]             # Figure size
)
# Alternative if scarches installed: sca.classifiers.scHPL.evaluate.heatmap(...)
```

---

## Integration with scArches Workflow

treeArches fits into the broader scArches pipeline:

```
1. Train scVI/scANVI on reference → scvi-scarches-reference-mapping.md
2. Learn hierarchy with scHPL     → THIS SKILL
3. Surgery on query               → scvi-scarches-reference-mapping.md
4. Update hierarchy OR predict    → THIS SKILL
5. Analyze novel cell types       → THIS SKILL
```

---

## Resources

- **treeArches Tutorial:** https://docs.scarches.org/en/latest/treearches_pbmc.html
- **treeArches Advanced:** https://docs.scarches.org/en/latest/treearches_identifying_new_ct.html
- **scHPL Paper:** https://www.nature.com/articles/s41587-021-01107-2
- **scArches Paper:** https://www.nature.com/articles/s41587-021-01133-0
- **scArches GitHub:** https://github.com/theislab/scarches
- **scHPL GitHub:** https://github.com/lcmmichielsen/scHPL
- **Foundation Skill:** `scvi-scarches-reference-mapping.md`

---

## When not to use

- Do not use for single-reference label transfer. Use scvi-scanvi or cellxgene-census-annotation.
- Do not use without a pre-trained scVI/scANVI reference model — train one first via scvi-scarches-reference-mapping.

---

## See also

- `scvi-scarches-reference-mapping`
- `scvi-scanvi`
- `scvi-framework`
- `cellxgene-census-annotation`

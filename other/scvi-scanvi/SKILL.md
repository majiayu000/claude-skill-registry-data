---
name: scvi-scanvi
description: scANVI — semi-supervised deep generative model for scRNA-seq with partial cell type labels. Use when you have seed labels (full or partial) and need label transfer with better bio-conservation than scVI alone. Always initialize from a trained scVI model. For unsupervised integration use scvi-basic.
license: MIT
---

# scANVI: Semi-Supervised Label Transfer

**Foundation:** inherits all shared patterns from `scvi-framework`. Jump to:
- `scvi-framework/references/setup-anndata.md` — add `labels_key` and `unlabeled_category` for scANVI
- `scvi-framework/references/training-and-gpu.md`
- `scvi-framework/references/common-outputs.md` — Bayesian DE and `predict()` for label transfer
- `scvi-framework/references/scarches-core.md` — shared query-mapping contract
- `scvi-framework/references/gotchas.md`, `scvi-framework/checks/pre-train-checklist.md`

Always initialize scANVI from a trained scVI model — see `scvi-basic`. This file covers only the parts that differ for scANVI.

## When to Use scANVI

- Partial or complete cell type labels available
- Transfer labels from reference to query
- Better bio-conservation than scVI alone
- Propagate seed labels from marker gene scoring

**Critical:** Always initialize from trained scVI model.

---

## Core Workflow: scVI → scANVI

```python
import scvi

# 1. Train scVI first (unsupervised base)
scvi.model.SCVI.setup_anndata(adata, layer="counts", batch_key="batch")
scvi_model = scvi.model.SCVI(adata, n_layers=2, n_latent=30)
scvi_model.train()

# PLANNING TO USE THIS AS A SURGERY REFERENCE? The base scVI MUST set:
#   use_layer_norm="both"   (LayerNorm stays valid for unseen query batches; BatchNorm does not)
#   use_batch_norm="none"   (frozen BatchNorm stats are wrong for new batches)
#   encode_covariates=True  (batch covariate must enter the encoder for surgery to graft on)
# Omitting any one makes load_query_data() fail or produce a degenerate projection.
# See scvi-scarches-reference-mapping.

# 2. Initialize scANVI from scVI
scanvi_model = scvi.model.SCANVI.from_scvi_model(
    scvi_model,
    labels_key="cell_type",
    unlabeled_category="Unknown"  # Label for cells without annotations
)

# 3. Train scANVI (few epochs needed)
scanvi_model.train(max_epochs=20, n_samples_per_label=100)

# 4. Get predictions
adata.obs["predicted"] = scanvi_model.predict()
adata.obsm["X_scANVI"] = scanvi_model.get_latent_representation()
```

---

## Seed Labeling (from Markers)

Propagate labels from confidently identified cells:

```python
import numpy as np

# Score cells with markers
markers = {"T_cell": ["CD3D", "CD3E"], "B_cell": ["CD19", "MS4A1"]}

# Create seed labels (Unknown for most cells)
seed_labels = np.array(["Unknown"] * adata.n_obs)
for ct, genes in markers.items():
    score = adata[:, genes].X.mean(axis=1).A1  # Mean expression
    top_idx = score.argsort()[-50:]  # Top 50 cells
    seed_labels[top_idx] = ct

adata.obs["seed_labels"] = seed_labels

# Train with seeds
scvi.model.SCVI.setup_anndata(adata, layer="counts", labels_key="seed_labels")
scvi_model = scvi.model.SCVI(adata)
scvi_model.train()

scanvi_model = scvi.model.SCANVI.from_scvi_model(scvi_model, unlabeled_category="Unknown")
scanvi_model.train(max_epochs=25)

adata.obs["predicted"] = scanvi_model.predict()
```

---

## Label Transfer Between Datasets

```python
import anndata

# Combine reference (labeled) and query (unlabeled)
ref_adata.obs["source"] = "reference"
query_adata.obs["source"] = "query"
adata = anndata.concat([ref_adata, query_adata])

# Create transfer labels
adata.obs["transfer_labels"] = "Unknown"
ref_mask = adata.obs["source"] == "reference"
adata.obs.loc[ref_mask, "transfer_labels"] = ref_adata.obs["cell_type"].values

# Train and predict
scvi.model.SCVI.setup_anndata(adata, layer="counts", batch_key="source")
scvi_model = scvi.model.SCVI(adata)
scvi_model.train()

scanvi_model = scvi.model.SCANVI.from_scvi_model(
    scvi_model, labels_key="transfer_labels", unlabeled_category="Unknown"
)
scanvi_model.train()

# Query predictions
query_preds = adata[adata.obs["source"] == "query"].obs["predicted"]
```

---

## Prediction Outputs

```python
# Hard predictions (most likely label)
predictions = scanvi_model.predict()

# Soft predictions (probabilities per class)
probs = scanvi_model.predict(soft=True)

# Uncertainty as entropy
entropy = -(probs * np.log(probs + 1e-10)).sum(axis=1)
adata.obs["uncertainty"] = entropy

# Confidence (max probability)
adata.obs["confidence"] = probs.max(axis=1)
```

---

## Training Parameters

```python
scanvi_model = scvi.model.SCANVI.from_scvi_model(
    scvi_model,
    labels_key="cell_type",
    unlabeled_category="Unknown",
    n_layers=1,  # Classifier layers
)

scanvi_model.train(
    max_epochs=20,
    n_samples_per_label=100,  # SET when any class has <500 cells: otherwise a minibatch may draw
                              # 0-1 cells from a rare class per step, starving its classifier head.
                              # Rule of thumb: use when min(class_count) < 500.
    plan_kwargs={
        "classification_ratio": 50  # Weight of classification loss (default)
        # Low (1-10): prioritize reconstruction
        # High (100+): prioritize classification
    }
)
```

---

## Handling Novel Cell Types

Cells with low confidence may be novel types:

```python
probs = scanvi_model.predict(soft=True)
max_prob = probs.max(axis=1)

# NOTE: scANVI confidence (max softmax probability) is a poor novelty detector.
# Cross-entropy training drives the winning logit far above the rest, so well-trained
# scANVI models routinely report >0.9 for transcriptionally ambiguous or out-of-distribution
# cells. The threshold below is a rough filter only when labels are well-separated in the
# reference; it does NOT reliably detect cells from conditions/states absent during training.
# For open-set novel-cell detection against a reference, use scHPL (treearches-hierarchy-learning)
# — it has an explicit reject class.
# Flag uncertain cells
uncertain = max_prob < 0.5
adata.obs["is_uncertain"] = uncertain

# Subcluster uncertain cells to check for novel populations
uncertain_adata = adata[uncertain]
sc.pp.neighbors(uncertain_adata, use_rep="X_scANVI")
sc.tl.leiden(uncertain_adata, resolution=0.3)
```

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Poor predictions | Ensure scVI trained well first |
| All cells same type | Check label balance; use `n_samples_per_label` |
| Novel types missed | Lower confidence threshold; subcluster uncertain |
| Reference/query mismatch | Same genes, similar normalization |

---

## Resources

- **Docs:** https://docs.scvi-tools.org/en/stable/user_guide/models/scanvi.html
- **Seed Labeling:** https://docs.scvi-tools.org/en/stable/tutorials/notebooks/scrna/seed_labeling.html
- **Paper:** https://www.embopress.org/doi/full/10.15252/msb.20209620

---

## When not to use

- Do not use without any labeled cells. scANVI is semi-supervised — it needs seed labels.
- Do not use on normalized data. Raw counts required.
- Do not use without training scVI first. Always initialize scANVI from scVI.
- Do not use for scATAC-seq or multiome.

---

## See also

- `scvi-framework`
- `scvi-basic`
- `anndata`
- `scvi-scarches-reference-mapping`
- `cellxgene-census-annotation`
- `treearches-hierarchy-learning` — for open-set detection of novel cell types not present in the label set, or for building a hierarchical ontology on top of the scANVI latent space

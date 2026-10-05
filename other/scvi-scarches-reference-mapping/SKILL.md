---
name: scvi-scarches-reference-mapping
description: "scArches architectural surgery to map a query dataset onto an existing scvi-tools reference (scVI, scANVI, totalVI, MultiVI, trVAE): gene padding, adapter layers, fine-tuning with a frozen encoder, weighted-KNN label transfer, and novel-state detection. Use when the reference exists and you want to project queries without retraining."
license: MIT
---

# scArches: Query-to-Reference Mapping

**Foundation:** inherits shared patterns from `scvi-framework`. Jump to:
- `scvi-framework/references/scarches-core.md` — the three mandatory flags and `prepare_query_anndata` / `load_query_data` contract
- `scvi-framework/references/setup-anndata.md`
- `scvi-framework/references/hub-loading.md` — for pretrained references
- `scvi-framework/references/interop-matrix.md` — which scvi models support scArches
- `scvi-framework/references/gotchas.md`, `scvi-framework/checks/pre-train-checklist.md`

This file covers only the advanced parts: architectural surgery, weighted-KNN label transfer, novel-state detection.

## When to Use scArches

- Map query data to existing reference atlas
- Transfer labels without retraining from scratch
- Identify novel cell states not in reference
- Collaborative atlas building

**Two options:**
- `scvi-tools` (native): scVI, scANVI, totalVI, MultiVI — surgery via `load_query_data()`
- `scarches` package: trVAE, scGen, expiMap, scPoli — models not in scvi-tools

treeArches is a workflow (scArches surgery + scHPL), not a separate model — see treearches-hierarchy-learning.

---

## Model Selection

```
Cell type annotation?
├─ With labels → scANVI
└─ Without labels → scVI + KNN transfer

Novel cell states?
└─ treeArches (see treearches-hierarchy-learning.md)

Multimodal?
├─ CITE-seq → totalVI
└─ Multiome → MultiVI
```

---

## Critical scArches Parameters

**MUST use these when training reference model:**

```python
model = scvi.model.SCVI(
    ref_adata,
    use_layer_norm="both",       # REQUIRED
    use_batch_norm="none",       # REQUIRED
    encode_covariates=True,      # REQUIRED
    n_layers=2,
    n_latent=30,
)
```

Without these, surgery will fail or produce poor results.

---

## Core Workflow (scvi-tools Native)

```python
import scvi
import anndata

# ========================================
# 1. TRAIN REFERENCE (with scArches params)
# ========================================
scvi.model.SCVI.setup_anndata(ref_adata, layer="counts", batch_key="batch")

ref_model = scvi.model.SCVI(
    ref_adata,
    use_layer_norm="both",
    use_batch_norm="none",
    encode_covariates=True,
    n_latent=30,
)
ref_model.train()
ref_model.save("ref_model/")

# ========================================
# 2. PREPARE QUERY
# ========================================
# Validates and pads missing genes
scvi.model.SCVI.prepare_query_anndata(query_adata, "ref_model/")

# ========================================
# 3. LOAD QUERY MODEL (surgery)
# ========================================
query_model = scvi.model.SCVI.load_query_data(query_adata, "ref_model/")

# ========================================
# 4. FINE-TUNE (weight_decay=0 preserves reference)
# ========================================
query_model.train(max_epochs=200, plan_kwargs={"weight_decay": 0.0})

# ========================================
# 5. GET JOINT EMBEDDING
# ========================================
query_adata.obsm["X_scVI"] = query_model.get_latent_representation()

# For combined visualization:
full_adata = anndata.concat([query_adata, ref_adata])
full_adata.obsm["X_scVI"] = query_model.get_latent_representation(full_adata)
```

---

## scANVI Reference Mapping (with Labels)

```python
# 1. Train reference scANVI
scvi.model.SCVI.setup_anndata(ref_adata, layer="counts", batch_key="batch")
ref_scvi = scvi.model.SCVI(ref_adata, use_layer_norm="both",
                            use_batch_norm="none", encode_covariates=True)
ref_scvi.train()

ref_scanvi = scvi.model.SCANVI.from_scvi_model(ref_scvi, labels_key="cell_type",
                                                unlabeled_category="Unknown")
ref_scanvi.train(max_epochs=20)
ref_scanvi.save("ref_scanvi/")

# 2. Map query
scvi.model.SCANVI.prepare_query_anndata(query_adata, "ref_scanvi/")
query_scanvi = scvi.model.SCANVI.load_query_data(query_adata, "ref_scanvi/")
query_scanvi.train(max_epochs=100, plan_kwargs={"weight_decay": 0.0})

# 3. Predict labels
query_adata.obs["predicted"] = query_scanvi.predict()
query_adata.obsm["X_scANVI"] = query_scanvi.get_latent_representation()
```

---

## Label Transfer via Weighted KNN

For scVI (no built-in classifier):

```python
from sklearn.neighbors import KNeighborsClassifier

# Get embeddings
ref_latent = ref_model.get_latent_representation(ref_adata)
query_latent = query_model.get_latent_representation(query_adata)

# Train KNN on reference
knn = KNeighborsClassifier(n_neighbors=50, weights="distance")
knn.fit(ref_latent, ref_adata.obs["cell_type"])

# Predict query
query_adata.obs["knn_predicted"] = knn.predict(query_latent)
query_adata.obs["knn_proba"] = knn.predict_proba(query_latent).max(axis=1)
```

---

## Detecting Novel Cell Types

Confidence scores are worth computing, but they are NOT a novelty detector after scArches surgery:

```python
# WARNING: scANVI confidence is NOT a novelty detector after scArches surgery.
# The softmax is a closed simplex over N known classes; with the classifier frozen,
# the reference decision surface is unchanged. Novel treated cells land in the nearest
# known region with near-1.0 confidence (observed: median conf=1.000, <0.5 fraction=0.4%
# across 89k cells). For genuine open-set rejection, use scHPL (treearches-hierarchy-learning).
# Still worth computing as a self-consistency score — but it is not calibrated P(correct).
probs = query_scanvi.predict(soft=True)
conf    = probs.max(axis=1)
entropy = -(probs * np.log(probs + 1e-10)).sum(axis=1)
query_adata.obs["confidence"] = conf
query_adata.obs["entropy"]    = entropy

# Subcluster the FLAGGED cells to characterize candidate novel states. Get the flag from
# scHPL open-set rejection (see treearches-hierarchy-learning), NOT a confidence threshold:
#     query_adata.obs["is_novel"] = scHPL_rejected_mask
novel_adata = query_adata[query_adata.obs["is_novel"]]
sc.pp.neighbors(novel_adata, use_rep="X_scANVI")
sc.tl.leiden(novel_adata, resolution=0.3)
```

---

## scarches Package (Additional Models)

For models not in scvi-tools:

```python
import scarches as sca

# Example: trVAE for strong batch effects
sca.models.TRVAE.setup_anndata(ref_adata, batch_key="batch")
model = sca.models.TRVAE(ref_adata)
model.train()
model.save("trvae_ref/")

# Query mapping
query_model = sca.models.TRVAE.load_query_data(query_adata, "trvae_ref/")
query_model.train(max_epochs=200)
```

See `treearches-hierarchy-learning.md` for novel cell type detection with hierarchy.

---

## HLCA (Human Lung Cell Atlas) Example

```python
from scvi.hub import HubModel

# Load HLCA reference
hmo = HubModel.pull_from_huggingface_hub(
    repo_name="scvi-tools/hlca-human-lung-scvi",
    revision="main"
)
ref_model = hmo.model
ref_adata = hmo.adata

# Map your query
scvi.model.SCVI.prepare_query_anndata(query_adata, ref_model)
query_model = scvi.model.SCVI.load_query_data(query_adata, ref_model)
query_model.train(max_epochs=200, plan_kwargs={"weight_decay": 0.0})

query_adata.obsm["X_scVI"] = query_model.get_latent_representation()
```

---

## Critical Gotchas

| Issue | Solution |
|-------|----------|
| Surgery fails | Reference must use `use_layer_norm="both"`, `use_batch_norm="none"` |
| Gene mismatch | `prepare_query_anndata` handles this; genes padded with zeros |
| Poor mapping | Use `weight_decay=0.0` to preserve reference embedding |
| New batches wrong | Ensure `encode_covariates=True` in reference |
| Wrong var_names order | Query genes reordered automatically by `prepare_query_anndata` |
| `UnpicklingError: Weights only load failed / GLOBAL numpy.core.multiarray._reconstruct` | torch >= 2.6 defaults `weights_only=True`; scvi 1.2.0 checkpoints contain numpy globals | Monkeypatch `torch.load` (snippet below); trusted checkpoints only |

**Environment compatibility — torch >= 2.6 / scvi-tools 1.2.0**

torch 2.6 changed `torch.load()` to default `weights_only=True`. scvi-tools 1.2.0 checkpoints embed numpy globals, so every `SCVI.load()` / `SCANVI.load()` / `load_query_data()` raises `UnpicklingError`. For **your own trusted** checkpoints, restore pre-2.6 behavior before any model load:

```python
# torch >= 2.6 / scvi-tools 1.2.0 incompatibility
# torch 2.6+ made torch.load() default weights_only=True; scvi 1.2.0 checkpoints embed
# numpy globals -> UnpicklingError on every SCVI.load() / SCANVI.load() / load_query_data().
# For YOUR OWN trusted checkpoints, restore pre-2.6 behavior BEFORE any model load:
import torch
_torch_load_orig = torch.load
def _torch_load_trusted(*args, **kwargs):
    kwargs.setdefault("weights_only", False)
    return _torch_load_orig(*args, **kwargs)
torch.load = _torch_load_trusted
# Do NOT use for untrusted third-party checkpoints.
```

---

## Resources

- **scvi-tools:** https://docs.scvi-tools.org/en/stable/tutorials/notebooks/scrna/scarches_scvi_tools.html
- **scarches:** https://docs.scarches.org/
- **HLCA:** https://www.nature.com/articles/s41591-023-02327-2
- **Paper:** https://www.nature.com/articles/s41587-021-01133-0

---

## When not to use

- Do not use for de novo integration without a pretrained reference. Use scvi-basic or scvi-framework.
- Do not use for hierarchical cell-type ontology mapping. Use treearches-hierarchy-learning.

---

## See also

- `scvi-framework`
- `scvi-hub-models`
- `treearches-hierarchy-learning`
- `scvi-scanvi`

Upstream docs: https://docs.scarches.org/en/latest/

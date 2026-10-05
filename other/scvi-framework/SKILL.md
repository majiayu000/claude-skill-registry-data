---
name: scvi-framework
description: "scvi-tools framework foundation and router — installation, a model-selection decision tree, and the shared setup_anndata / train / get_latent_representation contract. Use first when choosing among the scVI variants, or when a cross-cutting concern applies to any scvi-* child (raw counts, batch keys, scArches flags, hub loading, GPU)."
license: MIT
---

# scvi-tools Framework and Router

scvi-tools provides probabilistic models for single-cell omics on PyTorch. Part of the scverse ecosystem (Scanpy, AnnData, MuData).

This skill is the **router** for the scvi-* cluster. Every child skill (scvi-basic, scvi-scanvi, scvi-multivi, scvi-peakvi, scvi-mrvi, scvi-lda, scvi-linearscvi, scvi-contrastivevi, scvi-hub-models, scvi-scarches-reference-mapping) inherits the patterns documented here. When a concern is shared across models, the child skill links to the reference files below rather than restating them.

**Citation:** cite the [scvi-tools manuscript](https://www.nature.com/articles/s41587-021-01206-w) plus the model-specific paper.

---

## Installation

```bash
pip install -U scvi-tools                    # CPU
pip install -U "scvi-tools[cuda]"            # NVIDIA GPU
pip install -U "scvi-tools[metal]"           # Apple Silicon
pip install -U "scvi-tools[tutorials]"       # with scanpy, seaborn, etc.
```

Optional extras: `hub` (HuggingFace), `autotune` (Ray), `jax`, `regseq`.

---

## Model-selection decision tree

```
Have a pretrained reference?
├─ YES → scvi-hub-models → scvi-scarches-reference-mapping
└─ NO  → train new model:
    ├─ scRNA-seq only?
    │   ├─ Label transfer needed?             → scvi-scanvi
    │   ├─ Multi-donor / cohort study?        → scvi-mrvi
    │   ├─ Interpretable gene loadings?       → scvi-linearscvi
    │   ├─ Topic modeling (gene programs)?    → scvi-lda
    │   ├─ Perturbation / case-vs-control?    → scvi-contrastivevi
    │   └─ Basic integration                  → scvi-basic
    ├─ CITE-seq (RNA+protein)?                → totalVI (see upstream docs)
    ├─ 10x Multiome (RNA+ATAC paired)?        → scvi-multivi
    ├─ scATAC-seq only?                       → scvi-peakvi
    └─ Across unpaired RNA+ATAC?              → scglue-unpaired-multiomics-integration (non-scvi)
```

| Model | Modality | Key feature | Skill |
|---|---|---|---|
| scVI | scRNA-seq | Batch correction | `scvi-basic` |
| scANVI | scRNA-seq + labels | Semi-supervised transfer | `scvi-scanvi` |
| MrVI | scRNA-seq + samples | Donor-aware DE | `scvi-mrvi` |
| LinearSCVI | scRNA-seq | Linear decoder, gene loadings | `scvi-linearscvi` |
| AmortizedLDA | scRNA-seq | Topic modeling | `scvi-lda` |
| contrastiveVI | Perturbation scRNA | Salient vs background | `scvi-contrastivevi` |
| MultiVI | Multiome | Joint RNA+ATAC | `scvi-multivi` |
| PeakVI | scATAC-seq | Accessibility embedding | `scvi-peakvi` |
| scArches | Any | Query→reference | `scvi-scarches-reference-mapping` |
| Hub | Any | Pretrained atlases | `scvi-hub-models` |

---

## Shared contract (all children follow this)

```python
Model.setup_anndata(adata, layer="counts", batch_key="batch", ...)
model = Model(adata, n_latent=30)
model.train()
adata.obsm["X_model"] = model.get_latent_representation()
model.save("path/", save_anndata=True)
```

- Raw integer counts are required.
- `batch_key` must be categorical strings.
- Re-run `setup_anndata` after any change to the AnnData shape or dtypes.
- All models save/load with the same API.

---

## Cross-cutting references (load on demand)

| Topic | File |
|---|---|
| `setup_anndata`, batch vs sample vs covariate keys | `references/setup-anndata.md` |
| Training loop, GPU, reproducibility | `references/training-and-gpu.md` |
| Latent, denoised expression, Bayesian DE | `references/common-outputs.md` |
| Critical gotchas (symptom → cause → fix) | `references/gotchas.md` |
| Transitions between models | `references/interop-matrix.md` |
| scArches flags and query projection | `references/scarches-core.md` |
| HuggingFace hub loading | `references/hub-loading.md` |
| Autotune / scib-metrics | `references/hyperparameter-tuning.md` |
| ZINB / NB / Bernoulli / Poisson | `references/count-distributions.md` |
| Growing failure-mode playbook | `references/troubleshooting.md` |

Child skills link directly into these — do not copy-paste their content into a child SKILL.md. If a child needs a different treatment of a shared concern, override locally in that child's SKILL.md and cite the difference.

## Verification and self-evolution

- `scripts/validate_scvi_adata.py` — pre-flight check that any AnnData is ready for `setup_anndata`.
- `checks/pre-train-checklist.md` — 8-item checklist the agent should walk before calling `.train()`.
- `references/troubleshooting.md` — append-only log. Record new failure modes here instead of carving a new skill on first encounter.
- `references/cross-refs.yaml` — curated design record of the intended routing graph for this cluster, kept for reference when writing or auditing each child's `## See also` prose. There is no `metadata.complementary-skills` frontmatter anymore and no validator checks this file against the SKILL.md bodies — it is not enforced, so it can drift from the prose. Treat it as a curated starting point, not ground truth.

---

## Resources

- Docs: https://docs.scvi-tools.org/
- Tutorials: https://docs.scvi-tools.org/en/stable/tutorials/
- API: https://docs.scvi-tools.org/en/stable/api/
- Hub: https://huggingface.co/scvi-tools
- GitHub: https://github.com/scverse/scvi-tools

---

## When not to use

- Do not use this skill alone to run a model. Pair with the specific scvi-* skill for implementation details.
- Do not use for non-probabilistic workflows (plain PCA + Harmony). Use scanpy.

---

## See also

- `scvi-basic`
- `scvi-scanvi`
- `scvi-mrvi`
- `scvi-lda`
- `scvi-linearscvi`
- `scvi-contrastivevi`
- `scvi-multivi`
- `scvi-peakvi`
- `scvi-scarches-reference-mapping`
- `scvi-hub-models`
- `anndata`

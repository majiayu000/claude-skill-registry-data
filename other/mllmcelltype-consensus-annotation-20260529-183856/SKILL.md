---
name: mllmcelltype-consensus-annotation
description: "mLLMCelltype — reference-free cell-type annotation of scRNA-seq clusters by multi-LLM consensus over marker gene lists, with iterative cross-model discussion and per-cluster uncertainty (consensus proportion + Shannon entropy). Use when you have per-cluster marker genes (from scanpy rank_genes_groups or Seurat FindAllMarkers) and want automated, no-reference cell-type labels plus a confidence score to flag clusters for manual review. For label transfer from an annotated atlas use cellxgene-census-annotation; for semi-supervised label propagation from partial labels use scvi-scanvi."
license: MIT
metadata:
  scope: atomic
  requires: []
  skill-author: SciAgent-toolkit
  last-reviewed: 2026-05-24
  version: 0.1.0
  upstream-docs: https://github.com/cafferychen777/mLLMCelltype
  category: annotation
  tier: standard
  tags:
    - annotation
    - mllmcelltype
    - cell-type-annotation
    - llm
    - consensus
    - marker-genes
    - reference-free
    - uncertainty-quantification
    - scrna-seq
  complementary-skills:
    - scanpy
    - cellxgene-census-annotation
    - scvi-scanvi
    - single-cell-rna-qc
  contraindications:
    - "Do not use for label transfer from an annotated reference atlas. Use cellxgene-census-annotation instead."
    - "Do not use for semi-supervised propagation from partial ground-truth labels. Use scvi-scanvi instead."
    - "Do not pass Ensembl IDs (ENSG...) as markers — mLLMCelltype reasons over HGNC/MGI gene symbols. Convert var_names to symbols first."
---

# mLLMCelltype — Multi-LLM Consensus Cell-Type Annotation

## Overview

mLLMCelltype annotates scRNA-seq clusters by sending each cluster's marker gene list to several large language models, then reconciling their predictions through a consensus vote and (for disagreeing clusters) one or more rounds of structured cross-model discussion. It is **reference-free** — no annotated atlas, training, or embedding is required, only a per-cluster marker gene dictionary. Its headline differentiator over single-model LLM annotation and over reference-based transfer is built-in **uncertainty quantification**: every cluster gets a consensus proportion and Shannon entropy that flag low-confidence calls for human review.

**When to use this skill:**
- You have clusters (Leiden/Louvain) and per-cluster marker genes and want cell-type labels without a reference atlas.
- You want a confidence metric per cluster to triage which annotations need manual checking.
- You want to cross-validate annotations across multiple LLM providers rather than trusting one model.

**When NOT to use this skill:**
- You have a matched annotated reference atlas → use `cellxgene-census-annotation`.
- You have partial ground-truth labels to propagate semi-supervised → use `scvi-scanvi`.
- You only need raw clusters / marker genes (the upstream step) → use `scanpy`.

---

## Decision Tree

```
Need cell-type labels for scRNA-seq clusters?
│
├─ Have an annotated reference atlas (CELLxGENE / in-house)?  →  cellxgene-census-annotation
├─ Have partial ground-truth labels to propagate?            →  scvi-scanvi
└─ Reference-free, only marker genes available?
   │
   ├─ Want a fast single label, budget-limited?        →  annotate_clusters (one provider/model)
   └─ Want consensus + uncertainty across models?      →  interactive_consensus_annotation  ← primary path
```

---

## Quick Start

Install the package and the provider extras you need, set API keys, then annotate from a scanpy AnnData.

```bash
pip install "mllmcelltype[openai,anthropic,gemini]"   # add only the providers you use; [all] installs everything
```

```python
import os, scanpy as sc
from mllmcelltype import interactive_consensus_annotation

os.environ["OPENAI_API_KEY"]    = "sk-..."
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-..."
os.environ["GEMINI_API_KEY"]    = "..."

adata = sc.read_h5ad("clustered.h5ad")               # must already have a 'leiden' cluster column
sc.tl.rank_genes_groups(adata, "leiden", method="wilcoxon")

# Build {cluster_id: [top marker symbols]} — IDs preserved exactly as given
marker_genes = {
    cl: adata.uns["rank_genes_groups"]["names"][cl][:10].tolist()
    for cl in adata.obs["leiden"].cat.categories
}

res = interactive_consensus_annotation(
    marker_genes=marker_genes,
    species="human",
    tissue="peripheral blood",
    models=["gpt-5.5", "claude-sonnet-4-6", "gemini-3.1-pro-preview"],
    consensus_threshold=0.7,
    max_discussion_rounds=3,
)

adata.obs["cell_type"]            = adata.obs["leiden"].astype(str).map(res["consensus"])
adata.obs["consensus_proportion"] = adata.obs["leiden"].astype(str).map(res["consensus_proportion"])
adata.obs["entropy"]              = adata.obs["leiden"].astype(str).map(res["entropy"])
```

**Verify it worked:**

```python
# Every cluster received a label and confidence metrics
assert adata.obs["cell_type"].notna().all(), "Unmapped clusters — check that marker keys match leiden categories (str vs int)"
assert set(res["consensus"]) == set(marker_genes), "Cluster set mismatch between input and output"
# Confidence is in-range; flag low-consensus / high-entropy clusters for review
assert adata.obs["consensus_proportion"].between(0, 1).all()
low_conf = {c for c, p in res["consensus_proportion"].items() if p < 0.7}
print("Review these clusters manually:", low_conf)
```

---

## Progressive Depth

### Basic Usage

Single-model annotation (cheapest, no consensus) — useful for a quick first pass or when you only have one API key. The OpenRouter `:free` tier needs no credits.

```python
from mllmcelltype import annotate_clusters

annotations = annotate_clusters(
    marker_genes=marker_genes,
    species="human",
    tissue="peripheral blood",
    provider="openrouter",
    model="deepseek/deepseek-v4-pro:free",   # free, no credits
)  # -> {cluster_id: label}
```

`annotate_clusters` returns a plain `{cluster: label}` dict with **no** uncertainty metrics. Use it for exploration; use `interactive_consensus_annotation` for anything you will report.

### Intermediate Usage

Consensus annotation is the recommended path. Key parameters of `interactive_consensus_annotation`:

| Parameter | Default | Effect |
|---|---|---|
| `models` | provider defaults | List of model names (`"gpt-5.5"`) or provider dicts (`{"provider":"openrouter","model":"meta-llama/llama-4-maverick:free"}`). 3–4 diverse models is the sweet spot. |
| `consensus_threshold` | `0.7` | Agreement proportion below which a cluster is "controversial" and triggers discussion. |
| `entropy_threshold` | `1.0` | Shannon entropy above which a cluster is flagged controversial. |
| `max_discussion_rounds` | `3` | How many cross-model deliberation rounds controversial clusters get. |
| `api_keys` | env vars | Optional `{provider: key}` dict instead of environment variables. |
| `use_cache` / `cache_dir` | `True` | Caches per-model responses; identical re-runs are near-free. Set `force_rerun=True` to bypass. |

The return dict's main keys: `consensus` (final `{cluster: label}`), `consensus_proportion` (`{cluster: 0–1}`), `entropy` (`{cluster: float}`), plus discussion history. See `references/api-reference.md` for the full output schema and `format_discussion_report`.

### Advanced Usage

- **Mixed / OpenRouter models, free tiers, base_urls for proxies** — see `references/api-reference.md`.
- **R / Seurat workflow** (`interactive_consensus_annotation(input = FindAllMarkers_df, tissue_name=..., models=..., api_keys=...)`) — see `references/r-seurat-workflow.md`.
- **Hierarchical / multi-resolution annotation** and **uncertainty-driven re-clustering** of high-entropy clusters — see `references/uncertainty-and-hierarchy.md`.

---

## Verification Checklist

After running this skill, confirm:

- [ ] **Observable check:** `res["consensus"]` has exactly one label per input cluster and `adata.obs["cell_type"]` has no NaN (no key-type mismatch).
- [ ] **Confidence captured:** `consensus_proportion` and `entropy` are mapped into `adata.obs`; clusters with proportion < `consensus_threshold` or entropy > `entropy_threshold` are listed for manual review.
- [ ] **Biological plausibility:** Each label's marker list contains canonical markers for the assigned type (e.g. CD3D/CD3E → T cells); spot-check against `sc.pl.dotplot`.
- [ ] **Input integrity:** Markers were gene **symbols**, not Ensembl IDs, and cluster IDs round-trip back to the original `leiden` categories.

---

## Common Pitfalls

### Pitfall: Ensembl IDs instead of gene symbols
- **Symptom:** Vague or wrong labels ("unknown", generic "cells") across most clusters.
- **Cause:** Markers passed as `ENSG...` IDs; LLMs reason over HGNC/MGI symbols.
- **Fix:** Map to symbols before building the dict: `marker_genes = {c: [sym_map.get(g, g) for g in genes] for c, genes in marker_genes.items()}` using `adata.var["Gene"]` (or biomart).

### Pitfall: Cluster IDs don't map back (silent NaNs)
- **Symptom:** `adata.obs["cell_type"]` is partly/all NaN after `.map()`.
- **Cause:** `leiden` categories are ints/categoricals but result keys are strings (or vice versa).
- **Fix:** Normalize both sides — build markers keyed by `str(cl)` and map with `adata.obs["leiden"].astype(str).map(...)`.

### Pitfall: Missing provider extra / API key
- **Symptom:** `ImportError: cannot import name 'genai'` or a provider auth error mid-run.
- **Cause:** The optional provider library isn't installed, or its env var isn't set.
- **Fix:** `pip install "mllmcelltype[gemini]"` (etc.) and set the matching `*_API_KEY`. To avoid cost/quota surprises start with one provider or an OpenRouter `:free` model.

### Pitfall: Treating consensus labels as ground truth
- **Symptom:** Confidently wrong rare/novel cell types reported without caveat.
- **Cause:** Skipping the uncertainty metrics; consensus across LLMs can still be uniformly wrong.
- **Fix:** Always inspect `entropy` / `consensus_proportion`; manually validate high-entropy clusters with marker dotplots and sub-clustering.

### Pitfall: Repeated full-cost re-runs
- **Symptom:** Every execution re-bills all models even with unchanged input.
- **Cause:** Cache disabled or `force_rerun=True` left on.
- **Fix:** Keep `use_cache=True` with a stable `cache_dir`; only force re-run when models or markers change.

---

## Complementary Skills

| When you need... | Use skill | Relationship |
|---|---|---|
| Clustering + marker genes that feed this skill | `scanpy` | Prerequisite |
| MAD-based QC before clustering | `single-cell-rna-qc` | Prerequisite |
| Label transfer from an annotated atlas instead of reference-free LLM calls | `cellxgene-census-annotation` | Alternative |
| Semi-supervised propagation from partial labels | `scvi-scanvi` | Alternative |

---

## Resources

- **Repository:** https://github.com/cafferychen777/mLLMCelltype
- **Preprint (Yang et al., 2025):** https://doi.org/10.1101/2025.04.10.647852
- **PyPI:** https://pypi.org/project/mllmcelltype/
- **R docs:** https://cafferyang.com/mLLMCelltype/
- **Web app (no install):** https://mllmcelltype.com

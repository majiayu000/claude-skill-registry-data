---
name: cellxgene-census-annotation
description: "Transfer cell-type labels from the CELLxGENE Census to a query scRNA-seq dataset: pull a reference slice keeping its scVI embedding, project the query into that space on CPU, then take a local sklearn KNN vote. Use for supplementary label transfer without the tiledb stack. For cross-atlas embedding search use single-cell-vector-search."
license: MIT
---

# CELLxGENE Census — Cell-Type Annotation via Reference Data

## Purpose

The Census hosts standardized public single-cell atlases (human + mouse) with pre-computed scVI
embeddings, so you can transfer annotations from millions of reference cells without downloading the
underlying H5ADs. The robust route this skill teaches is a **local scVI-projection + KNN vote**:
pull a Census reference slice (keeping its `obsm['scvi']` and `cell_type`), project your query into
that same scVI latent with a frozen forward pass, then vote with a local `sklearn` KNN. This runs on
CPU, needs no `tiledb-vector-search`, and survives Census/scvi-tools version drift.

Treat the Census call as **one supplementary vote** in a larger annotation panel — a bounded
tie-breaker / corroborator, never the sole label source. When the leg fails or the network is
unavailable, degrade cleanly to `census_label = "not_run"`.

## Version facts (checked 2026-07-05)

- `cellxgene-census` **1.18** — the `experimental` submodule carries the embedding-metadata and
  (optional) vector-search helpers.
- `scvi-tools >= 1.1.0` is mandatory (the <1.1 classifier-logits bug corrupts scANVI/label
  uncertainty); the projection route below is validated on scvi-tools 1.2 / 1.4.
- Pin an **LTS `census_version`** for reproducibility (e.g. `"2024-07-01"`). Weekly builds are
  transient; LTS builds persist. Other LTS tags: `"2023-07-25"`, `"2023-12-15"`.
- `s3fs` is needed to fetch the pretrained model (anonymous access to a public CZI bucket).

---

## Core Workflow: local scVI-projection + KNN vote

The whole leg is one guarded function. The four steps are: (1) pull the reference slice keeping its
scVI embedding, (2) resolve + download the pretrained Census scVI model, (3) project the full-gene
query into that scVI space on CPU, (4) fit a local KNN on the reference and predict on the query.

### Step 1 — Reference slice (keep obsm['scvi'] + cell_type)

```python
import cellxgene_census
import cellxgene_census.experimental  # submodule is not auto-imported

census_version = "2024-07-01"                 # LTS, pinned
organism = "mus_musculus"                      # lower_underscore form works for all Census calls
label_attr = "cell_type"

with cellxgene_census.open_soma(census_version=census_version) as census:
    ref = cellxgene_census.get_anndata(
        census,
        organism=organism,
        # TileDB QueryCondition syntax (Python operators), NOT pandas .isin():
        obs_value_filter="tissue_general == 'lung' and is_primary_data == True",
        obs_embeddings=["scvi"],                             # keep the pre-computed scVI embedding
        obs_column_names=[label_attr, "tissue_general"],     # correct kwarg (NOT `attributes=`)
    )

ref_emb = ref.obsm["scvi"].astype("float32")     # the KNN training features — DO NOT discard
ref_lab = ref.obs[label_attr].astype(str).to_numpy()
```

`obs_embeddings=["scvi"]` returns each reference cell's pre-computed scVI latent in `obsm['scvi']`.
Keep it — it is the space the query is projected into and the feature matrix the KNN trains on.

### Step 2 — Resolve + download the pretrained Census scVI model (bare `model.pt`)

The Census scVI contrib model lives at
`s3://cellxgene-contrib-public/models/scvi/<census_version>/<organism>/model.pt`. It is a **bare
~177 MB `model.pt`, not a tar archive** — do not `tarfile.extract` it; the fix is to drop it into a
directory scvi-tools can load (`<dir>/model.pt`). Resolve the link through the experimental API
(it returns an `s3://` URI that `urllib` cannot open directly) and fetch it with anonymous `s3fs`.

```python
from pathlib import Path

def resolve_census_scvi_model(census_version: str, organism: str,
                              cache_dir: str = "objects/census_scvi_model") -> str:
    """Return a directory holding <dir>/model.pt for scvi-tools to load. Cache + skip re-download."""
    cache = Path(cache_dir)
    dst = cache / "model.pt"
    if dst.exists() and dst.stat().st_size > 0:
        return str(cache)                       # already cached
    cache.mkdir(parents=True, exist_ok=True)

    meta = cellxgene_census.experimental.get_embedding_metadata_by_name(
        embedding_name="scvi", organism=organism, census_version=census_version)
    link = meta["model_link"]                   # an s3:// URI, e.g. s3://cellxgene-contrib-public/...model.pt
    _download_s3_object(link, dst)
    assert dst.exists() and dst.stat().st_size > 0, f"model download produced no file at {dst}"
    return str(cache)


def _download_s3_object(s3_uri: str, dst: Path) -> None:
    """Anonymous s3fs (no creds for the public CZI bucket); https-rewrite fallback."""
    assert s3_uri.startswith("s3://"), f"expected s3:// URI, got {s3_uri!r}"
    bucket_key = s3_uri[len("s3://"):]
    try:
        import s3fs
        s3fs.S3FileSystem(anon=True).get(bucket_key, str(dst))
        return
    except Exception:                            # fall through to the https rewrite
        import urllib.request
        bucket, _, key = bucket_key.partition("/")
        urllib.request.urlretrieve(f"https://{bucket}.s3.amazonaws.com/{key}", str(dst))
```

### Step 3 — Project the FULL-GENE query into the Census scVI space (CPU, no training)

The model reconstructs from its own ~8000-gene Ensembl HVG set. Project a **full-gene query object
whose `var_names` are Ensembl IDs**, then let `prepare_query_anndata` pad/reorder to the model's gene
space. A forward-pass projection runs fine on CPU — there is no training and no GPU requirement.

```python
import scvi
import torch
import numpy as np

# torch >= 2.6 defaults torch.load(weights_only=True); the Census checkpoint embeds numpy globals,
# so loading a trusted model needs weights_only=False.
_orig_load = torch.load
torch.load = lambda *a, **k: _orig_load(*a, **{**k, "weights_only": False})

model_dir = resolve_census_scvi_model(census_version, organism)

query.X = query.layers["counts"].copy()          # raw integer counts
query.obs["batch"] = "my_query_batch"            # placeholder for the unseen scArches batch
scvi.model.SCVI.prepare_query_anndata(query, model_dir)   # pads to the model's ~8000 genes
vae_q = scvi.model.SCVI.load_query_data(query, model_dir, accelerator="cpu")
vae_q.is_trained = True                           # frozen encoder: forward pass only, skip fine-tuning
query_latent = vae_q.get_latent_representation().astype("float32")
```

Three caveats decide whether the vote is meaningful:

- **Full-gene, not HVG-subset.** A 2000-HVG query zero-fills ~75% of the model's genes and the
  projection collapses. Feed the full-gene (pre-HVG) query object.
- **Ensembl `var_names`.** The model's var space is Ensembl IDs. Match on Ensembl; symbol-mapping
  puts the query in the wrong gene space and silently degrades the projection.
- **CPU is enough.** `accelerator="cpu"` keeps the GPU free for the heavy training legs; this is a
  frozen forward pass. Supply any placeholder `batch` value — the query batch is unseen by design.

### Step 4 — Local KNN vote (replaces `find_nearest_obs` / `predict_obs_metadata`)

Fit a plain `sklearn` KNN on the reference `(obsm['scvi'], cell_type)` and predict on the projected
query latent. Confidence is the winning class probability. This is the robust default — no
`tiledb-vector-search` dependency, no drifting Census experimental signature.

```python
from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=30, n_jobs=-1).fit(ref_emb, ref_lab)
census_label = knn.predict(query_latent).astype(str)         # -> obs['census_label']
census_conf  = knn.predict_proba(query_latent).max(axis=1)   # -> obs['census_conf']
query.obsm["census_scvi"] = query_latent                     # SANITY UMAP/NN only, not final biology
```

`k = 30` is a robust default (higher k = smoother, more confident vote). Larger references warrant a
larger k. Store `obsm['census_scvi']` for a sanity UMAP; do not treat it as the analysis embedding.

---

## Guarded degrade (the leg must never abort the pipeline)

Because Census is one supplementary vote, wrap the whole leg so any failure (no network, missing
model, API drift, gene-space mismatch) resolves to a `not_run` sentinel with a loud traceback rather
than crashing the run.

```python
import traceback

def run_census(query, cfg) -> dict:
    n = query.n_obs
    not_run = {"census_label": np.full(n, "not_run", dtype=object),
               "census_conf":  np.full(n, np.nan, dtype=float),
               "census_scvi":  None, "ran": False}
    if not cfg.get("enabled", True):
        return not_run
    try:
        # ... Steps 1–4 above ...
        return {"census_label": census_label, "census_conf": census_conf,
                "census_scvi": query_latent, "ran": True}
    except Exception as exc:            # any failure is a clean skip (non-load-bearing leg)
        print(f"WARNING: Census leg failed ({type(exc).__name__}: {exc}) -> census_label='not_run'")
        print(traceback.format_exc())
        return not_run
```

Downstream consumers treat `census_label == "not_run"` as absent: it contributes nothing to any
tally and never labels a cell on its own.

---

## Standalone re-stamp (`CENSUS_ONLY`): recover just this leg cheaply

Once the heavy annotation ensemble has run, you often want to re-run **only** the Census leg — fix a
gene-space bug, bump the `census_version`, or recover a leg that skipped on a transient network
failure — without recomputing the expensive upstream votes. The pattern: load the existing annotated
object, run `run_census` on it, and merge `census_label` / `census_conf` / `obsm['census_scvi']` in
place while asserting the other legs' columns do not move.

```python
import os, anndata as ad

if os.environ.get("CENSUS_ONLY") == "1":
    adata = ad.read_h5ad(out_h5ad)              # the existing annotated checkpoint
    guard = {c: adata.obs[c].astype(str).to_numpy().copy()
             for c in adata.obs.columns if c.startswith("popv_") or c.startswith("scanvi_")}

    census = run_census(adata, census_cfg)      # re-run ONLY this leg
    adata.obs["census_label"] = census["census_label"]
    adata.obs["census_conf"]  = census["census_conf"]
    if census["census_scvi"] is not None:
        adata.obsm["census_scvi"] = census["census_scvi"]

    moved = [c for c, v in guard.items() if not np.array_equal(adata.obs[c].astype(str).to_numpy(), v)]
    assert not moved, f"CENSUS_ONLY moved non-census columns: {moved}"
    adata.write_h5ad(out_h5ad)
```

This is minutes of work versus hours for the full ensemble, and the guard assertion proves the
re-stamp touched only the Census columns.

---

## Vocabulary: Census speaks CELLxGENE ontology — canonicalize before any tally

`census_label` carries **CELLxGENE-ontology cell-type names** ("classical monocyte",
"CD8-positive, alpha-beta T cell"). Those strings will not string-match the labels from other
annotation legs (LungMAP `celltype_level3`, an internal marker vocabulary, a popV panel's
`ref_cell_type`), so a raw Census vote silently never agrees with anything and an N-of-legs
agreement threshold becomes unreachable — the "dead-tally" failure.

Map `census_label` into your shared canonical label space through a **crosswalk normalization
adapter** before it enters a consensus tally. This vocabulary harmonization is its own step, kept
separate from the fusion logic. See `multi-tool-consensus-annotation` for the framework that composes
this leg with the other voters and treats vocabulary harmonization as a first-class stage.

---

## Native Census vector search (optional; version-sensitive)

The Census `experimental` module ships a server-side nearest-neighbour path
(`find_nearest_obs` + `predict_obs_metadata`). It requires `pip install tiledb-vector-search` (an
extra that is frequently absent), and its signature drifts across releases: the old `attributes=`
kwarg is gone — current builds take `column_names=` (or `obs_column_names=`). Use it only when that
dependency is present and pinned; the local-KNN route above is the robust default.

```python
# Requires: pip install tiledb-vector-search   (often NOT installed)
neighbors = cellxgene_census.experimental.find_nearest_obs(
    embedding_name="scvi", organism=organism, census_version=census_version,
    query=query,          # must carry a matching obsm['scvi'] (project it first, as in Step 3)
    k=30, nprobe=20,
)
predictions = cellxgene_census.experimental.predict_obs_metadata(
    organism=organism, census_version=census_version, neighbors=neighbors,
    column_names=["cell_type"],   # NOTE: `attributes=` no longer exists; version-sensitive kwarg
)
```

If this path errors on a missing `tiledb-vector-search` or an unexpected kwarg, fall back to the
local-KNN vote — same inputs, no extra dependency.

---

## Domain context

**Census SOMA hierarchy:**
```
census["census_data"]["mus_musculus"]
    .obs                    # cell metadata (SOMADataFrame)
    .ms["RNA"].var          # gene metadata (Ensembl feature_id)
    .ms["RNA"].X("raw")     # raw counts
```

**Pre-computed embeddings:** `scvi` (continuous latent — the route this skill uses; good for
fine-grained states) and `geneformer` (token-based; better for broad classes, needs its own
tokenization). This skill's vote runs in the `scvi` space.

**Confidence reading:** KNN `predict_proba` max near or below ~0.5 flags a rare/ambiguous/novel cell.
A larger `k` yields smoother, more confident votes but blurs rare states. `is_primary_data == True`
removes technical duplicates (Census stores the same cell across multiple datasets).

---

## Common pitfalls

- **Treating `model.pt` as a tarball** → the S3 object is a bare `model.pt`. Drop it into
  `<dir>/model.pt` and point scvi-tools at `<dir>`; never `tarfile.extract`.
- **`urllib` on the `s3://` model_link** → `model_link` is an `s3://` URI. Use anonymous `s3fs`
  (or rewrite to `https://<bucket>.s3.amazonaws.com/<key>`).
- **HVG-subset query** → zero-fills the model's genes; project the full-gene object (Step 3).
- **Symbol `var_names`** → the model's space is Ensembl; match on Ensembl IDs.
- **Weekly `census_version`** → pin an LTS tag (`"2024-07-01"`) for reproducibility.
- **`torch.load` weights-only error** (torch ≥ 2.6) → patch `weights_only=False` for the trusted
  Census checkpoint (Step 3).
- **Raw Census labels in a tally** → canonicalize via a crosswalk first (see the Vocabulary section).

---

## Resources

- Census docs: https://chanzuckerberg.github.io/cellxgene-census/
- Census Python API: https://chanzuckerberg.github.io/cellxgene-census/python-api.html
- Census models / embeddings: https://cellxgene.cziscience.com/census-models

---

## When not to use

- Do not omit is_primary_data == True filters — Census contains duplicate cells across datasets.
- Do not use pandas .isin() syntax in obs_value_filter — Census uses TileDB QueryCondition syntax.
- Do not project a 2000-HVG query subset through the Census scVI model — it expects the full ~8000-gene Ensembl HVG set and HVG-subsetting zero-fills most model genes, degrading the vote. Project the full-gene query.
- Do not treat census_label as a sole label source — it is a supplementary vote (bounded tie-breaker/corroboration), never load-bearing.

---

## See also

- `single-cell-vector-search` — Alternative; cross-atlas embedding similarity search (SCimilarity / Census)
- `treearches-hierarchy-learning` — Alternative / complement; open-set novelty / hierarchical multi-reference learning
- `scvi-scanvi` — Alternative; semi-supervised label transfer from partial labels
- `scvi-scarches-reference-mapping` — Related (same projection primitive); scArches surgery to map a query onto a reference model
- `multi-tool-consensus-annotation` — Downstream; compose this vote with markers / scANVI / popV / treeArches into a frozen label (this leg is one voter)

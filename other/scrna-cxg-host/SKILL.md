---
name: scrna-cxg-host
description: "Two-phase skill for hosting AnnData on CellxGene over an internal network: Phase A preps the schema (float32 obsm, unique ids, X_umap); Phase B deploys N cellxgene containers behind nginx basic-auth via Docker Compose. Use for wet-lab-facing interactive exploration on an intranet — not one-off .h5ad viewing (cellxgene launch) or public hosting."
license: MIT
---

# scRNA CellxGene Host — schema preparation and Docker deployment

## Overview

Hosting an `.h5ad` on CellxGene for a wet lab needs two things the scanpy → AnnData → `cellxgene launch` path does not provide on its own. First, the AnnData schema must be strict — `obsm` arrays only (no DataFrames), unique `obs.index` (the cell_id) and `var_names`, `X_umap` present, and a `uns['title']`. Skip any of these and the cellxgene server starts but the UI hangs or autosave silently fails. Second, hosting at "the URL the wet lab clicks every morning" means a long-lived service: Docker Compose, a reverse proxy with auth, mounted annotation directories so labelling persists, and host-UID/GID alignment so files do not end up owned by root.

This skill encapsulates both. **Phase A** prepares the schema (and optionally re-embeds per-celltype subsets so the wet lab can pick a focused view). **Phase B** renders Docker / nginx templates and brings the stack up. Both phases are parametric — they do not assume which celltypes you want, which ports are free, or where on the host the data lives.

**When to use this skill:**
- You have an annotated `.h5ad` and a wet lab that wants to explore it interactively
- You want one full-dataset CXG instance + N per-celltype CXG instances on the same internal host
- Annotations made in CXG should persist across container restarts (autosave)
- The deployment must be reproducible and tearable down with one command

**When NOT to use this skill:**
- Throw-away local exploration of one file → `cellxgene launch path.h5ad` is enough
- Public-internet hosting → out of scope; needs SSL termination + harder auth
- Annotation transfer (CellTypist, atlas mapping) → `cellxgene-census-annotation`

---

## Decision Tree

```
Need to share single-cell data with the wet lab?
│
├─ One-off, local, throw-away         →  cellxgene launch <file.h5ad>
├─ Sustained internal hosting          →  THIS SKILL
└─ Public internet                      →  out of scope (SSL + auth hardening)
```

---

## Quick Start

Two phases. Run Phase A interactively; Phase B is a one-shot `docker compose up` after templates render.

> **Pre-finalized deliverable h5ad** (symbols already active as `var_names`, cleaned obs, named 2D UMAPs already present): A.2 (`ensure_unique_varnames`) is a no-op and A.5 (`ensure_umap`) is replaced by A.5b (drop high-dim obsm); the input path is `03_results/objects/<project>_annotated.h5ad`, not a stage checkpoint. Steps A.0, A.1, A.3, A.4, and A.6 still apply.

```python
# Phase A — schema prepare on the full dataset
from prepare_for_cxg import prepare, prepare_subsets

adata_full = prepare(
    in_path="03_results/checkpoints/07_umap.h5ad",
    out_path="03_results/objects/08_explore_full.h5ad",
    title="<ref-multi> • Full Dataset",
)

# Phase A-bis (optional) — re-embed per-celltype
subsets = prepare_subsets(
    in_path="03_results/checkpoints/07_umap.h5ad",
    out_dir="03_results/objects",
    celltype_column="celltype",
    celltypes=["T_cells", "B_cells", "Myeloid"],   # Decision Pause 1 resolves this
    leiden_resolution=0.8,
)
```

```bash
# Phase B — render templates and deploy
cp scripts/env.template .env
$EDITOR .env                                       # set HOSTNAME, UID, GID, paths, ports
./scripts/check_ports.sh                            # Decision Pause 2 — collision probe
python scripts/render_compose.py \
    --datasets full=08_explore_full.h5ad \
               t_cells=09_explore_T_cells.h5ad \
               b_cells=09_explore_B_cells.h5ad \
               myeloid=09_explore_Myeloid.h5ad
htpasswd -c -B annotations/htpasswd <wetlab_user>   # Decision Pause 3
docker compose up -d --build
docker compose ps                                   # 2N containers Up
```

**Verify it worked:**

```bash
curl -fI --user "<wetlab_user>:<password>" http://<HOSTNAME>:8080/
# expect HTTP/1.1 200 OK
docker compose logs cellxgene-full | tail -20      # cellxgene started cleanly
ls -la 03_results/annotation/full/                  # owned by host UID, writable
```

---

## Phase A — Schema preparation

The reference helpers live in `scripts/prepare_for_cxg.py` (ported from the <ref-scrna> `Python_scripts/cxg_utils.py`). Seven steps; run in this order:

### A.0 — Demote pandas extension dtypes to numpy-native

```python
enforce_cxg_dtypes(adata, sanitize_column_names=True)
# Int64 / UInt64 / Float64 / boolean / string  ->  float64 / bool / object
# Applied to obs, var, AND raw.var.  Also renames columns containing '.' -> '_'.
```

CellxGene 1.2.0 ships with `pandas==1.5.3 + numpy==1.23.5` (per the pinned Dockerfile) and **cannot decode pandas-nullable extension arrays at load time**. A single `Int64` column with `pd.NA` survives the .h5ad write through anndata's MaskedArray codec and crashes the cellxgene server with `TypeError: did not understand one of the types; 'None' not accepted`. The most common source is Seurat→AnnData conversion via `anndataR` (integer columns with NA → `Int64`), but pandas ≥ 1.0 will also produce these from any read with nullable inference. This step must run **before** every other Phase A step because some helpers (e.g. `final_checks`) themselves choke on `pd.NA`. **Provenance note:** this step is critical when the h5ad came from anndataR / R-origin conversion (which produces `Int64`/`boolean`/`string` extension dtypes); for Python-native h5ads built with explicit dtype assignments throughout, A.0 is a no-op — harmless to run, not required.

### A.1 — Convert obsm DataFrames to numpy arrays

```python
convert_obsm_to_arrays(adata)
# DataFrames -> np.float32 arrays; column names go to uns[f"{key}_columns"]
```

CellxGene accepts only numeric arrays in `obsm`. AUCell scores often arrive as DataFrames (column = signature name); the column names land in `uns` so they can be reattached in the UI.

### A.2 — Ensure unique `var_names`

```python
ensure_unique_varnames(adata)
# preference order: gene_name → gene_id → existing index; duplicates get __N suffix.
# Reindexes BOTH adata.var AND adata.raw.var (when .raw is set), because
# cellxgene queries dispatch through .raw.X whenever .raw is present and
# the column lookup uses .raw.var.index. Original index preserved in
# var['__orig_var_index'] on each side.
```

### A.3 — Ensure unique barcode and `cell_id` index

```python
ensure_unique_barcode_and_index(adata, joiner="_")
# obs['barcode_raw'] = original; obs['barcode'] = unique; obs.index = obs['barcode'] as string
```

The skill detects whether the barcode already contains `sample_id` as prefix (avoids `<sample-01>_<sample-01>-AAACGCT...`).

### A.4 — Realign aligned mappings

```python
realign_aligned_mappings(adata)
# Any DataFrame in obsm/varm gets its index replaced with the new string cell_id / var index
```

### A.5 — Ensure UMAP

```python
ensure_umap(adata, n_pcs=50)
# Computes PCA → neighbors → UMAP only if missing.
```

### A.5b — Drop non-2D obsm entries

cellxgene exposes every obsm key as a layout option; any array with shape[1] > 2 renders
as a meaningless scatter of its first two components. Run this AFTER A.5: `ensure_umap` may
(re)compute `X_pca` via neighbors, so drop the high-dim latents last.

```python
HIGH_DIM = ["X_pca", "X_scANVI", "X_lsi", "X_nmf"]   # add any project latents
for k in HIGH_DIM:
    if k in adata.obsm and adata.obsm[k].shape[1] > 2:
        del adata.obsm[k]
```

Expose only the 2D embeddings (e.g. `X_umap_unsupervised`, `X_umap_integrated`).

### A.6 — Final checks

```python
final_checks(adata)
# Asserts: obs/var unique, obs['barcode'] unique, at least one X_umap* key each (n,2), index dtypes are 'string'
```

Then write:

```python
adata.uns["title"] = "<project> • <stage>"
adata.write_h5ad("03_results/objects/08_explore_full.h5ad", compression="gzip")
```

Reference: [prepare-schema.md](./references/prepare-schema.md) for the full function bodies and the rationale behind each.

---

## Phase A-bis — Per-celltype subset re-embedding (optional)

Only run when the wet lab wants celltype-specific CXG instances. Each subset gets its own HVG / PCA / UMAP / leiden so the embedding reflects within-celltype structure (e.g., T-cell subpopulation states), not the all-cells structure.

```python
sc.pp.highly_variable_genes(adata_sub, n_top_genes=2000, flavor="seurat", subset=False)
# detect zero-variance genes BEFORE scaling
sc.pp.scale(adata_sub, max_value=10, zero_center=True)
# replace any NaN that scaling introduced with 0 (zero-variance → std=0 → X/0=NaN)
sc.tl.pca(adata_sub, n_comps=30, mask_var="highly_variable")
sc.pp.neighbors(adata_sub, n_pcs=30, n_neighbors=15)
sc.tl.umap(adata_sub)
sc.tl.leiden(adata_sub, resolution=0.8, key_added="leiden_0.8",
             flavor="igraph", n_iterations=2, directed=False)
# Then run Phase A on the subset.
```

The zero-variance handling is load-bearing — `sc.pp.scale` produces `NaN` for any gene with zero variance in the subset, and PCA crashes downstream. Detect before scaling, zero-fill after. Reference: [subset-reembed.md](./references/subset-reembed.md).

---

## Phase B — Docker deployment

Five steps, all driven by `.env`:

### B.1 — Provision `.env`

`scripts/env.template` is a placeholder file. Copy and edit:

```bash
HOSTNAME=cxg.research.example.org
UID=1000        # run `id -u` to fill
GID=1000        # run `id -g`
DATA_HOST_PATH=<project-root>/03_results/objects
ANNOTATIONS_HOST_PATH=<project-root>/03_results/annotation
CXG_PORT_FULL=5005          # internal (container-to-container)
NGINX_PORT_FULL=8080        # external (browser-facing)
CXG_PORT_T_CELLS=5006
NGINX_PORT_T_CELLS=8081
# ... one pair per dataset
```

The skill enforces the `<<placeholder>>` discipline — every project-specific value lives in `.env`, no host paths in version-controlled YAML.

### B.2 — Render templates

`scripts/docker-compose.yml.template` and `scripts/nginx.conf.template` use `<<UID>>`, `<<GID>>`, `<<DATA_HOST_PATH>>`, `<<ANNOTATIONS_HOST_PATH>>`, `<<CXG_PORT_<dataset>>>`, `<<NGINX_PORT_<dataset>>>`, `<<HOSTNAME>>`. A small `render_compose.py` (in `scripts/`) substitutes from `.env` and one `--datasets` argument.

### B.3 — Provision htpasswd

Apache `htpasswd` (bcrypt) tool builds the auth file:

```bash
htpasswd -c -B annotations/htpasswd <wetlab_user>      # one shared user, sufficient for small cohort
# add more users without -c:
htpasswd -B annotations/htpasswd <second_user>
```

### B.4 — `docker compose up -d --build`

Builds the local cellxgene image once; subsequent runs reuse it. Use the battle-tested [`scripts/Dockerfile.cellxgene`](./scripts/Dockerfile.cellxgene) verbatim — it pins `numpy==1.23.5` + `pandas==1.5.3` alongside `cellxgene==1.2.0` and adds a build-time `import` smoke test. Without those pins the build appears to succeed but the container crash-loops at startup with a numpy/pandas ABI mismatch (see "numpy/pandas binary incompatibility" pitfall below).

### B.5 — Verify

```bash
docker compose ps                                  # all 2N services Up
curl -fI --user "$U:$P" http://<HOSTNAME>:<NGINX_PORT_FULL>/
docker compose logs --tail=20 cellxgene-full       # 'INFO: starting on 0.0.0.0:5005'
```

Resource limits per cellxgene container: `30G` memory limit, `8G` reservation. Tune for project size. cellxgene flags: `--backed --annotations-dir /annotations --max-category-items 5000 --host 0.0.0.0 --port <port>`. Reference: [docker-compose-layout.md](./references/docker-compose-layout.md).

---

## Decision Pauses

Four pauses. Pauses 1 and 2 fire on first deploy on every server; Pauses 3 and 4 fire only when the corresponding state (`htpasswd`, host paths) is absent.

### DECISION PAUSE — Subset re-embedding strategy

> **Stop here.** Per-celltype subsets get independent HVG/PCA/UMAP/leiden — only worth doing if the wet lab wants per-celltype CXG instances. Confirm whether to subset, and which subsets.

**Question for the user:** Should I create per-celltype CXG instances? If yes, which celltypes?

| Option | What happens | When to choose | Default |
|--------|--------------|-----------------|---------|
| **A — None** | One CXG instance on the full object only | One overview view is enough; wet lab will filter inside CXG | yes (safest) |
| **B — User-named celltypes** | Skill enumerates distinct values of `obs[<celltype-column>]` (with cell counts), asks which to subset on | Wet lab wants focused per-celltype views and the column names are stable | |
| **C — Custom `obs` filter expressions** | Free-form per-subset filters (e.g., `T_mem: "celltype.startswith('T_') & state=='Memory'"`) | Subsets that don't follow a single column | |

**After the user chooses:** proceed with the chosen option. Append the choice to `analysis_config.yaml` under `decisions.scrna-cxg-host.subsets` so re-runs replay the decision.

### DECISION PAUSE — Port collision check

> **Stop here.** Run `./scripts/check_ports.sh` (`ss -tlnp` based). If any proposed port is occupied, present the conflict and ask the user to remap. Defaults: cellxgene `5005+`, nginx `8080+` (one of each per dataset).

**Question for the user:** Some proposed ports are already in use on the host. How should I remap?

| Option | What happens | When to choose | Default |
|--------|--------------|-----------------|---------|
| **A — Use defaults** | `5005+`/`8080+` per dataset | No conflicts detected | yes (when no conflicts) |
| **B — Auto-remap to free ports** | Skill probes for the next free port above the default range and proposes a remap | Default ports are taken; no policy on which range is allowed | yes (when conflicts detected) |
| **C — User-specified ports** | User names ports explicitly | Strict server policy on which port range is allowed | |

**After the user chooses:** write the resolved ports back to `.env` and `analysis_config.yaml::decisions::scrna-cxg-host::ports`.

### DECISION PAUSE — htpasswd users

> **Stop here.** No `htpasswd` file exists at the configured path. Ask for the basic-auth credentials.

**Question for the user:** Who should be able to access the CXG instances? One shared user is sufficient for a small wet-lab cohort; per-dataset users are also supported.

| Option | What happens | When to choose | Default |
|--------|--------------|-----------------|---------|
| **A — One shared user** | Single `htpasswd` file mounted into all nginx containers | Small wet-lab cohort, low rotation | yes |
| **B — Per-dataset users** | One `htpasswd-<dataset>` file each | Compartmentalised access (PI vs postdoc, etc.) | |
| **C — Defer to existing file** | Skill does not create `htpasswd`; user supplies path | Auth managed elsewhere (LDAP, SSO frontend) | |

**After the user chooses:** the skill prompts for usernames, runs `htpasswd -B -c` for the first and `htpasswd -B` for subsequent. Append `decisions.scrna-cxg-host.htpasswd_strategy` to `analysis_config.yaml`. Passwords are **not** recorded.

### DECISION PAUSE — Server paths

> **Stop here.** Confirm host paths for data (read-only mount) and annotations (read-write mount).

**Question for the user:** Where on this host are the prepared `.h5ad` files and where should annotations be persisted?

The skill suggests `<project>/03_results/objects/` for data and
`<project>/03_results/annotation/<dataset>/` for annotations. Override if the
deployment server keeps data on a different mount (e.g., `/scratch/`, `/data/`).

| Option | What happens | When to choose | Default |
|--------|--------------|-----------------|---------|
| **A — Conventions default** | `<project>/03_results/objects` + `<project>/03_results/annotation/<dataset>` | Project follows `scrna-pipeline-conventions` | yes |
| **B — Custom mount** | User names absolute paths; skill validates they exist and are owned by `UID:GID` | Server keeps data on a non-standard mount | |

**After the user chooses:** write to `.env` and `analysis_config.yaml::decisions::scrna-cxg-host::paths`.

---

### Decision Pause anti-patterns to avoid

- Picking a default silently because "it's faster"
- Trying one option without naming the tradeoff to the user
- Skipping the pause because a previous session's choice is in config — but the data has changed (new dataset added, ports changed on the host) since then
- Promising end-to-end automation while a pause is upcoming

---

## Verification Checklist

After running this skill, confirm:

- [ ] **All `obsm` are arrays.** `all(isinstance(adata.obsm[k], np.ndarray) for k in adata.obsm)` returns `True`.
- [ ] **No NaN in `obsm`.** `all(not np.isnan(adata.obsm[k]).any() for k in adata.obsm if adata.obsm[k].dtype.kind == "f")`.
- [ ] **Unique cell_id and var_names.** `adata.obs.index.is_unique and adata.var_names.is_unique`.
- [ ] **At least one `X_umap*` key present, all (n,2).** `any(k.startswith('X_umap') for k in adata.obsm)` returns True.
- [ ] **Title set.** `"title" in adata.uns`.
- [ ] **Pre-deploy schema check passes.** `python checks/validate_cxg_h5ad.py 03_results/objects/<dataset>.h5ad` exits 0.
- [ ] **All containers Up.** `docker compose ps --format json | jq -r '.[].State' | sort -u` returns only `running`.
- [ ] **Auth works.** `curl -fI --user "$U:$P" http://<HOSTNAME>:<NGINX_PORT_FULL>/` returns `HTTP/1.1 200`. Without auth: `401`.
- [ ] **Annotations directory writable from container.** `docker compose exec cellxgene-full touch /annotations/.test && rm /annotations/.test`.
- [ ] **Resource limits in effect.** `docker stats --no-stream` shows MEM LIMIT `30 GiB` per cellxgene container.

For automated verification: `python checks/validate_cxg_h5ad.py <path-to-h5ad>` (Phase A only).

---

## Common Pitfalls

### Pitfall: pandas extension dtypes survive into the deployed .h5ad

- **Symptom:** cellxgene container starts, then immediately crashes during data-load with:
  ```
  TypeError: did not understand one of the types; 'None' not accepted
  ```
  nginx returns `502`. Five rounds of "replace NaN with placeholders" do not help — because the issue is at the **dtype** level, not the value level.
- **Cause:** `obs` or `var` (or `raw.var`) carries pandas extension dtypes — most commonly `Int64`, `boolean`, or `string` — with `pd.NA` values. anndata serialises these via the MaskedArray codec; the cellxgene 1.2.0 reader (pandas 1.5.3 + numpy 1.23.5) hits `np.dtype(None)` while parsing the column header. `printf` of the column shows nothing wrong because `pd.NA` displays as `<NA>` and the values look clean — only `.dtype` reveals it.
  Common provenance: anndataR Seurat→AnnData conversion (any integer column with NAs becomes `Int64`); pyarrow-backed reads; pandas ≥ 1.0 nullable inference. Dotted column names (`var.features.rank`, `vf_vst_counts_variance.expected`) are a co-occurring smell from R-origin objects.
- **Fix:** Run Phase A.0 (`enforce_cxg_dtypes`). The shipped helper demotes every extension dtype to numpy-native (`Int64` → `float64` with `NaN`, `boolean` → `bool` with `False`-fill, `string` → `object` with `""`-fill), reaches into `.raw.var` the same way `ensure_unique_varnames` does, and sanitises dotted column names by default. The `validate_cxg_h5ad.py` check now flags this BEFORE deploy. Quick triage on a suspect file:
  ```python
  import anndata as ad
  a = ad.read_h5ad("<path>.h5ad")
  for label, df in (("obs", a.obs), ("var", a.var)):
      ext = [(c, df[c].dtype) for c in df.columns
             if str(df[c].dtype) in {"Int64","boolean","string","Float64"}]
      if ext: print(label, ext)
  ```
  If you wrote a custom prepare path that bypasses `prepare()`, call `enforce_cxg_dtypes(adata)` first — every other step assumes numpy-native dtypes.

### Pitfall: numpy/pandas binary incompatibility on cellxgene 1.2.0

- **Symptom:** cellxgene container crash-loops at startup; nginx returns `502 Bad Gateway`. `docker compose logs cellxgene-full` shows, on `import pandas`:
  ```
  ValueError: numpy.dtype size changed, may indicate binary incompatibility.
  Expected 96 from C header, got 88 from PyObject
  ```
- **Cause:** cellxgene 1.2.0's `requirements.txt` only floor-pins numpy (`numpy>1.22`) and ceiling-pins pandas (`pandas<2.0.0`). On `python:3.10-slim` today, pip resolves `numpy==2.x` (latest matching `>1.22`) + `pandas==1.5.x` (latest matching `<2.0`). The pandas 1.5.x wheel was compiled against numpy 1.x C-headers (`PyArray_Descr` = 88 bytes); numpy 2.0 grew that struct to 96 bytes. Pandas blows up at first import. Every dependent process in the container loop-restarts.
- **Fix:** Pin compatible numpy + pandas in the same `pip install` so the wheel resolver picks a single ABI generation. The shipped [`scripts/Dockerfile.cellxgene`](./scripts/Dockerfile.cellxgene) does this:
  ```dockerfile
  RUN pip install --no-cache-dir \
        "numpy==1.23.5" \
        "pandas==1.5.3" \
        "cellxgene==1.2.0"
  RUN python -c "import pandas, numpy; from server.cli.cli import cli"
  ```
  The trailing `python -c` import is a build-time smoke test — if the ABI ever breaks again, `docker compose build` fails fast with a clear error instead of producing a silent crash-loop image.
- **Alternative:** cellxgene 1.3.0 fixes this upstream (pins `numpy==2.0.1` + `pandas>=2.2.2`). Drop the explicit numpy/pandas pins if you bump the cellxgene version.

### Pitfall: var.index left as Ensembl IDs (gene autocomplete returns nothing)

- **Symptom:** Wet lab opens cellxgene, types a gene symbol (e.g. `Itgb2l`) into the gene-search box, and the autocomplete returns nothing. Only Ensembl-id queries (`ENSMUSG00000000157`) work.
- **Cause:** Phase 3 (scanpy QC + processing) typically leaves `var.index = gene_id` and stores symbols in `var['gene_name']`. CellxGene's gene autocomplete uses `var.index` only — it does not search column values. When `.raw` is set, gene queries dispatch through `.raw.X` and the column lookup uses `.raw.var.index`, so `.raw.var` matters separately.
- **Fix:** Run Phase A.2 (`ensure_unique_varnames`). The shipped helper reindexes both `adata.var` and (when set) `adata.raw.var` — the latter via `adata.raw.to_adata()` → set `var_names` → reassign `adata.raw = raw`, since `.raw` is read-only. The original index is preserved as `var['__orig_var_index']` on each side. Verify after `prepare()`:
  ```python
  print(adata.var_names[:3])        # should be symbols, not ENSMUSG...
  print(adata.raw.var_names[:3])    # same
  ```
  If you wrote a custom prepare path that bypasses `ensure_unique_varnames`, replicate the same `to_adata()` → reindex → reassign pattern for `.raw` — reindexing only `.var` leaves cellxgene's autocomplete stuck on Ensembl ids because the `.raw` shadow wins.

### Pitfall: obsm DataFrame left in place

- **Symptom:** cellxgene starts cleanly but the UI hangs or shows an empty embedding panel.
- **Cause:** A pandas DataFrame in `adata.obsm` (e.g., AUCell scores) — CellxGene's schema validator fails silently.
- **Fix:** Run Phase A.1 (`convert_obsm_to_arrays`). The pre-deploy check in `checks/validate_cxg_h5ad.py` catches this.

### Pitfall: `--backed` skipped → OOM on large objects

- **Symptom:** cellxgene container is OOM-killed minutes after start; `docker compose logs` shows the kernel's `Killed` line.
- **Cause:** Without `--backed`, cellxgene loads `X` into memory; a 200k-cell AnnData is ~5–10GB depending on density.
- **Fix:** The shipped compose template includes `--backed`; do not remove. If the container still OOMs, raise `deploy.resources.limits.memory` in `.env` or `compose.yml`.

### Pitfall: htpasswd readable only by root inside container

- **Symptom:** nginx container repeatedly restarts with `auth_basic_user_file ...: Permission denied`.
- **Cause:** Host file permissions on `htpasswd` are `0600` and the container runs as a non-root user.
- **Fix:** `chmod 0644 annotations/htpasswd` on the host. The file mounts read-only; world-readable inside the container is acceptable for the same reason `/etc/passwd` is.

### Pitfall: Annotations dir owned by root from a prior run

- **Symptom:** Wet-lab annotations save in the UI but disappear on container restart, or never persist to disk.
- **Cause:** The annotations host dir was created by a `root`-running container in a previous deploy; the new container, running as `${UID}:${GID}`, cannot write.
- **Fix:** `chown -R $UID:$GID 03_results/annotation/`. The compose template's `user: "${UID}:${GID}"` is what makes this matter — confirm `.env` reflects the host's `id -u`/`id -g`.

### Pitfall: Per-celltype subset re-embed without zero-variance handling

- **Symptom:** `sc.pp.scale` warns `invalid value encountered in sqrt`; subsequent `sc.tl.pca` crashes with `Input contains NaN`.
- **Cause:** Subset has genes with zero expression in every cell → variance 0 → `sqrt(0)=0` → divide-by-zero → NaN.
- **Fix:** Detect zero-variance genes *before* scaling (`gene_vars == 0`), and zero-fill any NaN that survived. The reference helper `prepare_subsets` does this; replicate the pattern in any custom subset code.

### Pitfall: Port already in use

- **Symptom:** `docker compose up` fails with `Bind for 0.0.0.0:8080 failed: port is already allocated`.
- **Cause:** Another service (often a stray cellxgene from a previous session, or another lab's deployment) holds the port.
- **Fix:** Run `./scripts/check_ports.sh` *before* `docker compose up`. The Decision Pause for port collisions surfaces conflicts and proposes remaps before they break the deploy.

### Pitfall: Wet lab edits a celltype label, restart wipes it

- **Symptom:** A user labels cells in CXG, the container is restarted, the labels are gone.
- **Cause:** `--annotations-dir` flag is missing or pointing at a path that is not a Docker-volume-mounted host directory.
- **Fix:** Both must be true: cellxgene is launched with `--annotations-dir /annotations`, and the compose mount has `<host>:/annotations` (read-write). Verify with `docker compose exec cellxgene-full ls /annotations`.

### Pitfall: `BlockingIOError: [Errno 11]` writing h5ad on NFS

- **Symptom:** `adata.write_h5ad(out)` raises `BlockingIOError: [Errno 11] Resource temporarily unavailable`.
- **Cause:** HDF5 default file-locking fails on NFS / network filesystems (advisory locks are unreliable). Common in devcontainers where the project directory is a network mount.
- **Fix:** `export HDF5_USE_FILE_LOCKING=FALSE` before the write (single-writer only).

---

## Resources

- CellxGene Discover: https://cellxgene.cziscience.com/
- cellxgene CLI launch flags: https://cellxgene.cziscience.com/docs/02__Annotate%20Data%20%26%20Maintain%20Their%20Versions
- nginx auth_basic: http://nginx.org/en/docs/http/ngx_http_auth_basic_module.html
- Docker Compose volume + UID semantics: https://docs.docker.com/storage/volumes/
- Reference Docker Compose example (anonymised, in-repo): `01_modules/.ref/<ref-scrna>/cellxgene-deploy/`

---

## When not to use

- Do not use for one-off cellxgene CLI exploration on a single .h5ad. Run cellxgene launch directly.
- Do not use on .h5ad with obsm DataFrames left in place. Phase A must run first; deploying an unprepared file produces 502s and silent autosave failures.
- Do not use for cell-type annotation transfer. Use cellxgene-census-annotation.
- Do not use to expose data on the public internet. The skill ships internal-network templates only; SSL termination + auth hardening are out of scope.

---

## See also

- `anndata` — Prerequisite-adjacent; operate on the `.h5ad` before schema-prep (subset, copy, layer manipulation)
- `scanpy` — Prerequisite; standard scRNA-seq UMAP/leiden pipeline (upstream of subset re-embed)
- `scrna-pipeline-conventions` — Assay convention; canonical AnnData objects and derived-format guarantees
- `scvi-scanvi` — Upstream (often); annotate cell types via reference mapping before hosting
- `cellxgene-census-annotation` — Adjacent / alternative; cell-type annotation transfer from CellxGene Census

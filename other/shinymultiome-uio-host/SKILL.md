---
name: shinymultiome-uio-host
description: 'shinymultiome-uio-host — two-phase skill for hosting a Signac-based 10x Multiome Seurat object on the Eskeland lab ShinyMultiome.UiO web app over an internal network. Phase A: object preflight on the .rds (verify/repair ChromatinAssay Annotation seqlevels, rewrite Fragments paths to container mounts, normalise assay names to peaks/RNA/SCT, optionally compute LinkPeaks and motif footprints, validate group.by columns). Phase B: Docker Compose deployment (R+Bioconductor Shiny container with parameterised global.R + N nginx reverse proxies with htpasswd basic-auth, host UID/GID-aware mounts, deterministic ports, port-collision probe, websocket-aware proxy with extended timeouts for long CoveragePlot redraws). Use when standing up wet-lab–facing chromatin track viewing for an annotated multiome .rds alongside an existing CellxGene RNA instance (the H2 path of multiome-deploy). For RNA-only CXG hosting use scrna-cxg-host. For ATAC-only ArchR-backed Shiny deployment use ShinyArchRUiO directly. For an interactive multi-panel VIP-style RNA+ATAC viewer use cellxgene-VIP.'
license: MIT
metadata:
  scope: implementation
  status: deprecated
  requires: []
  skill-author: SciAgent-toolkit
  last-reviewed: 2026-05-07
  category: workflow
  tier: rich
  version: 0.1.0
  upstream-docs: https://github.com/EskelandLab/ShinyMultiomeUiO
  tags:
  - hosting
  complementary-skills:
  - scrna-cxg-host
  - seurat-multimodal-analysis
  - chromvar-motif-accessibility
  - anndatar-seurat-scanpy-conversion
  - cellranger-arc-multiome
  contraindications:
  - Do not use for RNA-only single-cell hosting. Use scrna-cxg-host.
  - Do not use for ArchR-backed scATAC-only hosting. Deploy ShinyArchRUiO directly (the upstream that this skill's sibling is forked from).
  - Do not use as the primary annotation-autosave instance. ShinyMultiome.UiO is read-only; pair this skill with a scrna-cxg-host CellxGene instance for wet-lab labelling and use this one for ATAC track viewing.
  - Do not use for public-internet hosting. The skill ships internal-network templates only; SSL termination + auth hardening are out of scope.
  - Do not use without first running Phase A. A .rds with stale fragment paths or missing Annotation produces a Shiny app that starts cleanly but renders empty CoveragePlots — the failure is silent.
---

# ShinyMultiome.UiO Host

> **Deprecated (v3.3.0).** Moved to the attic — reference-only; not installed by any role. Revive by moving back to `skills/` and setting `status: stable`.

## Limitations

- **No Factorial Comparison:** The application does not natively support comparing the same clusters between different conditions in a factorial design (e.g., HFD vs LFD for 'B Cells'). It only supports visual comparisons and track rendering between cell types/clusters as defined by a single metadata column. For factorial differential accessibility or multi-condition track overlays, manual R plotting or more complex viewers are required.
- **Read-Only:** ShinyMultiome.UiO is a visualization tool only; it does not support saving new annotations or cell labels back to the object.
- **Single Metadata Focus:** Most tabs are optimized for grouping by a single categorical variable at a time (e.g., cell type or sample).

## Overview

ShinyMultiome.UiO is the Signac-based sister of ShinyArchR.UiO from the Eskeland lab. It takes a Seurat multiome object and serves four tabs (Clustering / Feature of Interest / Coverage Plot / TF Footprinting) over a Shiny frontend. The "10-line README" path runs a single laptop-side `shiny::runApp()` after editing two paths in `global.R` — that is **not** what this skill is for. This skill encapsulates what is missing for a sustained wet-lab deployment: parameterising the hard-coded `global.R` (genome BSgenome import, RDS path, fragments path, assay names), repairing the .rds so chromatin tracks actually render in a container (Annotation seqlevels, fragment file paths, group.by columns), and running the whole stack behind a basic-auth nginx with WebSocket pass-through and timeouts long enough for multi-cell-type track redraws.

This is the H2 deployment of the project's three-horizon multiome plan. It runs **alongside** an existing `scrna-cxg-host` instance: the wet lab labels in CellxGene (autosave) and views chromatin in ShinyMultiome (read-only). Two URLs, one cohort, one shared htpasswd.

**Phase A** prepares the `.rds` (in-place R script). **Phase B** renders Docker / nginx templates and brings the stack up. Both phases are parametric — they do not assume which genome you are on, which assay names your object uses, or where on the host the data lives.

**When to use this skill:**
- You have an annotated multiome Seurat `.rds` (RNA + ATAC ChromatinAssay) and a wet lab that needs ATAC track exploration
- You already deployed (or are about to deploy) `scrna-cxg-host` for RNA-side annotation — this skill is the chromatin counterpart
- The deployment must be reproducible and tearable down with one command
- Your object is on a non-`hg38`/`hg19`/`mm10` genome (e.g., **mm39**) and the upstream hard-coded `BSgenome.Hsapiens.UCSC.hg38` import will not work without parameterisation

**When NOT to use this skill:**
- Throw-away local exploration → edit upstream `global.R` and run `shiny::runApp()` directly
- RNA-only deployment → `scrna-cxg-host`
- ArchR-backed scATAC-only object (no Seurat) → deploy upstream `ShinyArchRUiO` instead
- Wet lab needs annotation persistence inside the chromatin viewer → no — pair with `scrna-cxg-host` and label there
- Public-internet hosting → out of scope

---

## Decision Tree

```
Need to share multiome data with the wet lab?
│
├─ One-off, local, throw-away          →  edit upstream global.R, shiny::runApp()
├─ RNA-only sustained hosting           →  scrna-cxg-host
├─ Multiome sustained hosting,
│  RNA + chromatin tracks, internal     →
│   ├─ Want extended plot library
│   │  (dotplot/GSEA/CLI)?              →  cellxgene-VIP (separate skill)
│   └─ Want Signac-native, low-risk
│      track viewer alongside CXG?      →  THIS SKILL
└─ Public internet                      →  out of scope
```

The "Tool Landscape" comparison this decision tree distils lives at `docs/multiome-deploy/TOOL-LANDSCAPE.md`.

---

## Quick Start

Two phases. Run Phase A interactively in R; Phase B is a one-shot `docker compose up` after templates render.

```r
# Phase A — object preflight (run from R)
source("scripts/prepare_for_shinymultiome.R")

obj <- prepare_for_shinymultiome(
  in_rds        = "03_results/checkpoints/S2_multiome_rough_annot_v8_mm39_validated.rds",
  out_rds       = "03_results/objects/S2_explore_shinymultiome.rds",
  genome_label  = "mm39",
  ensdb_pkg     = "EnsDb.Mmusculus.v107",
  rna_assay     = "RNA",
  atac_assay    = "peaks",   # rename if needed; upstream expects 'peaks'
  fragments_container_dir = "/data/fragments",
  group_by_columns = c("cell_type", "leiden_0.8", "sample_id"),
  compute_links = TRUE,       # LinkPeaks if missing
  compute_motif_footprints = FALSE  # opt-in; expensive
)
```

```bash
# Phase B — render templates and deploy
cp scripts/env.template .env
$EDITOR .env                                      # set HOSTNAME, UID, GID, paths, ports, genome
./scripts/check_ports.sh 8090 8091                # Decision Pause S3 — collision probe (defaults: 8090+)
python scripts/render_compose.py                   # substitutes <<placeholders>>
htpasswd -c -B annotations/htpasswd <wetlab_user>  # Decision Pause S4 — usually shared with scrna-cxg-host
docker compose -f docker-compose.shinymultiome.yml up -d --build
docker compose -f docker-compose.shinymultiome.yml ps
```

**Verify it worked:**

```bash
curl -fI --user "<wetlab_user>:<password>" http://<HOSTNAME>:<NGINX_PORT_SHINYMULTIOME>/
# expect HTTP/1.1 200 OK
docker compose logs shinymultiome | tail -30
# expect: "Listening on http://0.0.0.0:3838"
Rscript checks/validate_signac_rds.R 03_results/objects/S2_explore_shinymultiome.rds
# expect: 0 failures
```

---

## Phase A — Object preflight

Reference helper: `scripts/prepare_for_shinymultiome.R`. Seven steps; run in this order. All are idempotent — re-running them on an already-prepared `.rds` is a no-op.

### A.1 — Assay name normalisation

```r
normalize_assay_names(obj, rna_assay = "RNA", atac_assay = "peaks")
# Renames assays so upstream's hard-coded `DefaultAssay(pbmc) <- "peaks"` and
# `pbmc@assays[["peaks"]]@motifs` lookups work without patching server.R.
```

ShinyMultiome.UiO has `DefaultAssay(pbmc) <- "peaks"` baked into `server.R`. If your object's ATAC assay is called `ATAC` or `chromatin`, the server fails silently when switching to the Coverage tab. Two options: rename the assay in the `.rds` (this step), or fork upstream and parameterise the assay name (more work; not recommended for the default path).

### A.2 — Annotation seqlevels (mm39 / EnsDb path)

```r
ensure_signac_annotation(
  obj,
  ensdb_pkg = "EnsDb.Mmusculus.v107",
  genome    = "mm39",
  seqlevels_style = "UCSC"      # 'chr1', not '1'
)
# If Annotation(obj[["peaks"]]) is NULL or empty, builds from EnsDb.
# Always sets seqlevelsStyle to UCSC and genome(gr) to the requested label.
```

The "fragments are `chr1, chr2, ...` but `Annotation()` is `1, 2, ...`" mismatch is the #1 cause of empty CoveragePlots on mm39. The Signac default for `GetGRangesFromEnsDb` produces Ensembl-style seqlevels; this step always converts to UCSC.

### A.3 — Fragment file paths

```r
rewrite_fragment_paths(
  obj,
  container_dir = "/data/fragments",
  symlink_layout = TRUE          # if FALSE, the function leaves paths absolute
)
# Calls UpdatePath() for every Fragment object.
# Verifies the resolved file + .tbi exist on the *host* before saving.
```

The Fragment object stores absolute paths from the analysis machine. Inside the container those paths do not exist. This step rewrites them to the bind-mount path (default `/data/fragments`). The verification check is host-side — it cannot see the container yet — so it tests the host paths the bind-mount will expose.

### A.4 — group.by column validation

```r
validate_group_columns(
  obj,
  required = c("cell_type", "leiden_0.8", "sample_id"),
  max_values_per_column = 60     # ShinyMultiome.UiO becomes laggy beyond ~60
)
# Errors loudly if a required column is missing or has too many distinct values.
```

ShinyMultiome.UiO renders one CoveragePlot lane per group. Above ~60 cell types the plot becomes unreadable and the redraw exceeds nginx's default timeout. Either coarsen the grouping or remove that column from the dropdown.

### A.5 — Optional: LinkPeaks

```r
if (compute_links && length(Links(obj[[atac_assay]])) == 0) {
  obj <- Signac::LinkPeaks(
    obj, peak.assay = atac_assay, expression.assay = rna_assay,
    genes.use = NULL    # or a vector of marker genes for speed
  )
}
# Populates Links(obj). Coverage tab will overlay these as arcs.
```

Skip this if the wet lab does not need peak–gene link arcs. It is computationally heavy (10–60 min for a 50k-cell object).

### A.6 — Optional: motif scan + footprint precompute

```r
if (compute_motif_footprints) {
  obj <- Signac::AddMotifs(obj, genome = bsgenome_obj, pfm = jaspar_pfms)
  obj <- Signac::Footprint(obj, motif.name = motifs_of_interest, genome = bsgenome_obj)
}
```

Required for the **TF Footprinting** tab. Expensive (1–4 hours depending on motif count). The skill defaults to **off**; turn on if the footprint tab is part of the wet-lab deliverable. Reference: [`references/footprint-precompute.md`](./references/footprint-precompute.md).

### A.7 — Save

```r
saveRDS(obj, out_rds)
# Verify:
Rscript checks/validate_signac_rds.R out_rds
```

The validator (Phase A's automated check) asserts: assays named correctly, Annotation present and UCSC-styled, fragment paths point at files reachable from `<host_path_corresponding_to_container_mount>`, group.by columns present, optionally Links populated, optionally Motif slot populated.

Reference: [`references/signac-multiome-object-shape.md`](./references/signac-multiome-object-shape.md) for the full schema invariants and rationale per step.

---

## Phase B — Docker deployment

Five steps, all driven by `.env`:

### B.1 — Provision `.env`

`scripts/env.template` is a placeholder file. Copy and edit:

```bash
HOSTNAME=cxg.research.example.org
UID=1000        # run `id -u`
GID=1000        # run `id -g`
RDS_HOST_PATH=/scratch/<project>/03_results/objects
RDS_FILENAME=S2_explore_shinymultiome.rds
FRAGMENTS_HOST_PATH=/scratch/<project>/03_results/fragments
ANNOTATIONS_HOST_PATH=/scratch/<project>/03_results/annotation
SHINY_PORT=3838
NGINX_PORT_SHINYMULTIOME=8090
GENOME_LABEL=mm39
BSGENOME_PKG=BSgenome.Mmusculus.UCSC.mm39
ENSDB_PKG=EnsDb.Mmusculus.v107
RNA_ASSAY=RNA
ATAC_ASSAY=peaks
DEFAULT_REGION=Spp1
PROJECT_NAME=<ref-multi>
```

Every project-specific value lives in `.env`, no host paths in version-controlled YAML.

### B.2 — Render templates

`scripts/docker-compose.shinymultiome.yml.template`, `scripts/nginx-shinymultiome.conf.template`, and `scripts/overlay/global.R.template` use `<<UID>>`, `<<GID>>`, `<<RDS_HOST_PATH>>`, `<<FRAGMENTS_HOST_PATH>>`, `<<SHINY_PORT>>`, `<<NGINX_PORT_SHINYMULTIOME>>`, `<<GENOME_LABEL>>`, `<<BSGENOME_PKG>>`, `<<RDS_FILENAME>>`, `<<RNA_ASSAY>>`, `<<ATAC_ASSAY>>`, `<<HOSTNAME>>`. `render_compose.py` substitutes from `.env`.

### B.3 — Provision htpasswd

Reuse the same `htpasswd` file as the H1 `scrna-cxg-host` deploy when both stacks share users (the recommended default).

```bash
# Reuse:
ln -s ../../scrna-cxg-host/annotations/htpasswd annotations/htpasswd
# Or create a separate one:
htpasswd -B -c annotations/htpasswd <wetlab_user>
```

### B.4 — `docker compose -f docker-compose.shinymultiome.yml up -d --build`

Builds the local R+Bioconductor+Signac image once (slow first time, 30–60 min — `bioconductor/bioconductor_docker:RELEASE_3_19` plus `BSgenome.<species>.UCSC.<assembly>` pulls). Subsequent runs reuse the image.

The Dockerfile installs:
- R 4.4 (from bioconductor base image)
- Seurat 5.x, Signac 1.13+
- The genome-specific BSgenome package named by `BSGENOME_PKG`
- The matching EnsDb package named by `ENSDB_PKG`
- shiny, shinybusy, shinyBS, viridis, patchwork, ggplot2

The shiny app code is **vendored from upstream `EskelandLab/ShinyMultiomeUiO`** at a pinned commit (see [`scripts/overlay/README.md`](./scripts/overlay/README.md) for the pin and how to bump it). The skill ships a small overlay (`global.R.template`) that replaces upstream's hard-coded `library(BSgenome.Hsapiens.UCSC.hg38)`, hard-coded `seuratObject` path, and hard-coded `fragFilePath` with `.env`-driven values.

Reference: [`references/dockerfile-design.md`](./references/dockerfile-design.md).

### B.5 — Verify

```bash
docker compose -f docker-compose.shinymultiome.yml ps   # 2 services Up (shinymultiome + nginx-shinymultiome)
curl -fI --user "$U:$P" http://<HOSTNAME>:<NGINX_PORT_SHINYMULTIOME>/
docker compose logs --tail=30 shinymultiome             # 'Listening on http://0.0.0.0:3838'
```

In a browser:
- Clustering tab renders dim-reduction plots ✓
- Coverage Plot tab: enter a known-open gene, tracks render per `group.by` value ✓
- Feature of Interest tab: switch assay between `RNA` / `peaks` / `SCT`, plots redraw ✓
- TF Footprinting tab: only if A.6 was run; otherwise the dropdown will be empty (acceptable) ✓

Resource limits per shinymultiome container: tune by cell count — see "Memory Profile" in [`references/shiny-memory-and-timeouts.md`](./references/shiny-memory-and-timeouts.md). Default `memory: 32G` works up to ~80k cells; bump to `64G` for 80–200k.

---

## Decision Pauses

Six pauses. S1, S3, S4, S5 fire on first deploy; S2 fires when the .rds's assays do not match upstream's expectations; S6 fires only when Phase A.6 is being considered.

### DECISION PAUSE — Genome / BSgenome choice (S1)

> **Stop here.** Upstream ShinyMultiome.UiO hard-codes `library(BSgenome.Hsapiens.UCSC.hg38)`. Any other genome requires the matching BSgenome package to be installed in the container. The skill emits the package name into the rendered `global.R` based on `.env::BSGENOME_PKG` and into the Dockerfile's R-install step.

**Question for the user:** Which genome was the alignment done against?

| Option | What happens | When to choose | Default |
|--------|--------------|-----------------|---------|
| **A — `mm39` (`BSgenome.Mmusculus.UCSC.mm39`)** | Mouse mm39 / GRCm39, EnsDb.Mmusculus.v107+ | Project's S2 object | yes (project default) |
| **B — `hg38` (`BSgenome.Hsapiens.UCSC.hg38`)** | Human hg38 / GRCh38 — upstream default | Human PBMC / tissue, GRCh38 | |
| **C — `mm10` / `hg19` / other** | Older genomes; matching BSgenome may already be installed | Legacy datasets | |
| **D — Custom assembly** | Provide a path to a locally built BSgenome `.tar.gz`; skill installs in Dockerfile | Non-standard genome | |

**After the user chooses:** write `BSGENOME_PKG`, `ENSDB_PKG`, `GENOME_LABEL` to `.env` and `analysis_config.yaml::decisions::shinymultiome-uio-host::genome`.

### DECISION PAUSE — Assay name conventions (S2)

> **Stop here.** Upstream `server.R` has `DefaultAssay(pbmc) <- "peaks"` hard-coded for the Coverage and Footprint tabs, and `RNA` / `SCT` hard-coded in the Feature tab. The .rds assays must match these names exactly, or the tabs render empty.

**Question for the user:** The .rds assay names are `<detected list>`. The upstream expects `peaks` (ATAC) and `RNA`/`SCT` (expression). How should I reconcile?

| Option | What happens | When to choose | Default |
|--------|--------------|-----------------|---------|
| **A — Rename in the .rds** | `DefaultAssay()` swap + `RenameAssays()` in Phase A.1; saves a new `.rds`. Lossless. | Object only used downstream by this skill | yes |
| **B — Fork upstream and parameterise** | Patch `server.R` and `ui.R` to read assay names from a config; vendored in `scripts/overlay/`. | Object is shared with other tools that depend on the original assay names | |
| **C — Keep both** | Phase A.1 leaves the original assay AND adds a copy under the upstream name | Conservative; adds memory overhead | |

**After the user chooses:** record `RNA_ASSAY` and `ATAC_ASSAY` (the names *in the deployed .rds*) in `.env`. Append `decisions.shinymultiome-uio-host.assay_strategy` to `analysis_config.yaml`.

### DECISION PAUSE — Port collision check (S3)

> **Stop here.** Run `./scripts/check_ports.sh 8090 8091` (`ss -tlnp` based). Defaults: nginx-shinymultiome `8090`. If `scrna-cxg-host` is already on `8080+`, the proposed `8090` block is one above the standard CXG range to avoid collision.

| Option | What happens | When to choose | Default |
|--------|--------------|-----------------|---------|
| **A — Use defaults (8090)** | Single nginx port at 8090 | No conflicts | yes (when no conflicts) |
| **B — Auto-remap** | Probe upward from 8090 for the next free | Default is taken | yes (when conflicts) |
| **C — User-specified** | Strict server policy on which port range is allowed | Institutional policy | |

**After the user chooses:** write resolved port to `.env::NGINX_PORT_SHINYMULTIOME` and `analysis_config.yaml::decisions::shinymultiome-uio-host::ports`.

### DECISION PAUSE — htpasswd users (S4)

> **Stop here.** Confirm whether to share the htpasswd with the `scrna-cxg-host` deploy or maintain a separate one.

| Option | What happens | When to choose | Default |
|--------|--------------|-----------------|---------|
| **A — Share with scrna-cxg-host** | Symlink `annotations/htpasswd` to the CXG deploy's file | Same wet lab cohort sees both URLs | yes |
| **B — Independent** | Separate `htpasswd` file; users may differ from CXG side | Different access policies (e.g., chromatin viewer for ATAC team only) | |
| **C — Defer to existing file** | User supplies a path; skill does not create | Auth managed elsewhere (LDAP, SSO frontend) | |

**After the user chooses:** the skill prompts for usernames if Option B; runs `htpasswd -B -c` for the first and `htpasswd -B` for subsequent. Append `decisions.shinymultiome-uio-host.htpasswd_strategy` to `analysis_config.yaml`. Passwords are **not** recorded.

### DECISION PAUSE — Server paths (S5)

> **Stop here.** Confirm host paths for RDS (read-only mount), fragments (read-only mount), and annotations metadata (read-only — Shiny is not autosave-capable; the annotations dir here is just for the htpasswd file).

The skill suggests `<project>/03_results/objects/` for the prepared `.rds`, `<project>/03_results/fragments/` for fragments + .tbi, and reuse of the `<project>/03_results/annotation/htpasswd` from the H1 deploy.

| Option | What happens | When to choose | Default |
|--------|--------------|-----------------|---------|
| **A — Conventions default** | `<project>/03_results/objects` + `<project>/03_results/fragments` | Project follows `scrna-pipeline-conventions` | yes |
| **B — Custom mount** | User names absolute paths | Server keeps data on a non-standard mount (e.g., `/scratch/`, `/data/`) | |

**After the user chooses:** write to `.env` and `analysis_config.yaml::decisions::shinymultiome-uio-host::paths`.

### DECISION PAUSE — Footprint precompute (S6)

> **Stop here.** TF footprints are expensive. Decide whether to compute now (Phase A.6), skip (Footprint tab will be empty), or defer (compute later and re-deploy).

| Option | What happens | When to choose | Default |
|--------|--------------|-----------------|---------|
| **A — Skip** | Footprint tab dropdown is empty; other three tabs work fully | Wet lab does not need motif footprints | yes |
| **B — Compute now** | A.6 runs `AddMotifs` + `Footprint` on a curated motif list (default JASPAR2020 vertebrate core) | Footprints are part of the deliverable | |
| **C — Defer** | Skip for now; re-run Phase A.6 later, then `docker compose restart shinymultiome` | Tight deadline; can iterate | |

**After the user chooses:** if B, ask which motif set (JASPAR2020 vertebrate core / curated list / specific TFs). If C, leave a TODO note in `analysis_config.yaml::decisions::shinymultiome-uio-host::footprints` for the next deploy iteration.

---

### Decision Pause anti-patterns to avoid

- Picking a default silently because "it's faster"
- Trying one option without naming the tradeoff to the user
- Skipping the pause because a previous session's choice is in config — but the data has changed (new genome, new assay names) since then
- Promising end-to-end automation while a pause is upcoming

---

## Verification Checklist

After running this skill, confirm:

- [ ] **Assays named correctly.** `DefaultAssay(obj) %in% c(<<RNA_ASSAY>>, <<ATAC_ASSAY>>)` and `<<ATAC_ASSAY>> %in% Assays(obj)`.
- [ ] **Annotation present and UCSC-styled.** `length(Annotation(obj[[<<ATAC_ASSAY>>]])) > 0` and `seqlevels(Annotation(obj[[<<ATAC_ASSAY>>]]))[1] == "chr1"`.
- [ ] **Fragment files reachable.** Every `Fragments(obj[[<<ATAC_ASSAY>>]])` path resolves to a real file with a `.tbi` sibling.
- [ ] **group.by columns present.** All names in `.env::GROUP_BY_COLUMNS` are columns of `obj@meta.data`.
- [ ] **Pre-deploy schema check passes.** `Rscript checks/validate_signac_rds.R 03_results/objects/<dataset>.rds` exits 0.
- [ ] **All containers Up.** `docker compose ps --format json | jq -r '.[].State' | sort -u` returns only `running`.
- [ ] **Auth works.** `curl -fI --user "$U:$P" http://<HOSTNAME>:<NGINX_PORT_SHINYMULTIOME>/` returns `HTTP/1.1 200`. Without auth: `401`.
- [ ] **WebSocket pass-through.** Browser console shows no `failed: WebSocket`; Shiny app responds to slider/dropdown changes within ~5s for ~50k-cell object.
- [ ] **Resource limits in effect.** `docker stats --no-stream` shows MEM LIMIT `32 GiB` (or whatever was set) on the shinymultiome container.
- [ ] **Memory ceiling not breached during track rendering.** Open Coverage tab, switch group.by twice; container does not OOM.

For automated verification: `Rscript checks/validate_signac_rds.R <path-to-rds>` (Phase A) and `bash checks/validate_shinymultiome_env.sh` (Phase B; runs after `docker compose up`).

---

## Common Pitfalls

### Pitfall: Empty CoveragePlot, no error

- **Symptom:** Coverage tab opens, the gene name is accepted, the spinner runs ~5s and then a blank panel renders. No error in the Shiny logs.
- **Cause:** Annotation seqlevels are Ensembl-style (`1, 2, ...`) while fragments are UCSC (`chr1, chr2, ...`). `Signac::CoveragePlot` silently produces an empty range.
- **Fix:** Run Phase A.2 (`ensure_signac_annotation`). The function always converts seqlevels to UCSC. Verify after with `seqlevels(Annotation(obj[["peaks"]]))[1:3]` — must be `c("chr1","chr2","chr3")`.

### Pitfall: Fragment file path stale (host vs container)

- **Symptom:** `CoveragePlot` errors with `file not found: /Users/akshay/.../fragments.tsv.gz` or similar.
- **Cause:** `Fragments(obj)` stores the absolute path from the analysis machine; inside the container that path does not exist.
- **Fix:** Run Phase A.3 (`rewrite_fragment_paths`) with `container_dir = "/data/fragments"`. The compose template bind-mounts the host fragments dir at exactly that container path.

### Pitfall: BSgenome package not installed

- **Symptom:** Container crash-loops at startup; logs show `Error in library(BSgenome.Mmusculus.UCSC.mm39): there is no package called 'BSgenome.Mmusculus.UCSC.mm39'`.
- **Cause:** Upstream `global.R` hard-codes `library(BSgenome.Hsapiens.UCSC.hg38)`. The skill's `global.R.template` reads from `${BSGENOME_PKG}`, but the Dockerfile must also `install` the matching package at build time.
- **Fix:** The shipped `Dockerfile.shinymultiome` accepts `BSGENOME_PKG` as an `ARG`/`ENV` and does `BiocManager::install(Sys.getenv("BSGENOME_PKG"))` in a build step. Confirm the package name is correct (`BiocManager::available()` filtered for the species) before `docker compose build`. mm39 was added to Bioconductor in 3.16+; ensure the base image is `bioconductor_docker:RELEASE_3_19` or later.

### Pitfall: WebSocket upgrades stripped (Shiny "disconnected")

- **Symptom:** Shiny UI says "Disconnected from the server" within 5–30s of opening the browser tab.
- **Cause:** nginx is not configured for WebSocket upgrade headers. Shiny falls back to polling and trips its own keepalive timeout.
- **Fix:** The shipped `nginx-shinymultiome.conf.template` includes the canonical `Upgrade` / `Connection` headers and `proxy_read_timeout 300s;`. Verify with:
  ```bash
  curl -i -H "Connection: Upgrade" -H "Upgrade: websocket" --user "$U:$P" \
    http://<HOSTNAME>:<NGINX_PORT_SHINYMULTIOME>/websocket
  # expect 101 Switching Protocols, not 200 OK
  ```

### Pitfall: Long CoveragePlot redraw → 504 Gateway Timeout

- **Symptom:** Switch `group.by` to a 30-cell-type column on a 100kb region; spinner runs for ~60s then UI shows 504 / "Application failed to start".
- **Cause:** nginx default proxy timeout (60s) shorter than Signac's CoveragePlot computation for that region × group.by combo.
- **Fix:** Bump `proxy_read_timeout` and `proxy_send_timeout` to 300s in `nginx-shinymultiome.conf` (the shipped template already does this). Coarsen the `group.by` column or shorten the genomic window if redraws still time out.

### Pitfall: Object name mismatch (`pbmc` vs your variable)

- **Symptom:** Shiny app starts, all four tabs throw `object 'pbmc' not found`.
- **Cause:** Upstream `server.R` references the loaded object as `pbmc` (a global). The .rds path you provide must `readRDS()` into `pbmc <- ...`.
- **Fix:** The shipped `global.R.template` does:
  ```r
  pbmc <- readRDS(Sys.getenv("RDS_PATH"))
  ```
  i.e., the variable is always renamed to `pbmc` regardless of how the .rds was saved. No upstream patch needed. Do **not** edit `server.R` to rename — it is vendored and will be re-pulled on bumps.

### Pitfall: RAM blow-up on first session

- **Symptom:** Container OOM-killed 30s into the first request; `docker compose logs` shows the kernel `Killed` line.
- **Cause:** The Seurat object loads into RAM at session start. A 100k-cell multiome with two assays and a `Motif` slot can exceed 32 GB.
- **Fix:** Bump `deploy.resources.limits.memory` in compose to 64G; consider stripping the `Motif` slot or downsampling for the Shiny instance. Reference: [`references/shiny-memory-and-timeouts.md`](./references/shiny-memory-and-timeouts.md).

### Pitfall: Two Shiny processes contend for the same port

- **Symptom:** `docker compose up` fails with `port 3838 already in use` after a `restart`.
- **Cause:** Previous Shiny did not release the internal port cleanly during `restart`.
- **Fix:** Use `docker compose down && docker compose up -d` instead of `restart`. The shipped Makefile targets do this.

### Pitfall: Wet lab loses work because Shiny is read-only

- **Symptom:** A user explores in Shiny and expects annotations to save like in CellxGene.
- **Cause:** Architectural — Shiny is the viewer, CellxGene is the labeller.
- **Fix:** Wet-lab onboarding doc (one paragraph): "label in CellxGene at `<CXG URL>`, view chromatin in ShinyMultiome at `<this URL>`". Same session, two tabs. Reference: [`references/two-url-deployment.md`](./references/two-url-deployment.md).

### Pitfall: Footprint tab empty even after A.6

- **Symptom:** Phase A.6 ran (`AddMotifs` + `Footprint`), object saved, container started, Footprint tab still has empty dropdown.
- **Cause:** Upstream `server.R` reads motifs from `pbmc@assays[["peaks"]]@motifs@motif.names` and footprint enrichments from `pbmc@assays[["peaks"]]@positionEnrichment`. If A.6 wrote to a different assay (e.g., `ATAC` instead of `peaks`), upstream cannot find them.
- **Fix:** Ensure A.6 runs on the assay named by `<<ATAC_ASSAY>>` (default `peaks`). The validator (`validate_signac_rds.R`) checks both slots when motif precompute is enabled in `.env`.

---

## Complementary Skills

| When you need... | Use skill | Relationship |
|---|---|---|
| Build the multiome `.rds` from Cell Ranger ARC outputs | `cellranger-arc-multiome` | Prerequisite (often) |
| Standard Signac WNN integration upstream of this skill | `seurat-multimodal-analysis` | Prerequisite |
| RNA-only CellxGene host (the H1 alongside this H2) | `scrna-cxg-host` | Companion |
| Convert the multiome .rds RNA layer to .h5ad for CellxGene | `anndatar-seurat-scanpy-conversion` | Adjacent |
| Compute motif accessibility deviations (chromVAR, alternative to A.6 footprints) | `chromvar-motif-accessibility` | Alternative / Adjacent |
| Inspect the .rds interactively before deploy | Loupe (10x), or R session | Out-of-skill prereq |

---

## Resources

- ShinyMultiomeUiO repository: https://github.com/EskelandLab/ShinyMultiomeUiO
- ShinyMultiomeUiO preprint: https://www.biorxiv.org/content/10.1101/2023.06.20.545756v2
- ShinyArchR.UiO (sister project, ArchR-based): https://github.com/EskelandLab/ShinyArchRUiO — vendored at `01_scripts/.ref/ShinyArchRUiO/` for UI reference only.
- Signac CoveragePlot docs: https://stuartlab.org/signac/reference/CoveragePlot.html
- Signac multiome vignette (PBMC + Cicero): https://stuartlab.org/signac/articles/pbmc_multiomic.html
- BSgenome packages list: https://bioconductor.org/packages/release/data/annotation/
- Project deploy docs: `docs/multiome-deploy/PHASE3-ALT-SHINYMULTIOME.md` (the architectural plan this skill implements).

---
name: scop
description: Use when installing or configuring the R package scop, running scop::PrepareEnv, repairing scop_env Python dependencies, validating Seurat/reticulate integration, or cataloging scop visualization functions.
---

# scop

## Overview

`scop` is an R/Seurat-centered single-cell omics package that delegates many methods to Python through `reticulate`. Treat setup as a two-layer install: keep the R package lean, then build and verify a dedicated Python environment.

Use this skill for local or Linux workstation setup, troubleshooting `PrepareEnv()`, checking Python module imports, and summarizing `scop` plot families. For generic Seurat/Scanpy preprocessing, use the single-cell or Scanpy skills instead.

## Known-Good Local Baseline

| Layer | Verified state |
|---|---|
| R package | `scop 0.8.9` from `mengxu98/scop`; R `4.5.1` |
| Seurat stack | `Seurat 5.4.0`, `SeuratObject 5.4.0`, `reticulate 1.46.0` |
| Python env | `/home/h2048/miniconda3/envs/scop_env`, Python `3.10.1` |
| Safe shell prefix | `env -u LD_LIBRARY_PATH -u PYTHONPATH PYTHONNOUSERSITE=1` |
| Verification outputs | `/home/h2048/temp/scop_verify_20260512` |
| Plot catalog | `/home/h2048/temp/scop_plot_catalog_20260512.tsv` |

Always run checks with the safe shell prefix in this workspace; user-site and base-conda pollution have caused false failures before.

## Setup Recipe

1. **Install the R package with core dependencies only.** Avoid `dependencies = TRUE` unless the user explicitly needs every optional feature; it can pull fragile Suggests such as GitHub-only packages and system libraries.

```r
pak::pkg_install(
  "mengxu98/scop",
  dependencies = c("Depends", "Imports", "LinkingTo")
)
```

2. **Create or inspect the Python environment.** `scop::PrepareEnv()` can bootstrap `scop_env`, but do not assume all default modules succeed on the first pass.

```r
options(scop_envname = "scop_env")
scop::PrepareEnv(
  envname = "scop_env",
  conda = "/home/h2048/miniconda3/condabin/conda",
  pip_options = "-i https://pypi.tuna.tsinghua.edu.cn/simple"
)
```

`scop::env_info` is not exported in `scop 0.8.9`; use `scop::ListEnv()`, `reticulate::py_config()`, `conda list`, and direct Python imports instead.

3. **Repair common Python/conda gaps.** `bedtools` needs `bioconda`; `conda-forge` alone failed in the verified setup.

```bash
env -u LD_LIBRARY_PATH -u PYTHONPATH PYTHONNOUSERSITE=1 \
  /home/h2048/miniconda3/condabin/conda install --yes --name scop_env \
  -c conda-forge -c bioconda leidenalg=0.10.2 tbb=2022.2.0 \
  python-igraph=0.11.9 scvi-tools=1.2.1 bedtools
```

4. **Preserve the conda PyTorch/scVI stack.** Do not use `uv pip install --force-reinstall` for the full default module list; it attempted to pull huge CUDA/NVIDIA `torch` wheels and can destabilize the environment. Prefer normal `pip install --no-user` for missing packages.

5. **Pin the known incompatibilities.** With `pandas==2.0.3` and `jax/jaxlib==0.4.38`, imports were fixed by:

```bash
env -u LD_LIBRARY_PATH -u PYTHONPATH PYTHONNOUSERSITE=1 \
  /home/h2048/miniconda3/envs/scop_env/bin/python -m pip install --no-user --no-deps \
  xarray==2023.12.0 optax==0.2.4
```

6. **Install MultiMAP from codeload if GitHub clone fails.** The package imports as `MultiMAP`, not lowercase `multimap`.

```bash
env -u LD_LIBRARY_PATH -u PYTHONPATH PYTHONNOUSERSITE=1 \
  /home/h2048/miniconda3/envs/scop_env/bin/python -m pip install --no-user \
  https://codeload.github.com/Teichlab/MultiMAP/zip/refs/heads/master
```

## Validation Checklist

- R package loads: `library(scop); packageVersion("scop")`.
- Core R dependencies load: `Seurat`, `SeuratObject`, `reticulate`, `ggplot2`, `patchwork`.
- Exported plot functions exist in `asNamespace("scop")`.
- Python imports pass for: `scanpy`, `anndata`, `scvi`, `scglue`, `scanorama`, `bbknn`, `celltypist`, `cellphonedb`, `magic`, `scrublet`, `doubletdetection`, `palantir`, `scvelo`, `cellrank`, `wot`, `phate`, `pacmap`, `trimap`, `MultiMAP`, `pybedtools`, `loompy`.
- Isolated `pip check` reports no broken requirements.
- In this workspace, run `/home/h2048/temp/verify_scop_setup_20260512.R` to regenerate package/function TSVs and smoke-test figures.

## Plot Function Families

The verified catalog has 39 non-interactive plotting entries plus the SCExplorer launcher row.

| Family | Functions / modes |
|---|---|
| Embedding / projection | `CellDimPlot`, `FeatureDimPlot`, `CellDimPlot3D`, `FeatureDimPlot3D`, `CellDensityPlot`, `ProjectionPlot` |
| Heatmap / correlation | `GroupHeatmap`, `FeatureHeatmap`, `CellCorHeatmap`, `FeatureCorPlot` |
| Statistics / composition | `CellStatPlot`, `FeatureStatPlot`, `ProportionTestPlot` |
| Differential / enrichment | `DEtestPlot`, `VolcanoPlot`, `DEtestManhattanPlot`, `DEtestRingPlot`, `EnrichmentPlot`, `GSEAPlot`, `GSVAPlot`, `MetabolismPlot`, `scTenifoldKnkPlot` |
| Trajectory / dynamic | `LineagePlot`, `BranchStreamPlot`, `DynamicPlot`, `DynamicHeatmap`, `PAGAPlot`, `PseudotimeProjectionPlot`, `VelocityPlot`, `CytoTRACEPlot` |
| Spatial | `SpatialDimPlot` |
| Cell-cell communication | `CCCHeatmap`, `CCCNetworkPlot`, `CCCStatPlot` |
| Benchmark / genomic | `BenchmarkPlot`, `LISIPlot`, `DimsEstimatePlot`, `CoverageTrackPlot`, `TACSPlot` |
| Interactive | `PrepareSCExplorer`, `RunSCExplorer` |

Example smoke-test outputs from the verified setup: `CellDimPlot`, `FeatureDimPlot`, `CellStatPlot`, and `GroupHeatmap` PNGs under `/home/h2048/temp/scop_verify_20260512`.

## Common Failures

| Symptom | Fix |
|---|---|
| R install fails while pulling optional GitHub/Suggests packages | Reinstall with `dependencies = c("Depends", "Imports", "LinkingTo")` first |
| `bedtools` not found during `PrepareEnv()` conda stage | Add `-c bioconda` to the conda install channels |
| `scvi` import fails through `xarray` / pandas API mismatch | Pin `xarray==2023.12.0` |
| `optax` import fails with current `jax` | Pin `optax==0.2.4` |
| `MultiMAP` GitHub clone fails due TLS/gnutls | Install the codeload `master` zip URL; import-check `MultiMAP` |
| Lowercase `multimap` import fails | This is expected; the installed module name is `MultiMAP` |
| Strange imports from base conda or `~/.local` | Re-run with `env -u LD_LIBRARY_PATH -u PYTHONPATH PYTHONNOUSERSITE=1` |
| `scop::env_info` fails | It is not exported in `0.8.9`; use `ListEnv`, `py_config`, and direct module probes |

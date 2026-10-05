---
name: cellranger-multi-to-anndata
description: "Build one pooled AnnData from CellRanger Multi per-sample outputs across N pools, with gene-union concatenation, sample provenance in obs, and biomaRt Ensembl-to-symbol annotation. Use when starting a project from a multi-pool cellranger multi run, to produce the canonical 00_raw.h5ad checkpoint. For 10x Multiome use muon-multimodal-analysis."
license: MIT
---

# CellRanger Multi → AnnData

## Overview

`cellranger multi` produces one filtered count matrix per *sample* under `per_sample_outs/<sample>/count/sample_filtered_feature_bc_matrix.h5`, with N pools each containing 1–M samples. A typical project has 5 pools × 4 samples = 20 matrices. Joining them into one AnnData requires three things the naïve `sc.read_10x_h5` + `ad.concat` path mishandles: (1) gene sets diverge across pools (different references, different version drift, occasional dropped chromosomes), (2) sample provenance must be carried into `obs` so every cell is traceable to a sample and pool, (3) Ensembl IDs must be resolved to gene symbols *after* concat so all pools share one symbol table.

This skill encapsulates the robust pattern: per-sample read with column-name detection, gene-union concat (zero-fill missing genes), biomart symbol annotation, optional metadata join. The output is the canonical `00_raw.h5ad` checkpoint that `single-cell-rna-qc` consumes next.

**When to use this skill:**
- A `cellranger multi` run has produced one or more pools of `per_sample_outs/`
- Project metadata (TSV/CSV) needs to be left-joined onto cells via a sample-id column
- The next step is QC (`single-cell-rna-qc`) and integration (`scvi-basic` / `scvi-scanvi`)

**When NOT to use this skill:**
- 10x Multiome (RNA + ATAC paired) → use `muon-multimodal-analysis`
- STARsolo intronic / spliced+unspliced quantification → use `starsolo-spliced-unspliced`
- One sample, one matrix, no pool structure → `sc.read_10x_h5(path)` is enough
- Already have an `.h5ad` → use `anndata` for I/O / subsetting

---

## Decision Tree

```
Faced with raw 10x output?
│
├─ Multi-pool cellranger multi run            →  THIS SKILL
├─ Single-sample cellranger count             →  sc.read_10x_h5 directly
├─ 10x Multiome (RNA + ATAC paired)            →  muon-multimodal-analysis
├─ STARsolo (intronic, spliced/unspliced)     →  starsolo-spliced-unspliced
└─ Already have an .h5ad                       →  anndata (I/O on existing object)
```

---

## Quick Start

The script `scripts/build_anndata.py` is the parameterised entry point. From a notebook or analysis script:

```python
from pathlib import Path
import scanpy as sc

from build_anndata import build  # from this skill's scripts/

adata = build(
    cellranger_root=Path("00_data/raw/CellRanger"),
    metadata_tsv=Path("00_data/raw/SamplesMetadata.txt"),  # or None
    metadata_join_key="Sample",          # column in metadata_tsv that maps to sample_id
    species="mouse",                     # or "human", or "other" with prefixes={...}
    out_path=Path("03_results/checkpoints/00_raw.h5ad"),
)

print(adata.shape)                       # (n_cells, n_genes)
print(adata.obs["orig_ident"].nunique()) # n_samples
print(adata.obs["pool_id"].nunique())    # n_pools
```

**Predict before running.** What do you expect `adata.shape` to be? For <ref-multi> (5 pools × 20 samples, ~10–15k cells/sample post-CellRanger filter), expect 150–250k cells × ~30k genes. For an unfamiliar dataset, predict the cell count from CellRanger's `summary.csv` files and check after concat.

**Verify it worked:**

```python
assert adata.n_obs > 0
assert adata.obs["orig_ident"].nunique() == n_expected_samples
assert adata.obs["pool_id"].nunique() == n_expected_pools
assert adata.var["gene_name"].notna().sum() / adata.n_vars > 0.9  # biomart resolved >90%
assert (adata.X.data >= 0).all() if hasattr(adata.X, "data") else (adata.X >= 0).all()
```

---

## Standard Workflow

The skill is organised into six steps. Each step has an inspection point — predict before running, then verify.

### Step 1 — Discover

Glob the per-sample matrices. The reference glob is rooted at `<cellranger_root>` and walks pool directories:

```python
import glob, re
h5s = sorted(glob.glob(
    f"{cellranger_root}/**/per_sample_outs/*/*/sample_filtered_feature_bc_matrix.h5",
    recursive=True,
))
print(f"Found {len(h5s)} matrices")
```

Sample-id and pool-id are extracted from the path (regex pinned, not from CellRanger's metadata):

```python
sid  = re.search(r"per_sample_outs/([^/]+)/", fp).group(1)   # e.g., <sample-1>
pool = re.search(r"CellRanger/([^/]+)/",     fp).group(1)    # e.g., <pool-1>
```

The pool regex segment (`CellRanger`) is project-dependent — the <ref-scrna> reference uses `Counts/`. The skill's `build()` accepts a `pool_pattern` parameter; `references/pool-detection.md` lists the common patterns observed.

**Inspect.** `len(h5s)` should equal `n_pools × samples_per_pool`. If it is off, the glob is wrong before reading anything.

### Step 2 — Read robust (per sample)

`read_10x_h5_robust()` (in `scripts/build_anndata.py`, ported from the reference `Python_scripts/anndata_utils.py`) handles:

- Multi-feature schemas (10x sometimes ships Gene Expression + Antibody Capture in the same file). Reads with `gex_only=True`.
- Column-name drift across CellRanger versions: tries `gene_ids` / `gene_id` / `id` / `feature_id` for IDs, and `gene_symbols` / `gene_symbol` / `gene_names` / `gene_name` / `name` / `feature_name` for symbols.
- Sets `var_names` to Ensembl IDs (stable across versions); `var_names_make_unique()`.
- Adds `obs['barcode']` (raw 10x barcode), `obs['sample_id']`, `obs['pool_id']`; uniquifies `obs_names` as `f"{sample_id}-{barcode}"`.

### Step 3 — Concatenate gene-union

`robust_concat_with_gene_union()` takes the union of all per-sample gene sets, zero-fills missing genes, preserves gene metadata, and concatenates with `ad.concat(..., axis=0, join='outer', fill_value=0, merge='first')`. The `keys=` argument lifts each input's index into `obs[label]` (`label='orig_ident'` per the reference).

**Why a custom function and not `ad.concat(..., join='outer')` directly?** Anndata's outer-join concat *does* zero-fill, but it loses gene metadata for genes absent from the first input. The robust helper reconstructs a union `var` table first, then re-indexes each input to the full gene set before concat — preserving the per-gene metadata uniformly.

Reference patterns: `references/gene-union-concat.md`.

### Step 4 — Annotate symbols (biomart)

`annotate_genes_scanpy_biomart(adata, organism="mmusculus")` calls `sc.queries.biomart_annotations(organism, ["ensembl_gene_id", "external_gene_name", "gene_biotype"], use_cache=True)`. Cache is at `~/.cache/scanpy/biomart/`. Fallback: if biomart is unreachable, `gene_name = gene_id` (Ensembl IDs preserved as symbols). The `mt_biomart` boolean is set from `sc.queries.mitochondrial_genes(organism)`.

Reference patterns + cache invalidation: `references/biomart-symbols.md`.

### Step 5 — Join metadata (optional)

This is the first Decision Pause. The skill enumerates candidate metadata files and asks the user to pick. After a file is picked, the columns are shown and the user picks a join key. See "Decision Pauses" below.

For <ref-multi> the file is `00_data/raw/SamplesMetadata.txt` (10 columns, tab-separated, `Sample` is the natural join key). Candidate metadata schemas across reference projects: `references/metadata-shapes.md`.

### Step 6 — Write checkpoint

```python
out = Path("03_results/checkpoints/00_raw.h5ad")
out.parent.mkdir(parents=True, exist_ok=True)
adata.write_h5ad(out, compression="gzip")
```

The path follows
`scrna-pipeline-conventions/references/checkpoints-and-objects.md`.

---

## Decision Pauses

Three pauses. The first two fire whenever metadata is involved; the third fires only when species is ambiguous (i.e., not specified and not recorded in `analysis_config.yaml`).

### DECISION PAUSE — Metadata source

> **Stop here.** Present the options below to the user and wait for their selection before proceeding. Do not pick a default silently.

**Question for the user:** Which file should I use to enrich `obs` with sample metadata, if any?

| Option | What happens | When to choose | Default |
|--------|--------------|-----------------|---------|
| **A — None** | `obs` gets only `orig_ident`, `sample_id`, `pool_id`, `barcode` | Metadata will be joined later, or the project does not have a metadata file | yes (safest) |
| **B — Auto-detect** | Skill globs `00_data/raw/*Metadata*.[tsv,txt,csv]` and `00_data/raw/manifest.csv`, presents matches with column names + first 3 rows for confirmation | Metadata lives at a conventional path | |
| **C — Explicit path** | User names the file path | Metadata is non-standard, split across multiple files, or in a sibling project | |

**After the user chooses:** proceed with the chosen option. Append the choice to `analysis_config.yaml` under `decisions.cellranger-multi-to-anndata.metadata_source` so re-runs replay the decision. After choice A, skip Pause 2. After B/C, proceed to Pause 2.

### DECISION PAUSE — Join key

> **Stop here.** Present the options below to the user and wait for their selection before proceeding. Do not pick a default silently.

**Question for the user:** Which column in the metadata file maps to per-cell `sample_id`?

The skill prints the metadata file's column names + first three rows, plus the AnnData `obs` columns currently present (`orig_ident`, `sample_id`, `pool_id`, `barcode`). Common candidates: `Sample`, `sample_id`, `LibraryID`, `MultiSampleID`. The skill suggests but does not pick.

| Option | What happens | When to choose | Default |
|--------|--------------|-----------------|---------|
| **A — Suggested column** | Skill names the most-likely column based on header similarity to `sample_id` | Header matches a known pattern unambiguously | (no static default — suggested, not asserted) |
| **B — User-named column** | User picks any column from the metadata header | Header uses a project-specific name (e.g., `MultiSampleID`) | |
| **C — Composite key** | User picks ≥2 columns; skill builds a string key for the join | Sample-id is split across columns (e.g., `Pool` + `Position`) | |

**After the user chooses:** validate that the resulting key is unique in the metadata file and matches the cardinality of `obs['sample_id'].unique()`. If a sample is unmatched, surface it before joining. Append the choice to `analysis_config.yaml` under `decisions.cellranger-multi-to-anndata.metadata_join_key`.

### DECISION PAUSE — Species

> **Stop here.** Present the options below to the user and wait for their selection before proceeding. Do not pick a default silently.

This pause fires **only** when the `species` parameter is unset *and* no recorded value exists at `analysis_config.yaml::decisions::cellranger-multi-to-anndata::species`. Otherwise the skill uses the recorded value silently and proceeds.

**Question for the user:** What species are these cells? This sets downstream prefixes (`mt-`/`MT-`, `Rpl`/`RPL`, `Rps`/`RPS`) and the biomart organism code.

| Option | What happens | When to choose | Default |
|--------|--------------|-----------------|---------|
| **A — Mouse** | `mmusculus`, `mt-`, `Rpl`, `Rps` | Mouse-derived samples | yes |
| **B — Human** | `hsapiens`, `MT-`, `RPL`, `RPS` | Human-derived samples | |
| **C — Other** | User supplies organism code + prefix dict | PDX, mixed-species, exotic organism | |

**After the user chooses:** proceed with the chosen species. Append the choice to `analysis_config.yaml` under `decisions.cellranger-multi-to-anndata.species`.

---

### Decision Pause anti-patterns to avoid

- Picking a default silently because "it's faster"
- Trying one option without naming the tradeoff to the user
- Skipping the pause because a previous session's choice is in config — but the input data has changed shape (e.g., new pools appeared, new metadata file added) since then
- Promising end-to-end automation while a pause is upcoming

---

## Verification Checklist

After running this skill, confirm:

- [ ] **Cell count in expected range.** `adata.n_obs` matches the sum of CellRanger `summary.csv` "Estimated Number of Cells" across samples (within ~5% — `cellranger multi` filtering and our reads should agree).
- [ ] **Sample provenance complete.** `adata.obs["orig_ident"].nunique() == n_expected_samples` and `adata.obs["pool_id"].nunique() == n_expected_pools`.
- [ ] **Symbols resolved.** `adata.var["gene_name"].notna().sum() / adata.n_vars > 0.9` (biomart matched ≥90% of Ensembl IDs).
- [ ] **Counts integer, non-negative.** For sparse: `(adata.X.data >= 0).all()` and `np.allclose(adata.X.data, adata.X.data.astype(int))`.
- [ ] **Metadata join sound (if applied).** Every unique `obs['sample_id']` appears in the joined metadata; no `NaN` in the joined columns where the source had values. Print `adata.obs.groupby(["pool_id","orig_ident"]).size()` and compare against the metadata table.
- [ ] **Mitochondrial genes findable.** `adata.var["gene_name"].str.startswith(<species_mt_prefix>).sum() > 0` (mouse: `mt-`, expect 13–15; human: `MT-`, expect 37). Zero MT genes is almost always a wrong-species or wrong-symbol-resolution problem.

---

## Common Pitfalls

### Pitfall: Mixed feature schemas across pools

- **Symptom:** A pool with Antibody Capture or CRISPR Guide features fails the read with shape-mismatch errors during concat.
- **Cause:** `sc.read_10x_h5(fp)` returns *all* features by default; downstream concat sees feature-type mismatches across pools.
- **Fix:** Read with `gex_only=True` (the default in `read_10x_h5_robust`). Antibody data, if needed, is loaded into a separate AnnData and stored in MuData / `obsm`.

### Pitfall: Hashing-demuxed samples with overlapping barcodes

- **Symptom:** After concat, `adata.n_obs` is smaller than the per-sample sum; some barcodes appear collided; `obs_names` are not unique.
- **Cause:** Two pools used the same 10x cell-barcode whitelist; the same barcode appears in different samples but represents different cells.
- **Fix:** `read_10x_h5_robust` already prefixes `obs_names` as `f"{sample_id}-{barcode}"` and stores the raw barcode in `obs["barcode"]`. Verify with `assert adata.obs_names.is_unique` before writing.

### Pitfall: Stale biomart cache → wrong symbols

- **Symptom:** Genes that should map (e.g., `Pdcd1`) come back as Ensembl IDs; downstream marker plotting fails to find expected symbols.
- **Cause:** `sc.queries.biomart_annotations(use_cache=True)` returns a stale local cache from a different organism or Ensembl release.
- **Fix:** Inspect `~/.cache/scanpy/biomart/` and delete the relevant cache file, or call `use_cache=False` for one run. The skill exposes `biomart_use_cache=True` as a parameter; flip to `False` after suspected drift.

### Pitfall: Wrong species prefix → 0 MT genes downstream

- **Symptom:** `adata.var["gene_name"].str.startswith("MT-").sum()` is 0 in mouse data; downstream MAD QC over `pct_counts_mt` returns garbage thresholds.
- **Cause:** Skill ran with default `species="mouse"` but the user later treats the prefix as human (`MT-`).
- **Fix:** The species parameter is the single source of truth; downstream skills must consume `analysis_config.yaml::decisions::cellranger-multi-to-anndata::species`. Verify with the Verification Checklist's MT-count assertion.

### Pitfall: Zero-fill explodes memory on a wide gene-union

- **Symptom:** `robust_concat_with_gene_union` consumes >100 GB on a 50-pool dataset with diverged references.
- **Cause:** Zero-fill is applied *eagerly* in dense space when a per-sample `X` is dense.
- **Fix:** The reference helper detects sparse vs dense and uses `sparse.hstack` for sparse. Verify input AnnDatas have `sparse.isspmatrix(adata.X) is True`. If they are dense, convert before concat: `adata.X = sparse.csr_matrix(adata.X)`.

### Pitfall: Metadata join silently drops samples

- **Symptom:** `obs["Group"].isna().sum() > 0` after the join; some cells have no group label.
- **Cause:** The chosen join key has typos, casing differences, or trailing whitespace between AnnData and the metadata file.
- **Fix:** Pause 2's "validate before joining" step — the skill prints unmatched values (samples present in `obs['sample_id']` but absent in metadata) and asks for resolution before proceeding.

---

## Resources

- 10x CellRanger Multi: https://www.10xgenomics.com/support/software/cell-ranger/latest/analysis/running-pipelines/cr-multi
- AnnData docs: https://anndata.readthedocs.io
- Scanpy biomart queries: https://scanpy.readthedocs.io/en/stable/api/scanpy.queries.biomart_annotations.html
- Reference codebase patterns (read-only, in-repo): `01_modules/.ref/<ref-scrna>/02_Analysis/00_build_anndata.py` and `01_modules/.ref/<ref-scrna>/01_Scripts/Python_scripts/anndata_utils.py`

---

## When not to use

- Do not use for 10x Multiome (RNA + ATAC paired) data. Use muon-multimodal-analysis instead.
- Do not use for STARsolo intron-aware or spliced/unspliced counts. Use starsolo-spliced-unspliced instead.
- Do not use on an already-built .h5ad. Use anndata directly for I/O on existing objects.
- Do not use on cellranger count (single-sample) output. Read the single .h5 with scanpy.read_10x_h5 directly.

---

## See also

- `anndata` — Adjacent / prerequisite-adjacent; operate on the produced `.h5ad` (subset, save, copy)
- `single-cell-rna-qc` — Next step (Stage 1); run MAD-based QC on the produced `.h5ad`
- `scvi-basic` — Downstream (Stage 2); integrate batches and learn a latent space
- `scrna-pipeline-conventions` — Assay convention; checkpoint validation and milestone packaging
- `analysis-code-conventions` — Structural convention; stage placement and restartable data flow
- `muon-multimodal-analysis` — Alternative (different modality); multiome RNA + ATAC paired ingestion
- `starsolo-spliced-unspliced` — Alternative (different counting strategy); spliced/unspliced or intronic counting

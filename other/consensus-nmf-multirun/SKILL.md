---
name: consensus-nmf-multirun
description: "Multi-run consensus cNMF for robust gene-program discovery on a single scRNA-seq dataset: runs across obs subsets and QC variants, merges correlated programs, classifies them Biological/Technical/CellCycle, and annotates via g:Profiler. Use when one dataset has factorial conditions. For per-sample NMF use genenmf-metaprogram-discovery."
license: MIT
---

# Consensus cNMF — multi-run program discovery

## Overview

cNMF (Kotliar et al. 2019) finds gene programs as non-negative matrix factors of single-cell counts. Run once on a single dataset, it is sensitive to: which K you chose, whether QC was strict, which cells you included. The "consensus" pattern in this skill runs cNMF *multiple times* — full dataset ± QC, optionally per-subset ± QC — and consolidates the resulting programs by correlation. Programs that recur across runs (high cross-run correlation, ≥2 source variants) are robust; programs that show up in only one variant are flagged as Low confidence.

This skill is opinionated about three things. First, **K selection is manual**, per variant — the user inspects each `k_selection_plot.png` and picks K, predicting their expected number of programs before seeing the plot. Second, **subsets are user-driven** — the skill never invents a subset axis; whole-dataset is the safe default. Third, **the ANOVA factor is user-named** — the skill enumerates `obs` columns, the user picks one. The <ref-scrna> reference's `temp` factor and Th1/Th17 subsets are not baked in; they are examples of one project's choices.

**When to use this skill:**
- One single-cell dataset, one or more factorial conditions
- Annotated celltypes available (programs are interpreted per-celltype)
- Raw counts present in `adata.layers["counts"]`
- You want programs that are robust to QC variation and subset focus

**When NOT to use this skill:**
- Per-sample NMF + cross-donor consensus → `genenmf-metaprogram-discovery`
- Topic models (AmortizedLDA) → `scvi-lda`
- Linear, signed, single-model decomposition → `scvi-linearscvi`

---

## Decision Tree

```
Want gene programs in single-cell data?
│
├─ One dataset, factorial conditions, raw counts present  →  THIS SKILL
├─ Multiple donors, recurrent programs across donors      →  genenmf-metaprogram-discovery
├─ Discrete topic model                                    →  scvi-lda
├─ Linear interpretable single-model                       →  scvi-linearscvi
└─ Per-cell motif / TF activity                            →  chromvar-motif-accessibility
```

---

## Quick Start

Seven stages, one entry point per. Each stage writes a checkpoint that the next reads.

```python
from pathlib import Path

# Stage 1 — Run cNMF, one variant per (subset × QC) combination.
#   Decision Pause 1 (subset strategy) and 2 (QC variant) resolve before this fires.
from run_cnmf_subset import run

run(
    in_h5ad=Path("03_results/checkpoints/10_scored.h5ad"),
    output_dir=Path("03_results/cnmf"),
    name="full",
    obs_filter=None,                 # whole-dataset; subsets pass an expression
    qc_filter=False,                 # raw-only; True applies the project's QC thresholds
    k_range=range(8, 13),            # 8..12; subsets typically range(6, 12)
    n_iter=100,
    n_top_genes=2000,
    seed=42,
)
# After this: open output_dir/full/full.k_selection.png — Decision Pause 3 fires here.

# Stage 2 — Manual K-selection (Decision Pause 3 per variant).
# User states expected K; inspects plot; calls run.consensus(k=...).

# Stage 3 — Score all variants' programs onto full barcode space.
from transfer_programs import transfer
adata = transfer(
    base_h5ad="03_results/checkpoints/10_scored.h5ad",
    sources={
        "cNMF_full":   "03_results/cnmf/full/full_results.pkl",
        # add more variants as Stage 1 produces them
    },
    out_h5ad="03_results/checkpoints/13_all_programs.h5ad",
    correlation_csv="03_results/tables/all_programs_correlation.csv",
)

# Stages 4–5 — Cross-source correlation matrix + hierarchical merge (Decision Pause 4).
from merge_programs import merge
merged = merge(
    correlation_csv="03_results/tables/all_programs_correlation.csv",
    sources_pkls={...},                      # same dict as transfer()
    out_dir="03_results/tables/programs",
    correlation_threshold=0.7,                # default; override via Decision Pause 4
    top_genes_to_keep=100,
    top_genes_per_source=50,
)

# Stage 6 — g:Profiler annotation.
from annotate_programs import annotate
annotate(
    merged_csv=merged.merged_programs_path,
    organism="mmusculus",                     # consume from analysis_config.yaml::decisions::cellranger-multi-to-anndata::species
    out_csv="03_results/tables/programs/program_annotations.csv",
)

# Stage 7 — Per-celltype ANOVA against a user-named factor (Decision Pause 5).
from condition_anova import anova
anova(
    in_h5ad="03_results/checkpoints/13_all_programs.h5ad",
    factor_column="Metagroup",                # user choice from Decision Pause 5
    celltype_column="celltype",
    factor_levels=["Y_C", "O_C", "O_M"],     # subset of all levels; user choice
    out_csv="03_results/tables/programs/program_factor_anova.csv",
)
```

---

## Standard Workflow

### Stage 1 — Run cNMF, one variant per (subset × QC) combination

For each variant the user picks (Decision Pause 1 × Decision Pause 2):

1. `cnmf_obj = cNMF(output_dir=..., name=variant_name)`
2. `cnmf_obj.prepare(counts_fn=..., components=K_range, n_iter=100, num_highvar_genes=2000, seed=42)`
3. `cnmf_obj.factorize(worker_i=0, total_workers=1)`
4. `cnmf_obj.combine()`
5. `cnmf_obj.k_selection_plot()` — produces `<output_dir>/<name>/<name>.k_selection.png`

Variant defaults from the <ref-scrna> reference:

| Variant scope | K range | n_iter | Other |
|---------------|---------|--------|-------|
| Full dataset | `range(8, 13)` (i.e., 8..12) | 100 | density_threshold=0.01 at consensus |
| Subset | `range(6, 12)` (i.e., 6..11) | 100 | same |
| TEST_MODE (subsample 1k cells) | as above | 10 | only for sanity-checking the pipeline |

QC-filter thresholds (Decision Pause 2 Option B/C; reference 06b):

```python
mask = (
    (adata.obs["n_genes_by_counts"] >= 200) &
    (adata.obs["n_genes_by_counts"] <= 6000) &
    (adata.obs["pct_counts_mt"]   <= 20) &
    (adata.obs["pct_counts_ribo"] <= 50) &
    (~adata.obs["predicted_doublet"].fillna(False))
)
```

These thresholds are project-tunable but the defaults match the reference pipeline.

### Stage 2 — Manual K-selection (per variant)

Decision Pause 3 fires per variant. The pause body documents the inflection-point heuristic — read `references/k-selection.md`.

After the user names K, the consensus call:

```python
cnmf_obj.consensus(k=optimal_k, density_threshold=0.01, show_clustering=True)
usage, spectra_scores, spectra_tpm, top_genes = cnmf_obj.load_results(K=optimal_k, density_threshold=0.01)
# pickle: {"usage": usage, "spectra_scores": spectra_scores, "spectra_tpm": spectra_tpm,
#         "top_genes": top_genes, "k": optimal_k}
```

### Stage 3 — Score onto full barcode space

For every variant's `usage` matrix, rename columns with the variant's prefix (`cNMF_<variant>_P<i>`), join into the full dataset's `obs` on cell index. Cells absent from a subset get `NaN` for that variant's columns.

The <ref-scrna> prefixes follow this convention:

| Variant scope | Prefix |
|---------------|--------|
| Full + raw | `cNMF_full_P<i>` |
| Full + QC | `cNMF_fullQC_P<i>` |
| Subset `<S>` + raw | `cNMF_<S>_P<i>` |
| Subset `<S>` + QC | `cNMF_<S>QC_P<i>` |

Reference: [consolidate-programs.md](./references/consolidate-programs.md). Output checkpoint: `03_results/checkpoints/13_all_programs.h5ad`.

### Stage 4 — Cross-source correlation matrix

Compute `obs[program_cols].corr()` over cells with non-NaN scores. Save as `03_results/tables/all_programs_correlation.csv`. Pairs with `|r| > 0.7` are flagged as candidates for merging in Stage 5.

### Stage 5 — Hierarchical merge

Hierarchical clustering on `1 − |r|` distance, ward linkage. Cut at `1 − threshold` (default `1 − 0.7 = 0.3`).

For each cluster:

- **Singleton** (one program) → directly inherit top-100 genes; confidence = Low
- **Multi-program** → rank aggregation of top-50 genes per source program, score by `(rank_score) × (1 + coverage_score)`, keep top-100

Confidence tiers:

| n unique source variants | Tier |
|--------------------------|------|
| ≥ 4 | High |
| 2–3 | Medium |
| 1 | Low |

Programs are then classified by gene composition (top 50):

| Class | Trigger |
|-------|---------|
| `CellCycle` | cell-cycle gene fraction > 0.20 |
| `Ribosomal` | ribosomal-gene fraction > 0.20 |
| `Mitochondrial` | MT-prefix fraction > 0.20 |
| `Technical` | (ribo + MT + housekeeping) fraction > 0.30 |
| `ImmediateEarly` | IEG fraction > 0.15 |
| `Biological` | otherwise |

Reference: [merge-programs.md](./references/merge-programs.md). Cell-cycle / ribosomal / MT / IEG / housekeeping gene lists in [merge-programs.md § Gene panels](./references/merge-programs.md). The mouse panels in the reference are mouse-specific; for human projects update to capitalised symbols (`MKI67`, `TOP2A`, …).

### Stage 6 — Annotate via g:Profiler

For each merged program's top-50 genes:

```python
result = gp.profile(
    organism=organism,                          # 'mmusculus' / 'hsapiens' from analysis_config.yaml
    query=top_50_genes,
    sources=["GO:BP", "GO:MF", "GO:CC", "KEGG", "REAC"],
    significance_threshold_method="fdr",
)
```

Per-program CSV, plus a combined `program_annotations.csv` with a `program` column. Reference: [annotate-programs.md](./references/annotate-programs.md). Rate-limit handling: sleep 1s on `Exception`, retry once.

### Stage 7 — Per-celltype ANOVA against a user factor

Decision Pause 5 fires here. The user names a factor column (e.g., `Group`, `Treatment`, `Metagroup`) and the levels of interest. The skill iterates `(celltype × program)`:

```python
groups = [adata.obs[(ct_mask) & (factor == lvl)][program].dropna() for lvl in levels if ...]
if len(groups) >= 2:
    f_stat, p_val = stats.f_oneway(*groups)
    eta_squared = ss_between / ss_total
```

BH-FDR over all `(celltype, program, factor)` rows. Output: `program_factor_anova.csv` with columns `program, celltype, factor, levels_present, f_stat, p_value, eta_squared, highest_at, p_adj`.

Reference: [condition-anova.md](./references/condition-anova.md).

---

## Decision Pauses

Five pauses. Whole-dataset, single-variant, default merge threshold, default factor — a user happy with the simplest run can clear all five with a brief back-and-forth.

### DECISION PAUSE — Subset strategy

> **Stop here.** Present the options below to the user and wait for their selection before proceeding. Do not pick a default silently.

cNMF runs independently per subset. Subsetting strategy is project-specific; whole-dataset only is the safe default.

**Question for the user:** Should I run cNMF on the whole dataset only, or on subsets of `obs`? If subsets, what is the axis?

| Option | What happens | When to choose | Default |
|--------|--------------|-----------------|---------|
| **A — Whole dataset only** | One cNMF run on all cells | Simple project; no obvious subset axis; first pass | yes |
| **B — Per major celltype** | Skill enumerates distinct values of `obs[<celltype-column>]` (with cell counts), confirms subset list | Multicellular dataset, biology likely differs across major populations | |
| **C — Per condition** | Skill enumerates distinct values of a user-named factor; runs cNMF per level | Strong condition effect, want condition-specific programs | |
| **D — Per celltype × condition** | Cross-product of B and C | Both axes matter, compute budget allows; **expensive** (4–8× single run) | |
| **E — User-defined `obs` filter expressions** | Free-form per-subset, e.g., `{"Mem_T": "celltype.startswith('T_') & state=='Memory'"}` | Subsets that don't follow a single column | |

**After the user chooses:** confirm the resulting subset list (with cell counts per subset) before any cNMF run. Append the choice to `analysis_config.yaml` under `decisions.consensus-nmf-multirun.subset_strategy`.

### DECISION PAUSE — QC-variant strategy

> **Stop here.** Present the options below to the user and wait for their selection before proceeding. Do not pick a default silently.

Each subset can be run on raw counts, on QC-filtered counts, or on both. Raw-only is the safe default; both is more robust but doubles compute.

**Question for the user:** Which counts should cNMF run on?

| Option | What happens | When to choose | Default |
|--------|--------------|-----------------|---------|
| **A — Raw only** | One run per subset, no extra QC filter beyond pipeline upstream | Simple; trust upstream `single-cell-rna-qc` MAD filter | yes |
| **B — QC-filtered only** | One run per subset, stricter QC: `200 ≤ n_genes ≤ 6000`, `pct_mt ≤ 20`, `pct_ribo ≤ 50`, no doublets | Suspicious of upstream QC; want a clean baseline | |
| **C — Both (raw + QC)** | Two runs per subset, results merged downstream | Want robustness against QC artifacts; reference-style multi-run consensus | |

**After the user chooses:** append to `analysis_config.yaml` under `decisions.consensus-nmf-multirun.qc_variant`.

### DECISION PAUSE — K per variant

> **Stop here.** Present the options below to the user and wait for their selection before proceeding. Do not pick a default silently.

Open `<output_dir>/<variant>/<variant>.k_selection.png`. The plot shows reproducibility (top) and stability (bottom) across K. **State your expected K before viewing the plot** (predict-before-view); then look for the inflection — K just before the curve flattens.

**Question for the user:** What K should I use for variant `<variant>`?

| Option | What happens | When to choose | Default |
|--------|--------------|-----------------|---------|
| **A — Numeric K** | Skill uses this K for the variant | Inspect plot, name K | (no default — manual per variant) |
| **B — Defer** | Skill stops after k-selection plots and waits for the user to inspect all variants before committing | Want to inspect all variants' plots together before committing | |

**After the user chooses:** for each variant, call `cnmf_obj.consensus(k=K, density_threshold=0.01, show_clustering=True)`. Append per-variant K to `analysis_config.yaml` under `decisions.consensus-nmf-multirun.k_per_variant.<variant>`.

### DECISION PAUSE — Merge threshold

> **Stop here.** Present the options below to the user and wait for their selection before proceeding. Do not pick a default silently.

Programs from different runs are merged when their pairwise correlation exceeds threshold. `r > 0.7` works for most projects.

**Question for the user:** What correlation threshold should drive the hierarchical merge?

| Option | What happens | When to choose | Default |
|--------|--------------|-----------------|---------|
| **A — `r > 0.7`** | Standard merge | Most projects | yes |
| **B — `r > 0.5`** | Aggressive merge | Want fewer, more redundant programs | |
| **C — `r > 0.9`** | Conservative merge | Want to preserve subtle distinctions | |
| **D — Custom** | User names threshold | Rare; document why | |

**After the user chooses:** append to `analysis_config.yaml` under `decisions.consensus-nmf-multirun.merge_threshold`.

### DECISION PAUSE — Condition factor + contrasts for ANOVA

> **Stop here.** Present the options below to the user and wait for their selection before proceeding. Do not pick a default silently.

Skill enumerates `obs` columns with their distinct-value counts and dtypes (e.g., `Group: 2 (Young, Old)`, `Treatment: 4`, `Metagroup: 8`).

**Question for the user:** Which `obs` column is the factor? Which levels (or contrasts) are of interest?

| Option | What happens | When to choose | Default |
|--------|--------------|-----------------|---------|
| **A — All levels of one factor** | ANOVA across all levels, no level-pair contrasts | First-pass exploration; broad effect | (no default — user names factor) |
| **B — Subset of levels** | ANOVA over a user-named subset of levels | Reduce noise from low-cell-count levels; targeted hypothesis | |
| **C — Pairwise contrasts** | One ANOVA per level pair, FDR over the union | Specific contrast questions (Old-vs-Young, Treated-vs-Control) | |

**After the user chooses:** confirm the factor + levels with cell counts per level before running. Append to `analysis_config.yaml` under `decisions.consensus-nmf-multirun.anova_factor`.

---

### Decision Pause anti-patterns to avoid

- Picking a default silently because "it's faster"
- Trying one option without naming the tradeoff to the user
- Skipping the pause because a previous session's choice is in config — but the input AnnData has changed shape (different cells, different celltypes, new factor levels) since then
- Promising end-to-end automation while a pause is upcoming

---

## Verification Checklist

After running this skill, confirm:

- [ ] **k_selection plot exists per variant.** `ls <output_dir>/<variant>/<variant>.k_selection.png` returns one path per variant.
- [ ] **`13_all_programs.h5ad` has expected program columns.** `[c for c in adata.obs.columns if c.startswith("cNMF_")]` count equals `sum(K_per_variant.values())`.
- [ ] **Cross-source correlation matrix has no all-NaN rows.** `corr_df.isna().all(axis=1).sum() == 0`.
- [ ] **Merged program count is sensible.** Typically 10–20 after merging; if you see >50, threshold is too strict; if 2–3, too loose.
- [ ] **Confidence tier distribution makes sense.** High count > 0 means at least one program survived ≥4 sources; if all programs are Low, the multi-run design is not adding value.
- [ ] **At least one ANOVA `p_adj < 0.05`.** If zero, either the chosen factor is not the right axis, or the dataset is underpowered for the contrast.
- [ ] **Cross-run pair redundancy check.** `python checks/check_program_redundancy.py` returns no pairs with `r > 0.9` outside the same merged cluster (those are likely overfit / K too high).

For automated verification: `python checks/check_program_redundancy.py <correlation_csv> <merged_csv>`.

---

## Common Pitfalls

### Pitfall: TEST_MODE artefact (subsample 1000 cells) used downstream

- **Symptom:** Most program scores in `13_all_programs.h5ad` are NaN; the cross-source correlation matrix has many all-NaN rows.
- **Cause:** `06_run_cnmf.py` was run with `TEST_MODE=True` (subsample 1000 cells); the resulting usage matrix only covers those 1000 cells, but Stage 3 transferred them onto the full dataset.
- **Fix:** Re-run with `TEST_MODE=False`; in the parameterised script, the equivalent is leaving `n_iter=100` and not passing `--subsample`.

### Pitfall: Source-name prefix collision (`cNMF_full` vs `cNMF_fullQC`)

- **Symptom:** Programs from `cNMF_fullQC_P1` are mis-attributed to `cNMF_full` source during merge.
- **Cause:** The reference `merge_programs.py` had a bug where source prefixes were matched lexicographically; `cNMF_full` matched `cNMF_fullQC_P1` because `startswith` accepted the shorter prefix.
- **Fix:** Sort source prefixes by length descending before any `startswith` check. The shipped script does this; do not "simplify" to a sorted-alphabetically version.

### Pitfall: Factor confounded with batch

- **Symptom:** Many programs come up `p_adj < 0.05` against `Group` (Young/Old), but the same programs are also `p_adj < 0.05` against `pool` (the technical batch key).
- **Cause:** Aging samples were sequenced in different pools from young samples; condition and batch are aliased.
- **Fix:** Two paths — (a) include `pool` as a covariate (the shipped ANOVA does plain `f_oneway`; use a linear model from `statsmodels` instead, with `program ~ C(factor) + C(pool)`), or (b) acknowledge the confound, restrict to within-pool comparisons, document.

### Pitfall: Merging at `r > 0.5` collapses biology

- **Symptom:** After merge, you have 5 programs and they each look like they cover a broad mixed pathway; specific Th1 / Th17 / heat-shock signal is gone.
- **Cause:** Threshold too loose — programs that are correlated for *technical* reasons (e.g., they share ribosomal genes) are merged with biological programs.
- **Fix:** `r > 0.7` is the default for a reason. Try `0.75` or `0.8` for tighter clusters; `r > 0.5` is for projects where you want a heavily-aggregated overview.

### Pitfall: Forgetting raw counts in `layers["counts"]`

- **Symptom:** `cnmf prepare` errors with `KeyError: 'counts'` or runs but produces all-zero programs because the input was log-normalised.
- **Cause:** cNMF expects raw integer counts. Most scanpy pipelines normalise `.X` and forget to stash the raw counts.
- **Fix:** Before any normalisation, `adata.layers["counts"] = adata.X.copy()`. The Stage 1 script writes a counts-only file (`<name>_counts.h5ad`) for cNMF; ensure the source has the layer.

### Pitfall: Programs that score > 1.0 or < 0

- **Symptom:** Some `obs["cNMF_full_P3"]` values are negative or huge; downstream ANOVA p-values are unreliable.
- **Cause:** Spectra-scores were used instead of usage; or the cell ordering between the cNMF output and the AnnData diverged.
- **Fix:** `usage` matrix from `cnmf_obj.load_results()` is the canonical scoring; values should be in [0, 1] (a simplex per cell). Verify with `assert (usage.values >= 0).all() and (usage.sum(axis=1) <= 1.001).all()` before transfer.

### Pitfall: Per-celltype ANOVA on a celltype with one level

- **Symptom:** `f_oneway()` returns NaN; ANOVA row has `p_adj=NaN`; FDR correction breaks.
- **Cause:** The `<celltype, factor>` cell is so small that only one level of the factor has any cells.
- **Fix:** Skip cells where `len(groups) < 2`. The shipped `condition_anova.py` does this; surface the skipped pairs to the user as a warning.

---

## Resources

- cNMF GitHub: https://github.com/dylkot/cNMF
- Kotliar et al. 2019: https://doi.org/10.7554/eLife.43803
- g:Profiler API: https://biit.cs.ut.ee/gprofiler/page/apis
- Reference codebase patterns (in-repo): `01_modules/.ref/<ref-scrna>/02_Analysis/06*.py`, `07_*.py`, `08_*.py`

---

## When not to use

- Do not use for per-sample NMF + cross-donor consensus. Use genenmf-metaprogram-discovery.
- Do not use for AmortizedLDA topic modeling. Use scvi-lda.
- Do not use without a celltype annotation — programs are interpreted per-celltype during ANOVA.
- Do not use without raw counts in adata.layers['counts']. cNMF errors on log-normalised input.

---

## See also

- `scanpy` — Prerequisite; standard scRNA-seq pipeline upstream (QC, integration, annotation)
- `single-cell-rna-qc` — Prerequisite; MAD-based QC filtering before this skill
- `genenmf-metaprogram-discovery` — Alternative; per-sample NMF + cross-donor consensus, a different statistical object
- `bulk-rnaseq-pathway-explorer` — Downstream; build an interactive HTML pathway dashboard from program annotations
- `scrna-pipeline-conventions` — Assay convention; AnnData checkpoints and milestone packaging
- `analysis-code-conventions` — Structural convention; narrative stages and restartable data flow

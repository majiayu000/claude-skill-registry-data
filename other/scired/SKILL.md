---
name: scired
description: "sciRED — Python package for interpreting scRNA-seq factor analysis via Poisson-GLM nuisance regression, PCA, varimax rotation, a factor-covariate association table, and interpretability scoring. Use to residualise known confounders, extract rotated factors, and rank factor-covariate associations. For multi-view factor analysis use mofa-framework."
license: MIT
---

# sciRED: Supervised-Scoreboard Interpretation of scRNA Factor Analysis

**Foundation:** `factor-analysis-framework` is the super-family router and holds the shared concept content. Jump directly to:
- `factor-analysis-framework/references/benzecri-properties.md` — the four properties; sciRED's status is partial / absent across all four (see `references/geometric-caveats.md` below for the per-property breakdown).
- `factor-analysis-framework/references/modelling-vs-map.md` — sciRED is *neither* purely a model nor a map; it is a *labelled scoreboard* over a PCA + varimax map.
- `factor-analysis-framework/references/supplementary-projection.md` — the L1 patch that bolts true categorical-level barycenters and continuous-arrow overlays on top of sciRED's rotated factor matrix in ~20 lines.

This file covers only the parts that differ for sciRED (PCA + varimax + Poisson-GLM residualisation + supervised-classifier scoreboard).

---

## When to Use sciRED

- You have a single-omic cell × gene scRNA **count** matrix (not multi-view, not log-normalised).
- You have categorical covariate metadata (cell type, condition, donor, batch) and want to *rank* factors by association with each covariate level.
- You want varimax-rotated, sparse-ish factor loadings on residualised expression for marker-gene interpretation.
- You want a published, off-the-shelf four-step pipeline rather than rolling your own.

**Cell count:** 10³–10⁵ cells comfortably. Beyond ~10⁵ the per-gene `sm.GLM` loop in `glm.py:23` becomes the bottleneck.

---

## When NOT to Use sciRED

- **Multi-view / multi-omic** (RNA + ATAC + methylation in one model) → `mofa-framework` and its `mofa-mofapy2` implementation.
- **Want a Benzécri biplot** with categorical-level barycenters and continuous-variable arrows on the same axes as the cell scatter → apply the L1 supplementary-projection patch from `factor-analysis-framework` on top of sciRED's varimax-rotated factors. sciRED itself never co-projects rows and columns.
- **Raw-count-aware joint decomposition** (negative binomial / Poisson likelihood across the whole matrix, GLM-PCA) → `mofa-mofapy2` with `likelihoods=["poisson"]` or a future `glmpca-*` skill. sciRED's per-gene Poisson GLMs do *not* share information across genes — it is residualise-then-PCA, not joint count factorisation.
- **Nonlinear manifold viz** for cell-type clustering → UMAP / t-SNE; factor analysis assumes a (near-)linear bilinear decomposition.
- **n ≪ p pseudo-bulk** (donor × gene with n ≈ 10–100) → sciRED's PCA will be rank-deficient and FCAT will produce perfectly-separable, meaningless importance scores (see `references/geometric-caveats.md`).

---

## Decision Tree

```
Have a cell × gene count matrix?
│
├─ Want to map factors → covariate levels with a supervised scoreboard?
│   └─ sciRED (FCAT + FIST)
│
├─ Want a TRUE biplot (cells + genes + level barycenters on same axes)?
│   └─ sciRED scores + L1 patch from factor-analysis-framework
│
├─ Multi-view / multi-omic?
│   └─ mofa-mofapy2
│
└─ Just want UMAP for clustering?
    └─ scanpy (sc.pp.pca → sc.pp.neighbors → sc.tl.umap)
```

---

## Installation

From the upstream README (sciRED `README.md:30-44`):

```bash
# Prerequisites
pip install numpy pandas scanpy statsmodels seaborn umap-learn matplotlib \
            scikit-learn scipy xgboost scikit-image diptest==0.2.0
# Then sciRED itself
pip install sciRED
# Or from source
pip install git+https://github.com/delipouya/sciRED
```

Numba-dependent prerequisites may force a `numpy<=1.22.4` pin on some systems. See the README's "Common issues" note.

---

## Quick Start — The Canonical Four-Step Pipeline

Mirrors `example_scMixology.py:42-89` and `:118-121`. Inputs: an AnnData `data` with raw counts in `data.X` and metadata columns (`protocol`, `cell_line`, `nCount_originalexp`) on `data.obs`.

```python
import numpy as np
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline

from sciRED import glm, rotations as rot, metrics as met, ensembleFCA as efca
from sciRED.utils import preprocess as proc

NUM_COMPONENTS = 10
NUM_GENES = 2000

# 1. HVG-subset; pull raw counts as numpy
data, _ = proc.get_sub_data(data, num_genes=NUM_GENES)
y, genes, n_cells, n_genes = proc.get_data_array(data)

# 2. Design matrix for known confounders (library size + protocol + intercept)
x_protocol = proc.get_design_mat(metadata_col="protocol", data=data)
x = np.column_stack((data.obs.nCount_originalexp, x_protocol))
x = sm.add_constant(x)

# 3. Per-gene Poisson GLM → Pearson residuals (raw counts as response)
glm_fit = glm.poissonGLM(y, x)
resid = glm_fit["resid_pearson"].T          # (n_cells, n_genes)

# 4. PCA on standardised residuals
pipe = Pipeline([("scale", StandardScaler()),
                 ("pca", PCA(n_components=NUM_COMPONENTS))])
pca_scores = pipe.fit_transform(resid)
pca_loading = pipe.named_steps["pca"].components_  # (K, n_genes)

# 5. Varimax rotation of loadings; propagate to scores
vr = rot.varimax(pca_loading.T)
varimax_loading = vr["rotloading"]          # (n_genes, K)
pca_scores_varimax = rot.get_rotated_scores(pca_scores, vr["rotmat"])

# 6. FCAT — supervised scoreboard for one categorical covariate
fcat_celltype = efca.FCAT(data.obs["cell_line"], pca_scores_varimax,
                          scale="standard", mean="arithmatic", time_eff=True)

# 7. FIST — combine bimodality / variance / specificity into a clustermap
all_metrics = {
    "bimodality":     met.kmeans_bimodal_score(pca_scores_varimax),
    "factor_var":     met.factor_variance(pca_scores_varimax),
    "simpson":        met.simpson_diversity_index(fcat_celltype),
    "asv_celltype":   met.average_scaled_var(pca_scores_varimax, data.obs["cell_line"]),
}
fist = met.FIST(all_metrics)
```

**Output shapes:**

| Object | Shape | Notes |
|---|---|---|
| `pca_scores_varimax` | `(n_cells, K)` | Varimax-rotated factor scores |
| `varimax_loading` | `(n_genes, K)` | Varimax-rotated gene loadings |
| `fcat_celltype` | `(n_levels, K)` | Supervised classifier importance per (level, factor) |
| `fist` | `(K, n_metrics)` | Min-max-scaled scoreboard |

---

## Key API Surfaces

All file/line citations come from the in-repo audit at `docs/vision/latent/sciRED.md`.

### Preprocessing — `sciRED/utils/preprocess.py`

| Function | Location | Role |
|---|---|---|
| `get_data_array(data)` | `preprocess.py:7-22` | AnnData → `(numpy_X, genes, n_cells, n_genes)` |
| `get_sub_data(data, num_genes=2000)` | `preprocess.py:46-71` | HVG selection by **raw variance** on densified counts (not Seurat VST; biases toward high-mean genes) |
| `get_design_mat(metadata_col, data)` | `preprocess.py:102-115` | One-hot-encode a categorical metadata column |
| `get_library_design_mat(data, lib_size=...)` | `preprocess.py:119-125` | Stack a constant + library-size column |

### Poisson GLM residualisation — `sciRED/glm.py`

`poissonGLM(y, x)` (`glm.py:5-42`) fits `sm.GLM(y_a_gene, x, family=sm.families.Poisson())` once per gene in a sequential Python loop. Returns a dict with `resid_pearson`, `resid_deviance`, `resid_response`; only **Pearson** residuals are propagated in the upstream examples (`example_scMixology.py:60-63`). Each gene's GLM is independent — there is no joint count likelihood; this is residualise-then-PCA, not GLM-PCA.

### Rotations — `sciRED/rotations.py`

| Function | Location | Role |
|---|---|---|
| `varimax(x, normalize=True, eps=1e-5)` | `rotations.py:8-42` | Port of base-R `varimax()`; iterates `≤1000` times, breaks on `d < dpast*(1+eps)`. Returns `{"rotloading", "rotmat"}` |
| `promax(x, m=4, ...)` | `rotations.py:46-79` | Oblique alternative; runs `varimax` first then a least-squares refit |
| `get_rotated_scores(factor_scores, rotmat)` | `rotations.py:83-89` | `factor_scores @ rotmat` — propagates the rotation onto the score side |

Varimax sign and order are **not unique**. The same input yields different bases across runs / seeds. `example_scMixology.py:182-214` even computes the cross-correlation between varimax and promax factors as a diagnostic.

### FCAT — `sciRED/ensembleFCA.py`

The supervised-classifier "factor–covariate association table".

| Function | Location | Role |
|---|---|---|
| `get_binary_covariate(covariate_vec, level)` | `ensembleFCA.py:25-35` | 1-vs-rest indicator vector |
| `get_AUC_alevel(a_factor, a_binary_cov)` | `ensembleFCA.py:38-62` | Mann-Whitney AUC; **rescaled to feature-importance scale** as `2·|AUC − 0.5|` (`:80`) |
| `get_importance_df(...)` | `ensembleFCA.py:90-137` | Trains the ensemble. Default ensemble (`time_eff=True`, `:105-108`): **LogReg, DecisionTree, XGB** + AUC. Setting `time_eff=False` adds RandomForest and KNeighbors-permutation |
| Importance extraction | `ensembleFCA.py:117-129` | `\|coef\|` for LogReg, `feature_importances_` for tree models, permutation importance for KNN |
| `get_mean_importance_level(...)` | `ensembleFCA.py:142-194` | Per-(level) aggregator. `scale ∈ {standard, minmax, rank}`; `mean ∈ {arithmatic, geometric}` |
| `FCAT(covariate_vec, factor_scores, ...)` | `ensembleFCA.py:198-218` | Stack one row per covariate level. Returns `(n_levels, K)` DataFrame |
| `get_percent_matched_factors/covariates` | `ensembleFCA.py:221-236` | Threshold-based "how many factors light up?" diagnostic |
| `get_otsu_threshold(values)` | `ensembleFCA.py:240-247` | Otsu cut for picking the matched-factor threshold |

**FCAT is per-covariate.** To cover *N* covariates, call `efca.FCAT` *N* times and concatenate.

### FIST and per-factor metrics — `sciRED/metrics.py`

| Metric | Location | Returns |
|---|---|---|
| `kmeans_bimodal_score` (k-means silhouette) | `metrics.py:25-59` | Per-factor silhouette in 2-cluster split |
| `bimodality_index` (GMM-based) | `metrics.py:63-92` | √(π(1−π))·σ from a 2-component GMM |
| `factor_variance` | `metrics.py:96-105` | `np.var(factor_col)` — *not* `λ_α` after rotation |
| `simpson_diversity_index(fcat)` | `metrics.py:109-137` | Per-factor Simpson D over the FCAT column |
| `average_scaled_var(scores, covariate)` | `metrics.py:171-209` | Mean over levels of `var(scores\|level) / var(scores)` |
| `get_dip_test_all` | `metrics.py:298-312` | Hartigan dip statistic + p-value per factor |
| `get_weighted_variance_reduction_score` | `metrics.py:340-352` | k-means WVRS per factor |
| `FIST(all_metrics_dict)` + `get_scaled_metrics` | `metrics.py:355-383` | Min-max scaling per metric column; returns scaled DataFrame for clustermap |

**`get_scaled_metrics` is per-column min-max** (`metrics.py:355-367`) — adding or removing factors changes the colour scale of every other factor without changing the underlying biology. Treat FIST as a *visual ranking aid*, not as a calibrated score.

### Visualisation — `sciRED/utils/visualize.py`

| Function | Location | Plot |
|---|---|---|
| `plot_pca` | `visualize.py:8-43` | Cells on F1 × F_i for `i = 2…K`, looped |
| `plot_factor_scatter` | `visualize.py:47-66` | Cells on F_x × F_y, coloured by metadata |
| `plot_factor_loading` | `visualize.py:70-117` | **Genes** on F_x × F_y with top-N / bottom-N labelled — **NOT a biplot**, no cells, no arrows |
| `plot_FCAT` | `visualize.py:151-198` | (level × factor) heatmap |
| `plot_FIST` | `visualize.py:314-349` | (factor × metric) clustermap |
| `plot_sorted_factor_FCA_scores` | `visualize.py:354-371` | Bar plot of one FCAT row, sorted |
| `plot_relativeVar` | `visualize.py:374-419` | (level × factor) scaled-variance heatmap |

### Diagnostic — `sciRED/utils/corr.py`

`get_factor_libsize_correlation(scores, library_size)` (`corr.py:4-13`) is the only built-in technical-covariate check. The same one-line trick generalises to any continuous metadata column — that is the L1 continuous-arrow patch from `factor-analysis-framework/references/supplementary-projection.md`.

---

## Outputs

CSV-friendly exports (`example_scMixology.py:235-245`):

```python
# Loadings: (n_genes × K)
pd.DataFrame(varimax_loading, index=genes,
             columns=[f"F{i}" for i in range(1, K+1)]).to_csv("loadings.csv")

# Scores merged with cell metadata: (n_cells × (n_obs_cols + K))
scores_df = pd.DataFrame(pca_scores_varimax, index=data.obs.index,
                         columns=[f"F{i}" for i in range(1, K+1)])
pd.concat([data.obs.reset_index(drop=True),
           scores_df.reset_index(drop=True)], axis=1).to_csv("scores.csv")
```

These CSVs are exactly what the L1 supplementary-projection patch consumes.

---

## Common Issues

| Issue | Cause | Resolution |
|---|---|---|
| `np.log(y + 1e-10)` in upstream examples | Upstream uses a non-standard offset (`example_scMixology.py:43`) | Prefer `np.log1p(y)`. The `1e-10` offset is numerically unstable and not necessary — `poissonGLM` itself takes raw counts |
| Per-gene GLM loop slow on > 10⁴ genes | Sequential `sm.GLM(...).fit()` per gene (`glm.py:23-29`) | HVG-filter upstream via `proc.get_sub_data(data, num_genes=2000)` (`preprocess.py:46-71`); ~5× speedup |
| Varimax sign / order flips between runs | SVD `±1` indeterminacy + rotation non-uniqueness (`rotations.py:8-42`) | Impose a canonical sign downstream (e.g. force largest-absolute loading positive per factor); align across runs via Procrustes |
| FIST "Effect size" row not a Benzécri budget | `factor_variance` is post-rotation `np.var` (`metrics.py:96-105`); `get_scaled_metrics` then min-max-rescales it (`metrics.py:355-367`) | Do not present FIST values as fractions of total inertia. Report the FIST clustermap as a *visual ranking aid* only |
| FCAT scores swap when classifier set changes | `time_eff=True` drops RandomForest + KNN-perm (`ensembleFCA.py:105-108`); the three remaining (LogReg, DT, XGB) have very different inductive biases | Run both `time_eff=True` and `time_eff=False`, average; or use `permutation.py` shuffle null (`permutation.py:176-183`) |
| `pca.explained_variance_ratio_` not surfaced | Computed by sklearn, commented out at `example_scMixology.py:76`, never read again | Read it yourself; remember it refers to the **unrotated** PCA, not to the varimax basis |
| n ≪ p pseudo-bulk produces "perfect" FCAT scores | Rank-deficient PCA + perfectly separable classifiers | Don't run sciRED on pseudo-bulk (< 100 samples). Use `factomineR-framework` (planned) or `mofa-cellular` instead |
| Confounder included in design matrix has no axis | `poissonGLM` residualisation strips its main effect *before* PCA | Decide deliberately: residualise away technical confounders, **leave biological ones in the metadata** and let FCAT name them |

---

## Bringing sciRED Closer to a Biplot

sciRED's interpretation reads as **(level → factor) → (factor → top genes)**, two table lookups, never co-projected. Two cheap patches close most of the gap (see `references/geometric-caveats.md` and `factor-analysis-framework/references/supplementary-projection.md`):

```python
# Continuous-arrow overlay (~10 lines; generalises corr.py:4-13)
def continuous_arrows(scores, metadata_df):
    return {col: np.corrcoef(metadata_df[col], scores.T)[0, 1:]
            for col in metadata_df.select_dtypes(include="number")}

# Categorical-level barycenters (~10 lines; the move sciRED never makes)
def level_barycenters(scores, labels):
    return {lvl: scores[labels == lvl].mean(axis=0) for lvl in labels.unique()}
```

Both overlays can be plotted on the same `plot_factor_scatter` axes — they are valid in the post-varimax basis (varimax is orthogonal, so barycenters rotate consistently). They restore three of the four Benzécri properties on top of sciRED's existing varimax scores.

---

## Resources

- **Repository:** https://github.com/delipouya/sciRED
- **Paper:** Pouyabahar et al., *Interpretable single-cell factor decomposition using sciRED.* https://www.nature.com/articles/s41467-025-57157-2
- **Tutorials (in-source):** `tutorial1_scMixology.ipynb`, `tutorial2_stimulatedPBMC.ipynb`
- **Examples (in-source):** `example_scMixology.py`, `example_stimulatedPBMC.py`, `example_healthyHumanLiver.py`, `example_healthyHumanKidney.py`, `example_healthyRatLiver.py`
- **Internal audit:** `docs/vision/latent/sciRED.md` — full file:line breakdown

---

## When not to use

- Do not pass log-normalised data to poissonGLM. The GLM expects raw integer counts; pass the raw counts and log-normalise downstream if needed.
- Do not interpret varimax-rotated `explained_variance_ratio_` as a Benzécri inertia budget. Varimax breaks SVD uniqueness; per-factor variance is non-orthogonal and non-additive.
- Do not use plot_factor_loading as a biplot. It is a one-block gene-loadings scatter on F_x × F_y; the cell-scatter is a separate figure with no shared rescaling.
- Do not use FCAT/FIST without resampling stability. Classifier-based scoreboards are sensitive to seed and to varimax sign/order; cross-run comparability requires Procrustes alignment, which sciRED does not provide.
- Do not run on > ~10⁵ cells. The PCA core is dense `sklearn.decomposition.PCA`; the per-gene Poisson GLM loop is sequential; memory and runtime grow accordingly.

---

## See also

- `factor-analysis-framework` — Parent / super-family; conceptual framing for why sciRED strips three Benzécri properties
- `mofa-framework` — Alternative family; multi-view / multi-omic factor analysis
- `mofa-mofapy2` — the `mofa-framework` engine used for that alternative-family analysis
- `scanpy` — Prerequisite; HVG selection (`pp.highly_variable_genes`) and standard preprocessing before the factor decomposition
- `anndata` — Prerequisite; count loading and the AnnData object manipulation sciRED operates on

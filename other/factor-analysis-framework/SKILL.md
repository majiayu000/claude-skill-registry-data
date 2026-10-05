---
name: factor-analysis-framework
description: "Factor-analysis super-family router — chooses between probabilistic (MOFA-class) and geometric (FAMD/Benzecri-class) families by grain (cell vs pseudo-bulk), modality, and question (a MODEL of the data-generating process vs a MAP of the data table). Use first when starting any latent-decomposition analysis. Children: mofa-framework, scired."
license: MIT
---

# Factor-Analysis Super-Family Router

## Overview

Factor analysis is not one method but two competing intellectual traditions: a probabilistic one (Bayesian generative models, MOFA-class) that asks "is this a good MODEL of the data-generating process?", and a geometric one (Benzécri-school SVD on a metricized table, FAMD/MFA-class) that asks "is this a good MAP of the data table?". The two are orthogonal, not contradictory — every modern single-cell method makes architectural trades on this axis without naming the trade. This skill is the router that names it; concrete implementations live as children — today `mofa-framework` (multi-view family router) and `scired` (sciRED single-codebase implementation, single-omic). Planned families: `factomineR-framework`, `mixomics-framework`, `scitd-framework`, `diablo-framework`.

**When to use this skill:**
- Starting any multi-view / multi-block / multi-omic latent decomposition, especially with mixed continuous + categorical features.
- Working at pseudo-bulk × donor grain (donor × gene, donor × pathway-activity) and wanting a biplot rather than a UMAP.
- Asked to "interpret the latent space": route through the modelling-vs-map gate before picking a method.
- Choosing between MOFA, FAMD/MFA, mixOmics/DIABLO, scITD, sciRED — this skill names the axes.

**When NOT to use this skill:**
- Single-omic gene × cell, just want a 2D embedding for visualisation → use `scanpy` PCA + UMAP directly.
- Nonlinear manifold embedding for cell-type viz → UMAP / t-SNE; factor analysis assumes a (near-)linear bilinear decomposition.
- Pure batch correction with no interpretive ambition → `scvi-framework` family.
- You already know which family you want → skip this router and go to the child (`mofa-framework`, etc.).

---

## The two axes you must pick on

Every factor-analysis method scores independently on two axes. They look like one axis from inside any one paper; from outside they are clearly two. See `references/modelling-vs-map.md` for the long form; the short form:

| Axis | "Good MODEL" — modelling fitness | "Good MAP" — geometric interpretability |
|---|---|---|
| Question | Does this method match the data-generating process? | Does this method preserve the data table's structure in readable geometry? |
| What it rewards | Right likelihood per view, missing-data marginalisation, sparsity, scale, shared-vs-private factor decomposition, posterior uncertainty | Single SVD producing rows and columns in one space, inertia partitioning, categorical-level barycenter, distribution-free |
| Winner at single-cell scale | MOFA+ > NMF > sPLS > FAMD > raw CCA | FactoMineR / prince ≫ DIABLO ≈ mixOmics > scITD > MOFA ≈ sciRED |
| Tradition | Anglo-American statistical modelling (post-2010 ML stack) | French school (Benzécri, "Le modèle doit suivre les données, et non l'inverse.") |
| Best for | Predicting the next dataset; honest fitting of n≪p multi-omic counts | Understanding what is in this dataset; reading metadata onto the same axes as the samples |

> "Is this method a good MODEL of my data? = does it correctly represent the data-generating process? — Anglo-American axis. The field's habit since 2010.
> Is this method a good MAP of my data? = does it preserve the data's structure in a readable geometry? — French school axis. The field's blind spot."
> — `docs/vision/latent/post-synthesis-discussion.md §2`

You do not have to choose one axis: the supplementary-projection patch (below, §"Level-1 patch") lets a project fit on the modelling axis (MOFA, scVI mean, GLM-PCA) and *read* on the geometric axis. The router exists to make this choice deliberate.

---

## The Benzécri four-property frame

The geometric axis is operationally defined by four properties any classical factor-analytic method must satisfy. They come from Benzécri's *L'Analyse des Données* (1973) and were implemented faithfully in FactoMineR; the modern stack each ablates a different subset. See `references/benzecri-properties.md` for the full operational definitions and FactoMineR code citations.

| Codebase | Duality | Inertia partition | Categorical-as-barycenter | Distribution-free | Verdict |
|---|---|---|---|---|---|
| **FactoMineR** | yes — single SVD via `svd.triplet`, transition formula at `R/PCA.R:114-115` | yes — `$eig`, per-var `ctr`/`cos²` summing to 100% per axis (`R/PCA.R:103-119`) | yes — `quali.sup`/`quanti.sup` first-class, eta², v.test (`R/PCA.R:187-205`) | yes — one `base::svd()`, no priors | ground truth |
| **mixOmics** | partial — biplot exists but cosmetic rescaler at `R/biplot.R:77`, not √λ | partial — `prop_expl_var` is *redundancy* (`Rd(X,t_h)`), not eigenvalue fraction | no — `unmap()` makes 0/1 indicator without 1/√p_k rescaling; centroids in `plotIndiv` are visual only | yes — deterministic NIPALS/SVD | partial |
| **DIABLO** | weak — within-block only; no single SVD across blocks; post-hoc `cor()` recomputation | partial — AVE + per-block redundancy; no λ_α partition | no — Y is the outcome, drives axes; no `quali.sup` for unmodelled covariates | yes — deterministic block-power-iteration | partial |
| **MOFA** | no — Z and W are posterior expectations of two latent variables linked by a likelihood; no biplot function across MOFA2 / mofapy2 / MOFAcellulaR | no — per-(view,group,factor) R² does not sum; `max(0,.)` floor (`calculate_variance_explained.R:73-76`) | no at fit; post-hoc numbers exist in `summarise_factors` and `correlate_factors_with_covariates`, rendered as tile/`corrplot`, never as a biplot overlay | no — fully Bayesian VI, depends on prior/init/seed | strips all four |
| **sciRED** | no — PCA + varimax/promax; gene and cell scatters live on different axes; rotation breaks transition formula | partial — `explained_variance_ratio_` computed but unread; FIST min-max-scales `factor_variance` | no — categoricals are nuisance regressors / supervised targets / colourings, never barycenters | mixed — PCA distribution-free, Poisson GLM upstream is likelihood-based, varimax breaks SVD uniqueness | strips three |
| **scITD** | partial — Tucker-2 produces (donor scores, gene×celltype loadings) but core tensor fused into loadings at `run_tucker_ica.R:137`; only diagnostic `pca_unfolded` (L318-361) is a proper biplot | partial — `get_factor_exp_var` is rank-1 reconstruction loss; ICA rotation makes per-factor exp_var non-additive | failed — `get_meta_associations` is post-hoc regression returning R²/p, not coordinates | yes — Tucker + HOSVD-ALS + ICA + varimax all distribution-free | strips two |

What stands out: **categorical-level-as-barycenter** is the property that fell off the cliff. Three modern codebases (MOFA, scITD, sciRED) compute the right number — per-level mean factor score — somewhere in their codebases, then render it as a heatmap, table, or regression coefficient, never as a labelled point on the same axes as the rows. The patch is one renderer per host. See synthesis §1, §2.3.

---

## Family-selection decision tree

```
Starting a factor analysis?
│
├─ Grain: single-cell (n ≳ 10⁴ cells)?
│   │
│   ├─ Multi-view / multi-omic with per-view likelihoods needed?
│   │   ├─ Need missing-modality handling, ARD sparsity, shared-vs-private?
│   │   │   → mofa-framework             [implemented]
│   │   └─ Single-view, raw counts, want interpretable rotated factors?
│   │       → scired                     [implemented]
│   │
│   └─ Single-view RNA only, want a probabilistic embedding for downstream?
│       → scvi-framework (sibling super-family — VAEs, not bilinear factor analysis)
│
└─ Grain: pseudo-bulk (n ≲ 10³ donors / samples)?
    │
    ├─ Multi-block (RNA + ATAC + pathways + clinical metadata)?
    │   ├─ Want a TRUE biplot — sample points + variable arrows + categorical levels?
    │   │   → factomineR-framework (MFA)  [planned]
    │   ├─ Sparse / supervised multi-block (block-PLS, DIABLO)?
    │   │   → mixomics-framework          [planned]
    │   └─ Tensor structure (donor × gene × cell-type)?
    │       → scitd-framework             [planned]
    │
    └─ Single-block continuous / mixed?
        ├─ Mixed continuous + categorical, want quali.sup / quanti.sup overlay?
        │   → factomineR-framework (PCA/FAMD/MCA)  [planned]
        └─ Multi-view donor-level, prefer probabilistic?
            → mofa-framework (via MOFAcellulaR)    [implemented]
```

The question-type filter (good MODEL vs good MAP) is the *final* gate. After the grain and modality routes pick a candidate, ask:

- **MODEL question** ("predict / fit / honest likelihood") → keep the probabilistic candidate (MOFA, scVI).
- **MAP question** ("interpret / read metadata / wet-lab handoff") → either pick the geometric candidate (FactoMineR/MFA) directly, or apply the Level-1 patch on top of the probabilistic candidate.

For the full ranking on each axis see `references/modelling-vs-map.md`. For per-family detail see `references/families-roster.md`.

---

## The Level-1 supplementary-projection patch

This is the single most underused move in single-cell factor analysis, and the cheapest. Synthesis §5/§6 names it as the highest-leverage one-afternoon patch in the sequence.

Given any linear embedding `F: samples × K` (PCA, MOFA's Z, scVI mean, GLM-PCA, FAMD scores, MFA scores) and any metadata DataFrame:

- Place each **continuous** variable `v` as an arrow on the F1×F2 scatter, tip at `(cor(v, F_1), cor(v, F_2))`.
- Place each **categorical** level `ℓ` as a labelled point at the barycenter `colMeans(F[labels == ℓ, :])`, optionally rescaled by `1/√λ_α`.
- Report `v.test`, `eta²`, `cos²` per axis × level — the FactoMineR vocabulary.

This is one renderer per host (`MOFA2::correlate_factors_with_covariates` already computes the continuous numbers; `MOFA2::summarise_factors` already computes the categorical means; what is missing is the `geom_segment` + `geom_text` overlay on the same axes as `plot_factors`). Effort: ~50 lines per host; ~30 lines + a 100-line typed wrapper for a host-neutral helper.

Why it matters: nobody in single-cell ships this. The numeric machinery is hiding inside every modern codebase; the renderer that puts continuous arrows and categorical level-points on the *same* axes as the sample scatter is the part nobody wrote. That overlay restores three of the four Benzécri properties on top of *any* honest fitter — including MOFA, which fails all four at fit time.

Formulas, receipts, and the open questions (sign convention, finite-population correction, cardinality cap, cross-host comparability) are in `references/supplementary-projection.md`.

---

## Cross-cutting references (load on demand)

| Topic | File |
|---|---|
| Operational definitions of the four Benzécri properties + FactoMineR code citations | `references/benzecri-properties.md` |
| "Good MODEL vs good MAP" — the long-form essay reconciling the ml ranking with the geometric audit | `references/modelling-vs-map.md` |
| Per-family one-pagers (MOFA, FactoMineR/prince, mixOmics, DIABLO, scITD, sciRED) — scope, modality, strengths, weaknesses, status | `references/families-roster.md` |
| Level-1 patch formulas + receipts + open questions | `references/supplementary-projection.md` |

Child framework skills (`mofa-framework`, future `factomineR-framework`, …) link directly into these — do not copy-paste their content into a child SKILL.md.

---

## Resources

- Benzécri, J.-P. *L'Analyse des Données*. Dunod, 1973. (Book, no link.)
- FactoMineR: https://factominer.free.fr/
- MOFA2: https://biofam.github.io/MOFA2/
- mixOmics: http://mixomics.org/
- MOFA original paper: https://www.embopress.org/doi/full/10.15252/msb.20178124
- DIABLO / mixOmics multi-block: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0030153
- Whitepaper (internal): `docs/vision/research/The Geometry We Left Behind.md`
- Synthesis (internal): `docs/vision/latent/synthesis.md`

---

## When not to use

- Do not use this skill alone to run an analysis. Pair with one of the implemented children (mofa-framework for the MOFA family, scired for sciRED) or a planned family-framework once it lands.
- Do not use as a substitute for UMAP/t-SNE-style nonlinear viz. Use scanpy + UMAP/t-SNE instead. Factor analysis assumes a linear (or near-linear) bilinear decomposition.

---

## See also

- `mofa-framework`
- `scired`
- `scvi-framework`
- `scanpy`
- `anndata`
- `muon-multimodal-analysis`

Upstream docs: https://factominer.free.fr/index.html

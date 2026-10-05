---
name: dimensionality-reduction
description: "Reduction is a trade, not an improvement."
---

# Dimensionality Reduction (Verbose)

## Core Patterns

### Deciding Whether to Reduce at All

Reduction is a trade, not an improvement. You give up interpretability and some signal
in exchange for speed, decorrelation, or a picture. Reach for it when at least one of
these holds:

- Features vastly outnumber samples (p ≫ n) and a linear model cannot be regularized enough
- Features are strongly collinear and the model is sensitive to that (linear, k-NN, k-means)
- Inference latency or memory is bounded and the feature vector dominates it
- You need a 2-D view of structure for human consumption

Gradient boosting on 200 moderately correlated tabular features needs none of this.
Feeding it PCA components typically costs accuracy — the trees lose the axis-aligned
splits that matched real variables — and buys nothing.

### PCA

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ("scale", StandardScaler()),
    ("pca", PCA(n_components=0.95, svd_solver="full", random_state=0)),
    ("clf", LogisticRegression(max_iter=1000)),
])
```

PCA finds orthogonal directions of maximum variance via the SVD of the centred data
matrix. Two properties follow directly and explain most misuse:

**It is scale-dependent.** Variance is measured in the units of each column. A feature
in dollars will dominate one in years by a factor of millions. `PCA` centres but never
standardizes, so `StandardScaler` is mandatory for mixed units.

**It is unsupervised.** The directions of greatest variance need not be the directions
that separate classes. A low-variance component can carry all the discriminative
signal, and dropping it destroys the model while retaining 99% of variance.

Choosing the rank:

```python
pca = PCA().fit(X_scaled)
cum = pca.explained_variance_ratio_.cumsum()
print(f"90%: {(cum < 0.90).sum() + 1} comps, 95%: {(cum < 0.95).sum() + 1} comps")
```

Passing a float to `n_components` selects the smallest rank reaching that ratio.
Better still, treat it as a hyperparameter and let the downstream metric decide:

```python
GridSearchCV(pipe, {"pca__n_components": [10, 25, 50, 100]}, cv=5, scoring="roc_auc")
```

| Solver | When |
|---|---|
| `"full"` | n_features small; exact |
| `"randomized"` | n_features large, n_components ≪ n_features; much faster |
| `"auto"` | Default; picks by shape |

For data too large for memory, `IncrementalPCA` fits in `partial_fit` batches at a
small cost in precision.

### Sparse Data

```python
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

X = TfidfVectorizer(max_features=50_000).fit_transform(docs)   # sparse
svd = TruncatedSVD(n_components=300, random_state=0)           # LSA
Z = svd.fit_transform(X)
```

Never call `PCA` on a sparse matrix. Centring destroys sparsity: a 50,000-column TF-IDF
matrix at 0.1% density becomes fully dense and blows past available memory.
`TruncatedSVD` skips the centring step and operates on the sparse matrix directly.
Because it does not centre, its components are not identical to PCA's even on the same
data — a difference that matters when reproducing published numbers.

### Supervised Reduction

```python
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

lda = LDA(n_components=2)      # capped at n_classes - 1
Z = lda.fit_transform(X_scaled, y)
```

LDA maximizes between-class over within-class scatter, so it targets separability
rather than variance. The hard cap at `n_classes - 1` components is structural: binary
classification yields exactly one dimension. Because it uses `y`, LDA must be fitted
inside the CV fold like any supervised step.

### Manifold Methods for Visualization

```python
from sklearn.manifold import TSNE

Z = TSNE(n_components=2, perplexity=30, init="pca", random_state=0).fit_transform(X)
```

t-SNE preserves local neighbourhoods and deliberately discards global geometry. Three
consequences are routinely misread:

1. **Distances between clusters are meaningless.** Two clusters at opposite corners may
   be adjacent in the source space.
2. **Cluster sizes are meaningless.** t-SNE equalizes density; a large blob is not a
   larger or more variable group.
3. **`perplexity` changes the answer.** At 5 the plot fragments into micro-clusters; at
   50 it merges them. Run several values before drawing a conclusion.

t-SNE exposes no `transform`, so it cannot embed unseen points and cannot appear in a
serving pipeline. UMAP can (`umap.UMAP().transform`), is much faster at scale, and
retains more global structure — but it is still a visualization tool first, and any
claim that its clusters are "real" needs corroboration from the original space.

Standard practice on wide data: PCA down to ~50 components first, then t-SNE or UMAP.
This denoises and cuts runtime substantially.

### Feature Selection as the Alternative

When interpretability, auditability, or serving cost matter, selecting a subset beats
projecting into a new basis — you keep column names and can stop computing the columns
you dropped.

```python
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LassoCV

sel = SelectFromModel(LassoCV(cv=5)).fit(X_scaled, y)   # L1 drives weights to zero
kept = X.columns[sel.get_support()]
```

PCA still requires all original inputs at inference time — every component is a
combination of all of them — so it reduces model width but not data-collection cost.
Selection reduces both.

## Common Anti-Patterns

❌ **PCA on unstandardized features of mixed units.**
✅ `StandardScaler` immediately before `PCA`, in the same pipeline.

❌ **`PCA` on a sparse matrix** — centring densifies and exhausts memory.
✅ `TruncatedSVD`.

❌ **Fitting the reducer on the full dataset before splitting** — validation covariance
leaks into the basis.
✅ Reducer as a `Pipeline` step, refit per fold.

❌ **Interpreting PC1 as a business variable.**
✅ Treat components as opaque; use feature selection when explanation is required.

❌ **Reading inter-cluster distances or cluster sizes off a t-SNE plot.**
✅ Read only local neighbourhood membership; verify in the original space.

❌ **t-SNE embeddings as model features** — no `transform`, non-deterministic, not
serveable.
✅ PCA or UMAP if an embedding must be applied to new data.

❌ **Reducing before a gradient-boosted tree** to "help" it.
✅ Trees handle wide correlated inputs; measure before assuming reduction helps.

❌ **Fixing `n_components=2` because it plots nicely, then modelling on it.**
✅ Tune the rank against the downstream metric.

❌ **Assuming 95% retained variance means 95% retained signal.**
✅ Compare end-to-end scores with and without reduction.

## Dimensionality Reduction Checklist

- [ ] Reduction justified by p ≫ n, collinearity, latency, or visualization
- [ ] Features standardized before PCA
- [ ] `TruncatedSVD` used for sparse input, not `PCA`
- [ ] Reducer inside a `Pipeline`, fitted per fold
- [ ] `n_components` chosen from the variance curve or tuned by CV
- [ ] `explained_variance_ratio_` inspected, not assumed
- [ ] Baseline model without reduction measured for comparison
- [ ] Components never presented as interpretable variables
- [ ] `perplexity` varied before trusting any t-SNE structure
- [ ] t-SNE confined to visualization, never to a serving path
- [ ] PCA applied before t-SNE/UMAP on wide data
- [ ] Feature selection considered where interpretability or input cost matters
- [ ] Fitted reducer persisted with the model so serving uses the identical basis

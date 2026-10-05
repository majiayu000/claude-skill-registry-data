---
name: rna-velocity-trajectory
description: "Infers directional cellular trajectories from scRNA-seq using spliced/unspliced ratios. Use when predicting cell fates, differentiation endpoints, or driver genes from a single snapshot — covers scVelo, VeloVI, Chronocell, and CellRank. Needs intron-aware quantification; for the upstream counting use starsolo-spliced-unspliced."
license: MIT
---

# RNA Velocity & Trajectory Inference: Cellular Dynamics from Splicing Kinetics

**Foundation:** RNA velocity infers cellular differentiation trajectories and future cell states by modeling the ratio of unspliced (nascent) to spliced (mature) RNA. The change in spliced RNA over time—termed RNA velocity—predicts where cells are heading in gene expression space.

## When to Use RNA Velocity

- **Infer developmental trajectories** from single snapshot scRNA-seq data
- **Predict terminal cell fates** and differentiation endpoints
- **Identify driver genes** for cell state transitions
- **Validate lineage relationships** in differentiation systems
- **Analyze cell cycle dynamics** and proliferation states
- **Study transient cell populations** in development or disease

**Limitations:**
- Requires alignment to capture intronic reads (spliced/unspliced quantification)
- Time scale of process must match RNA half-life (~hours)
- Fails in steady-state systems (e.g., mature PBMCs with no transitions)
- Phase portraits must show expected almond shape for reliable inference
- Low-dimensional projections can be misleading; use CellRank for rigorous analysis

---

## Quick Start: scVelo

```python
import scvelo as scv
import scanpy as sc

# Load data with spliced/unspliced layers
adata = scv.read_loom("velocyto_output.loom")
# Or: adata.layers["spliced"], adata.layers["unspliced"] from kallisto|bustools

# Preprocessing
scv.pp.filter_and_normalize(adata, min_shared_counts=20, n_top_genes=2000)
scv.pp.moments(adata, n_pcs=30, n_neighbors=30)

# Compute velocity (dynamical model recommended)
scv.tl.recover_dynamics(adata, n_jobs=8)  # Infer kinetic rates
scv.tl.velocity(adata, mode="dynamical")

# Build velocity graph and visualize
scv.tl.velocity_graph(adata, n_jobs=8)
scv.pl.velocity_embedding_stream(adata, basis="umap", color="clusters")
```

---

## Velocity Models Comparison

| Model | Command | Assumptions | Use When |
|-------|---------|-------------|----------|
| **Steady-state** | `mode="deterministic"` | Equilibrium reached, common splicing rate | Quick exploration, simple systems |
| **EM/Dynamical** | `mode="dynamical"` after `recover_dynamics()` | Gene-specific rates, full kinetics | Publication-quality, complex trajectories |
| **Stochastic** | `mode="stochastic"` | Adds noise estimation | Uncertainty quantification |

**Dynamical model parameters:**
```python
scv.tl.recover_dynamics(
    adata,
    n_jobs=8,                    # Parallel processing
    fit_scaling=True,            # Gene-wise scaling
    var_names='velocity_genes',  # Subset to velocity genes
    max_iter=100                 # EM iterations
)
# Outputs: adata.var["fit_alpha", "fit_beta", "fit_gamma", "fit_t_", "fit_likelihood"]
```

---

## scVelo AnnData Output Fields

After running the scVelo workflow, the following fields are added to the AnnData object:

| Location | Key | Description |
|----------|-----|-------------|
| `adata.layers` | `velocity` | RNA velocity per gene per cell |
| `adata.layers` | `fit_t` | Fitted latent time per gene per cell (dynamical only) |
| `adata.obsm` | `velocity_umap` | 2D velocity vectors projected onto UMAP |
| `adata.obs` | `velocity_pseudotime` | Pseudotime inferred from velocity graph |
| `adata.obs` | `latent_time` | Shared latent time from dynamical model |
| `adata.obs` | `velocity_length` | Speed of each cell (magnitude) |
| `adata.obs` | `velocity_confidence` | Coherence of velocity direction |
| `adata.var` | `fit_likelihood` | Gene-level model fit quality (dynamical only) |
| `adata.var` | `fit_alpha` | Transcription rate per gene |
| `adata.var` | `fit_beta` | Splicing rate per gene |
| `adata.var` | `fit_gamma` | Degradation rate per gene |
| `adata.uns` | `velocity_graph` | Cell-cell transition probability matrix |

**Quick inspection:**
```python
# After running velocity workflow
print([k for k in adata.obs.columns if 'velocity' in k or 'latent' in k])
print([k for k in adata.layers.keys()])
print([k for k in adata.var.columns if 'fit_' in k])
```

---

## VeloVI: Variational Inference for Velocity

VeloVI provides uncertainty quantification via a variational autoencoder framework.

```python
from velovi import VELOVI, preprocess_data
import scvelo as scv

# Load and preprocess
adata = scv.datasets.pancreas()
scv.pp.filter_and_normalize(adata, min_shared_counts=30, n_top_genes=2000)
scv.pp.moments(adata, n_pcs=30, n_neighbors=30)
adata = preprocess_data(adata)  # Runs scVelo velocity internally

# Setup and train
VELOVI.setup_anndata(adata, spliced_layer="Ms", unspliced_layer="Mu")
vae = VELOVI(adata)
vae.train()  # ~5-10 min, early stopping enabled

# Extract outputs
latent_time = vae.get_latent_time(n_samples=25)
velocities = vae.get_velocity(n_samples=25, velo_statistic="mean")
adata.layers["velocity"] = velocities

# Uncertainty quantification
uncertainty_df, _ = vae.get_directional_uncertainty(n_samples=100)
adata.obs["velocity_uncertainty"] = uncertainty_df["directional_cosine_sim_variance"].values

# Gene-level confidence via permutation
perm_df, _ = vae.get_permutation_scores(labels_key="clusters")
adata.var["permutation_score"] = perm_df.max(1).values
```

**VeloVI advantages:**
- Probabilistic framework with uncertainty estimates
- Intrinsic uncertainty (per-cell) and extrinsic uncertainty (model stability)
- Permutation scores identify genes with reliable velocity signals
- Better handling of noisy data

---

## Chronocell: Biophysical Trajectory Modeling

Chronocell infers trajectories using explicit kinetic equations and topology specification. It provides pseudotime, state assignments, and kinetic parameter estimates.

**Installation:**
```python
import sys
sys.path.insert(0, '/path/to/FGP_2024')  # Local copy
# Or: pip install git+https://github.com/pachterlab/Chronocell.git
```

**Basic usage:**
```python
from Chronocell.inference import Trajectory
from Chronocell.utils import select_genes_by_G
from Chronocell.plotting import plot_t, plot_y
import numpy as np

# Prepare data (n_cells x n_genes x 2 array)
X = np.stack([
    adata.layers["unspliced"].toarray(),
    adata.layers["spliced"].toarray()
], axis=-1)

# Select informative genes via G-test
gene_mask = select_genes_by_G(adata, model="Poisson", n_genes=50)
X_select = X[:, gene_mask, :]

# Define topology: linear trajectory with 3 states
topo = np.array([[0, 1, 2]])           # State 0 → 1 → 2
tau = np.array([0.0, 1.0, 2.0, 3.0])   # Transition timepoints

# Fit trajectory
traj = Trajectory(topo, tau, model="two_species_ss", verbose=1)
traj = traj.fit(
    X_select,
    n_init=20,              # Multiple random restarts (critical)
    epoch=100,              # EM iterations
    params={'r': adata.obs["total_counts"].values},  # Read depth
    parallel=True,
    n_threads=8
)

# Extract results
cell_pseudotime = (traj.Q.sum(1) @ traj.t)  # Weighted average time
cell_states = traj.Q.sum(2).argmax(1)       # Most likely state
adata.obs["chronocell_time"] = cell_pseudotime

# Model comparison
print(f"ELBO: {traj.compute_lower_bound(X_select):.2f}")
print(f"AIC: {traj.compute_AIC(X_select):.2f}")
print(f"BIC: {traj.compute_BIC(X_select):.2f}")

# Visualize
plot_t(traj)                    # Cell-time-state posterior heatmap
plot_y(traj, idx=np.arange(5))  # Gene expression trajectories
```

**Chronocell models:**
| Model | Description | Use Case |
|-------|-------------|----------|
| `one_species` | Single RNA species (spliced only) | Simplified analysis |
| `two_species_ss` | Two species, steady-state splicing | Standard velocity data |
| `two_species_ss_tau` | Gene-wise time shifts | Non-steady-state genes |

**Topology examples:**
```python
# Linear: 0 → 1 → 2
topo = np.array([[0, 1, 2]])

# Bifurcating: 0 → 1 → {2, 3}
topo = np.array([[0, 1, 2],
                 [0, 1, 3]])

# Merging: {0, 1} → 2
topo = np.array([[0, 2],
                 [1, 2]])
```

---

## CellRank Integration

CellRank uses velocity to compute fate probabilities and terminal states, avoiding misleading 2D projections.

```python
import cellrank as cr

# Initialize kernel from velocity
vk = cr.kernels.VelocityKernel(adata)
vk.compute_transition_matrix()

# Combine with connectivity kernel for robustness
ck = cr.kernels.ConnectivityKernel(adata)
ck.compute_transition_matrix()
combined_kernel = 0.8 * vk + 0.2 * ck

# Compute fate probabilities
g = cr.estimators.GPCCA(combined_kernel)
g.compute_macrostates(n_states=5)
g.set_terminal_states_from_macrostates()
g.compute_fate_probabilities()

# Visualize
cr.pl.fate_probabilities(adata)
g.compute_lineage_drivers()
```

---

## Data Preparation

### Spliced/Unspliced Quantification

**Option 1: velocyto** (BAM-based)
```bash
velocyto run10x /path/to/cellranger_output gtf_file.gtf
# Output: velocyto_output.loom with spliced/unspliced layers
```

**Option 2: kallisto|bustools** (Pseudoalignment, faster)
```bash
kb count -i index.idx -g t2g.txt -x 10xv3 \
  --workflow lamanno --loom \
  R1.fastq.gz R2.fastq.gz
```

**Option 3: alevin-fry** (Memory efficient)
```bash
alevin-fry quant --usa  # Unspliced/spliced/ambiguous mode
```

### Loading into AnnData
```python
# From loom file
adata = scv.read_loom("output.loom")

# From separate matrices
adata = sc.read_h5ad("processed.h5ad")
adata.layers["spliced"] = spliced_matrix
adata.layers["unspliced"] = unspliced_matrix

# Verify layers exist
assert "spliced" in adata.layers and "unspliced" in adata.layers
```

---

## Downstream Analysis

### Latent Time
```python
scv.tl.latent_time(adata)
scv.pl.scatter(adata, color="latent_time", cmap="gnuplot")
```

### Velocity Confidence & Genes
```python
# Confidence per cell
scv.tl.velocity_confidence(adata)
scv.pl.scatter(adata, color="velocity_confidence")

# Top velocity genes
scv.tl.rank_velocity_genes(adata, groupby="clusters", min_corr=0.3)
top_genes = adata.uns["rank_velocity_genes"]["names"]["cluster_1"][:10]
scv.pl.scatter(adata, basis=top_genes[:3], color="clusters")
```

### Phase Portraits
```python
# Check model fit quality
scv.pl.velocity(adata, var_names=["Gene1", "Gene2", "Gene3"], color="clusters")
```

---

## Critical Gotchas

| Issue | Solution |
|-------|----------|
| No almond-shaped phase portrait | Gene violates kinetic assumptions; exclude from analysis |
| Backflow in velocity stream | Check if steady-state assumption violated; use dynamical model |
| All velocities point same direction | Insufficient dynamic range; check if system is at steady state |
| Low spliced/unspliced ratio | Poor intronic capture; check alignment to introns |
| Conflicting velocity directions | Use CellRank for robust fate inference instead of 2D projection |
| Missing `layers["spliced"]` | Need velocity-aware quantification (velocyto, kb count --lamanno) |
| Chronocell poor convergence | Increase `n_init` (20+), check topology matches biology |
| VeloVI training unstable | Reduce learning rate, increase n_epochs for warmup |

---

## Model Selection Guidelines

**When to use each tool:**

| Scenario | Recommended Tool |
|----------|-----------------|
| Quick exploration | scVelo steady-state |
| Publication-quality velocity | scVelo dynamical |
| Uncertainty quantification | VeloVI |
| Explicit topology/pseudotime | Chronocell |
| Fate probability, terminal states | CellRank |
| Cross-method validation | Run multiple, compare |

**Velocity gene selection:**
```python
# scVelo: automatic during recover_dynamics
# Manual: filter by fit likelihood
good_genes = adata.var["fit_likelihood"] > 0.1

# VeloVI: permutation score
good_genes = adata.var["permutation_score"] > 0.05
```

---

## Visualization Best Practices

```python
# Stream plot (most common, but can mislead)
scv.pl.velocity_embedding_stream(adata, basis="umap", color="clusters")

# Arrow plot (more precise direction)
scv.pl.velocity_embedding(adata, basis="umap", arrow_length=3, arrow_size=2)

# Grid plot (summarized flow)
scv.pl.velocity_embedding_grid(adata, basis="umap", color="clusters")

# Phase portraits for top genes (model validation)
top_genes = adata.var["fit_likelihood"].sort_values(ascending=False).index[:6]
scv.pl.scatter(adata, basis=top_genes, color="clusters", frameon=False)

# Latent time heatmap
scv.pl.heatmap(adata, var_names=top_genes, sortby="latent_time", col_color="clusters")
```

---

## Resources

**scVelo:**
- Documentation: https://scvelo.readthedocs.io
- Paper: Bergen et al. 2020, Nature Biotechnology
- Tutorial: https://scvelo.readthedocs.io/en/stable/DynamicalModeling/

**VeloVI:**
- Documentation: https://docs.scvi-tools.org/en/stable/user_guide/models/velovi.html
- Paper: Gayoso et al. 2022, Nature Biotechnology
- Tutorial: https://docs.scvi-tools.org/en/stable/tutorials/notebooks/scrna/velovi.html

**Chronocell:**
- GitHub: https://github.com/pachterlab/Chronocell
- Paper: Fang, Gorin & Pachter 2025, PLoS Computational Biology
- Local: `/01_Scripts/FGP_2024/Chronocell/`

**CellRank:**
- Documentation: https://cellrank.readthedocs.io
- Paper: Lange et al. 2022, Nature Methods

**RNA velocity theory:**
- Original paper: La Manno et al. 2018, Nature
- Review: Bergen et al. 2021, Molecular Systems Biology

---

## When not to use

- Do not use on steady-state systems (e.g. mature PBMCs) — velocity assumptions fail.
- Do not use without spliced/unspliced layers — requires intron-aware quantification upstream.

---

## See also

- `starsolo-spliced-unspliced`
- `scanpy`
- `anndata`

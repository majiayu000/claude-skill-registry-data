---
name: region-aware-matching
description: "Spatial region-aware cell matching for CODEX/scRNAseq integration"
author: smith6jt
date: 2024-12-27
---

# Region-Aware Matching - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-27 |
| **Goal** | Incorporate tissue heterogeneity (B cell follicles, T cell zones, etc.) into MaxFuse matching |
| **Environment** | Python 3.12, MaxFuse, scanpy, sklearn |
| **Status** | Implemented (3 approaches) |

## Context
Standard MaxFuse treats tissue as homogeneous during cell matching. In reality, tissues like spleen have distinct regions (B cell follicles, T cell zones, red pulp) where certain cell types should preferentially match. Without region awareness, B cells from scRNAseq might incorrectly match to CODEX cells in T cell zones.

## Verified Workflow

### Three-Pronged Approach
1. **Prior-weighted distance interpolation** - Encode biological expectations
2. **Neighborhood-augmented features** - Add spatial context to CODEX cells
3. **Post-hoc filtering** - Remove biologically implausible matches

### Key Functions Added to spatial_utils.py

```python
def detect_tissue_regions(locations, marker_expression, marker_names,
                          marker_to_region, n_neighbors=30, min_cluster_size=10,
                          eps_quantile=0.1):
    """
    Auto-detect tissue regions using:
    1. Classify cells by dominant marker expression (z-score > 0.5)
    2. Spatially cluster cells of each type using DBSCAN
    3. Assign region labels based on marker identity + spatial coherence
    """

def compute_region_celltype_prior(celltype_to_region_weights, rna_labels,
                                   spatial_regions, default_weight=1.0):
    """
    Build prior distance matrix for interpolation.
    Lower weight = more compatible (e.g., 0.1 for B cells in B follicles)
    Higher weight = less compatible (e.g., 5.0 for B cells in red pulp)
    """

def compute_neighborhood_augmented_features(features, locations, labels,
                                             n_neighbors=15, wt_on_features=0.7):
    """
    Augment features with spatial neighborhood composition.
    Cells near B cell follicles will have high B_cell neighbor counts.
    """
```

### Usage Pattern
```python
# 1. Detect tissue regions from CODEX markers
marker_to_region = {
    'CD20': 'B_follicle',
    'CD3e': 'T_zone',
    'CD68': 'Red_pulp'
}
regions, region_info = detect_tissue_regions(
    locations, marker_expression, marker_names, marker_to_region
)

# 2. Define prior weights
celltype_to_region_weights = {
    'B_cell': {'B_follicle': 0.1, 'T_zone': 2.0, 'Red_pulp': 5.0},
    'T_cell': {'B_follicle': 2.0, 'T_zone': 0.1, 'Red_pulp': 3.0},
}

# 3. Compute prior distance matrix
prior_dist = compute_region_celltype_prior(
    celltype_to_region_weights, rna_labels, regions
)

# 4. Interpolate with embedding distance
# final_dist = (1 - wt_on_base_dist) * embed_dist + wt_on_base_dist * prior_dist
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Hard region filtering | Too restrictive, lost valid matches | Use soft priors instead of hard constraints |
| Simple k-means on locations | Didn't capture irregular region shapes | DBSCAN better for tissue regions |
| Global marker thresholds | Batch effects across tissue | Use z-score normalization per marker |
| Matching only within regions | Some cell types span regions | Allow cross-region matches with penalty |

## Final Parameters

```yaml
# Region detection
n_neighbors: 30          # For k-NN density estimation
min_cluster_size: 10     # Minimum cells to form a region
eps_quantile: 0.1        # DBSCAN eps from k-NN distance distribution
z_score_threshold: 0.5   # Marker expression threshold

# Prior weights (tune per dataset)
compatible_weight: 0.1   # Expected cell type in region
neutral_weight: 1.0      # No prior knowledge
incompatible_weight: 5.0 # Unexpected cell type in region

# Distance interpolation
wt_on_base_dist: 0.3     # Weight on prior (0.2-0.4 works well)

# Neighborhood features
spatial_n_neighbors: 15
wt_on_features: 0.7      # Weight on expression vs neighborhood
```

## Key Insights
- Prior weights are log-transformed for smoother distance scaling
- Region detection works best with 2-4 marker genes per region
- Neighborhood features help even without explicit priors
- Post-hoc filtering catches remaining errors but loses some matches
- Start with weak priors (wt_on_base_dist=0.2), increase if needed

## References
- MaxFuse paper: Cross-modal matching with fuzzy smoothed embedding
- DBSCAN: Density-based spatial clustering
- Spleen tissue organization: B follicles, T zones, red/white pulp

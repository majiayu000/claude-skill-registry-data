---
name: single-cell-vector-search
description: "Searches large scRNA-seq atlases (SCimilarity 23M+, CELLxGENE Census 100M+) by embedding similarity to find matching cell states across diseases, tissues, and studies. Use for phenotype discovery, signature derivation from centroid queries, or cross-study cohort assembly. For plain label transfer use cellxgene-census-annotation."
license: MIT
---

# Single-Cell Vector Search Skill

## Overview
Search for similar cell states across large-scale scRNA-seq atlases (23M+ SCimilarity, 100M+ Census) using vector embeddings. Two main approaches with different strengths and requirements.

## Critical Tool Selection

**Use SCimilarity when:**
- ✅ Query is **human 10x Chromium data only**
- ✅ Need cell search across diseases/conditions
- ✅ Want to derive gene signatures or compute centroids
- ✅ Have **64GB+ RAM available locally**
- ✅ Want quality metrics (query_coherence) for centroid searches

**Use Census when:**
- ✅ Need **mouse or cross-species** queries
- ✅ Working with any organism in Census (human, mouse, etc.)
- ✅ Want **direct API access** (no local model download)
- ✅ Need scVI or TranscriptFormer embeddings
- ✅ Want label transfer or cell type prediction
- ✅ Limited local memory (<64GB)

## SCimilarity Workflow

### System Requirements
- **Memory**: Minimum 64GB RAM for kNN search
- **Platform**: 10x Chromium data only
- **Species**: Human only
- **Model size**: ~8GB download from Zenodo

### 1. Installation & Setup
```python
pip install scimilarity

# Download model from Zenodo (required, one-time ~8GB)
# https://zenodo.org/records/10685499
# Extract to /models/model_v1.1/

from scimilarity import CellQuery
from scimilarity.utils import lognorm_counts, align_dataset

# Load model (specify local path to downloaded model)
cq = CellQuery("/models/model_v1.1")
```

### 2. Preprocessing (CRITICAL - Must Match Training)
```python
# Step 1: Align genes to SCimilarity's gene order
# Zero-fills missing genes, removes genes not in model
adata = align_dataset(adata, cq.gene_order)

# Step 2: Normalize EXACTLY as model was trained (lognorm to 10k)
adata = lognorm_counts(adata)

# NEVER use other normalization - will give poor results
# Do NOT use sc.pp.normalize_total() or custom methods
```

### 3. Embedding Query Data
```python
# Embed all cells in your dataset
adata.obsm["X_scimilarity"] = cq.get_embeddings(adata.X)

# For visualization (optional)
import scanpy as sc
sc.pp.neighbors(adata, use_rep="X_scimilarity")
sc.tl.umap(adata)
```

### 4. Query Strategies

**Single Cell Query** (fast but noisy):
```python
# Query from a specific cell
query_cell = adata[cell_id]
query_embedding = cq.get_embeddings(query_cell.X)

k = 10000  # number of neighbors to return
nn_idxs, nn_dists, metadata = cq.search_nearest(query_embedding, k=k)

# metadata contains: study, sample, disease, tissue, prediction, etc.
```

**Centroid Query** (RECOMMENDED - more robust):
```python
# Mark cells for centroid (e.g., cells expressing markers)
adata.obs["query_cells"] = (condition)  # boolean mask

# Search returns centroid embedding + QC stats
centroid_emb, nn_idxs, nn_dists, metadata, qc_stats = \
    cq.search_centroid_nearest(adata, "query_cells")

# CRITICAL QC METRIC: query_coherence
print(qc_stats["query_coherence"])
# > 70: Excellent - tight, coherent cluster
# 50-70: Good - reasonably coherent
# 20-50: Marginal - scattered cluster, interpret cautiously
# < 20: Poor - do not trust results, redefine query
```

**Gene Signature Query**:
```python
# Score cells by signature
marker_genes = ["CD14", "FCGR1A", "CD68"]  # example
sc.tl.score_genes(adata, marker_genes, score_name="my_signature")

# Select top scoring cells
threshold = adata.obs["my_signature"].quantile(0.999)  # top 0.1%
adata.obs["query_cells"] = adata.obs["my_signature"] >= threshold

# Search via centroid
centroid_emb, nn_idxs, nn_dists, metadata, qc_stats = \
    cq.search_centroid_nearest(adata, "query_cells")
```

### 5. Result Interpretation
```python
# Filter self-referencing results (ALWAYS DO THIS)
query_study_id = "YOUR_STUDY_ID"
filtered = metadata[metadata.study != query_study_id]

# Calculate disease/tissue distributions
disease_props = filtered.disease.value_counts() / len(filtered) * 100

# Compare to background (optional but recommended)
ref_metadata = cq.cell_metadata  # all 23M cells metadata
predicted_celltype = "myofibroblast cell"  # example
background = ref_metadata[ref_metadata.prediction == predicted_celltype]
background_props = background.disease.value_counts() / len(background) * 100

# Enrichment shows true signal vs. reference imbalance
```

### 6. Deriving Gene Signatures (Advanced)
```python
from scimilarity import Interpreter

# Define positive (query) and negative (control) sets
pos = adata[adata.obs["query_cells"]]
neg = adata[~adata.obs["query_cells"]].copy()

# Subsample negative set to match positive size
neg = sc.pp.subsample(neg, n_obs=len(pos), copy=True)

# Compute attribution scores
explainer = Interpreter(cq.model, cq.gene_order)
attrs = explainer.get_attributions(pos.X, neg.X)
attrs_df = explainer.get_ranked_genes(attrs)

# Top genes define signature
# attrs_df is sorted by attribution score
# Use top N genes as refined signature
```

## Census Workflow

### System Requirements
- **Memory**: API-based, no local memory limits
- **Platform**: All platforms (10x, Smart-seq, etc.)
- **Species**: Human, mouse, cross-species with TranscriptFormer
- **Network**: API calls require internet

### 1. Installation & Setup
```python
pip install cellxgene-census scvi-tools

import cellxgene_census
from cellxgene_census import experimental as cxgexp

# Lock Census version for reproducibility
CENSUS_VERSION = "2025-01-30"
census = cellxgene_census.open_soma(census_version=CENSUS_VERSION)
```

### 2. Filter for Relevant Query Cells
```python
# Query Census directly with metadata filters
# CRITICAL: Use is_primary_data==True to avoid duplicates
query_filter = (
    "tissue_general == 'lung' and "
    "disease == 'idiopathic pulmonary fibrosis' and "
    "cell_type == 'myofibroblast cell' and "
    "is_primary_data == True"
)

# Get cell metadata to check what's available
obs_df = cellxgene_census.get_obs(
    census,
    "homo_sapiens",
    value_filter=query_filter,
    column_names=["soma_joinid", "cell_type", "tissue", "disease"]
)

print(f"Found {len(obs_df)} cells matching criteria")
```

### 3. Embed Query Data with scVI Model

**Download scVI model first** (organism-specific, one-time):
```python
# Get model metadata
scvi_info = cxgexp.get_embedding_metadata_by_name(
    "scvi", "homo_sapiens", CENSUS_VERSION
)

# Model location (update for Census version)
# https://cellxgene-contrib-public.s3.us-west-2.amazonaws.com/models/scvi/{CENSUS_VERSION}/homo_sapiens/model.pt
# Download to local directory, e.g., scvi-human-2025-01-30/
```

**Project query data into scVI space**:
```python
import scvi

# Prepare query data for scVI model
scvi.model.SCVI.prepare_query_anndata(
    adata_query, 
    f"scvi-human-{CENSUS_VERSION}"
)

# Load model and embed (no retraining)
vae_q = scvi.model.SCVI.load_query_data(
    adata_query, 
    f"scvi-human-{CENSUS_VERSION}"
)
vae_q.is_trained = True  # Enable forward pass only

# Get embeddings
adata_query.obsm["scvi"] = vae_q.get_latent_representation()
```

### 4. Vector Search via Census API
```python
# Find k nearest neighbors in Census
neighbors = cxgexp.find_nearest_obs(
    embedding_name="scvi",
    organism="homo_sapiens", 
    census_version=CENSUS_VERSION,
    query=adata_query,  # AnnData with .obsm["scvi"]
    k=50,  # neighbors per query cell
    memory_GiB=8,  # adjust based on available memory
    nprobe=20  # search accuracy (higher = more accurate but slower)
)

# Returns: NeighborObs with .distances and .neighbor_ids
# neighbor_ids are Census soma_joinids
```

### 5. Predict Cell Metadata
```python
# Predict tissue, cell type, etc. from neighbors
predictions = cxgexp.predict_obs_metadata(
    organism="homo_sapiens",
    census_version=CENSUS_VERSION,
    neighbors=neighbors,
    attributes=["tissue_general", "cell_type", "disease"]
)

# Returns DataFrame with predictions + confidence scores
# predictions["cell_type_confidence"] indicates certainty

# Add to query AnnData
adata_query.obs["predicted_cell_type"] = predictions["cell_type"]
adata_query.obs["confidence"] = predictions["cell_type_confidence"]
```

### 6. Fetch Neighbor Data for Analysis
```python
# Get AnnData for nearest neighbors
with cellxgene_census.open_soma(census_version=CENSUS_VERSION) as census:
    neighbors_adata = cellxgene_census.get_anndata(
        census,
        "homo_sapiens",
        "RNA",
        obs_coords=sorted(neighbors.neighbor_ids[:, 0].tolist()),
        obs_embeddings=["scvi"],
        X_name="normalized",
        column_names={
            "obs": ["soma_joinid", "tissue", "cell_type", "disease"]
        }
    )

# Combine query + neighbors for joint visualization
combined = anndata.concat([adata_query, neighbors_adata])
sc.pp.neighbors(combined, use_rep="scvi")
sc.tl.umap(combined)
```

## Key Differences Summary

| Aspect | SCimilarity | Census |
|--------|-------------|---------|
| **Data scope** | 23M human cells | 100M+ cells (mouse/human) |
| **Platform** | 10x Chromium only | All platforms |
| **Species** | Human only | Mouse, human, cross-species |
| **Deployment** | Local model (64GB RAM) | API-based (remote) |
| **Preprocessing** | Strict (align + lognorm) | Handled by scVI |
| **QC metrics** | query_coherence | confidence scores |
| **Best for** | Disease/condition search | Label transfer, cross-species |

## Critical Considerations

### SCimilarity-Specific
1. **Gene Alignment is Mandatory**: Use `align_dataset(adata, cq.gene_order)`
2. **Normalization Must Match**: Use `lognorm_counts(adata)` - nothing else
3. **Centroid Quality**: ALWAYS check `query_coherence` - don't trust < 20
4. **Coherent Queries**: Tight clusters → good results; scattered cells → poor
5. **Filter Self-References**: Query study always appears in top hits
6. **Memory**: 64GB minimum, crashes if insufficient

### Census-Specific
1. **Lock Census Version**: Always specify `census_version` for reproducibility
2. **Filter Duplicates**: Use `is_primary_data == True` in queries
3. **Download Models**: scVI models are organism + version specific
4. **Network Required**: API calls need active internet connection
5. **Confidence Scores**: Low confidence predictions need manual review
6. **Rate Limits**: API may throttle large queries

## Visualization Patterns

### SCimilarity Results
```python
# Disease/tissue proportions
props = filtered_metadata.disease.value_counts() / len(filtered_metadata) * 100
ax = props.plot(kind='barh', xlabel='percent of cells')
ax.set_xticklabels([f"{int(x)}%" for x in ax.get_xticks()])
```

### Census Results
```python
# UMAP colored by dataset origin
combined.obs["origin"] = ["query" if ... else "census"]
sc.pl.umap(combined, color=["origin", "tissue_general"])

# Confidence distribution
import seaborn as sns
sns.histplot(predictions["cell_type_confidence"], bins=50)
```

## Common Pitfalls

### SCimilarity
- ❌ **Using non-10x data** → Model trained on 10x only
- ❌ **Custom normalization** → Must use `lognorm_counts()`
- ❌ **Skipping gene alignment** → Results will be meaningless
- ❌ **Ignoring query_coherence** → Low scores = unreliable results
- ❌ **Scattered query cells** → Centroid of noise is noise
- ❌ **Not filtering self-study** → Inflated similarity to own data

### Census
- ❌ **Not locking version** → Results change between releases
- ❌ **Including duplicates** → Use `is_primary_data == True`
- ❌ **Wrong model version** → Match Census version to model version
- ❌ **Low nprobe value** → Faster but less accurate search (use ≥20)
- ❌ **Trusting low confidence** → Manually review predictions <0.5
- ❌ **Mixing species** → Use TranscriptFormer for cross-species

## Workflow Decision Tree

```
START: I have scRNA-seq data and want to find similar cells
│
├─ Is data 10x Chromium + human only?
│  ├─ YES: Do I have 64GB+ RAM?
│  │  ├─ YES → Use SCimilarity (better disease context search)
│  │  └─ NO → Use Census (API-based)
│  └─ NO (mouse, Smart-seq, etc.) → Use Census (only option)
│
├─ Do I need cross-species comparison?
│  └─ YES → Use Census TranscriptFormer
│
└─ Do I need quality metrics for search coherence?
   └─ YES → Use SCimilarity (has query_coherence)
```

## File Organization
```
/home/claude/           # Working directory
  query_data.h5ad       # Your preprocessed data
  /models/              # SCimilarity models (if using)
    model_v1.1/         # Downloaded from Zenodo
  /scvi-models/         # Census scVI models (if using)
    scvi-human-2025-01-30/
    scvi-mouse-2025-01-30/
  /results/             # Output analyses
    scimilarity/        # SCimilarity search results
    census/             # Census search results
/mnt/user-data/outputs/ # Final reports/plots for user
```

## Advanced Use Cases

### Deriving Cell-State Signatures (SCimilarity)
- Compare query population vs. control using `Interpreter`
- Returns attribution scores for all genes
- Use top genes as refined signature

### Label Transfer (Census)
- Embed query with scVI
- Find k=30-50 neighbors
- Vote on cell type from neighbors
- Check confidence scores

### Cross-Species Alignment (Census)
- Use TranscriptFormer embeddings
- Query both human and mouse
- Compare evolutionary conservation

### In Vitro vs. In Vivo (SCimilarity)
- Filter reference by `in_vivo` metadata field
- Compare similarity scores between conditions
- Identify most similar in vivo cells to in vitro state

## Citation Information

**SCimilarity**: Kellogg et al., bioRxiv (check for publication)
**Census**: CELLxGENE Census documentation at https://chanzuckerberg.github.io/cellxgene-census/

**Generate citations for Census data**:
```python
# Get dataset table
datasets = census["census_info"]["datasets"].read().concat().to_pandas()

# For your query results
slice_datasets = datasets[datasets["dataset_id"].isin(your_query_dataset_ids)]
print(*set(slice_datasets["citation"]), sep="\n\n")
```

---

## When not to use

- Do not use SCimilarity for mouse or non-10x data — it is human 10x Chromium only.
- Do not skip the required lognorm_counts / align_dataset preprocessing — SCimilarity breaks without training-matched normalization.

---

## See also

- `cellxgene-census-annotation`
- `scvi-scanvi`
- `treearches-hierarchy-learning`

Upstream docs: https://genentech.github.io/scimilarity/

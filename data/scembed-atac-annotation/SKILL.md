---
name: scembed-atac-annotation
description: "scEmbed transfers cell-type labels to scATAC queries using pre-trained region2vec embeddings and KNN search in a vector database, with no retraining. Use for fast annotation when a matching HuggingFace databio reference model exists and you want EV-projection into the reference UMAP. For scRNA-informed ATAC annotation use scvi-multivi."
license: MIT
---

# scEmbed - Transfer Learning for scATAC-seq Cell-Type Annotation

## Purpose
scEmbed enables fast cell-type annotation using pre-trained reference models and vector databases. Unlike supervised methods, it transfers knowledge through region co-occurrence patterns, requiring no model retraining—just KNN search in embedding space.

## Integration

**Upstream**: Requires binary accessibility matrix (from SnapATAC, ArchR, or Signac)
**Downstream**: Embeddings in `adata.obsm` compatible with scanpy UMAP/clustering
**Reference models**: HuggingFace `databio/*` collection (craft100k, luecken2021)
**Vector DBs**: Qdrant for fast KNN (can substitute ChromaDB, FAISS)

## Critical Principle: Model Consistency
**MANDATORY**: Query embeddings MUST use the identical pre-trained model as the reference database. Mismatched models break the shared embedding space and produce garbage annotations.

## Core Architecture Difference
**Critical concept**: scEmbed embeds *regions first*, then averages region vectors to create cell embeddings. This enables transfer learning through region overlap analysis, not typical neural network fine-tuning.

## Three Projection Workflows

**No Projection**: Train new model on query data, fit new UMAP
- Use when: No suitable reference exists

**E-Projection**: Use reference region embeddings, fit new UMAP on query
- Use when: Want reference knowledge but separate visualization

**EV-Projection**: Use reference embeddings AND reference UMAP topology
- Use when: Annotating query cells by placing them in reference space
- **Critical for cell-type annotation**: Query cells appear in same UMAP as reference, enabling label transfer

## Essential Workflow

```python
from geniml.scembed import ScEmbed
from gtars.tokenizers import Tokenizer

# 1. Load pre-trained model (HuggingFace: databio/*)
model = ScEmbed("databio/r2v-luecken2021-hg38-v2")

# 2. Tokenize: requires adata.var with 'chr', 'start', 'end'
tokenizer = Tokenizer.from_pretrained("databio/atacformer-base-hg38")
tokens = tokenize_anndata(adata, tokenizer)

# 3. Encode: returns cell embeddings (averaged region vectors)
embeddings = model.encode(adata)  # or model.encode_tokenized_cells(tokens)
adata.obsm['X_scembed'] = embeddings
```

## Critical Parameters

**Fragment QC thresholds** (before encoding):
- `min_fragments=200`: Remove empty droplets
- `max_fragments=10000`: Remove doublets
- Adjust based on library depth

**Projection mapping**:
- Query regions mapped to reference via `bedtools intersect` logic
- Unmapped regions ignored (not error)
- **Model consistency**: Query must use same pre-trained model as reference database

## Cell-Type Annotation Pattern

```python
# 1. Reference: Encode + store in vector DB
client.create_collection("ref", vectors_config=VectorParams(
    size=embeddings.shape[1], distance=Distance.DOT))
points = [PointStruct(id=i, vector=emb.tolist(), 
                      payload={"cell_type": label}) 
          for i, (emb, label) in enumerate(zip(embeddings, labels))]
client.upsert("ref", points)

# 2. Query: Encode with SAME model, KNN search
query_embeddings = model.encode(query_adata)
for emb in query_embeddings:
    neighbors = client.search("ref", query_vector=emb.tolist(), 
                             limit=5, with_payload=True)
    predicted_type = Counter([n.payload["cell_type"] 
                             for n in neighbors]).most_common(1)[0][0]
```

## Domain Context

**Why region embeddings work**: Co-accessible regions share regulatory context. Averaging their vectors captures cell state without modeling all pairwise region interactions.

**Transfer learning advantage**: Reference models trained on 100K+ cells (e.g., Luecken2021) capture robust co-accessibility patterns reusable on smaller query datasets.

**Speed**: No model training for queries—only overlap analysis + vector averaging. Annotate 5K cells in seconds vs. hours for supervised methods.

## Common Pitfalls

**Missing `.var` columns**: scEmbed needs `chr`, `start`, `end` in `adata.var`
- Fix: Parse from region names like "chr1_1000_2000"

**Model mismatch in projection**: Using different models for reference vs. query breaks the shared embedding space
- Fix: Always use same HuggingFace model path

**Over-clustering before annotation**: Leiden/Louvain before KNN search inflates cluster count
- Fix: KNN search on all cells, then assign cluster-level consensus labels

**Vector DB payload errors**: Forgetting cell-type labels in payload
- Fix: Always include `payload={"cell_type": ...}` in PointStruct

---

**Installation**: 
```bash
pip install geniml gtars qdrant-client
# Place in: /mnt/skills/user/scembed.md
```

**Test**: 
```bash
# Load fragments → tokenize → encode → UMAP in <2 min
python -c "from geniml.scembed import ScEmbed; print('Ready')"
```

**Token count**: ~580 tokens

---

## Cell-Type Annotation Workflow

### Step 1: Build Reference Database (Once per reference)

```python
from geniml.scembed import ScEmbed
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

# Load reference data with cell-type labels
ref_adata = sc.read_h5ad("reference.h5ad")

# Generate embeddings with specific model
model = ScEmbed("databio/r2v-luecken2021-hg38-v2")
embeddings = model.encode(ref_adata)

# Create vector database
client = QdrantClient("localhost", port=6333)
client.create_collection(
    collection_name="luecken2021",
    vectors_config=VectorParams(size=embeddings.shape[1], distance=Distance.DOT)
)

# Upsert with cell-type labels in payload
points = [
    PointStruct(
        id=ref_adata.obs.index[i],
        vector=embeddings[i].tolist(),
        payload={"cell_type": ref_adata.obs['cell_type'][i]}
    )
    for i in range(len(embeddings))
]
client.upsert(collection_name="luecken2021", points=points, wait=True)
```

### Step 2: Annotate Query Cells (Fast, No Training)

```python
from collections import Counter
import numpy as np

# Load unlabeled query data
query_adata = sc.read_h5ad("unlabeled_query.h5ad")

# CRITICAL: Use SAME model as reference database
model = ScEmbed("databio/r2v-luecken2021-hg38-v2")  # Must match!
query_embeddings = model.encode(query_adata)
query_adata.obsm['scembed_X'] = np.array(query_embeddings)

# KNN search + majority vote
client = QdrantClient("localhost", port=6333)
k = 5  # Hyperparameter: number of neighbors

annotations = []
for i, embedding in enumerate(query_embeddings):
    neighbors = client.search(
        collection_name="luecken2021",
        query_vector=embedding.tolist(),
        limit=k,
        with_payload=True
    )
    
    # Extract cell types from neighbors
    cell_types = [neighbor.payload["cell_type"] for neighbor in neighbors]
    
    # Majority vote
    predicted_type = Counter(cell_types).most_common(1)[0][0]
    annotations.append(predicted_type)

query_adata.obs['predicted_cell_type'] = annotations
```

### Step 3 (Optional): Cluster-Level Consensus

```python
# Improves speed + reduces noise from singleton cells
import scanpy as sc

# Cluster query cells first
sc.pp.neighbors(query_adata, use_rep='scembed_X')
sc.tl.leiden(query_adata, resolution=0.5)

# Annotate cluster centroids instead of individual cells
for cluster in query_adata.obs['leiden'].unique():
    cluster_mask = query_adata.obs['leiden'] == cluster
    cluster_embeddings = query_adata.obsm['scembed_X'][cluster_mask]
    
    # Use centroid for KNN search
    centroid = cluster_embeddings.mean(axis=0)
    neighbors = client.search(
        collection_name="luecken2021",
        query_vector=centroid.tolist(),
        limit=10,  # More neighbors for centroid
        with_payload=True
    )
    
    # Assign cluster label
    cluster_type = Counter([n.payload["cell_type"] 
                           for n in neighbors]).most_common(1)[0][0]
    query_adata.obs.loc[cluster_mask, 'cluster_cell_type'] = cluster_type
```

## Available Pre-Trained Models (HuggingFace databio/*)

### Human scATAC-seq Models
- **`r2v-luecken2021-hg38-v2`**: Human bone marrow, 120K cells, 10 donors (multiome benchmark)
- **`r2v-ChIP-atlas-hg38-v2`**: Trained on ChIP-seq atlas (regulatory landscape)
- **`r2v-10x-pbmc-5k-hg19`**: PBMC reference (5K cells, hg19)
- **`atacformer-craft100k-hg38`**: CRAFT atlas (100K cells, blood)
- **`atacformer-base-hg38`**: General-purpose human model

### Mouse Models
- **`r2v-mouse-atlas-mm9-v2`**: Mouse atlas (mm9 assembly)

### Model Selection Criteria
- **Tissue match**: Use luecken2021 for bone marrow/blood, mouse-atlas for mouse
- **Assembly match**: hg38 vs hg19 (liftOver if mismatched)
- **atacformer-* vs r2v-***: Both work; atacformer uses transformer architecture, r2v uses Word2Vec

## Critical Parameters

**`k` (KNN neighbors)**: 
- k=5-10 for individual cells
- k=10-20 for cluster centroids
- Higher k = smoother but less specific labels

**Distance metric**: 
- `Distance.DOT` (default, works for normalized embeddings)
- `Distance.COSINE` if embeddings not normalized

**Qdrant setup**: 
- Local: `QdrantClient("localhost", port=6333)`
- Requires `docker run -p 6333:6333 qdrant/qdrant` or installed binary

## Common Pitfalls

**Model mismatch**: Query uses different model than reference
- Symptom: Random/nonsense predictions
- Fix: Check `model = ScEmbed("databio/...")` matches exactly

**Missing `.var` columns**: scEmbed needs `chr`, `start`, `end` in `adata.var`
- Fix: Parse from region names before calling `model.encode()`

**Payload missing labels**: Forgot `payload={"cell_type": ...}` in reference upsert
- Symptom: KeyError during neighbor search
- Fix: Re-upsert reference with labels in payload

**Assembly mismatch**: Query (hg38) vs reference model (hg19)
- Fix: Use matching model or liftOver regions before encoding

## Domain Context

**Why this works**: Cells with similar chromatin accessibility cluster in embedding space. KNN borrows labels from nearest reference cells.

**Speed advantage**: No neural network training—annotation is pure vector search. 5K cells in <30 seconds on laptop.

**Specificity trade-off**: Labels limited to reference cell types. Novel cell types assigned to nearest known type (use confidence scores from neighbor consensus to flag ambiguous cells).

## Integration

**Upstream**: Requires `AnnData` with binary accessibility matrix + `.var['chr','start','end']`
**Downstream**: Predictions in `.obs['predicted_cell_type']` compatible with scanpy plotting
**Vector DB alternatives**: ChromaDB, FAISS, or simple sklearn NearestNeighbors (slower for large reference)

---

**Installation**: 
```bash
pip install geniml gtars qdrant-client scanpy
docker run -d -p 6333:6333 qdrant/qdrant  # Start Qdrant
# Place in: /mnt/skills/user/scembed.md
```

**Test**: 
```bash
python -c "from geniml.scembed import ScEmbed; from qdrant_client import QdrantClient; print('Ready')"
```

---

## When not to use

- Do not mix reference and query embeddings from different pre-trained models — shared embedding space is required or annotations will be garbage.
- Do not use for scRNA-informed annotation of multiome. Use scvi-multivi or label transfer via the RNA modality.

---

## See also

- `scvi-scarches-reference-mapping`
- `scvi-peakvi`
- `iterative-peak-merging`
- `single-cell-vector-search`

Upstream docs: https://github.com/databio/geniml

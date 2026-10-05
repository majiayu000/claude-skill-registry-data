---
name: scglue-unpaired-multiomics-integration
description: "Integrates unpaired single-cell multi-omics (scRNA + scATAC, no shared barcodes) using a prior-knowledge guidance graph linking genes to regulatory regions. Use when aligning separately-assayed RNA and ATAC experiments, inferring cis-regulatory links, or building cross-modality TF-target networks. For paired multiome use scvi-multivi."
license: MIT
---

# scGLUE (Graph Linked Unified Embedding) Skill

## Overview

scGLUE integrates unpaired single-cell multi-omics data (scRNA-seq, scATAC-seq, etc.) using a guidance graph that encodes prior regulatory knowledge. Unlike paired integration methods, scGLUE can align cells from different experiments with no barcode overlap.

**Key Features:**
- Unpaired and partially paired multi-omics integration
- Feature embeddings for regulatory inference
- Cis-regulatory region identification
- TF-target gene network construction
- Guidance graph-based alignment using prior knowledge

## Installation

```bash
# Create venv and install (NEVER use conda for scglue)
python -m venv scglue_env
source scglue_env/bin/activate
pip install scglue

# Optional: faiss for faster metacell clustering
pip install faiss-cpu  # or faiss-gpu if CUDA available

# For regulatory inference (pySCENIC)
pip install pyscenic pyarrow cytoolz
```

**Documentation:** https://scglue.readthedocs.io/

---

## Stage 1: Data Preprocessing

### 1.1 Read Data

```python
import anndata as ad
import networkx as nx
import scanpy as sc
import scglue
from matplotlib import rcParams

scglue.plot.set_publication_params()
rcParams["figure.figsize"] = (4, 4)

# Load AnnData objects
rna = ad.read_h5ad("rna_data.h5ad")
atac = ad.read_h5ad("atac_data.h5ad")
```

### 1.2 Preprocess scRNA-seq

```python
# CRITICAL: Back up raw counts FIRST (needed for model training)
rna.layers["counts"] = rna.X.copy()

# Select highly variable genes (Seurat v3 method recommended)
sc.pp.highly_variable_genes(rna, n_top_genes=2000, flavor="seurat_v3")
# For real analyses, consider 4000-6000 genes

# Standard preprocessing
sc.pp.normalize_total(rna)
sc.pp.log1p(rna)
sc.pp.scale(rna)

# PCA for encoder (100 components)
sc.tl.pca(rna, n_comps=100, svd_solver="auto")

# Optional: Visualize RNA domain
sc.pp.neighbors(rna, metric="cosine")
sc.tl.umap(rna)
sc.pl.umap(rna, color="cell_type")
```

### 1.3 Preprocess scATAC-seq

```python
# CRITICAL: Use LSI (TF-IDF + SVD), NOT standard PCA
# n_iter=15 increases precision of randomized SVD
scglue.data.lsi(atac, n_components=100, n_iter=15)

# Optional: Visualize ATAC domain
sc.pp.neighbors(atac, use_rep="X_lsi", metric="cosine")
sc.tl.umap(atac)
sc.pl.umap(atac, color="cell_type")
```

### 1.4 Prepare Genomic Coordinates

**For RNA (genes):**
```python
# Check if coordinates exist
rna.var.head()  # Look for chrom, chromStart, chromEnd

# If missing, annotate from GTF file
# Column names MUST be: chrom, chromStart, chromEnd (BED format)
scglue.data.get_gene_annotation(
    rna,
    gtf="gencode.vM25.chr_patch_hapl_scaff.annotation.gtf.gz",  # mm10
    # gtf="gencode.v38.annotation.gtf.gz",  # hg38
    gtf_by="gene_name"  # or "gene_id" if var_names are Ensembl IDs
)

# Verify
rna.var.loc[:, ["chrom", "chromStart", "chromEnd"]].head()
```

**For ATAC (peaks):**
```python
# If var_names are formatted as "chr1:3005833-3005982"
split = atac.var_names.str.split(r"[:-]")
atac.var["chrom"] = split.map(lambda x: x[0])
atac.var["chromStart"] = split.map(lambda x: x[1]).astype(int)
atac.var["chromEnd"] = split.map(lambda x: x[2]).astype(int)

atac.var.head()
```

---

## Stage 2: Graph Construction

### 2.1 RNA-Anchored Guidance Graph (Standard)

```python
# Default: peaks connected to genes if overlapping gene body OR promoter
guidance = scglue.genomics.rna_anchored_guidance_graph(rna, atac)

# Verify graph validity
scglue.graph.check_graph(guidance, [rna, atac])
# Output: All checks passed!

# HVG propagation: peaks reachable from HV genes are marked highly_variable
atac.var["highly_variable"].sum()  # Check how many peaks selected
```

### 2.2 Extended Guidance Graph (Recommended for Real Analyses)

```python
# For better regulatory inference, extend genomic range to 150kb around TSS
# with distance-decaying weights

# Option 1: Custom window graph with distance decay
from scglue.genomics import window_graph, Bed

# Get TSS positions
tss_bed = Bed(rna.var).strand_specific_start_site()

# Window graph: connect peaks within 150kb of TSS
peak_bed = Bed(atac.var)
tss2peak = window_graph(
    tss_bed.expand(150000, 150000),  # 150kb upstream/downstream
    peak_bed,
    window_size=0,  # 0 = require overlap with expanded region
    attr_fn=lambda x, y: {  # Distance-decaying weight
        "weight": 1.0 / (1 + abs((x["chromStart"] + x["chromEnd"]) / 2 -
                                  (y["chromStart"] + y["chromEnd"]) / 2) / 10000),
        "sign": 1
    }
)

# Option 2: Incorporate Hi-C, eQTL data
# Build separate graphs and compose them
from scglue.graph import compose_multigraph

# See scGLUE case study for detailed Hi-C/eQTL integration
```

### 2.3 Custom Graph for Non-Standard Modalities

**Example: RNA + ADT (CITE-seq style, unpaired)**
```python
import pandas as pd

# For ADT, connect protein to its encoding gene
# Rename proteins to match gene names where applicable
rename_proteins = {
    "CD103": "ITGAE", "CD11b": "ITGAM", "CD11c": "ITGAX",
    "CD8": "CD8A", "HLA-DR": "HLA-DRA", # etc.
}
adt.var_names = [rename_proteins.get(n, n) for n in adt.var_names]

# Create adjacency matrix
p = np.array(adt.var_names)
r = np.array(rna.var_names)
mask = np.repeat(p.reshape(-1, 1), r.shape[0], axis=1) == r

# Differentiate feature names across modalities
rna.var_names = [v + "_rna" for v in rna.var_names]
adt.var_names = [v + "_prot" for v in adt.var_names]

# Build graph
adj = pd.DataFrame(mask, index=adt.var_names, columns=rna.var_names)
diag_edges = adj[adj > 0].stack().index.tolist()
edges = [(n1, n2, {"weight": 1.0, "sign": 1}) for n1, n2 in diag_edges]

# Add self-loops (REQUIRED)
self_loops_rna = [(g, g, {"weight": 1.0, "sign": 1}) for g in rna.var_names]
self_loops_prot = [(g, g, {"weight": 1.0, "sign": 1}) for g in adt.var_names]

graph = nx.Graph()
graph.add_nodes_from(rna.var_names)
graph.add_nodes_from(adt.var_names)
graph.add_edges_from(edges)
graph.add_edges_from(self_loops_rna)
graph.add_edges_from(self_loops_prot)

# Verify
scglue.graph.check_graph(graph, [rna, adt])
```

### 2.4 Graph Requirements Checklist

All guidance graphs MUST satisfy:
1. **Node coverage:** All omics features in datasets must be graph nodes
2. **Edge weights:** Range (0, 1], stored as "weight" attribute
3. **Edge signs:** Value 1 or -1, stored as "sign" attribute
4. **Self-loops:** Every node must have self-loop (weight=1, sign=1)
5. **Symmetry:** Use undirected graphs (Graph, MultiGraph) or symmetric directed

---

## Stage 3: Model Training

### 3.1 Configure Datasets

```python
# For scRNA-seq: Negative binomial distribution, raw counts layer
scglue.models.configure_dataset(
    rna,
    "NB",  # Negative binomial for count data
    use_highly_variable=True,
    use_layer="counts",  # MUST be raw counts
    use_rep="X_pca"  # Encoder uses PCA embedding
)

# For scATAC-seq: Negative binomial, use LSI embedding
scglue.models.configure_dataset(
    atac,
    "NB",  # Also NB for ATAC count data
    use_highly_variable=True,  # Uses HV peaks from graph propagation
    use_rep="X_lsi"  # Encoder uses LSI embedding
)

# Optional: Batch correction
scglue.models.configure_dataset(
    rna, "NB",
    use_highly_variable=True,
    use_layer="counts",
    use_rep="X_pca",
    use_batch="batch"  # obs column for batch correction
)

# Optional: Cell type supervision
scglue.models.configure_dataset(
    rna, "NB",
    use_highly_variable=True,
    use_layer="counts",
    use_rep="X_pca",
    use_cell_type="cell_type"  # obs column for supervision
)
```

### 3.2 Extract HVF Subgraph

```python
from itertools import chain

# Only train on highly variable features
guidance_hvf = guidance.subgraph(chain(
    rna.var.query("highly_variable").index,
    atac.var.query("highly_variable").index
)).copy()

print(f"HVF graph: {guidance_hvf.number_of_nodes()} nodes, "
      f"{guidance_hvf.number_of_edges()} edges")
```

### 3.3 Train GLUE Model (Unpaired Data)

```python
# Train GLUE model
# Domains specified as dict with custom names
glue = scglue.models.fit_SCGLUE(
    {"rna": rna, "atac": atac},  # Domain dict
    guidance_hvf,
    fit_kws={"directory": "glue"}  # Save checkpoints/logs
)

# Training has two phases:
# 1. Pretraining: Basic VAE training
# 2. Fine-tuning: With alignment loss after estimating balancing weights

# Monitor with tensorboard:
# tensorboard --logdir=glue
```

### 3.4 Train GLUE Model (Partially Paired Data)

```python
# For paired cells: use IDENTICAL obs_names across modalities
# For unpaired cells: use DIFFERENT obs_names

# Example: De-anonymize 3000 paired cells
paired_cells = set(Random(0).sample(set(cell_barcodes), 3000))
rna.obs_names = [bc if bc in paired_cells else f"{bc}_RNA" for bc in rna_barcodes]
atac.obs_names = [bc if bc in paired_cells else f"{bc}_ATAC" for bc in atac_barcodes]

# Configure with obs_names usage
scglue.models.configure_dataset(
    rna, "NB",
    use_highly_variable=True,
    use_layer="counts",
    use_rep="X_pca",
    use_obs_names=True  # CRITICAL: Enable pairing detection
)
scglue.models.configure_dataset(
    atac, "NB",
    use_highly_variable=True,
    use_rep="X_lsi",
    use_obs_names=True  # CRITICAL: Enable pairing detection
)

# Train with PairedSCGLUEModel
glue = scglue.models.fit_SCGLUE(
    {"rna": rna, "atac": atac},
    guidance_hvf,
    model=scglue.models.PairedSCGLUEModel,  # Use paired model
    fit_kws={"directory": "glue"}
)
```

### 3.5 Save and Load Model

```python
# Save trained model
glue.save("glue.dill")

# Load model
glue = scglue.models.load_model("glue.dill")
```

---

## Stage 4: Integration Diagnostics

### 4.1 Check Integration Consistency

```python
# Compute integration consistency score
dx = scglue.models.integration_consistency(
    glue,
    {"rna": rna, "atac": atac},
    guidance_hvf
)
print(dx)
#   n_meta  consistency
# 0     10     0.191
# 1     20     0.158
# 2     50     0.114
# 3    100     0.087
# 4    200     0.067

# Visualize: curve should be ABOVE 0.05 line
import seaborn as sns
sns.lineplot(x="n_meta", y="consistency", data=dx)
plt.axhline(y=0.05, c="darkred", ls="--")
plt.xlabel("Number of metacells")
plt.ylabel("Integration consistency")
plt.title("Integration Quality Check")
```

**Interpretation:**
- Higher curve = more confident integration
- Empirically reliable if curve stays above 0.05
- Lower values may indicate: incompatible modalities, poor graph, or insufficient data

---

## Stage 5: Extract Embeddings

### 5.1 Cell Embeddings

```python
# Get cell embeddings for each modality
rna.obsm["X_glue"] = glue.encode_data("rna", rna)
atac.obsm["X_glue"] = glue.encode_data("atac", atac)

# Combine for joint visualization
combined = ad.concat([rna, atac])

sc.pp.neighbors(combined, use_rep="X_glue", metric="cosine")
sc.tl.umap(combined)
sc.pl.umap(combined, color=["cell_type", "domain"], wspace=0.65)
```

### 5.2 Feature Embeddings (Unique to scGLUE!)

```python
# Get feature embeddings from guidance graph
feature_embeddings = glue.encode_graph(guidance_hvf)
feature_embeddings = pd.DataFrame(feature_embeddings, index=glue.vertices)

# Store in varm slots
rna.varm["X_glue"] = feature_embeddings.reindex(rna.var_names).to_numpy()
atac.varm["X_glue"] = feature_embeddings.reindex(atac.var_names).to_numpy()

# Feature embeddings capture regulatory relationships!
# Use for downstream regulatory inference
```

### 5.3 Save Results

```python
rna.write("rna-emb.h5ad", compression="gzip")
atac.write("atac-emb.h5ad", compression="gzip")
nx.write_graphml(guidance_hvf, "guidance-hvf.graphml.gz")
```

---

## Stage 6: Regulatory Inference

### 6.1 Cis-Regulatory Inference

```python
import numpy as np
import pandas as pd

# Prepare feature data
genes = rna.var.query("highly_variable").index
peaks = atac.var.query("highly_variable").index

features = pd.Index(np.concatenate([rna.var_names, atac.var_names]))
feature_embeddings = np.concatenate([rna.varm["X_glue"], atac.varm["X_glue"]])

# Extract skeleton graph (limits search space, reduces false positives)
skeleton = guidance_hvf.edge_subgraph(
    e for e, attr in dict(guidance_hvf.edges).items()
    if attr.get("type") == "fwd"  # Only gene→peak direction
).copy()

# Infer regulatory connections
# Scores = cosine similarity between feature embeddings
reginf = scglue.genomics.regulatory_inference(
    features,
    feature_embeddings,
    skeleton=skeleton,
    random_state=0
)

# Filter significant connections (q-value < 0.05)
gene2peak = reginf.edge_subgraph(
    e for e, attr in dict(reginf.edges).items()
    if attr["qval"] < 0.05
)

print(f"Significant gene-peak connections: {gene2peak.number_of_edges()}")
```

### 6.2 Visualize with pyGenomeTracks

```python
# Save peak bed and gene-peak links
scglue.genomics.Bed(atac.var).write_bed("peaks.bed", ncols=3)
scglue.genomics.write_links(
    gene2peak,
    scglue.genomics.Bed(rna.var).strand_specific_start_site(),
    scglue.genomics.Bed(atac.var),
    "gene2peak.links",
    keep_attrs=["score"]
)

# Create tracks.ini config file
# Then run: pyGenomeTracks --tracks tracks.ini --region chr1:1000000-2000000 -o plot.png
```

### 6.3 Build TF-Target Gene Network

```python
# Load TF motif data (JASPAR)
# Download from: http://download.gao-lab.org/GLUE/cisreg/
motif_bed = scglue.genomics.read_bed("JASPAR2022-mm10.bed.gz")

# Get TFs covered in both RNA data and motif data
tfs = pd.Index(motif_bed["name"]).intersection(rna.var_names)
print(f"TFs available: {len(tfs)}")

# Step 1: Draft coexpression network with GRNBoost2
# Save RNA data as loom for pySCENIC
rna[:, np.union1d(genes, tfs)].write_loom("rna.loom")
np.savetxt("tfs.txt", tfs, fmt="%s")

# Run pySCENIC GRN (command line)
# pyscenic grn rna.loom tfs.txt -o draft_grn.csv --seed 0 --num_workers 20

# Step 2: Generate TF cis-regulatory ranking
peak_bed = scglue.genomics.Bed(atac.var.loc[peaks])
peak2tf = scglue.genomics.window_graph(peak_bed, motif_bed, 0, right_sorted=True)
peak2tf = peak2tf.edge_subgraph(e for e in peak2tf.edges if e[1] in tfs)

# Combine gene→peak and peak→TF via scGLUE
gene2tf_rank_glue = scglue.genomics.cis_regulatory_ranking(
    gene2peak, peak2tf, genes, peaks, tfs,
    region_lens=atac.var.loc[peaks, "chromEnd"] - atac.var.loc[peaks, "chromStart"],
    random_state=0
)

# Optional: Supplementary ranking from proximal promoters
flank_bed = scglue.genomics.Bed(rna.var.loc[genes]).strand_specific_start_site().expand(500, 500)
flank2tf = scglue.genomics.window_graph(flank_bed, motif_bed, 0, right_sorted=True)
gene2flank = nx.Graph([(g, g) for g in genes])
gene2tf_rank_supp = scglue.genomics.cis_regulatory_ranking(
    gene2flank, flank2tf, genes, genes, tfs,
    n_samples=0  # No sampling needed for uniform-length flanks
)

# Step 3: Save rankings for pySCENIC pruning
gene2tf_rank_glue.columns = gene2tf_rank_glue.columns + "_glue"
gene2tf_rank_supp.columns = gene2tf_rank_supp.columns + "_supp"

scglue.genomics.write_scenic_feather(gene2tf_rank_glue, "glue.genes_vs_tracks.rankings.feather")
scglue.genomics.write_scenic_feather(gene2tf_rank_supp, "supp.genes_vs_tracks.rankings.feather")

# Create annotation file
pd.concat([
    pd.DataFrame({"#motif_id": tfs + "_glue", "gene_name": tfs}),
    pd.DataFrame({"#motif_id": tfs + "_supp", "gene_name": tfs})
]).assign(
    motif_similarity_qvalue=0.0,
    orthologous_identity=1.0,
    description="placeholder"
).to_csv("ctx_annotation.tsv", sep="\t", index=False)

# Step 4: Prune with pySCENIC (command line)
# pyscenic ctx draft_grn.csv glue.genes_vs_tracks.rankings.feather supp.genes_vs_tracks.rankings.feather \
#     --annotations_fname ctx_annotation.tsv --expression_mtx_fname rna.loom \
#     --output pruned_grn.csv --rank_threshold 500 --min_genes 1 --num_workers 20

# Step 5: Load final network
grn = scglue.genomics.read_ctx_grn("pruned_grn.csv")

# Or use convenience wrapper
grn = scglue.genomics.build_tf_target_network(
    rna, atac, gene2peak, genes, peaks, tfs, motif_bed
)

# Visualize or export
nx.draw(grn, with_labels=True)
nx.write_graphml(grn, "pruned_grn.graphml.gz")  # For Cytoscape/Gephi
```

---

## Project-Specific: <dc-project> (mm10)

### Recommended Configuration

```python
# For <dc-project> integration with ~200k peaks

# Preprocessing
sc.pp.highly_variable_genes(rna, n_top_genes=4000, flavor="seurat_v3")  # More genes
scglue.data.lsi(atac, n_components=100, n_iter=15)

# Graph construction
scglue.data.get_gene_annotation(
    rna,
    gtf="/path/to/gencode.vM25.chr_patch_hapl_scaff.annotation.gtf.gz",
    gtf_by="gene_name"
)

# Build extended guidance graph (150kb window)
guidance = scglue.genomics.rna_anchored_guidance_graph(
    rna, atac,
    extend_range=150000,  # 150kb extension
    extend_fn=lambda x: 1.0 / (1 + x / 10000)  # Distance decay
)

# Configure for batch correction
scglue.models.configure_dataset(
    rna, "NB",
    use_highly_variable=True,
    use_layer="counts",
    use_rep="X_pca",
    use_batch="sample"  # AS009_1, AS009_2, etc.
)

# TF motif file for mm10
motif_bed = scglue.genomics.read_bed("JASPAR2022-mm10.bed.gz")
```

### Integration with Existing Checkpoints

```python
# Load preprocessed modalities
rna = sc.read_h5ad("path/to/rna_preprocessed.h5ad")
atac = sc.read_h5ad("path/to/atac_preprocessed.h5ad")

# Ensure raw counts available
if "counts" not in rna.layers:
    rna.layers["counts"] = rna.raw.X.copy()
```

---

## Common Pitfalls and Solutions

### Data Preprocessing
| Pitfall | Solution |
|---------|----------|
| Using normalized data for training | Always use `use_layer="counts"` with raw counts |
| Standard PCA for ATAC | Use `scglue.data.lsi()` instead |
| Missing genomic coordinates | Annotate with `scglue.data.get_gene_annotation()` |
| Wrong coordinate column names | Must be: chrom, chromStart, chromEnd |

### Graph Construction
| Pitfall | Solution |
|---------|----------|
| Missing self-loops | Every node needs self-loop (weight=1, sign=1) |
| Asymmetric directed graph | Use undirected Graph or symmetric DiGraph |
| Edge weights outside (0,1] | Normalize weights to valid range |
| No HVG propagation | Run `rna_anchored_guidance_graph` before training |

### Model Training
| Pitfall | Solution |
|---------|----------|
| Wrong distribution | Use "NB" for count data, "Normal" for normalized |
| Insufficient HVGs | Increase to 4000-6000 for real analyses |
| Paired data not detected | Set `use_obs_names=True` and use identical obs_names |
| Poor integration | Check consistency score; extend graph; add more HVGs |

### Regulatory Inference
| Pitfall | Solution |
|---------|----------|
| No TF motif data | Download from JASPAR/HOCOMOCO (see links above) |
| Missing pySCENIC | Install: `pip install pyscenic pyarrow cytoolz` |
| Limited promoter-only inference | Use extended 150kb windows with distance decay |

---

## Key API Reference

### Data Functions
```python
scglue.data.lsi(adata, n_components=100, n_iter=15)  # LSI for ATAC
scglue.data.get_gene_annotation(adata, gtf, gtf_by)  # Add genomic coords
```

### Graph Functions
```python
scglue.genomics.rna_anchored_guidance_graph(rna, atac)  # Build graph
scglue.genomics.window_graph(bed1, bed2, window_size)  # Overlap graph
scglue.graph.check_graph(graph, [adata1, adata2])  # Validate graph
scglue.graph.compose_multigraph(graphs)  # Merge graphs
```

### Model Functions
```python
scglue.models.configure_dataset(adata, prob_model, **kwargs)  # Configure
scglue.models.fit_SCGLUE(data_dict, graph, **kwargs)  # Train
scglue.models.integration_consistency(model, data_dict, graph)  # Check quality
model.encode_data(domain, adata)  # Get cell embeddings
model.encode_graph(graph)  # Get feature embeddings
model.save(path) / scglue.models.load_model(path)  # Save/load
```

### Regulatory Functions
```python
scglue.genomics.regulatory_inference(features, embeddings, skeleton)  # Infer
scglue.genomics.cis_regulatory_ranking(gene2peak, peak2tf, ...)  # TF ranking
scglue.genomics.build_tf_target_network(rna, atac, ...)  # Full pipeline
scglue.genomics.Bed(var_df)  # Create bed from var
scglue.genomics.write_links(graph, ...)  # Export for pyGenomeTracks
scglue.genomics.write_scenic_feather(ranking, path)  # Export for pySCENIC
```

---

## scGLUE vs SCENIC+ for GRN Inference

Both tools can infer gene regulatory networks from unpaired RNA + ATAC data, but they are **complementary, not competing**.

| Feature | scGLUE Regulatory Inference | SCENIC+ eRegulons |
|---------|----------------------------|-------------------|
| **Method** | Feature embedding cosine similarity | GBM importance + correlation + motif enrichment |
| **Output** | Gene-peak connections (q-value filtered) | TF-region-gene triplets with rankings |
| **Strengths** | Better enhancer-gene detection (f-score ~0.3-0.4) | Better TF-centric modules; AUC scoring per cell |
| **Weaknesses** | Requires separate pySCENIC step for TF assignment | Weaker enhancer-gene detection (f-score ~0.12) |
| **Best for** | Phase C integration + enhancer-gene validation | Phase B5 TF-centric GRN inference |

### Recommended Strategy

1. **SCENIC+ for GRN inference** (Phase B5): Use native unpaired metacell mode
2. **scGLUE for integration** (Phase C): Align with external atlases
3. **scGLUE regulatory inference as validation**: Run Stage 6 independently, compare gene-peak links with SCENIC+ eRegulon regions for high-confidence regulatory calls

### Do NOT Chain scGLUE → SCENIC+

There is **no established workflow** for using scGLUE output as SCENIC+ input. Attempting to create pseudo-paired data from scGLUE nearest-neighbor matching:
- Requires custom code (no tool support)
- May blur condition-specific regulatory signals
- Introduces artificial pairing that is not biologically meaningful
- Adds complexity without proven quality gains

Instead, run both tools independently and intersect results.

See [SCENIC+ skill](../scenic-grn-inference/SKILL.md) for GRN-specific workflows.

### Input Data Preparation

For converting Seurat objects to h5ad for scGLUE, see [multimodal-anndata-mudata.md](../multimodal-anndata-mudata/SKILL.md) Part 4.1.

---

## Resources

- **Documentation:** https://scglue.readthedocs.io/
- **GitHub:** https://github.com/gao-lab/GLUE
- **Paper:** Cao & Gao, Nature Biotechnology 2022
- **TF Motifs (mm10):** http://download.gao-lab.org/GLUE/cisreg/JASPAR2022-mm10.bed.gz
- **TF Motifs (hg38):** http://download.gao-lab.org/GLUE/cisreg/JASPAR2022-hg38.bed.gz
- **ENCODE ChIP-seq:** http://download.gao-lab.org/GLUE/cisreg/ENCODE-TF-ChIP-mm10.bed.gz

---

## When not to use

- Do not use for paired 10x Multiome (shared barcodes). Use scvi-multivi or muon-multimodal-analysis instead.
- Do not install via conda — use a dedicated venv to avoid dependency conflicts.

---

## See also

- `scvi-multivi`
- `muon-multimodal-analysis`
- `scenic-grn-inference`

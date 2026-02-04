---
name: rapids-singlecell-complete
description: RAPIDS Single-Cell GPU 文档完整镜像
---

# Rapids-Singlecell-Complete Skill

Comprehensive assistance with rapids-singlecell-complete development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:

**Core Single-Cell Analysis Tasks:**
- Performing GPU-accelerated single-cell RNA sequencing analysis
- Processing large-scale single-cell datasets that need GPU acceleration
- Implementing preprocessing pipelines (QC, normalization, HVG selection) on GPU
- Running dimensionality reduction (PCA, UMAP, t-SNE) with GPU acceleration
- Computing clustering algorithms (Louvain, Leiden) on large datasets
- Analyzing spatial transcriptomics data with GPU acceleration

**Performance-Critical Scenarios:**
- Working with datasets larger than 100K cells where CPU analysis is too slow
- Needing to process single-cell data in real-time or near real-time
- Running batch correction or integration across multiple samples
- Performing ligand-receptor analysis (gr.ligrec) on spatial data
- Processing multi-million cell datasets that require out-of-core computation

**Advanced GPU Workflows:**
- Setting up Dask CUDA clusters for multi-GPU processing
- Implementing out-of-core analysis with memory management
- Using RMM memory pools for optimal GPU performance
- Integrating with decoupler for pathway activity analysis
- Benchmarking GPU vs CPU performance for single-cell workflows

**Development and Debugging:**
- Optimizing existing scanpy workflows for GPU execution
- Troubleshooting GPU memory issues in single-cell analysis
- Converting CPU-based single-cell pipelines to GPU-accelerated versions
- Setting up GPU environments for single-cell analysis

## Quick Reference

### Essential GPU Setup and Memory Management

**Example 1** (python) - Basic GPU Memory Setup:
```python
import rapids_singlecell as rsc
import cupy as cp
import rmm
from rmm.allocators.cupy import rmm_cupy_allocator

# Initialize RMM memory pool for optimal performance
rmm.reinitialize(
    managed_memory=False,  # Disable for better P2P performance
    pool_allocator=True,   # Enable memory pooling
    devices=0
)
cp.cuda.set_allocator(rmm_cupy_allocator)
```

**Example 2** (python) - Moving Data Between GPU and CPU:
```python
# Move AnnData to GPU
adata.X = cpx.scipy.sparse.csr_matrix(adata.X)  # to GPU
adata.X = adata.X.get()  # back to CPU

# Or use convenience functions
rsc.get.anndata_to_GPU(adata)  # Move entire AnnData to GPU
rsc.get.anndata_to_CPU(adata)  # Move back to CPU
```

### Core Preprocessing Pipeline

**Example 3** (python) - Complete GPU Preprocessing Workflow:
```python
import rapids_singlecell as rsc

# Quality control metrics
rsc.pp.calculate_qc_metrics(adata, qc_vars=["MT"])

# Filter cells and genes
adata = adata[adata.obs["pct_counts_MT"] < 20]
rsc.pp.filter_genes(adata, min_cells=3)

# Normalization and log transformation
rsc.pp.normalize_total(adata, target_sum=1e4)
rsc.pp.log1p(adata)

# Highly variable gene selection
rsc.pp.highly_variable_genes(adata, n_top_genes=5000, flavor="seurat_v3")
adata = adata[:, adata.var["highly_variable"]]

# Scaling and regression
rsc.pp.regress_out(adata, keys=["n_counts", "percent_MT"])
rsc.pp.scale(adata, max_value=10)
```

### Dimensionality Reduction and Clustering

**Example 4** (python) - GPU-Accelerated Dimensionality Reduction:
```python
# Principal Component Analysis
rsc.pp.pca(adata, n_comps=50)

# Neighborhood graph construction
rsc.pp.neighbors(adata, n_neighbors=15)

# Clustering
rsc.tl.leiden(adata, resolution=0.5)

# UMAP embedding
rsc.tl.umap(adata)

# Visualization (can still use scanpy plotting)
import scanpy as sc
sc.pl.umap(adata, color="leiden")
```

### Advanced Multi-GPU Processing

**Example 5** (python) - Dask CUDA Cluster for Large Datasets:
```python
from dask.distributed import Client
from dask_cuda import LocalCUDACluster

# Set up multi-GPU cluster
cluster = LocalCUDACluster(
    CUDA_VISIBLE_DEVICES="0,1,2,3",
    protocol="ucx",  # Use NVLink for P2P
    threads_per_worker=1,
    rmm_pool_size="80%",
    rmm_managed_memory=False
)
client = Client(cluster)

# Load data lazily from Zarr
import anndata as ad, zarr
f = zarr.open("large_dataset.zarr")
adata = ad.AnnData(
    X=read_dask(f["X"], (20000, shape[1])),
    obs=ad.io.read_elem(f["obs"]),
    var=ad.io.read_elem(f["var"])
)
```

### Ligand-Receptor Analysis

**Example 6** (python) - Spatial Ligand-Receptor Interaction:
```python
# GPU-accelerated ligand-receptor analysis
interactions = rsc.squidpy_gpu._ligrec._get_interactions()

res_rsc = rsc.gr.ligrec(
    adata,
    n_perms=1000,
    interactions=interactions,
    cluster_key="CellType",
    copy=True,
    use_raw=True
)

# Access results
means = res_rsc["means"]  # Interaction means
pvalues = res_rsc["pvalues"]  # Statistical significance
```

### Decoupler-GPU for Pathway Analysis

**Example 7** (python) - GPU-Accelerated Pathway Activity:
```python
import decoupler as dc

# Load pathway database
model = dc.op.resource("PanglaoDB", organism="human")

# Run ULM on GPU
rsc.dcg.ulm(adata, model, tmin=3)

# Extract and visualize results
acts_ulm = dc.pp.get_obsm(adata, key="score_ulm")
sc.pl.umap(acts_ulm, color=['NK cells'], cmap='coolwarm', vcenter=0)
```

### Out-of-Core Processing

**Example 8** (python) - Memory-Efficient Large Dataset Processing:
```python
# For datasets larger than GPU memory
rsc.get.anndata_to_GPU(adata)

# Process in chunks with Dask
rsc.pp.normalize_total(adata)  # Lazy operation
rsc.pp.log1p(adata)  # Lazy operation

# HVG selection (triggers computation)
rsc.pp.highly_variable_genes(adata)
adata = adata[:, adata.var["highly_variable"]].copy()

# Persist intermediate results
adata.X = adata.X.persist()
adata.X.compute_chunk_sizes()
```

## Key Concepts

### GPU Memory Management
- **RMM Pool Allocator**: Manages GPU memory efficiently for repeated allocations
- **Managed Memory**: Allows oversubscription of GPU VRAM at performance cost
- **NVLink P2P**: Direct GPU-to-GPU communication for multi-GPU setups

### AnnData GPU Integration
- **GPU Arrays**: AnnData natively supports CuPy arrays and GPU sparse matrices
- **Lazy Operations**: Dask integration enables out-of-core processing
- **Memory Transfer**: Efficient CPU-GPU data movement utilities

### Performance Optimization
- **Chunk Size**: Optimize Dask chunk sizes (~20K rows) for GPU processing
- **Threading**: Use `threads_per_worker=1` for GPU workloads
- **Protocol Selection**: UCX for NVLink, TCP for managed memory scenarios

## Reference Files

This skill includes comprehensive documentation in `references/`:

### **api.md** - Core API Documentation (130 pages)
Contains the complete API reference including:
- **Usage Principles**: Basic workflow and AnnData setup
- **Preprocessing Functions** (`rsc.pp`): QC, normalization, scaling, HVG selection
- **Tools Functions** (`rsc.tl`): Dimensionality reduction, clustering, embeddings
- **Spatial Analysis** (`rsc.gr`): Ligand-receptor interactions, spatial autocorrelation
- **Decoupler-GPU** (`rsc.dcg`): Accelerated pathway analysis methods
- **Memory Management**: GPU-CPU data transfer utilities

### **other.md** - Supporting Documentation (35 pages)
Contains additional resources:
- **Notebook Examples**: Complete workflows and benchmarks
- **Performance Comparisons**: GPU vs CPU timing results
- **Ligrec Benchmark**: Detailed spatial analysis performance data
- **Visual Assets**: Diagrams and performance charts

## Working with This Skill

### For Beginners
1. **Start with Basic Setup**: Use Example 1-2 to initialize GPU memory and data transfer
2. **Follow Standard Workflow**: Use the preprocessing pipeline in Example 3
3. **Use Scanpy Compatibility**: Leverage existing scanpy knowledge - most functions are drop-in replacements
4. **Monitor GPU Memory**: Start with smaller datasets to understand memory requirements

### For Intermediate Users
1. **Optimize Memory Usage**: Implement RMM pooling and proper chunk sizes
2. **Multi-GPU Processing**: Set up Dask clusters using Example 5 for large datasets
3. **Spatial Analysis**: Use ligand-receptor analysis (Example 6) for spatial transcriptomics
4. **Performance Benchmarking**: Compare GPU vs CPU performance for your specific use case

### For Advanced Users
1. **Out-of-Core Processing**: Implement Example 8 for datasets larger than GPU memory
2. **Pathway Analysis**: Integrate decoupler-GPU (Example 7) for advanced biological interpretation
3. **Memory Tuning**: Experiment with RMM settings for optimal performance
4. **Custom Pipelines**: Build end-to-end GPU-accelerated single-cell workflows

### Navigation Tips
- **API Functions**: Check `api.md` for detailed parameter documentation
- **Performance Guidance**: Refer to notebook examples in `other.md` for benchmarks
- **Memory Issues**: Look for RMM and Dask configuration examples
- **Spatial Analysis**: Use `rsc.gr` functions for ligand-receptor and spatial statistics

## Resources

### **references/**
Organized documentation containing:
- Complete API reference with parameter descriptions
- Real-world code examples with performance metrics
- Links to original documentation for deeper exploration
- Structured table of contents for quick navigation

### **scripts/**
Add helper scripts for:
- GPU environment setup automation
- Memory optimization utilities
- Performance benchmarking tools
- Data conversion between CPU and GPU formats

### **assets/**
Add templates and examples for:
- Common single-cell analysis workflows
- Multi-GPU cluster configurations
- Memory optimization profiles
- Benchmarking result templates

## Notes

- **GPU Compatibility**: Requires NVIDIA GPU with CUDA support
- **Memory Requirements**: Dataset size limited by GPU VRAM (unless using out-of-core)
- **Scanpy Compatibility**: Most scanpy functions have direct GPU equivalents
- **Performance Gains**: Typical speedups of 10-100x for large datasets
- **Ecosystem Integration**: Works with cupy, dask, and RAPIDS ecosystem

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest API documentation
3. Performance benchmarks and examples will be updated accordingly

## Installation Prerequisites

Before using this skill, ensure you have:
- NVIDIA GPU with CUDA 11.0+ support
- RAPIDS ecosystem installed (cuDF, cuML, cuPy)
- Sufficient GPU VRAM for your dataset size
- Optional: Dask-CUDA for multi-GPU processing

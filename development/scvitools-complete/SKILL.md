---
name: scvitools-complete
description: scvi-tools 单细胞深度学习框架 - 100%覆盖文档（完整API+教程+模型训练+多模态整合）
---

# Scvitools-Complete Skill

Comprehensive assistance with scvi-tools development, the deep probabilistic framework for single-cell omics analysis.

## When to Use This Skill

This skill should be triggered when:
- **Working with scvi-tools models** - SCVI, totalVI, scANVI, MultiVI, etc.
- **Setting up single-cell analysis workflows** - data preprocessing, model training, evaluation
- **Implementing multi-omic integration** - CITE-seq, scRNA+ATAC, spatial transcriptomics
- **Performing differential expression analysis** with probabilistic models
- **Batch correction and data integration** across multiple datasets
- **Reference mapping and transfer learning** applications
- **Debugging scvi-tools models** or training issues
- **Learning scvi-tools best practices** and model selection
- **Optimizing hyperparameters** using autotune functionality
- **Working with spatial transcriptomics deconvolution** (DestVI, Cell2location)

## Quick Reference

### Essential Setup Patterns

**Pattern 1: Basic Data Loading and Setup**
```python
import scvi
import scanpy as sc

# Load dataset
adata = scvi.data.pbmc_seurat_v4_cite_seq()
sc.pp.filter_genes(adata, min_counts=3)

# Setup anndata for scVI model
scvi.model.SCVI.setup_anndata(
    adata,
    layer="counts",
    batch_key="batch",
    labels_key="cell_type"
)
```

**Pattern 2: Model Training and Inference**
```python
# Initialize and train SCVI model
model = scvi.model.SCVI(adata)
model.train()

# Get latent representation
latent = model.get_latent_representation()
adata.obsm["X_scVI"] = latent

# Get normalized expression
normalized = model.get_normalized_expression()
```

**Pattern 3: Multi-omic Integration with totalVI**
```python
# Setup for CITE-seq data
scvi.model.TOTALVI.setup_anndata(
    adata,
    layer="counts",
    batch_key="batch",
    protein_expression_obsm_key="protein_expression"
)

# Train totalVI model
model = scvi.model.TOTALVI(adata)
model.train()

# Get joint latent space
latent = model.get_latent_representation()
```

**Pattern 4: Hyperparameter Tuning with Autotune**
```python
from scvi import autotune
import ray.tune as tune

# Define search space
search_space = {
    "model_params": {
        "n_hidden": tune.choice([64, 128, 256]),
        "n_layers": tune.choice([1, 2, 3])
    },
    "train_params": {
        "max_epochs": 100,
        "plan_kwargs": {"lr": tune.loguniform(1e-4, 1e-2)}
    }
}

# Run autotune
results = autotune.run_autotune(
    scvi.model.SCVI,
    data=adata,
    mode="min",
    metrics="validation_loss",
    search_space=search_space,
    num_samples=5
)
```

**Pattern 5: Differential Expression Analysis**
```python
# Perform differential expression between cell types
de_results = model.differential_expression(
    groupby="cell_type",
    group1="T-cell",
    group2="B-cell"
)

# Get top DE genes
top_genes = de_results.sort_values("lfc_mean").head(10)
```

**Pattern 6: Reference Mapping and Transfer Learning**
```python
# Train on reference data
ref_model = scvi.model.SCVI(adata_ref)
ref_model.train()

# Map query data
query_model = scvi.model.SCVI.load_query_data(
    adata_ref,
    adata_query,
    freeze_model=True
)
query_model.train(max_epochs=50)

# Transfer cell type labels
preds = query_model.predict(adata_query)
```

**Pattern 7: Spatial Transcriptomics Deconvolution**
```python
# Train scLVM on single-cell reference
sc_model = scvi.model.SCVI(sc_adata)
sc_model.train()

# Train DestVI on spatial data
st_model = scvi.model.DestVI.from_scvi_model(
    st_adata,
    sc_model
)
st_model.train()

# Get cell type proportions
proportions = st_model.get_proportions()
```

**Pattern 8: Model Saving and Loading**
```python
# Save trained model
model.save("my_scvi_model/")

# Load model for later use
loaded_model = scvi.model.SCVI.load("my_scvi_model/")
## Key Concepts

### Core Models
- **SCVI**: Single-cell Variational Inference for scRNA-seq integration and denoising
- **totalVI**: Joint modeling of RNA and protein data (CITE-seq)
- **scANVI**: Semi-supervised variant for cell type annotation
- **MultiVI**: Integration of paired and unpaired multi-omic data
- **DestVI**: Spatial transcriptomics deconvolution with sub-cell-type resolution
- **PeakVI**: Analysis of scATAC-seq chromatin accessibility data

### Fundamental Components
- **Variational Autoencoders**: Core architecture for probabilistic modeling
- **Zero-Inflated Negative Binomial**: Default likelihood distribution for UMI counts
- **Latent Space**: Low-dimensional representation capturing biological variation
- **Batch Correction**: Removal of technical artifacts across experiments
- **Transfer Learning**: Adapting pretrained models to new datasets

## Reference Files

### api_data.md
**Data Loading and Dataset APIs**
- Built-in datasets (PBMC, heart cell atlas, synthetic data)
- Data reading functions (read_h5ad, read_csv, read_10x)
- Synthetic data generation utilities
- Multi-modal data organization functions

### development.md
**Developer Documentation**
- Development environment setup
- Code contribution guidelines
- Testing frameworks and standards
- Code style and documentation requirements

### getting_started.md
**User Guides and Model Documentation**
- In-depth model explanations (SCVI, DestVI, totalVI, etc.)
- Mathematical foundations and generative processes
- Practical usage examples and best practices
- Task-specific workflows (dimensionality reduction, DE analysis)

### other.md
**References and Citations**
- Complete bibliography of scvi-tools papers
- Method references and related publications
- Citation information for research use

### reference.md
**Complete API Reference**
- Detailed class and function documentation
- Parameter specifications and return values
- Advanced configuration options
- Internal architecture details

## Working with This Skill

### For Beginners
1. **Start with basic SCVI workflow**: Load data → setup_anndata → train → get_latent_representation
2. **Follow getting_started.md** for comprehensive model introductions
3. **Use built-in datasets** for initial experimentation
4. **Focus on data preprocessing** - quality control is crucial

### For Intermediate Users
1. **Explore multi-omic models** (totalVI, MultiVI) for integrated analysis
2. **Implement hyperparameter tuning** with the autotune module
3. **Use reference mapping** for transferring annotations
4. **Apply differential expression** analysis with probabilistic models

### For Advanced Users
1. **Implement custom models** using the base classes
2. **Develop new data loaders** for specialized assays
3. **Contribute to the codebase** following development guidelines
4. **Optimize performance** with multi-GPU training and JAX backend

### Navigation Tips
- **API questions**: Check reference.md for detailed function documentation
- **Workflow guidance**: Use getting_started.md for model-specific tutorials
- **Data handling**: Refer to api_data.md for data loading utilities
- **Development**: See development.md for contribution guidelines

## Resources

### Official Resources
- **scvi-tools Documentation**: https://scvi-tools.org
- **GitHub Repository**: https://github.com/scverse/scvi-tools
- **Community Forum**: https://discourse.scvi-tools.org
- **Zulip Chat**: https://scvi-tools.zulipchat.com

### Model Hub
- **scvi-hub**: Pretrained models for common applications
- **Reference Atlases**: CellxGENE and other large-scale datasets
- **Method Comparisons**: Benchmarking tools and metrics

### Common Workflows
- **Integration**: Batch correction across multiple datasets
- **Annotation**: Cell type labeling with scANVI
- **Multi-omics**: Joint analysis of RNA + protein + ATAC
- **Spatial**: Deconvolution and spatial mapping
- **Trajectory**: RNA velocity and developmental dynamics

## Notes

- **GPU Recommended**: Most models benefit significantly from GPU acceleration
- **Memory Management**: Large datasets may require data subsampling or batched training
- **Model Selection**: Choose models based on data type and analysis goals
- **Quality Control**: Always perform thorough QC before model training
- **Parameter Tuning**: Hyperparameters can significantly impact results

## Updating

To refresh this skill with updated documentation:
1. Re-run the documentation scraper with the same configuration
2. The skill will be rebuilt with the latest API changes and tutorials
3. Check the scvi-tools version compatibility for your use case

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api_data.md** - Api Data documentation
- **development.md** - Development documentation
- **getting_started.md** - Getting Started documentation
- **other.md** - Other documentation
- **reference.md** - Reference documentation
- **tutorials.md** - Tutorials documentation

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with the getting_started or tutorials reference files for foundational concepts.

### For Specific Features
Use the appropriate category reference file (api, guides, etc.) for detailed information.

### For Code Examples
The quick reference section above contains common patterns extracted from the official docs.

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.

## Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information

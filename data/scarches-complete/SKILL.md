---
name: scarches-complete
description: scArches 单细胞深度学习参考图谱框架 - 100%覆盖文档（26个HTML文件，包含完整API、教程、模型训练、多模态整合）
---

# Scarches-Complete Skill

Comprehensive assistance with scArches (single-cell architecture surgery) development, generated from official documentation. scArches enables integration of newly produced single-cell datasets into integrated reference atlases through decentralized training and model surgery.

## When to Use This Skill

This skill should be triggered when:
- **Building reference atlases** using scVI, trVAE, scANVI, totalVI, or expiMap models
- **Mapping query datasets** to existing reference atlases for cell type annotation
- **Performing cell type label transfer** from reference to query datasets
- **Integrating multi-modal data** (CITE-seq, scRNA-seq + ATAC, TCR + transcriptome)
- **Analyzing spatial transcriptomics** data with SageNet
- **Working with gene programs** and pathway analysis using expiMap
- **Training deep generative models** for single-cell data integration
- **Debugging scArches models** or optimization issues
- **Learning best practices** for single-cell reference mapping

## Quick Reference

### Essential Code Patterns

**Import and Setup**
```python
import warnings
warnings.simplefilter(action='ignore')
import scanpy as sc
import torch
import scarches as sca
import numpy as np
import gdown
```

**Reference Model Training (expiMap)**
```python
# Prepare data with gene annotations
sca.utils.add_annotations(adata, 'reactome.gmt', min_genes=12, clean=True)
adata._inplace_subset_var(adata.varm['I'].sum(1)>0)

# Initialize and train model
intr_cvae = sca.models.EXPIMAP(
    adata=adata,
    condition_key='study',
    hidden_layer_sizes=[256, 256, 256],
    recon_loss='nb'
)

# Train with early stopping
early_stopping_kwargs = {
    "early_stopping_metric": "val_unweighted_loss",
    "threshold": 0,
    "patience": 50,
    "reduce_lr": True,
    "lr_patience": 13,
    "lr_factor": 0.1,
}
intr_cvae.train(
    n_epochs=400,
    alpha_epoch_anneal=100,
    alpha=0.7,
    alpha_kl=0.5,
    early_stopping_kwargs=early_stopping_kwargs,
    use_early_stopping=True
)
```

**Query Dataset Mapping**
```python
# Load pretrained reference model
model = sca.models.SCANVI.load_query_data(adata_query, reference_model)

# Fine-tune on query data
model.train(
    n_epochs=100,
    train_size=1.0,
    lr=1e-4,
    use_early_stopping=True
)

# Get latent representation
latent = model.get_latent_representation()
```

**Cell Type Label Transfer**
```python
# Train weighted KNN classifier
knn_model = sca.utils.weighted_knn_trainer(
    train_adata,
    train_adata_emb='X_emb',
    n_neighbors=50
)

# Transfer labels to query
sca.utils.weighted_knn_transfer(
    query_adata,
    ref_adata_obs=train_adata.obs,
    label_keys='cell_type',
    knn_model=knn_model,
    threshold=0.5
)
```

**Multi-modal Integration (mvTCR)**
```python
# Initialize mvTCR model for TCR + transcriptome
model = sca.models.mvTCR.models.mixture_modules.moe.MoEModel(
    adata_train,
    params_architecture,
    balanced_sampling='clonotype',
    metadata=['clonotype', 'Sample', 'Type'],
    conditional='Cohort'
)

# Train model
model.train(n_epochs=200, early_stop=5)
```

**Model Sharing with Zenodo**
```python
# Upload trained model to Zenodo
download_link = sca.utils.zenodo.upload_model(
    model=trained_model,
    deposition_id='your_deposition_id',
    access_token='your_token',
    model_name='my_scarches_model'
)

# Download model from Zenodo
extract_dir = sca.utils.zenodo.download_model(
    link='download_link',
    save_path='models/',
    extract_dir=True
)
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

### Core Documentation
- **api_reference.md** - Complete API reference for all scArches functions and classes
  - Zenodo integration utilities for model sharing
  - Utility functions for annotations and KNN classification
  - Model training and inference methods

- **getting_started.md** - Installation and introduction guide
  - Installation via pip, conda, or from source
  - Overview of scArches capabilities and model types
  - Quick start examples and basic workflow

- **training_tips.md** - Best practices for model training
  - Loss function selection (nb, zinb, mse)
  - Hyperparameter recommendations
  - Architecture guidance for different data complexities

### Advanced Tutorials
- **tutorials_advanced.md** - Specialized model tutorials
  - mvTCR: Multi-modal TCR + transcriptome integration
  - Human Lung Cell Atlas mapping and classification
  - Advanced cell type label transfer techniques

- **tutorials_surgery_pipeline.md** - Complete surgery workflow
  - Reference model construction
  - Query dataset preparation and mapping
  - Joint analysis and visualization

- **tutorials_treearches.md** - Hierarchical cell type analysis
  - Tree-based cell type discovery
  - Novel cell state identification
  - Hierarchical annotation transfer

## Working with This Skill

### For Beginners
1. **Start with getting_started.md** to understand scArches concepts and installation
2. **Follow the basic surgery pipeline** for your first reference mapping project
3. **Use the Quick Reference examples** as templates for common tasks
4. **Consult training_tips.md** before training your first models

### For Intermediate Users
1. **Explore api_reference.md** for detailed function documentation
2. **Try advanced tutorials** for specialized applications (multi-modal, spatial)
3. **Use Zenodo integration** for model sharing and collaboration
4. **Experiment with different models** (scVI, scANVI, expiMap, totalVI) based on your data

### For Advanced Users
1. **Dive into model-specific tutorials** for complex use cases
2. **Optimize hyperparameters** using training tips and experimentation
3. **Implement custom workflows** using the comprehensive API
4. **Contribute models** to community atlases using Zenodo sharing

## Key Concepts

### Model Types
- **scVI**: Count-based integration using raw counts, assumes NB/ZINB distribution
- **trVAE**: Supports normalized or count data with MMD loss for better integration
- **scANVI**: Requires cell type labels for reference, enables classification
- **expiMap**: Incorporates gene programs for interpretable representation learning
- **totalVI**: Multi-modal CITE-seq reference construction
- **treeArches**: Hierarchical cell type discovery and novel state identification
- **SageNet**: Spatial transcriptomics mapping to coordinate frameworks
- **mvTCR**: T-cell receptor + transcriptome joint analysis

### Core Workflow
1. **Reference Construction**: Train model on integrated reference dataset
2. **Model Surgery**: Adapt pretrained model for query datasets
3. **Query Mapping**: Project query data into reference latent space
4. **Downstream Analysis**: Clustering, classification, trajectory analysis

### Data Requirements
- **Raw counts** preferred for scVI, scANVI, totalVI
- **Normalized data** acceptable for trVAE (set recon_loss='mse')
- **Highly variable genes**: Minimum 2000, increase to 5000 for complex datasets
- **Cell type labels**: Required for scANVI reference, optional for query

## Resources

### references/
Comprehensive documentation extracted from official sources containing:
- Detailed API documentation with parameter descriptions
- Step-by-step tutorials with real datasets
- Code examples with proper syntax highlighting
- Links to original documentation for further reading

### scripts/
Add helper scripts for:
- Data preprocessing pipelines
- Model training automation
- Batch effect evaluation
- Visualization utilities

### assets/
Store:
- Example datasets and preprocessing results
- Trained model checkpoints
- Configuration templates
- Visualization templates

## Notes

- This skill was generated from official scArches documentation (http://127.0.0.1:9180)
- Reference files preserve original structure and examples
- All code examples extracted from actual tutorials and API docs
- Training recommendations based on empirical best practices

## Updating

To refresh this skill with updated documentation:
1. Re-run the documentation scraper with current scArches version
2. Update reference files with latest API changes and tutorials
3. Verify code examples against newest scArches release
4. Test training workflows with updated hyperparameters

## Common Use Cases

### Cell Type Annotation
```python
# Map query to reference and transfer labels
query_adata = sca.utils.read('query_data.h5ad')
model = sca.models.SCANVI.load_query_data(query_adata, ref_model)
model.train(max_epochs=400)
predictions = model.predict(query_adata)
```

### Multi-modal Integration
```python
# CITE-seq data integration
model = sca.models.TOTALVI(adata)
model.train()
latent_rna, latent_protein = model.get_latent_representation()
```

### Spatial Mapping
```python
# Map scRNA-seq to spatial reference
sage_model = sca.models.SageNet(spatial_ref, query_sc)
spatial_predictions = sage_model.predict_locations(query_sc)
```

### Gene Program Analysis
```python
# Analyze query in context of known pathways
expimap_model = sca.models.EXPIMAP(reference, gene_sets='reactome')
gp_activities = expimap_model.get_gene_program_scores(query_data)
```

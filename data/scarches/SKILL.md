---
name: scarches
description: Comprehensive skill for scARCHES - Deep learning library for single-cell analysis of chromatin accessibility data. Use for scATAC-seq data processing, model training, batch correction, integration with scRNA-seq, and spatial chromatin analysis.
---

# Scarches Skill

Comprehensive assistance with scarches development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when you need to:

**Data Analysis & Processing:**
- Perform scATAC-seq data preprocessing and quality control
- Integrate multi-omics single-cell data (scRNA-seq + scATAC-seq)
- Map query datasets to reference atlases (e.g., Human Lung Cell Atlas)
- Apply batch correction across different single-cell experiments

**Model Development & Training:**
- Build and train scVI, SCANVI, TRVAE, or totalVI models
- Perform model surgery for adapting pre-trained models to new data
- Set up early stopping and hyperparameter optimization
- Handle raw count data vs. normalized data appropriately

**Advanced Applications:**
- Transfer cell type labels from reference to query datasets
- Work with multi-modal TCR data using mvTCR
- Perform spatial chromatin accessibility analysis
- Create comprehensive atlases and reference embeddings

**Technical Implementation:**
- Debug model training issues and convergence problems
- Optimize model architecture (layers, latent dimensions)
- Choose appropriate loss functions (nb, zinb, mse)
- Set up proper data preprocessing pipelines

## Quick Reference

### Essential Imports and Setup
```python
import scanpy as sc
import torch
import scarches as sca
from scarches.dataset.trvae.data_handling import remove_sparsity
import matplotlib.pyplot as plt
import numpy as np
import gdown

# Configure scanpy settings
sc.settings.set_figure_params(dpi=200, frameon=False)
sc.set_figure_params(figsize=(4, 4))
torch.set_printoptions(precision=3, sci_mode=False, edgeitems=7)
```

### Data Preparation for scARCHES
```python
# Ensure count data is in adata.X for models using 'nb' or 'zinb' loss
# Remove sparsity for memory efficiency
adata = remove_sparsity(adata)

# Remove obsm and varm matrices to prevent downstream errors
adata.obsm = {}
adata.varm = {}

# Check for integer count data
print(f"Data type: {adata.X.dtype}")
```

### Model Configuration Examples
```python
# TRVAE model with early stopping
condition_key = 'study'
cell_type_key = 'cell_type'
target_conditions = ['Pancreas CelSeq2', 'Pancreas SS2']

trvae_epochs = 500
surgery_epochs = 500

early_stopping_kwargs = {
    "early_stopping_metric": "val_unweighted_loss",
    "threshold": 0,
    "patience": 20,
    "reduce_lr": True,
    "lr_patience": 13,
    "lr_factor": 0.1,
}

# Create TRVAE model with NB loss (default)
trvae_model = sca.models.TRVAE(
    adata=adata,
    condition_key=condition_key,
    recon_loss='nb',  # Use 'mse' for normalized data, 'zinb' for zero-inflated
    beta=1.0,  # MMD regularization strength
    hidden_layers=[128, 128],
    latent_dim=10
)
```

### SCVI Model for Integration
```python
# Create SCVI model with ZINB loss (default)
scvi_model = sca.models.SCVI(
    adata=adata,
    gene_likelihood='zinb'  # Use 'nb' for negative binomial loss
)

# Train the model
scvi_model.train(max_epochs=400)

# Save for later use
scvi_model.save("scvi_model")
```

### Model Surgery for Query Data
```python
# Load pretrained model
scvi_model = sca.models.SCVI.load("scvi_model")

# Perform surgery to adapt to query data
query_model = sca.models.SCVI.load_query_data(
    scvi_model,
    adata_query,
    freeze_classifier=True  # Keep reference embeddings stable
)

# Train on query data with fewer epochs
query_model.train(max_epochs=200)

# Get latent representations
latent = query_model.get_latent_representation()
adata_query.obsm["X_scVI"] = latent
```

### Setting Up Model Variables for Reference Mapping
```python
# For HLCA (Human Lung Cell Atlas) mapping
batch_key = 'batch'           # How batches are identified
labels_key = 'cell_type'      # Cell type annotations
unlabeled_category = 'unlabeled'  # Category for unknown cells

# Set query batch (usually single batch per dataset)
adata_query.obs[batch_key] = 'my_dataset'

# Set all query cells as unlabeled for mapping
adata_query.obs[labels_key] = unlabeled_category
```

### KNN Classification for Label Transfer
```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import f1_score

# Train KNN on latent representations
knn = KNeighborsClassifier(n_neighbors=15)
knn.fit(reference_latent, reference_labels)

# Predict labels for query data
predicted_labels = knn.predict(query_latent)
adata_query.obs['predicted_cell_type'] = predicted_labels

# Calculate prediction confidence
confidence_scores = knn.predict_proba(query_latent)
adata_query.obs['prediction_confidence'] = np.max(confidence_scores, axis=1)
```

### Training Tips and Hyperparameters
```python
# Model architecture recommendations
hidden_layers = [128, 128]  # Default, good for most datasets
latent_dim = 10             # Default (10-20 recommended)
beta = 1.0                  # MMD strength for TRVAE

# Loss function selection
if has_raw_counts:
    recon_loss = 'nb' or 'zinb'  # For count data
else:
    recon_loss = 'mse'           # For normalized data

# Early stopping for TRVAE
early_stopping_kwargs = {
    "early_stopping_metric": "val_unweighted_loss",  # Best for TRVAE
    "threshold": 0,
    "patience": 20,
    "reduce_lr": True,
    "lr_patience": 13,
    "lr_factor": 0.1,
}
```

## Key Concepts

### Model Types
- **SCVI**: Single-cell Variational Inference for count data integration
- **SCANVI**: Semi-supervised extension with cell type labels
- **TRVAE**: Transfer VAE with MMD regularization for cross-dataset integration
- **totalVI**: Multi-modal model for RNA + protein data
- **mvTCR**: Multi-modal model for transcriptome + TCR data

### Model Surgery
A technique to adapt pre-trained reference models to new query data by:
1. Loading the reference model
2. Adding new query-specific parameters
3. Freezing reference embeddings
4. Training only query adaptation layers

### Loss Functions
- **nb (Negative Binomial)**: Good for count data with overdispersion
- **zinb (Zero-Inflated NB)**: Handles excess zeros in scATAC-seq
- **mse (Mean Squared Error)**: Use for normalized/log-transformed data

### Key Hyperparameters
- **beta**: MMD regularization strength (higher = more integration, lower = preserve biology)
- **alpha_kl**: KL divergence weight for SCVI/SCANVI
- **latent_dim**: Dimensionality of the latent space (10-20 recommended)
- **early_stopping_metric**: 'val_unweighted_loss' for TRVAE, 'elbo_validation' for SCVI

## Reference Files

This skill includes comprehensive documentation in `references/`:

### **api_reference.md** - Complete API Documentation
Contains detailed tutorials and walkthroughs:
- **Unsupervised surgery pipeline with SCVI**: Full workflow from data preparation to model adaptation
- **Unsupervised surgery pipeline with TRVAE**: Alternative approach with MMD regularization
- **Mapping to Human Lung Cell Atlas**: Step-by-step guide for reference mapping and label transfer
- Code examples for each major use case
- Data preprocessing and preparation instructions
- Model saving and loading procedures

### **models.md** - Model Architecture and Training
Essential information for model development:
- **Training tips**: Loss function selection based on data type
- **Architecture recommendations**: Hidden layers, latent dimensions for different dataset complexities
- **Hyperparameter tuning**: Beta values, early stopping criteria, regularization parameters
- **Performance guidelines**: When to increase model capacity vs. regularization
- **Best practices**: Variable gene selection, count data requirements

### **other.md** - Specialized Applications
Advanced use cases and domain-specific methods:
- **mvTCR Tutorial**: Multi-modal integration of transcriptome and TCR data for tumor-infiltrating lymphocytes
- Tissue origin inference using learned representations
- KNN classification on latent embeddings for downstream tasks
- Cancer type prediction from TIL data

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
1. **Start with basic data preprocessing**: Read the api_reference.md for essential imports and data setup
2. **Choose your first model**: Begin with SCVI for count data integration or TRVAE for cross-dataset mapping
3. **Follow the complete tutorials**: The SCVI and TRVAE surgery pipelines provide end-to-end workflows
4. **Check model training tips**: Review models.md for hyperparameter guidance

### For Intermediate Users
1. **Reference mapping**: Use the HLCA mapping tutorial when integrating your data with existing atlases
2. **Label transfer**: Implement KNN classification for automated cell type annotation
3. **Model surgery**: Adapt pre-trained models to new datasets efficiently
4. **Multi-modal analysis**: Explore mvTCR for TCR-RNA integration or totalVI for protein-RNA data

### For Advanced Users
1. **Model architecture optimization**: Experiment with deeper networks ([128,128,128]) for complex datasets
2. **Custom loss functions**: Modify reconstruction losses based on data characteristics
3. **Large-scale atlases**: Build comprehensive reference using the architecture and training guidelines
4. **Spatial chromatin analysis**: Apply to spatial transcriptomics data integration

### Navigation Tips
- **Data-first approach**: Always start with understanding your data type (counts vs. normalized)
- **Model selection flow**: Choose SCVI/SCANVI for count data, TRVAE for batch correction, mvTCR for TCR
- **Reference mapping workflow**: Follow HLCA tutorial step-by-step for first-time users
- **Troubleshooting**: Check models.md for training tips if models don't converge

## Resources

### references/
Organized documentation extracted from official sources:
- **Step-by-step tutorials** with complete code workflows
- **Real-world examples** from published datasets
- **Parameter tuning guides** based on experimental results
- **Best practice recommendations** from core developers
- **Links to original documentation** for further reading

### scripts/
Add your automation scripts here:
- Data preprocessing pipelines
- Model training and evaluation workflows
- Batch processing for multiple datasets
- Visualization and analysis utilities

### assets/
Store templates and reference materials:
- Configuration file templates for common use cases
- Example dataset formats and metadata schemas
- Visualization templates for model results
- Documentation for custom preprocessing steps

## Notes

### Data Requirements
- **Raw counts** are required for 'nb' and 'zinb' loss functions
- **Highly variable genes** (2000-5000) recommended for model training
- **Batch information** should be stored in adata.obs columns
- **Cell type labels** needed for SCANVI training in semisupervised mode

### Performance Considerations
- Use **remove_sparsity()** for better memory efficiency
- Implement **early stopping** to prevent overfitting
- Monitor **training loss curves** for convergence issues
- Adjust **beta parameter** based on integration quality vs. biological variation

### Common Pitfalls
- Using normalized data with count-based loss functions (nb, zinb)
- Forgetting to set query cells to 'unlabeled' category for mapping
- Not checking that gene symbols/match between reference and query
- Overfitting when using too many latent dimensions (>50)

## Updating

To refresh this skill with updated documentation:
1. Check the official scArches documentation at https://docs.scarches.org/
2. Re-run the scraper with updated source URLs if available
3. The skill will preserve existing structure while incorporating new examples and methods

For the most current information, always cross-reference with the official scArches documentation and GitHub repository.
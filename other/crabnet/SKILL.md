---
name: crabnet
description: Materials property prediction using only composition information via the Roost architecture. Use when predicting properties from chemical formulas without requiring crystal structure data.
metadata:
    skill-author: MindSpore Science Team
---

# Overview

CrabNet (Compositionally Restricted Attention Based Network) predicts materials properties using only chemical composition. It implements the Roost architecture with multi-head attention to learn element interactions without needing crystal structure data.

# Installation

```bash
# Via pip
pip install crabnet

# Or via conda (from the fork with easier API)
conda install -c sgbaird crabnet

# From source
git clone https://github.com/anthony-wang/CrabNet.git
conda env create --file conda-env.yml
conda activate crabnet
```

# Quick Start

```python
from crabnet.crabnet_ import CrabNet

# Initialize model
cb = CrabNet()

# Train with CSV containing 'formula' and 'target' columns
cb.train(data_dir="data/materials_data", mat_prop="my_property")

# Predict on new compositions
predictions = cb.predict(data_dir="data/materials_data", mat_prop="my_property")

# Or use the simplified API (from sparks-baird fork)
from crabnet.kingcrab import SubCrab
model = SubCrab()
model.fit(train_df, val_df)
predictions = model.predict(test_df)
```

# When to Use This Skill

Use CrabNet when you need to:

- Predict materials properties from **chemical formulas only** (e.g., "Fe2O3", "LiCoO2")
- Rapidly screen large composition spaces without DFT calculations
- Work with datasets lacking crystal structure information
- Build baseline models for composition-based property prediction
- Leverage attention mechanisms for interpretable element interaction analysis
- Perform transfer learning between related property prediction tasks

**Consider alternatives when:**
- Crystal structure is available and critical for accuracy (use CGCNN, MEGNet)
- You need to predict structure-dependent properties (e.g., elastic anisotropy)
- Dataset is extremely small (<50 samples) - consider simpler models

# Key Features

## Composition-Only Prediction
- Predict properties from chemical formulas alone (e.g., "Fe2O3")
- No crystal structure required - ideal for rapid screening
- Handles arbitrary compositions with multiple elements

## Attention Mechanism
- Multi-head attention learns element interaction patterns
- Interpretable attention weights for model explainability
- Captures non-linear composition-property relationships

## Model Architecture
- Transformer encoder with element embeddings
- Residual connections for deep networks
- Supports regression and classification tasks

# Common Use Cases

## Property Prediction
```python
# Predict bulk modulus from compositions
cb = CrabNet()
cb.train(data_dir="data/", mat_prop="bulk_modulus")
mae = cb.predict(data_dir="data/", mat_prop="bulk_modulus")
```

## Transfer Learning
- Pre-train on large datasets (OQMD, Materials Project)
- Fine-tune on smaller target property datasets
- Transfer knowledge between related properties

## Model Interpretability
- Extract per-head attention matrices
- Identify important element interactions
- Visualize learned element embeddings

# Best Practices

## Data Preparation
- Ensure compositions are normalized or consistently formatted
- Remove duplicate compositions with different targets
- Include uncertainty estimates if available
- Use stratified splitting for classification tasks

## Training
- Start with default hyperparameters; tune learning rate first
- Use robust loss functions (L1Loss) for outlier-heavy data
- Enable `--robust` flag for uncertainty quantification
- Monitor validation loss to prevent overfitting

## Model Selection
- Use k-fold cross-validation for reliable performance estimates
- Compare against dummy baselines (mean predictor)
- For small datasets (<1000 samples), increase epochs and use early stopping

## Evaluation
- Report MAE/RMSE with standard deviation across folds
- Use parity plots to visualize prediction quality
- Analyze residuals for systematic errors

# Troubleshooting

## Common Issues

### CUDA out of memory
- Reduce batch size: `cb.batch_size = 32`
- Use smaller model: `cb.d_model = 128`

### Poor predictions
- Check data quality: remove outliers, verify target values
- Increase training data or use transfer learning
- Verify composition format (use pymatgen Composition)

### Slow training
- Enable GPU: ensure PyTorch CUDA is installed
- Reduce number of attention heads: `cb.N_heads = 4`

### NaN losses
- Check for inf/NaN in training data
- Reduce learning rate: `cb.lr = 1e-4`
- Enable gradient clipping

# Data Format

Training CSV files require:
- `formula`: Chemical formula string (e.g., "Fe2O3", "NaCl")
- `target`: Numerical property value

# Resources

- GitHub: https://github.com/anthony-wang/CrabNet
- Paper: Wang et al., npj Comput Mater 7, 77 (2021)
- DOI: https://doi.org/10.1038/s41524-021-00545-1
- Language: Python
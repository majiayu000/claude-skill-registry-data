---
name: modnet
description: Material Optimal Descriptor Network for machine learning materials properties from composition or crystal structure. Use when building ML models for materials property prediction, especially with limited datasets or when learning multiple properties jointly.
metadata:
    skill-author: MindSpore Science Team
---

# Overview

MODNet (Material Optimal Descriptor Network) is a supervised ML framework for learning material properties from composition or crystal structure. Optimized for limited datasets with top MatBench performance (7/13 tasks). Supports multi-task joint learning.

# Installation

```bash
# Create environment
conda create -n modnet python=3.9
conda activate modnet

# Install from PyPI
pip install modnet

# Development install
git clone https://github.com/ppdebreuck/modnet
cd modnet
pip install -r requirements.txt
pip install -e .
```

# Quick Start

```python
from modnet.preprocessing import MODData
from modnet.models import MODNetModel

# Create MODData from compositions and targets
data = MODData(materials=structures,
               targets=targets,
               target_names=["band_gap"])
data.featurize()

# Split data
train, test = data.split([0.8, 0.2])

# Train model
model = MODNetModel([[["band_gap"]]])
model.fit(train)

# Predict
predictions = model.predict(test)
```

# When to Use This Skill

Use MODNet when you need to:

- Predict materials properties from **composition OR structure** (flexible input)
- Work with **limited datasets** (optimized for small data regimes)
- Learn **multiple properties jointly** (multi-task learning improves performance)
- Achieve strong baseline performance with minimal tuning
- Leverage pretrained models for transfer learning
- Benchmark against MatBench leaderboard

**Consider alternatives when:**
- Large datasets are available (>100k samples) - deep learning models may excel
- You need uncertainty quantification - consider ensemble methods
- Real-time predictions are required - consider lighter models

# Key Features

## Optimal Feature Selection
- Automatic descriptor selection from 1000+ features
- Genetic algorithm optimization for feature subsets
- Composition and structure-based features via matminer

## Neural Network Architecture
- Multi-layer feedforward network
- Bayesian optimization for hyperparameters
- Cross-validation with early stopping

## Multi-Task Learning
- Joint learning of correlated properties
- Shared feature representations improve small dataset performance
- Pretrained models available for refractive index and thermodynamics

## MatBench Integration
- Top performance on 7/13 MatBench tasks (as of 11/2021)
- Reproducible benchmarking framework
- Cross-validation support

# Common Use Cases

## Composition-Based Prediction
```python
from modnet.preprocessing import MODData
data = MODData(compositions=formulas, targets=properties)
data.featurize()
```

## Structure-Based Prediction
```python
from modnet.preprocessing import MODData
data = MODData(structures=structures, targets=properties)
data.featurize()
```

## Multi-Property Learning
```python
# Learn band gap and formation energy together
data = MODData(structures=structures,
               targets=[band_gaps, formation_energies],
               target_names=["band_gap", "formation_energy"])
model = MODNetModel([[["band_gap"], ["formation_energy"]]])
```

## Using Pretrained Models
```python
from modnet.models import MODNetModel
model = MODNetModel.load("refractive_index_model")
predictions = model.predict(new_data)
```

# Best Practices

## Data Preparation
- Clean structures before featurization (use pymatgen Structure.from_sites)
- Remove duplicate entries with conflicting targets
- Normalize targets for multi-task learning
- Use k-fold cross-validation for robust estimates

## Feature Engineering
- Let MODNet auto-select features; manual selection rarely helps
- Use `n_jobs` parameter for parallel featurization
- Cache featurized data to avoid recomputation

## Hyperparameter Tuning
- Start with default settings; they work well for most cases
- Use `num_classes` for classification tasks
- Adjust `n_hidden_layers` and `n_neurons` for complexity

## Model Evaluation
- Report cross-validated metrics with uncertainty
- Compare against simple baselines (dummy regressor)
- Analyze feature importance for interpretability

# Troubleshooting

## Common Issues

### Featurization errors
- Check structure validity: `structure.is_valid`
- Ensure consistent oxidation states for composition features
- Update matminer version if features are deprecated

### Slow training
- Reduce `n_jobs` if memory constrained
- Use subset of features: `data.feature_selection(n_features=100)`
- Enable early stopping

### Poor multi-task performance
- Verify target correlations; uncorrelated tasks may hurt
- Normalize targets to similar scales
- Use task-specific weighting

### Overfitting on small datasets
- Increase regularization
- Reduce model capacity
- Use pretrained models with fine-tuning

# Resources

- GitHub: https://github.com/ppdebreuck/modnet
- Documentation: https://modnet.readthedocs.io
- Paper: De Breuck et al., npj Comput Mater 7, 83 (2021)
- Language: Python
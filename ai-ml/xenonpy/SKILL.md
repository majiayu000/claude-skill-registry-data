---
name: xenonpy
description: Python library implementing machine learning tools for materials informatics. Use when computing materials descriptors, using pretrained models, or performing transfer learning for property prediction.
metadata:
    skill-author: MindSpore Science Team
---

## Overview

XenonPy is a comprehensive Python library for materials informatics with machine learning tools, materials descriptors, pretrained models, and transfer learning capabilities. It includes access to over 140,000 pretrained models via XenonPy.MDL and supports Bayesian molecular design with the iQSPR algorithm.

# XenonPy

Comprehensive Python library for materials informatics with ML tools, descriptors, pretrained models, and transfer learning capabilities.

## Installation

```bash
pip install xenonpy
```

From source:
```bash
git clone https://github.com/yoshida-lab/XenonPy
pip install .
```

Via Docker:
```bash
docker pull yoshidalab/xenonpy:latest
docker run -it yoshidalab/xenonpy
```

## Quick Start

```python
from xenonpy.descriptor import Compositions, Structures
from xenonpy.model import ModelLibrary

# Generate composition descriptors
desc = Compositions().featurize(['NaCl', 'SiO2'])

# Generate structure descriptors
desc = Structures().featurize(structures)

# Access pretrained models (XenonPy.MDL)
library = ModelLibrary()
models = library.get_models(property='thermal_conductivity')
```

## Key Features

- **Descriptors**: Compositional and structural features
- **XenonPy.MDL**: 140,000+ pretrained models
- **Transfer Learning**: Shotgun transfer for limited data
- **Database Interface**: Public materials databases
- **Bayesian Design**: iQSPR molecular design algorithm

## Descriptor Types

- 0D: Atomic/ionic radii, electronegativity, etc.
- 1D: Bond lengths, coordination numbers
- 2D: Topological indices, connectivity
- 3D: Radial distribution, angular features

## Common Use Cases

- Computing materials descriptors for ML
- Property prediction with limited data
- Transfer learning for materials design
- Bayesian molecular design

# When to Use This Skill

- Generating compositional and structural descriptors for ML
- Accessing 140,000+ pretrained models from XenonPy.MDL
- Implementing transfer learning (shotgun transfer) for small datasets
- Bayesian molecular design with iQSPR algorithm
- Property prediction across materials domains

# Best Practices

- Use pretrained models as starting point for fine-tuning
- Apply shotgun transfer when target data is limited
- Leverage XenonPy.MDL for property-specific model selection
- Combine composition and structure descriptors for best results
- Use Docker for reproducible environment setup

# Resources

- GitHub: https://github.com/yoshida-lab/XenonPy
- Docs: https://xenonpy.readthedocs.io
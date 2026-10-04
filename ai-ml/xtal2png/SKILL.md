---
name: xtal2png
description: Encode/decode crystal structures to/from PNG images. Use when applying image-based ML models (GANs, diffusion models) to crystal structure prediction or generation.
metadata:
    skill-author: MindSpore Science Team
---

# xtal2png

## Overview

xtal2png encodes/decodes crystal structures to/from grayscale PNG images. This QR-code-like representation enables direct use of image-based ML models (GANs, VAEs, diffusion models) for crystal structure tasks.

## Installation

```bash
# Conda (recommended)
conda create -n xtal2png -c conda-forge xtal2png m3gnet
conda activate xtal2png

# PyPI
pip install xtal2png
```

## Quick Start

```python
from xtal2png import XtalConverter, example_structures

# Encode structures to PNG
xc = XtalConverter(relax_on_decode=False)
data = xc.xtal2png(example_structures, show=True, save=True)

# Decode PNG back to structures
decoded_structures = xc.png2xtal(data, save=False)

# With surrogate DFT relaxation
xc_relax = XtalConverter(relax_on_decode=True)
relaxed = xc_relax.png2xtal(data)
```

## CLI Usage

```bash
# Encode CIF files to PNG
xtal2png --encode --path structure.cif --save-dir output/

# Decode PNG to CIF
xtal2png --decode --path structure.png --save-dir output/
```

## Key Capabilities

### Structure Encoding
- 64x64 grayscale PNG images
- Captures lattice, sites, chemistry
- Max 52 sites per structure

### Structure Decoding
- Reconstruct from PNG
- Optional M3GNet relaxation

### Model Integration
- GANs, VAEs, diffusion models
- CNN-based analysis

## Use Cases

- Image-based ML for crystals
- Generative modeling
- Structure classification
- Transfer learning

# When to Use This Skill

- Applying image-based ML models to crystal structure tasks
- Using GANs, VAEs, or diffusion models for crystal generation
- Encoding structures as PNG for CNN-based analysis
- Transfer learning from image models to materials domain
- Converting between structure and image representations

# Best Practices

- Use `relax_on_decode=True` with M3GNet for relaxed structures
- Limit to 52 atoms per structure for encoding
- Validate decoded structures with pymatgen StructureMatcher
- Use CLI for batch encoding/decoding operations
- Test reconstruction quality before ML model training

# Resources

- GitHub: https://github.com/sparks-baird/xtal2png
- Documentation: https://xtal2png.readthedocs.io
- Colab: https://colab.research.google.com/github/sparks-baird/xtal2png
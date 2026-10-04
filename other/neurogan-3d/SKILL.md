---
name: neurogan-3d
description: >
  NeuroGAN-3D methodology for high-fidelity 3D generative super-resolution of
  resting-state fMRI (rs-fMRI) spatial maps. Uses a GAN architecture to enhance
  spatial resolution of volumetric functional brain network maps, enabling more
  precise localization of functional units, reliable brain parcellation, and
  detection of subtle spatially-specific neurobiological alterations. Use when
  working with rs-fMRI super-resolution, volumetric brain map enhancement,
  generative models for neuroimaging, functional connectivity resolution
  improvement, or 3D GAN-based medical imaging. Triggers: NeuroGAN, fMRI
  super-resolution, 3D generative neuroimaging, spatial resolution enhancement,
  volumetric brain maps, rs-fMRI enhancement, GAN brain network.
  arXiv: 2605.08373 (Esfahani et al., 2026).
---

# NeuroGAN-3D: High-Fidelity 3D Generative Super-Resolution for fMRI

Enhances the spatial resolution of resting-state fMRI (rs-fMRI) spatial maps
using a generative adversarial network tailored to volumetric neuroimaging
computational demands.

## Problem Statement

Spatial resolution of rs-fMRI-derived spatial maps determines the ability to:
- Localize functional units with precision
- Perform reliable brain parcellation
- Detect subtle, spatially-specific neurobiological alterations (development, aging, disease)

Existing super-resolution methods are not optimized for volumetric neuroimaging
or fail to capture fine-grained spatial patterns in functional connectivity maps.

## Architecture

### Generator Network
```
Low-Res 3D fMRI volume → Encoder → Latent representation → Decoder → High-Res 3D volume
```
- 3D convolutional encoder capturing spatial structure
- Residual learning for high-frequency details
- Volumetric upsampling layers (3D transposed convolutions)

### Discriminator Network
```
High-Res 3D volume (real/generated) → 3D CNN → Real/Fake classification
```
- 3D convolutional discriminator evaluating spatial realism
- Patch-based discrimination for localized quality assessment

## Key Contributions

1. **First 3D GAN specifically designed for rs-fMRI spatial maps**
2. **Significantly outperforms conventional interpolation baselines** in preserving
   fine-grained spatial patterns of intrinsic functional networks
3. **Preserves biologically meaningful connectivity patterns** while enhancing
   spatial resolution
4. **Enables downstream analysis** at higher effective resolution

## Implementation Pattern

```python
import torch
import torch.nn as nn

class Generator3D(nn.Module):
    def __init__(self, in_channels, out_channels, base_filters=32):
        super().__init__()
        # Encoder
        self.enc = nn.Sequential(
            nn.Conv3d(in_channels, base_filters, 3, padding=1),
            nn.LeakyReLU(0.2),
            nn.Conv3d(base_filters, base_filters*2, 3, stride=2, padding=1),
            nn.LeakyReLU(0.2),
            nn.Conv3d(base_filters*2, base_filters*4, 3, stride=2, padding=1),
            nn.LeakyReLU(0.2),
        )
        # Decoder with upsampling
        self.dec = nn.Sequential(
            nn.ConvTranspose3d(base_filters*4, base_filters*2, 4, stride=2, padding=1),
            nn.ReLU(),
            nn.ConvTranspose3d(base_filters*2, base_filters, 4, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv3d(base_filters, out_channels, 3, padding=1),
        )

    def forward(self, x):
        return self.dec(self.enc(x))
```

## Training Considerations

- Use perceptual loss + adversarial loss for preserving biological structure
- Consider cycle consistency for validation
- Evaluate with both image quality metrics and downstream FC analysis
- Validate preserved connectivity patterns against ground truth (when available)

## Datasets and Validation

- Tested on rs-fMRI spatial maps
- Evaluated against conventional interpolation baselines (trilinear, bicubic)
- Measured by spatial fidelity metrics and preservation of functional network patterns

## Activation Keywords

- neurogan-3d, fMRI super-resolution, 3D GAN neuroimaging, volumetric brain maps,
  rs-fMRI enhancement, spatial resolution fMRI, generative super-resolution brain,
  functional map upsampling, GAN neuroimaging

---
name: cv-slice-as-channel-2d-cnn
description: Resample a 3D medical volume to a fixed depth N (e.g. 32) and feed the N slices as input *channels* to a 2D CNN with `in_chans=N` instead of using a 3D conv backbone — gets the volumetric context for a fraction of the memory and lets you use any timm 2D pretrained model
---

## Overview

3D CNNs are memory hungry, train slowly, and lack pretrained weights. For many volumetric tasks (RSNA Aneurysm Detection, RSNA Cervical Spine, brain CTA panels) you can collapse the depth dimension into the channel dimension: zoom the volume to a fixed `(N, H, W)` shape, transpose to `(H, W, N)`, and feed it to a 2D CNN created with `timm.create_model(..., in_chans=N)`. The model sees all N slices simultaneously per spatial position and learns inter-slice features through its 2D convs. You give up some explicit Z-axis structure but gain ImageNet-pretrained weights, smaller model, faster training, and the option to use any 2D backbone (EfficientNetV2, ConvNeXt, Swin).

## Quick Start

```python
import numpy as np
from scipy import ndimage
import timm
import torch

def to_slice_channels(volume, depth=32, h=384, w=384):
    z = (depth/volume.shape[0], h/volume.shape[1], w/volume.shape[2])
    v = ndimage.zoom(volume, z, order=1)  # (depth, h, w)
    return v.astype(np.float32) / 255.0   # use as channel-first directly

model = timm.create_model('tf_efficientnetv2_s',
                          num_classes=14, in_chans=32, pretrained=True)
x = torch.from_numpy(to_slice_channels(volume))[None]  # (1, 32, 384, 384)
logits = model(x)  # one forward pass for the whole volume
```

## Workflow

1. Pick a fixed depth N — 16/24/32 are sweet spots for memory vs. signal
2. Resample every series to `(N, H, W)` with linear (or trilinear) zoom; pad/crop edges
3. Build the 2D backbone with `in_chans=N` — timm initializes the new conv1 by averaging the 3 ImageNet channels and tiling
4. Train as a normal 2D classifier; one forward per series, one loss per series
5. For TTA, augment the (H, W) plane jointly across all channels — never permute the channel axis
6. At inference, single forward gives all volume-level predictions

## Key Decisions

- **N must be fixed at training and inference**: variable depth breaks `in_chans`.
- **Linear zoom is fine**: cubic adds little for medical CT/MR and is slower.
- **timm auto-handles `in_chans` weight init**: it averages the RGB pretrained conv1 and replicates — usually better than random for the new channels.
- **vs. 3D CNN**: trades explicit Z modeling for faster training, ImageNet priors, and smaller models. For tasks where Z-context is dominant (long bones), use 3D or BiGRU stack instead.
- **Don't normalize per-channel**: per-volume normalization is correct because the channels share intensity scale.
- **Combine with depth-axis augmentation**: random Z-crop and Z-flip (where label-safe) are cheap regularizers.

## References

- [RSNA2025 32ch img infer LB 0.69 share](https://www.kaggle.com/code/yamitomo/rsna2025-32ch-img-infer-lb-0-69-share)

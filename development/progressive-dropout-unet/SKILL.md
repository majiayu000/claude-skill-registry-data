---
name: cv-progressive-dropout-unet
description: Apply lower dropout in shallow/final U-Net layers and higher dropout in deep layers to preserve spatial detail while regularizing abstract features
---

# Progressive Dropout in U-Net

## Overview

Uniform dropout across all U-Net layers either under-regularizes deep layers or over-regularizes shallow ones. Progressive dropout uses lower rates (e.g., 0.25) in early encoder blocks and final decoder blocks where spatial detail matters, and higher rates (e.g., 0.5) in deep/bottleneck layers where features are abstract and prone to overfitting.

## Quick Start

```python
from keras.layers import *

def build_unet(input_layer, filters=16, dropout=0.5):
    # Encoder: progressive dropout
    c1 = conv_block(input_layer, filters)
    p1 = Dropout(dropout / 2)(MaxPooling2D((2, 2))(c1))    # 0.25

    c2 = conv_block(p1, filters * 2)
    p2 = Dropout(dropout)(MaxPooling2D((2, 2))(c2))         # 0.50

    c3 = conv_block(p2, filters * 4)
    p3 = Dropout(dropout)(MaxPooling2D((2, 2))(c3))         # 0.50

    c4 = conv_block(p3, filters * 8)
    p4 = Dropout(dropout)(MaxPooling2D((2, 2))(c4))         # 0.50

    # Bottleneck
    bn = conv_block(p4, filters * 16)

    # Decoder: mirror progressive dropout
    u4 = Dropout(dropout)(concatenate([Conv2DTranspose(
        filters * 8, (3, 3), strides=(2, 2), padding='same')(bn), c4]))
    # ... more decoder layers ...
    u1 = Dropout(dropout / 2)(concatenate([Conv2DTranspose(
        filters, (3, 3), strides=(2, 2), padding='same')(d2), c1]))

    return Conv2D(1, (1, 1), activation='sigmoid')(conv_block(u1, filters))
```

## Workflow

1. Set base dropout rate (e.g., 0.5)
2. Apply half rate at first encoder block and last decoder block
3. Apply full rate at all deeper layers
4. Place dropout after pooling (encoder) and after concatenation (decoder)

## Key Decisions

- **Half at edges**: shallow layers capture fine spatial details that dropout would destroy
- **Full at depth**: deep features are more redundant and benefit from stronger regularization
- **After pooling, not after conv**: avoids zeroing spatial features right before skip connections
- **Typical rates**: 0.25 shallow / 0.5 deep for datasets with < 5000 images

## References

- [U-net, dropout, augmentation, stratification](https://www.kaggle.com/code/phoenigs/u-net-dropout-augmentation-stratification)
- [U-net with simple ResNet Blocks (Forked)](https://www.kaggle.com/code/aerdem4/u-net-with-simple-resnet-blocks-forked)

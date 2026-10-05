---
name: cv-snapshot-cosine-ensemble
description: Cyclic cosine annealing LR that produces M diverse snapshots from a single training run for free ensembling
---

## Overview

Snapshot ensembling runs cosine LR cycles during a single training pass. Each cycle converges to a different minimum, giving M diverse models for the cost of training one. Combined with SWA or simple prediction averaging, this provides cheap ensemble diversity without M training runs.

## Quick Start

```python
import numpy as np
from keras.callbacks import LearningRateScheduler, ModelCheckpoint

class SnapshotCallbackBuilder:
    def __init__(self, nb_epochs, nb_snapshots, init_lr=0.1):
        self.T = nb_epochs
        self.M = nb_snapshots
        self.alpha_zero = init_lr

    def _cosine_anneal(self, epoch):
        cos_inner = np.pi * (epoch % (self.T // self.M)) / (self.T // self.M)
        return float(self.alpha_zero / 2 * (np.cos(cos_inner) + 1))

    def get_callbacks(self, model_prefix='snap'):
        return [
            ModelCheckpoint(f'{model_prefix}_best.h5', monitor='val_loss',
                            save_best_only=True),
            LearningRateScheduler(self._cosine_anneal),
        ]

# Usage: 50 epochs, 5 snapshots, init_lr=1e-3
builder = SnapshotCallbackBuilder(nb_epochs=50, nb_snapshots=5, init_lr=1e-3)
model.fit(..., epochs=50, callbacks=builder.get_callbacks('run1'))
```

## Workflow

1. Choose total epochs T and number of snapshots M (cycle length = T/M)
2. LR follows cosine schedule within each cycle, restarting to `init_lr` at cycle start
3. Save model weights at the end of each cycle (when LR hits minimum)
4. At inference, average predictions from all M snapshots
5. Optionally combine with SWA by averaging weights of the final few snapshots

## Key Decisions

- **M value**: 3-5 snapshots. More snapshots means shorter cycles and less convergence per snapshot.
- **init_lr**: Higher than normal (start of each cycle hits this). Typical 1e-3 → 1e-1 depending on model.
- **Cycle length**: T/M epochs — ensure each cycle has enough time to converge meaningfully.
- **vs. checkpoint ensemble**: Snapshot ensemble is more diverse because each cycle explores new minima via the LR restart.

## References

- [Nested Unet with EfficientNet Encoder](https://www.kaggle.com/code/meaninglesslives/nested-unet-with-efficientnet-encoder)

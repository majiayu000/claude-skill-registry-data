---
name: nlp-cyclical-lr-triangular
description: Cyclical learning rate (CLR) Keras callback that oscillates LR between base and max each batch for faster convergence
---

## Overview

Cyclical Learning Rate (Smith 2017) avoids the manual LR tuning problem by sweeping between `base_lr` and `max_lr` repeatedly during training. The triangular pattern often converges faster than static LR and helps the model escape sharp minima. Three modes: `triangular` (constant amplitude), `triangular2` (amplitude halves each cycle), `exp_range` (amplitude decays exponentially).

## Quick Start

```python
import numpy as np
import keras.backend as K
from keras.callbacks import Callback

class CyclicLR(Callback):
    def __init__(self, base_lr=1e-3, max_lr=6e-3, step_size=2000,
                 mode='triangular', gamma=1.0):
        super().__init__()
        self.base_lr = base_lr
        self.max_lr = max_lr
        self.step_size = step_size
        self.mode = mode
        self.gamma = gamma
        self.iterations = 0.
        if mode == 'triangular':
            self.scale_fn = lambda x: 1.
        elif mode == 'triangular2':
            self.scale_fn = lambda x: 1 / (2. ** (x - 1))
        elif mode == 'exp_range':
            self.scale_fn = lambda x: gamma ** x

    def clr(self):
        cycle = np.floor(1 + self.iterations / (2 * self.step_size))
        x = np.abs(self.iterations / self.step_size - 2 * cycle + 1)
        return self.base_lr + (self.max_lr - self.base_lr) * max(0, 1 - x) * self.scale_fn(cycle)

    def on_train_begin(self, logs=None):
        K.set_value(self.model.optimizer.lr, self.base_lr)

    def on_batch_end(self, batch, logs=None):
        self.iterations += 1
        K.set_value(self.model.optimizer.lr, self.clr())

# Usage
clr = CyclicLR(base_lr=1e-3, max_lr=6e-3, step_size=2000, mode='triangular2')
model.fit(X, y, callbacks=[clr])
```

## Workflow

1. Run a LR range test first: train for ~1 epoch sweeping LR from 1e-7 to 1, plot loss. `base_lr` = start of decrease, `max_lr` = start of divergence.
2. Set `step_size` to 2-8 times `num_batches_per_epoch` (a full cycle = `2 * step_size` iterations).
3. Attach the callback to `model.fit` — LR updates every batch, no extra code required.
4. Mode `triangular2` decays amplitude over cycles for fine-tuning; `exp_range` for very long training.

## Key Decisions

- **step_size = 2-8 × epoch**: Smaller means more cycles per epoch, larger means longer exploration per minimum.
- **mode**: `triangular` for short runs, `triangular2` for longer ones (decays amplitude), `exp_range` when you want smooth decay.
- **vs. fixed LR**: Typically faster convergence and often comparable or better final accuracy with no LR tuning.

## References

- [Single RNN with 4 folds (CLR)](https://www.kaggle.com/code/shujian/single-rnn-with-4-folds-clr)

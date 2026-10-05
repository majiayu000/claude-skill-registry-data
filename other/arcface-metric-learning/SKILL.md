---
name: cv-arcface-metric-learning
description: ArcFace angular margin loss layer for learning discriminative embeddings — used in image retrieval, product matching, and face recognition
domain: cv
---

# ArcFace Metric Learning

## Overview

ArcFace adds an angular margin penalty to the softmax loss, pushing embeddings of the same class closer and different classes further apart in hyperspherical space. Train a CNN with an ArcMarginProduct head, then discard the head and use the penultimate layer as your embedding extractor. Produces highly discriminative features for retrieval tasks.

## Quick Start

```python
import tensorflow as tf
import math

class ArcMarginProduct(tf.keras.layers.Layer):
    def __init__(self, n_classes, s=30, m=0.50, **kwargs):
        super().__init__(**kwargs)
        self.n_classes = n_classes
        self.s = s
        self.cos_m = tf.math.cos(m)
        self.sin_m = tf.math.sin(m)
        self.th = tf.math.cos(math.pi - m)
        self.mm = tf.math.sin(math.pi - m) * m

    def build(self, input_shape):
        self.W = self.add_weight(shape=(input_shape[0][-1], self.n_classes),
                                 initializer='glorot_uniform', trainable=True)

    def call(self, inputs):
        X, y = inputs
        cosine = tf.matmul(tf.math.l2_normalize(X, axis=1),
                           tf.math.l2_normalize(self.W, axis=0))
        sine = tf.math.sqrt(1.0 - tf.math.pow(cosine, 2))
        phi = cosine * self.cos_m - sine * self.sin_m
        one_hot = tf.cast(tf.one_hot(y, depth=self.n_classes), dtype=phi.dtype)
        output = (one_hot * phi) + ((1.0 - one_hot) * cosine)
        return output * self.s

# Training
backbone = tf.keras.applications.EfficientNetB3(include_top=False, pooling='avg')
x = backbone.output
margin = ArcMarginProduct(n_classes=num_products, s=30, m=0.5)
output = margin([x, label_input])
model.fit(...)

# Inference: extract embeddings (discard ArcFace head)
embedder = tf.keras.Model(inputs=model.input[0], outputs=model.layers[-4].output)
embeddings = embedder.predict(test_data)
```

## Key Decisions

- **s (scale)**: 30 is standard; higher values sharpen the distribution
- **m (margin)**: 0.5 radians; increase for harder separation, decrease if training diverges
- **L2 normalize**: both features and weights must be normalized for angular margin to work
- **Discard head at inference**: the classification head is only needed during training

## References

- Source: [unsupervised-baseline-arcface](https://www.kaggle.com/code/ragnar123/unsupervised-baseline-arcface)
- Competition: Shopee - Price Match Guarantee

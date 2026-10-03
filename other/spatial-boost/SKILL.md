---
name: spatial-boost
title: "SpatialBoost: Language-Guided Spatial Reasoning for Enhanced Vision"
version: 0.0.3
engine: skillxiv-v0.0.3-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2603.22057
keywords: [Vision Language, Spatial Reasoning, Attention Mechanism, Fine-tuning]
description: "Inject spatial understanding into VLMs via language-guided multi-turn Chain-of-Thought reasoning over hierarchical spatial knowledge (pixel→object→scene). Implement dual-channel attention mechanism preserving pre-trained vision features while progressively incorporating dense 3D spatial information. Frozen original parameters prevent catastrophic forgetting; only new channel and mixture weights update. Maintains visual fidelity while enabling precise spatial reasoning (depth, relative positions, distances)."
---

## Component Identification

**Old Design (Standard VLM)**
- Vision encoder produces flat feature representations
- No explicit spatial reasoning capability
- Spatial understanding encoded implicitly in learned features
- Single-channel attention (no spatial-specific processing)

**New Design (SpatialBoost)**
Parallel attention channel dedicated to spatial understanding, merged with original via trainable mixture factor.

## Motivation & Problem Statement

While VLMs excel at semantic understanding, spatial reasoning—particularly depth, relative positions, and precise distances—remains challenging. Adding spatial capability requires injecting new knowledge without disrupting pre-trained visual understanding (catastrophic forgetting risk). Language-guided reasoning provides interpretable spatial knowledge while LLM decoders generate natural spatial descriptions.

## The Modification

**Hierarchical Spatial Reasoning via Multi-Turn Chain-of-Thought**

The framework structures spatial understanding across three levels, querying progressively more complex spatial relationships:

```
Level 1: Pixel-level depth queries
  Question: "What is the depth at position (x, y)?"
  or "Which point is closer: (x1, y1) or (x2, y2)?"
  Output: Absolute or relative depth predictions

Level 2: Object-level spatial relationships
  Question: "Is [Object A] on the left side of [Object B]?"
  or "What 3D bounding box contains [Object]?"
  Uses 3D bounding boxes to compute relationships
  Output: Spatial relationship confirmation/measurement

Level 3: Scene-level distance reasoning
  Question: "How far apart are [Object A] and [Object B]?"
  Synthesizes Level 1 & 2 results for precise distance
  Output: Absolute distance or relative positioning
```

Each turn builds on prior reasoning steps, creating interpretable chain-of-thought decomposition.

**Dual-Channel Attention Mechanism**

Standard vision encoder attention modified to preserve and extend knowledge:

```python
# Original frozen attention
Attn(x) = softmax(Q·K^T / √d) · V

# New spatial attention channel
Attn+(x) = softmax(Q+·K+^T / √d) · V+
# Where Q+, K+, V+ are trained on spatial tasks

# Merged output with learnable mixture
Attn_final(x) = α · Attn(x) + (1 - α) · Attn+(x)
# α is trainable mixture weight per layer
```

**Training Strategy:**

```python
# Forward pass
for layer in vision_encoder:
    # Original channel (frozen)
    x = layer.attention(x)

    # New spatial channel (trained)
    x_spatial = layer.attention_spatial(x)

    # Merge with learned weight
    α = layer.mixture_weight
    x = α * x + (1 - α) * x_spatial

# Backward pass: only α and spatial channel parameters update
# Original parameters remain frozen (stop_gradient=True)
```

This dual-channel design prevents catastrophic forgetting: pre-trained semantic features remain available while new spatial pathways develop.

## Architectural Enhancements

For each transformer layer in vision encoder:
1. Add parallel attention layer (Attn+)
2. Add trainable mixture weight (α)
3. Keep original attention frozen
4. Use LLM decoder to generate spatial descriptions

The frozen original channel ensures:
- Semantic understanding preserved
- Robust fallback if spatial reasoning fails
- Minimal parameter overhead (only α and new weights)

## Fine-tuning Configuration

**Frozen Components:**
- Original attention parameters (Q, K, V transformations)
- All other vision encoder layers remain frozen
- Pre-trained knowledge fully preserved

**Trainable Components:**
- Spatial attention parameters (Q+, K+, V+)
- Mixture weights (α) per layer
- LLM decoder parameters
- LoRA adapters if using parameter-efficient fine-tuning

**Loss Function:**
Combine three supervision signals:
- Spatial description accuracy (LLM output matches ground truth)
- Depth prediction accuracy (pixel-level depth supervision)
- Spatial relationship classification (object-level spatial labels)

## Performance Characteristics

**Spatial Understanding Improvement:**
- Pixel-level depth prediction accuracy
- Object-level spatial relationship F1
- Scene-level distance estimation MAE

**Preservation of Original Capability:**
- Semantic understanding maintained (original attention frozen)
- Visual fidelity preserved (no degradation on non-spatial tasks)
- Inference latency increased by dual-channel overhead (~15-20% per layer)

## Conditions of Applicability

**Works well when:**
- Spatial reasoning is critical (autonomous driving, robotics, scene understanding)
- Dense 3D annotations available (pixel-level depths, bounding boxes)
- Model capacity sufficient for dual-channel attention
- Base model is already high-quality (adding spatial to weaker models may not help)

**Less optimal when:**
- Pure semantic understanding is sufficient (no spatial reasoning needed)
- Limited 3D supervision available (difficult to train spatial channel)
- Inference latency critical (dual-channel adds overhead)
- Parameter count constraints (new channel increases model size)

## Drop-In Replacement Checklist

- [x] Plug-and-play with standard VLM architectures (adds attention channel)
- [x] No changes to downstream components (output format unchanged)
- [x] Inference compatible with existing VLM pipelines
- [x] Can warm-start from pre-trained vision encoder (frozen weights)
- [x] Spatial outputs optional (graceful degradation if spatial channel fails)
- [x] Works with any 3D annotation format (pixel depths, bounding boxes, distances)

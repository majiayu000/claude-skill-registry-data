---
name: minicpm-sala
title: "MiniCPM-SALA: Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2602.11761"
keywords: [Attention Mechanisms, Long Context, Hybrid Architecture, Training Efficiency, Token Scaling]
description: "Combine sparse attention (25% of layers) and linear attention (75% of layers) via strategic layer placement to handle 1M-token contexts with 75% training cost reduction. Hybrid positional encoding preserves long-range information while maintaining position awareness."
---

# MiniCPM-SALA: Hybrid Attention for Efficient Long-Context

## Problem Context

Standard Transformer attention faces two prohibitive bottlenecks: quadratic computational complexity O(N²) and linear KV-cache memory growth. For million-token contexts, these constraints make full-attention models impractical. Sparse attention alone sacrifices global information. Linear attention lacks fidelity for fine-grained dependencies. Training new models from scratch incurs enormous computational cost.

## Core Concept

MiniCPM-SALA achieves efficient long-context modeling through **strategic mixing of complementary attention mechanisms** in a 1:3 ratio. Rather than using uniform attention throughout, 25% of layers employ sparse attention (InfLLM-V2) for precise long-range modeling while 75% use linear attention (Lightning Attention) for O(N) efficiency.

The key insight: sparse and linear attention have complementary strengths. A learned layer selection mechanism determines optimal sparse placement, enabling continual training to convert pre-trained models instead of training from scratch (75% cost reduction).

## Architecture Overview

- **Hybrid Mixing Ratio**: 25% sparse attention (InfLLM-V2), 75% linear attention (Lightning Attention)
- **Layer Selection Algorithm**: Determines sparse placement rather than uniform interleaving
- **Hybrid Positional Encoding (HyPE)**: RoPE on linear layers only, removed from sparse layers
- **Architectural Stability**: First and last layers remain softmax attention
- **Five-Stage Training Pipeline**: HALO conversion → stable training → short-decay → long-decay → SFT
- **QK-Normalization and Output Gates**: Stabilize gradients and prevent attention sinks

## Implementation

The hybrid attention layer selection mechanism:

```python
def select_layer_types(num_layers, sparse_ratio=0.25):
    """
    Determine which layers get sparse vs linear attention.
    Uses strategic placement rather than uniform distribution.
    """
    num_sparse = int(num_layers * sparse_ratio)

    # Strategic placement: concentrate sparse layers where most useful
    # (typically middle layers for long-range dependencies)
    sparse_positions = []
    for i in range(num_sparse):
        pos = int((i + 1) * num_layers / (num_sparse + 1))
        sparse_positions.append(pos)

    layer_types = []
    for i in range(num_layers):
        if i in sparse_positions:
            layer_types.append('sparse')
        else:
            layer_types.append('linear')

    return layer_types
```

Hybrid Positional Encoding (HyPE) implementation:

```python
class HybridPositionalEncoding(nn.Module):
    """
    Apply RoPE selectively based on attention type.
    Linear layers get RoPE for position awareness.
    Sparse layers skip RoPE to preserve long-range information.
    """

    def __init__(self, dim, max_seq_len):
        super().__init__()
        self.rope = RotaryPositionEmbedding(dim, max_seq_len)

    def apply_to_linear_layer(self, x, positions):
        """Apply RoPE to linear attention layers."""
        return self.rope(x, positions)

    def apply_to_sparse_layer(self, x, positions):
        """Skip RoPE for sparse layers—preserve long-range information."""
        return x  # No position encoding for sparse attention
```

Five-stage training pipeline:

```python
def continual_training_pipeline(pretrained_model, data_config):
    """
    Convert pre-trained softmax model to hybrid architecture
    with minimal training cost (75% reduction vs training from scratch).
    """
    model = copy_and_convert_attention(pretrained_model, sparse_ratio=0.25)

    stages = [
        {
            'name': 'HALO Conversion',
            'tokens': 1.3e9,
            'seq_length': 512,
            'description': 'Initialize hybrid architecture'
        },
        {
            'name': 'Stable Training',
            'tokens': 314.6e9,
            'seq_length': 4096,
            'description': 'Coordinate hybrid components'
        },
        {
            'name': 'Short-Decay Training',
            'tokens': 1e12,
            'seq_length': 4096,
            'description': 'Learning rate decay with high-quality data'
        },
        {
            'name': 'Long-Decay Training',
            'tokens': 'variable',
            'seq_length': '4K→520K progressive',
            'description': 'Extend context progressively'
        },
        {
            'name': 'Supervised Fine-Tuning',
            'tokens': 'variable',
            'seq_length': '64K-140K',
            'description': 'Enhance reasoning capabilities'
        }
    ]

    for stage in stages:
        print(f"Stage: {stage['name']}")
        # Train with specified configuration
        model = train_stage(
            model,
            tokens=stage['tokens'],
            seq_length=stage['seq_length'],
            data=data_config[stage['name'].lower()]
        )

    return model
```

Attention layer implementation with QK-Normalization:

```python
class HybridAttentionLayer(nn.Module):
    def __init__(self, dim, attention_type='linear', num_heads=8):
        super().__init__()
        self.attention_type = attention_type
        self.num_heads = num_heads

        if attention_type == 'sparse':
            self.attn = SparseAttention(dim, num_heads)
        else:
            self.attn = LinearAttention(dim, num_heads)

        # QK-Normalization for stability
        self.q_norm = nn.LayerNorm(dim)
        self.k_norm = nn.LayerNorm(dim)

        # Output gate for controlling information flow
        self.output_gate = nn.Linear(dim, dim)

    def forward(self, x):
        # Normalize queries and keys
        q = self.q_norm(x)
        k = self.k_norm(x)

        # Apply attention
        attn_out = self.attn(q, k, x)

        # Apply output gate
        gate = torch.sigmoid(self.output_gate(attn_out))
        output = attn_out * gate

        return output
```

## Practical Guidance

**When to use**:
- Processing 100K+ token contexts
- Need inference speed improvements (3.5x reported)
- Converting existing pre-trained models
- Have compute budget for multi-stage training

**Key implementation decisions**:

1. **Sparse Ratio**: 25% sparse layers is optimal for most tasks. Test 15-30% for domain-specific tuning
2. **Layer Selection**: Strategic placement (middle layers) > uniform distribution
3. **Positional Encoding**: Always remove RoPE from sparse layers to preserve long-range
4. **Stability Measures**: QK-normalization critical for smooth training
5. **Training Cost**: Expect 75% cost reduction vs training from scratch

**Context extension schedule**:
- Start with 4K tokens (stable)
- Gradually increase to 520K over progressive stages
- Use learning rate decay as context extends

**Expected improvements**:
- 3.5x inference speedup
- 1M-token context support where full-attention fails
- 75% training cost reduction vs from-scratch training
- Maintains reasoning quality on reasoning-intensive tasks

**Debugging common issues**:
- Training instability → increase QK-norm, reduce learning rate
- Poor long-context performance → verify RoPE only on linear layers
- Attention sinks → enable output gates and increase gate regularization

## Reference

Hybrid attention through strategic sparse-linear mixing demonstrates that complementary mechanisms can be combined efficiently. Continual training from pre-trained models enables practical adoption without retraining from scratch, making 1M-token models feasible.

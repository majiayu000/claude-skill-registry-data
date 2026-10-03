---
name: casa-vl-fusion
title: "CASA: Cross-Attention via Self-Attention for Efficient VL Fusion"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2512.19535
keywords: [vision-language, cross-attention, efficient, multi-image, streaming]
description: "Replace token-insertion for fusing vision and language with efficient cross-attention that maintains separate text self-attention. Enables text tokens to attend images within local windows, preserves gist tokens from prior images, and maintains near-constant memory costs for streaming video—more practical than direct token insertion for resource-constrained applications."
---

## Overview

CASA revisits cross-attention (CA) as a practical alternative to direct token insertion for vision-language fusion. Token insertion becomes prohibitively expensive for high-resolution images and video, while CA offers efficient fusing with careful design. Five key design differences restore CA's competitiveness.

## Core Technique

The key insight is that cross-attention requires specific design choices to match or exceed token-insertion performance.

**Five Critical Design Differences:**

```python
# CASA architecture components
class CASAVisionLanguageModel:
    def __init__(self):
        # D1: Separate parameter layers for cross-attention
        self.text_self_attention = SelfAttentionLayer()
        self.cross_attention = CrossAttentionLayer()  # Not shared

        # D2: Joint text-image attention with local windows
        self.local_window_size = 128

        # D3: Reduced self-attention layers for CA layers
        self.num_self_attn = 16
        self.num_cross_attn = 8  # Replaces some self-attn

        # D4: Optional image token FFN updates
        self.image_ffn = FFNLayer()

        # D5: Visual history via gist tokens
        self.gist_tokens = None

    def forward(self, text_tokens, image_features, prev_gist=None):
        """
        Process text and image with CASA design principles.
        """
        # Maintain text self-attention for robustness
        text_hidden = self.text_self_attention(text_tokens)

        # Joint attention: text attends to image + preceding text
        # within local windows for efficiency
        attended = self.cross_attention(
            query=text_hidden,
            key_value_image=image_features,
            key_value_text=text_hidden,
            window_size=self.local_window_size
        )

        # Optional: update image embeddings via FFN
        image_features = self.image_ffn(image_features)

        # D5: Compress current image into gist tokens for next round
        gist_tokens = self.compute_gist(image_features)

        return attended, gist_tokens
```

**Gist Tokens for Visual History:**
Preserve compressed representations of past images without growing memory.

```python
def compute_gist_tokens(image_features, num_gist=8):
    """
    Compress image features into small number of gist tokens
    representing essential visual information for future frames.
    """
    # Average pooling over spatial dimensions
    spatial_mean = torch.mean(image_features, dim=(1, 2))  # [batch, hidden]

    # Project to gist token dimension
    gist = apply_projection(spatial_mean, output_dim=hidden_dim)

    # Take top-k tokens by importance score
    importance_scores = compute_importance(gist)
    gist_tokens = select_top_k(gist, importance_scores, k=num_gist)

    return gist_tokens
```

**Streaming Efficiency with Constant Memory:**
Unlike token insertion, KV cache scales with gist tokens, not image resolution.

```python
def streaming_forward(model, text_query, new_frame, history_gist):
    """
    Process new frame without storing all prior image tokens.
    Memory is O(gist_tokens), not O(image_resolution).
    """
    # Current image gist
    gist_current = model.compute_gist(new_frame)

    # Combine historical gists (constant size)
    gist_memory = history_gist + [gist_current]

    # Cross-attention over gists (efficient)
    output = model.cross_attention(
        query=text_query,
        key_value=gist_memory
    )

    # Memory complexity: O(num_frames * gist_tokens)
    # vs O(num_frames * image_resolution²) for token insertion

    return output, gist_memory
```

## When to Use This Technique

Use CASA when:
- Processing high-resolution images or video streams
- Memory bandwidth is constrained
- Multi-image conversations with streaming
- Token insertion memory costs are prohibitive

## When NOT to Use This Technique

Avoid this approach if:
- Single low-resolution image tasks (token insertion suffices)
- Fine-grained pixel-level understanding needed (lose spatial detail)
- Very few images/frames (token insertion memory manageable)

## Implementation Notes

The framework requires:
- Separate cross-attention and self-attention layer implementations
- Local windowing mechanism for joint text-image attention
- Gist token computation and compression
- Streaming inference pipeline for video

## Key Performance

- Near-constant memory costs for streaming video
- Comparable or superior performance to token insertion
- Efficient multi-image conversation support
- Strong baseline on various VLM benchmarks

## References

- Cross-attention as efficient alternative to token insertion
- Local windowing for joint text-image attention
- Gist tokens for visual memory compression
- Streaming-friendly architecture design

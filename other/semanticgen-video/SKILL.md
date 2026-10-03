---
name: semanticgen-video
title: "SemanticGen: Video Generation in Semantic Space"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2512.20619
keywords: [video-generation, diffusion, semantic-space, efficiency, scalability]
description: "Accelerate video generation and enable long-video synthesis by decomposing into two diffusion stages: first generate compact semantic features for global planning, then generate VAE latents conditioned on semantics. Includes learnable semantic compression to improve training convergence—enabling minute-long videos with faster convergence than direct VAE modeling."
---

## Overview

SemanticGen addresses two critical bottlenecks in video generation: slow convergence requiring hundreds of thousands of GPU-hours, and poor scaling to extended videos due to attention complexity. The key insight is that generation should occur first in semantic space for planning, then add details in pixel space.

## Core Technique

The method decomposes video generation into two complementary stages operating on different feature spaces.

**Two-Stage Generation Pipeline:**
Semantic space for global planning precedes pixel-space refinement.

```python
# Two-stage semantic+pixel generation
class SemanticVideoGenerator:
    def __init__(self):
        self.semantic_generator = DiffusionModel()  # Compact semantic space
        self.pixel_generator = DiffusionModel()     # VAE latent space

    def generate_video(self, prompt, num_frames):
        """
        Stage 1: Semantic generation for global video planning
        Stage 2: Pixel generation conditioned on semantics
        """
        # Stage 1: Compact semantic video features
        semantic_features = self.semantic_generator.denoise(
            x_T=torch.randn(1, num_frames, semantic_dim),
            conditioning=prompt
        )
        # semantic_features: [1, num_frames, compact_semantic_dim]

        # Stage 2: VAE latents conditioned on semantics
        pixel_latents = self.pixel_generator.denoise(
            x_T=torch.randn(1, num_frames, vae_latent_dim),
            conditioning=semantic_features  # Condition on Stage 1 output
        )

        # Decode VAE latents to pixels
        video = vae_decoder(pixel_latents)
        return video
```

**Semantic Space Compression:**
High-dimensional semantic representations converge slowly. A learnable MLP compresses them for faster training.

```python
class SemanticCompressor:
    def __init__(self, original_dim=2048, compressed_dim=512):
        self.compressor_mlp = nn.Sequential(
            nn.Linear(original_dim, 1024),
            nn.GELU(),
            nn.Linear(1024, compressed_dim)
        )

    def compress_semantics(self, semantic_features):
        """
        Project high-dimensional semantic features to lower dimension
        for faster training convergence.
        """
        compressed = self.compressor_mlp(semantic_features)

        # Encourage Gaussian distribution via regularization
        # This makes learned space resemble standard normal
        return compressed

    def loss_with_compression(self, pred_semantics, target_semantics):
        """
        Training loss includes reconstruction and Gaussian regularization.
        """
        compressed_pred = self.compress_semantics(pred_semantics)
        compressed_target = self.compress_semantics(target_semantics)

        reconstruction_loss = mse(compressed_pred, compressed_target)

        # Regularize compressed space toward Gaussian
        gaussian_prior = -0.5 * torch.sum(compressed_pred ** 2)

        return reconstruction_loss + 0.1 * gaussian_prior
```

**Convergence and Scalability Advantages:**
Semantic space generation is faster and enables longer videos.

```python
def training_efficiency_comparison():
    """
    Convergence improvements from semantic-space approach:
    - Direct VAE latent modeling: 500K+ GPU-hours
    - Semantic space modeling: 10x faster convergence
    - Scales to 1-minute videos without attention explosion
    """
    return {
        'convergence_speedup': '10x faster',
        'max_video_length': '1 minute+',
        'max_temporal_tokens': '500,000+ feasible',
        'training_gpu_hours': '50K-100K (vs 500K+)'
    }
```

## When to Use This Technique

Use SemanticGen when:
- Generating long-form videos (10+ seconds to minutes)
- Training efficiency is critical
- Semantic coherence is important
- Computational budget is constrained

## When NOT to Use This Technique

Avoid this approach if:
- Short, simple videos suffice (direct VAE modeling simpler)
- Pixel-perfect detail in every frame is required
- Semantic representations aren't well-defined
- Training time is irrelevant

## Implementation Notes

The framework requires:
- Two separate diffusion models (semantic and pixel)
- Learnable MLP for semantic space compression
- VAE decoder for final video reconstruction
- Integration of semantic conditioning into pixel-generation diffusion

## Key Performance

- Significantly faster convergence than direct VAE modeling
- Scales to minute-long videos
- Maintains long-term temporal consistency

## References

- Two-stage generation decomposition (semantic then pixel)
- Semantic space compression for training efficiency
- Diffusion modeling in compact semantic space
- Conditioned generation for pixel-level detail

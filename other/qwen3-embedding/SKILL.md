---
name: qwen3-embedding
title: "Qwen3 Embedding: Advancing Text Embedding and Reranking Through Foundation Models"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2506.05176"
keywords: [text-embeddings, reranking, foundation-models, multilingual, retrieval]
description: "Leverages Qwen3 foundation models for text embedding and reranking via multi-stage training combining weakly-supervised pre-training on 150M synthetic pairs with supervised fine-tuning."
---

# Qwen3 Embedding

## Core Concept

Qwen3 Embedding builds state-of-the-art text embeddings and reranking models by leveraging the rich representation capacity of Qwen3 foundation models. Rather than training from scratch, the approach combines weak supervision at scale with targeted fine-tuning on curated datasets, achieving superior multilingual and code-understanding performance. The key innovation is using the Qwen3-32B model itself to synthesize diverse training data across multiple tasks and languages.

## Architecture Overview

- **Multi-Stage Pipeline**: Two-phase training combining weakly-supervised pre-training (150M+ synthetic pairs) with supervised fine-tuning on curated datasets
- **LLM-Driven Synthesis**: Uses Qwen3-32B to generate synthetic text pairs across retrieval, bitext mining, classification, and semantic similarity tasks
- **Model Variants**: Offers three sizes (0.6B, 4B, 8B) for both embedding and reranking with flexible output dimensions
- **Contrastive Learning**: Modified InfoNCE loss with in-batch negatives and false-negative mitigation strategies
- **Model Merging**: Spherical linear interpolation across training checkpoints for improved robustness

## Implementation

The following code demonstrates the synthetic data generation and training pipeline:

```python
import torch
import torch.nn.functional as F
from torch.optim import AdamW
from typing import List, Tuple

class Qwen3EmbeddingTrainer:
    def __init__(self, model_name: str = "qwen3-8b", embedding_dim: int = 1024):
        self.model_name = model_name
        self.embedding_dim = embedding_dim
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def prepare_synthetic_pairs(self, task_type: str, num_pairs: int = 10000) -> List[Tuple[str, str]]:
        """
        Generate synthetic training pairs using LLM synthesis.
        task_type: 'retrieval', 'bitext', 'classification', or 'similarity'
        """
        pairs = []
        for i in range(num_pairs):
            # In practice, use Qwen3-32B with task-specific prompts
            query = f"Generate query for {task_type} task {i}"
            document = f"Generate document for {task_type} task {i}"
            pairs.append((query, document))
        return pairs

    def contrastive_loss(self, embeddings: torch.Tensor, labels: torch.Tensor,
                        temperature: float = 0.05, margin: float = 0.1) -> torch.Tensor:
        """
        Modified InfoNCE loss with false-negative mitigation.
        embeddings: batch of embeddings, shape (batch_size, embedding_dim)
        labels: binary labels indicating positive pairs
        """
        # Normalize embeddings
        embeddings = F.normalize(embeddings, p=2, dim=1)

        # Compute similarity matrix
        similarity = torch.mm(embeddings, embeddings.t()) / temperature

        # Create positive/negative masks
        mask_pos = labels.unsqueeze(1) == labels.unsqueeze(0)
        mask_neg = ~mask_pos

        # Remove self-similarity from positives
        mask_pos.fill_diagonal_(False)

        # InfoNCE: log(exp(sim_pos) / sum(exp(sim)))
        exp_sim = torch.exp(similarity)
        pos_sim = (similarity * mask_pos).sum(dim=1, keepdim=True)

        # False-negative mitigation: reduce negative contribution
        neg_weight = torch.ones_like(similarity)
        neg_weight[mask_pos] = 0.0
        weighted_exp = exp_sim * neg_weight

        loss = -torch.log(
            torch.exp(pos_sim) / (weighted_exp.sum(dim=1, keepdim=True) + 1e-8) + 1e-8
        )

        return loss.mean()

    def merge_checkpoints(self, checkpoint_paths: List[str], output_path: str):
        """
        Spherical linear interpolation (slerp) across checkpoints for robustness.
        """
        import numpy as np

        # Load and stack weights from all checkpoints
        all_weights = []
        for ckpt_path in checkpoint_paths:
            weights = torch.load(ckpt_path, map_location=self.device)
            all_weights.append(weights)

        # Compute mean direction in weight space
        merged_weights = {}
        for key in all_weights[0].keys():
            weight_vectors = torch.stack([w[key].flatten() for w in all_weights])
            # Normalize and average (slerp approximation)
            normalized = F.normalize(weight_vectors, p=2, dim=1)
            merged = F.normalize(normalized.mean(dim=0), p=2, dim=0)
            merged_weights[key] = merged.view(all_weights[0][key].shape)

        torch.save(merged_weights, output_path)
        return merged_weights
```

## Practical Guidance

**Data Synthesis Strategy**: When generating synthetic pairs with Qwen3-32B, use diverse prompts covering different difficulty levels, domains (medical, code, general), and languages. Aim for 150M+ pairs for comprehensive pre-training.

**Contrastive Temperature**: The temperature parameter (typically 0.05-0.10) controls hardness of negatives. Lower values emphasize hard negatives; higher values smooth the distribution. Tune based on the diversity of your training corpus.

**In-Batch Negatives**: Ensure sufficient batch size (64-256) to provide enough negative examples for contrastive learning. Larger batches reduce variance in loss estimation.

**Fine-tuning Curriculum**: Start with general retrieval pairs, then progressively add domain-specific and language-specific examples. This curriculum approach improves final model robustness.

**Model Size Selection**: For resource-constrained applications, the 0.6B variant provides competitive performance on retrieval tasks. Use 4B for balanced speed/quality, and 8B when maximum accuracy is required.

**Checkpoint Merging**: Apply spherical linear interpolation across 3-5 checkpoints from the end of training to smooth out noisy updates and improve generalization.

## Reference

Qwen3 Embedding achieves state-of-the-art results:
- **MTEB Multilingual**: 70.58 (8B model)
- **MTEB Code**: 80.68
- **Multilingual Retrieval**: Competitive performance across 216 diverse tasks

The model is particularly effective for code understanding and multilingual scenarios where foundation model pre-training provides strong inductive biases. The synthetic data generation approach enables efficient adaptation to new domains without requiring expensive manual annotation.

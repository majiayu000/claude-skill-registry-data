---
name: bottom-up-policy
title: "Bottom-up Policy Optimization: Internal Policies in LMs"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2512.19673
keywords: [reinforcement-learning, interpretability, layer-wise, reasoning, llm]
description: "Optimize language model policies layer-by-layer rather than monolithically to understand internal reasoning structure. Decompose models into per-layer and per-module policies via residual streams, analyze entropy patterns revealing exploration→convergence phases, and optimize layers sequentially—improving reasoning on math tasks by up to 4.69 points."
---

## Overview

Bottom-up Policy Optimization (BuPO) treats language models as compositional reasoning systems rather than monolithic policies. By analyzing internal layer policies via residual streams, the framework reveals that models naturally exhibit a universal structure: early layers explore solution spaces while top layers converge to predictions. Sequential optimization respects this structure.

## Core Technique

The key insight is that residual streams enable additive decomposition of layer and module policies.

**Internal Policy Decomposition:**
Define policies at different architectural levels using hidden states and the unembedding matrix.

```python
# Layer and module policy definition
class InternalPolicyDecomposition:
    def __init__(self, model):
        self.model = model
        self.num_layers = len(model.layers)
        self.unembedding = model.unembedding

    def layer_policy(self, layer_idx):
        """
        Define policy for individual layer via its residual contribution.
        Policy: hidden_state @ unembedding → logits
        """
        def pi_layer(residual_stream, target_idx):
            # Extract this layer's residual contribution
            layer_output = residual_stream[layer_idx]
            # Convert to logits via unembedding
            logits = layer_output @ self.unembedding.weight
            return logits
        return pi_layer

    def module_policy(self, layer_idx, module_type):
        """
        Define policy for individual module (attention vs FFN).
        Isolate each module's contribution to reasoning.
        """
        if module_type == 'attention':
            return lambda x: self.model.layers[layer_idx].self_attn(x)
        elif module_type == 'ffn':
            return lambda x: self.model.layers[layer_idx].mlp(x)
```

**Internal Policy Entropy Analysis:**
Entropy patterns reveal universal reasoning structure across models.

```python
def analyze_entropy_structure(model, dataset):
    """
    Measure entropy of each layer's policy across inputs.
    High entropy: exploration of solution space
    Low entropy: convergence to prediction
    """
    entropy_by_layer = {}

    for layer_idx in range(len(model.layers)):
        layer_entropies = []

        for batch in dataset:
            residual_streams = model.get_residual_streams(batch)
            layer_hidden = residual_streams[layer_idx]

            # Compute logits for this layer
            logits = layer_hidden @ model.unembedding.weight
            probs = softmax(logits)

            # Entropy of layer's policy
            entropy = -sum(probs * log(probs))
            layer_entropies.append(entropy)

        entropy_by_layer[layer_idx] = np.mean(layer_entropies)

    # Typical pattern:
    # - Early layers: high entropy (exploring)
    # - Middle layers: medium entropy
    # - Top layers: low entropy (converged)

    return entropy_by_layer
```

**Sequential Layer-by-Layer Optimization:**
Optimize layers in order, establishing better foundations for upper layers.

```python
def sequential_layer_optimization(model, dataset, target_task):
    """
    Optimize each layer sequentially, respecting natural reasoning structure:
    early layers → feature refinement
    top layers → final prediction
    """
    num_layers = len(model.layers)

    for layer_idx in range(num_layers):
        print(f"Optimizing layer {layer_idx}/{num_layers}")

        # Freeze all other layers
        for i in range(num_layers):
            for param in model.layers[i].parameters():
                param.requires_grad = (i == layer_idx)

        # Compute layer-specific advantage
        layer_advantages = []
        for batch in dataset:
            # Get baseline from frozen layers up to this point
            baseline = model.forward_until_layer(batch, layer_idx - 1)

            # Get predictions with this layer
            with_layer = model.forward_until_layer(batch, layer_idx)

            # Advantage: improvement from this layer
            advantage = reward(with_layer) - reward(baseline)
            layer_advantages.append(advantage)

        # PPO update only for this layer
        policy_loss = -mean(layer_advantages) * log_prob(model.layers[layer_idx])
        policy_loss.backward()

        # Update this layer only
        optimizer.step()
        optimizer.zero_grad()
```

## When to Use This Technique

Use Bottom-up Policy Optimization when:
- Reasoning tasks with interpretability requirements
- Math and coding problem-solving
- Understanding internal model structure is valuable
- Sequential optimization aligns with your hardware/training

## When NOT to Use This Technique

Avoid this approach if:
- Single monolithic policy is most efficient
- Sequential layer optimization adds unacceptable overhead
- Interpretability not required (end-to-end faster)
- Model architecture doesn't support residual stream analysis

## Implementation Notes

The framework requires:
- Access to residual streams at each layer
- Unembedding matrix for policy conversion
- Layer-wise gradient control and optimization
- Entropy analysis infrastructure for structure understanding

## Key Performance

- Improvements up to 4.69 points on mathematical reasoning (AIME24)
- Consistent gains across Qwen and Llama models
- Interpretable reasoning structure
- Foundation for further optimization strategies

## References

- Layer and module policy decomposition via residual streams
- Internal policy entropy analysis
- Sequential optimization respecting reasoning structure
- Universal exploration→convergence pattern across models

---
name: gaussian-grpo
description: "Gaussian Group Relative Policy Optimization (G²RPO) for multimodal RL training. Replaces linear scaling with distributional matching to ensure gradient equity across diverse tasks. Use when training multimodal models, balancing perception vs reasoning, or stabilizing RL across heterogeneous reward topologies. Keywords: G²RPO, Gaussian GRPO, multimodal RL, entropy shaping, response length shaping, GRPO, reinforcement learning."
---

# Gaussian GRPO Skill

## Description
Advanced RL training objective for multimodal large language models that ensures gradient equity across heterogeneous tasks through Gaussian distributional matching.

## Activation Keywords
- G²RPO
- Gaussian GRPO
- multimodal RL training
- entropy shaping
- response length shaping
- GRPO optimization
- gradient equity
- reward topology variance

## Tools Used
- `exec`: Run training scripts
- `read`: Load training configurations
- `write`: Save trained model checkpoints

## Key Concepts

### Gaussian Distributional Matching
Force advantage distribution to converge to N(0,1):
- Ensures inter-task gradient equity
- Mitigates heavy-tail outlier vulnerabilities
- Symmetric updates for positive/negative rewards

### Response Length Shaping
Dynamic control of reasoning chain length:
- Elicit extended chains for complex queries
- Enforce direct outputs for visual grounding
- Balance perception vs reasoning tradeoff

### Entropy Shaping
Bound model exploration zone:
- Prevent entropy collapse (over-confident)
- Prevent entropy explosion (under-confident)
- Tight bounds on exploration variance

## Workflow

### Step 1: Normalize Advantages
Transform advantages to standard normal distribution:
```python
advantages_normalized = (advantages - mean) / std
# Mathematically force convergence to N(0,1)
```

### Step 2: Apply Response Length Shaping
Dynamically adjust target length:
```python
if task_type == 'reasoning':
    target_length = extended_chain_length
else:  # visual grounding
    target_length = direct_output_length
```

### Step 3: Entropy Shaping
Bound exploration:
```python
entropy = compute_entropy(policy_probs)
entropy_loss = max(entropy, min_entropy) + min(entropy, max_entropy)
```

### Step 4: Combine Losses
```python
total_loss = grpo_loss + length_loss + entropy_loss
```

## Benefits

1. **Gradient equity**: Different tasks contribute equally
2. **Outlier robustness**: Heavy-tail rewards don't dominate
3. **Stability**: Symmetric positive/negative updates
4. **Balance**: Perception and reasoning coexist

## Resources

- Reference paper: arxiv:2604.08539
- Key innovation: N(0,1) advantage distribution
---
name: deep-search-hmc
title: "Deep Search with Hierarchical Meta-Cognitive Monitoring"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2601.23188"
keywords: [Search Agents, Meta-Cognitive Monitoring, Uncertainty Calibration, Anomaly Detection]
description: "Monitor search agent reasoning quality via hierarchical uncertainty detection. Fast consistency checks identify anomalies; slow experience-driven feedback provides corrections. Minimal overhead while catching misalignment."
---

# Hierarchical Meta-Cognitive Monitoring for Search

## Problem
Deep search agents can pursue incorrect trajectories for many steps before detection. Standard uncertainty metrics like token entropy are ambiguous—high entropy may reflect legitimate exploration rather than errors.

Most search improvement methods apply global interventions expensive across all steps. Fine-grained, targeted monitoring is needed.

## Core Concept
The system implements two monitoring layers: a fast consistency monitor checking every step, and a slow experience-driven monitor activated on anomalies. The fast monitor compares reasoning uncertainty against evidence uncertainty—high misalignment triggers slow monitoring.

Rather than treating entropy in isolation, the system calibrates reasoning entropy to external evidence entropy, distinguishing legitimate exploration from actual failures.

## Architecture Overview

- **Fast Consistency Monitor**: Per-step checks measuring entropy alignment
- **Searching Entropy (SE)**: Evidence diversity from retrieval results
- **Reasoning Entropy (RE)**: Model token prediction uncertainty
- **Calibration Function**: Compare expected vs. observed reasoning entropy
- **Slow Experience Monitor**: Activated on anomalies; retrieves past experiences
- **Corrective Feedback**: Context-aware suggestions from experience memory

## Implementation

### Step 1: Compute Searching and Reasoning Entropies
Measure evidence and reasoning uncertainty independently.

```python
def compute_searching_entropy(retrieved_results, embedding_model):
    """Compute semantic diversity of retrieved evidence."""
    # Embed retrieved results
    embeddings = [embedding_model.encode(r) for r in retrieved_results]

    # Cluster embeddings to measure semantic diversity
    distances = pairwise_distances(embeddings)
    avg_distance = distances.mean()

    # Higher average distance = higher entropy
    searching_entropy = avg_distance / np.linalg.norm(embeddings[0])

    return searching_entropy

def compute_reasoning_entropy(model_logits):
    """Compute model prediction uncertainty."""
    # Standard entropy over token distribution
    probs = F.softmax(model_logits, dim=-1)
    reasoning_entropy = -(probs * torch.log(probs + 1e-6)).sum()

    return reasoning_entropy
```

### Step 2: Fast Consistency Monitoring
Check entropy calibration at each search step.

```python
def fast_consistency_monitor(reasoning_entropy, searching_entropy, threshold=1.0):
    """Detect misalignment between reasoning and evidence entropy."""
    # Expected reasoning entropy given evidence diversity
    expected_re = searching_entropy * 0.8  # Empirical calibration

    # Anomaly detection: reasoning entropy >> expected
    deviation = reasoning_entropy - expected_re

    is_anomaly = deviation > threshold

    return is_anomaly, deviation
```

### Step 3: Slow Experience-Driven Monitoring
Retrieve and apply past experiences when anomalies detected.

```python
class ExperienceMemory:
    def __init__(self, embedding_model):
        self.success_experiences = []
        self.failure_experiences = []
        self.embedding_model = embedding_model

    def retrieve_relevant_experience(self, current_state, k=3):
        """Find similar past experiences."""
        current_embedding = self.embedding_model.encode(current_state)

        # Compute similarities to stored experiences
        all_experiences = self.success_experiences + self.failure_experiences
        similarities = [
            cosine_similarity(current_embedding, self.embedding_model.encode(exp['state']))
            for exp in all_experiences
        ]

        # Return top-k most similar
        top_indices = np.argsort(similarities)[-k:]
        return [all_experiences[i] for i in top_indices]

    def generate_correction(self, current_state, retrieved_experiences, correction_model):
        """Generate corrective action from past experiences."""
        context = f"Current state: {current_state}\n\n"
        context += "Similar past experiences:\n"
        for exp in retrieved_experiences:
            context += f"- {exp['description']}\n"

        correction = correction_model.generate(context)
        return correction
```

### Step 4: Hierarchical Monitoring Loop
Integrate fast and slow monitoring in search loop.

```python
def search_with_hmc(model, initial_query, experience_memory, max_steps=50):
    """Execute search with hierarchical meta-cognitive monitoring."""
    current_state = initial_query
    search_trajectory = []

    for step in range(max_steps):
        # Retrieve evidence
        retrieved = retrieve_top_k(current_state, k=5)

        # Generate reasoning
        model_output = model.generate(current_state)
        logits = model.get_logits(current_state)

        # Compute entropies
        se = compute_searching_entropy(retrieved)
        re = compute_reasoning_entropy(logits)

        # Fast monitoring
        is_anomaly, deviation = fast_consistency_monitor(re, se)

        if is_anomaly:
            # Slow monitoring activation
            state_representation = f"Query: {current_state}\nDeviation: {deviation}"
            similar_experiences = experience_memory.retrieve_relevant_experience(state_representation)
            correction = experience_memory.generate_correction(state_representation, similar_experiences)

            # Apply correction
            model_output = correction

        search_trajectory.append({
            'step': step,
            'state': current_state,
            'anomaly': is_anomaly,
            'output': model_output
        })

        current_state = model_output

    return search_trajectory
```

## Practical Guidance

### Hyperparameter Configuration

| Parameter | Value | Notes |
|-----------|-------|-------|
| Fast monitor threshold (τ) | 1.0 * std | Calibrate on clean runs |
| Entropy similarity margin | k-sigma | k=1 for 68% confidence |
| Experience retrieval k | 3-5 | Balance coverage and cost |
| Searching entropy normalization | Embedding dim | Scale to embedding space |
| Slow monitor overhead | 3-7% | Additional latency acceptable |

### When to Use

- Open-domain search agents (web search, knowledge graphs)
- Multi-step reasoning that can diverge undetected
- Systems requiring interpretability of divergence detection
- Agents with access to experience/memory repositories
- Long-horizon tasks where early errors compound

### When Not to Use

- Deterministic, single-path tasks
- Real-time systems where overhead is critical
- Agents without reliable experience storage
- Supervised environments with explicit rewards
- Tasks with short, bounded search horizons

### Common Pitfalls

1. **Entropy misinterpretation**: High reasoning entropy alone doesn't indicate failure. Calibration against evidence critical.
2. **Experience bias**: Over-reliance on experience memory for novel states. Mix experience with heuristic corrections.
3. **Threshold sensitivity**: Threshold calibration depends on domain. Validate on held-out searches.
4. **Correction quality**: Corrections from experience are only as good as memory. Regularly validate and filter.

## Reference
Deep Search with Hierarchical Meta-Cognitive Monitoring
https://arxiv.org/abs/2601.23188

---
name: steer2adapt
title: "Steer2Adapt: Dynamically Composing Steering Vectors for Efficient LLM Adaptation"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2602.07276"
keywords: [Activation Steering, Domain Adaptation, Bayesian Optimization, Semantic Subspace, Inference-Time Adaptation]
description: "Adapt LLMs efficiently by composing multiple pre-existing semantic steering vectors via Bayesian optimization, balancing adaptation gain and safety without retraining model parameters."
---

# Steer2Adapt: Dynamically Composing Steering Vectors for Efficient LLM Adaptation

## Problem Context

Existing activation steering approaches suffer from inflexibility. Single static directions cannot adapt across task variations; complex tasks requiring multiple coordinated capabilities cannot be captured by one vector; and vectors optimized for one task may harm performance on related tasks.

## Core Concept

Steer2Adapt shifts steering from discovering individual task-specific directions to dynamically composing multiple reusable semantic vectors. Rather than learning new steering vectors from scratch for each task, the method finds optimal linear combinations of pre-existing concept vectors within a domain-specific subspace.

## Architecture Overview

- **Semantic Subspace Construction**: Identify k behavioral concepts and extract corresponding steering vectors using representation engineering
- **Composed Vector Search**: Use Bayesian Optimization to find optimal coefficients balancing adaptation gain and safety
- **Inference-Time Application**: Inject composite steering vector into model activations without parameter updates

## Implementation

**Phase 1: Semantic Subspace Construction**

```python
def construct_semantic_subspace(domain, concepts=None):
    # Define behavioral concepts for domain
    # (e.g., Big Five traits for reasoning)
    if concepts is None:
        concepts = ['Openness', 'Conscientiousness', 'Extroversion',
                    'Agreeableness', 'Neuroticism']

    # Extract steering vectors via representation engineering
    vectors = []

    for concept in concepts:
        # Generate positive/negative exemplars
        positive = generate_examples(concept, valence='positive')
        negative = generate_examples(concept, valence='negative')

        # Compute activations
        pos_acts = get_activations(model, positive, layer=target_layer)
        neg_acts = get_activations(model, negative, layer=target_layer)

        # Derive steering vector as mean difference
        steering_vec = np.mean(pos_acts) - np.mean(neg_acts)
        vectors.append(steering_vec)

    # Stack into subspace matrix
    V = np.column_stack(vectors)  # d x k matrix

    return V, concepts
```

**Phase 2: Composed Vector Search via Bayesian Optimization**

```python
def find_optimal_composition(task_examples, semantic_subspace):
    V, concepts = semantic_subspace
    k = V.shape[1]

    def objective_function(coefficients):
        # Compose steering vector
        v_combined = V @ coefficients

        # Evaluate adaptation gain
        gains = []
        for example in task_examples:
            # Predict without steering
            logits_baseline = model(example, steering=None)
            pred_baseline = np.argmax(logits_baseline)

            # Predict with steering
            logits_steered = model(example,
                                   steering=v_combined)
            pred_steered = np.argmax(logits_steered)

            # Gain: 1 if fixed prediction, 0 if already correct
            gain = (pred_baseline != example.label and
                   pred_steered == example.label)
            gains.append(gain)

        adaptation_gain = np.mean(gains)

        # Safety penalty: penalize flips from correct to wrong
        penalties = []
        for example in task_examples:
            logits_baseline = model(example, steering=None)
            pred_baseline = np.argmax(logits_baseline)

            logits_steered = model(example, steering=v_combined)
            pred_steered = np.argmax(logits_steered)

            # Penalty: 1 if flipped from correct to wrong
            penalty = (pred_baseline == example.label and
                      pred_steered != example.label)
            penalties.append(penalty)

        safety_penalty = np.mean(penalties)

        # Composite objective
        objective = adaptation_gain - λ * safety_penalty
        return objective

    # Bayesian Optimization to find optimal coefficients
    from scipy.optimize import differential_evolution

    bounds = [(-1, 1) for _ in range(k)]
    result = differential_evolution(
        lambda α: -objective_function(α),
        bounds, seed=42, maxiter=50
    )

    optimal_coefficients = result.x
    return optimal_coefficients
```

**Phase 3: Inference-Time Application**

```python
def generate_with_steering(prompt, task_description,
                          semantic_subspace):
    V, concepts = semantic_subspace

    # Find optimal composition for this task
    # (using few examples from task)
    examples = get_task_examples(task_description, k=3)
    optimal_coeff = find_optimal_composition(
        examples, semantic_subspace
    )

    # Compose steering vector
    v_combined = V @ optimal_coeff

    # Generate with steering injection
    output = model.generate_with_steering(
        prompt, steering_vector=v_combined
    )

    return output
```

## Practical Guidance

**When to use**: Deploy for in-distribution adaptation tasks where you have a fixed domain with multiple related sub-tasks. Effective for few-shot adaptation without retraining.

**Concept selection**: Choose concepts relevant to your domain. For reasoning tasks, use epistemological traits (e.g., logical rigor, creative thinking). For dialogue, use social dimensions (e.g., helpfulness, formality).

**Subspace composition**: Start with 5–10 concepts; too few = limited expressiveness; too many = optimization becomes harder.

**Calibration data**: Optimize coefficients using 3–10 examples per task. More examples improve robustness; diminishing returns after ~20.

**Safety tuning**: Adjust λ (safety penalty weight) based on task criticality. Low λ (0.1–0.3) for benign tasks; high λ (0.7–1.0) for safety-critical applications.

## Reference

The method achieves efficient adaptation by reusing frozen semantic vectors across tasks, eliminating the need for parameter retraining. The safety-aware Bayesian optimization ensures that adaptation gains don't come at the cost of breaking correct predictions, enabling risk-averse deployment in production settings.

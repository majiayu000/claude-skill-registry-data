---
name: r-horizon-long-horizon-reasoning
title: "R-Horizon: How Far Can Your Large Reasoning Model Really Go in Breadth and Depth?"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2510.08189"
keywords: [reasoning, benchmark, long-horizon, query-composition, large-reasoning-models]
description: "Construct multi-step reasoning benchmarks with interdependent problems to evaluate and improve long-horizon reasoning in large reasoning models. Enables evaluation of reasoning depth and breadth beyond single-step tasks."
---

# R-Horizon: Evaluating and Improving Long-Horizon Reasoning

Large reasoning models show surprising limitations in extended reasoning chains. Current benchmarks focus on single-horizon tasks, missing critical evaluation of how well models handle multi-step interdependent problems or allocate thinking across multiple sub-tasks.

R-Horizon addresses this by constructing reasoning tasks where multiple problems depend on each other, creating true long-horizon reasoning scenarios. This reveals whether models can sustain reasoning quality across deep chains or whether they degrade as reasoning depth increases.

## Core Concept

The framework constructs multi-step reasoning problems through **query composition**: building dependent sub-problems where solutions to earlier steps inform later steps. This naturally extends single-horizon reasoning benchmarks into long-horizon evaluation suites.

Key insight: models need to not only reason deeply but allocate their reasoning budget efficiently across multiple interconnected sub-problems.

## Architecture Overview

- **Query Composition Engine**: Takes base reasoning problems and creates dependency chains
- **Controlled Depth Variation**: Generate problems at varying reasoning depths to test breadth and depth separately
- **Reward Integration**: Connects with Reinforcement Learning with Verified Rewards (RLVR) for both evaluation and training
- **Benchmark Reusability**: Creates persistent evaluation benchmarks across multiple reasoning models

## Implementation Steps

The core workflow involves three stages: problem generation, composition, and evaluation.

**Stage 1: Base Problem Selection**

Start with high-quality reasoning problems. For mathematical reasoning, extract problems from benchmarks like AIME or Math competition datasets:

```python
# Load base reasoning problems
base_problems = load_benchmark_problems(
    source='aime_2024',
    difficulty='high'
)

# Filter for composability
composable = [
    p for p in base_problems
    if can_create_dependency(p)
]
```

**Stage 2: Dependency Graph Construction**

Create chains where problem N+1 depends on solution to problem N. Build a dependency graph that represents the reasoning structure:

```python
def create_composition_chain(problems, chain_length=5):
    """
    Build a chain of problems where each depends on previous solution.
    """
    chain = []
    for i in range(chain_length):
        base = problems[i]
        if i == 0:
            chain.append(base)
        else:
            # Modify problem to require solution from problem i-1
            dependent = inject_dependency(base, chain[i-1])
            chain.append(dependent)
    return chain

# Create multiple chain depth levels
depth_3_chains = create_composition_chain(problems, chain_length=3)
depth_5_chains = create_composition_chain(problems, chain_length=5)
depth_8_chains = create_composition_chain(problems, chain_length=8)
```

**Stage 3: Evaluation with RLVR**

Evaluate models on composed problems and use results to train reasoning improvement:

```python
def evaluate_reasoning_chains(model, chains):
    """
    Test model on multi-step reasoning chains.
    Returns per-step accuracy to track reasoning degradation.
    """
    results = {
        'step_accuracy': [],
        'chain_completion': 0,
        'thinking_allocation': []
    }

    for chain in chains:
        step_results = []
        for step_idx, problem in enumerate(chain):
            response = model.generate(
                prompt=problem,
                max_thinking_tokens=8000
            )
            is_correct = verify_solution(response)
            step_results.append(is_correct)

        results['step_accuracy'].append(step_results)
        if all(step_results):
            results['chain_completion'] += 1

    return results
```

## Practical Guidance

**When to Use R-Horizon:**
- Evaluating whether large reasoning models truly handle long-horizon tasks
- Creating curriculum-based training where models progress from single to multi-step reasoning
- Identifying where reasoning models degrade in extended chains

**When NOT to Use:**
- Single-step problem solving where long-horizon complexity adds no value
- Domains without clear problem interdependencies (unrelated tasks)

**Hyperparameter Considerations:**

| Parameter | Typical Range | Guidance |
|-----------|---------------|----------|
| Chain Depth | 3-10 | Deeper chains reveal more limitations; 5-6 balances evaluation informativeness |
| Problem Difficulty | Easy to Hard | Mix difficulties to avoid ceiling/floor effects |
| Thinking Budget | 4000-16000 tokens | Allow sufficient reasoning tokens; 8000 is baseline |
| Composition Type | Sequential/Graph | Sequential most straightforward; graph captures realistic dependencies |

**Common Pitfalls:**
- Creating false dependencies that don't require genuine reasoning across steps
- Using problems that are too easy, masking actual reasoning limitations
- Insufficient thinking budget that prevents models from demonstrating capability
- Not validating intermediate solutions, missing cascading errors

## Reference

Based on the research at: https://arxiv.org/abs/2510.08189

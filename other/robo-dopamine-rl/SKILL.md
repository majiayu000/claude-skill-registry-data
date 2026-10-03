---
name: robo-dopamine-rl
title: "Robo-Dopamine: General Process Reward Modeling for Robotic Manipulation"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2512.23703
keywords: [robotics, reinforcement-learning, reward-modeling, multi-view, process-rewards]
description: "Overcome reward function design challenges via General Reward Model (GRM) for step-wise progress assessment. Uses multi-view observations for occlusion robustness, hop-based progress normalization, Policy-Invariant Reward Shaping—enabling 95% robot task success within 150 interactions with theoretically-grounded dense rewards."
---

## Overview

Addresses reward design challenges in robotic manipulation via principled progress modeling.

## Core Technique

**General Reward Model:**

```python
# Hop-based progress: normalized by task span
progress = model.predict_progress(observation, task_span)

# Multi-view fusion
fused_progress = aggregate_views([view1, view2, view3])

# Policy-Invariant Reward Shaping
reward = outcome_reward + policy_invariant_shaping(fused_progress)
```

## Performance

- 92.8% task completion accuracy
- 95% success within 150 interactions
- Theoretically grounded reward shaping

## References

- Step-wise progress discretization
- Multi-view observation fusion
- Policy-Invariant Reward Shaping

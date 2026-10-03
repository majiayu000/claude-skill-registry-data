---
name: rise-robot
title: "RISE: Self-Improving Robot Policy with Compositional World Model"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2602.11075"
keywords: [Robot Learning, World Models, Reinforcement Learning, Imagination, Policy Optimization, Compositional]
description: "Enable robot policies to self-improve through imagination using learned dynamics and value models without physical trial-and-error. Compositional world model separates concerns enabling 35-45% performance gains on contact-rich manipulation."
---

# RISE: Self-Improving Robot Policy with Compositional World Model

## Problem Context

Vision-Language-Action (VLA) foundation models excel at semantic understanding but struggle with precise contact-rich manipulation requiring fine motor control. Physical trial-and-error RL is expensive and impractical for real robots. Standard world models struggle to balance action controllability with realistic prediction. The core challenge: learn manipulation policies efficiently without costly physical interaction.

## Core Concept

RISE shifts robot learning from the physical world to imagination using a **compositional world model with specialized dynamics and value components**. Rather than joint training, the approach separates:

1. **Dynamics Model**: Predicts future observations given actions (what happens)
2. **Value Model**: Evaluates imagined states for progress signals (is this good)

This separation enables on-policy RL in imagination, where the policy iteratively improves by proposing actions, simulating consequences, evaluating outcomes, and updating based on advantage signals—all without touching a physical robot.

## Architecture Overview

- **Dynamics Model**: Video diffusion architecture with Task-Centric Batching for action diversity
- **Value Model**: Dual-objective learning combining progress regression and Temporal-Difference signals
- **Advantage Computation**: Cumulative improvement across imagined trajectories
- **Policy Warm-up**: Offline initialization on real demonstrations
- **Self-Improving Loop**: Imagination-based RL for continuous refinement
- **Multi-view Setup**: Observations from multiple camera perspectives for robustness

## Implementation

The compositional world model operates through two specialized components trained with different objectives:

```python
class DynamicsModel(nn.Module):
    """Predicts future observations from current state and action."""

    def __init__(self):
        # Video diffusion backbone
        self.backbone = VideoDiffusion()

    def forward(self, observations, actions):
        """
        Predict next multi-view observations.
        observations: [B, C, H, W] current state
        actions: [B, action_dim] proposed action
        Returns: [B, C, H, W] predicted next observations
        """
        # Concatenate observations and action
        state_action = torch.cat([observations, actions], dim=1)
        # Denoise over iterative steps to refine prediction
        predictions = self.backbone.sample(state_action, steps=50)
        return predictions
```

The value model combines progress and failure signals:

```python
class ValueModel(nn.Module):
    """Evaluates imagined trajectories for advantage computation."""

    def __init__(self, vla_backbone):
        self.backbone = vla_backbone  # Pre-trained VLA
        self.progress_head = nn.Linear(hidden_dim, 1)
        self.td_head = nn.Linear(hidden_dim, 1)

    def forward(self, trajectory):
        """
        Evaluate trajectory quality with dual objectives.
        trajectory: sequence of observations
        Returns: advantage signals for policy optimization
        """
        features = self.backbone.encode(trajectory)

        # Progress regression: how much closer to goal
        progress = self.progress_head(features)

        # Temporal-Difference learning: detect failures vs successes
        td_values = self.td_head(features)

        # Combine signals
        return progress + td_values
```

Self-improving policy optimization loop:

```python
def self_improving_loop(policy, dynamics_model, value_model,
                       goal_spec, num_iterations=100):
    """
    Imagination-based RL loop without physical interaction.
    """
    for iteration in range(num_iterations):
        # Sample task from curriculum
        task = sample_task(goal_spec)

        # Generate action proposals with advantage conditioning
        optimal_advantages = compute_target_advantages(task)
        proposed_actions = policy.sample(
            observations=task.initial_obs,
            target_advantages=optimal_advantages
        )

        # Simulate in learned dynamics model
        imagined_trajectory = []
        obs = task.initial_obs
        for t in range(horizon):
            action = proposed_actions[t]
            obs = dynamics_model(obs, action)
            imagined_trajectory.append(obs)

        # Evaluate imagined trajectory
        values = value_model(imagined_trajectory)

        # Compute advantage: difference between proposed and evaluated
        advantages = optimal_advantages - values

        # Policy optimization step
        policy.update(task.initial_obs, proposed_actions, advantages)

        yield {
            'iteration': iteration,
            'mean_advantage': advantages.mean().item(),
            'policy_loss': policy.loss.item()
        }
```

## Practical Guidance

**When to use**: RISE is most effective for:
- Manipulation tasks requiring precise contact dynamics
- Scenarios where physical interaction is expensive or unsafe
- Multi-step reasoning about object interactions
- Learning from VLA foundation models

**Key implementation steps**:

1. **Data Collection**: Gather 1000+ real demonstrations across manipulation scenarios
2. **Dynamics Training**: Train video diffusion model with task-centric batching to maximize action diversity
3. **Value Model Initialization**: Initialize from pre-trained VLA to leverage semantic understanding
4. **Policy Warm-up**: Offline RL on demonstrations to learn baseline behavior
5. **Self-Improvement**: Launch imagination loop with curriculum progression

**Task-centric batching strategy**:
- Within each batch, vary action diversity within same task
- Prevents mode collapse where dynamics model learns averaging behavior
- Prioritizes different action consequences over scenario diversity

**Expected improvements**:
- Dynamic brick sorting: +35% absolute performance
- Backpack packing: +45% absolute performance
- Box closing: +35% absolute performance
- Typical 3-5x faster convergence compared to physical RL

**Failure modes to avoid**:
- Insufficient action diversity in dynamics training → learned averaging
- Value model overfitting on initial demonstrations → poor generalization
- Too-aggressive policy updates → divergence in imagination
- Horizon too short → myopic behavior

## Reference

Compositional world models enable efficient robot learning by separating dynamics prediction and value estimation. The self-improving loop demonstrates how imagination-based RL can substantially improve policies without expensive physical trial-and-error on real robots.

---
name: lamer-meta-rl
title: "Meta-RL Induces Exploration in Language Agents"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2512.16848
keywords: [meta-learning, reinforcement-learning, exploration, agents, language-models]
description: "Enable LLM agents to actively explore and adapt policies through meta-RL instead of converging to fixed behaviors. Uses cross-episode training with trajectory-level discounting and in-context policy adaptation via textual reflections—achieving 11-19% improvements in exploration-exploitation balance across interactive environments."
---

## Overview

LaMer (Language Agent Meta-RL) addresses the exploration problem in RL-trained language agents. Standard RL training locks agents into deterministic policies without learning systematic exploration strategies. This framework enables agents to actively test uncertain actions and gather information through structured meta-learning.

## Core Technique

The key innovation is optimizing across multiple episodes rather than individual episodes, enabling agents to learn exploration patterns.

**Cross-Episode Training with Trajectory Discounting:**
Meta-RL extends the training horizon beyond single episodes, encouraging early exploration while later episodes exploit gathered information.

```python
# Cross-episode meta-RL formulation
def meta_rl_loss(episodes, gamma_traj=0.99):
    """
    Compute loss across episode sequence, not individual episodes.
    gamma_traj discounts returns across episodes, not within them.
    """
    total_loss = 0
    trajectory_return = 0

    for i, episode in enumerate(episodes):
        # Compute single-episode return
        episode_return = sum(r * gamma**t for t, r in enumerate(episode.rewards))

        # Accumulate across episode boundaries
        trajectory_return = episode_return + gamma_traj * trajectory_return

        # Policy loss encourages early exploration, later exploitation
        loss = -trajectory_return * log_prob(episode.actions)
        total_loss += loss

    return total_loss / len(episodes)
```

**In-Context Policy Adaptation:**
After each episode, agents generate textual reflections identifying mistakes and planning improvements. These reflections modify the context directly without gradient updates.

```python
# In-context adaptation pattern
def adapt_policy_intext(agent, episode):
    """
    Agent generates text reflection modifying its own behavior.
    Leverages LLM's in-context learning without retraining.
    """
    reflection = agent.generate(f"""
        Analyze this episode:
        Actions taken: {episode.actions}
        Mistakes identified: [agent identifies errors]
        Improvement plan: [agent plans changes]
    """)

    # Append reflection to agent's system context
    agent.context.append(reflection)

    return agent  # Updated without gradient descent
```

**Exploration Metrics:**
The framework measures exploration via trajectory diversity and action variance across episodes, showing that meta-RL produces "more diverse and explorative trajectories" while improving overall performance.

## When to Use This Technique

Use LaMer when:
- Training agents for environments requiring active exploration
- Agents need to learn information-gathering strategies
- Multi-episode interaction patterns are available
- Balancing exploration and exploitation is critical

## When NOT to Use This Technique

Avoid this approach if:
- Single-episode, one-shot tasks (meta-RL overhead unnecessary)
- Deterministic policies are optimal
- No multi-episode interaction structure
- Real-time immediate exploitation is prioritized

## Implementation Notes

The framework requires:
- Multiple sequential episodes for training
- Textual reflection generation and parsing
- Cross-episode discount factor tuning
- Integration with existing RL training pipelines
- Works across diverse environments (Sokoban, MineSweeper, WebShop)

## Key Performance

- 11-19% improvements in pass@3 success rates
- More diverse and explorative trajectories than baselines
- Effective exploration-exploitation balance

## References

- Cross-episode training with trajectory-level discounting
- In-context policy adaptation via textual reflections
- Meta-reinforcement learning for exploration induction

---
name: turn-ppo
title: "Turn-PPO: Turn-Level Advantage Estimation for Agentic LLMs"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2512.17008
keywords: [reinforcement-learning, ppo, agents, advantage-estimation, multi-turn]
description: "Stabilize multi-turn agent RL by shifting from token-level to turn-level MDPs. Reformulates states and actions at conversation-turn granularity, uses learned turn-level critics, and applies Generalized Advantage Estimation—eliminating misalignment that destabilizes GRPO training on long-horizon agentic tasks."
---

## Overview

Turn-PPO addresses a fundamental instability in reinforcement learning for multi-turn LLM agents: existing token-level formulations create MDP misalignment with the actual multi-turn interaction structure. By reformulating state-action pairs at turn boundaries, this technique enables stable value estimation and improved credit assignment.

## Core Technique

The key insight is that multi-turn interactions have natural episodic structure that token-level approaches ignore.

**State-Action Reformulation at Turn Level:**
Instead of treating individual tokens as actions, entire LLM responses within a turn become single actions, with full conversation history as state.

```python
# Turn-level MDP formulation
class TurnMDP:
    def __init__(self):
        self.turn_states = []  # Full history at each turn
        self.turn_actions = []  # Complete responses per turn

    def add_turn(self, query, response):
        # State: complete history up to current query
        state = self.conversation_history + [query]
        # Action: entire response (all tokens at once)
        action = response
        self.turn_states.append(state)
        self.turn_actions.append(action)

    def compute_advantages(self):
        # Critic operates at turn level, not token level
        values = [self.critic(s) for s in self.turn_states]
        advantages = compute_gae(rewards, values, gamma=0.99)
        return advantages
```

**Learned Turn-Level Critic:**
Unlike GRPO's sample-based advantage estimation, a separate critic network predicts value for each turn's state, enabling principled GAE computation.

```python
# Generalized Advantage Estimation at turn level
def compute_gae(rewards, values, gamma=0.99, gae_lambda=0.95):
    advantages = []
    gae = 0
    for t in reversed(range(len(rewards))):
        # TD residual at turn level
        if t == len(rewards) - 1:
            delta = rewards[t] - values[t]
        else:
            delta = rewards[t] + gamma * values[t+1] - values[t]
        # Accumulate GAE
        gae = delta + gamma * gae_lambda * gae
        advantages.insert(0, gae)
    return advantages
```

**Advantage Computation:**
For intermediate turns: γV_{n+1}−V_n. For final turns: r−V_n. This creates coherent credit assignment across multi-turn trajectories.

## When to Use This Technique

Use Turn-PPO when:
- Training LLM agents for multi-turn interactions (chat, web navigation, tool use)
- You need stable RL training with improved sample efficiency
- Long-horizon reasoning tasks with sparse intermediate rewards
- Existing token-level PPO shows training instability

## When NOT to Use This Technique

Avoid this approach if:
- Single-turn generation tasks (standard PPO suffices)
- Token-level credit assignment is necessary
- Fixed turn structure isn't available
- Real-time online learning requires immediate token-level feedback

## Implementation Notes

The framework requires:
- A separate turn-level value function network
- Generalized Advantage Estimation implementation
- Reformulation of reward signals at turn boundaries
- Integration with existing PPO training loops

## Key Performance

Strong improvements on long-horizon benchmarks:
- WebShop environment tasks
- Sokoban multi-step navigation
- Multi-turn conversation and reasoning tasks

## References

- State-action reformulation at interaction turn granularity
- Learned value functions for turn-level advantage estimation
- Generalized Advantage Estimation (GAE) with proper temporal credit assignment

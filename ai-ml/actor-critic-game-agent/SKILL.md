---
name: llm-actor-critic-game-agent
description: Shared-backbone neural network with actor (policy) and critic (value) heads for grid-based game agent RL training
---

# Actor-Critic Game Agent

## Overview

For grid-based game agents (Halite, Lux AI, microRTS), an actor-critic architecture shares a feature backbone and splits into two heads: the actor outputs action probabilities, the critic estimates state value. Training uses the advantage (return - value) to update the actor via policy gradient and the critic via Huber loss. This is more sample-efficient than pure policy gradient and more stable than pure value-based methods.

## Quick Start

```python
import tensorflow as tf
import numpy as np

def build_actor_critic(state_dim, num_actions):
    inputs = tf.keras.Input(shape=(state_dim,))
    x = tf.keras.layers.Dense(128, activation='tanh')(inputs)
    x = tf.keras.layers.Dense(32, activation='tanh')(x)

    actor = tf.keras.layers.Dense(num_actions, activation='softmax')(x)

    cx = tf.keras.layers.Dense(128, activation='relu')(inputs)
    cx = tf.keras.layers.Dense(32, activation='relu')(cx)
    critic = tf.keras.layers.Dense(1)(cx)

    return tf.keras.Model(inputs=inputs, outputs=[actor, critic])

def compute_returns(rewards, gamma=0.99):
    returns = []
    discounted = 0
    for r in reversed(rewards):
        discounted = r + gamma * discounted
        returns.insert(0, discounted)
    returns = np.array(returns)
    return (returns - returns.mean()) / (returns.std() + 1e-8)

model = build_actor_critic(state_dim=441, num_actions=5)
```

## Workflow

1. Flatten game grid state into a feature vector
2. Forward through shared backbone → actor probabilities + critic value
3. Sample action from actor distribution, execute in environment
4. Collect (state, action, reward) trajectories for one episode
5. Compute discounted returns, normalize for advantage
6. Update actor with `-log_prob * advantage`, critic with Huber loss

## Key Decisions

- **State representation**: flattened grid is simplest; CNN on 2D grid captures spatial patterns
- **Shared vs separate backbones**: shared is parameter-efficient; separate prevents gradient interference
- **Gamma**: 0.99 for long games, 0.95 for short episodes
- **On-policy**: A2C collects fresh trajectories each update; PPO adds clipping for stability

## References

- [Designing game AI with Reinforcement learning](https://www.kaggle.com/code/basu369victor/designing-game-ai-with-reinforcement-learning)

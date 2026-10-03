---
name: dr-mas
title: "Dr. MAS: Stable RL for Multi-Agent LLM Systems"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2602.08847"
keywords: [Multi-Agent RL, GRPO, Advantage Normalization, Agent Orchestration, Gradient Stability]
description: "Enable stable multi-agent reinforcement learning by normalizing advantages per-agent rather than globally, preventing gradient-norm inflation in heterogeneous multi-agent systems."
---

# Dr. MAS: Stable RL for Multi-Agent LLM Systems

## Problem Context

When applying GRPO (Group Relative Policy Optimization) to multi-agent systems, agents with different reward distributions experience **gradient-norm inflation**. A global reward baseline poorly aligned with some agents' reward statistics causes their gradients to explode, destabilizing training. This is especially severe in heterogeneous setups where agents play specialized roles.

## Core Concept

**Agent-Wise Advantage Normalization (Dr. MAS)** replaces global advantage normalization with per-agent normalization. Each agent normalizes advantages using its own reward statistics (μₖ, σₖ) rather than a global baseline, preventing gradient scaling mismatches while enabling stable co-training of heterogeneous agents.

## Architecture Overview

- **Multi-Agent Orchestration**: Flexible framework supporting different agent architectures and roles
- **Per-Agent Reward Tracking**: Partition experiences by agent; compute agent-specific reward statistics
- **Advantage Normalization**: Normalize each agent's advantages using its own mean/variance
- **Shared Resource Pooling**: Optional model weight sharing and efficient GPU scheduling
- **Gradient Stability**: Prevent norm inflation through per-agent normalization

## Implementation

**Phase 1: Multi-Agent Experience Collection**

```python
class MultiAgentOrchestrator:
    """Coordinate multiple LLM agents with per-agent reward tracking"""

    def __init__(self, agents, shared_model=None):
        self.agents = agents  # List of agent configurations
        self.shared_model = shared_model  # Optional shared LLM
        self.experience_buffer = defaultdict(list)

    def collect_trajectory(self, task, max_steps=10):
        """
        Collect multi-agent trajectory for a task.
        Different agents may activate at different steps.
        """

        state = task.initial_state()
        trajectory = {
            'task': task,
            'steps': [],
            'agent_assignments': []  # Which agent acted at each step
        }

        for step in range(max_steps):
            # Determine which agent should act (e.g., via task router)
            agent_id = select_agent_for_step(self.agents, state, step)
            agent = self.agents[agent_id]

            # Agent generates action
            action = agent.act(state)

            # Execute action in environment
            next_state, reward = task.step(action)

            trajectory['steps'].append({
                'agent_id': agent_id,
                'state': state,
                'action': action,
                'reward': reward,
                'next_state': next_state
            })
            trajectory['agent_assignments'].append(agent_id)

            state = next_state

            if task.is_terminal(state):
                break

        return trajectory

    def partition_by_agent(self, trajectory):
        """
        Partition trajectory steps by agent for per-agent normalization.
        Returns: dict[agent_id] -> list of (state, action, reward) tuples
        """

        agent_experiences = defaultdict(list)

        for step in trajectory['steps']:
            agent_id = step['agent_id']
            agent_experiences[agent_id].append({
                'state': step['state'],
                'action': step['action'],
                'reward': step['reward']
            })

        return agent_experiences
```

**Phase 2: Per-Agent Reward Statistics**

```python
def compute_per_agent_statistics(experiences, agents):
    """
    Compute reward mean and variance for each agent separately.

    experiences: dict[agent_id] -> list of reward values
    """

    agent_stats = {}

    for agent_id, agent_exps in experiences.items():
        rewards = [exp['reward'] for exp in agent_exps]

        # Compute mean and std
        mean = np.mean(rewards) if rewards else 0.0
        std = np.std(rewards) if rewards else 1.0

        # Add small epsilon to prevent division by zero
        std = max(std, 1e-8)

        agent_stats[agent_id] = {
            'mean': mean,
            'std': std,
            'count': len(rewards)
        }

    return agent_stats
```

**Phase 3: Per-Agent Advantage Normalization**

```python
def compute_advantages_per_agent(trajectory, value_fn, agents,
                                agent_stats):
    """
    Compute advantages normalized per-agent using per-agent statistics.
    """

    advantages = []
    agent_assignments = trajectory['agent_assignments']

    for step_idx, step in enumerate(trajectory['steps']):
        agent_id = step['agent_id']
        state = step['state']
        reward = step['reward']
        next_state = step['next_state']

        # Compute TD residual
        value_current = value_fn(state)
        value_next = value_fn(next_state)
        td_residual = reward + 0.99 * value_next - value_current

        # Normalize using agent-specific statistics
        stats = agent_stats[agent_id]
        advantage = (td_residual - stats['mean']) / stats['std']

        advantages.append(advantage)

    return advantages

def per_agent_advantage_normalization(trajectory, value_fn, agents):
    """
    Full pipeline for per-agent normalization.
    """

    # Partition trajectory by agent
    agent_experiences = defaultdict(list)
    for step_idx, step in enumerate(trajectory['steps']):
        agent_id = step['agent_id']
        agent_experiences[agent_id].append({
            'step_idx': step_idx,
            'state': step['state'],
            'reward': step['reward'],
            'next_state': step['next_state']
        })

    # Compute per-agent statistics
    agent_stats = {}
    for agent_id, exps in agent_experiences.items():
        rewards = [exp['reward'] for exp in exps]
        mean = np.mean(rewards)
        std = np.std(rewards) + 1e-8
        agent_stats[agent_id] = {'mean': mean, 'std': std}

    # Compute advantages with per-agent normalization
    advantages = []
    for step_idx, step in enumerate(trajectory['steps']):
        agent_id = step['agent_id']
        reward = step['reward']

        value_curr = value_fn(step['state'])
        value_next = value_fn(step['next_state'])
        td = reward + 0.99 * value_next - value_curr

        # Apply per-agent normalization
        stats = agent_stats[agent_id]
        advantage = (td - stats['mean']) / stats['std']

        advantages.append(advantage)

    return advantages
```

**Phase 4: GRPO Update with Per-Agent Advantages**

```python
def grpo_update_per_agent(model, trajectories, value_fn, agents):
    """
    Group Relative Policy Optimization with per-agent advantage normalization.
    """

    for group in trajectories:  # Batch of trajectories
        # Compute per-agent advantages
        advantages = per_agent_advantage_normalization(
            group, value_fn, agents
        )

        # Compute log probabilities
        logprobs = []
        for step_idx, step in enumerate(group['steps']):
            agent_id = step['agent_id']
            state = step['state']
            action = step['action']

            agent = agents[agent_id]
            logprob = agent.log_probability(state, action)
            logprobs.append(logprob)

        logprobs = torch.stack(logprobs)
        advantages = torch.tensor(advantages)

        # GRPO loss (simplified)
        # Compare trajectories within group
        advantage_mean = advantages.mean()
        advantage_std = advantages.std() + 1e-8

        normalized_advantages = (advantages - advantage_mean) / advantage_std

        # Policy loss
        loss = -torch.mean(normalized_advantages * logprobs)

        loss.backward()
        optimizer.step()

        # Value function update
        returns = compute_returns(group)
        value_loss = mse_loss(value_fn(group['states']), returns)
        value_loss.backward()
        value_optimizer.step()
```

**Phase 5: Optional Model Sharing**

```python
class SharedLLMMultiAgent:
    """
    Multi-agent system with shared LLM backbone.
    Each agent has task-specific prompt/prefix.
    """

    def __init__(self, base_model, agent_configs):
        self.base_model = base_model
        self.agent_configs = agent_configs

    def act(self, agent_id, state):
        """Agent-specific action generation via prompting"""
        agent_config = self.agent_configs[agent_id]
        prompt = agent_config['system_prompt']

        # Append state context
        full_prompt = f"{prompt}\n\nState: {state}"

        # Generate action from shared model
        action = self.base_model.generate(full_prompt)

        return action
```

## Practical Guidance

**When to use**: Deploy for heterogeneous multi-agent systems (e.g., planner agent, executor agent, verifier agent) where agents have different roles and reward distributions.

**Agent design**: Define clear responsibilities per agent to ensure meaningful per-agent reward statistics. Agents with similar reward distributions can be grouped together.

**Shared models**: Model sharing reduces memory footprint but may introduce competition during training. Start without sharing; add if memory is tight.

**Agent configuration**: Each agent needs learning rate, entropy coefficient, and other hyperparameters. Can reuse across agents or tune per-agent.

**Reward signal design**: Ensure reward signals are agent-specific (e.g., planner rewarded for quality plan, executor for execution fidelity). Misaligned rewards prevent benefits of per-agent normalization.

## Reference

Dr. MAS achieves +5.6% average improvement over vanilla GRPO while dramatically reducing gradient spikes, enabling stable co-training of heterogeneous agents. The key insight is that per-agent normalization prevents gradient scaling mismatches arising from different reward distributions, crucial for multi-agent systems where agents have specialized roles and different learning curves.

---
name: chain-of-agents
title: "Chain-of-Agents: End-to-End Agent Foundation Models"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2508.13167
keywords: [agent-foundation-models, multi-agent-distillation, agentic-rl, tool-agents, web-agents]
description: "Train single models to simulate multi-agent collaboration through distillation from complex multi-agent systems and agentic RL, creating efficient Agent Foundation Models for tool use and web navigation."
---

# Chain-of-Agents: End-to-End Agent Foundation Models

## Core Concept

Complex tasks (web navigation, API orchestration) typically require coordination between specialized agents. But maintaining multiple agents is expensive. Chain-of-Agents teaches a single model to dynamically activate different tool and role-playing agents internally, simulating multi-agent collaboration end-to-end.

The innovation: distill a sophisticated multi-agent system into a single Agent Foundation Model (AFM) through supervised learning, then refine with agentic RL for verifiable tasks.

## Architecture Overview

- **Multi-Agent Distillation**: Capture multi-agent system outputs as training data
- **Dynamic Agent Activation**: Learn to switch between different "agents" (planning, tool-use, reasoning)
- **Tool Agent Coordination**: Simulate tool calling and result interpretation
- **Role-Playing Agents**: Switch between different personas for different subtasks
- **Agentic RL**: Refine on verifiable tasks (web success, code execution)
- **End-to-End Training**: Single model learns full agent behavior

## Implementation Steps

### 1. Data Collection from Multi-Agent Systems

Run a multi-agent system and collect interaction logs.

```python
class MultiAgentSystemSimulator:
    """Record outputs from multi-agent system for distillation"""
    def __init__(self, planning_agent, tool_agent, reasoning_agent):
        self.planning_agent = planning_agent
        self.tool_agent = tool_agent
        self.reasoning_agent = reasoning_agent

    def collect_trajectory(self, task):
        """Collect full interaction trajectory"""
        trajectory = {
            'task': task,
            'steps': []
        }

        state = {'step': 0, 'completed': False, 'result': None}

        while not state['completed'] and state['step'] < 10:
            # Planning: what to do
            plan = self.planning_agent.decide(task, state)

            # Tool use: execute
            if plan['type'] == 'tool':
                result = self.tool_agent.execute(plan['tool'], plan['args'])
            else:
                result = self.reasoning_agent.reason(plan['reasoning'])

            trajectory['steps'].append({
                'state': state,
                'action': plan,
                'result': result,
                'agent_type': plan['type']
            })

            state = {'step': state['step'] + 1, 'result': result, 'completed': result.get('done', False)}

        return trajectory
```

### 2. Build Supervised Fine-Tuning Dataset

Convert trajectories into training data (input -> next action).

```python
def trajectories_to_training_data(trajectories):
    """Convert multi-agent trajectories to SFT training data"""
    training_data = []

    for traj in trajectories:
        for i, step in enumerate(traj['steps']):
            # Context: task + history
            context = f"Task: {traj['task']}\n"
            for prev_step in traj['steps'][:i]:
                context += f"Step {prev_step['state']['step']}: "
                context += f"{prev_step['action']}\n"

            # Target: next action
            action = step['action']
            target = format_action(action)

            training_data.append({
                'input': context,
                'output': target,
                'agent_type': action.get('type', 'reasoning')
            })

    return training_data

def format_action(action):
    """Format action for language model output"""
    if action['type'] == 'tool':
        return f"<tool>{action['tool']}</tool> {action['args']}"
    else:
        return f"<reasoning>{action['reasoning']}</reasoning>"
```

### 3. Train Agent Foundation Model with SFT

Supervised fine-tune a base model on distilled trajectories.

```python
def train_afm_sft(base_model, training_data, num_epochs=3):
    """Fine-tune base model on agent trajectories"""
    optimizer = torch.optim.AdamW(base_model.parameters(), lr=1e-5)

    for epoch in range(num_epochs):
        for batch in create_batches(training_data, batch_size=32):
            inputs = base_model.tokenizer(batch['input'], return_tensors='pt', padding=True)
            targets = base_model.tokenizer(batch['output'], return_tensors='pt', padding=True)

            # Forward pass
            logits = base_model(**inputs).logits
            loss = torch.nn.functional.cross_entropy(
                logits.view(-1, base_model.config.vocab_size),
                targets['input_ids'].view(-1)
            )

            # Backward
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    return base_model
```

### 4. Implement Action Parsing and Execution

Parse model outputs as actions and execute them.

```python
class ActionExecutor:
    """Parse and execute actions from AFM"""
    def __init__(self, tool_registry):
        self.tools = tool_registry

    def parse_action(self, model_output):
        """Extract action from model output"""
        import re
        if '<tool>' in model_output:
            match = re.search(r'<tool>(\w+)</tool>(.*)', model_output)
            if match:
                tool_name = match.group(1)
                args = match.group(2).strip()
                return {'type': 'tool', 'tool': tool_name, 'args': args}
        elif '<reasoning>' in model_output:
            match = re.search(r'<reasoning>(.*?)</reasoning>', model_output)
            if match:
                return {'type': 'reasoning', 'text': match.group(1)}
        return {'type': 'unknown'}

    def execute(self, action):
        """Execute parsed action"""
        if action['type'] == 'tool':
            tool = self.tools.get(action['tool'])
            if tool:
                return tool.run(action['args'])
        return {'error': 'Unknown action'}
```

### 5. Agentic RL Refinement

Fine-tune on verifiable tasks using RL rewards.

```python
def train_afm_rl(afm_model, tasks_with_rewards, num_steps=1000):
    """Fine-tune AFM using RL on verifiable tasks"""
    optimizer = torch.optim.AdamW(afm_model.parameters(), lr=1e-6)
    executor = ActionExecutor(tool_registry)

    for step in range(num_steps):
        task = random.choice(tasks_with_rewards)

        # Generate trajectory
        trajectory = []
        state = {'completed': False}
        rewards_list = []

        for action_step in range(10):
            if state['completed']:
                break

            # AFM generates action
            action_logits = afm_model.forward(task, state)
            action = sample_action(action_logits)

            # Execute
            result = executor.execute(action)
            trajectory.append((action, result))

            # Reward
            reward = task['reward_fn'](result)
            rewards_list.append(reward)
            state = result

        # Policy gradient update
        if rewards_list:
            total_reward = sum(rewards_list) / len(rewards_list)
            # Loss: -log_prob * reward
            loss = compute_policy_loss(trajectory, total_reward)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    return afm_model
```

### 6. Evaluation

Evaluate AFM on web/tool use benchmarks.

```python
def evaluate_afm(afm_model, benchmark_tasks):
    """Evaluate AFM on agent tasks"""
    executor = ActionExecutor(tool_registry)
    success_rate = 0.0

    for task in benchmark_tasks:
        # Run AFM on task
        state = {'task': task}
        success = False

        for _ in range(10):
            action_logits = afm_model.forward(task, state)
            action = greedy_sample_action(action_logits)
            result = executor.execute(action)

            if result.get('success', False):
                success = True
                break

            state = result

        success_rate += 1.0 if success else 0.0

    return success_rate / len(benchmark_tasks)
```

## Practical Guidance

- **Distillation Scale**: Collect 10K-100K+ trajectories from multi-agent system
- **SFT Learning Rate**: 1e-5 for fine-tuning (conservative)
- **RL Learning Rate**: 1e-6 (much smaller than SFT)
- **Action Vocabulary**: 20-50 distinct action types
- **Max Steps**: 8-12 steps per task

## Reference

Chain-of-Agents (2508.13167): https://arxiv.org/abs/2508.13167

Distill multi-agent systems into single Agent Foundation Models through supervised learning from trajectories and agentic RL, achieving SOTA on web agents and tool-use while being more efficient than multi-agent coordination.

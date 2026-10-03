---
name: config-agents
title: "Learning to Configure Agentic AI Systems"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2602.11574"
keywords: [Agent Configuration, Hierarchical RL, Reinforcement Learning, Hyperparameter Optimization, System Design]
description: "Learn optimal configurations for agentic AI systems through hierarchical RL that treats configuration as a query-wise decision problem. Structure policy selects workflows/tools/budgets while prompt policy composes specific instructions, achieving 25% accuracy improvement with 35% cost reduction."
---

# Learning to Configure Agentic AI Systems

## Problem Context

Agentic AI systems have enormous configuration spaces: tool selection, workflow choice, computational budget, prompt templates, reasoning strategies, etc. Over 8,600 possible structural configurations exist in simple systems. Manual tuning is infeasible. Static heuristics fail across different query types. Different queries benefit from different configurations (some need web search, others need local reasoning; some need 1-step, others need 5-step reasoning). The challenge: learn to configure agents dynamically per query while balancing accuracy and cost.

## Core Concept

ARC (Agentic Resource & Configuration learner) treats configuration as a **query-wise decision problem** solved through hierarchical RL. A two-level policy system:

1. **Structure Policy**: High-level decisions
   - Which workflows (sequential, hierarchical, parallel)
   - Which tools (web search, calculator, code executor)
   - Computational budgets (tokens, steps, time)

2. **Prompt Policy**: Low-level decisions
   - Specific task instructions
   - CoT strategies
   - Output format constraints

Rather than exhaustive grid search, masked RL with SFT on successful trajectories enables efficient learning under sparse rewards.

## Architecture Overview

- **Hierarchical Policy Structure**: Two-level decision hierarchy
- **Structure Policy**: Workflow/tool/budget selection
- **Prompt Policy**: Instruction composition and constraints
- **Action Masking**: Prevent invalid action combinations
- **Sparse Reward Signal**: Only on task completion
- **Masked RL**: PPO variant with invalid action masking
- **Supervised Fine-Tuning**: Learn from successful trajectories
- **Query-Wise Adaptation**: Per-query configuration decisions

## Implementation

Hierarchical policy architecture:

```python
class HierarchicalConfigurationPolicy(nn.Module):
    """
    Two-level policy: structure policy + prompt policy.
    Structure decides what capabilities to use.
    Prompt decides how to ask for them.
    """

    def __init__(self, model, tool_library, workflow_library):
        super().__init__()
        self.model = model
        self.tools = tool_library
        self.workflows = workflow_library

        # Structure policy: high-level configuration
        self.structure_policy = nn.Sequential(
            nn.Linear(768, 512),
            nn.ReLU(),
            nn.Linear(512, 256)
        )

        # Workflow head: which workflow type
        self.workflow_head = nn.Linear(256, len(workflow_library))

        # Tool selection head: which tools to enable
        self.tool_head = nn.Linear(256, len(tool_library))

        # Budget head: token/step budget
        self.budget_head = nn.Linear(256, 10)  # 10 budget levels

        # Prompt policy: low-level instruction generation
        self.prompt_policy = nn.TransformerDecoder(
            nn.TransformerDecoderLayer(768, 8),
            num_layers=2
        )

    def structure_decision(self, query):
        """
        High-level structure decisions given query.
        Returns: workflow, tools, budget.
        """
        # Encode query
        query_features = self.model.encode(query)

        # Structure policy forward pass
        structure_hidden = self.structure_policy(query_features)

        # Decode structure choices
        workflow_logits = self.workflow_head(structure_hidden)
        tool_logits = self.tool_head(structure_hidden)
        budget_logits = self.budget_head(structure_hidden)

        # Sample/select decisions
        workflow = torch.softmax(workflow_logits, dim=-1)
        tools = torch.sigmoid(tool_logits)  # Multi-binary selection
        budget = torch.softmax(budget_logits, dim=-1)

        return {
            'workflow': workflow,
            'tools': tools,
            'budget': budget,
            'logits': {
                'workflow': workflow_logits,
                'tools': tool_logits,
                'budget': budget_logits
            }
        }

    def action_masking(self, structure_decision):
        """
        Mask invalid action combinations.
        E.g., can't use web_search without internet access budget.
        """
        workflow = structure_decision['workflow'].argmax()
        tools = structure_decision['tools']
        budget = structure_decision['budget'].argmax()

        # Define constraints
        constraints = {
            'web_search': ['sequential', 'hierarchical'],  # Need internet
            'code_execution': ['dedicated_budget'],  # Needs computation budget
            'long_reasoning': ['hierarchical']  # Better for CoT
        }

        # Create mask
        mask = torch.ones_like(tools)

        for tool_idx, tool_name in enumerate(self.tools.keys()):
            compatible_workflows = constraints.get(tool_name, [])

            # Check compatibility
            if compatible_workflows:
                workflow_name = self.workflows[workflow]
                if workflow_name not in compatible_workflows:
                    mask[tool_idx] = 0

        return mask

    def prompt_decision(self, query, structure_decision):
        """
        Low-level prompt composition given structure.
        Generates specific instructions for the agent.
        """
        # Get structure information
        workflow = structure_decision['workflow'].argmax()
        selected_tools = structure_decision['tools'].nonzero(as_tuple=True)[0]
        budget_level = structure_decision['budget'].argmax()

        # Build prompt based on decisions
        prompt_parts = []

        # Add workflow instruction
        workflow_name = list(self.workflows.keys())[workflow]
        if workflow_name == 'sequential':
            prompt_parts.append(
                "Solve step-by-step using one tool at a time.")
        elif workflow_name == 'hierarchical':
            prompt_parts.append(
                "Break into subproblems, solve each independently.")
        elif workflow_name == 'parallel':
            prompt_parts.append(
                "Work on multiple approaches simultaneously.")

        # Add tool instructions
        for tool_idx in selected_tools:
            tool_name = list(self.tools.keys())[tool_idx]
            tool_instruction = self.tools[tool_name]['instruction']
            prompt_parts.append(f"You can use: {tool_instruction}")

        # Add budget constraints
        budget_values = [100, 250, 500, 1000, 2000, 5000, 10000,
                        20000, 50000, 100000]
        max_tokens = budget_values[budget_level]
        prompt_parts.append(
            f"Keep total reasoning under {max_tokens} tokens.")

        # Add query
        prompt_parts.append(f"Query: {query}")

        composed_prompt = "\n".join(prompt_parts)

        return {
            'composed_prompt': composed_prompt,
            'workflow': workflow_name,
            'tools': [list(self.tools.keys())[i] for i in selected_tools],
            'budget': budget_values[budget_level]
        }

    def forward(self, query):
        """
        Full configuration pipeline.
        """
        structure = self.structure_decision(query)
        mask = self.action_masking(structure)
        prompt = self.prompt_decision(query, structure)

        return {
            'structure': structure,
            'mask': mask,
            'prompt': prompt
        }
```

Masked RL training:

```python
class MaskedRLTrainer:
    """
    Train configuration policy with action masking.
    Prevents invalid configurations during exploration.
    """

    def __init__(self, policy, environment):
        self.policy = policy
        self.env = environment
        self.optimizer = torch.optim.Adam(
            policy.parameters(), lr=1e-4)

    def compute_masked_logits(self, logits, mask):
        """
        Mask invalid actions before softmax.
        """
        # Set logits of invalid actions to very negative
        masked_logits = logits.clone()
        masked_logits[mask == 0] = -1e10

        return masked_logits

    def sample_masked_action(self, logits, mask):
        """
        Sample action respecting mask.
        """
        masked_logits = self.compute_masked_logits(logits, mask)
        probs = torch.softmax(masked_logits, dim=-1)

        # Sample valid action only
        valid_actions = torch.where(mask == 1)[0]
        sampled_idx = torch.multinomial(
            probs[valid_actions], num_samples=1)[0]

        return valid_actions[sampled_idx]

    def train_step(self, query_batch, num_epochs=1):
        """
        PPO training step with masked actions.
        """
        for epoch in range(num_epochs):
            for query in query_batch:
                # Get current policy output
                config = self.policy(query)
                structure = config['structure']
                mask = config['mask']

                # Sample configuration
                sampled_workflow = self.sample_masked_action(
                    structure['logits']['workflow'],
                    torch.ones(len(self.policy.workflows)))

                sampled_tools_logits = structure['logits']['tools']
                sampled_tools = self.sample_masked_action(
                    sampled_tools_logits, mask)

                # Execute configuration
                trajectory = self.env.execute_agent_with_config(
                    query, config)

                # Compute reward
                reward = self.env.compute_reward(trajectory)

                # Compute log probabilities
                log_prob = self.compute_log_probability(
                    structure, sampled_workflow, sampled_tools)

                # Policy gradient update
                loss = -reward * log_prob

                # Backward pass
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                yield {
                    'query': query,
                    'reward': reward.item(),
                    'loss': loss.item()
                }

    def compute_log_probability(self, structure_output,
                                sampled_workflow, sampled_tools):
        """Compute log probability of sampled action."""
        workflow_logits = structure_output['logits']['workflow']
        tools_logits = structure_output['logits']['tools']

        # Log probability of workflow choice
        workflow_log_prob = torch.nn.functional.log_softmax(
            workflow_logits, dim=-1)[sampled_workflow]

        # Log probability of tool selection
        tools_log_prob = torch.nn.functional.log_softmax(
            tools_logits, dim=-1)[sampled_tools]

        return workflow_log_prob + tools_log_prob
```

Supervised fine-tuning on successful trajectories:

```python
class ConfigurationSupervisedFinetuning:
    """
    Fine-tune policy on successful configuration examples.
    Bootstraps RL with high-quality trajectories.
    """

    def __init__(self, policy, successful_trajectories):
        self.policy = policy
        self.successful_trajs = successful_trajectories
        self.optimizer = torch.optim.Adam(
            policy.parameters(), lr=5e-5)

    def collect_successful_examples(self):
        """
        Gather examples where configuration led to success.
        """
        examples = []

        for traj in self.successful_trajs:
            query = traj['query']
            config = traj['configuration']
            reward = traj['reward']

            if reward > success_threshold := 0.8:
                examples.append((query, config))

        return examples

    def supervised_update(self, batch_size=32, num_epochs=5):
        """
        Train policy to reproduce successful configurations.
        """
        examples = self.collect_successful_examples()

        for epoch in range(num_epochs):
            for batch_start in range(0, len(examples), batch_size):
                batch = examples[batch_start:
                                batch_start + batch_size]

                batch_loss = 0.0

                for query, target_config in batch:
                    # Get policy output
                    policy_output = self.policy(query)

                    # Compute supervised loss
                    workflow_loss = self.compute_config_loss(
                        policy_output['structure']['logits']['workflow'],
                        target_config['workflow'])

                    tools_loss = self.compute_config_loss(
                        policy_output['structure']['logits']['tools'],
                        target_config['tools'])

                    loss = workflow_loss + tools_loss

                    batch_loss += loss.item()

                    # Backward pass
                    self.optimizer.zero_grad()
                    loss.backward()
                    self.optimizer.step()

                print(f"Epoch {epoch}: Average Loss={
                    batch_loss / len(batch):.4f}")

    def compute_config_loss(self, policy_logits, target_config):
        """Cross-entropy loss between policy and target."""
        # Convert target to probability distribution
        target_probs = torch.zeros_like(policy_logits)
        target_probs[target_config] = 1.0

        # KL divergence
        loss = torch.nn.functional.kl_div(
            torch.nn.functional.log_softmax(policy_logits, dim=-1),
            target_probs,
            reduction='batchmean')

        return loss
```

## Practical Guidance

**When to use**:
- Complex agent systems with many configuration choices
- Different query types benefit from different configurations
- Want to balance accuracy vs computational cost
- Have access to query-response pairs for training

**System design**:

1. **Define configuration space**:
   - Workflows: sequential, hierarchical, parallel
   - Tools: web search, calculator, code execution, etc.
   - Budgets: token limits, reasoning depth, etc.

2. **Implement environment**:
   - Execute agent with given configuration
   - Compute reward signal
   - Track success/failure

3. **Create action masks**:
   - Define compatible combinations
   - Prevent invalid configurations early
   - Reduce exploration wasted on invalid states

4. **Training pipeline**:
   - Collect successful trajectories
   - Supervised fine-tuning on successful examples
   - Masked RL for policy improvement
   - Alternate between SFT and RL phases

**Configuration space size**:
- Workflows: 3-5 types
- Tools: 5-15 available
- Budgets: 8-10 levels
- **Total combinations**: 3 × 2^15 × 10 = 983,040 possible configs
- **Constraint with masking**: 50-100 valid configs per workflow

**Expected improvements**:
- Accuracy: +25% vs static heuristic baselines
- Cost: -35% reduction in token usage
- Latency: -20% improvement in execution time
- Query-specific adaptation: 90%+ optimal config selection

**Training schedule**:

1. **Phase 1 (SFT)**: 1,000 successful trajectory examples
   - Learn to reproduce successful patterns
   - Initialize policy with high-quality examples
   - Epochs: 5-10

2. **Phase 2 (Masked RL)**: 5,000-10,000 exploration steps
   - Explore new configurations
   - Reinforce high-reward patterns
   - Learning rate: 1e-4

3. **Phase 3 (Refinement)**: 1,000-2,000 steps
   - Fine-tune on hardest queries
   - Balance exploration vs exploitation
   - Lower learning rate: 5e-5

**Evaluation**:
- Accuracy on test queries
- Token efficiency (accuracy per token)
- Configuration diversity
- Generalization to new query types
- Latency distribution

**Common configurations to learn**:

```
Simple factual queries:
- Workflow: sequential
- Tools: web_search only
- Budget: low (500-1000 tokens)

Complex reasoning queries:
- Workflow: hierarchical
- Tools: web_search + code_execution
- Budget: high (10000+ tokens)

Coding queries:
- Workflow: sequential
- Tools: code_executor + debugger
- Budget: medium-high (5000+ tokens)

Planning queries:
- Workflow: hierarchical
- Tools: reasoning_engine
- Budget: medium (2000-5000 tokens)
```

## Reference

Hierarchical RL with action masking enables learning optimal dynamic configurations for agentic AI systems. By decomposing configuration into structure (workflow/tools/budget) and prompt (instructions) decisions and constraining the action space through masks, systems can adapt per-query while exploring efficiently in a high-dimensional configuration space.

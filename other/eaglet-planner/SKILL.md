---
name: eaglet-planner
title: "A Goal Without a Plan Is Just a Wish: Efficient Global Planner Training for Long-Horizon Agent Tasks"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2510.05608"
keywords: [planning, long-horizon, reinforcement-learning, agent-training, executor-capability]
description: "Train efficient planners for long-horizon agent tasks using homologous consensus filtering to generate synthetic plans from strong LLMs and rule-based RL with executor capability rewards. Reduces training cost by 8x while maintaining state-of-the-art performance."
---

# EAGLET: Efficient Planner Training via Synthetic Plan Generation

Long-horizon agent planning requires expensive manual annotation or extensive RL training. EAGLET generates synthetic high-quality plans from advanced LLMs without manual labeling, then refines them with specialized RL using executor feedback signals.

Core insight: strong planning comes from both good initial plans and learning from execution signals. By bootstrapping from LLM-generated plans and using executor capability as reward signal, you achieve sample-efficient training at 8x lower cost than traditional RL.

## Core Concept

**Homologous Consensus Filtering**: Generate multiple candidate plans from a strong LLM and keep only those with high consensus across samples. This automatically filters out hallucinated or low-quality plans without human annotation.

**Executor Capability Gain Reward**: Reward signal based on whether executing the plan reveals new agent capabilities, not just whether tasks succeed. Encourages plans that push agent boundaries.

## Architecture Overview

- **Plan Synthesizer**: Advanced LLM (GPT-4/Claude) generates diverse candidate plans
- **Consensus Filter**: Scores plans by agreement across multiple samples and baseline quality
- **Executor Simulator**: Simulates plan execution to estimate feasibility
- **RL Trainer**: Refines planner with capability-gain rewards

## Implementation Steps

**Stage 1: Synthetic Plan Generation with Consensus Filtering**

Generate plans from strong LLM and filter by consensus:

```python
def generate_consensus_plans(task, num_candidates=10, strong_llm='gpt-4'):
    """
    Generate diverse plans and keep only consensus-agreed ones.

    Args:
        task: description of agent task
        num_candidates: how many plan samples to generate
        strong_llm: which model to use for generation

    Returns:
        filtered_plans: high-confidence plans
    """

    # Generate diverse candidates
    candidates = []
    for i in range(num_candidates):
        temperature = 0.8  # Encourage diversity

        prompt = f"""
        For the task: {task}

        Generate a detailed step-by-step plan.
        Consider:
        - Necessary preconditions
        - High-level milestones
        - Dependency ordering
        - Executor constraints
        """

        plan = strong_llm.generate(
            prompt,
            temperature=temperature,
            max_tokens=1024
        )
        candidates.append(plan)

    # Compute consensus scores
    consensus_scores = compute_plan_similarity(candidates)

    # Filter high-consensus plans
    threshold = np.percentile(consensus_scores, 40)  # Keep top 60%
    filtered_plans = [
        candidates[i] for i in range(len(candidates))
        if consensus_scores[i] >= threshold
    ]

    return filtered_plans

def compute_plan_similarity(plans):
    """
    Score plans by how similar they are to other plans.
    High similarity = high confidence.
    """
    scores = []
    for i, plan_i in enumerate(plans):
        # Extract key steps from plan
        steps_i = extract_plan_steps(plan_i)

        similarities = []
        for j, plan_j in enumerate(plans):
            if i != j:
                steps_j = extract_plan_steps(plan_j)
                sim = compute_step_similarity(steps_i, steps_j)
                similarities.append(sim)

        # Score = average similarity to other plans
        scores.append(np.mean(similarities))

    return scores
```

**Stage 2: Cold Start Fine-tuning**

Use filtered plans to bootstrap the agent planner:

```python
def cold_start_finetuning(
    planner_model,
    filtered_plans,
    task_descriptions,
    num_epochs=3
):
    """
    Initial fine-tuning on high-quality synthetic plans.
    Acts as warm start before RL refinement.
    """

    optimizer = torch.optim.AdamW(
        planner_model.parameters(),
        lr=5e-5
    )

    for epoch in range(num_epochs):
        for task, plan in zip(task_descriptions, filtered_plans):
            # Tokenize task and plan
            task_tokens = tokenize(task)
            plan_tokens = tokenize(plan)

            # Teacher forcing: model learns to generate plan given task
            logits = planner_model(task_tokens)

            # Compute cross-entropy loss
            loss = F.cross_entropy(
                logits.view(-1, vocab_size),
                plan_tokens.view(-1)
            )

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    return planner_model
```

**Stage 3: Executor Capability Reward Training**

Refine planner using execution feedback:

```python
def rl_training_with_capability_reward(
    planner_model,
    executor_agent,
    task_distribution,
    num_steps=5000
):
    """
    Train planner with rewards based on executor learning progress.
    Capability gain = new skills discovered through plan execution.
    """

    optimizer = torch.optim.AdamW(
        planner_model.parameters(),
        lr=1e-5
    )

    # Track executor capabilities
    initial_skills = executor_agent.get_skill_set()

    for step in range(num_steps):
        # Sample task
        task = sample_from(task_distribution)

        # Generate plan
        plan = planner_model.generate(
            task,
            max_length=512,
            temperature=0.7
        )

        # Execute plan
        execution_result = executor_agent.execute_plan(plan, task)

        # Compute rewards
        success_reward = 1.0 if execution_result['success'] else 0.0

        # Capability gain: what new skills were used?
        skills_used = execution_result['skills_used']
        new_skills = skills_used - initial_skills
        capability_reward = len(new_skills) * 0.5

        # Total reward: success + exploration bonus
        total_reward = success_reward + capability_reward

        # Policy gradient update
        log_prob = compute_log_probability(planner_model, plan)
        loss = -(log_prob * total_reward)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Update skill tracking
        if new_skills:
            initial_skills.update(new_skills)
```

## Practical Guidance

**When to Use EAGLET:**
- Long-horizon tasks (10+ steps) with limited labeled plan data
- When you have access to strong LLM for synthetic plan generation
- Tasks where executor capability is measurable/observable

**When NOT to Use:**
- Short tasks (1-3 steps) where manual annotation is simple
- Domain without clear skill/capability progression
- Executors where capability feedback is hard to define

**Plan Generation Tips:**

| Strategy | Best For | Tradeoff |
|----------|----------|----------|
| High temperature (0.9-1.0) | Diverse candidates | More filtering needed |
| Low temperature (0.5-0.6) | Focused candidates | Less coverage of solution space |
| Consensus threshold 40% | Inclusive filtering | More noisy plans included |
| Consensus threshold 60% | Strict filtering | Fewer plans, higher quality |

**Common Pitfalls:**
- Generating too few candidates (reduce diversity benefits)
- Consensus score overly permissive (include bad plans)
- Executor capability too strict (hard to satisfy)
- Not tracking skill progression (lose learning signal)

## Reference

Based on the research at: https://arxiv.org/abs/2510.05608

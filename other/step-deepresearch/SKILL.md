---
name: step-deepresearch
title: "Step-DeepResearch: Autonomous Research via Atomic Capabilities"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2512.20491
keywords: [research, agents, planning, information-seeking, reinforcement-learning]
description: "Enable autonomous AI research systems to move beyond web search toward true research through four composable atomic capabilities: planning/decomposition, deep search/synthesis, reflection/verification, and report generation. Progressive training across 32K→128K context with SFT and RL produces single ReAct agents matching proprietary systems with lower costs."
---

## Overview

Step-DeepResearch addresses the fundamental gap between web search and true research. Search optimization merely retrieves documents, while research demands intent decomposition, multi-source verification, and coherent synthesis. This framework decompose research into four trainable atomic capabilities.

## Core Technique

Rather than treating research as a monolithic task, decompose it into learnable, composable components.

**Four Atomic Capabilities Framework:**
Each capability is independently trainable and composable into end-to-end workflows.

```python
# Atomic capabilities for research automation
class ResearchCapabilities:
    def __init__(self):
        self.planner = PlanningAgent()           # Task decomposition
        self.searcher = DeepSearchAgent()        # Multi-hop synthesis
        self.verifier = ReflectionAgent()        # Error correction
        self.reporter = ReportGenerationAgent()  # Structured output

    def research_workflow(self, research_goal):
        """
        Orchestrate atomic capabilities into research process.
        """
        # Capability 1: Planning & Task Decomposition
        plan = self.planner.decompose(research_goal)
        # Returns: [subtask_1, subtask_2, ...]

        # Capability 2: Deep Search & Information Seeking
        evidence = self.searcher.multihop_search(plan)
        # Returns: {subtask: [sources, facts, citations]}

        # Capability 3: Reflection & Verification
        verified_evidence = self.verifier.cross_source_check(evidence)
        # Returns: {fact: confidence, citations: validated}

        # Capability 4: Report Generation
        report = self.reporter.synthesize(verified_evidence)
        # Returns: structured_report

        return report
```

**Progressive Training Pipeline:**
Multi-stage training injects atomic capabilities into successively larger contexts.

```python
def progressive_training(model, datasets):
    """
    Three-stage training enables atomic capability composition.
    """
    # Stage 1: Mid-training on 32K context
    # Inject atomic capability recognition via synthetic data
    print("Stage 1: Atomic capability injection (32K context)")
    capability_data = generate_atomic_capability_examples()
    model = train_on_data(model, capability_data, max_tokens=32000)

    # Stage 2: Extend to 128K context
    # Scale atomic capabilities and composition patterns
    print("Stage 2: Capability composition (128K context)")
    composition_data = generate_composition_examples()
    model = train_on_data(model, composition_data, max_tokens=128000)

    # Stage 3: Supervised Fine-Tuning
    # Compose capabilities into end-to-end task trajectories
    print("Stage 3: End-to-end trajectory composition (SFT)")
    trajectory_data = generate_research_trajectories(
        quality_filter=strict_filtering
    )
    model = supervised_finetune(model, trajectory_data)

    # Stage 4: Reinforcement Learning
    # Real-world environment interaction with rubric rewards
    print("Stage 4: RL with rubric-based rewards")
    rl_model = reinforce_with_rubrics(model, research_rubrics)

    return rl_model
```

**Rubric-Based Reward Signals:**
RL training uses structured rubrics extracted from successful research papers.

```python
class ResearchRubrics:
    def __init__(self):
        self.planning_rubric = [
            "Decomposition is exhaustive",
            "Subtasks are independent",
            "Coverage addresses original intent"
        ]
        self.search_rubric = [
            "Evidence is diverse (multiple sources)",
            "Facts are cross-referenced",
            "Citations are traceable"
        ]
        self.synthesis_rubric = [
            "Arguments are coherent",
            "Conclusions follow from evidence",
            "Alternative views are acknowledged"
        ]

    def compute_reward(self, trajectory, rubric):
        """
        Reward = fraction of satisfied rubric items.
        """
        satisfied = sum(
            1 for item in rubric
            if check_satisfaction(trajectory, item)
        )
        reward = satisfied / len(rubric)
        return reward
```

## When to Use This Technique

Use Step-DeepResearch when:
- Conducting automated open-ended research
- Combining multiple information sources
- Verification and cross-source validation needed
- Complex multi-step reasoning required

## When NOT to Use This Technique

Avoid this approach if:
- Single factual lookup (simple retrieval sufficient)
- Real-time constraints prohibit multi-step reasoning
- Research domain not covered by training data
- Task doesn't decompose naturally

## Implementation Notes

The framework requires:
- 32B-parameter model as baseline
- Progressive training infrastructure (32K→128K context)
- Atomic capability definition and examples
- Rubric extraction and scoring pipeline
- RL training with environment interaction

## Key Performance

- Comparable to proprietary research systems (GPT-4, Claude)
- Lower inference costs with 32B model
- Strong performance on structured research tasks

## References

- Atomic capability decomposition for research
- Progressive training across context sizes
- Rubric-based reward learning from research papers
- Multi-agent composition versus monolithic design

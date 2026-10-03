---
name: sage-rl-agent
title: "RL for Self-Improving Agent with Skill Library"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2512.17102
keywords: [reinforcement-learning, agents, skill-learning, self-improvement, grpo]
description: "Enable agents to continuously improve by accumulating reusable skills across sequential task chains. Train via GRPO across task sequences where skills persist and compound, provide dual rewards for both task completion and skill generation/reuse—improving completion rates 8.9% while reducing token costs by 59% compared to non-skill baselines."
---

## Overview

SAGE (Skill Augmented GRPO for self-Evolution) addresses the challenge of agent self-improvement through skill accumulation. Rather than relearning solutions to repeated problems, agents build a persistent skill library and are rewarded for both using existing skills and generating new ones that prove useful in downstream tasks.

## Core Technique

The key insight is that training across task sequences rather than individual tasks enables skill discovery and reuse.

**Sequential Rollout Training:**
Instead of treating each task independently, train across chains of related tasks where skills accumulate.

```python
# Sequential task training with skill persistence
class SAGE:
    def __init__(self):
        self.skill_library = {}
        self.task_chain = []

    def train_on_task_chain(self, task_sequence):
        """
        Process chain of similar tasks sequentially.
        Skills generated in early tasks are available for later tasks.
        """
        skill_library = {}  # Persistent across tasks

        for task_idx, task in enumerate(task_sequence):
            print(f"Task {task_idx}: {task.name}")

            # Rollout for this task (with available skills)
            trajectory = self.rollout_with_skills(task, skill_library)

            # Compute rewards (outcome + skill metrics)
            outcome_reward = compute_task_reward(trajectory)

            # Identify if agent generated new, useful skills
            new_skills = self.extract_skills(trajectory)
            for skill in new_skills:
                # Check if skill is useful for remaining tasks
                future_usefulness = assess_future_utility(
                    skill, task_sequence[task_idx+1:]
                )
                if future_usefulness > threshold:
                    skill_library[skill.name] = skill
                    outcome_reward += skill_generation_bonus

            # GRPO update with composite reward
            self.update_via_grpo(trajectory, outcome_reward)

        return skill_library
```

**Skill-Integrated Reward Structure:**
Dual incentives encourage both completing tasks and creating/reusing skills.

```python
def compute_skill_aware_reward(trajectory, skill_library):
    """
    Reward includes task completion and skill generation/reuse.
    """
    # Base task completion reward
    task_reward = 1.0 if trajectory.success else 0.0

    # Bonus for generating useful skills
    generated_skills = extract_generated_skills(trajectory)
    skill_generation_reward = len(generated_skills) * 0.1

    # Bonus for reusing existing skills
    reused_skills = extract_reused_skills(trajectory, skill_library)
    skill_reuse_reward = len(reused_skills) * 0.05

    total_reward = task_reward + skill_generation_reward + skill_reuse_reward

    return total_reward
```

**Skill Extraction and Reusability:**
Automatically extract executable functions from successful trajectories.

```python
class SkillExtractor:
    def extract_skills(self, trajectory):
        """
        Convert successful sub-trajectories into reusable skills.
        Skills are executable functions callable by agent.
        """
        skills = []

        # Identify repeated or complex sub-patterns
        for subtask in trajectory.subtasks:
            if subtask.importance > threshold:
                # Convert to reusable function
                skill = self.convert_to_function(subtask)

                # Verify it's truly reusable
                if self.test_on_similar_tasks(skill):
                    skills.append(skill)

        return skills

    def convert_to_function(self, subtask):
        """
        Convert trajectory segment into callable Python function.
        Example: subtask → def click_button_x(): ...
        """
        code = generate_code_from_trajectory(subtask)
        skill_function = compile_and_execute(code)
        return skill_function
```

## When to Use This Technique

Use SAGE when:
- Training agents across related task sequences
- Skill reuse can reduce total computation
- Tasks have common sub-goals or patterns
- Self-improvement through experience is desired

## When NOT to Use This Technique

Avoid this approach if:
- Single-task optimization (skill overhead unnecessary)
- Tasks are completely unrelated (no skill transfer)
- Skill extraction complexity not justified by gains
- Real-time learning requires immediate task focus

## Implementation Notes

The framework requires:
- GRPO training infrastructure
- Skill extraction mechanism from trajectories
- Persistent skill library management
- Dual-reward computation (task + skill)
- Integration with agent execution environment

## Key Performance

- 8.9% higher scenario completion rates
- 26% fewer interaction steps
- 59% fewer tokens than non-skill baselines
- Demonstrated on AppWorld benchmark

## References

- Sequential task training for skill accumulation
- Persistent skill library across task chains
- Skill-generation and skill-reuse rewards
- Automatic skill extraction from trajectories
- GRPO training with composite rewards

---
name: rl-rubric-anchors
title: "Reinforcement Learning with Rubric Anchors"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2508.12790
keywords: [reinforcement-learning, rubric-based-rewards, subjective-evaluation, open-ended-generation]
description: "Extend RL to open-ended tasks using structured rubrics as reward anchors, enabling fine-grained evaluation of subjective outputs without requiring binary correctness signals."
---

# Reinforcement Learning with Rubric Anchors

## Core Concept

Traditional RL for LLMs relies on verifiable rewards (code execution, test cases, factuality checks). But many tasks are subjective: writing quality, helpfulness, style, creativity. These resist binary correct/incorrect labels.

Rubric-based rewards translate subjective evaluation into structured scoring frameworks. A rubric specifies dimensions (clarity, relevance, tone) with criteria and point scales. This lets models learn to optimize complex, nuanced objectives through RL, making it practical to train on open-ended generation tasks.

The innovation: rubrics act as "anchors" providing interpretable, machine-readable reward signals for traditionally subjective domains.

## Architecture Overview

- **Structured Rubric Framework**: Multi-dimensional evaluation criteria with explicit scoring rules
- **Automated Rubric Scoring**: Apply rubrics to outputs to generate numerical rewards
- **Interpretable Rewards**: Each reward reflects specific quality dimension (clarity, completeness, etc.)
- **Human-LLM Rubric Creation**: Mix human-designed and LLM-generated rubrics for diverse tasks
- **Compositional Rewards**: Combine multiple rubric dimensions into unified reward signal
- **Style Control**: Rubrics enable training models for specific styles/tones

## Implementation Steps

### 1. Design Rubric Framework

Create a structured rubric template that defines scoring dimensions.

```python
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class RubricCriterion:
    """A single scoring criterion in a rubric"""
    dimension: str  # e.g., "clarity", "relevance"
    description: str
    score_levels: List[Tuple[int, str]]  # [(1, "Poor"), (2, "Fair"), ..., (5, "Excellent")]
    weight: float = 1.0  # Importance in overall score

class Rubric:
    """
    Structured rubric for evaluating outputs
    """
    def __init__(self, task_name: str, criteria: List[RubricCriterion]):
        self.task_name = task_name
        self.criteria = criteria

    def get_rubric_text(self) -> str:
        """
        Format rubric as readable text for LLM evaluation
        """
        text = f"Evaluation Rubric for {self.task_name}\n"
        text += "=" * 50 + "\n\n"

        for criterion in self.criteria:
            text += f"Dimension: {criterion.dimension}\n"
            text += f"Description: {criterion.description}\n"
            text += "Scoring Levels:\n"

            for score, description in criterion.score_levels:
                text += f"  {score}: {description}\n"

            text += "\n"

        return text

# Example: Essay Evaluation Rubric
essay_criteria = [
    RubricCriterion(
        dimension="clarity",
        description="How clearly is the argument presented?",
        score_levels=[
            (1, "Unclear, hard to follow"),
            (2, "Somewhat unclear"),
            (3, "Moderately clear"),
            (4, "Clear and well-organized"),
            (5, "Exceptionally clear and compelling")
        ],
        weight=0.25
    ),
    RubricCriterion(
        dimension="relevance",
        description="How relevant is the content to the prompt?",
        score_levels=[
            (1, "Off-topic or irrelevant"),
            (2, "Partially relevant"),
            (3, "Mostly relevant"),
            (4, "Highly relevant"),
            (5, "Perfectly aligned with prompt")
        ],
        weight=0.25
    ),
    RubricCriterion(
        dimension="depth",
        description="How detailed and substantive is the response?",
        score_levels=[
            (1, "Superficial, lacks depth"),
            (2, "Limited depth"),
            (3, "Moderate depth"),
            (4, "Good depth and detail"),
            (5, "Comprehensive and insightful")
        ],
        weight=0.3
    ),
    RubricCriterion(
        dimension="grammar",
        description="Grammar and writing quality",
        score_levels=[
            (1, "Many errors"),
            (2, "Several errors"),
            (3, "Few errors"),
            (4, "Minor errors only"),
            (5, "Flawless")
        ],
        weight=0.2
    )
]

essay_rubric = Rubric("Essay Writing", essay_criteria)
print(essay_rubric.get_rubric_text())
```

### 2. Implement LLM-Based Rubric Scoring

Use an LLM to evaluate outputs according to rubric criteria.

```python
class RubricScorer:
    """
    Score outputs using a rubric via LLM evaluation
    """
    def __init__(self, eval_llm_model, rubric: Rubric):
        self.eval_model = eval_llm_model
        self.rubric = rubric

    def score_output(self, prompt: str, output: str) -> Dict[str, float]:
        """
        Evaluate output using all rubric dimensions
        Returns dict: {dimension -> score (0.0-1.0)}
        """
        scores = {}

        for criterion in self.rubric.criteria:
            # Create evaluation prompt
            eval_prompt = f"""You are an expert evaluator. Please score the following output.

Rubric Dimension: {criterion.dimension}
Description: {criterion.description}

Scoring Levels:
{chr(10).join(f"  {score}: {desc}" for score, desc in criterion.score_levels)}

Original Prompt: {prompt}

Output to Evaluate:
{output}

Based on the rubric, assign a score (1-5) for this dimension. Provide reasoning.
Format your response as:
SCORE: X
REASONING: ...
"""

            response = self.eval_model.generate(eval_prompt, max_length=200)

            # Parse score from response
            score_value = self._extract_score(response)
            # Normalize to 0-1
            normalized_score = score_value / 5.0
            scores[criterion.dimension] = normalized_score

        return scores

    def _extract_score(self, response: str) -> int:
        """Extract numeric score from LLM response"""
        import re
        match = re.search(r'SCORE:\s*(\d)', response)
        if match:
            return int(match.group(1))
        return 3  # Default middle score

    def compute_weighted_reward(self, dimension_scores: Dict[str, float]) -> float:
        """
        Combine dimension scores into single reward using weights
        """
        total_reward = 0.0
        total_weight = 0.0

        for criterion in self.rubric.criteria:
            score = dimension_scores.get(criterion.dimension, 0.5)
            total_reward += score * criterion.weight
            total_weight += criterion.weight

        # Normalize by total weight
        return total_reward / total_weight if total_weight > 0 else 0.0
```

### 3. Create Rubric Library

Build a library of rubrics for different tasks.

```python
class RubricLibrary:
    """
    Repository of rubrics for different domains
    """
    def __init__(self):
        self.rubrics = {}

    def register_rubric(self, task_name: str, rubric: Rubric):
        """Register a rubric for a task"""
        self.rubrics[task_name] = rubric

    def get_rubric(self, task_name: str) -> Rubric:
        """Retrieve rubric for task"""
        return self.rubrics.get(task_name)

    def create_rubric_from_template(self, task_description: str, llm_model):
        """
        Generate a rubric automatically from task description
        """
        prompt = f"""Create a detailed evaluation rubric for the following task:

Task: {task_description}

Provide 4-5 key dimensions for evaluation, each with:
- Dimension name
- Clear description
- 5-point scoring scale with level descriptions

Format as JSON:
{{
  "dimensions": [
    {{
      "name": "dimension_name",
      "description": "...",
      "levels": [
        {{"score": 1, "description": "..."}},
        ...
      ]
    }},
    ...
  ]
}}"""

        response = llm_model.generate(prompt, max_length=1000)

        # Parse JSON response
        import json
        try:
            rubric_spec = json.loads(response)
            criteria = []

            for dim in rubric_spec['dimensions']:
                levels = [(lev['score'], lev['description']) for lev in dim['levels']]
                criterion = RubricCriterion(
                    dimension=dim['name'],
                    description=dim['description'],
                    score_levels=levels,
                    weight=1.0 / len(rubric_spec['dimensions'])
                )
                criteria.append(criterion)

            return Rubric(task_description, criteria)
        except:
            # Fallback: return simple rubric
            return self._create_default_rubric()

    def _create_default_rubric(self) -> Rubric:
        """Fallback default rubric"""
        criteria = [
            RubricCriterion(
                "quality",
                "Overall quality of response",
                [(1, "Poor"), (2, "Fair"), (3, "Good"), (4, "Very Good"), (5, "Excellent")]
            ),
            RubricCriterion(
                "relevance",
                "Relevance to prompt",
                [(1, "Irrelevant"), (2, "Somewhat relevant"), (3, "Relevant"),
                 (4, "Highly relevant"), (5, "Perfect match")]
            )
        ]
        return Rubric("Default", criteria)
```

### 4. Train Model with Rubric-Based Rewards

Implement RL training using rubric rewards.

```python
import torch
import torch.nn as nn
from torch.optim import Adam

def train_with_rubric_rewards(model, train_prompts, rubric: Rubric,
                             eval_model, num_epochs=10, batch_size=16):
    """
    Train model using PPO with rubric-based rewards
    """
    optimizer = Adam(model.parameters(), lr=1e-5)
    scorer = RubricScorer(eval_model, rubric)

    for epoch in range(num_epochs):
        epoch_loss = 0.0
        num_batches = 0

        for batch_start in range(0, len(train_prompts), batch_size):
            batch_prompts = train_prompts[batch_start:batch_start + batch_size]

            # 1. Generate outputs from model
            outputs = []
            log_probs_list = []

            for prompt in batch_prompts:
                output = model.generate(prompt, max_length=256)
                outputs.append(output)

                # Compute log probability
                log_prob = model.compute_log_prob(output)
                log_probs_list.append(log_prob)

            # 2. Score outputs using rubric
            rewards = []
            for prompt, output in zip(batch_prompts, outputs):
                dimension_scores = scorer.score_output(prompt, output)
                reward = scorer.compute_weighted_reward(dimension_scores)
                rewards.append(reward)

            # 3. Compute policy gradient loss
            rewards_tensor = torch.tensor(rewards, device=model.device)
            log_probs_tensor = torch.stack(log_probs_list)

            # Normalize advantages
            advantages = (rewards_tensor - rewards_tensor.mean()) / (rewards_tensor.std() + 1e-8)

            # Policy loss: -log_prob * advantage
            loss = -(log_probs_tensor * advantages).mean()

            # 4. Update model
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()

            epoch_loss += loss.item()
            num_batches += 1

            if num_batches % 10 == 0:
                avg_reward = rewards_tensor.mean().item()
                print(f"Epoch {epoch}, Batch {num_batches}: Loss={loss:.4f}, Reward={avg_reward:.3f}")

        print(f"Epoch {epoch} completed. Avg Loss: {epoch_loss / num_batches:.4f}")
```

### 5. Implement Rubric-Guided Generation

Use rubric feedback during decoding to guide generation.

```python
class RubricGuidedGeneration:
    """
    Generate outputs with rubric guidance
    """
    def __init__(self, model, rubric: Rubric, eval_model):
        self.model = model
        self.rubric = rubric
        self.scorer = RubricScorer(eval_model, rubric)

    def generate_optimized(self, prompt: str, target_dimensions: Dict[str, float],
                          num_candidates=4):
        """
        Generate output optimized for specific rubric dimensions

        Args:
            prompt: input prompt
            target_dimensions: {dimension -> desired_score (0-1)}
            num_candidates: number of candidates to evaluate

        Returns:
            best_output: output optimized for target dimensions
        """
        candidates = []
        scores = []

        # Generate multiple candidates
        for _ in range(num_candidates):
            candidate = self.model.generate(
                prompt,
                max_length=256,
                temperature=0.7,
                do_sample=True
            )
            candidates.append(candidate)

            # Score candidate
            dimension_scores = self.scorer.score_output(prompt, candidate)

            # Compute match to target dimensions
            match_score = self._compute_target_match(dimension_scores, target_dimensions)
            scores.append(match_score)

        # Return best candidate
        best_idx = scores.index(max(scores))
        return candidates[best_idx]

    def _compute_target_match(self, actual_scores: Dict[str, float],
                             target_scores: Dict[str, float]) -> float:
        """
        Compute how well actual scores match target scores
        """
        match = 0.0
        for dimension, target in target_scores.items():
            actual = actual_scores.get(dimension, 0.5)
            # Score: 1 - distance from target
            match += 1.0 - abs(actual - target)

        return match / len(target_scores) if target_scores else 0.0
```

### 6. Evaluation and Validation

Evaluate rubric-trained models.

```python
def evaluate_rubric_trained_model(model, test_prompts, rubric: Rubric,
                                 eval_model):
    """
    Evaluate model trained with rubric rewards
    """
    scorer = RubricScorer(eval_model, rubric)

    all_scores = {dim: [] for dim in [c.dimension for c in rubric.criteria]}
    all_rewards = []

    for prompt in test_prompts:
        output = model.generate(prompt, max_length=256)

        # Score output
        dimension_scores = scorer.score_output(prompt, output)
        for dim, score in dimension_scores.items():
            all_scores[dim].append(score)

        # Weighted reward
        reward = scorer.compute_weighted_reward(dimension_scores)
        all_rewards.append(reward)

    # Report results
    print("Evaluation Results:")
    print("-" * 50)
    for dim, scores in all_scores.items():
        avg_score = sum(scores) / len(scores)
        print(f"  {dim}: {avg_score:.3f}")

    avg_reward = sum(all_rewards) / len(all_rewards)
    print(f"  Average Reward: {avg_reward:.3f}")

    return all_scores, all_rewards
```

## Practical Guidance

### Hyperparameters & Configuration

- **Rubric Dimensions**: 4-6 dimensions per task (too many = noisy reward)
- **Score Levels**: 4-5 levels per dimension (5-point scales most common)
- **Weights**: Balance weights to reflect importance (sum to 1.0)
- **Learning Rate**: 1e-5 to 5e-5 (conservative due to subjective reward noise)
- **Candidate Evaluation**: 4-8 candidates per prompt (larger pool = better selection)

### When to Use Rubric Anchors

- Tasks are subjective (writing, helpfulness, creativity)
- You want interpretable, controllable reward signals
- You have domain expertise to create rubrics
- You can afford LLM evaluation per training step
- Style/tone control is important

### When NOT to Use Rubric Anchors

- Tasks have clear binary correctness (code, math)
- Computational budget for LLM evaluation is limited
- You need real-time training (LLM evaluation is slow)
- Reward signals must be absolutely consistent
- Tasks don't benefit from nuanced evaluation

### Common Pitfalls

1. **Over-Specific Rubrics**: Rubrics that are too detailed confuse LLM evaluators. Keep criteria focused and distinct.
2. **Unstable LLM Evaluation**: Different LLM evaluators may score differently. Use consistent eval model.
3. **Conflicting Dimensions**: If rubric dimensions conflict (brevity vs. depth), training becomes unstable.
4. **Weight Mismatch**: If weights don't reflect actual task priority, model optimizes wrong objectives.
5. **No Manual Validation**: Don't assume LLM scores match human judgment. Validate on small set with humans.

## Reference

Reinforcement Learning with Rubric Anchors (2508.12790): https://arxiv.org/abs/2508.12790

Extend RL to open-ended tasks using structured rubrics as reward anchors, enabling fine-grained optimization of subjective dimensions without binary correctness requirements, with control over style and quality trade-offs.

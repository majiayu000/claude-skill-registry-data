---
name: self-rewarding-vlm
title: Self-Rewarding VLM via Reasoning Decomposition
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2508.19652
keywords: [vision-language-model, self-reward, decomposition, hallucination, visual-reasoning]
description: "Enable VLMs to self-assess visual perception accuracy through decomposed two-stage reasoning: perception generation then validation, eliminating external supervision dependency"
---

# Self-Rewarding VLM via Reasoning Decomposition

## Core Concept

Vision-SR1 decomposes VLM reasoning into two sequential stages: (1) visual perception generation that produces self-contained descriptions, and (2) language-based validation where the model re-answers questions using only the generated perception. This creates an internal consistency signal for self-reward without requiring external labels. The approach addresses critical VLM failure modes: visual hallucinations and language shortcuts.

## Architecture Overview

- **Stage 1 - Perception Generation**: Model describes visual content sufficiently to answer questions
- **Stage 2 - Validation Reasoning**: Model validates perception by answering questions using only generated text
- **Self-Reward Computation**: Consistency between original and perception-based answers provides reward signal
- **Decomposed Supervision**: Explicit intermediate guidance for visual reasoning quality
- **No External Dependency**: Eliminates need for human annotations or external reward models

## Implementation Steps

### Stage 1: Perception Generation Component

Train the model to generate self-contained visual descriptions.

```python
# Perception generation: describe visual content for downstream reasoning
import torch
from torch import nn
from typing import Dict, List, Tuple

class PerceptionGenerator(nn.Module):
    """Generate self-contained visual descriptions"""

    def __init__(self, model_dim: int = 4096):
        super().__init__()
        self.model_dim = model_dim

    def forward(
        self,
        image_embeddings: torch.Tensor,  # [batch, num_patches, vision_dim]
        question: str
    ) -> str:
        """
        Generate visual perception that's sufficient to answer question
        without referring back to the image.

        Example:
        Image: A dog on a beach
        Question: "What animal is in the image?"
        Perception: "There is a brown dog standing on sandy beach"
        """
        # In practice, this integrates with a VLM like CLIP/LLaVA
        # For this example, we outline the architecture:

        # Combine image and question
        vision_encoded = self.encode_vision(image_embeddings)
        question_encoded = self.encode_question(question)

        # Generate perception description
        perception = self.generate_perception(
            vision_encoded,
            question_encoded
        )

        return perception

    def encode_vision(self, image_embeddings: torch.Tensor) -> torch.Tensor:
        """Encode visual features"""
        return image_embeddings.mean(dim=1)  # Simplified pooling

    def encode_question(self, question: str) -> torch.Tensor:
        """Encode question text"""
        # In practice, use tokenizer + embedding layer
        return torch.randn(1, self.model_dim)  # Placeholder

    def generate_perception(
        self,
        vision: torch.Tensor,
        question: torch.Tensor
    ) -> str:
        """Generate perception description"""
        # Autoregressive generation from combined vision + question
        return "A clear visual description of the scene"
```

### Stage 2: Validation Through Perception-Only Reasoning

Re-answer questions using only the generated perception.

```python
# Validation: answer questions using perception as sole input
class PerceptionValidator(nn.Module):
    """Validate perception quality through consistency checking"""

    def __init__(self, model_dim: int = 4096):
        super().__init__()
        self.model_dim = model_dim

    def forward(
        self,
        perception_text: str,
        question: str
    ) -> str:
        """
        Answer question using ONLY perception text, not original image.
        If answer consistent with original, perception is accurate.
        """
        # Encode perception and question
        perception_encoded = self.encode_text(perception_text)
        question_encoded = self.encode_text(question)

        # Generate answer from perception alone
        answer_from_perception = self.generate_answer(
            perception_encoded,
            question_encoded
        )

        return answer_from_perception

    def encode_text(self, text: str) -> torch.Tensor:
        """Encode text"""
        return torch.randn(1, self.model_dim)  # Placeholder

    def generate_answer(
        self,
        perception: torch.Tensor,
        question: torch.Tensor
    ) -> str:
        """Generate answer from perception"""
        return "Answer based on perception"
```

### Stage 3: Self-Reward Computation

Compute reward signals from consistency between original and perception-based reasoning.

```python
# Self-reward: measure consistency of reasoning
class SelfRewardComputer:
    """Compute self-reward from reasoning consistency"""

    def __init__(self, similarity_metric="exact_match"):
        self.metric = similarity_metric

    def compute_reward(
        self,
        original_answer: str,
        perception_based_answer: str,
        image_perception: str,
        question: str
    ) -> Tuple[float, Dict]:
        """
        Compute reward signal from consistency.

        High reward if:
        1. Original and perception-based answers match
        2. Perception is detailed and relevant
        3. No hallucination in perception (implicit)
        """

        # Core consistency check
        consistency = self.compute_consistency(
            original_answer,
            perception_based_answer
        )

        # Perception quality check
        perception_quality = self.evaluate_perception_quality(
            image_perception,
            question
        )

        # Combined reward
        reward = 0.7 * consistency + 0.3 * perception_quality

        return reward, {
            "consistency": consistency,
            "perception_quality": perception_quality,
            "answer_match": original_answer == perception_based_answer
        }

    def compute_consistency(
        self,
        answer1: str,
        answer2: str
    ) -> float:
        """
        Measure if two answers are consistent.
        Range: [0, 1], higher = more consistent
        """
        if self.metric == "exact_match":
            return float(answer1.strip().lower() == answer2.strip().lower())

        elif self.metric == "semantic_similarity":
            # Use embedding similarity
            import difflib
            ratio = difflib.SequenceMatcher(
                None,
                answer1.lower(),
                answer2.lower()
            ).ratio()
            return ratio

        elif self.metric == "f1_score":
            # Token-level F1 for open-ended answers
            answer1_tokens = set(answer1.lower().split())
            answer2_tokens = set(answer2.lower().split())

            intersection = answer1_tokens & answer2_tokens
            if not (answer1_tokens | answer2_tokens):
                return 1.0
            return 2 * len(intersection) / (len(answer1_tokens) + len(answer2_tokens))

        return 0.5

    def evaluate_perception_quality(
        self,
        perception: str,
        question: str
    ) -> float:
        """
        Evaluate if perception is detailed and relevant to question.

        Checks for:
        - Sufficient detail (word count)
        - Relevance to question (keyword overlap)
        - Specific descriptions (not vague)
        """
        # Extract question keywords
        import re
        question_words = set(re.findall(r'\w+', question.lower()))
        question_words -= {'what', 'where', 'when', 'why', 'how', 'is', 'are'}

        # Check perception mentions
        perception_words = set(re.findall(r'\w+', perception.lower()))

        # Keyword coverage
        keyword_overlap = len(question_words & perception_words) / max(len(question_words), 1)

        # Detail level (rough heuristic)
        word_count = len(perception.split())
        detail_score = min(word_count / 50, 1.0)  # 50 words = max detail

        # Specificity (avoid vague terms)
        vague_terms = {'thing', 'stuff', 'something', 'it', 'that'}
        vagueness = len([w for w in perception.lower().split() if w in vague_terms]) / max(word_count, 1)

        quality = 0.4 * keyword_overlap + 0.4 * detail_score + 0.2 * (1 - vagueness)
        return min(quality, 1.0)
```

### Stage 4: Reinforcement Learning Training

Train the VLM using self-reward signals.

```python
# RL training with self-rewards
class VLMRLTrainer:
    """Train VLM using self-reward signals"""

    def __init__(self, vlm_model, learning_rate=1e-5):
        self.model = vlm_model
        self.optimizer = torch.optim.AdamW(vlm_model.parameters(), lr=learning_rate)
        self.perception_gen = PerceptionGenerator()
        self.validator = PerceptionValidator()
        self.reward_computer = SelfRewardComputer()

    def train_step(self, batch: Dict) -> Dict:
        """
        Single training step using self-reward RL.

        Process:
        1. Generate visual perception
        2. Answer question from image (original)
        3. Answer question from perception only (validation)
        4. Compute self-reward from consistency
        5. Update model with reward signal
        """
        images = batch["images"]
        questions = batch["questions"]
        original_answers = batch["answers"]

        all_rewards = []
        all_losses = []

        for image, question, original_answer in zip(
            images, questions, original_answers
        ):
            # Stage 1: Generate perception
            perception = self.perception_gen(image, question)

            # Stage 2: Validate with perception-only reasoning
            perception_answer = self.validator(perception, question)

            # Stage 3: Compute self-reward
            reward, diagnostics = self.reward_computer.compute_reward(
                original_answer,
                perception_answer,
                perception,
                question
            )

            all_rewards.append(reward)

            # Stage 4: Policy gradient update
            # Higher reward = increase likelihood of this trajectory
            log_prob = self.get_trajectory_log_prob(
                image,
                perception,
                perception_answer
            )

            loss = -(log_prob * reward)  # Policy gradient
            all_losses.append(loss)

        # Backward pass on average loss
        total_loss = torch.stack(all_losses).mean()
        self.optimizer.zero_grad()
        total_loss.backward()
        self.optimizer.step()

        return {
            "loss": total_loss.item(),
            "avg_reward": sum(all_rewards) / len(all_rewards),
            "rewards": all_rewards
        }

    def get_trajectory_log_prob(
        self,
        image,
        perception,
        answer
    ) -> torch.Tensor:
        """Compute log probability of trajectory"""
        # In practice, sum log probs of all tokens generated
        return torch.tensor(0.0)  # Placeholder
```

### Stage 5: Evaluation and Validation

Assess improvement in reasoning quality and hallucination reduction.

```python
# Evaluation framework
class VLMEvaluator:
    """Evaluate VLM improvements from self-reward training"""

    def __init__(self, vlm_model):
        self.model = vlm_model

    def evaluate_hallucination_rate(
        self,
        test_examples: List[Dict],
        num_eval: int = 500
    ) -> float:
        """
        Measure reduction in hallucinations.
        Hallucination = claiming something present that isn't in image
        """
        hallucinations = 0

        for example in test_examples[:num_eval]:
            image = example["image"]
            question = example["question"]
            ground_truth = example["answer"]

            # Generate answer
            generated = self.model.generate(image, question)

            # Check for hallucination (answer conflicts with ground truth)
            if not self.is_consistent(generated, ground_truth):
                hallucinations += 1

        hallucination_rate = hallucinations / num_eval
        return hallucination_rate

    def evaluate_reasoning_quality(
        self,
        test_examples: List[Dict]
    ) -> Dict:
        """
        Evaluate multi-step reasoning accuracy.
        """
        results = {
            "exact_match": 0,
            "semantic_match": 0,
            "partial_credit": 0
        }

        for example in test_examples:
            image = example["image"]
            question = example["question"]
            ground_truth = example["answer"]

            generated = self.model.generate(image, question)

            # Exact match
            if generated.strip().lower() == ground_truth.strip().lower():
                results["exact_match"] += 1
                results["semantic_match"] += 1
                results["partial_credit"] += 1

            # Semantic match
            elif self.semantic_similarity(generated, ground_truth) > 0.8:
                results["semantic_match"] += 1
                results["partial_credit"] += 1

            # Partial credit
            elif self.token_overlap(generated, ground_truth) > 0.5:
                results["partial_credit"] += 1

        # Normalize
        num_examples = len(test_examples)
        for key in results:
            results[key] /= num_examples

        return results

    def is_consistent(self, answer1: str, answer2: str) -> bool:
        return self.semantic_similarity(answer1, answer2) > 0.7

    def semantic_similarity(self, text1: str, text2: str) -> float:
        # Placeholder: in practice use embedding similarity
        return 0.5

    def token_overlap(self, text1: str, text2: str) -> float:
        tokens1 = set(text1.lower().split())
        tokens2 = set(text2.lower().split())
        intersection = tokens1 & tokens2
        union = tokens1 | tokens2
        return len(intersection) / len(union) if union else 0
```

## Practical Guidance

### Training Configuration

- **Perception Generation**: Temperature 0.7, max_length 100 tokens
- **Validation Reasoning**: Temperature 0.0 (deterministic for consistency)
- **Reward Scaling**: Normalize rewards to [-1, 1] for stability
- **Learning Rate**: 1e-5 for fine-tuning, 1e-6 for small changes

### Failure Modes to Watch

- **Hallucinated Perceptions**: Model invents details not in image
  - Mitigation: Weight perception quality score higher
- **Reward Collapse**: All examples receive high reward regardless of quality
  - Mitigation: Use diverse evaluation set, track variance
- **Language Shortcuts**: Model answers without understanding vision
  - Mitigation: Enforce perception-only validation

### When to Use

- Improving VLMs without expensive annotation
- Reducing visual hallucinations in multimodal models
- Scenarios with limited labeled data
- Tasks requiring visual understanding + reasoning

### When NOT to Use

- Models already well-calibrated on target domain
- Scenarios requiring external ground truth validation
- Real-time systems (self-reward adds computational overhead)

### Design Insights

The key insight is that consistency between perception-based and image-based answers reveals reasoning quality. If a model hallucinates details in perception, it won't be able to re-answer questions correctly from that perception. This creates natural pressure toward accurate perception generation without explicit supervision.

## Reference

Self-Rewarding VLM via Reasoning Decomposition. arXiv:2508.19652
- https://arxiv.org/abs/2508.19652

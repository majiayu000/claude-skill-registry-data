---
name: calm-reasoning
title: "CALM Before STORM: Corrective Adaptation of Reasoning Models with Expert Hints"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2510.04204
keywords: [reasoning-models, domain-adaptation, expert-guidance, data-synthesis, efficient-adaptation]
description: "Adapt large reasoning models for optimization tasks using expert-guided hint correction. Generate high-quality training data with minimal expert intervention (<2.6% token modification). Trigger: fine-tune reasoning models on domain-specific tasks without large supervised datasets."
---

# CALM Before STORM: Expert-Guided Reasoning Adaptation

## Core Concept

Large Reasoning Models (LRMs) possess advanced thinking capabilities but often fail on domain-specific tasks like optimization modeling. CALM (Corrective Adaptation with Lightweight Modification) enables efficient adaptation by leveraging an expert to identify reasoning flaws and provide corrective hints. The model then uses these hints to generate improved reasoning trajectories—requiring modification of fewer than 2.6% of tokens. This creates a high-quality synthetic dataset for fine-tuning that preserves the LRM's native reasoning patterns.

The key insight: An expert doesn't need to write complete solutions; pointing out flaws lets the LRM fix its own reasoning, preserving generalization.

## Architecture Overview

- **Expert-Guided Hint Generation**: Expert identifies reasoning mistakes and suggests corrections
- **Synthetic Data Generation**: LRM generates improved reasoning traces given hints
- **Two-Phase Adaptation**: Supervised fine-tuning followed by RL refinement
- **Token-Efficient**: <2.6% of tokens modified by expert across dataset
- **Scalable**: Works with modest expert effort and computational resources

## Implementation Steps

### 1. Identify and Annotate Reasoning Flaws

Expert review identifies where the baseline LRM's reasoning breaks down.

```python
class ReasoningFlawDetector:
    """
    Identify reasoning errors in LRM output.
    Expert marks flaws with corrective hints.
    """
    def __init__(self, lrm_model, domain_validator):
        self.model = lrm_model
        self.validator = domain_validator  # Domain-specific correctness check

    def detect_flaws_in_trace(self, problem, reasoning_trace):
        """
        Analyze reasoning trace for domain-specific errors.

        Args:
            problem: Problem statement
            reasoning_trace: Model's reasoning text

        Returns:
            List of (position, error_type, expert_hint)
        """
        flaws = []

        # Parse reasoning into logical steps
        steps = parsing_model.extract_steps(reasoning_trace)

        for step_idx, step in enumerate(steps):
            # Check step validity in domain
            step_validation = self.validator.validate_step(
                problem,
                step,
                prior_steps=steps[:step_idx]
            )

            if not step_validation["is_valid"]:
                flaw = {
                    "position": step_idx,
                    "error_type": step_validation["error_category"],
                    "original_step": step,
                    "expert_hint": None  # To be filled by expert
                }
                flaws.append(flaw)

        return flaws

    def expert_annotation_interface(self, problem, reasoning_trace, detected_flaws):
        """
        Present interface for expert to add corrective hints.

        Returns:
            Annotated flaws with expert hints
        """
        print(f"Problem: {problem}")
        print(f"Reasoning trace:\n{reasoning_trace}")
        print(f"\nDetected {len(detected_flaws)} flaws:")

        for flaw_id, flaw in enumerate(detected_flaws):
            print(f"\nFlaw {flaw_id}: {flaw['error_type']}")
            print(f"  Original: {flaw['original_step']}")

            # Expert provides corrective hint
            hint = input(f"  Hint for correction: ").strip()
            flaw["expert_hint"] = hint

        return detected_flaws
```

### 2. Implement Hint-Based Data Synthesis

Given hints, have the LRM generate improved reasoning traces.

```python
class SyntheticDataSynthesizer:
    """Generate high-quality reasoning traces using expert hints."""

    def __init__(self, lrm_model):
        self.model = lrm_model

    def synthesize_improved_trace(self, problem, original_trace, annotated_flaws):
        """
        Generate improved reasoning by providing hints at flaw locations.

        Args:
            problem: Problem statement
            original_trace: Model's initial reasoning
            annotated_flaws: List of flaws with expert hints

        Returns:
            Improved reasoning trace
        """
        # Build prompt with problem and hints at flaw locations
        prompt = f"Problem: {problem}\n\nReasoning with corrections:\n"

        # Rewrite trace with hints integrated
        steps = parsing_model.extract_steps(original_trace)

        for step_idx, step in enumerate(steps):
            # Check if this step has a flaw with hint
            flaw_hint = None
            for flaw in annotated_flaws:
                if flaw["position"] == step_idx:
                    flaw_hint = flaw["expert_hint"]
                    break

            if flaw_hint:
                # Provide hint and ask model to regenerate this step
                prompt += f"Step {step_idx}: {step}\n"
                prompt += f"  Correction hint: {flaw_hint}\n"
                prompt += f"  Improved step: "

                # Generate improved version
                improved = self.model.generate(
                    prompt,
                    max_tokens=100,
                    temperature=0.3
                )

                prompt += f"{improved}\n"
            else:
                # Step was correct
                prompt += f"Step {step_idx}: {step}\n"

        # Generate final improved reasoning
        final_trace = self.model.generate(
            prompt + "\n[Complete reasoning]:\n",
            max_tokens=1500,
            temperature=0.2
        )

        return final_trace

    def compute_token_modification_ratio(self, original, improved):
        """
        Calculate what fraction of tokens were changed.
        """
        orig_tokens = original.split()
        improved_tokens = improved.split()

        # Simple token-level edit distance
        from difflib import SequenceMatcher

        matcher = SequenceMatcher(None, orig_tokens, improved_tokens)
        matching_ratio = matcher.ratio()

        modification_ratio = 1.0 - matching_ratio
        return modification_ratio
```

### 3. Build Synthetic Training Dataset

Combine original problem, expert hints, and synthetic improved traces into training data.

```python
class SyntheticDataset:
    """Manages synthetic training data generation and storage."""

    def __init__(self, synthesizer, validator):
        self.synthesizer = synthesizer
        self.validator = validator
        self.data = []
        self.token_modification_stats = []

    def build_dataset_with_hints(self, problems, original_traces, num_examples=None):
        """
        Generate synthetic dataset for all examples.

        Args:
            problems: List of problem statements
            original_traces: Corresponding LRM reasoning traces
            num_examples: Limit to subset (for expert annotation)

        Returns:
            List of training examples
        """
        if num_examples is None:
            num_examples = len(problems)

        for idx in range(min(num_examples, len(problems))):
            problem = problems[idx]
            original_trace = original_traces[idx]

            # Detect flaws (automatic) and annotate (expert)
            detector = ReasoningFlawDetector(self.model, self.validator)
            detected_flaws = detector.detect_flaws_in_trace(
                problem,
                original_trace
            )

            if len(detected_flaws) == 0:
                # No flaws; use original trace
                improved_trace = original_trace
            else:
                # Expert annotates flaws
                annotated_flaws = detector.expert_annotation_interface(
                    problem,
                    original_trace,
                    detected_flaws
                )

                # Synthesize improved trace
                improved_trace = self.synthesizer.synthesize_improved_trace(
                    problem,
                    original_trace,
                    annotated_flaws
                )

            # Measure token modification
            mod_ratio = self.synthesizer.compute_token_modification_ratio(
                original_trace,
                improved_trace
            )
            self.token_modification_stats.append(mod_ratio)

            # Add to dataset
            example = {
                "problem": problem,
                "reasoning": improved_trace,
                "flaws_corrected": len(detected_flaws),
                "token_modification_ratio": mod_ratio
            }
            self.data.append(example)

            print(f"Example {idx}: {len(detected_flaws)} flaws, "
                  f"{mod_ratio*100:.1f}% tokens modified")

        return self.data

    def statistics(self):
        """Report dataset statistics."""
        print(f"\nDataset Statistics:")
        print(f"  Examples: {len(self.data)}")
        print(f"  Avg token modification: {np.mean(self.token_modification_stats)*100:.2f}%")
        print(f"  Max token modification: {np.max(self.token_modification_stats)*100:.2f}%")
```

### 4. Fine-Tune with Supervised + RL

Train the adapted model using both supervised learning and reinforcement learning.

```python
def finetune_lrm_with_synthetic_data(
    base_model,
    synthetic_dataset,
    validator,
    config
):
    """
    Two-phase fine-tuning: SFT then RL.
    """
    optimizer = torch.optim.Adam(base_model.parameters(), lr=2e-5)

    # Phase 1: Supervised Fine-Tuning on synthetic data
    print("Phase 1: Supervised Fine-Tuning")
    for epoch in range(config.sft_epochs):
        for example in synthetic_dataset.data:
            problem = example["problem"]
            improved_reasoning = example["reasoning"]

            # Generate and compute loss
            output = base_model.generate(
                problem,
                return_logits=True
            )

            # Token-level cross-entropy loss
            loss = compute_cross_entropy_loss(
                output["logits"],
                improved_reasoning
            )

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    # Phase 2: Reinforcement Learning for correctness
    print("\nPhase 2: Reinforcement Learning Refinement")
    for epoch in range(config.rl_epochs):
        for example in synthetic_dataset.data:
            problem = example["problem"]
            ground_truth = example.get("ground_truth")

            # Generate reasoning
            reasoning = base_model.generate(problem, max_tokens=1500)

            # Validate correctness
            validation = validator.validate_solution(
                problem,
                reasoning
            )

            reward = 1.0 if validation["is_correct"] else 0.0

            # Policy gradient loss
            log_prob = base_model.compute_log_prob(reasoning)
            loss = -reward * log_prob

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    return base_model
```

### 5. Evaluate Adapted Model

Assess performance on downstream tasks (STORM datasets: optimization modeling benchmarks).

```python
def evaluate_adapted_lrm(adapted_model, benchmark_datasets):
    """
    Evaluate CALM-adapted model on domain-specific benchmarks.
    """
    results = {}

    for benchmark_name, dataset in benchmark_datasets.items():
        correct = 0
        total = 0

        for example in dataset:
            problem = example["problem"]
            ground_truth = example["ground_truth"]

            # Generate solution
            reasoning = adapted_model.generate(
                problem,
                max_tokens=2000
            )

            # Extract final answer and check correctness
            extracted_answer = extract_answer(reasoning)
            if extracted_answer == ground_truth:
                correct += 1

            total += 1

        accuracy = correct / total * 100
        results[benchmark_name] = accuracy

        print(f"{benchmark_name}: {accuracy:.1f}%")

    return results
```

## Practical Guidance

**Hyperparameters:**
- **Expert annotation budget**: ~100-500 problems with identified flaws
- **Token modification threshold**: 2.6% on average (if higher, hints too vague)
- **SFT epochs**: 3-5 (avoid overfitting)
- **RL epochs**: 2-3 (refine for correctness)
- **Learning rate**: 2e-5 (smaller than pretraining)

**When to Use:**
- Domain-specific adaptation of reasoning models (optimization, planning)
- Limited supervised data available
- Expert access for hint generation
- Want to preserve generalization from pretraining

**When NOT to Use:**
- Building reasoning models from scratch (use pretraining)
- Tasks with abundant labeled training data (standard SFT sufficient)
- No expert domain knowledge available
- Requires frequent model retraining (hints are one-time)

## Reference

[CALM Before STORM: Corrective Adaptation of Large Language Models for Optimization Modeling](https://arxiv.org/abs/2510.04204) — arXiv:2510.04204

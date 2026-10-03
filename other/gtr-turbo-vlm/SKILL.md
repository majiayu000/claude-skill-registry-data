---
name: gtr-turbo-vlm
title: "GTR-Turbo: Merged Checkpoint as Free Teacher for Agentic VLM Training"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2512.13043
keywords: [vision-language, reinforcement-learning, teacher-free, distillation, checkpoint-merging]
description: "Eliminate expensive external teacher dependencies in VLM RL training via merged-checkpoint teachers. Uses TIES merging of historical RL checkpoints to create free, stable teacher models for step-level guidance—matching external teacher performance while reducing training time 50% and computational costs 60%."
---

## Overview

GTR-Turbo shows that effective VLM RL training doesn't require external teachers—historical checkpoint merging provides guidance automatically.

## Core Technique

**Checkpoint Merging via TIES:**

```python
class CheckpointMergingTeacher:
    def __init__(self, checkpoint_history):
        self.checkpoints = checkpoint_history
        self.merged_model = None

    def merge_checkpoints(self):
        """
        TIES merging: Trim, Elect Sign, Merge for stable teacher.
        """
        # Collect weight differences from reference
        weight_diffs = []
        for ckpt in self.checkpoints:
            diff = ckpt.weights - reference_model.weights
            weight_diffs.append(diff)

        # TIES: Element-wise analysis
        merged = reference_model.weights.clone()
        for param_name in merged.state_dict():
            # Collect this parameter across checkpoints
            param_diffs = [wd[param_name] for wd in weight_diffs]

            # Vote by sign (elect sign)
            signs = torch.sign(torch.stack(param_diffs))
            elected_sign = torch.mode(signs, dim=0).values

            # Average magnitude
            magnitudes = torch.abs(torch.stack(param_diffs))
            avg_magnitude = torch.mean(magnitudes, dim=0)

            # Merge: elected sign * average magnitude
            merged[param_name] = elected_sign * avg_magnitude

        self.merged_model = create_model_from_weights(merged)
        return self.merged_model
```

**Two-Step Guidance Using Merged Teacher:**

```python
def apply_merged_teacher_guidance(student_model, merged_teacher, trajectory):
    """
    Use merged teacher for step-level guidance without external costs.
    """
    # Option 1: Supervised fine-tuning on reasoning tokens
    teacher_logits = merged_teacher.forward(trajectory.input)
    student_logits = student_model.forward(trajectory.input)

    sft_loss = cross_entropy(student_logits, teacher_logits)

    # Option 2: Soft logit distillation
    distillation_loss = kl_divergence(
        softmax(student_logits),
        softmax(teacher_logits)
    )

    return sft_loss + 0.1 * distillation_loss
```

**Training Loop:**

```python
def gtr_turbo_training(base_vlm, data, num_iterations):
    checkpoints = []

    for iteration in range(num_iterations):
        # RL training step
        loss = reinforcement_learning_step(base_vlm, data)

        # Periodic checkpoint merging
        if iteration % 100 == 0:
            checkpoints.append(base_vlm.clone())
            merged_teacher = merge_checkpoints(checkpoints)

            # Use merged teacher for guidance
            guidance_loss = apply_merged_teacher_guidance(
                base_vlm, merged_teacher, data
            )

            # Total loss
            total_loss = loss + 0.1 * guidance_loss
            total_loss.backward()
```

## Performance

- Matches external teacher performance
- 50% training time reduction
- 60% computational cost reduction
- No external model dependency

## When to Use

Use when: VLM RL training, avoiding external teachers, cost-conscious training.

## References

- TIES checkpoint merging
- Historical weight averaging
- Merged model as stable teacher
- Self-improvement without external guidance

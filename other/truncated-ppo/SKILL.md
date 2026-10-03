---
name: truncated-ppo
title: "Truncated Proximal Policy Optimization"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2506.15050"
keywords: [policy-optimization, PPO, training-efficiency, reasoning, truncated-rollouts]
description: "T-PPO improves training efficiency via truncated rollouts and extended GAE, enabling batch continuity without waiting for full sequence completion."
---

# Truncated Proximal Policy Optimization

## Core Concept

Truncated PPO (T-PPO) enhances training efficiency for reasoning LLMs through truncated rollouts and extended generalized advantage estimation (EGAE). Rather than waiting for complete generation sequences before updating, T-PPO divides long sequences into fixed-window chunks and applies EGAE to compute advantages from incomplete trajectories. This approach maintains constant batch size through replacement of finished sequences while achieving 60% wall-clock time reduction and 2.5x training efficiency improvement without sacrificing convergence on mathematical reasoning tasks.

## Architecture Overview

- **Truncated Rollout Strategy**: Divide response generation into fixed-length windows rather than waiting for completion
- **Extended GAE (EGAE)**: Generalize advantage estimation to incomplete trajectories by assuming terminal value equals penultimate state value
- **Batch Continuity**: Replace finished sequences with new samples, maintaining constant batch size and GPU utilization
- **Token Filtering**: Selectively filter training tokens to enable independent policy/value optimization
- **Successive Batching**: Continuously feed new prompts while earlier ones still generate

## Implementation

### Step 1: Implement Truncated Rollout Strategy

Divide long sequences into manageable chunks:

```python
import torch
import torch.nn as nn
from typing import List, Dict

class TruncatedRolloutBuffer:
    """
    Manages truncated rollouts: divides generation into windows.
    """
    def __init__(self, window_size=128, max_total_length=512):
        self.window_size = window_size
        self.max_total_length = max_total_length

    def create_windows(self, prompt_ids, max_new_tokens):
        """
        Divide expected generation into fixed-length windows.

        Args:
            prompt_ids: [batch, prompt_len] token IDs
            max_new_tokens: maximum tokens to generate per prompt

        Returns:
            window_config: dict with window boundaries and settings
        """
        batch_size = prompt_ids.shape[0]
        num_windows = (max_new_tokens + self.window_size - 1) // self.window_size

        window_config = {
            'window_size': self.window_size,
            'num_windows': num_windows,
            'batch_size': batch_size,
            'max_new_tokens': max_new_tokens
        }

        return window_config

    def process_truncated_generation(self, prompt_ids, generation_outputs,
                                    window_idx):
        """
        Extract tokens for a specific generation window.

        Args:
            prompt_ids: [batch, prompt_len]
            generation_outputs: full generated sequences (may not be complete)
            window_idx: which window to extract

        Returns:
            window_tokens: [batch, window_size] tokens in this window
            is_complete: [batch] boolean indicating if sequence completed
        """
        start_idx = window_idx * self.window_size
        end_idx = (window_idx + 1) * self.window_size

        # Extract window
        window_tokens = generation_outputs[:, start_idx:end_idx]

        # Pad if incomplete
        if window_tokens.shape[1] < self.window_size:
            padding = torch.full(
                (window_tokens.shape[0], self.window_size - window_tokens.shape[1]),
                fill_value=0  # or pad token ID
            )
            window_tokens = torch.cat([window_tokens, padding], dim=1)

        # Check completion
        is_complete = (window_tokens != 0).sum(dim=1) < self.window_size

        return window_tokens, is_complete
```

### Step 2: Implement Extended GAE

Generalize GAE to incomplete trajectories:

```python
class ExtendedGeneralizedAdvantageEstimation:
    """
    Extended GAE: handles incomplete (truncated) trajectories.
    Key assumption: V(s_l) = V(s_{l-1}) for ungenerated states.
    """
    def __init__(self, gamma=0.99, gae_lambda=0.95):
        self.gamma = gamma
        self.gae_lambda = gae_lambda

    def compute_advantages_truncated(self, rewards, values, dones,
                                    trajectory_length):
        """
        Compute advantages assuming incomplete trajectories.

        Args:
            rewards: [batch, seq_len] rewards at each position
            values: [batch, seq_len] state value estimates
            dones: [batch, seq_len] episode termination flags
            trajectory_length: list of actual lengths per batch

        Returns:
            advantages: [batch, seq_len] advantage estimates
            returns: [batch, seq_len] return estimates
        """
        batch_size, seq_len = rewards.shape
        advantages = torch.zeros_like(rewards)
        gae = 0

        # Iterate backwards through time
        for t in reversed(range(seq_len)):
            if t == seq_len - 1:
                # Last position: assume next value equals current for ungenerated
                next_value = values[:, t].clone()
                # Check if trajectory continues beyond window
                next_non_terminal = 1 - dones[:, t]
            else:
                next_value = values[:, t + 1]
                next_non_terminal = 1 - dones[:, t]

            delta = (
                rewards[:, t] +
                self.gamma * next_value * next_non_terminal -
                values[:, t]
            )

            # GAE computation with temporal decay
            gae = (
                delta +
                self.gamma * self.gae_lambda * next_non_terminal * gae
            )

            advantages[:, t] = gae

        # Compute returns
        returns = advantages + values

        return advantages, returns

    def compute_advantages_complete(self, rewards, values, dones):
        """
        Standard GAE for completed trajectories (reference).
        """
        batch_size, seq_len = rewards.shape
        advantages = torch.zeros_like(rewards)
        gae = 0

        # Bootstrap from final value
        next_value = values[:, -1].clone()

        for t in reversed(range(seq_len)):
            if t == seq_len - 1:
                next_non_terminal = 1 - dones[:, t]
                next_value = values[:, t]
            else:
                next_non_terminal = 1 - dones[:, t]
                next_value = values[:, t + 1]

            delta = (
                rewards[:, t] +
                self.gamma * next_value * next_non_terminal -
                values[:, t]
            )

            gae = (
                delta +
                self.gamma * self.gae_lambda * next_non_terminal * gae
            )

            advantages[:, t] = gae

        returns = advantages + values

        return advantages, returns
```

### Step 3: Implement Token Filtering

Selectively filter tokens for optimization:

```python
class TokenFilter:
    """
    Filters training tokens to improve efficiency.
    """
    @staticmethod
    def filter_high_advantage(tokens, advantages, log_probs,
                             percentile_threshold=50):
        """
        Focus on tokens with high absolute advantage.

        Args:
            tokens: [batch, seq_len] token IDs
            advantages: [batch, seq_len] advantage estimates
            log_probs: [batch, seq_len] log probabilities
            percentile_threshold: keep tokens above this percentile

        Returns:
            filtered_mask: [batch, seq_len] boolean mask
        """
        # Compute percentile threshold
        advantage_threshold = torch.kthvalue(
            advantages.reshape(-1),
            int(advantages.numel() * (100 - percentile_threshold) / 100)
        ).values

        # Create mask
        filtered_mask = torch.abs(advantages) > advantage_threshold

        return filtered_mask

    @staticmethod
    def filter_redundant_tokens(log_probs, entropy_threshold=0.1):
        """
        Filter low-entropy (confident) tokens to reduce redundancy.

        Args:
            log_probs: [batch, seq_len, vocab_size]
            entropy_threshold: keep if entropy > threshold

        Returns:
            filtered_mask: [batch, seq_len] boolean mask
        """
        # Compute entropy
        probs = torch.softmax(log_probs, dim=-1)
        entropy = -(probs * torch.log(probs + 1e-8)).sum(dim=-1)

        # Filter
        filtered_mask = entropy > entropy_threshold

        return filtered_mask

    @staticmethod
    def filter_composite(advantages, log_probs, weight_advantage=0.7):
        """
        Combine multiple filtering criteria.
        """
        mask_advantage = TokenFilter.filter_high_advantage(
            None, advantages, None, percentile_threshold=40
        )

        mask_entropy = TokenFilter.filter_redundant_tokens(
            log_probs, entropy_threshold=0.15
        )

        # Weighted combination
        combined_mask = (
            weight_advantage * mask_advantage.float() +
            (1 - weight_advantage) * mask_entropy.float()
        ) > 0.5

        return combined_mask
```

### Step 4: Implement Successive Batching

Maintain constant batch size with continuous sampling:

```python
class SuccessiveBatchSampler:
    """
    Samples batches continuously, replacing finished sequences.
    Maintains constant batch size for GPU efficiency.
    """
    def __init__(self, prompt_dataset, batch_size=32, window_size=128):
        self.prompt_dataset = prompt_dataset
        self.batch_size = batch_size
        self.window_size = window_size
        self.current_idx = 0
        self.active_sequences = []

    def get_next_batch(self):
        """
        Return batch with new samples replacing finished ones.

        Returns:
            batch: dict with prompts, generation_states
        """
        batch = {
            'new_prompts': [],
            'in_progress': self.active_sequences.copy()
        }

        # Add new sequences to replace finished ones
        num_new_needed = self.batch_size - len(self.active_sequences)

        for _ in range(num_new_needed):
            if self.current_idx >= len(self.prompt_dataset):
                self.current_idx = 0  # Cycle through dataset

            prompt = self.prompt_dataset[self.current_idx]
            batch['new_prompts'].append(prompt)
            self.active_sequences.append({
                'prompt': prompt,
                'generated_tokens': [],
                'generation_step': 0
            })
            self.current_idx += 1

        return batch

    def update_generation_state(self, window_outputs, finished_mask):
        """
        Update tracking of in-progress generations.

        Args:
            window_outputs: [batch, window_size] generated tokens
            finished_mask: [batch] boolean indicating finished sequences
        """
        # Remove finished sequences
        self.active_sequences = [
            seq for i, seq in enumerate(self.active_sequences)
            if not finished_mask[i]
        ]
```

### Step 5: Implement T-PPO Training Loop

Complete training with truncation and successive batching:

```python
class TruncatedPPOTrainer:
    """
    Full T-PPO trainer with truncated rollouts and batch continuity.
    """
    def __init__(self, model, value_model, window_size=128, batch_size=32):
        self.model = model  # policy model
        self.value_model = value_model
        self.window_size = window_size
        self.batch_size = batch_size
        self.egae = ExtendedGeneralizedAdvantageEstimation()
        self.rollout_buffer = TruncatedRolloutBuffer(window_size)
        self.batch_sampler = SuccessiveBatchSampler(
            [], batch_size=batch_size, window_size=window_size
        )

    def training_step(self, batch_prompts, batch_responses, window_idx,
                     verification_fn):
        """
        Single training step on a generation window.

        Args:
            batch_prompts: [batch, prompt_len]
            batch_responses: [batch, total_len] responses generated so far
            window_idx: which window to train on
            verification_fn: function to verify answer correctness
        """
        # Extract window
        window_tokens, is_complete = self.rollout_buffer.process_truncated_generation(
            batch_prompts, batch_responses, window_idx
        )

        # Compute rewards based on verification
        rewards = torch.zeros(self.batch_size, self.window_size)

        for i in range(self.batch_size):
            response_text = self.model.tokenizer.decode(batch_responses[i])
            is_correct = verification_fn(response_text)

            # Sparse reward: only at end of window or completion
            if is_complete[i] or (window_idx == self.rollout_buffer.window_size - 1):
                rewards[i, -1] = 1.0 if is_correct else 0.0

        # Compute values using value model
        with torch.no_grad():
            value_outputs = self.value_model(window_tokens)
            values = value_outputs.squeeze(-1)  # [batch, window_size]

        # Compute advantages
        advantages, returns = self.egae.compute_advantages_truncated(
            rewards,
            values,
            ~is_complete.unsqueeze(1),  # dones flags
            self.window_size
        )

        # Get policy log probs
        policy_outputs = self.model(window_tokens)
        log_probs = policy_outputs.log_probs  # [batch, window_size]

        # Filter tokens if desired
        token_filter = TokenFilter()
        filter_mask = token_filter.filter_composite(
            advantages, policy_outputs.logits
        )

        # PPO loss with clipping
        ratio = torch.exp(log_probs - policy_outputs.old_log_probs)
        clipped_ratio = torch.clamp(ratio, 1 - 0.2, 1 + 0.2)

        loss_actor = -torch.min(
            ratio * advantages,
            clipped_ratio * advantages
        )[filter_mask].mean()

        # Value loss
        loss_value = torch.nn.functional.mse_loss(values, returns)

        # Total loss
        loss = loss_actor + 0.5 * loss_value

        return loss, {
            'actor_loss': loss_actor.item(),
            'value_loss': loss_value.item(),
            'filtered_fraction': filter_mask.float().mean().item()
        }

    def train_epoch(self, dataloader, num_epochs=1):
        """
        Train for one epoch with successive batching.
        """
        optimizer = torch.optim.Adam(
            list(self.model.parameters()) +
            list(self.value_model.parameters()),
            lr=1e-4
        )

        for epoch in range(num_epochs):
            epoch_loss = 0
            epoch_metrics = {}

            for batch_idx, (prompts, responses) in enumerate(dataloader):
                # Determine number of windows
                max_len = responses.shape[1]
                num_windows = (max_len + self.window_size - 1) // self.window_size

                # Train on each window
                for window_idx in range(num_windows):
                    loss, metrics = self.training_step(
                        prompts, responses, window_idx,
                        verification_fn=self._verify_correctness
                    )

                    optimizer.zero_grad()
                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(
                        list(self.model.parameters()) +
                        list(self.value_model.parameters()),
                        1.0
                    )
                    optimizer.step()

                    epoch_loss += loss.item()

                    for k, v in metrics.items():
                        if k not in epoch_metrics:
                            epoch_metrics[k] = []
                        epoch_metrics[k].append(v)

            # Log results
            avg_loss = epoch_loss / (len(dataloader) * num_windows)
            print(f"Epoch {epoch + 1}, Loss: {avg_loss:.4f}")

            for k, v in epoch_metrics.items():
                print(f"  {k}: {sum(v) / len(v):.4f}")

    def _verify_correctness(self, response_text):
        """Verify if response is correct (domain-specific)"""
        return True  # Placeholder
```

## Practical Guidance

- **Window Size**: Larger windows (256) reduce overhead but increase memory; start with 128
- **EGAE Assumption**: V(s_l) = V(s_{l-1}) works well empirically; validate on your tasks
- **Token Filtering**: Apply selectively; too aggressive filtering can bias updates
- **Batch Continuity**: Requires prompt dataset large enough to avoid repetition
- **Speedup Target**: Expect 2-3x speedup; measure actual wall-clock time, not just theoretical
- **Hyperparameters**: Use standard PPO settings (clip=0.2, GAE lambda=0.95); adjust window size first
- **Evaluation**: Benchmark on long-sequence reasoning tasks (AIME, MATH500, code generation)
- **Comparison**: Always compare to standard PPO on same tasks to validate efficiency gains

## Reference

Paper: arXiv:2506.15050
Key metrics: 60% wall-clock reduction, 2.5x training efficiency on math reasoning
EGAE improvement: Handles incomplete trajectories enabling continuous batching
Related work: PPO, GAE, policy optimization, training efficiency

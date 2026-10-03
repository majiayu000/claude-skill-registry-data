---
name: laser-self-reward
title: "LaSeR: Reinforcement Learning with Last-Token Self-Rewarding"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2510.14943"
keywords: [self-rewarding, reinforcement-learning, reasoning, verification, llm-training]
description: "Compute reasoning rewards from the model's own next-token probability distribution at solution end. Integrates verification-based feedback into single model without separate evaluator, enabling efficient RL training with minimal overhead."
---

# LaSeR: Self-Rewarding Reasoning through Last-Token Analysis

Separate reward models add computational overhead to RL training. LaSeR extracts reward signals from the model itself by analyzing the probability distribution over the next token at a solution's conclusion, aligning with verification quality without auxiliary models.

Core insight: at the end of a reasoning solution, the model's uncertainty about what comes next correlates with solution quality. By using this self-generated signal as reward, you get verification-based training in one model, reducing RL complexity while improving reasoning performance.

## Core Concept

**Last-Token Reward Signal**: After generating a complete solution, compute the log-probability of a special verification token at position N+1. This probability difference from baseline quantifies solution quality.

**Joint Optimization**: Simultaneously optimize reasoning quality and self-verification through shared model parameters, enabling efficient RL without separate reward models.

## Architecture Overview

- **Solution Generator**: Standard LLM generating reasoning traces
- **Self-Verifier**: Uses final position to compute confidence
- **Reward Computer**: Converts log-probabilities to training signal
- **RL Optimizer**: Updates both generation and verification jointly

## Implementation Steps

**Stage 1: Compute Last-Token Reward Signals**

Extract rewards from final token probabilities:

```python
import torch
import torch.nn as nn
from transformers import AutoModelForCausalLM, AutoTokenizer

class LastTokenRewardComputer:
    def __init__(self, model_name):
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Special tokens for verification
        self.correct_token_id = self.tokenizer.encode("[CORRECT]")[0]
        self.incorrect_token_id = self.tokenizer.encode("[INCORRECT]")[0]

    def compute_solution_reward(self, solution_tokens, kl_coeff=0.1):
        """
        Compute reward based on last-token self-rewarding.

        The key insight: at the solution's end, compute:
        reward = (logp[correct_token] - logp[incorrect_token]) / kl_coeff

        Args:
            solution_tokens: tensor of shape [batch, seq_len]
            kl_coeff: scaling coefficient for KL control

        Returns:
            rewards: scalar reward per sample
        """

        batch_size = solution_tokens.shape[0]
        rewards = []

        with torch.no_grad():
            # Get logits at final position (after solution)
            # Condition on full solution to get next-token distribution
            logits = self.model(solution_tokens).logits

            # Get logits at final position
            final_logits = logits[:, -1, :]  # [batch, vocab_size]

            # Compute log probabilities
            log_probs = torch.nn.functional.log_softmax(final_logits, dim=-1)

            # Extract log-probs for verification tokens
            correct_log_prob = log_probs[:, self.correct_token_id]
            incorrect_log_prob = log_probs[:, self.incorrect_token_id]

            # Compute reward: difference scaled by KL coefficient
            reward = (
                (correct_log_prob - incorrect_log_prob) / kl_coeff
            ).clamp(-5, 5)  # Clamp for stability

        return reward

    def compute_batch_rewards(self, solutions_batch):
        """
        Compute rewards for batch of solutions.
        """

        rewards = []

        for solution in solutions_batch:
            solution_tokens = torch.tensor(
                self.tokenizer.encode(solution)
            ).unsqueeze(0)

            reward = self.compute_solution_reward(solution_tokens)
            rewards.append(reward.item())

        return torch.tensor(rewards)
```

**Stage 2: RL Training with Last-Token Rewards**

Integrate self-reward into policy gradient training:

```python
def laser_training_loop(
    model,
    tokenizer,
    problem_dataloader,
    num_steps=5000,
    learning_rate=1e-5
):
    """
    Train model with last-token self-rewarding.
    """

    reward_computer = LastTokenRewardComputer(model)
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=learning_rate
    )

    for step in range(num_steps):
        # Sample problem batch
        problems = next(iter(problem_dataloader))
        problem_tokens = tokenizer(
            problems,
            return_tensors='pt',
            padding=True
        )['input_ids'].cuda()

        # Generate solutions with temperature sampling
        with torch.no_grad():
            # Generate multiple solutions per problem for exploration
            solutions_list = []

            for temp in [0.7, 1.0, 1.3]:
                solution_ids = model.generate(
                    problem_tokens,
                    max_length=512,
                    temperature=temp,
                    top_p=0.95,
                    do_sample=True
                )

                solutions_list.append(solution_ids)

        # Compute rewards for solutions
        all_rewards = []
        all_logprobs = []

        for solution_ids in solutions_list:
            # Compute self-reward
            rewards = reward_computer.compute_batch_rewards(
                [tokenizer.decode(sol) for sol in solution_ids]
            )

            all_rewards.append(rewards)

            # Compute log probabilities of solutions under current policy
            outputs = model(solution_ids, labels=solution_ids)
            logprobs = -outputs.loss.unsqueeze(0)  # Negative loss

            all_logprobs.append(logprobs)

        # Stack rewards and log probs
        all_rewards = torch.stack(all_rewards)  # [num_temps, batch]
        all_logprobs = torch.stack(all_logprobs)  # [num_temps, batch]

        # Select best solution per problem
        best_temp_idx = all_rewards.argmax(dim=0)
        best_rewards = all_rewards[
            best_temp_idx,
            torch.arange(all_rewards.shape[1])
        ]

        best_logprobs = all_logprobs[
            best_temp_idx,
            torch.arange(all_logprobs.shape[1])
        ]

        # Policy gradient: maximize expected reward
        policy_loss = -(best_logprobs * best_rewards).mean()

        # Auxiliary loss: train self-verification
        # Verify that model becomes better at predicting [CORRECT]
        # for correct solutions
        verify_loss = compute_verification_loss(
            model,
            solutions_list,
            best_rewards
        )

        # Combined loss
        total_loss = policy_loss + 0.1 * verify_loss

        # Update
        optimizer.zero_grad()
        total_loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()

        if step % 100 == 0:
            print(
                f"Step {step}, Policy Loss: {policy_loss:.4f}, "
                f"Mean Reward: {best_rewards.mean():.4f}"
            )

def compute_verification_loss(model, solutions_list, rewards):
    """
    Auxiliary loss to train self-verification capability.
    Model should predict high probability of [CORRECT] for good solutions.
    """

    # Flatten solutions and rewards
    all_solutions = []
    all_rewards = []

    for sol_batch, rew_batch in zip(solutions_list, rewards):
        for sol, rew in zip(sol_batch, rew_batch):
            all_solutions.append(sol)
            all_rewards.append(rew)

    all_rewards = torch.tensor(all_rewards)

    # Target: high probability of [CORRECT] for high-reward solutions
    # Normalize rewards to [0, 1] to use as soft targets
    normalized_rewards = (all_rewards - all_rewards.min()) / (
        all_rewards.max() - all_rewards.min() + 1e-8
    )

    # Compute verification loss
    verify_loss = 0.0

    for sol, target_conf in zip(all_solutions, normalized_rewards):
        # Get logits at final position
        logits = model(sol.unsqueeze(0)).logits[0, -1, :]
        correct_logit = logits[model.config.correct_token_id]

        # Cross-entropy with target confidence
        target = torch.tensor(target_conf)
        loss = torch.nn.functional.binary_cross_entropy_with_logits(
            correct_logit.unsqueeze(0),
            target.unsqueeze(0)
        )

        verify_loss = verify_loss + loss

    return verify_loss / len(all_solutions)
```

**Stage 3: Inference with Self-Guided Reasoning**

Generate solutions with self-verification guidance:

```python
def generate_with_self_guidance(
    model,
    problem,
    tokenizer,
    max_iterations=3,
    temperature=0.7
):
    """
    Generate solution with internal verification feedback.
    Iteratively refine based on self-reward signals.
    """

    best_solution = None
    best_reward = -float('inf')

    for iteration in range(max_iterations):
        # Generate solution
        problem_tokens = tokenizer.encode(problem)
        problem_tensor = torch.tensor(problem_tokens).unsqueeze(0).cuda()

        with torch.no_grad():
            solution_ids = model.generate(
                problem_tensor,
                max_length=512,
                temperature=temperature,
                do_sample=True,
                return_dict_in_generate=True,
                output_scores=True
            )

        # Decode solution
        solution = tokenizer.decode(solution_ids.sequences[0])

        # Compute self-reward
        reward_computer = LastTokenRewardComputer(model)
        reward = reward_computer.compute_batch_rewards([solution])[0]

        # Track best solution
        if reward > best_reward:
            best_reward = reward
            best_solution = solution

        # Adaptive temperature: increase for exploration if needed
        if reward < 0:
            temperature = min(temperature + 0.1, 1.5)

    return best_solution, best_reward.item()
```

## Practical Guidance

**When to Use LaSeR:**
- RL training where reward models are bottleneck
- Reasoning tasks with clear correctness signals
- Single-model deployment (no separate evaluator)

**When NOT to Use:**
- Tasks without clear verification tokens
- Multi-step RL where multiple reward signals needed
- Weak self-verification capability in base model

**Verification Token Design:**

| Approach | Pros | Cons |
|----------|------|------|
| Special tokens ([CORRECT]) | Clean, efficient | Requires vocab changes |
| Natural tokens ("right", "wrong") | No vocab changes | Noisy signal |
| Learned token embeddings | Flexible | Extra parameters |

**Common Pitfalls:**
- KL coefficient too large (weak rewards, slow learning)
- KL coefficient too small (unstable training)
- Not clamping rewards (extreme values destabilize)
- Verification tokens not well-represented in pretraining

**Typical Reward Scales:**

| Configuration | Reward Range | Training Stability |
|---------------|--------------|-------------------|
| KL coeff = 0.05 | [-100, 100] | Unstable |
| KL coeff = 0.1 | [-50, 50] | Stable |
| KL coeff = 0.2 | [-25, 25] | Very stable |

## Reference

Based on the research at: https://arxiv.org/abs/2510.14943

---
name: nabla-reasoner
title: "∇-Reasoner: LLM Reasoning via Test-Time Gradient Descent in Latent Space"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2603.04948"
keywords: [Inference Time Scaling, Reasoning, Gradient Descent, Reward Optimization, Latent Space Optimization]
description: "Improves LLM reasoning quality at inference time by optimizing token logits using gradient descent, combining reward model signals with KL-regularization. Bridges parametric training-time and non-parametric test-time scaling through token-level optimization."
---

# ∇-Reasoner: Achieving Better Reasoning Through Test-Time Gradient Descent on Token Logits

LLM reasoning during inference typically relies on sampling and rejection—generate multiple candidate responses and select based on reward. This zeroth-order search is inefficient in high-dimensional token spaces, especially for sparse reward landscapes. ∇-Reasoner reformulates inference-time reasoning as first-order optimization: instead of blind sampling, use gradients from reward and language models to refine token predictions during generation.

The key insight is that token logits are differentiable with respect to both the language model's likelihood and a learned reward function. By applying gradient descent to these logits, the model can iteratively improve reasoning quality while maintaining linguistic fluency through KL regularization.

## Core Concept

Standard decoding: x_1, x_2, ... ~ π_θ(·|prefix) (sample from fixed policy)

∇-Reasoner: Optimize logits using gradient descent on:

L = -R(x) + λ KL(π_optimized || π_θ)

where R(x) is reward from a learned reward model and KL regularization keeps logits close to the base model's predictions. This combines two objectives: maximize rewards while staying faithful to the base language model.

The optimization operates in logit space (differentiable) rather than discrete token space, enabling gradient-based refinement. After optimization, resample tokens from improved logit distributions.

## Architecture Overview

- **Token Logit Optimization**: Perform gradient descent on token logits at each generation step
- **Dual Objective**: Maximize reward while minimizing KL divergence from base model
- **Iterative Refinement**: Generate full trajectory, optimize, then resample with acceptance filtering
- **Gradient Caching**: Reuse gradients when token predictions stabilize to reduce computation
- **Rollout Sharing**: Leverage KV cache across steps to amortize cost

## Implementation Steps

Implement gradient-based optimization of token logits combined with rejection sampling for conservative updates.

**Base Gradient-Based Token Optimization**

```python
import torch
import torch.nn.functional as F

def optimize_token_logits_for_step(
    prompt,
    generated_prefix,
    logits_initial,
    reward_model,
    language_model,
    num_optimization_steps=5,
    learning_rate=0.01,
    kl_weight=1.0
):
    """
    Optimize logits for the next token using gradient descent.

    Args:
        prompt: [seq_len] token indices
        generated_prefix: [gen_len] previously generated tokens
        logits_initial: [vocab_size] logits from base model
        reward_model: callable returning scalar reward for a sequence
        language_model: base LLM (frozen, for KL reference)
        num_optimization_steps: gradient descent iterations
        learning_rate: step size for gradient updates
        kl_weight: coefficient for KL regularization

    Returns:
        logits_optimized: [vocab_size] improved logits
        gradient_cache: cached gradients for potential reuse
    """
    logits_opt = logits_initial.clone().detach().requires_grad_(True)
    optimizer = torch.optim.Adam([logits_opt], lr=learning_rate)

    # Reference logits (frozen)
    with torch.no_grad():
        logits_ref = language_model.get_logits(prompt, generated_prefix)

    best_loss = float('inf')
    best_logits = logits_opt.clone().detach()

    for step in range(num_optimization_steps):
        optimizer.zero_grad()

        # Sample a token from current logits
        probs = F.softmax(logits_opt, dim=0)
        token_sampled = torch.multinomial(probs, num_samples=1).item()

        # Build candidate sequence
        candidate_seq = torch.cat([prompt, generated_prefix, torch.tensor([token_sampled])])

        # Compute reward for this trajectory (expensive, so only for promising tokens)
        if probs[token_sampled] > 0.1:  # Only reward plausible tokens
            with torch.enable_grad():
                reward = reward_model(candidate_seq)
                reward_loss = -reward  # Maximize reward
        else:
            reward_loss = torch.tensor(0.0, device=logits_opt.device)

        # KL regularization: stay close to reference model
        kl_div = torch.sum(
            F.softmax(logits_ref, dim=0) * (F.log_softmax(logits_ref, dim=0) - F.log_softmax(logits_opt, dim=0))
        )

        # Total loss
        loss = reward_loss + kl_weight * kl_div

        # Gradient step
        loss.backward()
        optimizer.step()

        if loss.item() < best_loss:
            best_loss = loss.item()
            best_logits = logits_opt.clone().detach()

    return best_logits, None  # gradient_cache would store intermediate gradients


def resample_token_with_rejection(
    logits_optimized,
    logits_original,
    language_model_score,
    rejection_threshold=0.9
):
    """
    Resample token from optimized logits with acceptance filtering.

    Args:
        logits_optimized: [vocab_size] improved logits
        logits_original: [vocab_size] base model logits
        language_model_score: likelihood score from base model
        rejection_threshold: acceptance probability threshold

    Returns:
        token: selected token index
        accepted: whether token was accepted
    """
    probs_opt = F.softmax(logits_optimized, dim=0)
    probs_orig = F.softmax(logits_original, dim=0)

    # Sample candidate token
    token_candidate = torch.multinomial(probs_opt, num_samples=1).item()

    # Acceptance probability: ratio of optimized to original
    acceptance_prob = min(1.0, probs_opt[token_candidate].item() / (probs_orig[token_candidate].item() + 1e-10))

    # Accept if probability exceeds threshold
    accepted = torch.rand(1).item() < acceptance_prob

    return token_candidate, accepted
```

**Full Inference Loop with Trajectory-Level Optimization**

```python
class GradientDescentReasoner:
    def __init__(self, language_model, reward_model, kl_weight=1.0, optimize_every_n=1):
        self.language_model = language_model
        self.reward_model = reward_model
        self.kl_weight = kl_weight
        self.optimize_every_n = optimize_every_n  # Optimize every N tokens
        self.kv_cache = {}

    def generate_with_optimization(self, prompt, max_length=128, optimization_budget=50):
        """
        Generate sequence with iterative logit optimization.

        Args:
            prompt: initial token sequence [prompt_len]
            max_length: maximum generation length
            optimization_budget: total gradient steps allowed

        Returns:
            generated_sequence: [gen_len]
            rewards: list of rewards during generation
        """
        generated = []
        token_history = []
        rewards_trajectory = []
        steps_used = 0

        for gen_step in range(max_length):
            # Get base model logits
            with torch.no_grad():
                logits_base = self.language_model.get_logits(
                    prompt, torch.tensor(generated)
                )

            # Decide whether to optimize this step
            use_optimization = (gen_step % self.optimize_every_n == 0) and (steps_used < optimization_budget)

            if use_optimization:
                # Gradient-based optimization
                logits_opt, _ = optimize_token_logits_for_step(
                    prompt,
                    torch.tensor(generated),
                    logits_base,
                    self.reward_model,
                    self.language_model,
                    num_optimization_steps=min(5, optimization_budget - steps_used),
                    kl_weight=self.kl_weight
                )

                # Resample with rejection filtering
                token_new, accepted = resample_token_with_rejection(
                    logits_opt, logits_base, None
                )

                if not accepted:
                    # Fall back to base model sampling
                    token_new = torch.multinomial(F.softmax(logits_base, dim=0), 1).item()

                steps_used += 1
            else:
                # Standard sampling without optimization
                token_new = torch.multinomial(F.softmax(logits_base, dim=0), 1).item()

            generated.append(token_new)
            token_history.append((token_new, use_optimization))

            # Compute reward for trajectory (sparse, only occasionally)
            if len(generated) % 10 == 0 or gen_step == max_length - 1:
                with torch.no_grad():
                    full_seq = torch.cat([prompt, torch.tensor(generated)])
                    reward = self.reward_model(full_seq).item()
                    rewards_trajectory.append(reward)

        return generated, rewards_trajectory


def inference_with_gradient_acceleration(
    language_model,
    reward_model,
    prompt,
    temperature=0.7,
    optimization_frequency=2,  # Optimize every N tokens
    total_budget=100  # Max gradient steps
):
    """
    High-level interface for gradient-based reasoning.

    Args:
        language_model: base LLM
        reward_model: learned reward function
        prompt: input prompt
        temperature: sampling temperature
        optimization_frequency: apply optimization every N generations
        total_budget: gradient computation budget

    Returns:
        generated_text: optimized generation
    """
    reasoner = GradientDescentReasoner(
        language_model,
        reward_model,
        kl_weight=1.0,
        optimize_every_n=optimization_frequency
    )

    tokens, rewards = reasoner.generate_with_optimization(
        prompt,
        max_length=128,
        optimization_budget=total_budget
    )

    return tokens, rewards
```

## Practical Guidance

**Hyperparameters**:
- KL weight: 1.0 is typical; higher (2-5) keeps logits closer to base model; lower (0.1-0.5) prioritizes reward
- Learning rate: 0.001-0.01 for logit optimization; smaller = more conservative
- Optimization steps per token: 3-5 provides good quality/cost tradeoff
- Optimization frequency: Every token is expensive; every 2-3 tokens balances quality and cost

**When to Apply**:
- Complex reasoning tasks where base model struggles (math, planning)
- Scenarios with well-trained reward models (RL-trained models preferred)
- Tasks where inference time compute budget is available
- Problems requiring chain-of-thought reasoning with high quality

**When NOT to Apply**:
- Real-time applications with strict latency constraints
- Tasks with poorly calibrated reward models (bad signal worsens performance)
- Decoding where low latency is critical (adds 2-5x inference time)
- Simple tasks where base model already performs well

**Key Pitfalls**:
- KL weight too low—logits diverge from base model, producing gibberish
- Reward model poorly calibrated—optimization can exploit model weaknesses
- Optimization steps too few—insufficient refinement; too many—diminishing returns
- Not using rejection sampling—poor tokens slip through

**Acceleration Techniques**:
- **Gradient Caching**: Reuse gradients across steps when token predictions stabilize
- **Rollout Trajectory Reusing**: Share KV cache across multiple candidate trajectories
- **Selective Token Optimization**: Skip optimization for high-confidence tokens or easy positions

**Evidence**: Bridges parametric (training-time) and non-parametric (test-time) scaling; improves reasoning accuracy 5-15% on challenging benchmarks; proves equivalence to deamortized policy optimization via Wasserstein gradient flow.

Reference: https://arxiv.org/abs/2603.04948

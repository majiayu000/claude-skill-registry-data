---
name: pass-at-k-training
title: "Pass@k Training for Balancing Exploration and Exploitation"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2508.10751
keywords: [reinforcement-learning, pass-at-k, exploration, exploitation, reward-design]
description: "Use Pass@k as the reward metric in RL training to balance exploration and exploitation, enabling models to learn diverse sampling strategies while maintaining correctness."
---

# Pass@k Training for Balancing Exploration and Exploitation

## Core Concept

Traditional RL training for code/reasoning models uses Pass@1 as the reward: a binary signal indicating whether the first generated sample is correct. This encourages conservative, deterministic outputs.

Pass@k training instead uses Pass@k (the probability that at least one of k samples is correct) as the reward signal. This fundamentally changes the incentive structure: the model learns to maximize the diversity of solutions while maintaining correctness, balancing exploration and exploitation naturally.

The key insight from analysis is that exploration (diverse samples) and exploitation (high quality samples) are not conflicting—they mutually enhance each other when optimized via Pass@k.

## Architecture Overview

- **Pass@k Reward Signal**: Directly use Pass@k (1 - (1-p)^k where p is pass rate) as the reward instead of binary Pass@1
- **Analytical Advantage Function**: Derive an efficient way to compute policy gradients using Pass@k reward
- **Diversity Incentive**: Implicitly encourages models to generate diverse solutions since multiple different correct answers increase the Pass@k score
- **Exploration-Exploitation Balance**: Automatic balance emerges from the Pass@k objective—can't maximize Pass@k with purely deterministic policy
- **Verifiable Reward Framework**: Works within RLVR (RL with Verifiable Rewards) where correctness can be checked programmatically

## Implementation Steps

### 1. Set Up Verifiable Reward Function

Define a function that checks correctness of outputs. This is typically code execution verification or test case evaluation.

```python
def verify_correctness(response, problem_id, test_cases, execution_fn):
    """
    Verify if generated response (code, solution) is correct.
    Returns 1.0 if correct, 0.0 otherwise.
    """
    try:
        # Execute generated code on test cases
        results = []
        for test_input, expected_output in test_cases[problem_id]:
            actual_output = execution_fn(response, test_input)
            results.append(actual_output == expected_output)

        # Return 1.0 if passes all tests, 0.0 otherwise
        is_correct = all(results)
        return 1.0 if is_correct else 0.0
    except Exception:
        return 0.0

# Example: code generation task
test_cases = {
    'problem_1': [
        ('input1', 'expected1'),
        ('input2', 'expected2'),
    ],
    'problem_2': [
        # ... more test cases
    ]
}
```

### 2. Collect Multiple Samples per Problem

Generate k samples from the policy for each problem. Each sample can be correct or incorrect.

```python
def sample_k_responses(model, problem, k=4, temperature=0.8):
    """
    Generate k diverse responses from the model for a single problem
    """
    responses = []
    for _ in range(k):
        response = model.generate(
            problem,
            max_length=512,
            temperature=temperature,
            do_sample=True,
            top_p=0.95
        )
        responses.append(response)

    return responses

def evaluate_batch(model, problems, k=4, test_cases=None):
    """
    Evaluate k samples per problem and compute correctness
    """
    all_responses = []
    all_rewards = []

    for problem_id, problem_text in enumerate(problems):
        # Generate k samples
        responses = sample_k_responses(model, problem_text, k=k)
        all_responses.append(responses)

        # Verify correctness for each sample
        rewards = []
        for response in responses:
            correct = verify_correctness(response, problem_id, test_cases, execute_code)
            rewards.append(correct)

        all_rewards.append(rewards)

    return all_responses, all_rewards
```

### 3. Compute Pass@k Reward

Calculate Pass@k score for each problem: the probability that at least one of k samples is correct.

```python
def compute_pass_at_k(rewards, k):
    """
    Compute Pass@k score given correctness of k samples.

    Args:
        rewards: [batch_size, k] binary correctness for each of k samples
        k: number of samples

    Returns:
        pass_at_k: [batch_size] Pass@k score in [0, 1]
    """
    batch_size = rewards.shape[0]
    pass_at_k = torch.zeros(batch_size, device=rewards.device)

    for i in range(batch_size):
        # Pass@k = 1 - (1 - p)^k where p is fraction of correct samples
        num_correct = rewards[i].sum().item()
        p = num_correct / k

        pass_at_k_score = 1.0 - (1.0 - p) ** k
        pass_at_k[i] = pass_at_k_score

    return pass_at_k
```

### 4. Design Advantage Function for Pass@k

Derive the advantage for each individual sample based on how it contributes to Pass@k.

```python
def compute_pass_at_k_advantage(rewards, sample_idx, k):
    """
    Compute advantage for a single sample.

    Analytical insight: A correct sample has advantage based on how much
    it improves Pass@k. An incorrect sample has negative advantage if the
    policy's base Pass@k is high.

    Args:
        rewards: [k] correctness for k samples (binary)
        sample_idx: which sample to compute advantage for
        k: number of samples

    Returns:
        advantage: scalar advantage for this sample
    """
    is_correct = rewards[sample_idx].item()
    num_correct = rewards.sum().item()
    num_incorrect = k - num_correct

    if is_correct:
        # Correct sample increases Pass@k
        # Advantage = probability of improving Pass@k when this sample is removed
        if num_correct == 1:
            # This is the only correct sample
            # Removing it reduces Pass@k to 0
            p_without = 0.0
        else:
            # Other correct samples still exist
            p_without = 1.0 - (1.0 - (num_correct - 1) / k) ** k
            p_without = (num_correct - 1) / k

        pass_at_k_baseline = 1.0 - (1.0 - num_correct / k) ** k
        p_with = 1.0  # With this sample, at least 1 is correct

        advantage = (pass_at_k_baseline - p_with + 1.0) / k
    else:
        # Incorrect sample decreases Pass@k if it's the only option
        pass_at_k_baseline = 1.0 - (1.0 - num_correct / k) ** k

        # If this incorrect sample is removed, Pass@k unchanged
        advantage = -pass_at_k_baseline / k

    return advantage

def compute_pass_at_k_advantages(rewards):
    """
    Compute advantages for all k samples based on Pass@k contribution.
    """
    k = rewards.shape[0]
    advantages = torch.zeros_like(rewards, dtype=torch.float32)

    for sample_idx in range(k):
        advantages[sample_idx] = compute_pass_at_k_advantage(rewards, sample_idx, k)

    # Normalize advantages
    advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

    return advantages
```

### 5. Policy Gradient Update with Pass@k

Compute policy gradients using Pass@k advantages and update the model.

```python
def compute_pass_at_k_loss(model, problems, responses, rewards, k=4):
    """
    Compute loss for Pass@k training using policy gradient.
    """
    batch_size = len(problems)
    total_loss = 0.0

    for problem_idx in range(batch_size):
        problem_text = problems[problem_idx]
        problem_responses = responses[problem_idx]  # k responses
        problem_rewards = rewards[problem_idx]  # k correctness values

        # Compute advantages based on Pass@k contribution
        advantages = compute_pass_at_k_advantages(torch.tensor(problem_rewards))

        # Compute log probabilities for each response
        for sample_idx, response in enumerate(problem_responses):
            # Get log probability of this response under current policy
            input_ids = tokenizer.encode(problem_text)
            output_ids = tokenizer.encode(response)

            logits = model(input_ids).logits
            log_probs = F.log_softmax(logits, dim=-1)

            # Sum log probs for all tokens in response
            response_log_prob = 0.0
            for token_idx, token_id in enumerate(output_ids):
                if token_idx < len(logits):
                    response_log_prob += log_probs[token_idx, token_id]

            # Policy gradient: -log_prob * advantage
            # (negative because optimizer minimizes loss)
            sample_loss = -response_log_prob * advantages[sample_idx]
            total_loss += sample_loss

    return total_loss / batch_size
```

### 6. Training Loop with Pass@k Reward

Implement the full training loop that periodically samples, evaluates, and updates.

```python
def train_pass_at_k(model, train_problems, test_cases, num_epochs=10, k=4):
    """
    Train model using Pass@k as reward signal
    """
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=num_epochs)

    for epoch in range(num_epochs):
        epoch_loss = 0.0
        num_batches = 0

        for problem_batch in batch_iterator(train_problems):
            # 1. Sample k responses per problem
            responses, rewards = evaluate_batch(
                model, problem_batch, k=k, test_cases=test_cases
            )

            # 2. Compute Pass@k for each problem
            rewards_tensor = torch.tensor(rewards, dtype=torch.float32)
            pass_at_k_scores = compute_pass_at_k(rewards_tensor, k)

            # 3. Compute loss with Pass@k advantages
            loss = compute_pass_at_k_loss(model, problem_batch, responses, rewards, k=k)

            # 4. Update model
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()

            epoch_loss += loss.item()
            num_batches += 1

            if num_batches % 10 == 0:
                avg_pass_at_k = pass_at_k_scores.mean().item()
                print(f"Epoch {epoch}, Batch {num_batches}")
                print(f"  Loss: {loss:.4f}, Pass@{k}: {avg_pass_at_k:.4f}")

        scheduler.step()
        print(f"Epoch {epoch} Average Loss: {epoch_loss / num_batches:.4f}")
```

## Practical Guidance

### Hyperparameters & Configuration

- **k Value**: 4-8 for standard training; higher k improves exploration but increases computation
- **Temperature**: 0.7-0.9 for diverse sampling; controls randomness during generation
- **Learning Rate**: 5e-5 to 2e-4 (slightly higher than standard RL due to Pass@k signal)
- **Batch Size**: 16-32 problem batches (each with k samples, so 64-256 total generations)
- **Advantage Normalization**: Always normalize advantages per problem to prevent extreme gradients

### When to Use Pass@k Training

- You have verifiable correctness signals (code execution, test cases)
- You want models that generate diverse correct solutions
- You're training reasoning or code generation models
- Inference will sample multiple solutions and use the best one
- Balancing quality and diversity is important

### When NOT to Use Pass@k Training

- You can only evaluate correctness without test cases (e.g., open-ended generation)
- Single high-quality answer is essential (diversity unwanted)
- Computational budget doesn't allow k samples per problem
- Your correctness signal is unreliable or noisy
- You need online RL (every generation is deployed immediately)

### Common Pitfalls

1. **Too Few Samples (k < 4)**: Insufficient to learn diversity. Pass@k improvement plateaus below k=4.
2. **Mismatched Advantage Scaling**: If advantages aren't normalized, training becomes unstable. Always normalize per-problem.
3. **Low Temperature During Sampling**: If temperature is too low, samples aren't diverse; Pass@k signal becomes meaningless.
4. **Ignoring Correctness Verification**: Invalid verification function ruins training. Test on small set first.
5. **No Baseline Model**: Compare against Pass@1 training to ensure Pass@k actually improves your metric.

## Reference

Pass@k Training (2508.10751): https://arxiv.org/abs/2508.10751

Using Pass@k as the reward metric in RL training enables models to learn diverse solution generation while maintaining correctness, naturally balancing exploration and exploitation through analytical advantage functions.

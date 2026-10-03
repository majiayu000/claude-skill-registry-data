---
name: simko-pass-k
title: "SimKO: Simple Pass@K Policy Optimization"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2510.14807"
keywords: [pass-k, policy-optimization, diverse-generation, reinforcement-learning, reasoning]
description: "Improve pass@K by using asymmetric probability boosting: increase probabilities of top-K correct solutions while penalizing top-1 incorrect predictions. Focus boosting on high-entropy tokens where exploration helps most."
---

# SimKO: Asymmetric Policy Optimization for Solution Diversity

Standard RL training for LLMs focuses on single correct answers, reducing diversity in generated solutions. SimKO recognizes that models benefit from learning multiple solution paths and uses asymmetric training: boosting correct solutions broadly while aggressively penalizing top-1 incorrect predictions to encourage alternatives.

Core insight: overfitting to single solutions suppresses diversity. By asymmetrically training—rewarding diverse correct paths while blocking top-1 wrong paths—models maintain quality while improving pass@K for reasoning tasks.

## Core Concept

**Asymmetric Probability Shaping**: Boost probabilities of all top-K correct solutions, but only penalize top-1 incorrect predictions. This encourages diversity while avoiding solution pollution.

**High-Entropy Focus**: Apply asymmetric training primarily to high-entropy tokens where uncertainty creates opportunity for diverse reasoning branches.

## Architecture Overview

- **Solution Generator**: Standard LLM generating multiple outputs
- **Correctness Verifier**: Checks solution correctness
- **Entropy Monitor**: Identifies high-uncertainty decision points
- **Asymmetric Optimizer**: Applies differential training based on correctness and entropy

## Implementation Steps

**Stage 1: Multi-Solution Generation and Verification**

Generate and verify multiple solutions:

```python
import torch
import torch.nn as nn
import numpy as np

class MultiSolutionGenerator:
    def __init__(self, model_name, num_samples=8):
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name
        )

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.num_samples = num_samples
        self.verifier = SolutionVerifier()

    def generate_solutions(
        self,
        problem,
        temperature=0.8,
        max_length=512
    ):
        """
        Generate multiple solutions via sampling.
        """

        input_ids = self.tokenizer.encode(
            problem,
            return_tensors='pt'
        )

        solutions = []
        logprobs = []

        for _ in range(self.num_samples):
            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids,
                    max_length=max_length,
                    temperature=temperature,
                    do_sample=True,
                    return_dict_in_generate=True,
                    output_scores=True
                )

                solution_ids = outputs.sequences[0]
                solution_logprobs = sum(
                    score.log().item()
                    for score in outputs.scores
                )

            solution_text = self.tokenizer.decode(solution_ids)
            solutions.append(solution_text)
            logprobs.append(solution_logprobs)

        return solutions, logprobs

    def verify_solutions(self, problem, solutions):
        """
        Verify correctness of each solution.
        """

        results = []

        for solution in solutions:
            is_correct = self.verifier.check_solution(
                problem,
                solution
            )

            results.append(is_correct)

        return results

class SolutionVerifier:
    def check_solution(self, problem, solution):
        """
        Verify solution correctness.
        (Problem-specific verification logic)
        """

        # For math problems: parse and evaluate
        # For logic: check consistency
        # For code: execution test
        # This is domain-specific

        return True  # Placeholder
```

**Stage 2: Entropy-Aware Asymmetric Training**

Apply differential training based on correctness and entropy:

```python
def compute_token_entropy(logits):
    """
    Compute entropy of token probability distribution.
    """

    probs = torch.softmax(logits, dim=-1)
    entropy = -(probs * torch.log(probs + 1e-10)).sum(dim=-1)

    return entropy

def simko_training_step(
    model,
    problem,
    solutions,
    logprobs,
    correctness,
    optimizer,
    entropy_threshold=0.7
):
    """
    Single training step with SimKO asymmetric optimization.
    """

    # Re-encode solutions to get token-level logits
    problem_ids = model.tokenizer.encode(problem)
    problem_tokens = torch.tensor(problem_ids).unsqueeze(0)

    losses = []

    for solution_idx, (solution, is_correct) in enumerate(
        zip(solutions, correctness)
    ):
        solution_ids = model.tokenizer.encode(solution)
        full_ids = torch.cat(
            [problem_tokens, torch.tensor(solution_ids).unsqueeze(0)],
            dim=-1
        )

        # Forward pass: get logits for all tokens
        with torch.no_grad():
            outputs = model(full_ids, return_dict=True)
            logits = outputs.logits[0]

        # Compute entropy at each token position
        entropy = compute_token_entropy(logits)
        high_entropy_mask = (
            entropy > np.percentile(
                entropy.cpu().numpy(),
                entropy_threshold * 100
            )
        )

        # Get log probabilities for solution tokens
        solution_logprobs = []

        for token_idx, token_id in enumerate(solution_ids):
            # Map token position in full sequence
            full_pos = len(problem_ids) + token_idx

            logits_at_pos = logits[full_pos]
            log_prob = torch.nn.functional.log_softmax(
                logits_at_pos,
                dim=-1
            )[token_id]

            solution_logprobs.append(log_prob)

        # Asymmetric training
        if is_correct:
            # For correct solutions: boost all top-K paths
            # Increase probability of entire solution
            loss = -torch.stack(solution_logprobs).sum()

            # Additional boost for high-entropy tokens
            # (these are where we want diversity)
            high_entropy_logprobs = [
                lp for lp, high_ent in zip(
                    solution_logprobs,
                    high_entropy_mask
                )
                if high_ent
            ]

            if high_entropy_logprobs:
                diversity_bonus = torch.stack(
                    high_entropy_logprobs
                ).sum()

                loss = loss - 0.5 * diversity_bonus

        else:
            # For incorrect solutions: penalize top-1 path
            # Only block the most likely alternative
            top_loss_logprobs = sorted(
                solution_logprobs,
                reverse=True
            )[:3]  # Block top-3 most likely tokens

            loss = torch.stack(top_loss_logprobs).sum()

            # But only aggressively on high-entropy tokens
            # to avoid blocking valid paths
            high_entropy_top_logprobs = [
                lp for lp, high_ent in zip(
                    sorted(solution_logprobs, reverse=True),
                    sorted(high_entropy_mask.cpu().numpy(), reverse=True)
                )
                if high_ent
            ]

            if high_entropy_top_logprobs:
                loss = loss + torch.stack(
                    high_entropy_top_logprobs
                ).sum()

        losses.append(loss)

    # Backprop
    total_loss = torch.stack(losses).mean()

    optimizer.zero_grad()
    total_loss.backward()
    optimizer.step()

    return total_loss.item()
```

**Stage 3: Training Loop with Pass@K Evaluation**

Implement full training with pass@K metric:

```python
def simko_training_loop(
    model,
    problem_dataloader,
    num_epochs=5,
    num_samples_per_problem=8,
    learning_rate=1e-5
):
    """
    Train with SimKO for improved pass@K.
    """

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=learning_rate
    )

    generator = MultiSolutionGenerator(model, num_samples_per_problem)

    for epoch in range(num_epochs):
        total_loss = 0.0

        for batch_idx, batch in enumerate(problem_dataloader):
            problems = batch['problems']

            for problem in problems:
                # Generate multiple solutions
                solutions, logprobs = generator.generate_solutions(
                    problem,
                    temperature=0.7
                )

                # Verify correctness
                correctness = generator.verify_solutions(
                    problem,
                    solutions
                )

                # Training step
                loss = simko_training_step(
                    model,
                    problem,
                    solutions,
                    logprobs,
                    correctness,
                    optimizer,
                    entropy_threshold=0.75
                )

                total_loss += loss

            # Evaluate pass@K
            if batch_idx % 10 == 0:
                pass_at_k = evaluate_pass_at_k(
                    model,
                    generator,
                    batch,
                    k=4
                )

                avg_loss = total_loss / (batch_idx + 1)

                print(
                    f"Epoch {epoch}, Batch {batch_idx}, "
                    f"Loss: {avg_loss:.4f}, "
                    f"Pass@4: {pass_at_k:.4f}"
                )

def evaluate_pass_at_k(model, generator, problems, k=4):
    """
    Evaluate pass@k metric.
    """

    correct_count = 0
    total = 0

    for problem in problems['problems']:
        solutions, _ = generator.generate_solutions(
            problem,
            temperature=0.7
        )

        correctness = generator.verify_solutions(
            problem,
            solutions[:k]
        )

        if any(correctness):
            correct_count += 1

        total += 1

    return correct_count / total if total > 0 else 0.0
```

## Practical Guidance

**When to Use SimKO:**
- Reasoning tasks with multiple valid solutions (math, logic)
- Improving pass@K metric specifically
- Models that tend to converge to single solution

**When NOT to Use:**
- Tasks with single correct answer (generation, translation)
- Models already generating diverse solutions
- Verification function unreliable

**Entropy Threshold Tuning:**

| Threshold | Effect | Best For |
|-----------|--------|----------|
| 0.5 | Only strongest decision points | Subtle adjustments |
| 0.7 | Moderate uncertainty | Standard setting |
| 0.9 | Broad exploration | Weak diversity baseline |

**Asymmetry Strength:**

| Correct Boost | Wrong Penalty | Pass@K Gain |
|---------------|---------------|------------|
| 0.3x | 0.5x | +2% |
| 0.5x | 1.0x | +4-5% |
| 1.0x | 2.0x | +6-8% |

**Common Pitfalls:**
- Entropy threshold too strict (miss good decision points)
- Asymmetry too strong (suppresses correct paths)
- Verification function noisy (trains on wrong signals)
- Not focusing on high-entropy tokens (wasted training)

## Reference

Based on the research at: https://arxiv.org/abs/2510.14807

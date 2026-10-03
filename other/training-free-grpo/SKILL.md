---
name: training-free-grpo
title: "Training-Free Group Relative Policy Optimization via Token Priors"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2510.08191
keywords: [policy-optimization, parameter-free, token-priors, efficient-rl, semantic-advantage]
description: "Improve LLM outputs without parameter updates using learned token priors that guide inference. Trigger: optimize agent behavior in deployment without model retraining or fine-tuning."
---

# Training-Free Group Relative Policy Optimization

## Core Concept

Traditional GRPO requires expensive parameter updates through RL training. Training-Free GRPO achieves similar policy optimization by learning experiential knowledge as token priors—probability boosts applied at inference time—rather than modifying model parameters. This enables rapid deployment-time optimization using minimal ground-truth data (dozens of examples) while maintaining model integrity and enabling easy rollback.

The key insight: Semantic advantage signals (which outputs are better) can guide inference through learned token distributions without touching model weights.

## Architecture Overview

- **Token Prior Learning**: Distill group advantage into inference-time token probability shifts
- **Multi-Epoch Learning**: Iterative refinement of token priors from small seed data
- **Inference-Time Application**: Apply learned priors during generation without retraining
- **Semantic Advantage**: Relative preference signals, not absolute rewards
- **Minimal Data Requirements**: Works with <100 ground-truth examples

## Implementation Steps

### 1. Collect Initial Preference Data

Generate multiple outputs and identify high-quality ones without dense rewards.

```python
class PreferenceDataCollector:
    """Collect preference data from model outputs."""

    def __init__(self, model, num_candidates=4):
        self.model = model
        self.num_candidates = num_candidates

    def collect_preference_group(self, prompt):
        """
        Generate k candidates and rank them by quality.

        Args:
            prompt: Input prompt

        Returns:
            Ranked outputs with quality scores
        """
        candidates = []

        # Generate multiple candidates
        for _ in range(self.num_candidates):
            output = self.model.generate(
                prompt,
                max_tokens=256,
                temperature=0.8
            )
            candidates.append(output)

        # Rank by quality (multiple metrics)
        rankings = []
        for candidate in candidates:
            quality = compute_output_quality(prompt, candidate)
            rankings.append({
                "output": candidate,
                "quality_score": quality
            })

        # Sort by quality
        rankings.sort(key=lambda x: x["quality_score"], reverse=True)

        return rankings

    def collect_seed_dataset(self, prompts, num_samples=50):
        """
        Collect preference groups for seed prompts.
        """
        dataset = []

        for prompt in prompts[:num_samples]:
            group = self.collect_preference_group(prompt)
            dataset.append({
                "prompt": prompt,
                "preference_group": group
            })

        return dataset
```

### 2. Implement Token Prior Learning

Learn which tokens should be amplified during inference.

```python
class TokenPriorLearner:
    """
    Learn token probability shifts from preference data.
    """
    def __init__(self, model, vocab_size):
        self.model = model
        self.vocab_size = vocab_size

        # Token prior: log-probability shift for each token
        self.token_prior = torch.zeros(vocab_size, requires_grad=True)
        self.optimizer = torch.optim.Adam([self.token_prior], lr=0.01)

    def tokenize_outputs(self, outputs):
        """Convert outputs to token sequences."""
        return [self.model.tokenize(o) for o in outputs]

    def compute_group_advantage(self, tokens_groups):
        """
        Compute semantic advantage: how much better is top output?

        Args:
            tokens_groups: List of tokenized outputs, ranked by quality

        Returns:
            Advantage signal (higher = more advantage for top outputs)
        """
        # Top output vs. mean of others
        top_tokens = tokens_groups[0]
        other_tokens = tokens_groups[1:]

        # Calculate token overlap (semantic similarity)
        top_set = set(top_tokens)
        other_sets = [set(t) for t in other_tokens]

        # Jaccard similarity of top vs. others
        similarities = []
        for other_set in other_sets:
            intersection = len(top_set & other_set)
            union = len(top_set | other_set)
            jaccard = intersection / (union + 1e-8)
            similarities.append(jaccard)

        # Advantage: how different is top from others?
        avg_similarity = np.mean(similarities)
        advantage = 1.0 - avg_similarity  # Dissimilarity = advantage

        return advantage

    def train_token_priors(self, preference_dataset, num_epochs=10):
        """
        Learn token priors from preference data.
        """
        for epoch in range(num_epochs):
            epoch_loss = 0

            for example in preference_dataset:
                prompt = example["prompt"]
                preference_group = example["preference_group"]

                # Extract outputs ranked by quality
                outputs = [item["output"] for item in preference_group]
                token_groups = self.tokenize_outputs(outputs)

                # Compute group advantage
                advantage = self.compute_group_advantage(token_groups)

                # Tokens to amplify: those in high-quality outputs
                top_tokens = token_groups[0]

                # Loss: amplify good tokens, suppress bad ones
                loss = 0
                for token_id in top_tokens:
                    # Want high prior for tokens in good outputs
                    loss -= self.token_prior[token_id] * advantage

                for other_tokens in token_groups[1:]:
                    for token_id in other_tokens:
                        # Want low prior for tokens in worse outputs
                        loss += self.token_prior[token_id] * 0.1

                # Update
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                epoch_loss += loss.item()

            print(f"Epoch {epoch}: loss={epoch_loss / len(preference_dataset):.4f}")

        return self.token_prior
```

### 3. Apply Token Priors at Inference

Modify generation probabilities using learned priors.

```python
class TokenPriorInference:
    """
    Generate outputs with learned token priors applied.
    """
    def __init__(self, model, token_prior):
        self.model = model
        self.token_prior = token_prior

    def generate_with_prior(self, prompt, max_tokens=256, temperature=1.0):
        """
        Generate with token prior guidance.

        Args:
            prompt: Input prompt
            max_tokens: Max generation length
            temperature: Sampling temperature

        Returns:
            Generated output
        """
        output_tokens = []

        for _ in range(max_tokens):
            # Get model logits
            logits = self.model.get_logits(prompt)

            # Apply token prior
            adjusted_logits = logits + self.token_prior

            # Sample from adjusted distribution
            probs = torch.softmax(adjusted_logits / temperature, dim=-1)
            next_token_id = torch.multinomial(probs, 1).item()

            output_tokens.append(next_token_id)

            # Update prompt for next iteration
            next_token_text = self.model.decode_token(next_token_id)
            prompt += next_token_text

            if self.model.is_stop_token(next_token_id):
                break

        return self.model.decode_tokens(output_tokens)

    def batch_generate_with_prior(self, prompts, num_outputs=4):
        """
        Generate multiple outputs per prompt with priors.
        """
        results = {}

        for prompt in prompts:
            outputs = []
            for _ in range(num_outputs):
                output = self.generate_with_prior(prompt, temperature=0.8)
                outputs.append(output)

            results[prompt] = outputs

        return results
```

### 4. Iterative Refinement Loop

Continually improve token priors with more preference data.

```python
def iterative_token_prior_refinement(
    model,
    initial_prompts,
    num_iterations=5,
    num_new_prompts_per_iter=20
):
    """
    Iteratively refine token priors with new data.
    """
    # Initialize
    collector = PreferenceDataCollector(model)
    preference_data = collector.collect_seed_dataset(
        initial_prompts,
        num_samples=50
    )

    learner = TokenPriorLearner(model, model.vocab_size)
    token_prior = learner.train_token_priors(preference_data, num_epochs=5)

    # Iterative refinement
    for iteration in range(num_iterations):
        print(f"\nIteration {iteration + 1}")

        # Generate outputs with current priors
        inference = TokenPriorInference(model, token_prior)
        new_prompts = sample_new_prompts(
            model,
            num_new_prompts_per_iter
        )

        new_preferences = collector.collect_seed_dataset(
            new_prompts,
            num_samples=num_new_prompts_per_iter
        )

        # Combine with previous data
        preference_data.extend(new_preferences)

        # Retrain token priors
        learner = TokenPriorLearner(model, model.vocab_size)
        token_prior = learner.train_token_priors(
            preference_data,
            num_epochs=5
        )

        # Evaluate improvement
        improvement = evaluate_preference_satisfaction(
            preference_data,
            token_prior
        )
        print(f"  Improvement: {improvement:.2f}")

    return token_prior
```

### 5. Deployment and Monitoring

Deploy with learned priors and monitor effectiveness.

```python
class TrainingFreeGRPODeployment:
    """Manage deployment of training-free GRPO."""

    def __init__(self, model, token_prior, rollback_buffer_size=5):
        self.model = model
        self.token_prior = token_prior
        self.inference = TokenPriorInference(model, token_prior)
        self.rollback_buffer = []
        self.max_rollback = rollback_buffer_size

    def generate_with_monitoring(self, prompt):
        """
        Generate output and monitor quality.
        """
        output = self.inference.generate_with_prior(prompt)

        quality = compute_output_quality(prompt, output)

        # Log for monitoring
        log_entry = {
            "prompt": prompt,
            "output": output,
            "quality": quality,
            "token_prior_version": hash(self.token_prior)
        }

        self.rollback_buffer.append(log_entry)

        if len(self.rollback_buffer) > self.max_rollback:
            self.rollback_buffer.pop(0)

        return output, quality

    def rollback_to_previous_prior(self):
        """
        Revert to previous token prior if quality degrades.
        """
        if len(self.rollback_buffer) > 1:
            # Evaluate if recent outputs worse than previous batch
            recent_quality = np.mean([
                e["quality"] for e in self.rollback_buffer[-5:]
            ])
            older_quality = np.mean([
                e["quality"] for e in self.rollback_buffer[-10:-5]
            ])

            if recent_quality < 0.9 * older_quality:
                print("Quality degradation detected. Rolling back token prior.")
                return True

        return False

    def evaluate_prior_effectiveness(self, test_prompts, num_candidates=4):
        """
        Measure improvement from token priors vs. baseline.
        """
        with_prior_results = []
        without_prior_results = []

        for prompt in test_prompts:
            # With prior
            output_with = self.inference.generate_with_prior(prompt)
            quality_with = compute_output_quality(prompt, output_with)
            with_prior_results.append(quality_with)

            # Without prior (baseline)
            baseline_inference = TokenPriorInference(
                self.model,
                torch.zeros_like(self.token_prior)
            )
            output_without = baseline_inference.generate_with_prior(prompt)
            quality_without = compute_output_quality(prompt, output_without)
            without_prior_results.append(quality_without)

        improvement = (
            np.mean(with_prior_results) /
            (np.mean(without_prior_results) + 1e-8) - 1
        ) * 100

        return {
            "with_prior_quality": np.mean(with_prior_results),
            "baseline_quality": np.mean(without_prior_results),
            "improvement_percent": improvement
        }
```

## Practical Guidance

**Hyperparameters:**
- **Num candidates per prompt**: 4-8 (balance diversity vs. cost)
- **Token prior learning rate**: 0.01 (conservative)
- **Num epochs for training**: 5-10 per iteration
- **Seed dataset size**: 50-100 examples
- **Temperature for generation**: 0.8 (encourage diversity)

**When to Use:**
- Model deployment where retraining impractical
- Rapid optimization needed with minimal labeled data
- Want to preserve model parameters for compliance/safety
- Prefer inference-time adaptation vs. fine-tuning

**When NOT to Use:**
- Significant model architecture changes needed
- Task distribution very different from pretraining
- Real-time constraints prohibit inference-time computation
- Model parameters must remain unchanged (e.g., signed verification)

## Reference

[Training-Free Group Relative Policy Optimization](https://arxiv.org/abs/2510.08191) — arXiv:2510.08191

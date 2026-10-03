---
name: markovian-thinker
title: "The Markovian Thinker: Streaming Language Models with Decoupled Thinking"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2510.06557
keywords: [reasoning, efficient-inference, streaming, rl-training, context-management]
description: "Enable LLMs to scale reasoning length from O(n²) to O(n) by structuring thinking into fixed-size chunks with learnable cross-chunk summaries. Trigger: train reasoning models with unbounded or expensive chain-of-thought sequences."
---

# The Markovian Thinker: Decoupled Chunk-Based Reasoning

## Core Concept

Traditional RL-based reasoning in LLMs suffers from **quadratic compute scaling** as thinking length grows. The Markovian Thinker solves this by decomposing reasoning into fixed-size chunks where the model learns to write concise summaries at chunk boundaries. This enables the context to reset between chunks while maintaining reasoning continuity—achieving linear scaling instead of quadratic.

The key insight: Markovian structure allows "chunked thinking" where state transitions depend only on the previous chunk summary, not the entire prior history.

## Architecture Overview

- **Chunk-Based Decomposition**: Divide reasoning into fixed windows (e.g., 8K tokens)
- **Boundary Summaries**: Model learns to write compressed summaries at chunk edges
- **Context Reset Strategy**: Environment resets context window after each chunk, reinitializing with prompt + summary
- **Delethink RL Environment**: Custom RL environment that enforces chunk boundaries
- **Linear Recurrence**: Only the previous summary state carries forward, enabling O(n) compute

## Implementation Steps

### 1. Design Chunk Structure and Boundaries

Define your chunk size based on available context window and thinking complexity. Typical configurations use 8K-token chunks for a 16K context window.

```python
class ChunkThinkingConfig:
    chunk_size = 8192  # tokens per thinking segment
    context_window = 16384
    summary_max_tokens = 256  # compressed carryover state
    model_size = "1.5B"  # parameter count

    def validate(self):
        assert self.summary_max_tokens < self.chunk_size // 32
        assert self.context_window >= 2 * self.chunk_size
```

### 2. Implement Delethink Environment

The environment enforces chunk boundaries and manages context resets. It provides reward signals for reasoning quality while penalizing inefficient summaries.

```python
class DeleteinkEnvironment:
    def __init__(self, model, chunk_config):
        self.model = model
        self.chunk_size = chunk_config.chunk_size
        self.summary_tokens = chunk_config.summary_max_tokens

    def step(self, thinking_tokens, summary_text):
        # Measure reasoning quality on current chunk
        chunk_reward = self.evaluate_chunk(thinking_tokens)

        # Penalize verbose summaries
        summary_penalty = -0.01 * len(summary_text.split())

        # Reset context for next chunk
        self.context = self.build_context(summary_text)

        return chunk_reward + summary_penalty

    def evaluate_chunk(self, tokens):
        # Verify solution correctness from this chunk alone
        solution = self.extract_solution(tokens)
        return self.reward_for_correctness(solution)
```

### 3. Train with RL on Chunk Boundaries

Use policy gradient methods (PPO, GRPO) but apply them within the chunked structure. The key difference from standard RL is that you train the model to optimize **both** reasoning quality within chunks and summary quality at boundaries.

```python
def train_chunked_reasoning(model, dataset, config):
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    for epoch in range(config.num_epochs):
        for problem in dataset:
            # Start with fresh context
            context = f"Problem: {problem}\n"
            accumulated_summary = ""
            total_reward = 0

            # Process thinking in chunks
            for chunk_idx in range(config.max_chunks):
                # Generate thinking for this chunk (8K tokens)
                thinking = model.generate(
                    context,
                    max_new_tokens=config.chunk_size
                )

                # Extract solution attempt
                solution = extract_solution(thinking)

                # Evaluate and get reward
                chunk_reward = evaluate_solution(solution, problem)

                # Generate summary (must fit in ~256 tokens)
                summary = model.generate_summary(
                    thinking,
                    max_tokens=config.summary_tokens
                )

                # Compute policy loss
                loss = -chunk_reward * log_prob(thinking, summary)

                # Backprop and update
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                total_reward += chunk_reward
                accumulated_summary += f"\n[Summary {chunk_idx}]: {summary}"

                # Reset context for next chunk
                context = f"{problem}\n{accumulated_summary}\n"

                # Early stopping if solution found
                if is_correct_solution(solution):
                    break
```

### 4. Inference: Stream and Decode

At inference time, the model streams thinking across chunks, regenerating context at boundaries without storing full history.

```python
def stream_chunked_thinking(model, problem, config):
    context = f"Problem: {problem}\nThinking:\n"
    summaries = []
    max_thinking_tokens = 24000  # Total thinking budget

    token_count = 0
    chunk_num = 0

    while token_count < max_thinking_tokens:
        # Generate next chunk of thinking
        chunk_thinking, chunk_tokens = model.stream_generate(
            context,
            max_tokens=config.chunk_size,
            return_token_count=True
        )

        token_count += chunk_tokens
        chunk_num += 1

        # Try to extract solution
        candidate_solution = extract_solution(chunk_thinking)
        if is_valid_solution(candidate_solution):
            return candidate_solution

        # Generate summary for carry-forward
        summary = extract_key_insights(chunk_thinking)
        summaries.append(summary)

        # Reset context with accumulated summaries
        context = f"{problem}\nPrior insights: {'; '.join(summaries[-3:])}\nContinuing...\n"

        print(f"Chunk {chunk_num} complete. Total: {token_count} tokens")

    return extract_final_solution(chunk_thinking)
```

## Practical Guidance

**Hyperparameters:**
- **Chunk size**: 8K-16K tokens (balance thinking depth vs. context reuse)
- **Summary length**: 8-16% of chunk size (compressed carryover state)
- **Reward signal**: Use correctness-based rewards, penalize verbose summaries
- **Training budget**: ~7 H100-months per 1.5B model (vs. 27 months without chunking)

**When to Use:**
- Training reasoning models with long thinking sequences (>16K tokens)
- Resource-constrained settings where quadratic compute is prohibitive
- Multi-step problems requiring iterative refinement

**When NOT to Use:**
- Short reasoning chains where overhead of summaries outweighs benefits
- Tasks requiring full history for each step (non-Markovian structure)
- Single-shot prediction where streaming brings minimal benefit

## Reference

[The Markovian Thinker: Streaming Language Models with Delethink for Linear-Time Reasoning](https://arxiv.org/abs/2510.06557) — arXiv:2510.06557

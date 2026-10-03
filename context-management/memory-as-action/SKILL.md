---
name: memory-as-action
title: "Memory as Action: Autonomous Context Curation for Long-Horizon Agentic Tasks"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2510.12635"
keywords: [memory-management, context-curation, long-horizon, reinforcement-learning, context-efficiency]
description: "Treat memory management as learnable RL policy actions (delete/insert) rather than fixed mechanisms. Enable models to autonomously decide what to keep, remove, or add to context, reducing average context length by 51% while matching larger models."
---

# Memory as Action: Learning to Manage Context Efficiently

Long-context models suffer from attention dilution as context grows. Rather than using fixed memory management rules, Memory as Action lets the model learn what information to retain through reinforcement learning, optimizing memory operations as policy actions.

Core insight: working memory should be dynamic and task-aware. By treating memory deletion and insertion as learnable actions, models learn to maintain only decision-critical context, reducing context length by 51% while improving accuracy through better attention focus.

## Core Concept

**Memory as Policy Action**: Define memory operations (delete, insert) as learnable actions optimized through RL, not static rules. The model decides what to keep based on reasoning state.

**In-Place Editing**: Rather than regenerating context, make surgical edits: delete irrelevant information, insert new conclusions. This is interpretable and efficient.

**End-to-End Optimization**: Joint optimization of context and task performance ensures memory serves the actual reasoning process.

## Architecture Overview

- **Memory State Tracker**: Maintains current context window
- **Action Policy**: Learns which tokens to delete/insert
- **Task Executor**: Uses curated memory for reasoning
- **Reward Signal**: Task performance + memory efficiency

## Implementation Steps

**Stage 1: Define Memory Operations**

Implement memory editing as differentiable operations:

```python
import torch
import torch.nn as nn

class MemoryEditor(nn.Module):
    def __init__(self, hidden_dim=768, max_memory_size=2048):
        super().__init__()

        self.hidden_dim = hidden_dim
        self.max_memory_size = max_memory_size

        # Policy for deciding what to delete
        self.delete_policy = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid()
        )

        # Policy for deciding what to insert
        self.insert_policy = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim)
        )

    def compute_delete_scores(self, memory_tokens, current_state):
        """
        Score each memory token for deletion.
        High score = should delete.
        """

        batch_size, seq_len, _ = memory_tokens.shape

        # Expand current state to match sequence
        current_expanded = current_state.unsqueeze(1).expand(
            -1, seq_len, -1
        )

        # Concatenate memory token with current state
        combined = torch.cat(
            [memory_tokens, current_expanded],
            dim=-1
        )

        # Compute delete scores
        delete_scores = self.delete_policy(combined).squeeze(-1)

        return delete_scores  # [batch, seq_len]

    def compute_insertion_vectors(self, current_state):
        """
        Generate vectors to insert into memory.
        """

        insertion_vectors = self.insert_policy(current_state)

        return insertion_vectors  # [batch, hidden_dim]

    def apply_memory_edits(
        self,
        memory_tokens,
        delete_scores,
        insertion_vectors,
        delete_threshold=0.5
    ):
        """
        Apply deletion and insertion operations to memory.
        """

        batch_size, seq_len, dim = memory_tokens.shape

        # Determine which tokens to delete
        delete_mask = (delete_scores > delete_threshold)

        # Keep tokens below threshold
        kept_tokens = memory_tokens[~delete_mask]

        # Compute new memory size
        new_size = kept_tokens.shape[0]

        # Insert new vectors if we have space
        if new_size + 1 <= self.max_memory_size:
            new_memory = torch.cat(
                [kept_tokens, insertion_vectors.unsqueeze(1)],
                dim=0
            )
        else:
            new_memory = kept_tokens[:self.max_memory_size]

        return new_memory, {
            'deleted_tokens': delete_mask.sum(),
            'inserted_tokens': 1 if (new_size + 1) <= self.max_memory_size else 0,
            'final_size': new_memory.shape[0]
        }
```

**Stage 2: RL Training with Memory Rewards**

Train memory operations through policy gradient:

```python
def compute_memory_reward(
    task_performance,
    context_length,
    baseline_length
):
    """
    Combined reward: task success + efficiency.
    """

    # Task reward: normalized to [0, 1]
    task_reward = task_performance

    # Efficiency reward: reduce excess context
    excess_context = max(0, context_length - baseline_length)
    efficiency_penalty = -0.01 * excess_context

    total_reward = task_reward + efficiency_penalty

    return total_reward

def memory_action_rl_training(
    model,
    memory_editor,
    task_dataloader,
    num_steps=10000
):
    """
    Train memory editor with RL.
    """

    optimizer = torch.optim.AdamW(
        list(model.parameters()) + list(memory_editor.parameters()),
        lr=1e-4
    )

    for step in range(num_steps):
        task_batch = next(iter(task_dataloader))

        context = task_batch['context']
        query = task_batch['query']
        target = task_batch['target']

        # Initialize memory
        memory = model.get_embedding(context)
        baseline_length = memory.shape[1]

        # Compute memory operations
        delete_scores = memory_editor.compute_delete_scores(
            memory,
            model.get_embedding(query)
        )

        # Sample delete decisions (for exploration)
        delete_threshold = 0.5 - 0.1 * (step / num_steps)  # Anneal
        delete_mask = (delete_scores > delete_threshold)

        # Apply edits
        current_state = model.get_embedding(query)
        new_memory, edit_info = memory_editor.apply_memory_edits(
            memory,
            delete_scores,
            memory_editor.compute_insertion_vectors(current_state),
            delete_threshold=delete_threshold
        )

        # Execute task with edited memory
        prediction = model.forward_with_memory(
            query,
            new_memory
        )

        # Compute task loss
        task_loss = torch.nn.functional.cross_entropy(
            prediction,
            target
        )

        # Compute memory reward
        task_performance = 1.0 if (prediction.argmax() == target).item() else 0.0
        memory_reward = compute_memory_reward(
            task_performance,
            new_memory.shape[1],
            baseline_length
        )

        # Log probabilities of memory actions
        # Delete probability for deleted tokens
        delete_log_prob = torch.log(
            delete_scores[delete_mask] + 1e-10
        ).mean()

        # Insert log probability (constant, just contribute to entropy)
        insert_log_prob = -0.5  # Mild regularization

        # Policy loss: maximize expected reward
        policy_loss = -(memory_reward * (delete_log_prob + insert_log_prob))

        # Total loss
        total_loss = task_loss + 0.1 * policy_loss

        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()

        if step % 100 == 0:
            print(
                f"Step {step}, Task Loss: {task_loss:.4f}, "
                f"Memory Size: {new_memory.shape[1]}, "
                f"Reward: {memory_reward:.4f}"
            )
```

**Stage 3: Inference with Learned Memory Curation**

Deploy models with autonomous memory management:

```python
def inference_with_memory_curation(
    model,
    memory_editor,
    long_context,
    query,
    max_total_steps=50
):
    """
    Execute query while autonomously managing memory.
    """

    memory = model.get_embedding(long_context)
    baseline_length = memory.shape[1]

    step_results = []

    for step in range(max_total_steps):
        # Current query embedding
        query_emb = model.get_embedding(query)

        # Score tokens for deletion
        delete_scores = memory_editor.compute_delete_scores(
            memory,
            query_emb
        )

        # Compute insertion vectors
        insertion_vectors = memory_editor.compute_insertion_vectors(
            query_emb
        )

        # Apply edits (greedy threshold)
        new_memory, edit_info = memory_editor.apply_memory_edits(
            memory,
            delete_scores,
            insertion_vectors,
            delete_threshold=0.6
        )

        memory = new_memory

        # Execute reasoning step with curated memory
        prediction = model.forward_with_memory(query, memory)

        step_results.append({
            'prediction': prediction,
            'memory_size': memory.shape[1],
            'deleted': edit_info['deleted_tokens'],
            'inserted': edit_info['inserted_tokens']
        })

        # Check if done
        if model.is_complete(prediction):
            break

    return step_results
```

## Practical Guidance

**When to Use Memory as Action:**
- Long-horizon tasks (10+ reasoning steps) with information accumulation
- Settings where context length is bottleneck
- Tasks where not all context is equally relevant throughout

**When NOT to Use:**
- Short tasks where memory management overhead outweighs benefit
- Tasks requiring access to all historical context
- Real-time inference where deletion overhead is prohibitive

**Memory Operation Strategies:**

| Strategy | Delete Threshold | Insert Rate |
|----------|------------------|-------------|
| Aggressive | 0.7 | Every 5 steps |
| Balanced | 0.5 | Every 3 steps |
| Conservative | 0.3 | Every step |

**Typical Results:**

| Baseline | Memory Reduction | Accuracy Change |
|----------|------------------|-----------------|
| 4096 tokens | 51% reduction | +2-3% |
| 8192 tokens | 45% reduction | +1-2% |
| 2048 tokens | 30% reduction | Neutral |

**Common Pitfalls:**
- Delete threshold too aggressive (lose critical information)
- Insertion rate too high (memory still grows)
- Not validating deleted information isn't needed later
- Training on easy tasks (memory management not learned)

## Reference

Based on the research at: https://arxiv.org/abs/2510.12635

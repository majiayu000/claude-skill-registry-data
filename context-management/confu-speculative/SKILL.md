---
name: confu-speculative
title: "ConFu: Contemplate the Future for Better Speculative Sampling"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2603.08899"
keywords: [Inference Optimization, Speculative Decoding, Draft Models, Token Acceptance, LLM Acceleration]
description: "Improves speculative decoding acceptance rates by exposing target model's intermediate reasoning through contemplate tokens. Achieves 8-11% acceptance rate improvement over EAGLE through future-direction guidance without extra forward passes."
---

# ConFu: Improving Speculative Decoding Through Target Model Future Reasoning

Speculative decoding accelerates LLM inference by drafting tokens with a lightweight model and verifying with the target model. However, draft models condition only on the current prefix, causing distribution drift over multiple steps. As draft tokens diverge from target model preferences, verification acceptance rates drop, reducing speedup gains.

ConFu solves this by exposing the target model's intermediate reasoning through special contemplate tokens. These tokens trigger the target model to generate its internal predictions of future token distributions, guiding the draft model toward better candidates without requiring additional forward passes.

## Core Concept

Standard speculative decoding: draft model generates token independently, target verifies

ConFu: Insert contemplate token that makes target model emit its predicted next-token distribution, share this with draft model for better guidance

The key insight: contemplate tokens allow the target model to communicate its reasoning direction without extra computation—they're generated during the verification pass and reused for subsequent draft guidance. This transforms a passive verification step into active guidance.

## Architecture Overview

- **Contemplate Token Mechanism**: Special tokens trigger target model to encode future predictions as continuous embeddings
- **Dual Prediction Path**: Target model generates both next token AND contemplate embedding during verification
- **Dynamic MoE Selection**: Learned Mixture-of-Experts chooses context-appropriate guidance based on hidden states
- **Parallel Verification**: Process multiple draft candidates simultaneously using contemplate-guided predictions
- **Memory Efficiency**: Anchor token sampling reduces memory overhead by selective insertion

## Implementation Steps

Implement contemplate token guidance in a speculative decoding framework.

**Contemplate Token and Embedding Generation**

```python
import torch
import torch.nn as nn

class ContemplateMechanism(nn.Module):
    """Generates and uses contemplate embeddings for guidance."""

    def __init__(self, hidden_dim, vocab_size):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.vocab_size = vocab_size

        # Special token for contemplation
        self.contemplate_token_id = vocab_size - 1  # Reserved special token

        # MLP to encode target model's hidden state as guidance
        self.guidance_encoder = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim * 2),
            nn.ReLU(),
            nn.Linear(hidden_dim * 2, hidden_dim)
        )

        # MoE router for context-aware guidance selection
        self.moe_router = nn.Linear(hidden_dim, 4)  # Route to 4 expert guides
        self.moe_experts = nn.ModuleList([
            nn.Linear(hidden_dim, vocab_size) for _ in range(4)
        ])

    def get_contemplate_guidance(self, target_hidden_state):
        """
        Generate guidance embedding from target model's hidden state.

        Args:
            target_hidden_state: [batch_size, hidden_dim] final layer hidden state

        Returns:
            guidance_embedding: [batch_size, hidden_dim] continuous guidance
            expert_logits: [batch_size, vocab_size] MoE-weighted predictions
        """
        # Encode hidden state as guidance
        guidance = self.guidance_encoder(target_hidden_state)  # [batch_size, hidden_dim]

        # Dynamic MoE selection based on context
        router_logits = self.moe_router(target_hidden_state)  # [batch_size, 4]
        router_weights = torch.softmax(router_logits, dim=1)  # [batch_size, 4]

        # Compute weighted combination of expert predictions
        expert_outputs = []
        for expert in self.moe_experts:
            expert_out = expert(target_hidden_state)  # [batch_size, vocab_size]
            expert_outputs.append(expert_out)

        expert_stack = torch.stack(expert_outputs, dim=1)  # [batch_size, 4, vocab_size]
        expert_logits = torch.sum(
            router_weights.unsqueeze(2) * expert_stack, dim=1
        )  # [batch_size, vocab_size]

        return guidance, expert_logits


class TargetModelWithContemplate(nn.Module):
    """Target LLM extended with contemplate token mechanism."""

    def __init__(self, base_model, hidden_dim, vocab_size):
        super().__init__()
        self.base_model = base_model
        self.contemplate_mechanism = ContemplateMechanism(hidden_dim, vocab_size)

    def forward(self, input_ids, return_contemplate=False):
        """
        Forward pass with optional contemplate guidance.

        Args:
            input_ids: [batch_size, seq_len] token indices
            return_contemplate: whether to generate contemplate guidance

        Returns:
            logits: [batch_size, vocab_size] next token logits
            contemplate_guide: optional [batch_size, vocab_size] guidance logits
        """
        # Standard LLM forward
        outputs = self.base_model(input_ids, output_hidden_states=True)
        logits = outputs.logits[:, -1, :]  # [batch_size, vocab_size] last token
        hidden_states = outputs.hidden_states[-1][:, -1, :]  # [batch_size, hidden_dim]

        if return_contemplate:
            # Generate contemplate guidance
            guidance, expert_logits = self.contemplate_mechanism.get_contemplate_guidance(
                hidden_states
            )
            return logits, expert_logits
        else:
            return logits
```

**Draft Model Guidance Integration**

```python
class GuidedDraftModel(nn.Module):
    """Draft model enhanced with contemplate guidance."""

    def __init__(self, base_draft_model, hidden_dim):
        super().__init__()
        self.base_model = base_draft_model
        self.hidden_dim = hidden_dim

        # Guidance fusion layer
        self.guidance_fusion = nn.Linear(hidden_dim * 2, hidden_dim)

    def forward(self, input_ids, contemplate_guidance=None):
        """
        Generate draft token, optionally conditioned on contemplate guidance.

        Args:
            input_ids: [batch_size, seq_len] prefix tokens
            contemplate_guidance: [batch_size, vocab_size] target model's guidance logits

        Returns:
            draft_logits: [batch_size, vocab_size] draft token distribution
        """
        # Base draft model forward
        draft_outputs = self.base_model(input_ids, output_hidden_states=True)
        draft_logits = draft_outputs.logits[:, -1, :]
        draft_hidden = draft_outputs.hidden_states[-1][:, -1, :]

        if contemplate_guidance is not None:
            # Fuse guidance with draft hidden state
            # Contemplate guidance acts as soft prompt for future direction
            guidance_influence = self.guidance_fusion(
                torch.cat([draft_hidden, contemplate_guidance.unsqueeze(1).expand_as(draft_hidden)], dim=1)
            )

            # Blend draft logits with guidance signal
            blended_logits = draft_logits + 0.3 * guidance_influence[:, :draft_logits.shape[1]]
            return blended_logits

        return draft_logits
```

**Speculative Decoding Loop with ConFu**

```python
def speculative_decode_with_confu(
    target_model,
    draft_model,
    input_ids,
    max_length=256,
    num_draft_tokens=4,
    anchor_interval=5
):
    """
    Speculative decoding with contemplate guidance.

    Args:
        target_model: TargetModelWithContemplate instance
        draft_model: GuidedDraftModel instance
        input_ids: [batch_size, seq_len] initial tokens
        max_length: maximum generation length
        num_draft_tokens: tokens drafted before verification
        anchor_interval: insert contemplate anchor every N tokens

    Returns:
        generated_ids: [batch_size, seq_len + generated_len]
        acceptance_stats: dict with acceptance rates
    """
    batch_size = input_ids.shape[0]
    generated = input_ids.clone()

    total_drafted = 0
    total_accepted = 0
    contemplate_guides = [None] * batch_size

    for step in range(max_length):
        # Decide whether to insert contemplate anchor
        use_anchor = (step % anchor_interval == 0)

        # Step 1: Draft tokens
        draft_tokens_step = []
        for draft_idx in range(num_draft_tokens):
            # Get draft prediction, potentially guided by contemplate
            draft_logits = draft_model(
                generated,
                contemplate_guidance=contemplate_guides[0] if contemplate_guides[0] is not None else None
            )

            # Sample from draft
            draft_token = torch.multinomial(
                torch.softmax(draft_logits, dim=-1),
                num_samples=1
            ).squeeze(-1)

            draft_tokens_step.append(draft_token)
            generated = torch.cat([generated, draft_token.unsqueeze(1)], dim=1)
            total_drafted += batch_size

        # Step 2: Verify all drafted tokens with target model
        # Build sequences with all draft tokens
        verification_input = generated

        # Get target model predictions with contemplate
        target_logits, contemplate_guides_new = target_model(
            verification_input,
            return_contemplate=use_anchor
        )

        # Compare target vs draft
        target_probs = torch.softmax(target_logits, dim=-1)

        # Acceptance check: does target prefer the drafted token?
        for draft_idx, draft_token in enumerate(draft_tokens_step):
            draft_prob = draft_probs = torch.softmax(
                draft_model(
                    verification_input[:, :-(num_draft_tokens - draft_idx)],
                    contemplate_guidance=None
                ), dim=-1
            )
            target_prob = target_probs

            # Rejection sampling: accept if target >= draft with some probability
            acceptance_ratio = target_prob.gather(-1, draft_token.unsqueeze(1)) / (
                draft_prob.gather(-1, draft_token.unsqueeze(1)) + 1e-10
            )
            accept = torch.rand_like(acceptance_ratio) < acceptance_ratio.clamp(0, 1)

            if accept.any():
                total_accepted += accept.sum().item()

        # Update contemplate guides for next iteration
        if use_anchor:
            contemplate_guides = contemplate_guides_new

    return generated, {
        'total_drafted': total_drafted,
        'total_accepted': total_accepted,
        'acceptance_rate': total_accepted / (total_drafted + 1e-10)
    }
```

## Practical Guidance

**Hyperparameters**:
- Anchor token interval: 5 tokens (insert contemplate every 5 steps)
- Guidance influence weight: 0.3 (blend with draft logits)
- MoE experts: 4 (balances capacity and efficiency)
- Draft tokens per verification: 4-8 (typical for speedup)

**When to Apply**:
- Speculative decoding where draft model diverges from target (common case)
- Long-context generation where multiple draft tokens needed
- Models with large parameter gaps between draft and target
- Scenarios where token acceptance rates are bottleneck

**When NOT to Apply**:
- Draft and target models are well-aligned (vanilla speculative is sufficient)
- Single token draft (overhead not justified)
- Real-time systems where MoE routing adds latency

**Key Pitfalls**:
- Anchor interval too large—stale guidance; too small—memory overhead
- MoE routing untrained—poor guidance quality
- Guidance weight too high—draft overshadowed; too low—insufficient improvement
- Not syncing contemplate guides across batch—shape mismatches

**Integration Notes**: Works as wrapper around existing speculative decoding; requires extending target model with contemplate mechanism; draft model remains largely unchanged.

**Evidence**: Achieves 8-11% acceptance rate improvement over EAGLE-3 baseline; largest gains at lower sampling temperatures; enables 1.3-1.5x speedup boost over vanilla speculative decoding.

Reference: https://arxiv.org/abs/2603.08899

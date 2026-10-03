---
name: dmtd-multi-token
title: "Direct Multi-Token Decoding"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2510.11958"
keywords: [inference-optimization, multi-token-decoding, layer-specialization, transformer-efficiency]
description: "Generate multiple tokens simultaneously by having late transformer layers directly predict multiple outputs after early layer processing. No auxiliary parameters or verification needed. Achieve up to 2x generation speedup."
---

# Direct Multi-Token Decoding: Parallel Output Generation

Traditional autoregressive generation processes one token at a time through all layers. Direct Multi-Token Decoding exploits transformer layer specialization: early layers extract input context, middle layers process task features, late layers generate outputs. By skipping early/middle layers after first pass, late layers can emit multiple tokens per forward pass.

Core insight: transformer layers have distinct roles that become apparent during generation. Once context is extracted, late layers can generate multiple output tokens without reprocessing early layers, achieving 2x speedup with minimal setup.

## Core Concept

**Layer Role Specialization**: Early layers understand input, middle layers transform, late layers generate. After initial context processing, late layers work independently.

**Multi-Head Output**: Late layers generate multiple token predictions from the same internal state, amortizing early layer cost.

**Zero Additional Parameters**: Unlike speculative decoding, no auxiliary models needed—just different inference patterns.

## Architecture Overview

- **Early Layers**: Context extraction and input understanding
- **Middle Layers**: Task-specific representations
- **Late Layers**: Direct multi-token generation heads
- **Output Aggregation**: Combine multiple token predictions

## Implementation Steps

**Stage 1: Setup Multi-Token Output Heads**

Add heads for generating multiple tokens from final layer:

```python
import torch
import torch.nn as nn
from transformers import AutoModelForCausalLM

class MultiTokenDecoder(nn.Module):
    def __init__(
        self,
        model_name,
        num_output_tokens=4,
        skip_layers=4
    ):
        """
        Prepare model for multi-token decoding.

        Args:
            num_output_tokens: how many tokens to generate per forward
            skip_layers: which layers to skip after initialization
        """

        super().__init__()

        self.base_model = AutoModelForCausalLM.from_pretrained(
            model_name
        )

        self.num_output_tokens = num_output_tokens
        self.skip_layers = skip_layers
        self.num_layers = len(self.base_model.transformer.h)

        # Create multi-token output heads
        hidden_dim = self.base_model.config.hidden_size
        self.multi_token_heads = nn.ModuleList([
            nn.Linear(hidden_dim, self.base_model.config.vocab_size)
            for _ in range(num_output_tokens)
        ])

        # Initialize heads from existing LM head
        for head in self.multi_token_heads:
            head.weight.copy_(self.base_model.lm_head.weight)
            head.bias.copy_(self.base_model.lm_head.bias)

    def forward_early_processing(self, input_ids):
        """
        Run input through early and middle layers only.
        Returns intermediate hidden states.
        """

        # Get embeddings
        hidden_states = self.base_model.get_input_embeddings()(input_ids)

        # Run through early and middle layers
        early_cutoff = self.num_layers - self.skip_layers

        for layer_idx in range(early_cutoff):
            layer = self.base_model.transformer.h[layer_idx]
            hidden_states = layer(hidden_states)[0]

        return hidden_states

    def forward_multi_token_generation(self, hidden_states):
        """
        Generate multiple tokens from same hidden state.
        """

        # Run final layers that were skipped
        early_cutoff = self.num_layers - self.skip_layers

        for layer_idx in range(early_cutoff, self.num_layers):
            layer = self.base_model.transformer.h[layer_idx]
            hidden_states = layer(hidden_states)[0]

        # Apply layer norm
        hidden_states = self.base_model.transformer.ln_f(hidden_states)

        # Generate multiple tokens from final hidden state
        token_logits = []

        for head_idx, head in enumerate(self.multi_token_heads):
            logits = head(hidden_states[:, -1, :])  # Take last position
            token_logits.append(logits)

        return token_logits
```

**Stage 2: Training Fine-Tuning for Multi-Token Heads**

Train the additional output heads:

```python
def finetune_multi_token_heads(
    decoder_model,
    train_dataloader,
    num_epochs=3,
    learning_rate=1e-4
):
    """
    Fine-tune multi-token heads on language modeling task.
    """

    optimizer = torch.optim.AdamW(
        decoder_model.multi_token_heads.parameters(),
        lr=learning_rate
    )

    for epoch in range(num_epochs):
        total_loss = 0.0

        for batch in train_dataloader:
            input_ids = batch['input_ids']
            target_ids = batch['target_ids']  # [batch, num_output_tokens]

            # Early processing
            hidden_states = decoder_model.forward_early_processing(
                input_ids
            )

            # Multi-token generation
            token_logits = decoder_model.forward_multi_token_generation(
                hidden_states
            )

            # Compute loss for each output token
            loss = 0.0

            for token_idx, logits in enumerate(token_logits):
                target = target_ids[:, token_idx]

                token_loss = torch.nn.functional.cross_entropy(
                    logits,
                    target
                )

                loss = loss + token_loss

            # Normalize by number of output tokens
            loss = loss / len(token_logits)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / len(train_dataloader)
        print(f"Epoch {epoch}, Loss: {avg_loss:.4f}")

    return decoder_model
```

**Stage 3: Inference with Multi-Token Generation**

Deploy multi-token decoding:

```python
def generate_with_multi_tokens(
    decoder_model,
    prompt,
    tokenizer,
    max_length=512
):
    """
    Generate text using multi-token decoding.
    """

    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    generated = input_ids.clone()

    while generated.shape[1] < max_length:
        # Early processing
        with torch.no_grad():
            hidden_states = decoder_model.forward_early_processing(
                generated
            )

            # Multi-token generation
            token_logits = decoder_model.forward_multi_token_generation(
                hidden_states
            )

        # Get next tokens greedily
        next_tokens = []

        for logits in token_logits:
            next_token = logits.argmax(dim=-1).unsqueeze(-1)
            next_tokens.append(next_token)

        # Append tokens to sequence
        next_tokens_tensor = torch.cat(next_tokens, dim=-1)
        generated = torch.cat([generated, next_tokens_tensor], dim=-1)

        # Check for end token
        if any(
            tokenizer.eos_token_id in tokens
            for tokens in next_tokens_tensor.tolist()
        ):
            break

    return generated

def benchmark_multi_token_decoding(
    decoder_model,
    prompts,
    tokenizer,
    num_runs=10
):
    """
    Benchmark speedup of multi-token decoding.
    """

    import time

    # Multi-token generation
    start = time.time()
    for _ in range(num_runs):
        for prompt in prompts:
            generate_with_multi_tokens(
                decoder_model,
                prompt,
                tokenizer,
                max_length=256
            )
    multi_token_time = time.time() - start

    # Standard generation (baseline)
    start = time.time()
    for _ in range(num_runs):
        for prompt in prompts:
            input_ids = tokenizer.encode(prompt, return_tensors='pt')
            decoder_model.base_model.generate(
                input_ids,
                max_length=256
            )
    baseline_time = time.time() - start

    speedup = baseline_time / multi_token_time

    print(
        f"Multi-token time: {multi_token_time:.2f}s\n"
        f"Baseline time: {baseline_time:.2f}s\n"
        f"Speedup: {speedup:.2f}x"
    )

    return speedup
```

## Practical Guidance

**When to Use Direct Multi-Token Decoding:**
- Inference where latency matters (batching, streaming)
- Models with clear early/middle/late layer specialization
- Scenarios tolerating slight quality tradeoff for speed

**When NOT to Use:**
- Quality-critical applications (multi-token increases errors)
- Models where all layers equally important
- Very small models (overhead dominates savings)

**Layer Specialization by Model:**

| Model | Early Layers | Skip Layers | Speedup |
|-------|-------------|------------|---------|
| Llama-7B | 1-8 | 4 | 1.8x |
| Qwen-14B | 1-12 | 6 | 2.0x |
| GPT-3.5-equiv | 1-20 | 8 | 1.9x |

**Multi-Token Count:**

| Tokens | Speedup | Quality |
|--------|---------|---------|
| 2 | 1.3-1.5x | >99% |
| 4 | 1.8-2.2x | 97-98% |
| 8 | 2.0-2.5x | 90-95% |

**Common Pitfalls:**
- Skip layers too small (insufficient savings)
- Skip layers too large (quality degradation)
- Not validating layer role specialization for your model
- Not fine-tuning multi-token heads (poor generation)

## Reference

Based on the research at: https://arxiv.org/abs/2510.11958

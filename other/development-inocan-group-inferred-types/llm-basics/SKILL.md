---
name: llm-basics
description: LLM architecture, tokenization, transformers, and inference optimization. Use for understanding and working with language models.
sasmp_version: "1.3.0"
bonded_agent: 01-llm-fundamentals
bond_type: PRIMARY_BOND
---

# LLM Basics

Master the fundamentals of Large Language Models.

## Quick Start

### Using OpenAI API
```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain transformers briefly."}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

### Using Hugging Face
```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "meta-llama/Llama-2-7b-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

inputs = tokenizer("Hello, how are", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=50)
print(tokenizer.decode(outputs[0]))
```

## Core Concepts

### Transformer Architecture
```
Input → Embedding → [N × Transformer Block] → Output

Transformer Block:
┌───────────────────────────┐
│ Multi-Head Self-Attention │
├───────────────────────────┤
│   Layer Normalization     │
├───────────────────────────┤
│   Feed-Forward Network    │
├───────────────────────────┤
│   Layer Normalization     │
└───────────────────────────┘
```

### Tokenization
```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")
text = "Hello, world!"

# Encode
tokens = tokenizer.encode(text)
print(tokens)  # [15496, 11, 995, 0]

# Decode
decoded = tokenizer.decode(tokens)
print(decoded)  # "Hello, world!"
```

### Key Parameters
```python
# Generation parameters
params = {
    'temperature': 0.7,      # Randomness (0-2)
    'max_tokens': 1000,      # Output length limit
    'top_p': 0.9,            # Nucleus sampling
    'top_k': 50,             # Top-k sampling
    'frequency_penalty': 0,  # Reduce repetition
    'presence_penalty': 0    # Encourage new topics
}
```

## Model Comparison

| Model | Parameters | Context | Best For |
|-------|------------|---------|----------|
| GPT-4 | ~1.7T | 128K | Complex reasoning |
| GPT-3.5 | 175B | 16K | General tasks |
| Claude 3 | N/A | 200K | Long context |
| Llama 2 | 7-70B | 4K | Open source |
| Mistral 7B | 7B | 32K | Efficient inference |

## Local Inference

### With Ollama
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Run a model
ollama run llama2

# API usage
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Why is the sky blue?"
}'
```

### With vLLM
```python
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Llama-2-7b-hf")
sampling = SamplingParams(temperature=0.8, max_tokens=100)

outputs = llm.generate(["Hello, my name is"], sampling)
```

## Best Practices

1. **Start simple**: Use API before local deployment
2. **Mind context**: Stay within context window limits
3. **Temperature tuning**: Lower for facts, higher for creativity
4. **Token efficiency**: Shorter prompts = lower costs
5. **Streaming**: Use for better UX in applications

## Error Handling & Retry

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def call_llm_with_retry(prompt: str) -> str:
    return client.chat.completions.create(...)
```

## Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| Rate limit errors | Too many requests | Add exponential backoff |
| Empty response | max_tokens=0 | Check parameter values |
| High latency | Large model | Use smaller model |
| Timeout | Prompt too long | Reduce input size |

## Unit Test Template

```python
def test_llm_completion():
    response = call_llm("Hello")
    assert response is not None
    assert len(response) > 0
```

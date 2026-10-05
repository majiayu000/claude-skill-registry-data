---
name: llm-deployment
description: Use when lLM deployment and serving — vLLM, Ollama, TGI, llama.cpp. Model
  quantization, GPU optimization, API serving. Use when working with llm deployment.
domain: core
author: oyi77
license: Apache-2.0
subdomain: core-platform
tags:
- api
- deployment
- infrastructure
- llm
- memory
- self-improvement
version: 1.0.0
category: core
---


## Overview

Running LLMs in production — local inference with Ollama/llama.cpp to high-throughput serving with vLLM/TGI. Quantization, GPU optimization, OpenAI-compatible APIs.

## Capabilities

- Local deployment (Ollama, llama.cpp, LM Studio)
- High-throughput serving (vLLM, TGI)
- Quantization (GGUF, GPTQ, AWQ)
- GPU memory optimization (FlashAttention, PagedAttention)
- OpenAI-compatible API endpoints

## When to Use
**Trigger phrases:**
- "llm deployment"
- "LLM deployment and serving — vLLM, Ollama, TGI, llama"


- Self-hosted LLM for privacy/cost
- High-throughput API serving
- Running on consumer GPUs (24GB or less)

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code
```python
# Example workflow for this skill
def execute(input_data):
    # Step 1: Validate input
    if not input_data:
        raise ValueError("Input data is required")

    # Step 2: Process core logic
    result = process(input_data)

    # Step 3: Validate output
    validate_output(result)

    return result
```


### Ollama
```bash
ollama pull llama3.1:8b && ollama serve
curl http://localhost:11434/api/generate -d '{"model":"llama3.1:8b","prompt":"Hello!","stream":false}'
```

### vLLM
```bash
python -m vllm.entrypoints.openai.api_server --model meta-llama/Llama-3.1-8B-Instruct --tensor-parallel-size 2
# Use: OpenAI(base_url="http://localhost:8000/v1", api_key="dummy")
```

### llama.cpp
```bash
cmake -B build -DGGML_METAL=ON && cmake --build build -j
./build/bin/llama-server -m model.gguf --host 0.0.0.0 --port 8080 -ngl 99
```

### Quantize
```python
# GPTQ
from transformers import AutoModelForCausalLM, GPTQConfig
model = AutoModelForCausalLM.from_pretrained("model", quantization_config=GPTQConfig(bits=4))
```

## Common Patterns

- Benchmark: measure tokens/sec, latency p50/p99
- Multi-GPU: tensor-parallel-size = GPU count
- Memory: gpu-memory-utilization=0.9, max-model-len for context

## How to Use

1. Invoke the skill when relevant domain keywords appear in the request
2. Provide required inputs as specified in the skill definition
3. Review the output for correctness before delivering to the user
4. Combine with related skills for complex multi-step workflows

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] Error handling covers edge cases
- [ ] Results are accurate and actionable

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will add monitoring later" | Without monitoring, you cannot detect failures. Add it from day one. |
| "One model is enough" | Different tasks need different models. Route intelligently. |
| "Premature optimization" | Infrastructure decisions are hard to change later. Design for scale early. |
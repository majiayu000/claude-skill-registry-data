---
name: dspy-vllm
description: Use vLLM for high-throughput production serving of self-hosted models with DSPy via dspy.LM with openai/ prefix and api_base. Use when you want production LLM serving, tensor parallelism, multi-GPU inference, batch processing, or high-concurrency self-hosted models. Also used for vllm, vLLM, production serving, high throughput LLM, tensor parallelism, self-hosted production, PagedAttention, local production server, GPU serving, batch inference, vllm serve, pip install vllm, multi-GPU LLM, speculative decoding, continuous batching, deploy local model, NVIDIA GPU serving, openai compatible server, AWQ quantization vllm, GPTQ vllm, dspy.LM api_base vllm, openai/ provider prefix vllm, connect DSPy to vLLM.
---

# vLLM — High-Throughput Production Serving for DSPy

Guide the user through serving self-hosted models with vLLM for production DSPy deployments. High concurrency, multi-GPU, OpenAI-compatible API.

## Step 1: Understand the setup

Before generating vLLM configuration, clarify:

1. **What GPU hardware?** — Model (A100, H100, RTX 4090), count, and VRAM per GPU. This determines tensor parallelism and quantization needs.
2. **Which model?** — Model name and size (7B, 13B, 70B). Determines VRAM requirements and whether quantization is needed.
3. **Workload type?** — Production serving (concurrent users), batch processing (offline), or optimization (running MIPROv2/BootstrapFewShot)?
4. **Already using Ollama locally?** — If yes, help them add vLLM for production while keeping Ollama for dev.

## What is vLLM

[vLLM](https://github.com/vllm-project/vllm) is a high-throughput inference engine (74k+ GitHub stars) for LLMs. Key features:

- **PagedAttention** — 4x memory efficiency vs naive attention, serves more concurrent users
- **Continuous batching** — processes requests as they arrive, no waiting for batch to fill
- **Tensor parallelism** — split models across multiple GPUs
- **OpenAI-compatible API** — drop-in replacement, DSPy connects via `openai/` provider
- **Speculative decoding** — use a small draft model to speed up large model generation

## When to use vLLM

| Scenario | Use vLLM? | Alternative |
|----------|-----------|-------------|
| Production API (10+ concurrent users) | **Yes** | — |
| Multi-GPU serving | **Yes** | — |
| Batch processing (1000s of inputs) | **Yes** | — |
| Local development on macOS | No | Ollama (`/dspy-ollama`) |
| Apple Silicon (M1/M2/M3) | No | Ollama (`/dspy-ollama`) |
| Quick prototyping | No | Ollama (`/dspy-ollama`) |
| Cloud API (no self-hosting) | No | OpenAI/Anthropic (`/dspy-lm`) |

**vLLM requires NVIDIA GPUs** (CUDA). It does not support Apple Silicon or AMD GPUs (ROCm support is experimental).

## Setup

### Install

```bash
pip install vllm
```

Requires: Python 3.9+, NVIDIA GPU with CUDA 12.1+, Linux (recommended) or WSL2.

### Start a vLLM server

```bash
# Basic — serve a model with OpenAI-compatible API
vllm serve meta-llama/Llama-3.1-8B-Instruct

# With common options
vllm serve meta-llama/Llama-3.1-8B-Instruct \
    --host 0.0.0.0 \
    --port 8000 \
    --max-model-len 8192 \
    --gpu-memory-utilization 0.9 \
    --dtype auto
```

The server exposes `/v1/chat/completions` and `/v1/completions` endpoints.

### Connect DSPy to vLLM

```python
import dspy

lm = dspy.LM(
    "openai/meta-llama/Llama-3.1-8B-Instruct",
    api_base="http://localhost:8000/v1",
    api_key="none",  # required but any value works
    temperature=0.7,
    max_tokens=1000,
)
dspy.configure(lm=lm)

# Now all DSPy modules use your vLLM-served model
classify = dspy.ChainOfThought("text -> category, reasoning")
result = classify(text="Server is down, customers can't log in!")
print(result.category)
```

**Note:** `dspy.HFClientVLLM` is deprecated. Use `dspy.LM("openai/...")` with `api_base` instead.

## Tensor parallelism (multi-GPU)

Split large models across multiple GPUs:

```bash
# 2 GPUs
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --tensor-parallel-size 2

# 4 GPUs
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --tensor-parallel-size 4
```

**Rule of thumb:** `--tensor-parallel-size` = number of GPUs the model needs. A 70B FP16 model needs ~140GB VRAM → 2x A100-80GB or 4x A100-40GB.

## GPU sizing guide

| Model size | FP16 VRAM | INT4 (AWQ/GPTQ) VRAM | Recommended GPU |
|-----------|-----------|----------------------|-----------------|
| 7-8B | ~16 GB | ~5 GB | 1x RTX 4090 or A10G |
| 13-14B | ~28 GB | ~8 GB | 1x A100-40GB or 1x RTX 4090 |
| 30-34B | ~68 GB | ~20 GB | 1x A100-80GB or 2x RTX 4090 |
| 70B | ~140 GB | ~40 GB | 2x A100-80GB or 4x A100-40GB |
| 70B | — | ~40 GB | 1x A100-80GB (quantized) |

Add ~20% overhead for KV cache. `--gpu-memory-utilization 0.9` is a good default.

## Quantization

Serve quantized models for reduced VRAM:

```bash
# AWQ quantized (recommended — fastest)
vllm serve TheBloke/Llama-2-70B-Chat-AWQ \
    --quantization awq

# GPTQ quantized
vllm serve TheBloke/Llama-2-70B-Chat-GPTQ \
    --quantization gptq
```

AWQ is generally faster than GPTQ on NVIDIA GPUs. Quality loss from INT4 quantization is typically small for 70B+ models.

## Key vLLM server options

```bash
vllm serve <model> \
    --host 0.0.0.0 \                    # bind address
    --port 8000 \                        # port
    --tensor-parallel-size 1 \           # number of GPUs
    --max-model-len 8192 \               # max sequence length
    --gpu-memory-utilization 0.9 \       # fraction of GPU memory to use
    --dtype auto \                       # auto, float16, bfloat16
    --max-num-seqs 256 \                 # max concurrent sequences
    --enable-prefix-caching \            # cache common prompt prefixes
    --quantization awq \                 # awq, gptq, or none
    --speculative-model <draft-model> \  # enable speculative decoding
    --num-speculative-tokens 5 \         # tokens to speculate
    --pipeline-parallel-size 1 \         # pipeline stages across GPUs (depth)
    --data-parallel-size 1 \             # data parallel replicas
    --api-key <secret>                   # require this key on all requests
```

### Prefix caching

Enable `--enable-prefix-caching` when many requests share the same system prompt or few-shot prefix (common in DSPy optimized programs):

```bash
vllm serve meta-llama/Llama-3.1-8B-Instruct \
    --enable-prefix-caching
```

This caches the KV cache for shared prompt prefixes, significantly speeding up DSPy programs that use the same few-shot demos across requests.

## DSPy optimization with vLLM

vLLM handles concurrent requests well, making it faster than Ollama for optimization:

```python
import dspy

lm = dspy.LM(
    "openai/meta-llama/Llama-3.1-8B-Instruct",
    api_base="http://localhost:8000/v1",
    api_key="none",
    max_tokens=1000,
)
dspy.configure(lm=lm)

# MIPROv2 sends many concurrent LM calls — vLLM handles this well
optimizer = dspy.MIPROv2(metric=metric, auto="medium")
optimized = optimizer.compile(program, trainset=trainset)
```

**Tip:** Start the vLLM server with `--max-num-seqs 256` to handle the optimizer's parallel requests efficiently.

## Develop with Ollama, deploy with vLLM

The recommended workflow for self-hosted models:

```python
import os
import dspy

# Same DSPy code, different LM config
if os.environ.get("ENV") == "production":
    # vLLM in production (high throughput, NVIDIA GPU)
    lm = dspy.LM(
        "openai/meta-llama/Llama-3.1-8B-Instruct",
        api_base="http://gpu-server:8000/v1",
        api_key="none",
    )
else:
    # Ollama in development (easy setup, any platform)
    lm = dspy.LM(
        "ollama_chat/llama3.1:8b",
        api_base="http://localhost:11434",
        api_key="",
        num_ctx=8192,
    )

dspy.configure(lm=lm)

# Everything below is identical regardless of backend
program = dspy.ChainOfThought("question -> answer")
program.load("optimized_program.json")
result = program(question="How do refunds work?")
```

The optimized program (instructions + demos) transfers between backends because DSPy optimizes at the prompt level, not the model level.

## Production deployment patterns

### Docker

```dockerfile
FROM vllm/vllm-openai:latest
ENV MODEL_NAME=meta-llama/Llama-3.1-8B-Instruct
EXPOSE 8000
CMD ["--model", "${MODEL_NAME}", "--host", "0.0.0.0", "--port", "8000", "--max-model-len", "8192"]
```

### Health check

```bash
curl http://localhost:8000/health
# Returns 200 when ready
```

### Behind a load balancer

Run multiple vLLM instances behind nginx or a cloud load balancer for horizontal scaling:

```bash
# Instance 1 (GPU 0)
CUDA_VISIBLE_DEVICES=0 vllm serve meta-llama/Llama-3.1-8B-Instruct --port 8001

# Instance 2 (GPU 1)
CUDA_VISIBLE_DEVICES=1 vllm serve meta-llama/Llama-3.1-8B-Instruct --port 8002
```

## Gotchas

- **Claude uses the deprecated `dspy.HFClientVLLM` class.** This was removed in DSPy 2.5+. Always use `dspy.LM("openai/model-name", api_base="http://localhost:8000/v1", api_key="none")` instead.
- **Claude omits `api_key` when connecting to vLLM.** LiteLLM (which DSPy uses under the hood) requires the `api_key` parameter even though vLLM does not authenticate. Set `api_key="none"` — any non-empty string works.
- **Claude recommends vLLM for macOS or Apple Silicon users.** vLLM requires NVIDIA GPUs with CUDA. If the user mentions macOS, M1/M2/M3/M4, or no NVIDIA GPU, route to `/dspy-ollama` instead.
- **Claude forgets `--enable-prefix-caching` for DSPy workloads.** DSPy optimized programs prepend the same few-shot demos to every request. Without prefix caching, vLLM recomputes the KV cache for those shared tokens on every call. Always recommend it for DSPy serving.
- **Claude sets `--max-model-len` too high for available VRAM.** This causes OOM on startup. Calculate available VRAM minus ~20% for KV cache overhead. For a 70B FP16 model on 2x A100-80GB, cap at ~8192 tokens. Suggest `--gpu-memory-utilization 0.9` as the default and tell users to lower `--max-model-len` if they hit OOM.

## Additional resources

- [vLLM documentation](https://docs.vllm.ai/en/latest/)
- [vLLM serve CLI reference](https://docs.vllm.ai/en/latest/cli/serve.html)
- [vLLM GitHub](https://github.com/vllm-project/vllm)
- For API details, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **LM configuration basics** (providers, parameters, caching) — `/dspy-lm`
- **Local development with Ollama** — `/dspy-ollama`
- **Deploying as an API** (FastAPI wrapper around your DSPy program) — `/ai-serving-apis`
- **Reducing costs** (model routing, caching) — `/ai-cutting-costs`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

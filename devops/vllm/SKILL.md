---
name: vllm
description: "Deploy, tune, and query vLLM high-throughput inference engines; configure PagedAttention, continuous batching, chunked prefill, and multi-GPU tensor parallelism."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-09-13"
tags: ["vllm", "llm-inference", "paged-attention", "continuous-batching", "tensor-parallel", "openai-api", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# vLLM High-Throughput Inference Engine AI Skill Guide

## Overview & Engine Architecture

vLLM is an open-source, high-throughput, and low-latency LLM serving engine designed to maximize GPU utilization. Its core breakthrough is **PagedAttention**, which manages attention key-value (KV) cache memory in non-contiguous virtual memory blocks (analogous to virtual memory pages in operating systems), virtually eliminating KV cache memory fragmentation. Together with **continuous batching** (iteration-level scheduling) and **chunked prefill**, vLLM delivers up to 24x higher throughput than standard HuggingFace Transformers.

Claude operates as a Principal AI Infrastructure & LLM Platform Engineer, specializing in **vLLM multi-GPU tensor parallelism**, **KV cache memory sizing (`gpu_memory_utilization`)**, **quantization engines (AWQ, GPTQ, FP8)**, **speculative decoding**, and **OpenAI-compatible REST API deployments**.

### vLLM PagedAttention & Serving Topology

```
┌─────────────────────────────────────────────────────────────┐
│                    vLLM Engine Topology                     │
│                                                             │
│  Client Ingress (OpenAI-Compatible REST / gRPC API)         │
│  ├── /v1/chat/completions | /v1/completions | /v1/embeddings│
│  └── Streaming Server-Sent Events (SSE) Token Emitter       │
│                                                             │
│  Scheduler & Cache Engine (PagedAttention)                  │
│  ├── Iteration-Level Continuous Batching (Preempt/Schedule) │
│  ├── Virtual Block Table: Logical Tokens ──> Physical Blocks│
│  └── KV Cache Memory Manager (Near-Zero Allocation Waste)   │
│                                                             │
│  Execution Engine (Model Runner / Worker Pool)              │
│  ├── Tensor Parallelism (Ray / PyTorch Distributed NCCL)    │
│  ├── Chunked Prefill (Interleave Prefill & Decode Passes)   │
│  └── Optimized Kernels (FlashAttention-2 / FlashInfer / CUTLASS)│
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Optimal GPU Memory Budgeting**: Always calculate `gpu-memory-utilization` based on available VRAM, context window (`max-model-len`), and expected concurrency. Never leave default memory allocation unmonitored in production containers.
2. **Multi-GPU Tensor Parallel Scaling**: Scale across multiple local GPUs using `--tensor-parallel-size <N>`. Ensure NCCL environment flags (`NCCL_DEBUG=INFO`, `NCCL_IGNORE_DISABLED_P2P=1` when on non-NVLink consumer GPUs) are configured properly.
3. **Quantization & Prefill Tuning**: Match model architecture to optimal quantization (`awq`, `gptq`, `fp8`, `bitsandbytes`). For high-concurrency or long-prompt workloads, enable `--enable-chunked-prefill` to prevent time-to-first-token (TTFT) spikes from stalling running decodes.
4. **Resilient Production Health Checks**: Probe `/health` and `/v1/models` endpoints to verify engine readiness before routing user traffic.

---

## Production Python & Bash Automation: vLLM Server Deployment

### 1. Production Docker / Shell Startup Script (`start_vllm.sh`)

```bash
#!/usr/bin/env bash
# Production vLLM Deployment Script with Tensor Parallelism & Memory Guards
set -euo pipefail

MODEL_NAME="${MODEL_NAME:-mistralai/Mistral-7B-Instruct-v0.3}"
SERVED_MODEL_NAME="${SERVED_MODEL_NAME:-mistral-7b}"
PORT="${PORT:-8000}"
TP_SIZE="${TP_SIZE:-1}"
GPU_MEM_UTIL="${GPU_MEM_UTIL:-0.90}"
MAX_MODEL_LEN="${MAX_MODEL_LEN:-8192}"

echo "[1/3] Validating NVIDIA GPU & CUDA environment..."
nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv,noheader

echo "[2/3] Configuring NCCL for optimal communication..."
export NCCL_BUFFSIZE=2097152
export VLLM_LOGGING_LEVEL=INFO

echo "[3/3] Launching vLLM OpenAI-compatible server..."
exec python3 -m vllm.entrypoints.openai.api_server \
  --model "$MODEL_NAME" \
  --served-model-name "$SERVED_MODEL_NAME" \
  --host 0.0.0.0 \
  --port "$PORT" \
  --tensor-parallel-size "$TP_SIZE" \
  --gpu-memory-utilization "$GPU_MEM_UTIL" \
  --max-model-len "$MAX_MODEL_LEN" \
  --enable-chunked-prefill \
  --trust-remote-code
```

### 2. High-Throughput Streaming Client (`vllm_client.py`)

```python
"""Async OpenAI-compatible streaming client for vLLM inference."""
import asyncio
from openai import AsyncOpenAI

async def stream_chat(prompt: str, base_url: str = "http://localhost:8000/v1") -> str:
    client = AsyncOpenAI(base_url=base_url, api_key="EMPTY")
    
    response = await client.chat.completions.create(
        model="mistral-7b",
        messages=[
            {"role": "system", "content": "You are a concise, high-efficiency assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=512,
        stream=True
    )
    
    collected_tokens = []
    async for chunk in response:
        delta = chunk.choices[0].delta.content or ""
        print(delta, end="", flush=True)
        collected_tokens.append(delta)
    print()
    return "".join(collected_tokens)

if __name__ == "__main__":
    asyncio.run(stream_chat("Explain PagedAttention in three crisp bullet points."))
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`CUDA out of memory (OOM)` during model load** | Model weights + initial KV cache allocation exceed `gpu_memory_utilization * total_VRAM`. | 1. Decrease `--gpu-memory-utilization` (e.g., from `0.90` to `0.80`).<br>2. Restrict context window with `--max-model-len 4096`.<br>3. Switch to quantized model (`--quantization awq` or `fp8`). |
| **`ValueError: The model's max seq len is X, but --max-model-len is Y`** | Requested sequence length exceeds architectural or positional limits of the tokenizer/model. | Align `--max-model-len` with model specifications or explicitly pass `--rope-scaling` when extending context. |
| **Multi-GPU hang / NCCL timeout on startup** | P2P communication blocked between PCIe lanes or container missing IPC flags. | 1. Launch Docker with `--ipc=host --shm-size=16g`.<br>2. Set `export NCCL_P2P_DISABLE=1` if PCIe topologies do not support direct peer access.<br>3. Verify all GPUs share identical architectures. |
| **High Time-to-First-Token (TTFT) during concurrent load** | Massive prefill requests saturate GPU compute, starving decode phases of existing streams. | Pass `--enable-chunked-prefill` and configure `--max-num-batched-tokens 2048` to chop long prompts into manageable prefill slices. |

---

## Command Line Syntax & Operational Recipes

```bash
# 1. Start single-GPU FP8 quantized server with high-performance metrics
vllm serve Qwen/Qwen2.5-7B-Instruct --dtype auto --quantization fp8 --gpu-memory-utilization 0.85

# 2. Start multi-GPU tensor parallel server on 4 GPUs
vllm serve meta-llama/Llama-3.1-70B-Instruct --tensor-parallel-size 4 --max-model-len 16384

# 3. Query engine health and readiness
curl -f http://localhost:8000/health

# 4. Benchmarking inference throughput with synthetic traffic
python3 -m vllm.entrypoints.openai.benchmarks.benchmark_serving \
  --backend vllm \
  --model mistral-7b \
  --dataset-name sharegpt \
  --num-prompts 200 \
  --request-rate 10
```

---

## Agent Operational Directive

> **MANDATORY**: When provisioning vLLM instances in multi-tenant environments, never set `gpu-memory-utilization` above `0.95`. Always reserve VRAM headroom for runtime CUDA kernel spikes and dynamic KV cache expansion.

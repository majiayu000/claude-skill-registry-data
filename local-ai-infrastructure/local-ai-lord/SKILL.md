---
name: local-ai-lord
description: Lord skill for local AI and edge deployment — runtime selection (Ollama, LM Studio, vLLM, llama.cpp, MLX), quantization, GPU acceleration, OpenAI-compatible APIs, and hybrid local+cloud patterns. Do not use for local seo tasks — use `local-seo` instead.
triggers:
  - local ai lord
  - local ai
  - ollama
  - lm studio
  - llama.cpp
  - vllm
  - localai
  - edge ai
  - ذكاء اصطناعي محلي
  - تشغيل محلي
personas:
  - ML
  - SRE
  - SEC
  - DEVOPS
  - ARCH
  - MLOPS
tech_stack: []
lord: true

---

# Local AI Lord

[OBJ] Deploy and operate AI models locally and at the edge — runtime selection, quantization, GPU acceleration, monitoring, and security — with hybrid local+cloud fallback patterns.

## Problem

Cloud AI APIs have per-token costs, latency, data residency constraints, and availability dependencies. Local AI eliminates per-token cost, keeps data on-device, and works offline — but requires careful runtime selection, quantization tradeoffs, GPU management, and security hardening. A wrong runtime or quantization choice turns a fast local model into a slow, OOM-crashing mess.

## Rules

1. [REQ] **Local runtime selection.** Ollama 0.33 (easiest, model management, OpenAI-compatible API), LM Studio 0.4.0 (GUI, model discovery, OpenAI-compatible), Jan (open-source, cross-platform), GPT4All (CPU-first, lightweight), llama.cpp (max control, C++, every platform), vLLM 0.28 (high-throughput server, GPU, PagedAttention), LocalAI (drop-in OpenAI replacement, multi-model), Tabby (code completion focused), Apple MLX (Apple Silicon optimized). Match runtime to hardware and use case.
2. [REQ] **Model selection and quantization.** Default to Q4_K_M (good quality/size balance) or Q5_K_M (higher quality, larger). GGUF format for Ollama/llama.cpp/LM Studio. Test quality degradation vs the full-precision model on your task — do not assume Q4 is "good enough" without measurement.
3. [REQ] **GPU acceleration.** CUDA (NVIDIA, most supported), Metal (Apple Silicon, MLX/llama.cpp), ROCm (AMD, Linux), Vulkan (cross-vendor, llama.cpp), WebGPU (browser, experimental). Verify GPU is actually used — check VRAM utilization, not just that it doesn't error.
4. [REQ] **Memory management.** Model must fit in VRAM/RAM with headroom for context. Rule of thumb: model size × 1.3 (overhead). If model + context > VRAM, it spills to CPU = 10-100× slower. Monitor VRAM usage; OOM kills are silent in some runtimes.
5. [REQ] **Context window optimization.** Larger context = more VRAM + slower. Set context to the actual need, not the model max. Use context caching (vLLM prefix caching, Ollama keep_alive) for repeated system prompts. Rotating context (sliding window) for long conversations.
6. [REQ] **OpenAI-compatible API.** Expose a local OpenAI-compatible endpoint (Ollama, LM Studio, vLLM, LocalAI all support this). Applications talk to `http://localhost:PORT/v1/chat/completions`. Enables swapping local ↔ cloud by changing the base URL. No application code changes needed.
7. [REQ] **Batch vs streaming inference.** Use streaming for interactive UX (token-by-token display). Use batch for throughput (process multiple requests together — vLLM continuous batching). Never batch interactive requests — latency per token matters more than throughput.
8. [REQ] **Concurrent requests.** vLLM supports high concurrency via continuous batching. Ollama supports sequential or limited parallel (OLLAMA_NUM_PARALLEL). LM Studio supports limited concurrent. Match concurrency setting to hardware — too high = OOM, too low = poor throughput.
9. [REQ] **Caching strategies.** Prefix caching (cache the system prompt + few-shot examples — vLLM, SGLang support this). Semantic caching (cache similar queries — use a vector DB). KV cache reuse across requests with same prefix. Caching reduces latency and cost for repeated patterns.
10. [REQ] **Monitoring.** Track: GPU memory utilization, GPU temperature, queue depth, tokens/sec, time-to-first-token (TTFT), request latency P50/P95, OOM events, model load time. Alert on VRAM >90%, queue depth > threshold, TTFT regression. No local deployment without monitoring.
11. [REQ] **Security — network binding.** Bind to `127.0.0.1` or `localhost` by default. Never bind to `0.0.0.0` without auth. If remote access needed, use a reverse proxy (nginx/caddy) with TLS + authentication. Exposed local AI = unauthenticated LLM access = prompt injection attack surface.
12. [REQ] **Security — auth.** If the local API is network-accessible, require API key authentication. Ollama: use a reverse proxy with auth. vLLM: `--api-key` flag. LM Studio: not designed for remote — use proxy. No unauthenticated network-exposed AI endpoint.
13. [REQ] **Security — sandboxing.** If the local AI executes tools or code (agent mode), sandbox the execution environment: Docker container, gVisor, or seccomp. No local AI agent with tool execution runs without sandboxing — prompt injection can invoke tools.
14. [REQ] **Cost comparison with cloud.** Calculate break-even: (cloud cost per 1M tokens) × (monthly token volume) vs (hardware cost / amortization + electricity). Local wins at high volume. Cloud wins at low volume or spiky load. Document the analysis — do not assume local is always cheaper.
15. [REQ] **Hybrid local+cloud patterns.** Route by task: local for simple/fast/private tasks, cloud for complex/high-quality tasks. Use a gateway (Portkey, LiteLLM, OpenRouter) to route based on task type, latency budget, or data sensitivity. Fallback: if local is overloaded, route to cloud. No hard dependency on either.
16. [PROHIBIT] Exposing a local AI endpoint to the network without TLS + authentication, or running a local AI agent with tool execution outside a sandbox — these are critical security failures.

## References

- Ollama: https://ollama.com
- LM Studio: https://lmstudio.ai
- llama.cpp: https://github.com/ggerganov/llama.cpp
- vLLM: https://vllm.ai
- LocalAI: https://localai.io
- Apple MLX: https://github.com/ml-explore/mlx
- Tabby: https://tabbyml.com
- Jan: https://jan.ai
- GPT4All: https://gpt4all.io

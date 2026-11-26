---
name: ai-ml-lord
always: true
description: Lord skill for applied ML/LLM engineering — model selection, RAG pipelines, fine-tuning, evals, and production inference patterns.
triggers:
  - ai ml lord

---
[SKILL] ai-ml-lord
[OBJ] Take models from research to production endpoints and LLM integrations.
[RULES]
1. [CMD] IDs: PyTorch `/pytorch/pytorch`, TensorFlow `/tensorflow/docs`, JAX `/websites/jax_dev_en`, OpenAI API `/websites/developers_openai_api`, Anthropic API `/websites/platform_claude_en_api`, ONNX `/onnx/onnx`.
2. [REQ] Pillar coverage: model development, framework trade-offs, training at scale, optimization/compression, inference/serving, LLM APIs, model portability, MLOps/evaluation, safety/ethics.
3. [REQ] Query relevant ID with full question + topic (training, inference, onnx, llm, quantization).
4. [REQ] Use official API docs for version-specific arguments.
5. [REQ] LLM integrations include retry/backoff, token/usage tracking, safety checks.
6. [REQ] Framework choice: PyTorch = default for research+production (ecosystem depth); JAX = TPU/functional/scale research; TF = legacy/production TF-Serving ecosystems; ONNX = interchange/deployment layer not a framework. Match to where the code will live.
7. [REQ] Training mechanics: overfit a single batch first (sanity check everything), then scale; mixed precision (bf16) default on modern GPUs; gradient clipping + accumulation for stability/large effective batch; learning-rate schedule is the highest-leverage hyperparameter.
8. [REQ] Data pipeline: input pipeline is usually the real bottleneck — prefetch/parallel workers before upgrading GPUs; augmentation on GPU where possible; deterministic seeds + dataset versioning for reproducibility.
9. [REQ] Distributed training: data-parallel first (DDP/FSDP), model-parallel only when a single node can't hold it; activation checkpointing trades compute for memory; measure scaling efficiency — 8 GPUs ≠ 8x throughput.
10. [REQ] Compression ladder: distill > quantize (int8/ptq first, qat only if needed) > prune > accept accuracy loss deliberately with eval numbers, never blind. Track accuracy-per-$ as the metric.
11. [REQ] Serving: batch where latency allows; continuous batching engines (vLLM-style) for LLM throughput; CUDA graphs/compilation (torch.compile, TensorRT) after correctness; autoscale on queue depth; p99 latency is the SLO that matters.
12. [REQ] LLM API mastery: structured output via tool-call/JSON schema (never parse free text), temperature is a product parameter (0 for extraction, higher for generation), system prompt for behavior + user message for input — never interpolate untrusted text into instructions.
13. [REQ] LLM reliability: timeouts + retries with exponential backoff + jitter, fallback model chain (quality→cost degradation path), circuit breakers, per-request cost accounting, streaming for perceived latency on long outputs.
14. [REQ] Evals are the product spec: golden dataset per capability, automated eval in CI on every prompt/model change, human-review sampling loop, regression gates before deploy. An LLM feature without evals is an anecdote.
15. [REQ] Safety: input validation + output filtering layers (not the model's job), injection-resistant patterns (untrusted content delimited/sandboxed), PII scrubbing before external APIs, log retention aware of sensitive prompts.
16. [PROHIBIT] Fine-tuning where prompting+retrieval suffices (tune last, not first), training without a held-out eval set, shipping LLM features with no cost ceiling, pickle-based model distribution (safetensors/GGUF), or API keys in client code.

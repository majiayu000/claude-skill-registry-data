---
name: inference-runtime-select
description: Use at the start of any model-inference feature to choose the runtime by deployment target (browser tab, one desktop, GPU server, or iOS/Android) and size the model to the device's memory before writing integration code.
stacks: [node, python]
domains: [web, data]
phases: [dev]
tags: [inference, llm, webgpu, onnx, coreml, executorch, ollama, vllm, quantization]
scope: kit
---
**When to use.** Before integrating any local/served model. *Why:* the right engine is a function of
*where it runs*, not benchmarks; picking wrong means a rewrite. Memory budget gates model choice.

**Procedure.**
1. Name the target surface → map to runtime: browser → Transformers.js/WebLLM/ONNX Runtime Web; one desktop → Ollama/llama.cpp; many users on GPU → vLLM/SGLang; mobile → Core ML/ExecuTorch/LiteRT/ORT-Mobile.
2. Size it: Q4 ≈ 0.5 GB/1B params; model + KV cache must fit usable VRAM. Pick a smaller model over sub-Q4 quantization (low precision fabricates).
3. Plan first-load weight caching (Cache API/OPFS on web).
4. **Done when:** a chosen-runtime + model + memory-budget line is recorded, and a smoke inference runs on the target device.

**Knowledge:** KNOWLEDGE-LIBRARY.md §A3.

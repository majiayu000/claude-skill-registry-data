---
name: llama-cpp
description: >
  Guide for llama.cpp, the C/C++ LLM inference framework by ggml-org. Covers the C API
  (llama.h), GGUF format, quantization (Q4_K_M, Q8_0, IQ4_XS), CMake builds, GPU backends
  (CUDA, Vulkan, Metal, ROCm), HTTP server with OpenAI-compatible API, embeddings, grammar
  constraints, function calling, LoRA, speculative decoding, multimodal, and UE5 integration.
  Use when: llama.cpp, GGUF models, local LLM inference, llama.h, llama-server, quantizing,
  ggml, building/linking llama.cpp, GPU acceleration, llama.cpp embeddings, grammar/JSON
  output, llama.cpp in Unreal Engine, llama_* API functions, GGUF format, converting
  HuggingFace to GGUF, or comparing with vLLM/Ollama/TensorRT-LLM.
---

# llama.cpp -- C/C++ LLM Inference Framework Guide

## Official Documentation

| Source | URL |
|--------|-----|
| **GitHub Repository** | https://github.com/ggml-org/llama.cpp |
| **C API Header (llama.h)** | https://github.com/ggml-org/llama.cpp/blob/master/include/llama.h |
| **C++ RAII Wrappers** | https://github.com/ggml-org/llama.cpp/blob/master/include/llama-cpp.h |
| **Build Instructions** | https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md |
| **Server Documentation** | https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md |
| **Quantization Tool** | https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/README.md |
| **GGUF Specification** | https://github.com/ggml-org/ggml/blob/master/docs/gguf.md |
| **Function Calling Docs** | https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md |
| **Multimodal Docs** | https://github.com/ggml-org/llama.cpp/blob/master/docs/multimodal.md |
| **Examples Directory** | https://github.com/ggml-org/llama.cpp/tree/master/examples |
| **HuggingFace GGUF Hub** | https://huggingface.co/docs/hub/gguf-llamacpp |
| **Llama-Unreal Plugin** | https://github.com/getnamo/Llama-Unreal |

## What is llama.cpp?

llama.cpp is a pure C/C++ LLM inference engine with minimal dependencies, designed for high-performance local inference across CPUs and GPUs. Key properties:

- **MIT licensed**, extremely active development (~daily releases, currently b8766+)
- **Widest hardware support**: NVIDIA (CUDA), AMD (ROCm/Vulkan), Apple (Metal), Intel (SYCL/Vulkan), Qualcomm (OpenCL), ARM, WebGPU
- **GGUF model format**: single-file, mmap-compatible, 40+ quantization types from 1.5-bit to 16-bit
- **Built-in HTTP server**: OpenAI-compatible API, Anthropic Messages API, streaming, function calling, multimodal
- **Language bindings**: Python (llama-cpp-python), Go, Rust, C#, Node.js, Java, Swift, and more

## Quick Start

### Run a model via server (fastest path)

```bash
# Install
brew install llama.cpp    # macOS/Linux
winget install llama.cpp  # Windows

# Start server with a HuggingFace model
llama-server -hf bartowski/Llama-3.3-70B-Instruct-GGUF:Q4_K_M -ngl 99

# Query via curl
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello"}],"temperature":0.8}'
```

### Embed in a C++ project (library usage)

```cpp
#include "llama.h"

// 1. Init backends and load model
ggml_backend_load_all();
auto params = llama_model_default_params();
params.n_gpu_layers = 99;
llama_model * model = llama_model_load_from_file("model.gguf", params);

// 2. Create context
auto ctx_params = llama_context_default_params();
ctx_params.n_ctx = 4096;
llama_context * ctx = llama_init_from_model(model, ctx_params);

// 3. Tokenize, decode, sample (see C API reference for full pattern)
```

### Build from source with GPU

```bash
git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
cmake -B build -DGGML_CUDA=ON      # or GGML_VULKAN=ON, GGML_METAL=ON
cmake --build build --config Release -j
```

## Core Architecture

```
llama.cpp/
  include/
    llama.h          # C API (primary interface)
    llama-cpp.h      # C++ RAII wrappers (unique_ptr aliases)
    ggml.h           # Tensor computation library
  common/
    common.h         # High-level convenience layer
  tools/
    server/          # HTTP server (llama-server)
    quantize/        # Model quantization tool
  examples/
    simple/          # Minimal inference example
    simple-chat/     # Multi-turn chat example
```

**Inference pipeline:**
```
Model (GGUF file)
  -> llama_model_load_from_file()  [load + mmap weights]
  -> llama_init_from_model()       [create context with KV cache]
  -> llama_tokenize()              [text -> tokens]
  -> llama_decode()                [run transformer, fill KV cache]
  -> llama_get_logits()            [get output probabilities]
  -> llama_sampler_sample()        [select next token]
  -> llama_token_to_piece()        [token -> text]
  -> repeat decode/sample loop until EOS
```

## Quantization Quick Reference

| Type | Bits | Quality | Recommended For |
|------|------|---------|-----------------|
| **Q4_K_M** | ~4.5 | Good | **Default choice** -- best quality/size balance |
| **Q5_K_M** | ~5.5 | Very good | When ~20% more space is acceptable |
| **Q8_0** | 8 | Near-lossless | Validation, quality-critical tasks |
| **IQ4_XS** | ~4.25 | Best at 4-bit | With imatrix, slightly smaller than Q4_K_M |
| **Q3_K_M** | ~3.5 | Acceptable | RAM-constrained scenarios |
| **IQ2_XS** | ~2.3 | Reduced | Extreme compression (needs imatrix) |
| **F16** | 16 | Reference | Full precision baseline |

```bash
# Quantize a model
llama-quantize model-f16.gguf model-q4km.gguf Q4_K_M

# Convert from HuggingFace
python convert_hf_to_gguf.py /path/to/hf_model --outfile model.gguf
```

## GPU Backends

| Backend | Flag | Hardware |
|---------|------|----------|
| CUDA | `GGML_CUDA=ON` | NVIDIA GPUs |
| Metal | auto on macOS | Apple Silicon |
| Vulkan | `GGML_VULKAN=ON` | Cross-platform (NVIDIA/AMD/Intel) |
| HIP | `GGML_HIP=ON` | AMD GPUs (ROCm) |
| SYCL | `GGML_SYCL=ON` | Intel GPUs |

**GPU offloading** (`-ngl 99`) is the single most impactful performance setting.

## Server API

The built-in server provides OpenAI-compatible endpoints:

| Endpoint | Purpose |
|----------|---------|
| `POST /v1/chat/completions` | Chat (streaming supported) |
| `POST /v1/completions` | Text completion |
| `POST /v1/embeddings` | Embeddings |
| `POST /v1/messages` | Anthropic Messages API |
| `POST /completion` | Native API with full parameter control |
| `GET /health` | Health check |
| `GET /metrics` | Prometheus metrics |

Features: function calling (`--jinja`), grammar constraints (`--grammar`/`--json-schema`), multimodal (vision+audio), parallel decoding, speculative decoding, router mode, LoRA hot-swap, built-in web UI.

## CMake Integration

```cmake
# Method 1: Subdirectory (embedding)
add_subdirectory(vendor/llama.cpp)
target_link_libraries(myapp PRIVATE llama ggml)

# Method 2: Installed package
find_package(llama REQUIRED)
target_link_libraries(myapp PRIVATE llama)
```

## Detailed Reference Documents

- **C/C++ API reference**: See [references/c-api-reference.md](references/c-api-reference.md) for complete llama.h function signatures, types, enums, structs, sampling chain API, and full working examples
- **Build system & integration**: See [references/build-and-integration.md](references/build-and-integration.md) for all CMake options, GPU backend builds, library linking methods, Docker, and package managers
- **Server REST API**: See [references/server-api.md](references/server-api.md) for all HTTP endpoints, CLI flags, environment variables, curl examples, function calling, grammar constraints, and Python client usage
- **GGUF & quantization**: See [references/quantization-guide.md](references/quantization-guide.md) for GGUF format spec, all 40+ quantization types, imatrix generation, model conversion, hardware requirements, and supported architectures
- **Performance & GPU backends**: See [references/performance-and-backends.md](references/performance-and-backends.md) for backend comparison, CUDA/Vulkan/Metal optimization, memory management, speculative decoding, and hardware recommendations
- **Unreal Engine integration**: See [references/unreal-engine-integration.md](references/unreal-engine-integration.md) for Llama-Unreal plugin, custom C++ integration with Build.cs, HTTP server approach, performance in-game, and common UE pitfalls

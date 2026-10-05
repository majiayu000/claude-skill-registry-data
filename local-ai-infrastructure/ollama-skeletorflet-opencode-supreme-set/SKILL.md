---
name: ollama
description: Ollama for local LLM inference and model management
---

### Core Concepts
- **Model Management**: `ollama pull <model>` downloads, `ollama run <model>` launches
- **Modelfile**: Configuration file to customize model parameters, system prompt, template
- **Ollama API**: REST endpoint at `localhost:11434` for chat, generate, embeddings
- **Local Inference**: Run LLMs entirely offline on CPU or GPU with no cloud dependency
- **Quantization**: GGUF format with Q4_K_M, Q5_K_M, Q8_0 levels balancing speed/quality
- **OpenAI Compatibility**: Drop-in replacement via `OPENAI_BASE_URL=http://localhost:11434/v1`

### Common Patterns
- `ollama pull llama3.2:3b` then `ollama run llama3.2:3b` for first-time setup
- Custom Modelfile with `FROM llama3.2`, `PARAMETER temperature 0.7`, `SYSTEM "You are..."`
- Python client: `requests.post("http://localhost:11434/api/generate", json={"model": "llama3.2", "prompt": "..."})`
- OpenAI-compatible: `openai.OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")`
- Embeddings via `POST /api/embeddings` with model like `nomic-embed-text`

### Best Practices
- Match quantization to hardware: Q4_K_M for 8GB VRAM, Q8_0 for 16GB+
- Set `OLLAMA_NUM_PARALLEL=4` and `OLLAMA_MAX_LOADED_MODELS=2` for concurrent use
- Use Modelfile `TEMPLATE` for chat format alignment with each model
- Pre-pull models during deployment to avoid first-request latency
- Monitor `ollama ps` to see loaded models and memory usage

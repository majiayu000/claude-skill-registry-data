---
name: system/model-selector
description: Select the correct Ollama base model (and adapters) based on task type, resource fit, and registry availability. Use to translate Modelfile FROM/ADAPTER decisions into agent behavior.
---

# Model Selector (Ollama Controller)

Capabilities
- fetch_model_registry: list local (`ollama list`) and remote options.
- evaluate_resource_fit: check VRAM/CPU fit vs. model size/quantization.
- select_base_architecture: pick code (DeepSeek), chat (Llama3), vision (LLaVa), etc.
- apply_lora_adapter: attach/choose adapters when needed.

Dependencies
- proxy-aware-fetcher (optional for remote registry)
- embedding-backend-selector (for embeddings route)

Outputs
- chosen model name, adapter info, and rationale.

---
name: conscience/embedding-backend-selector
description: Choose the best embedding backend (OpenVINO NPU → Ollama embeddings → sentence-transformers CPU) and fall back gracefully with logging. Use when embedding reliability matters.
---

# Embedding Backend Selector

Capabilities
- assess_backends: probe availability/latency of NPU, Ollama embeddings, sentence-transformers.
- select_backend: choose best available backend per policy.
- fallback_on_error: switch to next backend and log the event.

Dependencies
- embedding-repair
- reliability-budget (optional SLO tracking)

Inputs
- policy (preferred order), test text.

Outputs
- chosen backend info, status, error log if any.

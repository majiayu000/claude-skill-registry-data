---
name: chappie-backend
description: Backend development for CHAPPiE. Use when working on FastAPI APIs, the modular runtime, vLLM, Groq, Ollama, training, or compatibility factories.
---

# CHAPPiE Backend

## Entrypoints

- App API: `python3 app.py`, port 8010
- Steering API: `python3 -m brain.steering_api_server`, port 8000
- Training: `python3 -m Chappies_Trainingspartner.training_daemon`
- Runtime factory: `web_infrastructure.chappie_runtime.create_chappie_backend`
- Compatibility factory: `web_infrastructure.backend_wrapper.create_chappie_backend`

## Runtime modules

| File | Responsibility |
|---|---|
| `chappie_runtime.py` | public facade, construction and lifecycle |
| `turn_pipeline.py` | shared sync/stream turn order |
| `turn_context.py` | input normalization and context gates |
| `contracts.py` | typed internal contracts |
| `generation.py` | current brain lookup and generation |
| `formatting.py` | parsing, sanitizing and API message formatting |
| `persistence.py` | chat, STM and finalization writes |
| `backend_wrapper.py` | lightweight legacy imports only |

Routers use public runtime methods. Do not add new private-wrapper coupling.

## Providers

- vLLM is the fixed production web-chat route.
- Ollama and Groq remain supported for factory, CLI, training and research.
- There is no active Cerebras provider.
- Preserve provider fallback order unless a separate behavior change is approved.
- `GenerationGateway` must resolve the current brain lazily after settings reload.

## API and streaming

Preserve request schemas, response fields, status codes, SSE event names, ordering and completion behavior. Sync and stream use the same `TurnContext` and finalization intent.

## Tests

```bash
python3 tests/test_runtime_architecture.py
python3 tests/test_api_contract.py
python3 tests/test_vllm_response_handling.py
python3 tests/test_ollama_response_handling.py
python3 tests/test_training_daemon_lifecycle.py
```

Use `requirements/ci.txt` for deterministic backend tests. Do not require GPU weights in offline CI.

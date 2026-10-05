---
name: ai-provider-debug
description: Debug and troubleshoot AI/LLM provider integrations in ettametta. Use when investigating API failures, rate limits, fallback chain issues, model selection problems, or cost anomalies across 17+ providers.
---
# AI Provider Debugging

## Quick Diagnostics

```bash
curl http://localhost:8000/api/v1/llm/providers
curl http://localhost:8000/api/v1/llm/models
curl -X POST http://localhost:8000/api/v1/llm/reset-circuits
```

## Provider Registry

| Provider | SDK | Primary Use |
|---|---|---|
| Groq | groq SDK | Default LLM, fast inference |
| OpenAI | openai SDK | High-reasoning (GPT-4o) |
| Anthropic | anthropic SDK | Premium reasoning (Claude 3.5) |
| Google Gemini | google.genai | Cost-effective medium tasks |
| Ollama | OpenAI-compat | Zero-cost local inference |
| xAI (Grok) | openai (custom URL) | Grok-2 reasoning |
| DeepSeek | openai (custom URL) | DeepSeek-Chat/Coder |
| Mistral | openai (custom URL) | Mistral-Large |
| Cohere | cohere SDK | Command-R-Plus |
| Cerebras | openai (custom URL) | Llama-3.3-70b (30 RPM free) |
| Cloudflare | REST dict | Llama-3.1-70b |
| Hugging Face | REST dict | Llama-3.3-70B |
| OpenRouter | openai (custom URL) | Multi-model gateway |
| NVIDIA NIM | openai (custom URL) | Llama-3.3-70b |
| SiliconFlow | openai (custom URL) | Qwen2.5-72B |
| Ollama Cloud | openai (custom URL) | Qwen2.5:72b |
| Dify | Custom client | Orchestrator/workflow |
| vLLM | REST (OpenAI-compat) | High-throughput inference |

## Three Orchestration Layers

**1. IntelligenceHub** (`src/services/llm/intelligence_hub.py`)
- Complexity routing: low -> ollama, medium -> gemini/groq, high -> openai
- Circuit breaker per engine (5 failures -> open, 60s recovery)
- Auto-heal: rate limits after 10 min, 3+ errors -> degraded

**2. UnifiedLLMService** (`src/services/llm/service.py`)
- 7 providers, tries requested then iterates all
- tenacity retries: 3 attempts, exponential backoff 1-10s

**3. BaseEttamettaAgent** (`src/services/base_agent.py`)
- 17 providers, fixed fallback: primary -> ollama -> xai -> deepseek -> cerebras -> groq -> openai -> openrouter -> mistral -> siliconflow -> nvidia -> gemini -> anthropic

## Fallback Chains

- **VLM (Vision):** Groq Vision -> Local Moondream2 -> Gemini 1.5 Flash -> heuristic
- **CrewAI:** Groq (llama-3.3-70b-versatile) -> OpenAI (gpt-4o-mini) -> Ollama
- **Ollama self-failover:** primary URL -> localhost:11434

## Key Files

| File | Purpose |
|---|---|
| src/services/llm/service.py | UnifiedLLMService (7 providers) |
| src/services/llm/intelligence_hub.py | IntelligenceHub (complexity routing) |
| src/services/llm/dify_client.py | DifyClient with retries |
| src/services/base_agent.py | BaseEttamettaAgent (17 providers) |
| src/services/openclaw/agent.py | OpenClawAgent (17+ providers) |
| src/services/video_engine/vlm_service.py | VLMService (vision chain) |
| src/api/utils/vault.py | 3-tier secret resolution |
| src/api/utils/llm_vault.py | LLM vault (17 providers) |
| src/api/utils/resilience.py | CircuitBreaker |
| src/api/routes/llm.py | LLM API endpoints |

## Common Issues

### All providers failing — circuit breakers open
```bash
curl -X POST http://localhost:8000/api/v1/llm/reset-circuits
```

### Rate limited — auto-heal not working
IntelligenceHub auto-heals after 10 min. If stuck: reset circuits, check for 429 in logs.

### Placeholder key rejected
IntelligenceHub rejects keys containing "your_", "placeholder", "CHANGE_ME". Set real keys.

### Ollama not responding
```bash
docker compose ps ollama
curl http://localhost:11434/api/tags
docker compose exec ollama ollama list
```

### API key priority
Three-tier in `vault.py`: UserSetting DB -> SystemSettings DB -> .env

## Rate Limits

| Tier | Limit |
|---|---|
| FREE | 100/hr |
| PRO/PREMIUM/BASIC | 500/hr |
| SOVEREIGN/STUDIO | 5000/hr |

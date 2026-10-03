---
name: benchmark-ollama-llm
description: Profile Ollama LLM prefill/decode TPS across short text, long prompts, and vision+text inputs. Handles API routing, metric extraction, and result interpretation.
---

# Benchmark Ollama LLM Performance

Profile an Ollama model's prefill and decode throughput (TPS), token counts, and latency.

## Steps

1. **Write a Python script** using `requests` to hit `http://localhost:11434`.
2. **Route API endpoints correctly**:
   - Text-only prompts → `/api/generate`
   - Vision/multimodal prompts → `/api/chat`
3. **Extract timing metrics** from the JSON response:
   - `prompt_eval_duration` (prefill time)
   - `eval_duration` (decode time)
   - `prompt_eval_count` (prefill tokens)
   - `eval_count` (decode tokens)
4. **Calculate TPS**: `count / (duration / 1e9)`. If duration is `0`, report `0 TPS`.
5. **Run benchmarks** across categories: short text, long prompt, vision+text.

## Interpretation & Pitfalls

- **Decode TPS**: Stable metric. Expect ~80-120 TPS for 8B models on consumer iGPUs.
- **Prefill TPS inflation**: Long prompts often show artificially high prefill TPS (e.g., 100k+). Ollama caches prompt embeddings; the API returns near-zero `prompt_eval_duration` for cached prompts, inflating the calculated TPS. Always treat short-text prefill (~1k-3k TPS) as the accurate baseline.
- **Vision+Text failures**: The `/api/chat` endpoint for some multimodal models omits `prompt_eval_duration` and `eval_duration` in the JSON response. If timing stats are missing, report `N/A` and note the endpoint limitation. Verify the model actually supports vision (`ollama list`).
- **API Key/Billing**: Not required for local Ollama. Ensure Ollama is running and serving the target model (`ollama ps`).

## Example Python Snippet
```python
import requests, time
url = "http://localhost:11434/api/generate" # or /api/chat
payload = {"model": "mymodel", "prompt": "test", "stream": False}
r = requests.post(url, json=payload).json()
pe_d = r.get("prompt_eval_duration", 0)
ev_d = r.get("eval_duration", 0)
pe_c = r.get("prompt_eval_count", 0)
ev_c = r.get("eval_count", 0)
prefill_tps = pe_c / (pe_d / 1e9) if pe_d > 0 else 0
decode_tps = ev_c / (ev_d / 1e9) if ev_d > 0 else 0
```

---
name: traffic-cop
description: "Use for API-key health checks, rotation, and monitoring."
tags:
  - api-keys
  - rate-limiting
  - health-check
  - monitoring
  - key-rotation
  - openamer
---

# Traffic Cop — API-Key-Health-Check + Rate-Limit-Rotation

## Trigger

Use this skill whenever you need to:
- Check API key health across all providers
- Rotate a rate-limited or failed API key
- View usage statistics for API keys
- Set up or debug the Traffic Cop cron job

## Script

Das Skript `scripts/traffic-cop.py` liest alle API-Keys aus der `.env` (OpenAmer Home, `~/.env`, oder Repo `.env`), führt live HTTP-Health-Checks gegen die Provider-Endpoints durch und speichert den Zustand in `~/.traffic-cop/state.json`.

### CLI

```bash
python scripts/traffic-cop.py --check   # Live-Health-Check aller Keys
python scripts/traffic-cop.py --status  # Zeigt gespeicherten Key-Status
python scripts/traffic-cop.py --rotate <provider>  # Manuelle Key-Rotation
python scripts/traffic-cop.py --stats   # Nutzungsstatistik
```

### Exit-Codes

| Code | Bedeutung |
|------|-----------|
| 0 | Alle Keys OK |
| 1 | Einige Keys gedrosselt/fehlerhaft |
| 2 | Alle Keys tot — keine API erreichbar |

### Unterstützte Provider

OpenRouter, Ollama, OpenAI, Anthropic, Groq, Fireworks, DeepSeek, Mistral, Cohere, Together, Perplexity, Replicate, Gemini/Google AI, NovitaAI, GLM (z.ai), Kimi, DeepInfra, AI21, FAL, HuggingFace, ElevenLabs

Multi-Key-Pool pro Provider wird durch NUMERIC-Suffixe unterstützt (z.B. `OPENAI_API_KEY_2`, `OPENAI_API_KEY_3`).

### Cron

```bash
# Alle 15 Minuten Health-Check (automatisch via OpenAmer jobs.json)
# Job: traffic-cop, Script: traffic-cop.py
```

### State-Datei

`~/.traffic-cop/state.json` — JSON mit:
- `keys`: Pro Env-Var: provider, health, last_checked, last_ok, error_count, 429_count, 401_count
- `rotation`: Rotation-Log je Provider (current_index, historische Rotationen)
- `stats`: Aggregierte Statistiken (total_checks, total_rotations, total_errors, total_429, total_401)

### Fehlerbehandlung

- **429**: Rate-Limited → Key-State auf `rate_limited`, Rotation initiierbar
- **401/403**: Auth-Fail → Key-State auf `auth_fail`
- **Timeout**: DNS/Netzwerk-Problem → Key-State auf `timeout`
- **Unbekannt**: Anderer HTTP-Fehler → Key-State auf `error`
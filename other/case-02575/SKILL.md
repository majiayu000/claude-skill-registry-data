---
name: prompt-cache
description: SHA-256 prompt deduplication for LLM and TTS calls — hash normalize prompts, check cache before calling APIs, store results for instant replay. Use when making repeated or similar API calls to avoid redundant spending. Works with any database backend (SQLite, Turso, Postgres).
version: 1.0.0
metadata:
  {
      "openclaw": {
            "emoji": "\ud83d\udcbe",
            "requires": {
                  "bins": [],
                  "env": []
            },
            "primaryEnv": null,
            "network": {
                  "outbound": false,
                  "reason": "Local cache operations only. No external network calls."
            }
      }
}
---

# Prompt Cache

A lightweight caching layer that prevents regenerating identical content. Saved approximately 60% of API quota in production by catching duplicate prompts before they hit the API.

## How It Works

1. Normalize the prompt (lowercase, collapse whitespace)
2. Combine with context keys (user name, language, model)
3. SHA-256 hash the combined key
4. Check cache table for existing result
5. On miss: call API, store result. On hit: return cached result instantly.

## Usage

```python
import prompt_cache

# Check before calling expensive API
cached = await prompt_cache.get_cached(
    prompt="Tell me a story about clouds",
    child_name="Sophie",
    language="fr"
)

if cached:
    return cached  # Free! No API call needed.

# Cache miss — call the API
result = await generate_story(prompt, child_name, language)

# Store for next time
await prompt_cache.set_cached(prompt, child_name, language, result)
```

## Schema

```sql
CREATE TABLE IF NOT EXISTS prompt_cache (
    prompt_hash TEXT NOT NULL,
    child_name TEXT NOT NULL,
    language TEXT NOT NULL,
    story_json TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (prompt_hash, child_name, language)
);
```

## Adapt the Keys

The default implementation uses `(prompt, child_name, language)` as the cache key. Adapt to your domain:

- **Chat completions:** `(system_prompt, user_message, model)`
- **TTS:** `(text, voice_id, model_id)`
- **Image gen:** `(prompt, seed, model, size)`

## Files

- `scripts/prompt_cache.py` — Cache implementation (35 lines)

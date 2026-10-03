---
name: chappie-config
description: CHAPPiE's configuration system. Use when adding settings, changing config.py, updating schemas, or working with CHAPPIE_CONFIG.json and training config.
---

# CHAPPiE Configuration

## Sources

| Source | Role |
|---|---|
| `config/config.py` | settings, defaults, paths, provider enum and JSON mapping |
| `config/example_config.py` | readable tracked template |
| `config/prompts.py` | all active LLM prompt templates |
| `config/emotions.py` | ten emotion definitions and VAD mapping |
| `CHAPPIE_CONFIG.json` | ignored local overrides and secrets |
| `config/training_config.json` | ignored autonomous-training config |
| `api/schemas/` | external request/response validation |

There is no active `config/root_config.py`, `config/brain_config.py` or `CHAPPIE_CONFIG.example.json`.

## Providers

```python
class LLMProvider(str, Enum):
    OLLAMA = "ollama"
    GROQ = "groq"
    VLLM = "vllm"
```

vLLM with local Qwen is the production default. Never reintroduce Cerebras names into active config.

## Rules

- Add global values only in `config/config.py` and its example structure.
- Preserve unknown and missing-value compatibility.
- Keep local secrets in ignored files; never print keys in reload logs.
- Update API schemas, frontend types, docs and config tests together.
- Treat provider priority and persisted-key removal as explicit migrations.
- Existing root `training_config.json` remains readable; new writes use `config/training_config.json`.
- Import-time creation of data directories is currently a documented compatibility behavior.

## Tests

```bash
python3 tests/test_settings_integrity.py
python3 tests/test_root_config.py
python3 tests/test_runtime_switching.py
python3 tests/test_training_config_ui.py
```

---
name: models-dev
description: Query models.dev API to compare AI model pricing across all providers.
---

# models.dev

Compare AI model pricing across providers using the [models.dev](https://models.dev) open-source database.

## Usage

# Compare DeepSeek V4 Flash across all providers
curl -s "https://models.dev/api/v1/models/deepseek/deepseek-v4-flash" | \
  jq -r '.providers[] | "\(.name): \$\(.cost.input // "?")/\$\(.cost.output // "?")"'

### Common model IDs

| Model | ID |
|-------|-----|
| DeepSeek V4 Flash | `deepseek/deepseek-v4-flash` |
| DeepSeek V4 Pro | `deepseek/deepseek-v4-pro` |
| Claude Opus 4.8 | `anthropic/claude-opus-4-8` |
| GPT-5 | `openai/gpt-5` |

Use `deepseek/deepseek-v4-pro` for the more capable model.

## API

```
GET https://models.dev/api/v1/models/{model_id}           # providers + pricing
GET https://models.dev/api/v1/model/{provider}/{model_id}  # model metadata only
GET https://models.dev/api/v1/models/{model_id}?metadata=true  # both
```

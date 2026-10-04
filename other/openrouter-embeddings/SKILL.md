---
name: openrouter-embeddings
description: Generate text embeddings via OpenRouter using Qwen3-Embedding-8B.
---

# openrouter-embeddings

Text → embedding vector via OpenRouter. Default model: `qwen/qwen3-embedding-8b`.

## Usage

Resolve `TOOL_DIR` = the directory containing this `SKILL.md`. Commands below use `TOOL_DIR` as a symbolic placeholder; replace it with the resolved, quoted path before running Bash.

### Single text

```bash
export OPENROUTER_API_KEY=sk-or-v1-...

python3 TOOL_DIR/scripts/embed.py \
  --text "The quick brown fox jumps over the lazy dog" \
  --output vec.json
```

### Batch from JSONL

Input `records.jsonl` (one JSON per line):
```
{"id": "row_0", "text": "Every place name in the United States."}
{"id": "row_1", "text": "Nearby stars and potential exoplanets."}
```

Run:
```bash
python3 TOOL_DIR/scripts/embed.py \
  --jsonl records.jsonl \
  --output records_with_embeddings.jsonl \
  --batch-size 32
```

Output is the same JSONL with an added `embedding` field per line.

## Flags

| Flag | Default | Description |
|---|---|---|
| `--text` | — | Embed one string (mutually exclusive with `--jsonl`) |
| `--jsonl` | — | Embed many; each line must have a `text` field |
| `--output` | required | Output path |
| `--model` | `qwen/qwen3-embedding-8b` | Any embedding model on OpenRouter |
| `--batch-size` | `32` | Records per API call (jsonl mode) |
| `--dimensions` | — | Optional: truncate to N dims if supported |

## Endpoint

`POST /api/v1/embeddings` — OpenAI-compatible schema.

Request:
```json
{ "model": "qwen/qwen3-embedding-8b", "input": ["text1", "text2", ...] }
```

Response:
```json
{ "data": [ { "embedding": [0.01, -0.02, ...], "index": 0 }, ... ], "model": "...", "usage": {...} }
```

## Notes

- `qwen3-embedding-8b` outputs high-dimensional dense vectors suitable for semantic similarity, clustering, RAG.
- For cheaper batches, consider `qwen/qwen3-embedding-4b` or other listed embedding models (`GET /api/v1/embeddings/models`).

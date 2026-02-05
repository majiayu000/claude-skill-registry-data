---
name: setup-environment
description: Set up the embedding model for semantic search. model2vec-rs downloads models automatically; use when build fails or model download issues occur.
---

# Environment Setup for Semantic Search

## Instructions

glhf uses model2vec-rs with Potion-base-32M for embeddings. The model downloads automatically on first use.

## Quick Setup

No manual setup required:

```bash
cargo build --release
./target/release/glhf index
```

The embedding model (~130MB) will download to the HuggingFace cache on first run.

## Model Details

| Property | Value |
|----------|-------|
| Model | minishlab/potion-base-32M |
| Dimensions | 512 |
| Size | ~130MB |
| Cache Location | `~/.cache/huggingface/` |

## Verify Setup

```bash
# Run embedding tests
cargo test embed -- --ignored
```

## Common Issues

| Error | Solution |
|-------|----------|
| `Failed to load model` | Check internet connection, model will auto-download |
| `No space left` | Clear HuggingFace cache: `rm -rf ~/.cache/huggingface/` |
| `Slow first run` | Normal - model downloads once, then cached |

## Skip Embeddings

For text-only search (faster indexing, no model download):

```bash
glhf index --skip-embeddings
```

This enables FTS5 search but disables semantic/hybrid modes.

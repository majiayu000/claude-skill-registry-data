---
name: embedding-models
description: Embedding model configurations and cost calculators
allowed-tools: Bash, Read, Write, Edit, WebFetch
---

# Embedding Models Skill

Embedding model selection, configuration, and cost optimization for RAG pipelines.

## Use When

- Selecting embedding models for vector search
- Configuring OpenAI, Cohere, or HuggingFace embeddings
- Calculating embedding generation costs
- Optimizing embedding performance vs cost tradeoffs
- Setting up local vs cloud embedding models
- Implementing embedding caching strategies
- User mentions: "embeddings", "vector models", "embedding costs", "semantic search models"

## Model Selection Guide

### Commercial Models

**OpenAI Embeddings:**
- `text-embedding-3-small` - 1536 dims, $0.02/1M tokens, balanced performance
- `text-embedding-3-large` - 3072 dims, $0.13/1M tokens, highest quality
- `text-embedding-ada-002` - 1536 dims, $0.10/1M tokens, legacy model

**Cohere Embeddings:**
- `embed-english-v3.0` - 1024 dims, multilingual support
- `embed-english-light-v3.0` - 384 dims, faster/cheaper
- `embed-multilingual-v3.0` - 1024 dims, 100+ languages

### Open Source Models (HuggingFace)

**Sentence Transformers:**
- `all-MiniLM-L6-v2` - 384 dims, 80MB, fast and efficient
- `all-mpnet-base-v2` - 768 dims, 420MB, high quality
- `multi-qa-mpnet-base-dot-v1` - 768 dims, optimized for Q&A
- `paraphrase-multilingual-mpnet-base-v2` - 768 dims, 50+ languages

**Specialized Models:**
- `BAAI/bge-small-en-v1.5` - 384 dims, SOTA small model
- `BAAI/bge-base-en-v1.5` - 768 dims, excellent retrieval
- `BAAI/bge-large-en-v1.5` - 1024 dims, top performance
- `intfloat/e5-base-v2` - 768 dims, strong general purpose

## Cost Calculator

Use the cost calculator script to estimate embedding costs:

```bash
# Calculate costs for different models and volumes
python scripts/calculate-embedding-costs.py \
  --documents 100000 \
  --avg-tokens 500 \
  --model text-embedding-3-small

# Compare multiple models
python scripts/calculate-embedding-costs.py \
  --documents 100000 \
  --avg-tokens 500 \
  --compare
```

## Setup Scripts

### OpenAI Embeddings
```bash
bash scripts/setup-openai-embeddings.sh
```

Configures OpenAI embedding client with API key management and retry logic.

### HuggingFace Embeddings
```bash
bash scripts/setup-huggingface-embeddings.sh
```

Downloads and configures sentence-transformers models locally.

### Cohere Embeddings
```bash
bash scripts/setup-cohere-embeddings.sh
```

Sets up Cohere embedding client with API credentials.

## Configuration Templates

### OpenAI Configuration
```python
# templates/openai-embedding-config.py
from openai import OpenAI
client = OpenAI(api_key="your-key")

embeddings = client.embeddings.create(
    model="text-embedding-3-small",
    input=["Your text here"]
)
```

### HuggingFace Configuration
```python
# templates/huggingface-embedding-config.py
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(["Your text here"])
```

### Custom Model Template
```python
# templates/custom-embedding-model.py
# Wrapper for any embedding model with consistent interface
```

## Optimization Strategies

**Cost Optimization:**
1. Use smaller models for high-volume applications
2. Implement embedding caching (see examples/embedding-cache.py)
3. Batch embedding generation (see examples/batch-embedding-generation.py)
4. Consider local models for sensitive data

**Performance Optimization:**
1. Use GPU acceleration for local models
2. Batch processing for throughput
3. Dimension reduction for storage/speed
4. Model distillation for faster inference

## Model Comparison Matrix

| Model | Dimensions | Size | Speed | Quality | Cost |
|-------|-----------|------|-------|---------|------|
| text-embedding-3-small | 1536 | API | Fast | Good | $0.02/1M |
| text-embedding-3-large | 3072 | API | Medium | Excellent | $0.13/1M |
| all-MiniLM-L6-v2 | 384 | 80MB | Very Fast | Good | Free |
| all-mpnet-base-v2 | 768 | 420MB | Fast | Excellent | Free |
| bge-base-en-v1.5 | 768 | 420MB | Fast | Excellent | Free |
| embed-english-v3.0 | 1024 | API | Fast | Excellent | $0.10/1M |

## Examples

**Batch Embedding Generation:**
```python
# examples/batch-embedding-generation.py
# Process large document collections efficiently
```

**Embedding Cache:**
```python
# examples/embedding-cache.py
# Cache embeddings to avoid redundant API calls
```

## Decision Framework

**Use OpenAI when:**
- Need highest quality embeddings
- Low to medium volume (<10M tokens/month)
- Prefer managed service over self-hosting
- Working with latest models

**Use Cohere when:**
- Need multilingual support
- Require production SLA
- Want embedding customization
- Need both embedding and reranking

**Use HuggingFace/Local when:**
- High volume (>10M tokens/month)
- Data privacy requirements
- Have GPU infrastructure
- Cost optimization priority
- Offline/air-gapped environments

## References

- Sentence Transformers: https://www.sbert.net/
- OpenAI Embeddings: https://platform.openai.com/docs/guides/embeddings
- Cohere Embeddings: https://docs.cohere.com/docs/embeddings
- MTEB Leaderboard: https://huggingface.co/spaces/mteb/leaderboard

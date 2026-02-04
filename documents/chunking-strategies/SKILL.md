---
name: chunking-strategies
description: Document chunking strategies for RAG systems. Use when implementing document processing pipelines to determine optimal chunking approaches based on document type and retrieval requirements.
---

# Chunking Strategies Skill

This skill provides chunking strategies for RAG document processing.

## Chunking Methods

### 1. Fixed-Size Chunking
```python
def fixed_size_chunk(text: str, chunk_size: int = 500, overlap: int = 50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks
```

### 2. Semantic Chunking
Split on natural boundaries (sentences, paragraphs).

```python
def semantic_chunk(text: str, max_tokens: int = 500):
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = []
    current_tokens = 0

    for para in paragraphs:
        para_tokens = count_tokens(para)
        if current_tokens + para_tokens > max_tokens:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = [para]
            current_tokens = para_tokens
        else:
            current_chunk.append(para)
            current_tokens += para_tokens

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))
    return chunks
```

### 3. Recursive Chunking
Hierarchical splitting on multiple separators.

```python
SEPARATORS = ["\n\n", "\n", ". ", " "]

def recursive_chunk(text: str, max_size: int, separators: list[str]):
    if len(text) <= max_size:
        return [text]

    sep = separators[0] if separators else ""
    chunks = []
    parts = text.split(sep)

    for part in parts:
        if len(part) <= max_size:
            chunks.append(part)
        elif len(separators) > 1:
            chunks.extend(recursive_chunk(part, max_size, separators[1:]))
        else:
            chunks.append(part[:max_size])

    return chunks
```

## Chunking by Document Type

| Document Type | Recommended Strategy | Chunk Size |
|---------------|---------------------|------------|
| Technical docs | Semantic (headers) | 500-1000 tokens |
| Legal documents | Semantic (sections) | 1000-2000 tokens |
| Code | Function/class based | 200-500 tokens |
| Conversations | Message boundaries | 100-300 tokens |
| General text | Recursive | 300-500 tokens |

## Chunk Enrichment

```python
@dataclass
class EnrichedChunk:
    content: str
    metadata: dict
    summary: str  # LLM-generated
    keywords: list[str]
    parent_id: str  # For hierarchical retrieval
```

## Best Practices

- Add overlap between chunks (10-20%)
- Preserve semantic boundaries
- Include metadata (source, position)
- Consider hierarchical chunking for long docs
- Test retrieval quality with different sizes

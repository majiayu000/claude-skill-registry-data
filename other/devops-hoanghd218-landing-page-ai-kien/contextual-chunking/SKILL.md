---
name: contextual-chunking
description: Contextual Retrieval implementation for RAG - chunks clinical notes with LLM-generated context prepended to each chunk before embedding. Improves citation accuracy by 49% per Anthropic research.
---

# Contextual Chunking Skill

## Overview

This skill implements Anthropic's Contextual Retrieval pattern for RAG systems. It chunks clinical notes into fixed-size segments (1000 tokens, 200 token overlap) and generates 50-100 token contextual summaries for each chunk using Phi-4. The context is prepended to chunks before embedding, significantly improving retrieval accuracy for citation extraction.

## When to Use

Use this skill when:
- Preparing clinical notes for RAG-based summarization
- Creating embeddings for ChromaDB storage
- Need to improve citation accuracy and reduce hallucinations
- Processing multi-page clinical notes for semantic search

## Research Background

**Anthropic Contextual Retrieval Paper**: Prepending chunk-specific context improves retrieval accuracy by 49% over standard RAG. The context helps the embedding model understand each chunk's role within the larger document.

## Installation

**IMPORTANT**: This skill has its own isolated virtual environment (`.venv`) managed by `uv`. Do NOT use system Python.

Initialize the skill's environment:
```bash
# From the skill directory
cd .agent/skills/contextual-chunking
uv sync  # Creates .venv and installs dependencies from pyproject.toml
```

Dependencies are in `pyproject.toml`:
- `tiktoken` - Token counting for Phi-4

## Usage

**CRITICAL**: Always use `uv run` to execute code with this skill's `.venv`, NOT system Python.

### Basic Chunking with Context

```python
# From .agent/skills/contextual-chunking/ directory
# Run with: uv run python -c "..."
from contextual_chunking import ContextualChunker

# You'll need to import ollama-client separately
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "ollama-client"))
from ollama_client import OllamaClient

# Initialize
chunker = ContextualChunker(
    ollama_client=OllamaClient(),
    chunk_size=1000,        # Tokens per chunk
    chunk_overlap=200,      # Overlap between chunks (20%)
    context_size=75         # Context tokens (50-100 range)
)

# Chunk clinical note
clinical_note = "Patient presents with chest pain radiating to left arm..."

enriched_chunks = chunker.chunk_with_context(
    document_text=clinical_note,
    doc_id="note_123"
)

# Each enriched chunk contains:
for chunk in enriched_chunks:
    print(f"Chunk ID: {chunk['id']}")
    print(f"Original text: {chunk['original_text'][:100]}...")
    print(f"Context: {chunk['context']}")
    print(f"Enriched (context + text): {chunk['enriched_text'][:150]}...")
    print(f"Offsets: {chunk['start_offset']}-{chunk['end_offset']}")
    print("---")
```

### Integration with ChromaDB

```python
from src.skills.chroma_client.chroma_client import ChromaClient

# 1. Chunk with context
enriched_chunks = chunker.chunk_with_context(clinical_note, "note_123")

# 2. Store enriched chunks in ChromaDB
chroma_client = ChromaClient()
chroma_client.add_chunks(
    collection_name="clinical_note_session_456",
    chunks=[chunk['enriched_text'] for chunk in enriched_chunks],
    metadatas=[{
        'chunk_id': chunk['id'],
        'start_offset': chunk['start_offset'],
        'end_offset': chunk['end_offset'],
        'original_text': chunk['original_text']
    } for chunk in enriched_chunks],
    ids=[chunk['id'] for chunk in enriched_chunks]
)
```

## Context Generation Prompt

The LLM generates context with this prompt template:

```
Given the whole document context, provide succinct context (50-100 tokens) to situate this chunk for search retrieval purposes.

Document title/type: Clinical Note
Document context: [First 2000 chars of full document]

Chunk to contextualize:
{chunk_text}

Provide ONLY the context (no explanations):
```

**Example Output**:
```
Context: This section describes the patient's presenting symptoms during initial triage, specifically cardiovascular complaints requiring urgent evaluation.
```

## Chunk Structure

Each enriched chunk dictionary contains:
```python
{
    'id': 'note_123_chunk_0',
    'original_text': 'Patient presents with chest pain...',
    'context': 'This section describes presenting symptoms...',
    'enriched_text': 'This section describes presenting symptoms... Patient presents with chest pain...',
    'start_offset': 0,
    'end_offset': 1200,
    'token_count': 1000
}
```

## Configuration

**Parameters**:
- `chunk_size`: Tokens per chunk (default: 1000)
  - Too small: Context fragmentation, poor retrieval
  - Too large: Embedding quality degrades, slower search
  
- `chunk_overlap`: Token overlap (default: 200, ~20%)
  - Prevents information loss at boundaries
  - Critical for accurate citation offsets
  
- `context_size`: Context tokens (default: 75, range: 50-100)
  - Balances informativeness vs token cost
  - Generated by LLM for each chunk

## Best Practices

1. **Token Counting**: Use tiktoken for accurate Phi-4 token counts
2. **Context Quality**: Verify LLM generates succinct, relevant context
3. **Offset Tracking**: Maintain character offsets for citation extraction
4. **Batch Processing**: Generate contexts in batches for efficiency
5. **Cache Contexts**: Store enriched chunks to avoid regeneration

## Performance Considerations

**Chunking a 10-page note (5000 tokens)**:
- Chunks: ~5 chunks (1000 tokens each, 200 overlap)
- Context generation: 5 LLM calls (~5-10 seconds total)
- Total time: 10-15 seconds (acceptable for offline processing)

**Trade-offs**:
- **Pro**: 49% better retrieval accuracy
- **Pro**: Fewer hallucinations, better citations
- **Con**: Additional LLM inference time
- **Con**: Slightly higher token usage

## Error Handling

- If LLM context generation fails, fall back to empty context (still functional)
- If chunk exceeds token limit, split further
- Preserve original text and offsets even if context fails

## Integration with RAG Pipeline

**Workflow**:
1. **Chunk**: Use this skill to create enriched chunks
2. **Embed**: Store in ChromaDB (automatic embedding)
3. **Retrieve**: Query ChromaDB for relevant chunks
4. **Extract**: Use `citation-extraction` skill to validate citations
5. **Cleanup**: Clear ChromaDB collection after session

## Implementation

See `contextual_chunking.py` for the full Python implementation.

## References

- [Anthropic Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)
- [LangChain RAG Guide](https://python.langchain.com/docs/use_cases/question_answering)

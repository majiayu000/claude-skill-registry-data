---
name: intelligent-text-chunking
description: Split large texts into meaningful, AI-optimized chunks while preserving semantic coherence and document structure. Use when processing large documents for AI training, RAG systems, or when you need to break down content while maintaining context and relationships.
---

# Intelligent Text Chunking

## Overview

A sophisticated text segmentation skill that splits large texts into meaningful, AI-optimized chunks while preserving semantic coherence, document structure, and contextual relationships. Essential for processing large documents for AI training, RAG systems, and memory-constrained applications.

## Capabilities

- **Semantic Awareness**: Respects topic boundaries and meaning transitions
- **Structure Preservation**: Maintains document hierarchy and formatting context
- **Multi-language Support**: Handles accented characters and diverse writing systems
- **Configurable Strategies**: Multiple chunking approaches for different use cases
- **Context Preservation**: Intelligent overlap management for context continuity
- **Quality Optimization**: Balances chunk size with content coherence

## Chunking Strategies

### 1. Semantic Chunking

Split text based on meaning and topic boundaries rather than arbitrary size limits.

### 2. Structural Chunking

Follow document organization (headings, sections, lists) for natural divisions.

### 3. Fixed-Size Chunking

Create consistent-sized chunks with intelligent boundary selection.

### 4. Sliding Window Chunking

Create overlapping chunks for enhanced context preservation.

## Implementation Examples

### Language-Aware Processing

```python
# Multi-language sentence detection
sentence_patterns = {
    'english': ['.', '!', '?', ';'],
    'chuukese': ['.', '!', '?'],
    'general': ['.', '!', '?', ';', '。', '！', '？']
}

def detect_language_patterns(text):
    has_accents = bool(re.search(r'[áéíóúàèìòùāēīōūâêîôû]', text))
    return 'chuukese' if has_accents else 'english'
```

### Basic Usage

```python
from .intelligent_chunker import IntelligentTextChunker, ChunkType

chunker = IntelligentTextChunker(
    max_chunk_size=1024,
    overlap_ratio=0.15,
    preserve_sentences=True
)

chunks = chunker.chunk_document(text, ChunkType.SEMANTIC)
```

## Best Practices

1. **Size Balancing**: Balance chunk size with content coherence
2. **Context Preservation**: Use appropriate overlap for your use case
3. **Language Awareness**: Configure for specific languages when known
4. **Quality Validation**: Check chunk quality with sample reviews
5. **Use Case Optimization**: Choose strategy based on downstream use

## Dependencies

- `re`: Regular expression pattern matching
- `spacy`: Advanced sentence segmentation
- `nltk`: Natural language processing utilities
- `langdetect`: Language identification support

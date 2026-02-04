---
name: generation
description: Generates answers by synthesizing information from retrieved documents with citations. Use as final RAG pipeline step, when creating answers from multiple sources, or when the user mentions answer generation or synthesis.
---

# Answer Generation

## Instructions

Generate answers using functions in `components/generator.py`. Synthesizes information from graded-relevant documents or provides fallback when no context available.

**Default workflow:**

```python
# Use original query (not rewritten) for generation
result = generate_answer_with_metadata(original_query, relevant_documents)
answer = result['answer']
```

**Key functions:**

```python
# Standard generation with metadata (preferred)
result = generate_answer_with_metadata(query, documents, include_sources=True)
# Returns: answer, num_documents_used, has_context, sources, collections_used

# Basic generation
result = generate_answer(query, documents)
# Returns: answer, num_documents_used, has_context, model_used
```

**Generation modes:**

1. **With context** (documents provided): Synthesizes from multiple documents with source attribution
2. **Without context** (no documents or empty list): Acknowledges lack of information, provides helpful fallback

**Critical:** Always use `original_query` for generation, NOT `current_query` (which may be rewritten). This ensures the answer addresses what the user actually asked.

**Implementation:** `components/generator.py`, uses `GENERATION_MODEL` from `config.py` (default: Haiku 4.5), temperature 0.3, max tokens 2000.

## Examples

### Example 1: Standard generation with context

```python
# Input
result = generate_answer_with_metadata(
    "What gaming laptops do you have?",
    relevant_documents  # 3 documents from catalog
)

# Output
{
    "answer": "We have several gaming laptops including TechBook Pro 15 with RTX 4060...",
    "num_documents_used": 3,
    "has_context": True,
    "sources": ["techmart_catalog.csv"],
    "collections_used": ["catalog"]
}
```

### Example 2: Fallback (no documents)

```python
# Input
result = generate_answer("obscure query", [])

# Output
{
    "answer": "I don't have relevant information about this in our knowledge base...",
    "num_documents_used": 0,
    "has_context": False,
    "sources": [],
    "collections_used": []
}
```

### Example 3: Pipeline integration

```python
# After retrieval, grading, retries
if relevant_documents:
    # Generate with context
    generation_result = generate_answer_with_metadata(
        original_query,  # NOT current_query
        relevant_documents
    )
    print(f"✓ Answer from {generation_result['num_documents_used']} docs")
else:
    # Fallback after exhausting retries
    generation_result = generate_answer(original_query, [])
    print("⚠ Fallback answer (no relevant docs)")

print(generation_result['answer'])
```

### Example 4: Using original vs rewritten query

```python
# Setup
original_query = "gaming laptops"
current_query = "high performance gaming laptop computers RTX graphics"  # Rewritten

# After retrieval with current_query
relevant_docs = filter_relevant_documents(graded_docs)

# Generate with ORIGINAL query
result = generate_answer(original_query, relevant_docs)  # ✓ Correct
# NOT: generate_answer(current_query, relevant_docs)     # ✗ Wrong
```

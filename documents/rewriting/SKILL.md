---
name: rewriting
description: Enhances vague queries for better retrieval with context-aware improvements. Use during adaptive retry when no relevant documents found, when queries are unclear, or when the user mentions query enhancement or rewriting.
---

# Query Rewriting

## Instructions

Rewrite queries using `rewrite_query()` in `components/rewriter.py`. Typically triggered when `len(relevant_docs) == 0` during adaptive retry.

**Default usage:**

```python
# During retry after no relevant docs found
previous_context = f"Previous query '{current_query}' found {len(docs)} documents but none were relevant."

rewrite_result = rewrite_query(current_query, previous_context=previous_context)
current_query = rewrite_result['rewritten_query']
```

**Rewriting strategies:**
- Expand abbreviations: "fast computer" → "high performance laptop processor"
- Clarify vague terms: "won't work" → "troubleshooting device not powering on"
- Incorporate context: "What about warranty" + product context → "warranty coverage for [product]"
- Add synonyms: "cheap" → "affordable budget inexpensive"

**Returns:**
- `rewritten_query`: Enhanced query string
- `reasoning`: Explanation of changes

**Critical for adaptive retry:** Call only when `len(relevant_docs) == 0` and `num_retries < RETRY_LIMIT`. Pass context from previous failed attempt.

**Implementation:** `components/rewriter.py`, uses `REWRITE_MODEL` from `config.py` (default: Haiku 4.5), temperature 0.3.

## Examples

### Example 1: Basic rewriting (no context)

```python
# Input
result = rewrite_query("fast computer")

# Output
{
    "rewritten_query": "high performance laptop with fast processor and SSD storage",
    "reasoning": "Expanded 'fast' to specific performance characteristics"
}
```

### Example 2: Context-aware rewriting

```python
# Input
result = rewrite_query(
    "What about warranty",
    previous_context="User interested in ZenithBook 13 Evo laptop"
)

# Output
{
    "rewritten_query": "What is the warranty coverage and terms for ZenithBook 13 Evo laptop",
    "reasoning": "Incorporated product context and made question explicit"
}
```

### Example 3: Adaptive retry integration

```python
# After grading finds no relevant docs
if len(relevant_documents) == 0 and num_retries < RETRY_LIMIT:
    # Build context
    previous_context = f"Previous query '{current_query}' found {len(retrieved_documents)} documents but none were relevant."

    # Rewrite
    rewrite_result = rewrite_query(current_query, previous_context)
    current_query = rewrite_result['rewritten_query']

    print(f"Retry {num_retries + 1}: {current_query}")
    num_retries += 1
    # Loop back to retrieval
```

### Example 4: Vague troubleshooting

```python
# Input
result = rewrite_query("won't work")

# Output
{
    "rewritten_query": "troubleshooting device not functioning properly or not turning on",
    "reasoning": "Clarified vague complaint into specific troubleshooting query"
}
```

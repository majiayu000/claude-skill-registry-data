---
name: grading
description: Evaluates document relevance to queries using binary scoring (yes/no) with reasoning. Use when filtering retrieved documents, determining relevance for answer generation, or when the user mentions grading, filtering, or document quality.
---

# Document Grading

## Instructions

Grade documents for relevance using the functions in `components/grader.py`. The grading uses Claude API with structured outputs for consistent binary decisions.

**Default workflow:**

1. Retrieve documents from ChromaDB or web search
2. Call `grade_documents(query, documents)` to grade all documents
3. Call `filter_relevant_documents(graded_docs)` to get only relevant ones
4. Check if `len(relevant_docs) == 0` to trigger retry logic

**Key functions:**

```python
# Grade multiple documents (preferred)
graded_docs = grade_documents(query, documents)

# Filter to relevant only
relevant_docs = filter_relevant_documents(graded_docs)

# Grade single document (if needed)
result = grade_document(query, document)
```

**Grading returns:**
- `relevant`: Boolean (True/False)
- `reasoning`: Explanation of decision

**Critical for adaptive retry:** When ALL documents are graded as not relevant (`len(relevant_docs) == 0`), the pipeline triggers query rewriting and retry.

**Implementation:** `components/grader.py`, uses `GRADING_MODEL` from `config.py` (default: Haiku 4.5), temperature 0.

## Examples

### Example 1: Standard grading workflow

```python
from components.grader import grade_documents, filter_relevant_documents
from tools.chromadb_tool import query_chromadb

# Input
docs = query_chromadb("gaming laptops", top_k=5)
# Retrieved: 5 documents from catalog

# Grade
graded = grade_documents("gaming laptops", docs)
relevant = filter_relevant_documents(graded)

# Output
# Found 3 relevant documents out of 5 total
# Each has grading_result: {relevant: True, reasoning: "..."}
```

### Example 2: Triggering retry

```python
# Input: Vague query
docs = query_chromadb("fast computer", top_k=5)
graded = grade_documents("fast computer", docs)
relevant = filter_relevant_documents(graded)

# Output
# len(relevant) == 0
# → Triggers query rewrite and retry
```

### Example 3: In adaptive RAG pipeline

```python
# After retrieval
graded_documents = grade_documents(current_query, retrieved_documents)
relevant_documents = filter_relevant_documents(graded_documents)

if len(relevant_documents) == 0:
    # No relevant docs - rewrite query and retry
    if num_retries < RETRY_LIMIT:
        rewrite_result = rewrite_query(current_query, previous_context)
        current_query = rewrite_result['rewritten_query']
        num_retries += 1
        # Loop back to retrieval
else:
    # Found relevant docs - proceed to generation
    generate_answer(original_query, relevant_documents)
```

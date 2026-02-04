---
name: document-indexing
description: Extract structured metadata from documents using AI. Classify content types, extract topics and tools. Supports async batch processing.
---

# Document Indexing

## Overview

Extract structured metadata from fetched documents using LLM:
- **Content type**: blog, tutorial, guide, reference, etc.
- **Topics & Tools**: Main subjects and technologies
- **Structure**: Code examples, procedures, narrative

Creates `DocumentMetadata` records for search and clustering.

## Quick Start

```bash
# Index single document
kurt index 5494cc13

# Batch index (async, 5-10x faster)
kurt index --url-prefix https://example.com/

# Re-index with custom concurrency
kurt index --url-prefix https://example.com/ --force --max-concurrent 10
```

**Prerequisites:** Documents must be FETCHED (`kurct content fetch`)

## Commands

```bash
# Single
kurt index <doc-id>
kurt index <doc-id> --force

# Batch (async parallel)
kurt index --url-prefix <url>
kurt index --url-contains <string>
kurt index --max-concurrent 10     # Default: 5

# Filters
kurt index --status FETCHED --url-prefix <url>
```

## Content Types

`BLOG` | `TUTORIAL` | `GUIDE` | `REFERENCE` | `WHITEPAPER` | `CASE_STUDY` | `FAQ` | `CHANGELOG` | `MARKETING` | `OTHER`

## Extracted Metadata

```json
{
  "content_type": "TUTORIAL",
  "extracted_title": "Machine Learning Guide",
  "primary_topics": ["Machine Learning", "Python"],
  "tools_technologies": ["TensorFlow", "Pandas"],
  "has_code_examples": true,
  "has_step_by_step_procedures": true,
  "has_narrative_structure": false
}
```

## Performance

- **Sequential**: ~3-5s per document
- **Parallel (5 concurrent)**: ~1s per document avg
- **Example**: 92 docs in 30s (parallel) vs 5 mins (sequential)

## Python API

```python
from kurt.indexing import extract_document_metadata, batch_extract_document_metadata
import asyncio

# Single
result = extract_document_metadata("abc-123")

# Batch
results = asyncio.run(batch_extract_document_metadata(
    ["abc-123", "def-456"],
    max_concurrent=5
))
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Document not FETCHED" | Run `kurct content fetch <id>` first |
| "Content file not found" | Re-fetch document |
| Slow batch | Increase `--max-concurrent` |
| Rate limits | Reduce `--max-concurrent` |

## Next Steps

- **ingest-content-skill** - Fetch documents first
- **document-management-skill** - Query and manage documents

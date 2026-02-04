---
name: ccg-rag
description: "Use this skill for semantic code search and codebase understanding. CCG-RAG provides intelligent retrieval using code embeddings and knowledge graphs."
allowed-tools:
  - mcp__code-guardian__rag_*
  - mcp__code-guardian__documents_*
---

# CCG-RAG: Semantic Codebase Search

Intelligent code and documentation retrieval using embeddings and knowledge graphs.

## When to Use

Activate this skill when:
- Need to understand unfamiliar codebase
- Searching for code by functionality (not just text)
- Finding related code patterns
- Building context for complex tasks

## Core Capabilities

### 1. Code Search
```
rag_query           - Semantic search across codebase
rag_related_code    - Find similar code patterns
rag_build_index     - Index/reindex codebase
```

### 2. Document Search
```
documents_search    - Search documentation
documents_find_by_type - Find docs by type (api, guide, spec)
documents_list      - List all indexed documents
```

## Search Modes

### Semantic Search
Find code by describing what it does:
```
"authentication middleware"
"error handling functions"
"database connection setup"
```

### Pattern Search
Find similar implementations:
```
"find functions similar to validateUser"
"show me other API endpoints"
"related test patterns"
```

### Documentation Search
```
"API documentation for auth"
"setup guide for database"
"architecture decisions"
```

## How It Works

### Code Chunking
- Functions and classes extracted as units
- Tree-sitter parsing for accurate boundaries
- Preserves context (imports, comments)

### Embeddings
- Code-specific embeddings (UniXcoder/Qwen3)
- Natural language descriptions for each chunk
- Hybrid search: semantic + keyword

### Knowledge Graph
- Function call relationships
- Import/export dependencies
- Type hierarchies

## Example Usage

### Find Authentication Code
```
User: "Find all code related to user authentication"

rag_query({ query: "user authentication login session" })

Results:
1. src/auth/login.ts:authenticate() - Main login handler
2. src/middleware/auth.ts:verifyToken() - JWT verification
3. src/services/session.ts:createSession() - Session management
```

### Find Similar Patterns
```
User: "Show me code similar to the error handler in api.ts"

rag_related_code({ file: "src/api.ts", function: "handleError" })

Results:
1. src/services/db.ts:handleDbError() - 85% similar
2. src/utils/errors.ts:formatError() - 72% similar
```

### Search Documentation
```
User: "Find API documentation for payments"

documents_search({ query: "payment API integration" })

Results:
1. docs/api/payments.md - Payment API Reference
2. docs/guides/stripe-integration.md - Stripe Setup Guide
```

## Two-Stage Retrieval

For accurate results, CCG-RAG uses:

1. **Vector Search** - Fast semantic matching
2. **LLM Rerank** - Intelligent relevance scoring

```
Query → Embed → Top 20 candidates → LLM rerank → Top 5 results
```

## Index Management

### Build Index
```
rag_build_index({
  paths: ["src/", "lib/"],
  exclude: ["node_modules", "dist"],
  languages: ["typescript", "javascript"]
})
```

### Index Status
```
rag_status()

{
  "indexed_files": 245,
  "chunks": 1847,
  "last_updated": "2025-12-04T08:00:00Z",
  "embedding_model": "qwen3-embedding-8b"
}
```

## Best Practices

1. **Natural language queries** - Describe what you're looking for
2. **Combine with memory** - Store important findings
3. **Use for context** - Build understanding before changes
4. **Keep index fresh** - Rebuild after major changes

## Integration with Latent Mode

RAG enhances Latent Chain Mode:

```
🔍 [analysis]
1. rag_query({ query: "current auth implementation" })
2. Identify hot spots from RAG results
3. Build comprehensive codeMap

📋 [plan]
1. rag_related_code({ function: "targetFunction" })
2. Find similar patterns to follow
3. Plan patches based on existing conventions
```

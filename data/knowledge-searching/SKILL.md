---
name: knowledge-searching
description: Retrieves implementation knowledge, code examples, and documentation references. Use to inform technical decision-making when the user requires specific library usage, framework patterns, or syntax details. Trigger on requests to 'search docs', 'find code examples', or 'check implementation details'.
---

# Knowledge Searching

## Overview

Retrieves implementation knowledge to inform decision-making across the software development lifecycle. 

**Use this skill when you need:**
- Implementation details for specific libraries/frameworks
- Code examples for patterns or features
- Documentation references libraries/frameworks usage

**Announce at start:** "I'm using the knowledge-research skill to gather implementation details."

## Core Functions

### Searching Specific Documentation:
1. **Get sources** → `rag_get_available_sources()` - Returns list with id, title, url
2. **Find source ID** → Match to documentation (e.g., "Supabase docs" → "src_abc123")
3. **Search** → `rag_search_knowledge_base(query="vector functions", source_id="src_abc123")`

### General Research:
```bash
# Search knowledge base (2-5 keywords only!)
rag_search_knowledge_base(query="authentication JWT", match_count=5)

# Find code examples
rag_search_code_examples(query="React hooks", match_count=3)
```

## Query Guidelines

### ✅ Good Queries (2-5 keywords)
- `"authentication JWT"`
- `"vector functions"`
- `"React hooks"`
- `"Go context timeout"`
- `"SQL row level security"`

### ❌ Bad Queries (too long/verbose)
- ~~`"How do I implement JWT authentication in Go?"`~~
- ~~`"What are the best practices for vector similarity search?"`~~
- ~~`"Show me examples of React hooks for state management"`~~

**Rule:** Keep queries SHORT and keyword-focused for optimal search results.
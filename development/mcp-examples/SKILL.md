---
name: MCP Examples
description: This skill should be used when the user asks for "MCP examples", "real-world patterns", "code search patterns", "browser proxy patterns", "process management patterns", "show me examples", or wants to see actual implementations from lci, agnt, or other real MCPs.
version: 0.1.0
---

# MCP Examples

## Purpose

Provide real-world MCP patterns from production servers: code search (lci), browser integration (agnt), process management, and knowledge bases.

## When to Use

- Need concrete examples of patterns
- Want to see actual implementations
- Designing similar functionality
- Learning from working systems

## Code Search Pattern (lci)

### Architecture
- **Pattern:** Hub-and-Spoke + Progressive Discovery
- **Tools:** 8+ tools
- **Token System:** result_id, symbol_id

### Key Tools

**search - Hub tool**
```json
{
  "input": {"pattern": "string", "filter": "optional"},
  "output": {
    "results": [
      {"id": "r1", "name": "User.authenticate", "preview": "...", "conf": 0.95}
    ],
    "has_more": true,
    "total": 127
  }
}
```

**get_definition - Spoke tool**
```json
{
  "input": {"id": "r1"},
  "output": {
    "symbol_id": "s1",
    "name": "User.authenticate",
    "signature": "...",
    "source": "...",
    "location": {"file": "user.ts", "line": 42}
  }
}
```

**Token efficiency:** ID reference saves ~80% tokens vs. repeating full code

### Progressive Detail Example

```
Query: "authenticate"

High match (0.95): Full details (200 tokens)
  - Name, signature, docs, preview, location

Medium match (0.70): Summary (50 tokens)
  - Name, type, file

Low match (0.40): Minimal (10 tokens)
  - Name, ID only
```

## Browser Proxy Pattern (agnt)

### Architecture
- **Pattern:** CRUD + Aggregation
- **Tools:** 10+ tools
- **Token Systems:** proxy_id, session_id, request_id

### Key Tools

**proxy_start - Create**
```json
{
  "input": {"target_url": "http://localhost:3000"},
  "output": {
    "proxy_id": "dev",
    "listen_addr": "http://localhost:12345",
    "status": "running"
  }
}
```

**currentpage - Aggregation**
```json
{
  "input": {"proxy_id": "dev"},
  "output": {
    "session_id": "page-1",
    "url": "http://localhost:3000",
    "errors_count": 3,          // Not full error objects
    "interactions_count": 127,   // Not every interaction
    "mutations_count": 45,       // Not every mutation
    "performance": {...}
  },
  "detail_access": "Use detail=['errors'] for full data"
}
```

**Key pattern:** Counts in overview, full data on request

### Hierarchical IDs

```
proxy_id (dev)
  ↓
session_id (page-1)
  ↓
request_id (req_a1b2)
```

Each level provides more specificity.

## Process Management Pattern

### Architecture
- **Pattern:** CRUD + Lazy Loading
- **Tools:** 8+ tools
- **Token System:** process_id

### Progressive Status

**Level 1 - Count**
```json
{
  "active": 5,
  "stopped": 2
}
```

**Level 2 - List**
```json
{
  "processes": [
    {"id": "p1", "name": "dev-server", "status": "running"},
    {"id": "p2", "name": "test", "status": "running"}
  ]
}
```

**Level 3 - Status**
```json
{
  "id": "p1",
  "status": "running",
  "uptime": "2h15m",
  "memory": "245MB",
  "preview": "Server listening :3000"
}
```

**Level 4 - Full**
```json
{
  /* ...all Level 3... */,
  "full_output": "... complete logs ...",
  "env": {...},
  "metrics": {...}
}
```

## Knowledge Base Pattern

### Architecture
- **Pattern:** Discovery-Detail
- **Tools:** Search, topics, articles
- **Token System:** article_id, topic_id

### Layered Access

```
list_topics()
  → ["auth", "deploy", "monitor"]

get_topic_summary("auth")
  → {articles: 12, updated: "2024-01"}

search_articles("OAuth")
  → [{id: "a1", title: "...", preview: "..."}]

get_article("a1")
  → {title, content, related: [...]}
```

## Common Patterns Across Examples

### 1. ID Reference System

All use IDs to avoid repeating data:
- **lci:** result_id → symbol_id
- **agnt:** proxy_id → session_id → request_id
- **process:** process_id
- **kb:** topic_id → article_id

**Savings:** 70-90% token reduction

### 2. Progressive Detail

All vary detail by context:
- **lci:** By confidence (0.95 = full, 0.40 = minimal)
- **agnt:** By request (counts vs. full arrays)
- **process:** By depth (count → list → status → full)
- **kb:** By layer (topics → summary → full article)

### 3. Automation Flags

All include standard flags:
```json
{
  "has_more": boolean,
  "total": integer,
  "returned": integer,
  "complete": boolean
}
```

### 4. Accept Extra Parameters

All accept unknown params with warnings:
```typescript
const {known, params, ...extra} = input
if (extra) warnings.push(`Unknown: ${Object.keys(extra)}`)
```

## Anti-Patterns Seen and Fixed

### ❌ Repeating Data

**Before (wasteful):**
```json
// Tool 1
{"results": [{"name": "...", "code": "... 200 lines ..."}]}

// Tool 2 needs same data
// User copies entire result
```

**After (efficient):**
```json
// Tool 1
{"results": [{"id": "r1", "name": "...", "preview": "10 lines"}]}

// Tool 2
input: {"id": "r1"}  // Reference only
```

### ❌ No Progressive Detail

**Before:**
```json
{
  "results": [
    {"name": "...", "full": "... 500 tokens ..."},
    {"name": "...", "full": "... 500 tokens ..."},
    {"name": "...", "full": "... 500 tokens ..."}
  ]
}
```

**After:**
```json
{
  "results": [
    {"id": "a1", "conf": 0.95, "full": "..."},  // Only high confidence
    {"id": "b2", "conf": 0.70, "summary": "..."},
    {"id": "c3", "conf": 0.40}  // Just ID
  ]
}
```

### ❌ Flat Structure

**Before (15+ tools, no organization):**
```
search_users, search_posts, get_user, get_post, ...
```

**After (grouped):**
```
Query Tools: search
Lookup Tools: get_user, get_post
Management: create_user, update_user
```

## Real-World Token Savings

### lci code_search Tool

**Without IDs:**
- Average result: 250 tokens (full code)
- 10 results: 2,500 tokens

**With IDs:**
- Average preview: 50 tokens
- 10 results: 500 tokens
- **Savings:** 80%

### agnt currentpage Tool

**Without aggregation:**
- Full errors array: 400 tokens
- Full interactions: 600 tokens
- Full mutations: 300 tokens
- **Total:** 1,300 tokens

**With aggregation:**
- Error count: 10 tokens
- Interaction count: 10 tokens
- Mutation count: 10 tokens
- **Total:** 30 tokens (97% savings)
- Use detail parameter for full arrays when needed

## Additional Resources

### Examples Directory

- **`examples/lci-workflow.json`** - Complete lci search workflow
- **`examples/agnt-workflow.json`** - Browser debugging workflow
- **`examples/process-workflow.json`** - Process management workflow

## Quick Reference

**Proven patterns:**

1. **Hub-and-Spoke** - lci (search → details)
2. **CRUD** - agnt (lifecycle management)
3. **Aggregation** - agnt currentpage (counts not arrays)
4. **Lazy Loading** - process status (overview → full)
5. **Discovery-Detail** - kb (topics → articles)

**Key lessons:**

- IDs save 70-90% tokens
- Progressive detail by relevance/confidence
- Counts in overview, arrays on request
- Accept extra params with warnings
- Automation flags for AI agents

Study these real-world examples when designing similar functionality.

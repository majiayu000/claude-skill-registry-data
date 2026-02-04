---
name: Response Optimization
description: This skill should be used when the user asks about "JSON flags", "token IDs", "cross-tool references", "progressive detail", "response optimization", "human and LLM readable", "automation flags", "confidence-based detail", or discusses optimizing MCP responses for both human and machine consumption. Provides patterns for human/LLM readable responses with automation-friendly structures.
version: 0.1.0
---

# Response Optimization

## Purpose

Design MCP tool responses that work for both humans (readable) and AI agents (parseable), with JSON flags for automation, token/ID systems for cross-tool references, and progressive detail levels based on relevance or confidence.

## When to Use

Apply these patterns when:
- Responses need to be both human-readable and machine-parseable
- Tools generate data consumed by other tools
- Detail level should vary by relevance/confidence
- Automation needs status flags (`has_more`, `truncated`)
- Token efficiency is critical

## Core Concepts

### 1. Human/LLM Readable Format

Design responses that serve both audiences:

**Human needs:**
- Scannable structure
- Clear labels
- Sparse tables for overview
- Narrative descriptions

**LLM/AI needs:**
- Structured JSON
- Consistent schemas
- Automation flags
- Parseable data

**Example response:**

```json
{
  "results": [
    {"id": "r1", "name": "authenticate", "confidence": 0.95},
    {"id": "r2", "name": "authorize", "confidence": 0.75}
  ],
  "has_more": true,
  "total": 127,
  "truncated": false,
  "summary": "Found 127 matches, showing top 2. Use get_details(id) for more."
}
```

**Human reads:** "127 matches, top 2 shown, use get_details for more"
**AI parses:** `has_more: true, total: 127, result IDs for next tools`

### 2. JSON Automation Flags

Standard flags that enable AI agents to understand response state:

**Common flags:**

| Flag | Type | Purpose | Example |
|------|------|---------|---------|
| `has_more` | boolean | More results available | `true` |
| `total` | integer | Total matches found | `127` |
| `truncated` | boolean | Response was truncated | `false` |
| `confidence` | number | Result quality (0-1) | `0.95` |
| `complete` | boolean | Operation finished | `true` |
| `partial` | boolean | Partial results returned | `false` |
| `estimated` | boolean | Values are estimates | `false` |

**Example usage in responses:**

```json
{
  "results": [...],
  "metadata": {
    "has_more": true,
    "total": 1247,
    "returned": 10,
    "truncated": false,
    "complete": true,
    "query_time_ms": 4
  }
}
```

**AI agent logic:**
```typescript
// Pseudocode
if (response.metadata.has_more) {
  // Offer to fetch more results
} else if (response.metadata.truncated) {
  // Warn user about truncation
} else {
  // This is everything
}
```

### 3. Token/ID Systems for Cross-Tool References

Use IDs instead of repeating data between tools:

**Anti-pattern (wasteful):**
```json
// Tool 1: search
{
  "results": [
    {
      "name": "User.authenticate",
      "file": "/src/models/user.ts",
      "line": 42,
      "code": "async authenticate(password: string) {\n  // ... 50 lines ...\n}",
      "documentation": "... 200 words ..."
    }
  ]
}

// Tool 2: get_details
// User repeats entire context
```

**Good pattern (efficient):**
```json
// Tool 1: search
{
  "results": [
    {
      "id": "def_a1b2",
      "name": "User.authenticate",
      "preview": "async authenticate(password: string)",
      "confidence": 0.95
    }
  ]
}

// Tool 2: get_definition
// Input: {id: "def_a1b2"}
// Returns full details
```

**Token savings:** ~80% reduction (50 tokens vs 250 tokens)

**ID format patterns:**

```
Short hash:     a1b2, c3d4, e5f6
Prefixed:       def_a1b2, ref_c3d4, sym_e5f6
Sequential:     result_1, result_2, result_3
UUID subset:    a1b2c3d4
```

**Recommendation:** Short hash (4-8 chars) with optional prefix for clarity

### 4. Progressive Detail by Relevance

Vary detail level based on match strength, confidence, or relevance:

**Example: Search results with confidence-based detail**

```json
{
  "results": [
    {
      "id": "r1",
      "confidence": 0.95,
      "name": "User.authenticate",
      "type": "function",
      "file": "src/models/user.ts",
      "line": 42,
      "signature": "async authenticate(password: string): Promise<boolean>",
      "documentation": "Authenticates user with password",
      "preview": "Full code preview here..."
    },
    {
      "id": "r2",
      "confidence": 0.70,
      "name": "User.validate",
      "type": "function",
      "summary": "Basic validation method"
    },
    {
      "id": "r3",
      "confidence": 0.40,
      "name": "User.check"
    }
  ]
}
```

**Detail levels:**
- **High confidence (>0.8):** Full details (signature, docs, preview)
- **Medium confidence (0.5-0.8):** Summary only
- **Low confidence (<0.5):** Name + ID only (use get_details for more)

**Token distribution:**
- High: ~200 tokens each
- Medium: ~50 tokens each
- Low: ~10 tokens each

**Benefits:**
- Most relevant results get full attention
- Token budget focused on likely matches
- User can request details for any result

### 5. Sparse Tables + JSON Arrays

Provide both formats for different consumers:

**Sparse table (human-friendly):**
```
Results
=======

ID   | Name              | Type     | Confidence | File
---- | ----------------- | -------- | ---------- | ----
r1   | User.authenticate | function | 0.95       | user.ts
r2   | User.validate     | function | 0.70       | user.ts
r3   | User.check        | function | 0.40       | user.ts

Use get_definition(id) for full details
```

**JSON array (machine-friendly):**
```json
{
  "results": [
    {"id": "r1", "name": "User.authenticate", "type": "function", "confidence": 0.95, "file": "user.ts"},
    {"id": "r2", "name": "User.validate", "type": "function", "confidence": 0.70, "file": "user.ts"},
    {"id": "r3", "name": "User.check", "type": "function", "confidence": 0.40, "file": "user.ts"}
  ],
  "has_more": false,
  "total": 3
}
```

**When to use each:**
- Sparse table: Info tools, overview outputs, human-focused
- JSON array: All programmatic outputs, AI agent consumption

## Automation Flag Patterns

### Pattern 1: Pagination Flags

```json
{
  "results": [...],
  "pagination": {
    "has_more": true,
    "total": 1247,
    "returned": 10,
    "offset": 0,
    "limit": 10,
    "next_token": "eyJ..."  // Optional cursor
  }
}
```

### Pattern 2: Completion Flags

```json
{
  "status": "partial",
  "complete": false,
  "progress": 0.45,
  "estimated_completion": "2s",
  "results": [...],
  "continue_token": "abc123"
}
```

### Pattern 3: Quality Flags

```json
{
  "results": [...],
  "quality": {
    "confidence": 0.85,
    "estimated": false,
    "stale": false,
    "cached": true,
    "cache_age_seconds": 30
  }
}
```

### Pattern 4: Error/Warning Flags

```json
{
  "results": [...],
  "errors": [],
  "warnings": [
    "Unknown parameter 'foo' ignored",
    "Large result set, consider filtering"
  ],
  "partial_errors": false
}
```

## Token/ID Relationship Patterns

### Pattern 1: Single ID Type

```
search() → result_id[]
get_definition(result_id) → details
```

Simple, works for small MCPs (5-10 tools)

### Pattern 2: Typed IDs

```
search() → result_id[] (prefixed: res_*)
get_definition(result_id) → symbol_id (prefixed: sym_*)
find_references(symbol_id) → reference_id[] (prefixed: ref_*)
```

Clear type distinction, works for 10-20 tools

### Pattern 3: Hierarchical IDs

```
proxy_start() → proxy_id
currentpage(proxy_id) → session_id
proxylog(proxy_id, session_id) → request_id[]
```

Parent-child relationships, works for complex stateful MCPs

## Progressive Detail Examples

### Example 1: Code Search Results

**Query:** "authenticate"

**Response with progressive detail:**

```json
{
  "results": [
    {
      "id": "a1b2",
      "confidence": 0.98,
      "full_detail": {
        "name": "User.authenticate",
        "type": "async function",
        "file": "src/models/user.ts",
        "line": 42,
        "signature": "async authenticate(password: string): Promise<boolean>",
        "documentation": "Authenticates user credentials against database",
        "preview": "async authenticate(password: string) {\n  const hash = await bcrypt.hash(password, this.salt)\n  return hash === this.passwordHash\n}"
      }
    },
    {
      "id": "c3d4",
      "confidence": 0.72,
      "summary": {
        "name": "AuthService.authenticate",
        "type": "function",
        "file": "src/services/auth.ts"
      }
    },
    {
      "id": "e5f6",
      "confidence": 0.45,
      "minimal": {
        "name": "validateAuth"
      }
    }
  ],
  "has_more": true,
  "total": 47,
  "note": "High confidence results show full details. Use get_definition(id) for others."
}
```

### Example 2: Process Status

**Progressive detail by request:**

**Level 1 - Overview:**
```json
{
  "active_processes": 5,
  "use": "list_processes for details"
}
```

**Level 2 - List:**
```json
{
  "processes": [
    {"id": "p1", "name": "dev-server", "status": "running"},
    {"id": "p2", "name": "test-suite", "status": "running"}
  ]
}
```

**Level 3 - Detail:**
```json
{
  "process": {
    "id": "p1",
    "name": "dev-server",
    "status": "running",
    "uptime": "2h 15m",
    "memory": "245MB",
    "cpu": "15%",
    "output_preview": "Server listening on :3000"
  }
}
```

**Level 4 - Full:**
```json
{
  "process": {
    /* ... all Level 3 fields ... */,
    "full_output": "... complete logs ...",
    "env": {...},
    "metrics": {...}
  }
}
```

## Accept Extra Parameters (Critical Pattern)

**Always accept, warn, don't reject:**

```typescript
// Pseudocode
function search(params: any) {
  const {pattern, filter, max, ...extra} = params

  // Build response
  const results = performSearch(pattern, filter, max)

  // Warn about unknowns (don't fail)
  const warnings = []
  if (Object.keys(extra).length > 0) {
    warnings.push(`Unknown parameters ignored: ${Object.keys(extra).join(', ')}`)
  }

  return {
    results,
    warnings,
    has_more: results.length < total,
    total
  }
}
```

**Why critical:** AI agents hallucinate parameters. Be permissive unless severe issue (security, corruption).

## Additional Resources

### Reference Files

- **`references/automation-flags.md`** - Comprehensive flag catalog
- **`references/id-systems.md`** - ID generation and management patterns

### Examples

- **`examples/progressive-detail-search.json`** - Complete search response example
- **`examples/cross-tool-ids.json`** - ID reference flow across multiple tools

## Quick Reference

**Response optimization checklist:**

- [ ] Both human-readable and machine-parseable
- [ ] Automation flags included (`has_more`, `total`, etc.)
- [ ] ID system for cross-tool references
- [ ] Progressive detail by confidence/relevance
- [ ] Sparse tables for human, JSON arrays for machines
- [ ] Accept extra parameters with warnings
- [ ] Clear next steps for users
- [ ] Token-efficient design

**Key patterns:**

1. **Dual format:** Sparse tables + JSON arrays
2. **Automation flags:** Standard metadata for AI agents
3. **ID references:** Avoid repeating data between tools
4. **Progressive detail:** More detail for higher confidence
5. **Permissive inputs:** Accept and warn, don't reject

Focus on making responses useful for both humans reading them and AI agents processing them.

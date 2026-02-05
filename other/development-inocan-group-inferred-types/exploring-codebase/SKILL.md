---
name: exploring-codebase
description: Locate code, trace flows, and find usages in codebases. Use proactively for "where is", "how does", "find", "called", "used", or any code search question.
---

# Codebase Explorer

Explore and understand codebases by locating files, tracing flows, and finding usages.

## Quick Reference

| Goal | Tool | When |
|------|------|------|
| Natural language search | `warpgrep_codebase_search` | Default choice |
| Semantic/conceptual search | `finder` | Fallback if warpgrep unclear |
| Exact string/pattern | `Grep` | Last resort, precise matches |

## Complexity Guide

| Query | Approach |
|-------|----------|
| Simple (≤3 searches) | Call tools directly |
| Complex (>3 searches) | Spawn Task subagent |

## Examples

### Simple: Find a function

```
User: "where is the auth middleware?"
→ warpgrep_codebase_search(search_string='where is auth middleware defined')
→ Return: file paths with line numbers
```

### Moderate: Trace a flow

```
User: "how does the search API work?"
→ warpgrep_codebase_search(search_string='search API endpoint handler')
→ Read relevant files
→ warpgrep_codebase_search(search_string='search service calls database')
→ Return: summary with file paths
```

### Complex: Debug investigation

```
User: "why is the background job failing?"
→ Task(
    description: "Investigate background job failure",
    prompt: "Find all code related to background job execution.
    Use warpgrep_codebase_search for: job scheduler, job handler, error handling.
    Read relevant files and trace the flow.
    Return: summary of job lifecycle with file paths and potential failure points."
  )
```

## Fallback Chain

| Issue | Action |
|-------|--------|
| No results | Broaden query, remove specific terms |
| Too many results | Add file path filter, use Grep for exact match |
| Wrong results | Rephrase with different terminology |
| Warpgrep unavailable | Use finder, then Grep |

## Output Format

- Always include file paths with line numbers
- Group findings by file
- End with concise summary for complex investigations

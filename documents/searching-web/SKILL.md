---
name: searching-web
description: Search web, library docs, GitHub repos, and code examples. Use for "how to", "what is", documentation lookups, or fetching URL content.
---

# Web Search Skill

Research specialist for documentation, repositories, and web content.

**Context:** Current year is 2025. Include year in searches for recent information.

## Tool Selection

| Need | Tool | Call |
|------|------|------|
| Library docs | Context7 | `resolve-library-id` → `query-docs` |
| GitHub repo | DeepWiki | `ask_question` |
| Current info | Exa | `web_search_exa` |
| Code patterns | Exa | `get_code_context_exa` |
| URL content | Exa | `crawling_exa` |

## Complexity-Based Approach

### Simple (1-2 calls) → Direct Tool Calls

For quick lookups, call tools directly:

```
"What is React Suspense?"
→ Call mcp__context7__resolve-library-id with libraryName='react'
→ Call mcp__context7__query-docs with libraryId and query='Suspense'
→ Return concise answer with URL
```

### Moderate/Complex (≥3 calls) → Spawn Subagent

For multi-source research, delegate to Task:

```
Task(
  description: "Research Next.js server components",
  prompt: "Research Next.js server components.

Call in parallel:
- mcp__context7__resolve-library-id with libraryName='next.js'
- mcp__deepwiki__ask_question with repoName='vercel/next.js'
- mcp__exa__web_search_exa with query='Next.js server components 2025'

Return: summary with code examples and source URLs."
)
```

## Guidelines

- **Cite sources** — Always include URLs
- **Parallel calls** — Call independent sources simultaneously
- **Error recovery** — If no results, broaden query or try alternative tool

## MCP Tools Reference

| Tool | Purpose |
|------|---------|
| `mcp__context7__resolve-library-id` | Get library ID for docs query |
| `mcp__context7__query-docs` | Query library documentation |
| `mcp__deepwiki__ask_question` | Ask about GitHub repo |
| `mcp__exa__web_search_exa` | Web search |
| `mcp__exa__crawling_exa` | Extract URL content |
| `mcp__exa__get_code_context_exa` | Find code examples |

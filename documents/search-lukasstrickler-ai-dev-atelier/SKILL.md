---
name: search
description: "Search the web, library documentation, and GitHub repositories using Tavily, Context7, and GitHub Grep MCPs. Use when: (1) Looking up documentation for libraries or frameworks, (2) Searching for code examples or tutorials, (3) Finding API references or specifications, (4) Researching best practices or solutions, (5) Looking up error messages or troubleshooting guides, (6) Finding library installation instructions, (7) Searching for real-world code patterns in GitHub repositories, or (8) When you need current web information or documentation. Triggers: search, look up, find documentation, search web, lookup, find examples, search for, how to, tutorial, API reference, documentation for, error message, troubleshoot, best practices, find code examples, GitHub search."
---

# Search

Search web, library docs, and GitHub code using progressive escalation.

## Quick Start

**Decision Tree:**
- **Library/framework docs?** → Context7 `get-library-docs`
- **Code examples/patterns?** → GitHub Grep `grep_searchGitHub`
- **Web info/tutorials?** → Tavily `tavily_search`
- **Multiple sources needed?** → Run tools in parallel

**Default Workflow:**
1. Start simple: `search_depth: "basic"`, `maxResults: 5`
2. If insufficient: Escalate to Level 2 (expand query, increase results)
3. If repeated problem: Escalate to Level 3 (parallel queries, extraction, crawling)

## Tools Overview

### Tavily (Web Search)
| Tool | Purpose | Key Params |
|------|---------|------------|
| `tavily_search` | Web search | `search_depth`, `topic`, `time_range`, `include_domains` |
| `tavily_extract` | Extract from URLs | `extract_depth`, `query` (for reranking) |
| `tavily_crawl` | Multi-page crawl | `max_depth`, `select_paths`, `instructions` |
| `tavily_map` | Discover site structure | `max_depth`, `limit` |

### Context7 (Library Docs)
| Tool | Purpose | Key Params |
|------|---------|------------|
| `resolve-library-id` | Get library ID | `libraryName` |
| `get-library-docs` | Fetch docs | `mode: "code"/"info"`, `topic`, `page` |

### GitHub Grep (Code Search)
| Tool | Purpose | Key Params |
|------|---------|------------|
| `grep_searchGitHub` | Search code patterns | `query`, `language`, `repo`, `path`, `useRegexp` |

**Critical:** GitHub Grep searches **literal code patterns**, not keywords!
- ✅ Good: `useState(`, `getServerSession`, `(?s)try {.*await`
- ❌ Bad: `react tutorial`, `how to authenticate`

## Progressive Escalation Levels

### Level 1: Simple Search (Default)
**When:** Quick lookups, straightforward questions, first encounter

1. Tavily: `search_depth: "basic"`, `maxResults: 5`
2. Context7: `mode: "code"` for API, `mode: "info"` for concepts
3. GitHub Grep: literal code patterns with language filter
4. **Parallel execution** when appropriate

**Sufficient? → Done. Insufficient? → Level 2**

### Level 2: Enhanced Search
**When:** Initial results incomplete, need more examples, outdated results

1. **Expand query:** Add synonyms, context (keep <400 chars)
2. **Increase:** `maxResults: 10-15`, `search_depth: "advanced"`
3. **Filter domains:** `include_domains: ["stackoverflow.com", "github.com"]`
4. **Time filter:** `time_range: "year"` for recent info
5. **Two-step extraction:** Search → Filter by score (>0.5) → Extract top URLs

**Sufficient? → Done. Insufficient? → Level 3**

### Level 3: Deep Research
**When:** Problem encountered 2+ times, complex topic, building knowledge base

1. **Parallel queries:** 3-5 query variations with synonyms
2. **Systematic extraction:** Top 5-10 URLs with `extract_depth: "advanced"`
3. **Website exploration:** `tavily_map` → `tavily_crawl`
4. **GitHub deep dive:** Multiple pattern variations, regex, cross-repo comparison
5. **Cross-reference:** Verify across multiple sources

## Key Tips (Reminders)

### Query Formulation
- **400 char limit** - Break complex queries into sub-queries
- **Natural language works better** - Full sentences > keywords
- **Be specific** - Include technology, use case, context
- For full guide: See `references/query-guide.md`

### Score-Based Filtering
- Tavily results include `score` (0-1)
- **>0.5 typically good** - Adjust based on distribution
- Filter before extracting to save credits

### Two-Step Extraction Pattern
```
1. Search with search_depth: "advanced"
2. Filter URLs by score (>0.5)
3. Extract top 2-5 URLs with extract_depth: "basic"
4. Upgrade to "advanced" only if needed
```

### GitHub Grep Patterns
```
# API usage
Query: getServerSession
Language: ['TypeScript'], Path: '/api/'

# Multiline with regex
Query: (?s)useEffect\(\(\) => {.*cleanup
useRegexp: true
```

### Cost Optimization
- `basic` = 1 credit, `advanced` = 2 credits
- Prefer two-step extraction over `include_raw_content: true`
- Use `tavily_map` before `tavily_crawl`

For advanced techniques: See `references/advanced-techniques.md`

## Common Patterns

| Pattern | Level 1 | Level 2 | Level 3 |
|---------|---------|---------|---------|
| **Error resolution** | Exact error + SO domain | Remove quotes, add context | Extract top answers, cross-ref docs |
| **Best practices** | "Tech best practices 2024" | Domain filter + extract | Parallel aspect searches |
| **API reference** | Context7 with topic | + Tavily + GitHub Grep | Crawl official docs |
| **Code patterns** | GitHub Grep literal | + language/path filters | Regex + cross-repo |

For workflow examples: See `references/examples/example-workflows.md`

## References

- **`references/reference-parameters.md`** - Complete parameter reference for all tools
- **`references/query-guide.md`** - Query structuring, 400 char limit, expansion strategies
- **`references/advanced-techniques.md`** - Two-step extraction, post-processing, cost optimization
- **`references/examples/example-workflows.md`** - Practical workflow examples

## Output

Search results are used directly in context. No files saved unless requested. For comprehensive research with evidence cards, use the `research` skill.

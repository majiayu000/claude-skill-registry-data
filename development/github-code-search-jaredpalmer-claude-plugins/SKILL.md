---
name: github-code-search
description: Search GitHub code across millions of repositories using grep.app. Use when you need to find code patterns, implementations, examples, or understand how features are built in public codebases. (project)
---

# GitHub Code Search via grep.app

## Overview

This skill enables searching across millions of public GitHub repositories using the grep.app service. It uses a **code mode** pattern where you write and execute TypeScript code to query the grep.app MCP server, filter results locally, and return only relevant findings.

## When to Use

- Find implementations of specific patterns (e.g., "how do other projects implement OAuth2?")
- Search for usage examples of APIs or libraries
- Analyze architectural patterns across codebases
- Find code snippets matching regex patterns
- Research best practices by examining popular repositories

## Setup Requirements

The grep.app MCP server must be configured. Add it with:

```bash
claude mcp add --transport http grep https://mcp.grep.app
```

Verify with `/mcp` - you should see `grep` listed.

## Code Mode Pattern

Instead of calling MCP tools directly (which loads all tool definitions into context), this skill uses **code execution** for efficiency:

1. Write TypeScript code that calls the grep MCP server
2. Execute the code via Bash with `bun` or `npx tsx`
3. Filter and process results in the execution environment
4. Return only relevant findings to minimize token usage

This approach reduces token usage by 90%+ compared to direct tool calls with large result sets.

## Implementation

### Option 1: Use the bundled search script (recommended)

A ready-to-use TypeScript search script is included:

```bash
bun run skills/github-code-search/scripts/search.ts "query" [--lang=Language] [--repo=owner/repo] [--limit=N] [--regexp]
```

**Examples:**

```bash
# Search for "use cache" in TypeScript files
bun run skills/github-code-search/scripts/search.ts "use cache" --lang=TypeScript --limit=5

# Search in a specific repository
bun run skills/github-code-search/scripts/search.ts "cacheLife" --repo=vercel/next.js --limit=10

# Use regex patterns
bun run skills/github-code-search/scripts/search.ts "async.*await" --regexp --lang=TypeScript
```

**Output format** (JSON):

```json
{
  "query": "cacheLife",
  "options": { "language": "TypeScript", "limit": 3 },
  "total": 2931,
  "results": [
    {
      "repo": "vercel/next.js",
      "path": "packages/next/src/server/use-cache/cache-life.ts",
      "url": "https://github.com/vercel/next.js/blob/canary/packages/next/src/server/use-cache/cache-life.ts",
      "matches": [{ "lineNumber": 5, "content": "export type »CacheLife« = {" }]
    }
  ]
}
```

The `»` and `«` markers indicate where the search term was matched.

### Option 2: Inline TypeScript (for custom processing)

For more complex searches with custom filtering, write inline TypeScript:

```typescript
// Execute with: bun -e "..."
const response = await fetch(
  'https://grep.app/api/search?q=useOptimistic&l=TypeScript'
)
const data = await response.json()

// Process results locally - this is the efficiency gain!
const filtered = data.hits.hits
  .filter((hit: any) => hit.repo.includes('react'))
  .slice(0, 5)
  .map((hit: any) => ({ repo: hit.repo, path: hit.path }))

console.log(JSON.stringify(filtered, null, 2))
```

## Quick Search (Direct API)

For simple searches, use curl directly:

```bash
curl -s "https://grep.app/api/search?q=useOptimistic+hook&l=TypeScript" | jq '.hits.hits[:5] | .[] | {repo: .repo.raw, path: .path.raw}'
```

## Parameters

| Parameter | Description                                                | Example                            |
| --------- | ---------------------------------------------------------- | ---------------------------------- |
| `q`       | Search query (required). Supports regex with `regexp:true` | `"use cache"`, `async.*await`      |
| `l`       | Language filter                                            | `TypeScript`, `Python`, `Go`       |
| `r`       | Repository filter                                          | `vercel/next.js`, `facebook/react` |
| `regexp`  | Enable regex mode                                          | `true`                             |

## Example Queries

### Find "use cache" implementations in Next.js projects

```bash
curl -s "https://grep.app/api/search?q=%22use%20cache%22&l=TypeScript" | jq '.hits.hits[:10] | .[] | {repo: .repo.raw, path: .path.raw}'
```

### Search for error handling patterns

```bash
curl -s "https://grep.app/api/search?q=catch.*error.*log&regexp=true&l=TypeScript" | jq '.hits.total'
```

### Find implementations in a specific repo

```bash
curl -s "https://grep.app/api/search?q=cacheLife&r=vercel/next.js" | jq '.hits.hits[] | {path: .path.raw, lines: .content.lines}'
```

## Best Practices

1. **Start broad, then narrow**: Begin with a general query, then add language/repo filters
2. **Use regex for patterns**: Enable `regexp=true` for complex pattern matching
3. **Limit results locally**: Process and filter in code before returning to save tokens
4. **Cache common searches**: Store results for frequently-used queries
5. **Respect rate limits**: The grep.app API has rate limits; batch queries when possible

## Integration with MCP Tools

If the grep MCP server is configured, you can also use it via MCP tools:

```typescript
// Via MCP (if mcp__grep__search is available)
mcp__grep__search({
  query: 'authentication middleware',
  language: 'TypeScript',
  useRegexp: false,
})
```

However, the code mode approach (curl + jq or TypeScript script) is preferred for:

- Large result sets that need filtering
- Complex post-processing logic
- Chaining multiple searches
- Minimizing context window usage

## Troubleshooting

- **No results**: Try broadening the query or removing filters
- **Rate limited**: Wait a few seconds and retry, or use the MCP server which may have higher limits
- **Timeout**: Large queries may timeout; add more specific filters

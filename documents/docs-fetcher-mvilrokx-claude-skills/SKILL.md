---
name: docs-fetcher
description: Fetch up-to-date library documentation directly into context to prevent hallucinated APIs and outdated code examples. Use when user says "use docs", "fetch docs for [library]", "check [library] docs", or asks about a library's API, methods, or usage patterns and current documentation would be helpful. Also use proactively when generating code for libraries where version-specific accuracy matters.
---

# Docs Fetcher

Fetch current documentation for libraries to ensure accurate, up-to-date code generation.

## Workflow

### Trigger Detection

Activate this skill when:

- User explicitly requests: "use docs", "fetch docs for X", "check X documentation"
- User asks about specific API methods, parameters, or patterns for a supported library
- Generating code where version-specific accuracy is critical

### Execution Steps

1. **Identify the library** from user request or code context
2. **Look up documentation URLs** in [references/libraries.md](references/libraries.md)
3. **Fetch relevant pages** using `fetch_webpage` tool with appropriate URLs
4. **Use fetched content** to inform code generation or answer

### Fetching Strategy

For comprehensive coverage, fetch multiple pages:

```
fetch_webpage(urls: [
  "https://fastapi.tiangolo.com/tutorial/dependencies/",
  "https://fastapi.tiangolo.com/advanced/advanced-dependencies/"
])
```

For quick lookups, fetch the most relevant single page.

## Adding Libraries

To add a new library, edit [references/libraries.md](references/libraries.md):

1. Find the official documentation URL
2. Identify key pages: quickstart, API reference, common patterns
3. Add entry following the existing format

## Limitations

- Fetches only explicitly listed URLs (no recursive crawling)
- Some documentation sites may block or limit fetches
- Very large pages may be truncated
- No version pinning — fetches current docs

## When NOT to Use

- General programming questions not library-specific
- Libraries not in the mapping (inform user, suggest they provide URLs)
- Simple questions where training knowledge is sufficient

---
name: context7-mcp
description: Always use Context7 MCP to fetch up-to-date library/API documentation before generating code that depends on external libraries or config. Use when the user asks for setup steps, configuration, or code involving third-party libraries. Prefer Context7 docs over memory. Include citations to the retrieved docs when possible.
---

# Context7 MCP (Up-to-date docs)

## Default behavior

Whenever the task involves any external library/framework:
- Next.js, React, Vite
- Supabase SDK
- PyMuPDF, pdfplumber
- Tailwind, shadcn/ui
- FastAPI, Pydantic
- Anthropic SDK
- Any npm/pip package

**Do this:**
1. Resolve the correct library ID in Context7
2. Pull the relevant docs snippet(s)
3. Only then generate code/config
4. If docs conflict with assumptions, prefer docs

## Setup (if not installed)

### Remote server (recommended)
```bash
claude mcp add --transport http context7 https://mcp.context7.com/mcp --header "CONTEXT7_API_KEY: YOUR_API_KEY"
```

### Local server (npx)
```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY
```

API key is optional for basic usage, but helps with rate limits/private repos.

## Available tools

### resolve-library-id
Find the correct library identifier:
```
Input: "react" or "fastapi"
Output: library ID to use with get-library-docs
```

### get-library-docs
Fetch documentation for a library:
```
Input: library ID + optional topic filter
Output: relevant documentation snippets
```

## Usage patterns

### Before writing code
```
1. User asks: "Add Supabase auth to the app"
2. Claude: resolve-library-id("supabase")
3. Claude: get-library-docs(id, topic="authentication")
4. Claude: Generate code based on current docs
```

### When docs conflict with memory
- Always prefer Context7 docs (more recent)
- Mention the source version when relevant
- If uncertain, cite the doc snippet

## Recommended rule (add to CLAUDE.md)

> "Always use Context7 when I need code generation, setup or configuration steps, or library/API documentation."

## Output requirements

When Context7 is used:
- State what library/topic was looked up
- Cite version if available
- Use precise, version-aware steps from docs

## Common libraries for DeepRead

| Library | Use case |
|---------|----------|
| `anthropic` | Claude API integration |
| `fastapi` | Backend API routes |
| `pydantic` | Data validation |
| `pymupdf` | PDF parsing |
| `react` | Frontend components |
| `vite` | Build tool |
| `tailwindcss` | Styling |
| `supabase-js` | Database client |

---
name: context7
description: "Look up current, version-specific library documentation using Context7. Use proactively when working with libraries or explicitly via /context7."
user-invocable: true
arguments: "Optional library name and query (e.g., 'next.js app router', 'react useEffect cleanup')"
argument-hint: "[library] [query]"
---

# /context7

Fetch up-to-date library documentation using the Context7 MCP server. This avoids generating code with deprecated APIs or hallucinated methods.

## Instructions

### Explicit invocation (`/context7 <args>`)

If `$ARGUMENTS` is provided, parse it as a library name and optional query:
1. Call `mcp__context7__resolve-library-id` with the library name to get the Context7 library ID
2. Call `mcp__context7__query-docs` with the resolved ID and query to fetch current documentation
3. Summarize the relevant docs and apply them to the current task

Examples:
- `/context7 next.js app router` — look up Next.js App Router docs
- `/context7 react` — browse React documentation
- `/context7 prisma migrations` — look up Prisma migration docs

### Proactive use (no explicit invocation)

Use Context7 automatically during normal coding when:
- **Implementing with a framework you're unsure about** — check current API before generating code
- **Version-specific behavior matters** — the project pins a specific major version and you need to match its API
- **Recently evolved libraries** — Next.js, React (server components), SvelteKit, tRPC, Prisma, Drizzle, TanStack, and similar fast-moving projects
- **New dependencies** — the project has a dependency you haven't seen in this session; look up its API before using it
- **User asks to "use context7"** — always honor explicit requests

Skip Context7 when:
- Working with stable, well-known APIs (Node.js built-ins, basic Express patterns, standard SQL)
- The user has already provided documentation or examples in the conversation
- Making trivial changes that don't involve library API calls

### MCP Tools Reference

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `mcp__context7__resolve-library-id` | Find a library's Context7 ID | `libraryName` (required) |
| `mcp__context7__query-docs` | Fetch docs for a library | `libraryId` (required, e.g., `/vercel/next.js`), `query` (required) |

### Workflow

1. **Resolve** — call `resolve-library-id` with the library name to get its ID (format: `/org/project`)
2. **Query** — call `query-docs` with the ID and a specific question
3. **Apply** — use the returned documentation to write accurate, current code

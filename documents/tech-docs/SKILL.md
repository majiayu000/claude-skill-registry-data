---
name: tech-docs
description: Access local technical documentation before searching the internet. Use FIRST when researching any tech stack question.
allowed-tools: Read, Glob, Grep, Bash
---

# Technical Documentation Skill

**ALWAYS search `.docs/` FIRST** before searching the internet!

## Documentation Directory

```
.docs/
├── README.md           # Overview
├── nextjs.md           # Next.js 16 App Router
├── tanstack-query.md   # TanStack Query / React Query
├── better-auth.md      # Better Auth
├── gorm.md             # GORM ORM
├── gorilla-mux.md      # Gorilla Mux Router
├── goca.md             # Goca CLI
├── orval.md            # Orval API Client Generator
├── shadcn.md           # shadcn/ui Components
├── tailwind.md         # Tailwind CSS 4
├── kamal-deploy.md     # Kamal Deployment
└── logging.md          # Logging (zerolog + Pino)
```

## Search Documentation (RECOMMENDED)

Use the semantic search tool to find relevant documentation:

```bash
# Search for specific topics
make search-docs q="prefetchQuery" n=5
make search-docs q="HydrationBoundary" n=3
make search-docs q="authentication session" n=5

# Output is LLM-optimized with relevance scores
```

**When to use search-docs:**
- Looking for specific patterns or APIs
- Finding code examples for a concept
- Researching how to implement something
- The docs are large and you need targeted results

## Workflow

1. **Question about a technology?**
   → First: `make search-docs q="your question"` to find relevant sections
   → Or: Read `.docs/<tech>.md` directly if you know the file

2. **Docs not available?**
   → Then search the internet
   → Save results in `.docs/` for later

3. **Docs outdated?**
   → Update with latest info

## Example Usage

```
User: "How does HydrationBoundary work in TanStack Query?"

1. Run: make search-docs q="HydrationBoundary" n=5
2. Review the top results with relevance scores
3. If needed, read full file: .docs/tanstack-query.md
4. If not found/incomplete:
   - WebFetch from TanStack Query docs
   - Save relevant info to .docs/tanstack-query.md
5. Answer the question
```

## Tool Calling Pattern

When the user asks about tech stack topics, use this pattern:

```bash
# Step 1: Search for relevant docs
make search-docs q="<user question keywords>" n=5

# Step 2: If results found, read the specific section
# The search output shows file and section info

# Step 3: If no results, fetch new docs
make fetch-docs url=<documentation-url> name=<tech-name>
```

## Fetching New Documentation

```bash
# Fetch docs from any URL
make fetch-docs url=https://tanstack.com/query/latest/docs

# With custom name
make fetch-docs url=https://nextjs.org/docs name=nextjs
```

## Priority

1. `make search-docs` (semantic search, fast, targeted)
2. `.docs/` files (local, fast, project-specific)
3. `.claude/skills/` (project-specific patterns)
4. Internet (only if local not available)

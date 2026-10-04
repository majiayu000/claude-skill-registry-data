---
name: find-library-docs
description: >-
  Find current documentation, API references, and code examples for libraries, frameworks, SDKs, CLI tools, and cloud
  services. Use when answering or implementing work that depends on technology-specific APIs, configuration, setup,
  migrations, or debugging behavior. Match documentation to the relevant version.
---

# Library Documentation Lookup

Retrieve current documentation and code examples using the Context7 CLI. Verify API details against documentation for
the relevant version. Use the library's official documentation or source repository when Context7 is unavailable or
incomplete, following the error handling guidance below.

Prefer running without global installation:

```bash
npx ctx7@latest <command>
```

Do not install or upgrade the CLI globally unless the user explicitly asks.

## Workflow

Two-step process: resolve the library name to an ID, then query docs with that ID.

```bash
# Step 1: Resolve library ID
ctx7 library <name> <query>

# Step 2: Query documentation
ctx7 docs <libraryId> <query>
```

You MUST call `ctx7 library` first to obtain a valid library ID UNLESS the user explicitly provides a library ID in the
format `/org/project` or `/org/project/version`.

IMPORTANT: Do not run these commands more than 3 times per question. If you cannot find what you need after 3 attempts,
use the best result you have.

Run Context7 CLI requests outside Codex's default sandbox. If a Context7 CLI command fails with DNS or network errors
such as ENOTFOUND, host resolution failures, or fetch failed, rerun it outside the sandbox instead of retrying inside
the sandbox.

## Step 1: Resolve a Library

Resolves a package/product name to a Context7-compatible library ID and returns matching libraries.

```bash
ctx7 library react "How to clean up useEffect with async operations"
ctx7 library nextjs "How to set up app router with middleware"
ctx7 library prisma "How to define one-to-many relations with cascade delete"
```

Always pass a `query` argument — it is required and directly affects result ranking. Use the user's intent to form the
query, which helps disambiguate when multiple libraries share a similar name. Do not include any sensitive or
confidential information such as API keys, passwords, credentials, personal data, or proprietary code in your query.

### Result fields

Each result includes:

- **Library ID** — Context7-compatible identifier (format: `/org/project`)
- **Name** — Library or package name
- **Description** — Short summary
- **Code Snippets** — Number of available code examples
- **Source Reputation** — Authority indicator (High, Medium, Low, or Unknown)
- **Benchmark Score** — Quality indicator (100 is the highest score)
- **Versions** — List of versions if available. Use one of those versions if the user provides a version in their query.
  The format is `/org/project/version`.

### Selection process

1. Analyze the query to understand what library/package the user is looking for
2. Select the most relevant match based on:
   - Name similarity to the query (exact matches prioritized)
   - Description relevance to the query's intent
   - Documentation coverage (prioritize libraries with higher Code Snippet counts)
   - Source reputation (consider libraries with High or Medium reputation more authoritative)
   - Benchmark score (higher is better, 100 is the maximum)
3. If multiple good matches exist, acknowledge this but proceed with the most relevant one
4. If no good matches exist, clearly state this and suggest query refinements
5. For ambiguous queries, request clarification before proceeding with a best-guess match

### Version-specific IDs

If the user mentions a specific version, use a version-specific library ID:

```bash
# General (latest indexed)
ctx7 docs /vercel/next.js "How to set up app router"

# Version-specific
ctx7 docs /vercel/next.js/v14.3.0-canary.87 "How to set up app router"
```

The available versions are listed in the `ctx7 library` output. Use the closest match to what the user specified.

## Step 2: Query Documentation

Retrieves up-to-date documentation and code examples for the resolved library.

```bash
ctx7 docs /facebook/react "How to clean up useEffect with async operations"
ctx7 docs /vercel/next.js "How to add authentication middleware to app router"
ctx7 docs /prisma/prisma "How to define one-to-many relations with cascade delete"
```

### Writing good queries

The query directly affects the quality of results. Be specific and include relevant details. Do not include any
sensitive or confidential information such as API keys, passwords, credentials, personal data, or proprietary code in
your query.

| Quality | Example                                                    |
| ------- | ---------------------------------------------------------- |
| Good    | `"How to set up authentication with JWT in Express.js"`    |
| Good    | `"React useEffect cleanup function with async operations"` |
| Bad     | `"auth"`                                                   |
| Bad     | `"hooks"`                                                  |

Use the user's full question as the query when possible, vague one-word queries return generic results.

The output contains two types of content: **code snippets** (titled, with language-tagged blocks) and **info snippets**
(prose explanations with breadcrumb context).

## Authentication

Works without authentication. For higher rate limits:

```bash
# Option A: environment variable
export CONTEXT7_API_KEY=your_key

# Option B: OAuth login
ctx7 login
```

## Error Handling

If Context7 fails because of quota, network, missing coverage, or unusable results:

1. Briefly state why Context7 could not answer the question. For quota failures, suggest `ctx7 login` when useful.
2. Search the library vendor's official documentation, release notes, API reference, or source repository. Prefer
   version-matched primary sources and cite the pages used.
3. If no authoritative source is available, say so and clearly label any inference or memory-derived guidance as
   potentially outdated.

Do not silently fall back to remembered API details.

## Common Mistakes

- Library IDs require a `/` prefix — `/facebook/react` not `facebook/react`
- Always run `ctx7 library` first — `ctx7 docs react "hooks"` will fail without a valid ID
- Use descriptive queries, not single words — `"React useEffect cleanup function"` not `"hooks"`
- Do not include sensitive information (API keys, passwords, credentials) in queries

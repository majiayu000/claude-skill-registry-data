---
name: using-context7
description: Use when working with any library/framework/SDK to fetch current docs. Beats training-data memory which is stale.
---

# Using Context7

## What this is

Context7 is an MCP server that fetches **current** documentation for libraries, frameworks, and SDKs on demand. Your training data is months-to-years stale; Context7 is the corrective.

## When to use

Use whenever the user asks about:

- A library's API, configuration, or setup (`React`, `Next.js`, `Django`, `Prisma`, `Tailwind`, `Express`, `Spring`, `FastAPI`, `LangChain`, ...)
- Version-specific behavior or migration (`Next.js 14 → 15`, `React 18 → 19`)
- "How do I do X with Y" where Y is any named library/framework
- Best practices or recommended patterns for a specific tool
- Configuration files (`tailwind.config.js`, `next.config.ts`, `prisma.schema`)

**Even if you "feel like you know" the answer** — query Context7 first. Library APIs churn fast: server actions, app router, RSC, Tailwind v4, Prisma 6 migrations all shipped after most training cutoffs. Confidence-from-memory is the failure mode.

## When NOT to use

- Refactoring existing code (the code itself is the spec)
- Writing PowerShell/Bash scripts (general shell knowledge)
- Debugging business logic (no library API involved)
- Code review for style/correctness
- Generic programming concepts (sorting algorithms, OOP patterns, recursion)
- Internal company code (Context7 only knows public libraries)

## Workflow

Two-call pattern, always in this order:

### Step 1: Resolve library ID

```
mcp__context7__resolve-library-id
  libraryName: "Next.js"           # official name with punctuation
  query: "How to set up server actions in Next.js 15"
```

Returns one or more matches in the form `/org/project` or `/org/project/version`. Pick the highest-reputation, highest-snippet-count match. If the user named a version (`React 19`, `Next.js 14.3`), prefer the versioned ID like `/vercel/next.js/v14.3.0-canary.87`.

**Skip step 1 only when the user already gave you the ID** in `/org/project` form (rare).

### Step 2: Query docs

```
mcp__context7__query-docs
  libraryId: "/vercel/next.js"
  query: "How to set up server actions with form validation in Next.js 15"
```

The query goes to the Context7 API. Be specific.

## Query writing — good vs bad

**Good queries** (specific intent, named feature, target version):
- "How to set up JWT authentication middleware in Express.js"
- "Prisma schema for a one-to-many relation with cascade delete"
- "React 19 useFormStatus hook example with form submission"
- "Tailwind v4 custom theme tokens with CSS variables"
- "FastAPI dependency injection for database session lifecycle"

**Bad queries** (vague, single-word, intent unclear):
- "auth"
- "hooks"
- "react"
- "config"
- "best practices"

If your query is one word or one short noun phrase, rewrite it before sending.

## Constraints

- Maximum **3 calls per question** to Context7. If you can't find what you need after 3 calls, work with what you have.
- Don't pass secrets, API keys, customer data, or proprietary code in the `query` field — it leaves your machine.
- The `libraryName` field on `resolve-library-id` should be the **official spelling**: `Next.js` not `nextjs`, `Three.js` not `threejs`, `Customer.io` not `customerio`.

## Red flags — stop and use Context7

- User asks "how do I do X in [framework] [version]" and you start typing from memory
- You're about to give a CLI command (`npx create-...`, `pnpm add ...`) without checking
- You're explaining a config file format from memory
- You catch yourself thinking "I'm pretty sure it's `useFormStatus`..." — verify it
- You're migrating code between two versions and reasoning about the diff from memory

## Anti-pattern: skipping resolution

Do **not** invent a library ID and call `query-docs` directly. The resolution step is what guarantees you hit the right project (there are many `react-*` packages) and the right version. Skipping it leads to docs for the wrong library.

## Combining with other tools

- **Followed by Write/Edit**: query Context7, then write code informed by current API
- **With deepwiki**: use Context7 for *how to use* a library, deepwiki for *how a repo is built internally*
- **With sequential-thinking**: when designing an architecture that spans multiple libraries, query each, then reason

## One-liner reminder

If a library name appears in the user's question and you haven't queried Context7 yet, you're about to ship stale information.

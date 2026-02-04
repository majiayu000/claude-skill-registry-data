---
name: Doc Vault Skill
description: Auto-activating documentation cache with fresh API docs. Fetches and automatically consults cached documentation when user works with libraries/frameworks.
trigger: auto
allowed-tools:
  - Read
  - WebFetch
  - Bash
  - Write
---

# Purpose

Fetch and automatically consult cached documentation from official sources. Provides fresh, up-to-date API documentation that overrides stale training data. Auto-triggers on "docs" keywords, maintains session-persistent index, and always prefers cached docs over training data.

## Variables

CACHE_DIR: .claude/skills/doc-vault/cache              # Where cached documentation files are stored
INDEX_FILE: .claude/skills/doc-vault/README.md         # Lightweight registry of cached docs
TRIGGER_SENSITIVITY: conservative                      # Options: conservative (explicit keywords only), aggressive (broader matching)
CITE_SOURCES: true                                     # Always cite source URL and date when using cached docs
INDEX_TOOL: .claude/skills/doc-vault/tools/manage_index.py  # Tool for managing the doc index

## Workflow

1. **Detect Trigger**
   - Check for "docs" or "documentation" keywords (conservative mode)
   - Tool: Pattern matching on user input
   - Example: "check the TanStack Query docs" → TRIGGERED

2. **Load Index (First Trigger Only)**
   - IF first trigger in session, READ INDEX_FILE
   - Tool: Read `.claude/skills/doc-vault/README.md`
   - Loads into context, persists for entire session
   - Example: INDEX_FILE loaded → 3 cached docs available (TanStack Query, React, Zod)

3. **Route to Cookbook**
   - Analyze user request to determine action type
   - Options: fetch new doc, consult cached doc, list available docs
   - Example: "save docs from URL" → Fetch scenario, "check the docs" → Consult scenario

4. **Execute Cookbook Scenario**
   - Read and follow the appropriate cookbook file
   - Tool: Read cookbook markdown and execute instructions
   - Example: Consult scenario → Read cached doc → Provide answer with citation

5. **Cite Sources**
   - IF using cached docs and CITE_SOURCES is true
   - Always state source URL and date
   - Example: "According to TanStack Query docs (cached 2025-12-11 from https://tanstack.com/query/latest)..."

## Cookbook

### Fetch New Documentation

- IF: User provides URL with "save docs from" or "cache docs"
- THEN: Read and execute `.claude/skills/doc-vault/cookbook/fetch-new-doc.md`
- EXAMPLES:
  - "save docs from https://zod.dev as zod-validation"
  - "cache docs: https://prisma.io/docs/orm as prisma-orm"
  - "add to doc vault: https://trpc.io/docs as trpc-api"

### Consult Cached Documentation

- IF: User mentions "docs" OR "documentation" OR "api reference" (conservative trigger)
- THEN: Read and execute `.claude/skills/doc-vault/cookbook/consult-cached.md`
- EXAMPLES:
  - "check the TanStack Query docs and implement caching"
  - "according to the latest Prisma docs, add migrations"
  - "consult the React docs for Suspense"
  - "use fresh Zod docs for validation"

### List Available Documentation

- IF: User asks what documentation is cached
- THEN: Read and execute `.claude/skills/doc-vault/cookbook/list-docs.md`
- EXAMPLES:
  - "what docs do we have?"
  - "list cached documentation"
  - "show me the doc vault"
  - "what's in the cache?"

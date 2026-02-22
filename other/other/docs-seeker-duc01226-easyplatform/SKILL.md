---
name: docs-seeker
description: "[Docs] Search technical documentation using executable scripts to detect query type, fetch from llms.txt sources (context7.com), and analyze results. Use when user needs: (1) Topic-specific documentation (features/components/concepts), (2) Library/framework documentation, (3) GitHub repository analysis, (4) Documentation discovery with automated agent distribution strategy"
version: 3.1.0
allowed-tools: Bash, WebFetch, WebSearch
---

# Documentation Discovery via Scripts

## Summary

**Goal:** Search and retrieve technical documentation using executable scripts with llms.txt standard and context7.com sources.

| Step | Action | Key Notes |
|------|--------|-----------|
| 1 | Detect query type | `node scripts/detect-topic.js "<query>"` -- topic-specific vs general |
| 2 | Fetch documentation | `node scripts/fetch-docs.js "<query>"` -- auto URL construction + fallback |
| 3 | Analyze results | `node scripts/analyze-llms-txt.js` -- categorize URLs, recommend agent distribution |

**Key Principles:**
- Scripts first -- never manually construct URLs; scripts handle fallback chains automatically
- Zero-token overhead -- scripts run without context loading
- Progressive disclosure -- load workflow/reference docs only when needed

## Overview

**Script-first** documentation discovery using llms.txt standard.

Execute scripts to handle entire workflow - no manual URL construction needed.

## Primary Workflow

**ALWAYS execute scripts in this order:**

```bash
# 1. DETECT query type (topic-specific vs general)
node scripts/detect-topic.js "<user query>"

# 2. FETCH documentation using script output
node scripts/fetch-docs.js "<user query>"

# 3. ANALYZE results (if multiple URLs returned)
cat llms.txt | node scripts/analyze-llms-txt.js -
```

Scripts handle URL construction, fallback chains, and error handling automatically.

## Scripts

**`detect-topic.js`** - Classify query type

- Identifies topic-specific vs general queries
- Extracts library name + topic keyword
- Returns JSON: `{topic, library, isTopicSpecific}`
- Zero-token execution

**`fetch-docs.js`** - Retrieve documentation

- Constructs context7.com URLs automatically
- Handles fallback: topic → general → error
- Outputs llms.txt content or error message
- Zero-token execution

**`analyze-llms-txt.js`** - Process llms.txt

- Categorizes URLs (critical/important/supplementary)
- Recommends agent distribution (1 agent, 3 agents, 7 agents, phased)
- Returns JSON with strategy
- Zero-token execution

## Workflow References

**[Topic-Specific Search](./workflows/topic-search.md)** - Fastest path (10-15s)

**[General Library Search](./workflows/library-search.md)** - Comprehensive coverage (30-60s)

**[Repository Analysis](./workflows/repo-analysis.md)** - Fallback strategy

## References

**[context7-patterns.md](./references/context7-patterns.md)** - URL patterns, known repositories

**[errors.md](./references/errors.md)** - Error handling, fallback strategies

**[advanced.md](./references/advanced.md)** - Edge cases, versioning, multi-language

## Execution Principles

1. **Scripts first** - Execute scripts instead of manual URL construction
2. **Zero-token overhead** - Scripts run without context loading
3. **Automatic fallback** - Scripts handle topic → general → error chains
4. **Progressive disclosure** - Load workflows/references only when needed
5. **Agent distribution** - Scripts recommend parallel agent strategy

## Quick Start

**Topic query:** "How do I use date picker in shadcn?"

```bash
node scripts/detect-topic.js "<query>"  # → {topic, library, isTopicSpecific}
node scripts/fetch-docs.js "<query>"    # → 2-3 URLs
# Read URLs with WebFetch
```

**General query:** "Documentation for Next.js"

```bash
node scripts/detect-topic.js "<query>"         # → {isTopicSpecific: false}
node scripts/fetch-docs.js "<query>"           # → 8+ URLs
cat llms.txt | node scripts/analyze-llms-txt.js -  # → {totalUrls, distribution}
# Deploy agents per recommendation
```

## Environment

Scripts load `.env`: `process.env` > `.claude/skills/docs-seeker/.env` > `.claude/skills/.env` > `.claude/.env`

See `.env.example` for configuration options.

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed

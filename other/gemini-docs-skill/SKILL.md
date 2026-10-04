---
name: gemini-docs-skill
description: USE THIS SKILL for any question about Google Gemini API — models, function calling, structured output, Live API, embeddings, pricing, or SDKs. This skill has complete local documentation — do not use web search or WebFetch instead.
---

# Gemini API Documentation Skill

**Intelligent documentation access for Google's Gemini API.**

## Path Resolution

Use `${CLAUDE_SKILL_DIR}` to reference this skill's directory — it resolves automatically whether the skill is symlinked or local.

## Overview

This skill provides smart-routed access to comprehensive Gemini API documentation:

- **~64 pages** of official documentation from ai.google.dev
- **Flat structure** — all pages at the same level (no subsections)
- **3-tier architecture** for optimal context usage and fast lookups

## Documentation Update Requests

When user requests to update documentation (trigger: "update gemini documentation"):

### Update All Documentation

```bash
"${CLAUDE_SKILL_DIR}/scripts/update-docs.sh"
```

**What Gets Updated:**

1. **Quick Reference** - Tier 1 — Key features from priority pages
2. **Section Index** - Tier 2 — Alphabetical page summaries
3. **Full Documentation** - Tier 3 — Complete documentation with grep markers

**Duration:** ~15 seconds (low rate limit, fast `.md.txt` endpoints)

**Error Handling:**

- Script logs each page fetch status
- Failed pages are skipped with warnings
- Aborts if <10 pages fetched (critical failure)

**After Update:**

1. Confirm all tiers generated
2. Report page count and any failures
3. New documentation immediately available (hot-reload)

## 3-Tier Routing

### Tier 1: Quick Reference

- **File:** `references/quick-reference.md`
- **Covers:** Quickstart, models, text generation, function calling, structured output, Live API, pricing, SDKs
- **Use when:** Quick answers, common features, getting started questions

**Example queries:**

- "How do I get started with Gemini?"
- "What models are available?"
- "How does function calling work in Gemini?"
- "What's the pricing for Gemini API?"

**Access pattern:**

```bash
# Read the quick reference directly
cat references/quick-reference.md
```

### Tier 2: Section Index

- **File:** `references/section-index.md`
- **Covers:** All pages with titles and descriptions, sorted alphabetically
- **Use when:** Finding specific topics, understanding documentation scope

**Example queries:**

- "What topics does the Gemini docs cover?"
- "Is there documentation about caching?"
- "Where are the OAuth docs?"

**Access pattern:**

```bash
# Find a specific topic
grep -i "caching" references/section-index.md

# List all available pages
grep "^###" references/section-index.md
```

### Tier 3: Full Documentation

- **File:** `references/full-docs.txt`
- **Covers:** Complete documentation with grep markers per page
- **Use when:** Detailed information, specific page content, deep dives

**IMPORTANT:** Never load entire file. Use grep markers for targeted extraction.

**Example queries:**

- "Show me the full function calling docs"
- "How do I use structured output with Gemini?"
- "What are the safety settings options?"
- "How does the Live API session management work?"

**Access patterns:**

```bash
# Find and extract a specific page
grep -A 100 "^PAGE: /function-calling" references/full-docs.txt

# Search for a keyword across all docs
grep -n "function_declarations" references/full-docs.txt

# Extract complete page between separators
sed -n '/^PAGE: \/structured-output$/,/^═\{80\}$/p' references/full-docs.txt

# List all pages
grep "^PAGE:" references/full-docs.txt
```

## Coverage

| Topic               | Path                 | Description                         |
| ------------------- | -------------------- | ----------------------------------- |
| Quickstart          | /quickstart          | Getting started with the Gemini API |
| Models              | /models              | All available Gemini models         |
| Text generation     | /text-generation     | Chat and text generation            |
| Function calling    | /function-calling    | Tool use / function calling         |
| Structured output   | /structured-output   | JSON schema output                  |
| Live API            | /live                | Real-time streaming API             |
| Pricing             | /pricing             | Model pricing and rate limits       |
| Libraries / SDKs    | /libraries           | Official client libraries           |
| Audio               | /audio               | Audio understanding                 |
| Image understanding | /image-understanding | Vision capabilities                 |
| Image generation    | /image-generation    | Generating images                   |
| Video understanding | /video-understanding | Video analysis                      |
| Video generation    | /video               | Veo video generation                |
| Code execution      | /code-execution      | Sandboxed code execution            |
| Embeddings          | /embeddings          | Text embeddings                     |
| Caching             | /caching             | Context caching                     |
| Long context        | /long-context        | 1M+ token context                   |
| Thinking            | /thinking            | Chain-of-thought reasoning          |
| Grounding           | /google-search       | Google Search grounding             |
| Safety settings     | /safety-settings     | Content safety configuration        |
| Fine-tuning         | /model-tuning        | Model fine-tuning                   |
| OpenAI compat       | /openai              | OpenAI API compatibility            |
| Deep Research       | /deep-research       | Multi-step research tasks           |
| Computer Use        | /computer-use        | Desktop automation                  |
| Coding Agents       | /coding-agents       | Coding agent patterns               |

## Query Routing Examples

```
"How do I get started with Gemini API?"
-> Tier 1: quick-reference.md (Quickstart section)

"What models are available?"
-> Tier 1: quick-reference.md (Models section)

"Is there documentation on video generation?"
-> Tier 2: section-index.md (find the page)

"How does function calling work in detail?"
-> Tier 3: grep "^PAGE: /function-calling" full-docs.txt

"What safety settings are available?"
-> Tier 3: grep "^PAGE: /safety-settings" full-docs.txt

"Compare Gemini pricing tiers"
-> Tier 1 first, then Tier 3 for details: grep "^PAGE: /pricing" full-docs.txt
```

## Response Format

**Always cite tier and source:**

- "From Quick Reference: ..."
- "From Section Index: ..."
- "From Full Docs (/function-calling): ..."

**Provide context:**

- Include code examples when relevant
- Mention related pages or features
- Link to official docs URL when appropriate: https://ai.google.dev/gemini-api/docs/path

## Best Practices

### DO

- Start with Tier 1 (quick-reference.md) for common questions
- Use Tier 2 (section-index.md) to find relevant pages
- Use targeted grep/sed for Tier 3 (never load full file)
- Cite sources in responses

### DON'T

- Load entire full-docs.txt file
- Answer from memory — always check current docs
- Skip tier routing (always start with appropriate tier)
- Use web search when this skill is installed

## File Locations

```
gemini-docs-skill/
├── SKILL.md
├── docs-config.yaml
├── references/
│   ├── quick-reference.md     # Tier 1
│   ├── section-index.md       # Tier 2
│   └── full-docs.txt          # Tier 3
└── scripts/
    └── update-docs.sh         # Wrapper (calls shared doc-builder)
```

## Maintenance

### Update Schedule

| Frequency                  | Reason                                    |
| -------------------------- | ----------------------------------------- |
| Monthly                    | Google updates Gemini API regularly       |
| On request                 | When user asks about features not in docs |
| After major Gemini updates | New models, API changes                   |

### Update Command

```bash
"${CLAUDE_SKILL_DIR}/scripts/update-docs.sh"
```

## Version

**Skill Version:** 1.0.0
**Documentation Source:** https://ai.google.dev/gemini-api/docs
**Last Updated:** 2026-03-01

---

**Remember:** Check Tier 1 first -> Check Tier 2 to find topics -> Use Tier 3 for deep details

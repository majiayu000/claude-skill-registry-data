---
description: Optimize for AI search — LLM visibility, AI Overviews, and citation strategy
---

# AI SEO

Optimize "$ARGUMENTS" for AI-powered search — LLM citations, Google AI Overviews, ChatGPT, Perplexity, and other AI search surfaces.

## Prerequisites

Read `.metapowers/marketing/$ARGUMENTS/00-strategy.md`. If this file does not exist, tell the user:

> Phase 0 (Strategy) has not been completed for "$ARGUMENTS". Run `/marketing:customer-research $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check and log to `.metapowers/marketing/$ARGUMENTS/skip-log.md`.

## Process

1. **Read context:**
   - Read `.metapowers/marketing/$ARGUMENTS/00-strategy.md` for positioning and audience
   - Read `.metapowers/marketing/$ARGUMENTS/01-reach.md` if it exists (for content and SEO context)
   - Read `plugins/marketing/shared/seo-checklist.md` for AI search section

2. **Audit current AI visibility:**
   - Use WebSearch to check if "$ARGUMENTS" appears in AI-generated answers
   - Test key queries in multiple AI search tools
   - Note which competitors are being cited by AI

3. **Analyze AI citation patterns:**
   - What content structure gets cited by LLMs? (lists, definitions, comparisons, data)
   - Which domains are most frequently cited in the category?
   - What makes content "LLM-friendly"? (clear structure, authoritative sources, direct answers)

4. **Develop optimization strategy:**
   - Content structure recommendations (clear H2s, direct answers, FAQ format)
   - Entity optimization (be clearly identifiable as an entity with consistent naming)
   - E-E-A-T signals (experience, expertise, authority, trust markers)
   - Structured data to aid AI understanding
   - Citation-worthy content types (original research, data, tools, definitions)

5. **Write the artifact** — append to `.metapowers/marketing/$ARGUMENTS/01-reach.md` under a `## AI SEO` section:
   - **Current AI Visibility** — where "$ARGUMENTS" appears (or doesn't) in AI answers
   - **Citation Patterns** — what gets cited in this category
   - **Optimization Strategy** — content structure, entity, E-E-A-T recommendations
   - **Content Recommendations** — specific content to create for AI visibility
   - **Monitoring Plan** — how to track AI search presence

## Output

AI SEO strategy appended to `.metapowers/marketing/$ARGUMENTS/01-reach.md`. Present a summary highlighting:
- Current AI search visibility status
- Top 3 optimization opportunities
- Most impactful content type to create

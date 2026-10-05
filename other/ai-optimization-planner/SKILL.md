---
name: ai-optimization-planner
alias: /ai-optimization-planner
description: "Plan AI Overview readiness improvements — RAG retrievability, E-E-A-T signals, query fan-out coverage, semantic HTML, schema markup, agentic channel setup."
version: 1.0.0
disallowedTools: Bash
---

# AI Optimization Planner

## JTBD (Jobs To Be Done)

### Primary Job
When my site or content exists and I want to improve its eligibility for Google AI Overviews,
I want a structured AIO readiness plan,
so I can address the specific signal gaps that affect whether my content is retrieved and cited in AI-generated answers.

### Secondary Jobs
- When I have good traditional SEO but my content isn't appearing in AI Overviews, I want to understand which AIO-specific signals are missing.
- When I'm preparing an e-commerce or local business site for Google's emerging agentic search experiences (Merchant Center, GBP, UCP), I want a readiness assessment.
- When I know I need to improve E-E-A-T but don't know where to start, I want a prioritized plan with specific improvements across Experience, Expertise, Authoritativeness, and Trustworthiness.

### This Skill Is For
- A team with existing content that isn't appearing in AI Overviews despite good traditional SEO.
- A publisher wanting to understand the E-E-A-T signal gaps that reduce AIO inclusion probability.
- A commerce or local business team preparing for Google's agentic search channels.
- An engineering team needing a concrete schema markup and semantic HTML implementation plan.

### This Skill Is NOT For
- Writing new content from scratch — use `copy-planner` for that.
- Structural SEO review (heading hierarchy, meta descriptions, intent alignment, internal linking) — use `seo-advisor` for that.
- Adding `llms.txt`, AI-specific markup, or keyword variants for AI modes — Google's AIO guide explicitly states these are not AIO signals.
- Keyword research, SERP analysis, or traffic prediction — use Ahrefs, SEMrush, or Google Search Console.

### Resolution Paths

| User Situation | What Happens | What They Leave With |
|---------------|-------------|----------------------|
| Content exists, not in AI Overviews | AIO planner audits E-E-A-T, fan-out, schema, and RAG eligibility | Tiered improvement plan with acceptance criteria |
| Preparing for agentic channels | Phase 3e assesses Merchant Center, GBP, UCP readiness | Agentic Channel Readiness report with Tier 3 tasks |
| Schema markup confusion | Phase 3d maps expected vs actual Schema.org types | Specific schema property list to implement |
| Discovery before planning | Phase 2 surfaces community tools and MCPs | Tooling survey with availability table |

### When to Escalate
- **Structural SEO first**: Always invoke `seo-advisor` before or in parallel — structural SEO is a prerequisite for AIO eligibility, not a substitute.
- **Content gaps require original writing**: Escalate to `copy-planner` + `copy-critic` when Phase 3b (E-E-A-T) identifies MAJOR commodity content gaps.
- **HTML/multimedia restructuring**: Escalate to `web-design-planner` or `design-partner` when Phase 3d identifies MAJOR semantic HTML landmark or layout gaps.
- **Accessibility overlap**: Escalate to `a11y-planner` when semantic HTML improvements overlap with accessibility compliance needs.

---

## Purpose

Google's AI Overviews are powered by RAG (Retrieval-Augmented Generation). Content that appears in AI Overviews satisfies a different signal set than content that ranks in traditional search:

1. **Snippet eligibility** — not just indexed, but eligible for Google to extract and use
2. **Non-commodity content** — first-hand Experience that distinguishes original from recycled material
3. **Query fan-out coverage** — addressing the related queries Google generates, not just the primary query
4. **Semantic HTML and schema markup** — structure that browser agents can parse as reliably as humans
5. **Agentic readiness** — for transactional sites, the structured data and platform integrations that Google's agents need

`seo-advisor` covers the structural layer (headings, meta, intent, internal linking). This skill covers the AIO-specific layer above it.

---

## What This Skill Does

- ✓ Discovers and surveys available MCP tools (Search Console, Playwright, web search) for the planning session
- ✓ Audits indexing status and snippet eligibility (RAG prerequisites)
- ✓ Assesses E-E-A-T across all four dimensions with STRONG/PARTIAL/ABSENT ratings
- ✓ Generates query fan-out analysis (5–8 related queries) and maps content coverage
- ✓ Audits semantic HTML landmark elements and Schema.org markup gaps
- ✓ Assesses multimedia richness (original vs stock, informational vs decorative)
- ✓ Evaluates agentic channel readiness (Merchant Center, GBP, UCP) for transactional sites
- ✓ Produces a tiered implementation plan (Tier 1: quick wins, Tier 2: content investment, Tier 3: platform/architecture)
- ✓ Defines test strategy and review checkpoints with companion skills

## What This Skill Does NOT Do

- ✗ Write or rewrite content
- ✗ Audit structural SEO (heading hierarchy, meta descriptions, internal linking)
- ✗ Recommend `llms.txt` or AI-specific markup (not AIO signals per Google)
- ✗ Predict rankings or traffic
- ✗ Run shell commands, execute code, or query live APIs directly (use MCP tools instead)

---

## MCP and Tool Baseline

These tools enhance the plan's accuracy when available. The planner degrades gracefully when they are not available but flags assumptions as FRAGILE.

| Tool | Purpose | Impact If Unavailable |
|------|---------|----------------------|
| Search Console MCP / `gsc-cli` | Verify indexing status and snippet eligibility | Indexing assumed; flagged FRAGILE |
| Playwright MCP | Inspect as-rendered DOM, schema markup, landmark elements | Source-only HTML review |
| Web search MCP (Exa, Brave, Tavily) | Test current AIO appearance; validate fan-out query coverage | Manual testing instructions provided |
| Lighthouse CLI / PageSpeed Insights API | Core Web Vitals as indirect indexing quality signal | CWV noted as out-of-scope |
| Schema.org Validator | Validate schema markup before deployment | Manual validation instructions |

## External Discovery

Phase 2 of the planning protocol uses these discovery mechanisms to surface community tools:

- **`discover-skills.sh`** (meta-router repo): Run with keywords `"AIO"`, `"Search Console"`, `"E-E-A-T"` to find relevant community skills
- **GitHub search**: Search `"Search Console" site:github.com skill SKILL.md` and `"E-E-A-T" OR "AI Overviews" site:github.com claude skill`

Discovery is surfaced as options for the user. External skills are never auto-invoked.

---

## Use_When

- Content team reports "our articles have good SEO but don't appear in AI Overviews"
- E-commerce site preparing for Google Shopping AI responses (Merchant Center, Product schema)
- Local business wanting to appear in local agentic responses (GBP, LocalBusiness schema)
- Developer team needs a concrete Schema.org implementation checklist
- Content strategist wants to understand E-E-A-T gaps before commissioning new content
- Pre-publishing AIO readiness check on high-investment content

## Do_Not_Use_When

- Need to write content from scratch → use `copy-planner`
- Need structural SEO review (heading hierarchy, meta, internal links, intent) → use `seo-advisor`
- Need keyword research or SERP analysis → use Ahrefs, SEMrush, Google Search Console
- Planning to add `llms.txt` or AI-specific markup → read Google's AIO guide first; these are not signals
- Content doesn't exist yet → start with `copy-planner` then return here for AIO review

---

## Paired With

- **`ai-optimization-critic`**: Companion reviewer — invoke at review checkpoints 1 (post-audit) and 3 (post-content-investment)
- **`seo-advisor`**: Structural SEO complement — run first or in parallel; invoke at checkpoint 2 (post-Tier-1)
- **`copy-planner`**: When E-E-A-T audit identifies MAJOR commodity content gaps requiring original writing
- **`copy-critic`**: After Tier 2 content investment, before final `ai-optimization-critic` review
- **`web-design-planner`** / **`design-partner`**: When semantic HTML or multimedia gaps require layout/component restructuring
- **`a11y-planner`**: When semantic HTML improvements overlap with accessibility compliance

---

## Steps

### Standard Mode

When invoked with `/ai-optimization-planner [site or content URL/samples]`:

1. Run Phase 1: Scope and Context — establish content type, agentic goal, risk level
2. Run Phase 2: Discovery and Tooling Survey — MCP availability, companion routing, community skill discovery
3. Run Phase 3a–3e (conditional on content type): RAG retrievability, E-E-A-T, fan-out, semantic HTML, agentic channels
4. Run Phase 4: Assumption Register
5. Run Phase 5: Test Strategy
6. Run Phase 6: Implementation Plan (Tier 1 / Tier 2 / Tier 3)
7. Run Phase 7: Review Checkpoint Plan
8. Output all required headings (see Output Format Contract)

### Output Format Contract

These headings must appear in the output (load-bearing for parsers):

```
## Feature Overview
## Tooling Survey
## RAG Retrievability Report
## E-E-A-T Signal Matrix
## Query Fan-Out Coverage Matrix
## Semantic HTML Signal Map
## Agentic Channel Readiness
## Assumption Register
## Implementation Plan
## Test Strategy
## Review Checkpoint Plan
```

`## Agentic Channel Readiness` must be present for all outputs — use "N/A: non-transactional content" for informational sites.

---

## Companion_Skills

- **ai-optimization-critic**: Companion reviewer for checkpoint reviews
- **seo-advisor**: Structural SEO prerequisite and checkpoint 2 reviewer
- **copy-planner**: Content investment companion for Tier 2 gaps
- **copy-critic**: Content quality reviewer before AIO eligibility re-review
- **web-design-planner**: Platform/architecture companion for Tier 3 semantic HTML work
- **a11y-planner**: Semantic HTML companion when accessibility overlaps AIO

---

**Version:** 1.0.0
**Last Updated:** 2026-05-19
**Standalone Ready:** Yes
**Perspective Module:** No

---
name: ai-product-teardown
description: "Structured teardown of AI products (ChatGPT, Claude, Gemini, Perplexity, Copilot, etc.). Analyzes product decisions, UX patterns, technical architecture, business model, and competitive positioning."
argument-hint: "[product name or feature]"
---

# AI Product Teardown Skill

Perform a structured, opinionated teardown of any AI product — analyzing the product decisions, UX, technical architecture, business model, and competitive positioning from a PM lens.

## When to Use
- User asks "Tear down [AI product]" or "Analyze [AI product]"
- User wants to understand the product thinking behind an AI feature
- User wants to build product intuition about AI products
- User says `/ai-product-teardown` followed by a product name
- Great for: ChatGPT, Claude, Gemini, Perplexity, Copilot, Midjourney, Cursor, v0, NotebookLM, etc.

## Framework: AI Product Teardown (7 Sections)

### Section 1: Product Overview
- **What it is**: One-sentence description
- **Company**: Who built it, their mission, and strategic context
- **Launch date & trajectory**: When launched, key milestones, current scale
- **Target users**: Primary and secondary audiences
- **Business model**: How it makes money (or plans to)

### Section 2: Core Value Proposition
- **Job to be Done**: What fundamental job does this product do for users?
- **10x moment**: What's the moment where users think "this is magic"?
- **Switching cost**: What would it take to switch away?
- **Network effects**: Does it get better with more users? How?

### Section 3: UX & Product Decisions
Walk through the key product decisions and evaluate each:
- **Onboarding flow**: How does a new user go from zero to value?
- **Core interaction model**: Chat? Canvas? Structured output? Multi-modal?
- **Information architecture**: How is functionality organized?
- **Personalization**: How does it adapt to different users?
- **Error handling**: What happens when the AI is wrong?

For each decision, evaluate:
- What they got RIGHT and why
- What they got WRONG or could improve
- What trade-off they're making (and whether you'd make the same one)

### Section 4: Technical Architecture (PM Lens)
Analyze the technical choices from a product perspective:
- **Model strategy**: Which model(s)? Why that capability level?
- **Latency vs. quality trade-off**: Where do they sit on the spectrum?
- **Context & memory**: How does it handle conversation history?
- **Safety & guardrails**: What's their content policy approach?
- **Tool use / plugins / integrations**: How extensible is it?
- **Pricing architecture**: How do technical costs map to pricing?

### Section 5: Growth & Distribution
- **Acquisition channels**: How do users find this? (organic, viral, paid, partnerships)
- **Activation**: What gets users to the "aha moment"?
- **Retention loops**: What brings users back?
- **Monetization**: Free → paid conversion strategy
- **Viral mechanics**: Does usage naturally create awareness?

### Section 6: Competitive Positioning
- **Direct competitors**: Who else does this job?
- **Positioning map**: Plot on 2x2 (e.g., capability vs. safety, consumer vs. enterprise)
- **Sustainable moats**: What's defensible? (data, distribution, brand, model quality, ecosystem)
- **Vulnerability**: Where could a competitor win?

### Section 7: PM Recommendations
If you were the PM, what would you do next?
- **Top 3 features to build** (with reasoning and expected impact)
- **Top 1 thing to kill or change** (what's not working)
- **Strategic bet**: One big swing that could transform the product
- **Metrics to watch**: What would you track weekly?

## Output Format
Write as an opinionated product review — structured but with a clear point of view. Use screenshots/descriptions of specific UI elements where relevant. Aim for ~2000 words. Be specific and cite real features.

## Research-First Workflow
1. **Research** — Search for latest product updates, user reviews, competitor announcements, company blog posts, and usage data. Do 5-10 searches.
2. **Cite sources** — Include `[linked source](url)` inline for factual claims.
3. **Display** the complete teardown.

## What Good Looks Like
- Shows you've done homework on the product landscape
- Demonstrates structured product thinking on real products
- Reveals your product taste and judgment
- Provides concrete examples to reference in product discussions
- Builds intuition about AI product patterns across the industry

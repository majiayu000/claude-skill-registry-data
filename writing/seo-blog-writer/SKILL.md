---
name: seo-blog-writer
description: Write an SEO blog post, how-to, listicle, comparison, refresh or localized article from an approved brief, answer-first and without generic AI prose. Use for "write this blog post", "draft the article from this brief", "refresh this page", "write a listicle", "make this sound less like AI".
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/seo-blog-writer
---

# SEO blog writer

Write SEO blog, how-to, listicle, comparison, refresh, and localized drafts from a detailed, approved brief, and hand back a publishable draft or refresh package with its meta, schema, links, asset list and fact-check notes. This skill does not pick topics from scratch. If the brief is weak, contradictory, or missing critical facts, stop and return a brief defect report instead of producing generic content.

> **Romeo's rule:** Answer the question, admit the drawbacks, and cut anything a reader would skim past; nobody ever wished an article had more throat-clearing.

## Use this when

- A detailed brief is approved and you need a publishable draft or refresh package.
- You need a how-to, listicle, comparison or alternatives page, profession/use-case guide, landing-style article or localized article written to a brief.
- An existing ranking page needs a careful refresh that leaves its URL and ranking-sensitive parts alone.
- A draft reads like generic AI prose and needs a de-robot pass.

## Don't use this for

- Writing without a brief, or from a thin one → `seo-content-brief`.
- Picking the topic or keyword → `seo-opportunity-research`.
- Scoring the draft before it ships → `seo-content-qa`.
- Putting the finished draft into a CMS → `cms-publishing-adapter`.

## What you need

### Required

- Approved content brief.
- Content type: how-to, listicle, comparison, alternatives, profession/use-case guide, refresh, landing-style article, localized article.
- Target keyword cluster and search intent.
- Brand voice and banned phrases.
- Product facts and prohibited claims.
- Required links and conversion page.
- Required assets or image policy.
- Schema requirements.
- Output format: Markdown, HTML, document draft, CMS JSON, or handoff package.

### Helpful

- SERP summaries.
- Existing draft or URL for refresh.
- Screenshots/images.
- Competitor fact sources.
- Localization glossary.
- CMS constraints.

### No tools?

This skill needs no paid tools: the brief, the product facts and a text editor are enough. If you can't fetch URLs, ask the user to paste the existing page (for a refresh), the competitor pages behind any claim you need to make, and any source you must cite. Get screenshots from the user, or list them in the missing asset queue; never describe an image you don't have. Check any JSON-LD you write by pasting it into the Schema Markup Validator (validator.schema.org) or Google's Rich Results Test.

## Ground rules

- Answer first. Background comes later.
- Write for one reader, not a generic audience segment.
- Use simple words and short paragraphs.
- Be specific early: numbers, exact tools, real situations, concrete tradeoffs.
- Do not write filler transitions between every section.
- Do not sound like a neutral encyclopedia when the reader needs a decision.
- Be honest about product fit. Credibility beats forced promotion.
- Do not invent pricing, capabilities, testimonials, review scores, privacy claims, competitor claims, or legal/medical/financial claims.

## Mandatory anti-AI voice rules

Before output, run a de-robot pass:

- Remove generic openings like "In today's fast-paced world", "Let's dive in", "Unlock", "Harness", "Game-changer", "Ever-evolving", "It is important to note", "Whether you're a...".
- Remove repetitive sentence starts.
- Break perfect parallel structure across list items when it sounds synthetic.
- Replace vague adjectives like powerful, robust, seamless, cutting-edge with specific benefits or delete them.
- Use honest drawbacks for tools and comparisons.
- Avoid hedging every claim with may/might/could unless uncertainty is real.
- Keep conclusions useful, not a rephrased intro.
- Use punctuation accepted by the site's style guide. If em dashes are banned, remove all em dashes.

## Universal structure

Every draft must include:

1. TL;DR near the top.
   - Listicle: all items with links and one-line best-fit/value.
   - How-to: 2-3 sentence summary of what to do.
   - Comparison: quick verdict and who each option fits.
   - Refresh: concise answer that improves the existing page without disrupting ranking-sensitive areas.

2. Answer-first block immediately after TL;DR.
   - 2-4 short sentences.
   - Directly answer the main query.
   - Make it self-contained and quotable.

3. Short intro.
   - 2-3 short paragraphs max.
   - No generic scene-setting.
   - State the problem and what the reader will get.

4. Main sections.
   - H2/H3 hierarchy follows the brief.
   - Important H2 sections open with a short direct answer before detail.
   - Use tables/bullets only when they make scanning easier.

5. Conclusion.
   - Short, decision-oriented, with a clear next action.

6. FAQs.
   - Concise, direct, matched to search questions.
   - Add FAQPage markup only if the brief requires it; Google retired FAQ rich results in May 2026, so it wins no rich result there.

## Content type templates

### How-to guide

Use when the reader wants instructions.

Structure:

- TL;DR.
- Answer-first summary.
- Requirements/prerequisites only if needed.
- Steps near the top. Do not bury steps below long background sections.
- Each step: action, short explanation, expected result.
- Troubleshooting.
- Alternatives or built-in options if SERP expects them.
- FAQs.
- Related internal links.

Rules:

- Start steps with verbs.
- Keep background after the core process.
- Add screenshots where steps involve software UI.

### Listicle

Use when the reader is comparing multiple tools/options.

Structure:

- TL;DR with all tools and links.
- Early verdict: best overall, best budget, best for specific use cases.
- Methodology: short and credible.
- Comparison table if 5+ items.
- H2 per tool:
  - what it is
  - best for
  - key strengths
  - biggest downside
  - pricing when safely known
  - verdict
- FAQs.

Rules:

- Every featured tool needs a homepage/relevant link.
- Every featured tool needs an image/screenshot unless the asset policy says otherwise.
- Do not rank the site's own product #1 by default. Rank it only where evidence and fit support it.
- Include at least one honest drawback per tool when relevant.

### Comparison / alternatives

Use when the reader is choosing between named products or searching competitor alternatives.

Structure:

- TL;DR verdict.
- Who should choose each product.
- Optional third-option/product framing only if honest and approved.
- Comparison table with row-level winner/fit where useful.
- Pricing/value section with clear assumptions.
- Feature sections.
- Privacy/security/fact-sensitive section if relevant.
- Decision scenarios.
- FAQs.

Rules:

- Source-check competitor claims.
- Do not claim market superiority without evidence.
- Use careful language for reviews, Reddit sentiment, accuracy, speed, CPU/RAM, storage, privacy, and pricing.
- Avoid defamatory or aggressive claims.

### Profession / use-case guide

Structure:

- TL;DR.
- Why this audience cares.
- Specific workflows.
- Setup or recommended tool path.
- Tips by scenario.
- Risks/limitations.
- FAQs.

Rules:

- Use examples from that job, not generic productivity copy.
- Avoid medical/legal claims unless sourced and approved.

### Refresh

Use when improving an existing ranking page.

Rules:

- Preserve existing URL.
- Preserve title/meta by default on pages with meaningful rankings/impressions.
- Improve top answer block, TL;DR, FAQs, internal links, clarity, examples, and stale facts first.
- Do not restructure ranking-sensitive pages beyond the brief.
- Mark any risky title/meta/slug recommendation separately for human approval.

### Localized article

Rules:

- Use researched local keywords and slugs, not direct translations.
- Match local search intent and SERP page type.
- Use the approved locale voice, pronouns, CTA language, currency, and claims.
- Avoid English-first assumptions.

## SEO requirements

- Primary keyword in title/H1 for new content.
- Primary keyword in first 100 words where natural.
- Related terms distributed naturally.
- Question-style headings when they match query language.
- Internal links to conversion pages first, then supporting content.
- External links for named tools, platforms, sources, or claims.
- Meta title/description suggestions for new content or when requested.
- Schema matching visible content.

## Product/factual safety

Before output, check:

- Pricing matches provided facts.
- Free/free-trial wording is accurate.
- Platform support is accurate.
- Privacy/security/processing claims match approved language.
- Competitor claims are sourced or softened.
- No fake testimonials, review counts, benchmarks, awards, or customer logos.
- No unsupported regulated claims.

## Asset rules

- Listicles/comparisons: every featured tool/product needs link + image/screenshot unless exempted.
- Use approved asset libraries before fresh generation/capture.
- Include alt text that describes the actual product or UI, not keyword stuffing.
- If assets are missing, output a clear asset queue rather than pretending they exist.

## Steps

1. **Check the brief.** Confirm it gives target intent and job type, carries product facts for product-heavy content, and does not require unsupported claims or duplicate an existing page. If any check fails, stop and return a brief defect report (see Stop and flag if).
2. **Pick the template.** Choose the content type template that matches the brief. For a refresh, read the existing page first and note what is ranking-sensitive.
3. **Draft to the universal structure.** TL;DR, answer-first block, short intro, main sections in the brief's H2/H3 order, conclusion, FAQs, plus the template's own structure and rules.
4. **Apply the SEO requirements.** Title/H1, first 100 words, headings, internal and external links, meta suggestions, schema matching visible content.
5. **Run the de-robot pass.** Apply every mandatory anti-AI voice rule to the whole draft, not just the intro.
6. **Run the product/factual safety check.** Fix or soften every claim that fails it, and log risky claims in the fact-check notes.
7. **Resolve assets.** Apply the asset rules; anything missing goes in the missing asset queue.
8. **Package the output.** Produce everything in What to hand back, in the requested format.

## What to hand back

Fill in this template. The draft goes in the format the brief asked for; everything else stays in Markdown.

```markdown
**What I found:** <what was written, for which brief, query and content type>
**What matters most:** <the riskiest claim, deviation or missing input>
**What to do first:** <e.g. supply 3 screenshots, then run QA>

## Draft
<full draft in the requested format: Markdown, HTML, document draft, CMS JSON, or handoff package>

## Meta
- Meta title: <...>
- Meta description: <...>

## Schema JSON-LD
<JSON-LD block, or "not required by the brief">

## Links
- Internal: <URL> | anchor | why
- External: <URL> | what it supports

## Assets
- Present: <file or URL> | alt text
- Missing asset queue: <what is needed> | where it goes | suggested alt text

## Fact-check notes
- <risky claim> | source or "provided by site owner" | softened: yes / no

## QA handoff notes
- <deviations from the brief and why; what QA should check hardest>

## What I could not check
- <e.g. competitor pricing page not reachable; claim softened>
```

## Stop and flag if

Fail instead of writing, and return a brief defect report (what is missing or contradictory, and what is needed to proceed), if:

- Brief does not specify target intent and job type.
- Product facts are missing for product-heavy content.
- The requested angle requires unsupported claims.
- The draft would duplicate an existing page without a refresh/consolidation brief.
- Required output format cannot be produced from available information.

## Next step

- Run `seo-content-qa` with the draft, the brief and the fact-check notes.
- Once QA passes, run `cms-publishing-adapter` with the approved draft, meta, schema and asset list.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills

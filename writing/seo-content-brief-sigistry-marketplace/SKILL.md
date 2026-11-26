---
name: seo-content-brief
description: Turn a chosen SEO opportunity into a precise content brief (create vs refresh, intent, outline, title/meta policy, product facts, links, assets, schema, QA criteria) before anyone writes. Use for "write a content brief", "brief for this keyword", "outline this article", "plan a refresh of this page".
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/seo-content-brief
---

# SEO content brief

Turn a selected SEO opportunity into a precise brief for create, refresh, landing, comparison, or consolidation work. Use it after research or audit selects an opportunity and before a writer or editor changes content. A good brief is a control surface. It prevents generic writing, duplicate pages, risky title/meta edits, unsupported claims, and CMS-specific leakage. It hands back a brief a writer can follow and QA can use to pass or fail the draft.

> **Romeo's rule:** If QA can't fail a draft against your brief, you haven't written a brief, you've written a wish.

## Use this when

- Research or an audit has picked an opportunity and someone, person or agent, is about to write or change content.
- You need to decide, in writing, whether this is a new page or a refresh of an existing one.
- A page that already ranks needs changes and you want them surgical, with the title/meta risk spelled out.
- A listicle, comparison, how-to or landing page needs a brief that forces the verdict, steps or value proposition to the top.
- You need acceptance criteria that QA can judge a draft against.

## Don't use this for

- Choosing which topic or keyword to go after → `seo-opportunity-research`.
- Writing the draft itself → `seo-blog-writer`.
- Scoring a finished draft → `seo-content-qa`.
- Only rewriting titles and meta descriptions for clicks → `title-meta-ctr`.

## What you need

### Required

- Selected opportunity with score and evidence.
- Recommended action: create, refresh, landing page, comparison page, consolidation, internal-link update, snippet review.
- Target keyword cluster and secondary terms.
- Search intent and SERP notes.
- Existing URL or proposed URL.
- Site inventory record for existing pages.
- Business/product profile.
- Product facts and prohibited claims.
- Required conversion pages and internal links.
- Brand/editorial rules.
- Output target: Markdown, HTML, doc, CMS package, or task brief.

### Helpful

- Top SERP page summaries.
- Screenshots/media requirements.
- Analytics/conversion data.
- Customer support/sales/product usage evidence.
- Localization glossary.
- CMS constraints.

### No tools?

Take the opportunity and its evidence from the user or from pasted research output. For SERP notes, search the target query in a private window set to the target country and record the top 5 results: page type, title angle, headings (view-source or reader view), tables, media. For an existing page, view-source gives you the `<title>`, meta description, `<h1>`, canonical and any JSON-LD; a Search Console Performance export filtered to that page tells you whether it already ranks and for what. Rich Results Test or the Schema Markup Validator shows what structured data the page has now. Product facts and prohibited claims must come from the user: ask rather than guess, and mark anything unconfirmed as an open question.

## Ground rules

- The brief must choose create vs refresh before writing starts.
- Search intent must be explicit enough that QA can fail the draft if it misses it.
- The article/page must answer the core query near the top.
- Existing ranked pages need surgical instructions, not casual rewrites.
- For listicles and comparisons, the verdict must appear early.
- For how-to posts, steps must appear near the top.
- For commercial landing pages, conversion path matters more than long editorial coverage.
- For localization, use researched local keywords, not translated English terms.

## Steps

1. **Confirm the job type.**
   - New blog post: no existing page satisfies the intent.
   - Refresh: existing page is close but weak, stale, or under-structured.
   - Landing page: query is commercial/platform/tool-specific and needs conversion focus.
   - Comparison page: query includes vs, alternatives, competitors, pricing, buyer objections, or decision support.
   - Consolidation: multiple URLs split the same intent.
   - Internal-link update: target page exists and mainly needs authority flow.
   - Snippet review: CTR is weak and visible SERP promise may be the issue.

2. **State the reader and business reason.**
   - Who is searching?
   - What job are they trying to do?
   - Where are they in the funnel?
   - What product or conversion page should this support?
   - Why now?

3. **Lock the intent.**
   - Classify: informational, commercial, comparison, transactional, troubleshooting, local, template/tool, navigational, mixed.
   - Describe what the first useful answer must say.
   - List what the page should not become. Example: do not turn a platform landing page into a generic blog guide.

4. **Summarize SERP expectations.**
   - Dominant page types.
   - Common headings and sections.
   - Content gaps.
   - Table/tool/media/schema expectations.
   - Risks: forum-heavy SERP, wrong intent, outdated competitor facts, medical/legal/privacy claims.

5. **Set title/meta policy.**
   - New page: provide title/H1/meta direction.
   - Existing ranked page: default to preserving title/meta unless the opportunity explicitly requires snippet work and risk is accepted.
   - If changing title/meta is recommended, state why current data justifies the risk.

6. **Define the top-of-page structure.**
   - TL;DR requirements:
     - listicle: bullet list of all items with links and one-line value.
     - how-to: 2-3 sentence summary.
     - comparison: clear who-should-pick-what verdict.
     - landing page: direct value proposition and fit.
   - Answer-first block: 2-4 short sentences that directly answer the main query.
   - For how-to, require steps before background discussion.

7. **Create the outline.**
   - H1.
   - Section sequence with H2/H3 headings.
   - Purpose of each section.
   - Required examples, tables, screenshots, product images, code snippets, or data points.
   - Required FAQ questions.
   - Schema type: Article, SoftwareApplication, Product, ItemList, Comparison-like Article, BreadcrumbList, as appropriate. Don't specify FAQPage or HowTo to win a rich result: Google removed HowTo rich results in 2023, and FAQ rich results (limited to government and health sites from 2023) were retired entirely in May 2026. A visible FAQ section is still fine; see `schema-markup` for whether any markup is worth adding.

8. **Add product and factual constraints.**
   - Approved claims.
   - Pricing/free-trial wording.
   - Platform support.
   - Privacy/security/processing claims.
   - Claims that require a source.
   - Claims to avoid.
   - Competitors that may/may not be named.

9. **Add linking rules.**
   - Primary conversion page to link.
   - Supporting internal links.
   - External links required for named tools, competitors, platforms, or sources.
   - Anchor guidance.
   - Link to conversion pages before supporting blog posts when both are relevant.

10. **Add asset rules.**
    - For listicles/comparisons: every featured tool/product needs a link and image/screenshot unless explicitly exempted.
    - Give preferred dimensions, storage, alt text, and whether generated imagery is allowed.
    - For existing screenshot libraries, require reuse before fresh capture.

11. **Define QA acceptance criteria.**
    - Minimum score or pass/fail gate.
    - Critical facts that must be correct.
    - Structure checks.
    - Human-writing checks.
    - Link/asset/schema checks.
    - CMS/output constraints.

## What to hand back

Fill in this template. Every outline heading must be specific to this query; if a heading could sit in any article, rewrite it.

```markdown
# Brief: <brief title>

**What I found:** <the opportunity, in one plain-English sentence>
**What matters most:** <the one thing this page must get right>
**What to do first:** <create / refresh / ... and the first move>

## Job type and recommended action
- Job type: <new blog post / refresh / landing page / comparison page / consolidation / internal-link update / snippet review>
- Recommended action: <...>

## Target keyword cluster
- Primary: <...>
- Secondary: <...>

## Target URL or proposed slug
- <URL or /slug>

## Reader and search intent
- Who is searching: <...>
- Job they are trying to do: <...>
- Funnel stage: <...>
- Intent: <informational / commercial / comparison / transactional / troubleshooting / local / template-tool / navigational / mixed>
- First useful answer must say: <...>
- This page must not become: <...>

## Business reason
- Supports: <product or conversion page>
- Why now: <evidence>

## SERP summary
- Dominant page types: <...>
- Common headings and sections: <...>
- Content gaps: <...>
- Table / tool / media / schema expectations: <...>
- Risks: <...>

## Title/meta policy
- <new page: title, H1 and meta direction / existing ranked page: preserve, or change with the data that justifies the risk>

## Required top-of-page structure
- TL;DR: <format required for this content type>
- Answer-first block: <what the 2-4 sentences must answer>

## Detailed outline
- H1: <...>
- H2: <heading> | purpose: <...> | must include: <examples, tables, screenshots, data points>
  - H3: <...>
- Required FAQ questions: <...>

## Product and factual constraints
- Approved claims: <...>
- Pricing/free-trial wording: <...>
- Platform support: <...>
- Privacy/security/processing claims: <...>
- Claims that require a source: <...>
- Claims to avoid: <...>
- Competitors that may / may not be named: <...>

## Links and conversion path
- Primary conversion page: <URL>
- Supporting internal links: <URL> | anchor guidance
- Required external links: <named tools, competitors, platforms, sources>

## Required assets
- <asset> | dimensions | storage | alt text | generated imagery allowed: yes / no

## Schema requirements
- <type(s) and what visible content they must match>

## QA acceptance criteria
- Gate: <minimum score or pass/fail rule>
- Critical facts that must be correct: <...>
- Structure checks: <...>
- Human-writing checks: <...>
- Link / asset / schema checks: <...>
- CMS / output constraints: <...>

## Risks and open questions
- <...>

## What I could not check
- <e.g. SERP not inspected live; product pricing not confirmed>
```

## Stop and flag if

Fail the brief, and say so instead of handing it on, if:

- It does not clearly choose create vs refresh.
- It ignores an existing page that already matches intent.
- It lacks an answer-first/TL;DR requirement.
- It gives generic outline headings that could fit any article.
- It omits product facts or prohibited claims.
- It omits internal-link and conversion-path guidance.
- It recommends changing title/meta on an existing ranked page without a risk note.
- It cannot be used by QA to judge pass/fail.

## Next step

- Hand the brief to `seo-blog-writer` (or `comparison-page-writer` for best X, X vs Y and alternatives pages), with the product facts and any existing page content.
- When the draft comes back, give the same brief to `seo-content-qa`; its acceptance criteria are the contract.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
